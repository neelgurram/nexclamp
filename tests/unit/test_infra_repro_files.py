"""Structural checks of the reproducibility files (lock, CITATION.cff, Makefile, Dockerfile, CI, conda).

These do not replace building the Docker image or running CI (neither is possible on the
authoring machine); they catch drift between the files, e.g. a pyproject pin that the lock
no longer satisfies or a Makefile recipe indented with spaces.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest
import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

REPO_ROOT = Path(__file__).resolve().parents[2]


def _lock_pins() -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in (REPO_ROOT / "requirements.lock").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        assert re.fullmatch(r"[A-Za-z0-9_.\-]+==[A-Za-z0-9_.+\-]+", line), f"not an exact pin: {line!r}"
        name, version = line.split("==")
        key = canonicalize_name(name)
        assert key not in pins, f"duplicate pin for {name}"
        pins[key] = version
    return pins


def _pyproject() -> dict:
    return tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_lock_is_exact_and_excludes_the_project_itself():
    pins = _lock_pins()
    assert "neurosem" not in pins
    assert not re.search(r"^\s*-e\b", (REPO_ROOT / "requirements.lock").read_text(encoding="utf-8"), re.MULTILINE)
    assert len(pins) > 20


@pytest.mark.parametrize("group", ["dependencies", "dev"])
def test_lock_satisfies_pyproject_requirements(group):
    project = _pyproject()["project"]
    reqs = project["dependencies"] if group == "dependencies" else project["optional-dependencies"]["dev"]
    pins = _lock_pins()
    for spec in reqs:
        req = Requirement(spec)
        key = canonicalize_name(req.name)
        assert key in pins, f"{req.name} missing from requirements.lock"
        assert req.specifier.contains(pins[key], prereleases=True), f"lock pin {req.name}=={pins[key]} violates {spec}"


def test_citation_cff_core_fields():
    cff = yaml.safe_load((REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert {"cff-version", "message", "title", "authors"} <= set(cff)
    assert cff["cff-version"] == "1.2.0"
    assert cff["type"] == "software"
    assert cff["license"] == "BSD-3-Clause"
    assert str(cff["version"]) == _pyproject()["project"]["version"]
    assert {"given-names": "Neel", "family-names": "Gurram"} in cff["authors"]
    assert "doi" not in cff


MAKE_TARGETS = ["setup", "java", "test", "test-fast", "validate-models", "pilot", "reproduce-paper",
                "docker-build", "docker-test", "lint"]


def test_makefile_targets_and_tab_indented_recipes():
    text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    defined = set(re.findall(r"^([A-Za-z][\w-]*):(?!=)", text, re.MULTILINE))
    phony = set(re.search(r"^\.PHONY:(.*)$", text, re.MULTILINE).group(1).split())
    for target in MAKE_TARGETS:
        assert target in defined, f"missing target {target}"
        assert target in phony, f"{target} not declared .PHONY"
    in_recipe = False
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^[A-Za-z.][\w.-]*:(?!=)", line):
            in_recipe = True
            continue
        if not line.strip() or line.startswith("#"):
            in_recipe = in_recipe and bool(line.strip())
            continue
        if in_recipe and line[0] in " \t":
            assert line.startswith("\t"), f"Makefile line {n} is indented with spaces"
    for command in ("validate-models", "pilot --campaign", "reproduce-paper --campaign"):
        assert f"$(NEUROSEM) {command}" in text
    # setup must refuse a non-3.12 interpreter before and after creating the venv
    assert text.count("$(REQUIRE_PY312)") >= 2 and "sys.version_info[:2] == (3, 12)" in text


def test_dockerfile_pins_base_digest_java_and_runs_unprivileged():
    text = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert re.search(r"^FROM python:3\.12[\w.-]*@sha256:[0-9a-f]{64}$", text, re.MULTILINE)
    assert re.search(r"^ARG TEMURIN_RELEASE=jdk-21\.", text, re.MULTILINE)
    assert len(re.findall(r"^ARG TEMURIN_JRE_SHA256_\w+=[0-9a-f]{64}$", text, re.MULTILINE)) == 2
    assert "scripts/bootstrap_java.py" in text and "--expect-sha256" in text
    assert "pip install -r requirements.lock" in text
    users = re.findall(r"^USER (\S+)$", text, re.MULTILINE)
    assert users and users[-1] not in ("root", "0")
    assert re.search(r'^CMD \["python", "-m", "pytest"', text, re.MULTILINE)


def _dockerignore_patterns() -> list[str]:
    lines = (REPO_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]


def _docker_pattern_regex(pattern: str) -> re.Pattern[str]:
    """Docker's .dockerignore syntax: Go ``filepath.Match`` plus ``**`` for any number of directories."""
    pattern, out, i = pattern.strip("/"), "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        elif pattern[i] == "[":
            j = pattern.index("]", i)
            out, i = out + pattern[i:j + 1], j + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(out)


def dockerignored(rel_path: str, patterns: list[str]) -> bool:
    """True if Docker leaves ``rel_path`` (POSIX, repo-relative) out of the build context.

    A pattern that matches a parent directory excludes everything below it; ``!`` patterns
    re-include, and the last matching pattern wins.
    """
    parts = rel_path.split("/")
    ignored = False
    for raw in patterns:
        negate = raw.startswith("!")
        rx = _docker_pattern_regex(raw[1:] if negate else raw)
        if any(rx.fullmatch("/".join(parts[:k])) for k in range(1, len(parts) + 1)):
            ignored = not negate
    return ignored


# Repository files that tests read. The image's default command runs the whole suite, so none of
# these may be excluded from the Docker build context (.github once was, which failed the suite).
FILES_READ_BY_TESTS = ["Dockerfile", ".dockerignore", "Makefile", "environment.yml", "requirements.lock",
                       "pyproject.toml", "CITATION.cff", ".github/workflows/ci.yml", "scripts/bootstrap_java.py",
                       "configs/study.yaml", "configs/features.yaml", "configs/tolerances.yaml",
                       "data/model_manifest.csv"]


def test_dockerignore_excludes_local_state_but_keeps_test_inputs():
    patterns = _dockerignore_patterns()
    assert {".git", ".venv", ".tools", "work"} <= set(patterns)
    for local in (".git/HEAD", ".venv/Scripts/python.exe", ".tools/jdk-21.0.12.1+1/bin/java", "work/tmp/x.txt",
                  "src/neurosem/__pycache__/cli.cpython-312.pyc", "results/raw/pilot/r1/traces.npz",
                  "docs/handoff/spec.pdf"):
        assert dockerignored(local, patterns), f"{local} should not be copied into the image"
    for needed in FILES_READ_BY_TESTS:
        assert (REPO_ROOT / needed).is_file(), f"{needed} listed but missing"
        assert not dockerignored(needed, patterns), f"{needed} is read by tests but excluded from the Docker context"
    assert not dockerignored("src/neurosem/cli.py", patterns) and not dockerignored("tests/conftest.py", patterns)


def test_ci_workflow_structure():
    wf = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
    triggers = wf.get("on", wf.get(True))  # PyYAML reads the bare key `on` as boolean True
    assert "push" in triggers and "pull_request" in triggers
    tests, docker = wf["jobs"]["tests"], wf["jobs"]["docker"]
    assert tests["runs-on"] == "ubuntu-latest" and docker["runs-on"] == "ubuntu-latest"
    uses = {s["uses"].split("@")[0]: s for s in tests["steps"] if "uses" in s}
    assert uses["actions/setup-python"]["with"]["python-version"] == "3.12"
    assert uses["actions/setup-java"]["with"] == {"distribution": "temurin", "java-version": "21"}
    for step in tests["steps"] + docker["steps"]:
        if "uses" in step:
            assert re.fullmatch(r"[\w.-]+/[\w.-]+@v\d+", step["uses"]), f"action not pinned to a major: {step['uses']}"
    runs = "\n".join(s.get("run", "") for s in tests["steps"])
    assert "pip install -r requirements.lock" in runs and "pip install --no-deps -e ." in runs
    assert "pytest" in runs
    assert "docker build" in "\n".join(s.get("run", "") for s in docker["steps"])


def test_environment_yml_is_python312_plus_lock():
    env = yaml.safe_load((REPO_ROOT / "environment.yml").read_text(encoding="utf-8"))
    deps = env["dependencies"]
    assert "python=3.12" in deps and "pip=26.2.1" in deps  # same pip as the venv, Docker and CI routes
    pip_section = next(d["pip"] for d in deps if isinstance(d, dict))
    assert "-r requirements.lock" in pip_section
    # conda passes this section to pip as a requirements file, where pip 26.2.1 rejects --no-deps
    # ("no such option"), so the separate `--no-deps -e .` step of the other routes cannot be used.
    assert not any("--no-deps" in entry for entry in pip_section)
    assert "defaults" not in env["channels"]
