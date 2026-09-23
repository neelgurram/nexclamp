"""Final readiness testing, in one recorded sequence (Neel's 2026-09-17 instruction).

Steps, in order, all logged under ``results/audits/readiness/<stamp>/``:

1. the complete test suite from the beginning (no cached selection, no ``-x``);
2. the linter and the type checker;
3. a clean-environment install of the package and its pinned dependencies;
4. an end-to-end smoke test **in that clean environment**;
5. verification that the Pilot 1 raw data still matches its recorded hashes;
6. the command-line entry point and the canonical package import;
7. every log saved verbatim;
8. a report of passes, failures, skips, warnings and exact versions.

An earlier green run does not count once anything has changed: this records the commit and whether
the tree was dirty, and the Pilot 2 authorisation gate refuses a record that is not the current,
clean commit.

    python scripts/readiness.py                      # full sequence
    python scripts/readiness.py --skip-clean-env     # everything except steps 3 and 4
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp import config  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, sha256_file, utc_now  # noqa: E402

INPUT_PATHS = ("src", "scripts", "tests", "configs", "docs", "manifests", "data", "workflows",
               "pyproject.toml", "requirements.lock", "environment.yml", "Makefile", "Dockerfile")


def inputs_dirty() -> list[str]:
    """Uncommitted changes to the files that define a run (audit and result outputs are excluded).

    Running the readiness sequence and a campaign necessarily writes new files under ``results/``;
    those are outputs, not inputs. What must be committed is everything that decides what runs.
    """
    out = subprocess.run(["git", "status", "--porcelain", "--", *INPUT_PATHS], cwd=REPO_ROOT,
                         capture_output=True, text=True, check=False).stdout
    return [ln[3:] for ln in out.splitlines() if ln.strip()]


SUMMARY = re.compile(r"(\d+) (passed|failed|error|errors|skipped|xfailed|xpassed|warnings?|deselected)")


def run(cmd: list[str], log: Path, cwd: Path = REPO_ROOT, env: dict[str, str] | None = None) -> dict:
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, check=False)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(f"$ {' '.join(cmd)}\n\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n", encoding="utf-8")
    return {"command": " ".join(cmd), "returncode": proc.returncode, "duration_s": round(time.time() - t0, 1),
            "log": log.name, "tail": (proc.stdout or proc.stderr).strip().splitlines()[-3:]}


def parse_pytest(log: Path) -> dict[str, int]:
    text = log.read_text(encoding="utf-8")
    line = ""
    for ln in text.splitlines():
        if "passed" in ln or "failed" in ln or "error" in ln:
            line = ln if ("=====" in ln or not line) else line
    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "xfailed": 0, "xpassed": 0, "warnings": 0}
    for n, what in SUMMARY.findall(line):
        key = {"error": "errors", "errors": "errors", "warning": "warnings", "warnings": "warnings"}.get(what, what)
        if key in counts:
            counts[key] = int(n)
    counts["summary_line"] = line.strip()
    return counts


def versions() -> dict:
    out = {"python": sys.version.split()[0], "platform": platform.platform(), "executable": sys.executable}
    try:
        from nexclamp.simulators.jneuroml import JNeuroML

        sim = JNeuroML()
        out["simulator"] = sim.version_info() if sim.available() else {"available": False}
    except Exception as exc:  # recorded, never hidden
        out["simulator"] = {"error": str(exc)}
    pinned = {}
    for line in (REPO_ROOT / "requirements.lock").read_text(encoding="utf-8").splitlines():
        if "==" in line and not line.startswith("#"):
            name, ver = line.split("==", 1)
            pinned[name.strip()] = ver.split()[0].strip()
    out["pinned_requirements"] = pinned
    jdk = REPO_ROOT / ".tools" / "jdk_provenance.json"
    if jdk.is_file():
        out["jdk"] = json.loads(jdk.read_text(encoding="utf-8"))
    return out


def clean_env_install(out: Path, steps: dict) -> Path | None:
    venv = Path(os.environ.get("TEMP", "/tmp")) / f"neuraxis_readiness_{int(time.time())}"
    steps["3_clean_env_create"] = run([sys.executable, "-m", "venv", str(venv)], out / "logs" / "venv_create.log")
    py = venv / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    if not py.exists():
        return None
    steps["3_clean_env_pip"] = run([str(py), "-m", "pip", "install", "-q", "-r", "requirements.lock"],
                                   out / "logs" / "venv_pip.log")
    steps["3_clean_env_package"] = run([str(py), "-m", "pip", "install", "-q", "--no-deps", "-e", "."],
                                       out / "logs" / "venv_package.log")
    return py


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skip-clean-env", action="store_true", help="skip the clean-environment install and its smoke test")
    ap.add_argument("--campaign", default="pilot", help="campaign whose raw data must be unchanged")
    a = ap.parse_args(argv)
    stamp = utc_now().replace("-", "").replace(":", "")[:15] + "Z"
    out = config.results_dir() / "audits" / "readiness" / stamp
    (out / "logs").mkdir(parents=True, exist_ok=True)
    commit, dirty = git_state()
    steps: dict[str, dict] = {}
    t0 = time.time()

    # 1. the complete test suite, from the beginning
    suite_log = out / "logs" / "pytest.log"
    steps["1_test_suite"] = run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-rA", "--durations=15"],
                                suite_log)
    counts = parse_pytest(suite_log)
    steps["1_test_suite"].update(counts)

    # 2. lint and type check. Both are RECORDED BASELINES, not gates (R-15): their findings are
    # annotation gaps and style rules, counted here and tightened module by module after Pilot 2.
    steps["2_ruff"] = run([sys.executable, "-m", "ruff", "check", "src", "tests", "scripts"], out / "logs" / "ruff.log")
    steps["2_mypy"] = run([sys.executable, "-m", "mypy", "src"], out / "logs" / "mypy.log")
    for name, pattern in (("2_ruff", r"Found (\d+) errors"), ("2_mypy", r"Found (\d+) errors")):
        text = (out / "logs" / f"{name.split('_')[1]}.log").read_text(encoding="utf-8")
        m = re.search(pattern, text)
        steps[name].update({"findings": int(m.group(1)) if m else 0, "baseline_only": True,
                            "note": "recorded baseline, not a readiness gate (R-15)"})

    # 3 + 4. clean-environment install and end-to-end smoke test in it
    smoke_report = None
    if not a.skip_clean_env:
        py = clean_env_install(out, steps)
        if py is not None:
            smoke_out = out / "smoke"
            steps["4_smoke_test"] = run([str(py), "-m", "nexclamp", "smoke-test", "--out", str(smoke_out)],
                                        out / "logs" / "smoke.log")
            rep = smoke_out / "smoke_report.json"
            if rep.is_file():
                smoke_report = json.loads(rep.read_text(encoding="utf-8"))
                dest = config.results_dir() / "audits" / "smoke_test" / stamp
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copy2(rep, dest / "smoke_report.json")
                for name in ("pytest.log",):
                    if (smoke_out / name).is_file():
                        shutil.copy2(smoke_out / name, dest / name)
                steps["4_smoke_test"]["passed"] = bool(smoke_report.get("passed"))
                steps["4_smoke_test"]["copied_to"] = dest.relative_to(REPO_ROOT).as_posix()

    # 5. Pilot 1 raw data unchanged
    manifest = config.results_dir() / "processed" / a.campaign / "ARCHIVE_MANIFEST.sha256"
    raw_root = config.results_dir() / "raw" / a.campaign
    checked = bad = 0
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip() or not line.split()[1].startswith("raw/"):
                continue
            digest, rel = line.split()[0], line.split()[1]
            p = raw_root / rel[len("raw/"):]
            checked += 1
            bad += 0 if (p.is_file() and sha256_file(p) == digest) else 1
    steps["5_pilot1_raw_hashes"] = {"files_checked": checked, "mismatched_or_missing": bad,
                                    "manifest": manifest.relative_to(REPO_ROOT).as_posix() if manifest.is_file() else None,
                                    "returncode": 0 if checked and not bad else 1}

    # 6. CLI and canonical package import
    steps["6_cli_help"] = run([sys.executable, "-m", "nexclamp", "--help"], out / "logs" / "cli_help.log")
    steps["6_import"] = run([sys.executable, "-c",
                             "import nexclamp, nexclamp.experiments.campaign as c; print(nexclamp.__version__, c.__name__)"],
                            out / "logs" / "import.log")

    failed = [k for k, v in steps.items() if v.get("returncode", 0) != 0 and not v.get("baseline_only")]
    if smoke_report is not None and not smoke_report.get("passed"):
        failed.append("4_smoke_test")
    pending = inputs_dirty()
    record = {"created_utc": utc_now(), "stamp": stamp, "commit": commit, "dirty": dirty,
              "inputs_dirty": pending,
              "duration_s": round(time.time() - t0, 1), "steps": steps, "versions": versions(),
              "passed": counts.get("passed", 0), "failed": counts.get("failed", 0), "errors": counts.get("errors", 0),
              "skipped": counts.get("skipped", 0), "warnings": counts.get("warnings", 0),
              "suite_summary": counts.get("summary_line", ""), "failed_steps": sorted(set(failed)),
              "lint_findings": steps["2_ruff"].get("findings"), "type_findings": steps["2_mypy"].get("findings"),
              "all_steps_passed": not failed,
              "note": "Final readiness record. An earlier run does not count once anything changed."}
    (out / "readiness.json").write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8",
                                        newline="\n")
    for k, v in steps.items():
        ok = (v.get("returncode", 0) == 0 or v.get("baseline_only")) and v.get("passed", True)
        mark = "PASS" if ok else "FAIL"
        if v.get("baseline_only"):
            mark = f"BASELINE {v.get('findings', 0)} findings"
        print(f"[{mark}] {k}: {v.get('summary_line') or v.get('command') or v}")
    print(f"\nsuite: {counts.get('summary_line', 'no summary')}")
    print(f"commit {commit} (tree dirty: {dirty}; uncommitted inputs: {pending or 'none'}); record: {(out / 'readiness.json').relative_to(REPO_ROOT).as_posix()}")
    print("READY" if not failed else f"NOT READY: {sorted(set(failed))}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
