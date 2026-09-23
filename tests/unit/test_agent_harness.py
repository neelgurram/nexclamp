"""Milestone 9 agent-study harness: task files, isolation of exports, scoring, trial logs.

No agent is started by these tests. Tests that seed faults need nexclamp.mutations and
nexclamp.transforms and are skipped (with the import error) when either registry is missing.
Exports are made with ``allow_dirty=True`` (development-only) unless a test controls the Git
state, because the working tree under test is not necessarily committed.
"""

from __future__ import annotations

import dataclasses as dc
import datetime as dt
import difflib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

from nexclamp import units
from nexclamp.experiments import agent
from nexclamp.models import materialize
from nexclamp.provenance import ImmutableWriteError, sha256_file, sha256_json

REPO = Path(__file__).resolve().parents[2]
S = agent.LayerStatus
NE = S.NOT_EVALUATED
T05, T06 = "t05_unit_conversion", "t06_single_conductance_change"
RS_CELL = "model/NeuroML2/cells/RS/RS.cell.nml"
RS_NET = "model/NeuroML2/cells/RS/RS.net.nml"
RS_LEMS = "model/NeuroML2/cells/RS/LEMS_RS.xml"
HH_CELL = "model/examples/NML2_SingleCompHHCell.nml"
CLEAN = {"commit": "a" * 40, "tracked_tree_dirty": False, "dirty_paths": [], "clean": True}


@pytest.fixture(scope="module")
def policy():
    return agent.load_policy()


@pytest.fixture(scope="module")
def tasks(policy):
    return agent.load_all_tasks(policy=policy)


@pytest.fixture(scope="module")
def hidden(tasks):
    return {tid: agent.load_hidden_spec(tid) for tid in tasks}


def _replace(path: Path, old: str, new: str) -> None:
    data = path.read_bytes()
    assert data.count(old.encode()) == 1, f"{old!r} occurs {data.count(old.encode())} times in {path.name}"
    path.write_bytes(data.replace(old.encode(), new.encode()))


def _replace_all(path: Path, old: str, new: str) -> None:
    data = path.read_bytes()
    assert data.count(old.encode()) >= 1, f"{old!r} does not occur in {path.name}"
    path.write_bytes(data.replace(old.encode(), new.encode()))


def _set_attr(path: Path, tag: str, element_id: str, attr: str, value: str) -> None:
    """Set one attribute on the single <tag id=element_id> start tag, byte-preserving elsewhere."""
    text = path.read_bytes().decode("utf-8")
    tags = list(re.finditer(rf'<{tag}\b[^<>]*\bid="{re.escape(element_id)}"[^<>]*>', text))
    assert len(tags) == 1, (tag, element_id, len(tags))
    new_tag, n = re.subn(rf'(\s{attr}=")[^"]*(")', lambda m: m.group(1) + value + m.group(2), tags[0].group(0))
    assert n == 1, (tag, element_id, attr)
    path.write_bytes((text[:tags[0].start()] + new_tag + text[tags[0].end():]).encode("utf-8"))


def _export(tid, root, policy, models, name=None, **kw):
    name = name or f"{tid}-r01"
    kw.setdefault("allow_dirty", True)
    return agent.prepare_trial(tid, root / "trials" / name, private_dir=root / "private" / name, policy=policy,
                               models=models, **kw)


def _require_registries():
    try:
        agent.load_operator_registry("mutations")
        agent.load_operator_registry("transforms")
    except agent.OperatorsUnavailable as exc:
        pytest.skip(f"seeded-fault export needs nexclamp.mutations and nexclamp.transforms: {exc}")


# ----------------------------------------------------------------------------- task and hidden specs
def test_nine_tasks_cover_the_specification_task_types(tasks):
    assert len(tasks) == 9
    assert sorted(t.type for t in tasks.values()) == sorted(agent.TASK_TYPES)
    assert agent.TRANSFORMATION_TASK_TYPES | agent.ANSWER_ONLY_TASK_TYPES == set(agent.TASK_TYPES)


def test_seeds_and_oracles_use_architecture_operator_names(tasks, hidden):
    seeded = [t for t in tasks.values() if t.seeded_fault]
    assert {t.type for t in seeded} == set(agent.SEEDED_TASK_TYPES)
    for tid, t in tasks.items():
        for step in list(t.seeded_fault.steps if t.seeded_fault else ()) + list(hidden[tid].oracle_steps):
            assert step.operator in agent.REGISTRY_OPERATORS[step.registry]


def _bad_seed(op="flip_sign"):
    return {"description": "x", "steps": [{"registry": "mutations", "operator": op,
                                           "site": {"file": "NeuroML2/cells/RS/RS.cell.nml", "locator_contains": "IM_all"}}],
            "expected_after": [{"file": "NeuroML2/cells/RS/RS.cell.nml", "xpath": "//channelDensity[@id='IM_all']",
                                "attribute": "ionChannel", "value": "IM"}]}


@pytest.mark.parametrize("label, mutate", [
    ("unknown key", lambda d: d.update(extra=1)),
    ("unknown type", lambda d: d.update(type="write_a_paper")),
    ("unknown model", lambda d: d.update(base_model="no_such_model")),
    ("repair without seed", lambda d: d.update(type="repair_channel_reference")),
    ("seed on unseeded type", lambda d: d.update(seeded_fault=_bad_seed("scale_conductance"))),
    ("unknown operator", lambda d: d.update(type="repair_channel_reference", seeded_fault=_bad_seed())),
    ("operator without file edit", lambda d: d.update(type="repair_channel_reference",
                                                      seeded_fault=_bad_seed("recording_resolution"))),
    ("escaping path", lambda d: d.update(allowed_files=["model/../configs/study.yaml"])),
    ("outside model", lambda d: d.update(allowed_files=["configs/study.yaml"])),
    ("reserved answer file", lambda d: d.update(answer_files=["TASK.md"])),
    ("budget over policy", lambda d: d["budget"].update(max_turns=10_000)),
    ("wrong schema", lambda d: d.update(schema="other/1")),
])
def test_task_schema_rejects_invalid_definitions(label, mutate, tasks, policy, models, tmp_path):
    src = tasks[T06].task_dir
    d = yaml.safe_load((src / "task.yaml").read_text(encoding="utf-8"))
    shutil.copytree(src, tmp_path / T06)
    assert agent.load_task(T06, tmp_path, policy=policy, model_ids=models).task_id == T06   # the copy is valid
    mutate(d)
    (tmp_path / T06 / "task.yaml").write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(agent.TaskSpecError):
        agent.load_task(T06, tmp_path, policy=policy, model_ids=models)


def test_prompts_do_not_reveal_hidden_checks(tasks, hidden):
    for tid, t in tasks.items():
        assert agent.check_prompt_isolation(t) == [], tid
        text = t.prompt_path.read_text(encoding="utf-8")
        if t.seeded_fault is None or t.type == "restore_changed_stimulus":
            continue   # requested changes and documented protocols are part of the task statement
        assert t.seeded_fault.description not in text
        for a in hidden[tid].assertions:
            if a.get("expected") is not None and a.get("normalize") != "path":
                assert not re.search(rf"(?<![\w.]){re.escape(str(a['expected']))}(?![\w.])", text), (tid, a["expected"])
    assert agent.check_prompt_isolation(tasks[T06], "Use the hidden oracle with scale_conductance on P05_long_step.")


def test_public_checks_match_policy_and_reference_files(tasks, policy, models):
    for tid, t in tasks.items():
        pc = agent.load_public_checks(t.public_tests_dir)
        sim = pc["simulation"]
        assert sim["spike_time_abs_tol_ms"] == policy.public_checks["spike_time_abs_tol_ms"]
        assert sim["spike_threshold_mV"] == policy.public_checks["spike_threshold_mV"]
        snap = agent.REPO_ROOT / "models" / "raw" / models[t.base_model].snapshot
        for f in pc["validate"] + [sim["lems"]]:
            assert (snap / f.removeprefix("model/")).is_file(), (tid, f)
        assert (sim["reference"] is None) == (t.type == "change_one_conductance")


def test_hidden_specs_are_consistent_with_reference_models(tasks, hidden, models, tmp_path):
    for tid, h in hidden.items():
        t = tasks[tid]
        assert h.path.read_text(encoding="utf-8").startswith(f"# {agent.HIDDEN_SENTINEL}")
        root = tmp_path / tid
        materialize(models[t.base_model], root / "model")
        for f in list(h.validate_files) + [h.execution["lems"]]:
            assert (root / f).is_file(), (tid, f)
        if t.seeded_fault:          # every seeded site exists exactly once in the reference model
            for e in t.seeded_fault.expected_after:
                assert len(agent._select(agent.parse_xml(root / "model" / e.file), e.xpath)) == 1
        if h.oracle_base == "pristine" and not h.oracle_steps:
            # repair targets are the original values: value assertions must hold on the reference
            for a in h.assertions:
                if a["kind"] in ("quantity_equals", "attribute_equals"):
                    assert agent.evaluate_assertion(a, root, root).passed, (tid, a.get("name"))
    # t06: the requested value is exactly twice the reference value
    a = next(a for a in hidden[T06].assertions if a["kind"] == "quantity_equals")
    ref = agent._select(agent.parse_xml(tmp_path / T06 / RS_CELL), a["xpath"])[0].get(a["attribute"])
    assert units.parse(a["expected"]).si == pytest.approx(2 * units.parse(ref).si, rel=1e-12)
    # t09: the scored answer names the seeded element and attribute
    seed = tasks["t09_behaviour_diagnosis"].seeded_fault.expected_after[0]
    answers = {a["field"]: a["expected"] for a in hidden["t09_behaviour_diagnosis"].assertions}
    assert answers["file"] == seed.file and answers["attribute"] == seed.attribute
    assert f"@id='{answers['element_id']}'" in seed.xpath


def test_policy_documents_mandatory_exclusions_and_exports_no_framework(policy):
    # configs/agent_policy.yaml is frozen and names the harness module under the pre-rename package
    # path, so that one entry is matched against the accepted aliases instead of the current name.
    assert set(agent.MANDATORY_EXCLUDES) - set(agent.HARNESS_MODULE_PATHS) <= set(policy.extra_excludes)
    assert any(p in policy.extra_excludes for p in agent.HARNESS_MODULE_PATHS)
    assert policy.framework_include == ()
    assert policy.permissions["network"] == "denied"
    # ignore patterns cover scratch and caches only; simulator outputs are derived from the LEMS files
    assert not any(p.startswith("model/") for p in policy.ignore_paths)


# ----------------------------------------------------------------------------- export isolation
@pytest.mark.parametrize("rel", [
    ".git/HEAD", "sub/.git/config", "agent_study/hidden/t01_unit_repair/hidden_checks.yaml",
    "agent_study/tasks/t01_unit_repair/task.yaml", "docs/m0_evidence/tools/efel.verify.json", "results/raw/c/r/run.json",
    "work/tmp/a.txt", "data/splits/heldout/any_name.txt", "models/raw/X/PROVENANCE.json",
    "src/nexclamp/experiments/agent.py", "tests/unit/test_agent_harness.py", "configs/agent_policy.yaml",
    "src/nexclamp/__pycache__/x.cpython-312.pyc", "docs/agent_study_protocol.md",
])
def test_mandatory_exclusions(rel):
    assert agent.is_mandatory_excluded(rel)


def test_ordinary_files_are_not_excluded():
    for rel in ("README.md", "src/nexclamp/units.py", "docs/ARCHITECTURE.md", "data/model_manifest.csv"):
        assert not agent.is_mandatory_excluded(rel)


def test_export_tree_never_exports_hidden_material_even_if_everything_is_included(tmp_path):
    src = tmp_path / "repo"
    files = {".git/HEAD": "ref", "nested/.git/config": "x", "agent_study/hidden/t01_x/hidden_checks.yaml": "secret",
             "agent_study/tasks/t01_x/task.yaml": "seed", "docs/m0_evidence/a.json": "{}", "results/raw/r.json": "{}",
             "work/tmp/a.txt": "a", "configs/agent_policy.yaml": "p", "src/nexclamp/experiments/agent.py": "code",
             "tests/unit/test_x.py": "t", "README.md": "readme", "src/nexclamp/core.py": "core",
             "docs/ARCHITECTURE.md": "arch"}
    for rel, text in files.items():
        (src / rel).parent.mkdir(parents=True, exist_ok=True)
        (src / rel).write_text(text, encoding="utf-8")
    out = tmp_path / "out"
    copied = agent.export_tree(src, out, include=("**",))
    assert set(copied) == {"README.md", "src/nexclamp/core.py", "docs/ARCHITECTURE.md"}
    assert agent.list_files(out) == sorted(copied)
    for rel, digest in copied.items():
        assert sha256_file(out / rel) == digest == sha256_file(src / rel)
    assert agent.scan_for_leaks(out) == []


def test_leak_scan_flags_markers_git_and_forbidden_names(tmp_path):
    (tmp_path / "notes.md").write_text("see agent_study/hidden for details", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "task.yaml").write_text("x", encoding="utf-8")
    (tmp_path / "sub" / "x.txt").write_text(agent.HIDDEN_SENTINEL, encoding="utf-8")
    (tmp_path / ".git").mkdir()
    problems = " | ".join(agent.scan_for_leaks(tmp_path))
    for needle in ("notes.md", "sub/task.yaml", "sub/x.txt", ".git"):
        assert needle in problems


def test_prepare_trial_exports_only_public_material(tmp_path, tasks, policy, models):
    exp = _export(T06, tmp_path, policy, models)
    d = exp.trial_dir
    files = agent.list_files(d)
    assert {p.split("/")[0] for p in files} == {"TASK.md", "EXPORT_MANIFEST.json", "model", "public_tests"}
    assert (d / "TASK.md").read_bytes() == tasks[T06].prompt_path.read_bytes()
    assert {"public_tests/run_public_checks.py", "public_tests/public_checks.json"} <= set(files)
    assert not {Path(p).name for p in files} & {"task.yaml", "hidden_checks.yaml", "PROVENANCE.json", "export_record.json"}
    assert not any(".git" in p.split("/") for p in files)
    assert (d / "scratch").is_dir()
    assert agent.scan_for_leaks(d) == []
    assert agent.verify_export(d) == []
    assert not agent._inside(exp.private_dir, d.parent)          # the answer key is not reachable via ../
    record = agent.load_export_record(exp.private_dir)
    assert record["content_sha256"] == exp.content_sha256 and record["seed"] == []
    assert record["prompt_sha256"] == sha256_file(tasks[T06].prompt_path)
    assert record["public_tests_sha256"] == agent.public_tests_sha256(tasks[T06].public_tests_dir)
    assert record["export_id"] == d.name and isinstance(record["development_only"], bool)


def test_export_manifest_hashes_match_and_detect_changes(tmp_path, policy, models):
    d = _export(T06, tmp_path, policy, models).trial_dir
    manifest = json.loads((d / "EXPORT_MANIFEST.json").read_text(encoding="utf-8"))
    for rel, digest in manifest["files"].items():
        assert sha256_file(d / rel) == digest
    assert manifest["content_sha256"] == sha256_json(manifest["files"])
    _replace(d / RS_CELL, 'condDensity="0.07 mS_per_cm2"', 'condDensity="0.14 mS_per_cm2"')
    (d / "scratch" / "notes.txt").write_text("x", encoding="utf-8")
    assert agent.verify_export(d) == ["added: scratch/notes.txt", f"modified: {RS_CELL}"]


@pytest.mark.parametrize("tid", [T06, "t09_behaviour_diagnosis"])
def test_exported_timestamps_do_not_reveal_the_seeded_file(tid, tmp_path, policy, models):
    if tid != T06:
        _require_registries()
    exp = _export(tid, tmp_path, policy, models)
    assert dt.datetime.fromisoformat(agent.EXPORT_MTIME_UTC).timestamp() == agent.EXPORT_MTIME_EPOCH
    for root in (exp.trial_dir, exp.private_dir / "baseline"):
        times = agent.tree_mtimes(root)
        assert len(times) > 10 and set(times.values()) == {float(agent.EXPORT_MTIME_EPOCH)}, root
        assert agent.check_export_times(root) == []
    manifest = json.loads((exp.trial_dir / "EXPORT_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["timestamps_normalized_to_utc"] == agent.EXPORT_MTIME_UTC
    os.utime(exp.trial_dir / RS_CELL)                          # a transfer that stamps the current time
    assert agent.check_export_times(exp.trial_dir) == [f"mtime differs: {RS_CELL}"]


def test_prepare_trial_is_deterministic_and_refuses_unsafe_locations(tmp_path, policy, models):
    kw = dict(private_root=tmp_path / "private", policy=policy, models=models, allow_dirty=True)
    a = agent.prepare_trial(T05, tmp_path / "trials" / "a", **kw)
    b = agent.prepare_trial(T05, tmp_path / "trials" / "b", **kw)
    assert a.content_sha256 == b.content_sha256
    assert a.private_dir == (tmp_path / "private" / "a").resolve()           # default: <private_root>/<trial name>
    inside = REPO / "work" / "tmp" / "agent-study" / "inside_repo_trial"
    with pytest.raises(agent.AgentStudyError, match="outside the NeuroSem repository"):
        agent.prepare_trial(T05, inside, **kw)
    assert not inside.exists()
    with pytest.raises(FileExistsError):
        agent.prepare_trial(T05, tmp_path / "trials" / "a", **kw)
    unsafe = {
        "overlap": tmp_path / "trials" / "c" / "private",
        "sibling": tmp_path / "trials" / "c.private",
        "under sibling": tmp_path / "trials" / "records" / "c",
        "trial parent": tmp_path / "trials",
        "repository": REPO / "work" / "tmp" / "agent-study" / "private_c",
    }
    for label, private in unsafe.items():
        with pytest.raises(agent.AgentStudyError):
            agent.prepare_trial(T05, tmp_path / "trials" / "c", private_dir=private, policy=policy, models=models,
                                allow_dirty=True)
        assert not (tmp_path / "trials" / "c").exists(), label
    assert not (REPO / "work" / "tmp" / "agent-study" / "private_c").exists()
    # the dedicated private root inside the repository is the one allowed in-repo location
    agent.check_trial_locations(tmp_path / "trials" / "d", REPO.joinpath(*agent.PRIVATE_REL, "d"), REPO)


def test_prepare_trial_refuses_uncommitted_inputs(tmp_path, policy, models, monkeypatch):
    state = {**CLEAN, "clean": False, "dirty_paths": ["agent_study/tasks/t06_single_conductance_change/prompt.md"]}
    monkeypatch.setattr(agent, "source_state", lambda repo, paths: dict(state))
    with pytest.raises(agent.AgentStudyError, match="uncommitted"):
        _export(T06, tmp_path, policy, models, allow_dirty=False)
    assert not (tmp_path / "trials").exists()
    dev = _export(T06, tmp_path, policy, models, name="dev", allow_dirty=True)
    record = agent.load_export_record(dev.private_dir)
    assert dev.development_only and record["development_only"] and record["source_dirty_paths"] == state["dirty_paths"]
    monkeypatch.setattr(agent, "source_state", lambda repo, paths: dict(CLEAN))
    clean = _export(T06, tmp_path, policy, models, name="clean", allow_dirty=False)
    assert not clean.development_only and agent.load_export_record(clean.private_dir)["source_git_commit"] == "a" * 40


def test_source_state_treats_paths_outside_the_repository_as_uncommitted(tmp_path):
    state = agent.source_state(REPO, [tmp_path])
    assert state["clean"] is False and any("outside the repository" in p for p in state["dirty_paths"])


@dc.dataclass(frozen=True)
class _Site:
    operator: str
    file: str
    locator: str
    params: dict


class _FakeScale:
    """Registry stand-in with the operator protocol: sites carry precomputed changes."""

    name = "scale_conductance"

    def __init__(self, factors=(0.5, 2.0)):
        self.factors = tuple(factors)

    def sites(self, ws):
        return [_Site(self.name, "m.nml", "/neuroml/x[@id='a']",
                      {"factor": f, "changes": [{"attribute": "g", "old": "1", "new": str(f)}]}) for f in self.factors]

    def apply(self, ws, site):
        return [], {}, {}


def test_operator_adapter_selects_exact_sites_and_never_imposes_parameters(tmp_path, monkeypatch):
    monkeypatch.setattr(agent, "load_operator_registry", lambda registry: {"scale_conductance": _FakeScale()})
    ws = agent.Workspace(tmp_path, None)

    def step(params, args=None, file="m.nml"):
        return agent.OperatorStep("mutations", "scale_conductance", agent.SiteSelector(file, "@id='a'"), params, args or {})

    assert agent.apply_operator_step(ws, step({"factor": 2.0})).params["factor"] == 2.0
    assert agent.apply_operator_step(ws, step({"new": "0.5"})).params["factor"] == 0.5     # matched via recorded change
    with pytest.raises(agent.SeedError, match="available"):
        agent.apply_operator_step(ws, step({"factor": 0.1}))
    applied = agent.apply_operator_step(ws, step({"factor": 0.1}, {"factors": [0.1]}))
    assert applied.params["factor"] == 0.1 and applied.operator_args == {"factors": [0.1]}
    with pytest.raises(agent.SeedError, match="constructor"):
        agent.apply_operator_step(ws, step({"factor": 0.1}, {"bogus": 1}))
    with pytest.raises(agent.SeedError, match="no site"):
        agent.apply_operator_step(ws, step({}, file="other.nml"))


@pytest.mark.parametrize("tid", ["t01_unit_repair", "t02_stimulus_restore", "t07_channel_reference_repair",
                                 "t09_behaviour_diagnosis"])
def test_prepare_trial_applies_seeded_fault_by_operator_name(tid, tmp_path, tasks, policy, models):
    _require_registries()
    try:
        exp = _export(tid, tmp_path, policy, models)
    except agent.OperatorsUnavailable as exc:   # registry importable but incomplete (module still being built)
        pytest.skip(f"seeded-fault export needs the {tid} operators: {exc}")
    task = tasks[tid]
    for e in task.seeded_fault.expected_after:
        ok, msg = agent.check_expectation(exp.trial_dir / "model", e)
        assert ok, msg
    assert [s["operator"] for s in exp.seed] == [s.operator for s in task.seeded_fault.steps]
    pristine = materialize(models[task.base_model], tmp_path / "pristine").root
    changes = agent.semantic_diff(pristine, exp.trial_dir / "model")
    assert changes and {c.file for c in changes} <= {s.site.file for s in task.seeded_fault.steps}
    assert agent.scan_for_leaks(exp.trial_dir) == []
    # seeding is byte-minimal: exactly one line differs from the original, so formatting artefacts
    # of re-serialisation cannot point at the edited file
    for rel in {s.site.file for s in task.seeded_fault.steps}:
        old = (pristine / rel).read_bytes().decode("utf-8").splitlines()
        new = (exp.trial_dir / "model" / rel).read_bytes().decode("utf-8").splitlines()
        diff = [ln for ln in difflib.unified_diff(old, new, lineterm="", n=0)
                if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
        assert len(diff) == 2, diff
    unchanged = set(agent.list_files(pristine)) - {s.site.file for s in task.seeded_fault.steps}
    assert all((pristine / r).read_bytes() == (exp.trial_dir / "model" / r).read_bytes() for r in unchanged)


def test_minimal_attribute_rewrite_keeps_every_other_byte():
    original = (b'<?xml version="1.0" encoding="UTF-8"?>\n\n<neuroml xmlns="http://www.neuroml.org/schema/neuroml2"\n'
                b'    id="doc">\n    <notes></notes>\n    <channelDensity id="a" condDensity="1 mS_per_cm2"\n'
                b'        erev="-90 mV"/>\n    <channelDensity id="b" condDensity="1 mS_per_cm2" erev="-90 mV"/>\n'
                b'</neuroml>\n')
    reserialised = (b'<?xml version="1.0" encoding="UTF-8"?>\n<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" '
                    b'id="doc">\n    <notes/>\n    <channelDensity id="a" condDensity="1 mS_per_cm2" erev="-80 mV"/>\n'
                    b'    <channelDensity id="b" condDensity="1 mS_per_cm2" erev="-90 mV"/>\n</neuroml>\n')
    out = agent.minimal_attribute_rewrite(original, reserialised, "m.nml")
    assert out == original.replace(b'erev="-90 mV"/>\n    <channelDensity id="b"', b'erev="-80 mV"/>\n    <channelDensity id="b"')
    structural = reserialised.replace(b'    <channelDensity id="b" condDensity="1 mS_per_cm2" erev="-90 mV"/>\n', b"")
    with pytest.raises(agent.SeedError, match="attribute values only"):
        agent.minimal_attribute_rewrite(original, structural, "m.nml")


# ----------------------------------------------------------------------------- semantic diff and edit scope
DOC = """<?xml version="1.0" encoding="UTF-8"?>
<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" id="doc">
    <!-- a comment -->
    <ionChannel id="Kd" conductance="10pS" species="k"/>
    <cell id="c"><biophysicalProperties id="b"><membraneProperties>
        <channelDensity id="Kd_all" ionChannel="Kd" condDensity="5.0 mS_per_cm2" erev="-100 mV"/>
    </membraneProperties></biophysicalProperties></cell>
</neuroml>
"""


def _diff(tmp_path, before: str, after: str) -> list[agent.Change]:
    for name, text in (("before", before), ("after", after)):
        (tmp_path / name).mkdir(parents=True, exist_ok=True)
        (tmp_path / name / "m.nml").write_text(text, encoding="utf-8")
    return agent.semantic_diff(tmp_path / "before", tmp_path / "after")


def test_semantic_diff_ignores_formatting_comments_and_attribute_order(tmp_path):
    formatted = ('<neuroml id="doc" xmlns="http://www.neuroml.org/schema/neuroml2"><ionChannel species="k" id="Kd" '
                 'conductance="10pS"/>\n<cell id="c">\n  <biophysicalProperties id="b">\n<membraneProperties>'
                 '<channelDensity erev="-100 mV" condDensity="5.0 mS_per_cm2" ionChannel="Kd" id="Kd_all"/>'
                 '</membraneProperties></biophysicalProperties></cell></neuroml>')
    assert _diff(tmp_path, DOC, formatted) == []


def test_semantic_diff_sees_namespace_and_tail_text(tmp_path):
    swapped = DOC.replace('xmlns="http://www.neuroml.org/schema/neuroml2"', 'xmlns="http://example.org/other"')
    ns = _diff(tmp_path / "ns", DOC, swapped)
    assert [(c.kind, c.attribute, c.locator, c.new) for c in ns] == [
        ("attribute_changed", agent.NAMESPACE_ATTRIBUTE, "/neuroml", "http://example.org/other")]
    assert agent.classify_changes(ns, [], representation_only_is_unauthorized=False).unauthorized == ns
    stray = DOC.replace('species="k"/>', 'species="k"/>stray text')
    tail = _diff(tmp_path / "tail", DOC, stray)
    assert [(c.kind, c.attribute, c.new) for c in tail] == [("text_changed", agent.TAIL_ATTRIBUTE, "stray text")]


def test_ignore_patterns_and_declared_outputs_hide_only_new_files(tmp_path):
    lems = ('<Lems>\n  <Target component="sim1" reportFile="report.txt"/>\n  <Simulation id="sim1" length="1ms" '
            'step="0.01ms" target="n">\n    <OutputFile id="of" fileName="results/v.dat">'
            '<OutputColumn id="v" quantity="p/v"/></OutputFile>\n  </Simulation>\n</Lems>\n')
    before, after = tmp_path / "before", tmp_path / "after"
    for root in (before, after):
        (root / "model" / "sim").mkdir(parents=True)
        (root / "model" / "sim" / "LEMS_x.xml").write_text(lems, encoding="utf-8")
        (root / "model" / "sim" / "data.dat").write_text("1 2\n", encoding="utf-8")
        (root / "scratch").mkdir()
    assert {"model/sim/results/v.dat", "model/sim/report.txt", "results/v.dat"} <= agent.declared_output_paths([before])
    (after / "model" / "sim" / "results").mkdir()
    (after / "model" / "sim" / "results" / "v.dat").write_text("0 0\n", encoding="utf-8")   # simulator output
    (after / "model" / "sim" / "report.txt").write_text("r", encoding="utf-8")               # simulator output
    (after / "scratch" / "x.txt").write_text("s", encoding="utf-8")                          # scratch
    assert agent.semantic_diff(before, after, ("scratch/**",)) == []
    (after / "model" / "sim" / "data.dat").write_text("9 9\n", encoding="utf-8")            # exported file edited
    (after / "model" / "sim" / "inputs.dat").write_text("1\n", encoding="utf-8")
    (after / "model" / "x86_64").mkdir()
    (after / "model" / "x86_64" / "evil.nml").write_text("<neuroml/>", encoding="utf-8")
    kinds = {(c.kind, c.file) for c in agent.semantic_diff(before, after, ("scratch/**",))}
    assert kinds == {("file_modified", "model/sim/data.dat"), ("file_added", "model/sim/inputs.dat"),
                     ("file_added", "model/x86_64/evil.nml")}
    # even an ignore pattern that matches an exported file cannot hide its modification or removal
    kinds = {(c.kind, c.file) for c in agent.semantic_diff(before, after, ("scratch/**", "model/**/*.dat"))}
    assert kinds == {("file_modified", "model/sim/data.dat"), ("file_added", "model/x86_64/evil.nml")}
    (after / "model" / "sim" / "data.dat").unlink()
    assert ("file_removed", "model/sim/data.dat") in {(c.kind, c.file) for c in agent.semantic_diff(
        before, after, ("model/**/*.dat",))}
    patch = agent.make_patch(before, after, ("scratch/**", "model/**/*.dat"))
    assert "a/model/sim/data.dat" in patch and "report.txt" not in patch and "x86_64/evil.nml" in patch


def test_semantic_diff_reports_located_changes_and_rules_classify_them(tmp_path):
    after = (DOC.replace('erev="-100 mV"', 'erev="-90 mV"').replace('condDensity="5.0 mS_per_cm2"', 'condDensity="50 S_per_m2"')
             .replace('<ionChannel id="Kd"', '<include href="x.nml"/><ionChannel id="Kdr"'))
    changes = _diff(tmp_path, DOC, after)
    by_attr = {(c.kind, c.attribute): c for c in changes}
    erev = by_attr[("attribute_changed", "erev")]
    assert erev.locator.endswith("channelDensity[@id='Kd_all']") and erev.si_equal is False
    assert by_attr[("attribute_changed", "condDensity")].si_equal is True
    rename = by_attr[("attribute_changed", "id")]
    assert rename.locator == "/neuroml/ionChannel[@id='Kd']" and rename.after_locator == "/neuroml/ionChannel[@id='Kdr']"
    assert by_attr[("element_added", None)].after_locator == "/neuroml/include[1]"
    rules = [agent.PermittedChange("m.nml", ("attribute_changed",), r"channelDensity\[@id=.Kd_all.\]$", ("erev",))]
    res = agent.classify_changes(changes, rules)
    assert [c.attribute for c in res.permitted] == ["erev"]
    assert [c.attribute for c in res.representation_only] == ["condDensity"]
    assert {(c.kind, c.attribute) for c in res.unauthorized} == {("attribute_changed", "id"), ("element_added", None)}
    strict = agent.classify_changes(changes, rules, representation_only_is_unauthorized=True)
    assert len(strict.unauthorized) == 3


def test_edit_scope_and_patch_on_an_exported_trial(tmp_path, hidden, policy, models):
    exp = _export(T06, tmp_path, policy, models)
    d, base = exp.trial_dir, exp.private_dir / "baseline"
    rules = hidden[T06].permitted_changes

    def scope():
        return agent.classify_changes(agent.semantic_diff(base, d, policy.ignore_paths), rules)

    assert scope() == agent.EditScopeResult([], [], [])
    _replace(d / RS_CELL, 'condDensity="0.07 mS_per_cm2"', 'condDensity="0.14 mS_per_cm2"')
    (d / "model/NeuroML2/cells/RS/RS.dat").write_text("0 -0.07\n", encoding="utf-8")   # declared simulator output: ignored
    (d / "scratch" / "notes.txt").write_text("scratch", encoding="utf-8")               # scratch space: ignored
    res = scope()
    assert len(res.permitted) == 1 and res.unauthorized == []
    _replace(d / "model/NeuroML2/channels/IM/IM.channel.nml", 'conductance="10pS"', 'conductance="20pS"')
    _replace(d / "public_tests/public_checks.json", '"spike_time_abs_tol_ms": 1.0', '"spike_time_abs_tol_ms": 100.0')
    (d / "model/NeuroML2/cells/RS/inputs.dat").write_text("1\n", encoding="utf-8")      # not a declared output
    kinds = {(c.file, c.kind) for c in scope().unauthorized}
    assert kinds == {("model/NeuroML2/channels/IM/IM.channel.nml", "attribute_changed"),
                     ("public_tests/public_checks.json", "file_modified"),
                     ("model/NeuroML2/cells/RS/inputs.dat", "file_added")}
    patch = agent.make_patch(base, d, policy.ignore_paths)
    assert re.search(r'^-.*condDensity="0\.07 mS_per_cm2"', patch, re.M)
    assert re.search(r'^\+.*condDensity="0\.14 mS_per_cm2"', patch, re.M)
    assert "scratch/notes.txt" not in patch and "RS.dat" not in patch


# ----------------------------------------------------------------------------- hidden assertions
def test_quantity_assertions_accept_equivalent_spellings_and_reject_decimal_slips(tmp_path, hidden, policy, models):
    exp = _export(T06, tmp_path, policy, models)
    d, base = exp.trial_dir, exp.private_dir / "baseline"
    run = lambda: [agent.evaluate_assertion(a, d, base).passed for a in hidden[T06].assertions]  # noqa: E731
    assert run() == [False, True]
    _replace(d / RS_CELL, 'condDensity="0.07 mS_per_cm2"', 'condDensity="1.4 S_per_m2"')
    assert run() == [True, True]
    _replace(d / RS_CELL, 'condDensity="1.4 S_per_m2"', 'condDensity="0.014 S_per_cm2"')
    assert run() == [False, True]


def test_answer_assertions_normalize_paths(tmp_path, hidden):
    specs = hidden["t09_behaviour_diagnosis"].assertions
    run = lambda: [agent.evaluate_assertion(a, tmp_path, tmp_path).passed for a in specs]  # noqa: E731
    assert run() == [False, False, False]
    answer = tmp_path / "diagnosis.yaml"
    answer.write_text("file: .\\model\\NeuroML2\\cells\\RS\\RS.cell.nml\nelement_id: Kd_all\nattribute: erev\n"
                      "suspected_original_value: -100.0 mV\nexplanation: shifted K reversal\n", encoding="utf-8")
    assert run() == [True, True, True]
    answer.write_text("file: model/NeuroML2/cells/RS/RS.cell.nml\nelement_id: Kd_all\nattribute: condDensity\n",
                      encoding="utf-8")
    assert run() == [True, True, False]
    answer.write_text("file: [unclosed\n", encoding="utf-8")
    assert run() == [False, False, False]


def _refactor_hh_channels(model_root: Path) -> None:
    """A correct refactor: move each inline channel to examples/channels/<id>.channel.nml and include it."""
    cell = model_root / "examples" / "NML2_SingleCompHHCell.nml"
    text = cell.read_text(encoding="utf-8")
    (model_root / "examples" / "channels").mkdir()
    includes = []
    for m in re.finditer(r'<ionChannelHH id="(\w+)".*?</ionChannelHH>', text, re.S):
        (model_root / "examples" / "channels" / f"{m.group(1)}.channel.nml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" '
            f'id="{m.group(1)}_file">\n    {m.group(0)}\n</neuroml>\n', encoding="utf-8")
        includes.append(f'    <include href="channels/{m.group(1)}.channel.nml"/>')
    text = re.sub(r'<ionChannelHH id="\w+".*?</ionChannelHH>', "", text, flags=re.S)
    text = text.replace('id="NML2_SingleCompHHCell">', 'id="NML2_SingleCompHHCell">\n' + "\n".join(includes), 1)
    cell.write_text(text, encoding="utf-8")


def test_refactor_assertions_and_edit_rules(tmp_path, hidden, policy, models):
    tid = "t04_include_refactor"
    exp = _export(tid, tmp_path, policy, models)
    d, base = exp.trial_dir, exp.private_dir / "baseline"
    _refactor_hh_channels(d / "model")
    results = [agent.evaluate_assertion(a, d, base) for a in hidden[tid].assertions]
    assert all(r.passed for r in results), [r for r in results if not r.passed]
    res = agent.classify_changes(agent.semantic_diff(base, d, policy.ignore_paths), hidden[tid].permitted_changes)
    assert res.unauthorized == [] and len(res.permitted) == 9
    # a changed rate constant in a moved channel is caught by the include-resolved comparison
    _replace(d / "model/examples/channels/naChan.channel.nml", 'rate="4per_ms"', 'rate="5per_ms"')
    flat = next(a for a in hidden[tid].assertions if a["kind"] == "flattened_equivalent")
    assert not agent.evaluate_assertion(flat, d, base).passed


KD_CHANNEL = "model/NeuroML2/channels/Kd/Kd.channel.nml"


def _t03_rename(d: Path) -> None:
    _replace(d / KD_CHANNEL, '<ionChannel id="Kd"', '<ionChannel id="Kdr"')
    for cell in ("RS", "FS", "LTS", "IB"):
        _replace(d / f"model/NeuroML2/cells/{cell}/{cell}.cell.nml", 'ionChannel="Kd"', 'ionChannel="Kdr"')
        _replace_all(d / f"model/NeuroML2/cells/{cell}/LEMS_{cell}.xml", "/Kd_all/Kd/", "/Kd_all/Kdr/")


def _t01_extra(d: Path) -> None:
    _set_attr(d / HH_CELL, "channelDensity", "naChans", "condDensity", "120 mS_per_cm2")
    _set_attr(d / HH_CELL, "channelDensity", "kChans", "condDensity", "37 mS_per_cm2")


# (task, label, agent edit, all hidden assertions pass, unauthorized edit detected)
SOLUTIONS = [
    ("t01_unit_repair", "correct unit", lambda d: _set_attr(d / HH_CELL, "channelDensity", "naChans", "condDensity",
                                                            "120 mS_per_cm2"), True, False),
    ("t01_unit_repair", "decimal slip", lambda d: _set_attr(d / HH_CELL, "channelDensity", "naChans", "condDensity",
                                                            "12 mS_per_cm2"), False, False),
    ("t01_unit_repair", "also edits kChans", _t01_extra, True, True),
    ("t02_stimulus_restore", "amplitude restored", lambda d: _set_attr(d / RS_NET, "pulseGenerator", "Input_1",
                                                                       "amplitude", "0.75nA"), True, False),
    ("t02_stimulus_restore", "duration lengthened instead", lambda d: _set_attr(d / RS_NET, "pulseGenerator", "Input_1",
                                                                                "duration", "0.5s"), False, False),
    ("t03_channel_rename", "full rename", _t03_rename, True, False),
    ("t03_channel_rename", "channel file only", lambda d: _replace(d / KD_CHANNEL, '<ionChannel id="Kd"',
                                                                    '<ionChannel id="Kdr"'), False, False),
    ("t07_channel_reference_repair", "reference repaired", lambda d: _set_attr(d / RS_CELL, "channelDensity", "IM_all",
                                                                               "ionChannel", "IM"), True, False),
    ("t07_channel_reference_repair", "Display paths edited", lambda d: _replace_all(d / RS_LEMS, "/IM_all/IM/",
                                                                                   "/IM_all/Kd/"), False, True),
    ("t08_runtime_improvement", "larger step", lambda d: _set_attr(d / RS_LEMS, "Component", "sim1", "step", "0.005ms"),
     True, False),
    ("t08_runtime_improvement", "shorter simulation", lambda d: _set_attr(d / RS_LEMS, "Component", "sim1", "length",
                                                                          "400ms"), False, True),
]


@pytest.mark.parametrize("tid, label, edit, assertions_pass, unauthorized", SOLUTIONS,
                         ids=[f"{s[0]}-{s[1]}" for s in SOLUTIONS])
def test_hidden_evaluators_on_correct_and_wrong_solutions(tid, label, edit, assertions_pass, unauthorized, tmp_path,
                                                          tasks, hidden, policy, models):
    if tasks[tid].seeded_fault:
        _require_registries()
    exp = _export(tid, tmp_path, policy, models)
    d, base = exp.trial_dir, exp.private_dir / "baseline"
    edit(d)
    results = [agent.evaluate_assertion(a, d, base) for a in hidden[tid].assertions]
    assert all(r.passed for r in results) is assertions_pass, [r for r in results if not r.passed]
    changes = agent.semantic_diff(base, d, policy.ignore_paths)
    scope = agent.classify_changes(changes, hidden[tid].permitted_changes,
                                   representation_only_is_unauthorized=hidden[tid].representation_only_is_unauthorized)
    assert bool(scope.unauthorized) is unauthorized, scope.unauthorized
    assert any(c.file.startswith("model/") for c in changes)


# ----------------------------------------------------------------------------- aggregation
def _outcomes(**over):
    out = {layer: agent.LayerOutcome(layer, S.PASS) for layer in agent.LAYERS}
    out.update({layer: agent.LayerOutcome(layer, status) for layer, status in over.items()})
    return out


@pytest.mark.parametrize("over, basic, neuro, silent, category", [
    ({}, True, True, False, "success"),
    ({"hidden_assertions_pass": S.NOT_APPLICABLE}, True, True, False, "success"),
    ({"hidden_battery_passes": S.NOT_APPLICABLE}, True, True, None, "success"),   # no battery: says nothing
    ({"hidden_battery_passes": S.FAIL}, True, False, True, "hidden_battery_failure"),
    ({"schema_valid": S.FAIL, "executes": NE, "canonical_passes": NE, "hidden_battery_passes": NE},
     False, False, False, "structurally_invalid"),
    ({"executes": S.FAIL, "canonical_passes": NE, "hidden_battery_passes": NE}, False, False, False, "non_executable"),
    ({"canonical_passes": S.ERROR, "hidden_battery_passes": NE}, None, None, None, "indeterminate"),
    ({"hidden_battery_passes": S.ERROR}, True, None, None, "indeterminate"),
    ({"edit_scope": S.FAIL}, True, False, False, "unauthorized_edit"),
    ({"canonical_passes": S.FAIL, "hidden_battery_passes": NE, "edit_scope": S.FAIL}, False, False, False,
     "canonical_failure"),
    ({"canonical_passes": S.ERROR, "hidden_battery_passes": NE, "hidden_assertions_pass": S.FAIL}, None, False, None,
     "hidden_assertion_failure"),
])
def test_aggregate_on_synthetic_layer_outcomes(over, basic, neuro, silent, category):
    s = agent.aggregate("t00_synthetic", _outcomes(**over), trial_id="r1")
    assert (s.basic_pass, s.neurosem_pass, s.basic_pass_battery_fail, s.category) == (basic, neuro, silent, category)
    assert s.unauthorized_edits_detected is (over.get("edit_scope") is S.FAIL)
    assert s.first_failed_layer == next((n for n in agent.LAYERS if _outcomes(**over)[n].status is S.FAIL), None)


def test_aggregate_rejects_inconsistent_outcomes():
    with pytest.raises(ValueError, match="cascade"):
        agent.aggregate("t", _outcomes(schema_valid=S.FAIL))
    with pytest.raises(ValueError, match="cascade"):
        agent.aggregate("t", _outcomes(canonical_passes=S.ERROR))
    partial = _outcomes()
    del partial["edit_scope"]
    with pytest.raises(ValueError):
        agent.aggregate("t", partial)


def _score(trial_id, over=None, *, task_type="change_one_conductance", model_changed=True, provisional=False):
    return agent.aggregate("t", _outcomes(**(over or {})), trial_id=trial_id, provisional=provisional,
                           task_type=task_type, model_changed=model_changed)


def test_summarize_scores_reports_the_permitted_claim_fraction():
    battery_fail = {"hidden_battery_passes": S.FAIL}
    scores = [
        _score("a"),                                                               # determinate, not silent
        _score("b", battery_fail),                                                 # silent failure
        _score("c", {"canonical_passes": S.ERROR, "hidden_battery_passes": NE}),   # indeterminate
        _score("d", {"edit_scope": S.FAIL}),                                       # determinate, not silent
        _score("e", battery_fail),                                                 # invalid log
        _score("f", battery_fail, task_type="diagnose_behaviour_change"),          # answer-only task type
        _score("g", model_changed=False),                                          # no transformation made
        _score("h", battery_fail, provisional=True),                               # development score
        _score("i", {"hidden_battery_passes": S.NOT_APPLICABLE}),                  # battery not applicable
        _score("j", model_changed=None),                                           # edit scope unknown
    ]
    summary = agent.summarize_scores(scores, invalid_trials=["e"])
    assert summary["n_trials"] == 9 and summary["n_trials_excluded_invalid"] == 1 and summary["provisional_scores"] == 1
    claim = summary["basic_pass_battery_fail"]
    assert claim == {"count": 1, "denominator": 3, "fraction": pytest.approx(1 / 3), "excluded_provisional": 1,
                     "excluded_not_transformation_task": 1, "excluded_no_model_change": 1,
                     "excluded_model_change_unknown": 1, "excluded_indeterminate": 2}
    assert sum(v for k, v in claim.items() if k.startswith("excluded")) + claim["denominator"] == summary["n_trials"]
    assert summary["by_category"] == {"hidden_battery_failure": 3, "indeterminate": 1, "success": 4,
                                      "unauthorized_edit": 1}
    assert summary["layer_status_counts"]["canonical_passes"] == {"error": 1, "pass": 8}
    rows = summary["by_task_type"]
    assert rows["change_one_conductance"]["claim_denominator"] == 3 and rows["change_one_conductance"]["claim_count"] == 1
    assert rows["diagnose_behaviour_change"] == {"n_trials": 1, "provisional": 0, "basic_pass": 1, "neurosem_pass": 0,
                                                 "claim_count": 0, "claim_denominator": 0}


class _StubEvaluators(agent.DefaultEvaluators):
    """Real edit-scope and assertion evaluators; synthetic simulator layers."""

    def __init__(self):
        super().__init__(sim=None)
        self.calls = []

    def schema_valid(self, ctx):
        self.calls.append("schema_valid")
        return agent.LayerOutcome("schema_valid", S.PASS)

    def executes(self, ctx):
        self.calls.append("executes")
        raise RuntimeError("simulator crashed")

    def canonical_passes(self, ctx):
        self.calls.append("canonical_passes")
        return agent.LayerOutcome("canonical_passes", S.PASS)

    def hidden_battery_passes(self, ctx):
        self.calls.append("hidden_battery_passes")
        return agent.LayerOutcome("hidden_battery_passes", S.PASS)


def test_score_trial_cascade_and_error_handling(tmp_path, policy, models):
    exp = _export(T06, tmp_path, policy, models)
    ev = _StubEvaluators()
    score = agent.score_trial(T06, exp.trial_dir, agent.FrozenConfig.development(tmp_path / "results"),
                              private_dir=exp.private_dir, evaluators=ev, policy=policy, models=models)
    assert ev.calls == ["schema_valid", "executes"]
    assert score.layers["executes"].status is S.ERROR and "simulator crashed" in score.layers["executes"].details["reason"]
    assert score.layers["canonical_passes"].status is NE
    assert score.layers["edit_scope"].status is S.PASS
    assert score.layers["hidden_assertions_pass"].status is S.FAIL      # nothing was changed
    assert (score.basic_pass, score.neurosem_pass, score.category) == (None, False, "hidden_assertion_failure")
    assert score.provisional and score.export_content_sha256 == exp.content_sha256
    assert (score.task_type, score.model_changed) == ("change_one_conductance", False)
    path = tmp_path / "score.json"
    agent.write_score(score, path)
    assert json.loads(path.read_text(encoding="utf-8"))["layers"]["executes"]["status"] == "error"
    with pytest.raises(agent.AgentStudyError, match="no private export record"):
        agent.score_trial(T06, exp.trial_dir, agent.FrozenConfig.development(tmp_path / "results"),
                          private_root=tmp_path / "nowhere", evaluators=ev, policy=policy, models=models)


def _frozen_yaml(tmp_path: Path, drop: tuple[str, ...] = (), **over) -> Path:
    tol = tmp_path / "tolerances.csv"
    tol.write_text("model_id,protocol_id,feature\n", encoding="utf-8")
    d = {"schema": agent.FROZEN_SCHEMA, "campaign": "agent_frozen_test", "results_root": str(tmp_path / "results"),
         "dt_ms": 0.005, "timeout_s": 60.0, "tolerance_table": str(tol), "tolerance_table_sha256": sha256_file(tol),
         "tolerance_multiplier": 1.0, "selected_protocols": ["P01_step"], "reference_rheobase_nA": {"m": 0.1},
         "configs": {n: {"path": f"configs/{n}.yaml", "sha256": sha256_file(REPO / "configs" / f"{n}.yaml")}
                     for n in ("study", "features", "tolerances")},
         "evaluator_git_commit": "a" * 40, **agent.freeze_hashes()}
    d.update(over)
    for key in drop:
        del d[key]
    path = tmp_path / "frozen_agent_eval.yaml"
    path.write_text(yaml.safe_dump(d), encoding="utf-8")
    return path


def test_load_frozen_config_requires_every_hash_and_refuses_provisional(tmp_path, tasks):
    frozen = agent.load_frozen_config(_frozen_yaml(tmp_path))
    assert not frozen.provisional and frozen.task_sha256 == {t: s.sha256 for t, s in tasks.items()}
    assert frozen.policy_sha256 == agent.load_policy().sha256 and frozen.evaluator_git_commit == "a" * 40
    with pytest.raises(agent.FrozenConfigError, match="provisional"):
        agent.load_frozen_config(_frozen_yaml(tmp_path, provisional=True))
    for key in ("policy_sha256", "prompt_sha256", "public_tests_sha256", "evaluator_git_commit"):
        with pytest.raises(agent.FrozenConfigError, match="missing"):
            agent.load_frozen_config(_frozen_yaml(tmp_path, drop=(key,)))
    with pytest.raises(agent.FrozenConfigError, match="changed after freezing"):
        agent.load_frozen_config(_frozen_yaml(tmp_path, policy_sha256="0" * 64))
    # a prompt edited after freezing is refused
    tasks_copy = tmp_path / "tasks"
    shutil.copytree(agent.TASKS_DIR, tasks_copy, ignore=shutil.ignore_patterns("__pycache__"))
    (tasks_copy / T06 / "prompt.md").write_text("changed", encoding="utf-8")
    with pytest.raises(agent.FrozenConfigError, match=r"prompt_sha256\[t06"):
        agent.load_frozen_config(_frozen_yaml(tmp_path), tasks_root=tasks_copy)


def test_score_trial_needs_a_frozen_config_and_accepts_its_path(tmp_path, policy, models, monkeypatch):
    dirty = {**CLEAN, "clean": False, "dirty_paths": ["agent_study/tasks"]}
    monkeypatch.setattr(agent, "source_state", lambda repo, paths: dict(dirty))
    exp = _export(T06, tmp_path, policy, models)
    kw = dict(private_dir=exp.private_dir, evaluators=_StubEvaluators(), policy=policy, models=models)
    with pytest.raises(agent.FrozenConfigError, match="needs a frozen evaluation config"):
        agent.score_trial(T06, exp.trial_dir, None, **kw)
    with pytest.raises(agent.FrozenConfigError, match="provisional"):
        agent.score_trial(T06, exp.trial_dir, _frozen_yaml(tmp_path, provisional=True), **kw)
    with pytest.raises(agent.FrozenConfigError, match="development-only"):   # loaded from its path, then enforced
        agent.score_trial(T06, exp.trial_dir, str(_frozen_yaml(tmp_path)), **kw)


def test_frozen_scoring_checks_export_record_and_evaluator_state(tmp_path, policy, models, monkeypatch):
    state = dict(CLEAN)
    monkeypatch.setattr(agent, "source_state", lambda repo, paths: dict(state))
    exp = _export(T06, tmp_path, policy, models, allow_dirty=False)
    frozen = dc.replace(agent.FrozenConfig.development(tmp_path / "results"), provisional=False,
                        evaluator_git_commit="a" * 40, **agent.freeze_hashes())
    kw = dict(private_dir=exp.private_dir, evaluators=_StubEvaluators(), policy=policy, models=models)
    score = agent.score_trial(T06, exp.trial_dir, frozen, **kw)
    assert score.provisional is False and score.model_changed is False
    with pytest.raises(agent.FrozenConfigError, match="prompt: current file differs"):
        agent.score_trial(T06, exp.trial_dir, dc.replace(frozen, prompt_sha256={T06: "0" * 64}), **kw)
    with pytest.raises(agent.FrozenConfigError, match="exported from commit"):
        agent.score_trial(T06, exp.trial_dir, dc.replace(frozen, evaluator_git_commit="b" * 40), **kw)
    with pytest.raises(agent.FrozenConfigError, match="hidden spec"):
        agent.score_trial(T06, exp.trial_dir, dc.replace(frozen, hidden_spec_sha256={}), **kw)
    state.update(commit="b" * 40)                         # evaluator moved on after the freeze
    with pytest.raises(agent.FrozenConfigError, match="evaluator is at commit"):
        agent.score_trial(T06, exp.trial_dir, frozen, **kw)
    state.update(commit="a" * 40, clean=False, dirty_paths=["src/nexclamp/experiments/agent.py"])
    dev = _export(T06, tmp_path, policy, models, name="dev", allow_dirty=True)
    state.update(clean=True, dirty_paths=[])
    with pytest.raises(agent.FrozenConfigError, match="development-only"):
        agent.score_trial(T06, dev.trial_dir, frozen, **{**kw, "private_dir": dev.private_dir})


def test_frozen_config_rejects_changed_hidden_spec(hidden, tmp_path):
    h = hidden["t01_unit_repair"]
    frozen = dc.replace(agent.FrozenConfig.development(tmp_path), provisional=False,
                        hidden_spec_sha256={h.task_id: h.sha256})
    frozen.check_hidden_spec(h)
    assert agent.hidden_spec_hashes()[h.task_id] == h.sha256
    with pytest.raises(agent.FrozenConfigError):
        dc.replace(frozen, hidden_spec_sha256={h.task_id: "0" * 64}).check_hidden_spec(h)
    with pytest.raises(agent.FrozenConfigError):
        agent.FrozenConfig.development(tmp_path).tolerance_table_obj()


# ----------------------------------------------------------------------------- trial log
def _log(task, policy, **over):
    log = agent.TrialLog(
        trial_id=f"{task.task_id}-r01", task_id=task.task_id, claude_code_version="test-version",
        model_identifier="test-model", access_date="2026-09-13", permissions=dict(policy.permissions),
        permissions_sha256=policy.permissions_sha256, budget=dict(task.budget),
        prompt_sha256=sha256_file(task.prompt_path), transcript_path="transcript.jsonl", transcript_sha256="a" * 64,
        patch_path="patch.diff", patch_sha256="b" * 64, logs=[],
        costs={"usd": None, "input_tokens": None, "output_tokens": None, "source": "not reported by the tool"},
        human_interventions=[], export_content_sha256="c" * 64,
        session={"fresh_session": True, "resumed": False, "command_line": ["agent-cli"], "environment_id": "vm-01"},
        started_utc="2026-09-13T10:00:00+00:00", ended_utc="2026-09-13T10:40:00+00:00", termination="completed")
    return dc.replace(log, **over)


def test_trial_log_validation(tasks, policy):
    task = tasks[T06]
    record = {"content_sha256": "c" * 64}
    assert agent.validate_trial_log(_log(task, policy), task=task, policy=policy, export_record=record) == []
    cases = {
        "human intervention": dict(human_interventions=[{"utc": "2026-09-13T10:05:00+00:00", "action": "answered"}]),
        "prompt hash": dict(prompt_sha256="0" * 64),
        "budget": dict(budget={**task.budget, "max_turns": 5}),
        "clean export": dict(export_content_sha256="d" * 64),
        "fresh, non-resumed": dict(session={"fresh_session": True, "resumed": True, "command_line": [],
                                             "environment_id": "vm"}),
        "YYYY-MM-DD": dict(access_date="13/09/2026"),
        "real calendar date": dict(access_date="2026-13-45"),
        "logs must be": dict(logs=[{"path": "session.log"}]),
        "costs.source": dict(costs={"usd": 1.0, "input_tokens": 1, "output_tokens": 1}),
        "permissions": dict(permissions={**policy.permissions, "network": "allowed"}),
    }
    for needle, over in cases.items():
        problems = agent.validate_trial_log(_log(task, policy, **over), task=task, policy=policy, export_record=record)
        assert any(needle in p for p in problems), (needle, problems)


def test_trial_log_rehashes_files_and_checks_the_patch(tmp_path, tasks, policy, models):
    task = tasks[T06]
    exp = _export(T06, tmp_path, policy, models)
    _replace(exp.trial_dir / RS_CELL, 'condDensity="0.07 mS_per_cm2"', 'condDensity="0.14 mS_per_cm2"')
    rec = tmp_path / "record"
    rec.mkdir()
    (rec / "transcript.jsonl").write_bytes(b'{"role": "user"}\n')
    (rec / "session.log").write_bytes(b"log line\n")
    (rec / "patch.diff").write_bytes(agent.make_patch(exp.private_dir / "baseline", exp.trial_dir,
                                                      policy.ignore_paths).encode("utf-8"))
    log = _log(task, policy, transcript_sha256=sha256_file(rec / "transcript.jsonl"),
               patch_sha256=sha256_file(rec / "patch.diff"),
               logs=[{"path": "session.log", "sha256": sha256_file(rec / "session.log")}])
    kw = dict(task=task, policy=policy, root=rec, private_dir=exp.private_dir, trial_dir=exp.trial_dir)
    assert agent.validate_trial_log(log, **kw) == []
    (rec / "session.log").write_bytes(b"edited later\n")
    assert agent.validate_trial_log(log, **kw) == ["log session.log sha256 does not match the file"]
    (rec / "session.log").write_bytes(b"log line\n")
    (rec / "patch.diff").write_bytes(b"")
    problems = agent.validate_trial_log(log, **kw)
    assert "patch sha256 does not match the file" in problems
    assert "patch file differs from make_patch(baseline, trial)" in problems


def test_trial_log_is_written_once(tmp_path, tasks, policy):
    log = _log(tasks[T06], policy)
    path = tmp_path / "trial_log.json"
    agent.write_trial_log(log, path)
    assert agent.read_trial_log(path) == log
    agent.write_trial_log(log, path)                     # identical bytes: no-op
    with pytest.raises(ImmutableWriteError):
        agent.write_trial_log(dc.replace(log, notes="edited later"), path)


# ----------------------------------------------------------------------------- public checks
def _runner_module():
    spec = importlib.util.spec_from_file_location("run_public_checks", agent.PUBLIC_COMMON_DIR / agent.PUBLIC_RUNNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_public_runner_is_standalone_and_matches_reference_spike_detection(tmp_path):
    source = (agent.PUBLIC_COMMON_DIR / agent.PUBLIC_RUNNER).read_text(encoding="utf-8")
    assert "import nexclamp" not in source and "from nexclamp" not in source
    assert not any(m in source for m in agent.LEAK_MARKERS)
    runner = _runner_module()
    t = np.arange(0.0, 200.0, 0.01)
    v = -65.0 + 90.0 * np.maximum(0.0, np.sin(2 * np.pi * t / 23.0)) ** 8
    assert runner.spike_times(t.tolist(), v.tolist(), -20.0) == agent.spike_times(t.tolist(), v.tolist(), -20.0)
    dat = tmp_path / "out.dat"
    dat.write_text("0.0 -0.065\n0.0001 0.02\n", encoding="utf-8")
    t_ms, v_mV = runner.read_output(dat, 1)
    assert t_ms == pytest.approx([0.0, 0.1]) and v_mV == pytest.approx([-65.0, 20.0])


def _runner_env(sim):
    return {**os.environ, "NEUROSEM_JAVA": str(sim.java), "NEUROSEM_JNML_JAR": str(sim.jar)}


@pytest.mark.jnml
def test_public_runner_on_exported_hh_trial(sim, tmp_path, policy, models):
    ref = agent.TASKS_DIR / T05 / "public_tests" / "canonical_reference.json"
    if not ref.is_file():
        pytest.fail("public reference missing: run python agent_study/build_public_references.py")
    exp = _export(T05, tmp_path, policy, models)
    cmd = [sys.executable, str(exp.trial_dir / "public_tests" / agent.PUBLIC_RUNNER)]
    ok = subprocess.run(cmd, cwd=exp.trial_dir, capture_output=True, text=True, env=_runner_env(sim), timeout=600)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "ALL PUBLIC CHECKS PASSED" in ok.stdout
    base = exp.private_dir / "baseline"
    assert agent.semantic_diff(base, exp.trial_dir, policy.ignore_paths) == []     # checks ran in scratch/
    _replace(exp.trial_dir / HH_CELL, 'condDensity="120.0 mS_per_cm2"', 'condDensity="120.0 S_per_m2"')
    bad = subprocess.run(cmd, cwd=exp.trial_dir, capture_output=True, text=True, env=_runner_env(sim), timeout=600)
    assert bad.returncode == 1 and "[FAIL] canonical reference" in bad.stdout, bad.stdout


def _synthetic_canonical_tolerances(path: Path, model_id: str) -> Path:
    """A tiny tolerance table for the canonical protocol so that the real ``compare`` runs.

    Numeric tolerance 1e-3 (feature units): tighter than any physiological change, looser than
    floating-point noise between SI-equal spellings. Synthetic values for the harness test only.
    """
    from nexclamp.protocols.definitions import CANONICAL_FEATURES, CANONICAL_ID
    from nexclamp.validation.convergence import TolEntry, ToleranceTable

    entries = [TolEntry(model_id, CANONICAL_ID, f, "categorical" if f == "firing_regime" else "numeric", None, None, None,
                        "defined", "defined", 0.0, 0.0, 0.0, None if f == "firing_regime" else 1e-3, "abs_floor",
                        "synthetic harness test")
               for f in CANONICAL_FEATURES]
    ToleranceTable(entries).to_csv(path)
    return path


@pytest.mark.jnml
def test_score_trial_real_layers_on_hh_unit_conversion(sim, tmp_path, policy, models):
    tol = _synthetic_canonical_tolerances(tmp_path / "tol.csv", models[agent.load_task(T05, model_ids=models).base_model]
                                          .model_id)
    frozen = dc.replace(agent.FrozenConfig.development(tmp_path / "results"), tolerance_table=tol,
                        tolerance_table_sha256=sha256_file(tol))
    evaluators = agent.DefaultEvaluators(sim)
    good = _export(T05, tmp_path / "good", policy, models)
    _replace(good.trial_dir / HH_CELL, 'condDensity="3.0 S_per_m2"', 'condDensity="0.3 mS_per_cm2"')
    _replace(good.trial_dir / HH_CELL, 'condDensity="360 S_per_m2"', 'condDensity="36 mS_per_cm2"')
    s = agent.score_trial(T05, good.trial_dir, frozen, private_dir=good.private_dir, evaluators=evaluators,
                          policy=policy, models=models)
    status = {k: v.status for k, v in s.layers.items()}
    assert status["schema_valid"] is S.PASS and status["executes"] is S.PASS
    # the canonical layer runs the real feature comparison against the oracle: an SI-equal rewrite passes
    assert status["canonical_passes"] is S.PASS, s.layers["canonical_passes"].details
    # no frozen protocol selection: the battery cannot be scored, so the trial is indeterminate
    assert status["hidden_battery_passes"] is S.ERROR
    assert status["hidden_assertions_pass"] is S.PASS and status["edit_scope"] is S.PASS
    assert s.category == "indeterminate" and s.neurosem_pass is None and s.basic_pass is True
    assert s.basic_pass_battery_fail is None and s.model_changed is True
    assert agent.verify_export(good.trial_dir) == [f"modified: {HH_CELL}"]   # scoring ran in a copy
    assert not (good.trial_dir / "model" / "LEMSexamples" / "results").exists()

    slip = _export(T05, tmp_path / "slip", policy, models)
    _replace(slip.trial_dir / HH_CELL, 'condDensity="3.0 S_per_m2"', 'condDensity="0.3 mS_per_cm2"')
    _replace(slip.trial_dir / HH_CELL, 'condDensity="360 S_per_m2"', 'condDensity="3.6 mS_per_cm2"')
    s2 = agent.score_trial(T05, slip.trial_dir, frozen, private_dir=slip.private_dir, evaluators=evaluators,
                           policy=policy, models=models)
    assert s2.layers["schema_valid"].status is S.PASS and s2.layers["executes"].status is S.PASS
    assert s2.layers["canonical_passes"].status is S.FAIL and s2.layers["canonical_passes"].details["detections"]
    assert s2.layers["hidden_battery_passes"].status is NE
    assert s2.layers["hidden_assertions_pass"].status is S.FAIL and s2.layers["edit_scope"].status is S.FAIL
    assert (s2.basic_pass, s2.neurosem_pass, s2.unauthorized_edits_detected, s2.category) == (
        False, False, True, "canonical_failure")


@pytest.mark.jnml
def test_refactored_hh_model_validates_and_reproduces_reference(sim, tmp_path, policy, models):
    from nexclamp.simulators.base import OutputSpec

    exp = _export("t04_include_refactor", tmp_path, policy, models)
    _refactor_hh_channels(exp.trial_dir / "model")
    assert sim.validate([exp.trial_dir / HH_CELL]).valid is True
    res = sim.run_lems(exp.trial_dir / "model/LEMSexamples/LEMS_NML2_Ex5_DetCell.xml",
                       [OutputSpec("results/ex5_v.dat", {"v": 1})])
    assert res.status.value == "ok", res.message
    ref = json.loads((exp.trial_dir / "public_tests" / "canonical_reference.json").read_text(encoding="utf-8"))
    got = agent.spike_times(res.traces["v"].t_ms.tolist(), res.traces["v"].v_mV.tolist(), ref["spike_threshold_mV"])
    # same equations; only component order in the documents changed (allow float-summation noise)
    assert got == pytest.approx(ref["spike_times_ms"], abs=1e-3)
