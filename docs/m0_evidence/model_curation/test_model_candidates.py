"""Tests for the model-curation deliverables (data/model_candidates.csv and models/candidates/).

Live checks on real files: the CSV schema matches the reference manifest, every pinned file still
hashes to what was downloaded and to the git blob of the pinned commit, the fail-closed licence gate
accepts the stored OSB licence texts and rejects altered ones, the XML include parser reproduces each
fetched closure exactly, cells are single-compartment, the sag screen refuses spike-contaminated
baselines, and (with Java) cell files validate, the Ih-block control runs, and a shipped harness
reproduces its OMV reference spike times.

Tests whose names start with ``test_evidence_`` only check that stored evidence files agree with each
other and with the CSV. They cannot detect a regression in a model or the simulator, and a timestamp
comparison inside files written by the same script cannot prove historical order.

This file sits outside ``testpaths = ["tests"]`` (pyproject.toml) because tests/ is owned by another
module, so a plain ``pytest`` run skips it. Run it explicitly from the repository root:
    .venv/Scripts/python -m pytest docs/m0_evidence/model_curation/test_model_candidates.py -q
(build note docs/build_notes/model-curation.md, item 6, asks for a move to tests/integration/).
"""

from __future__ import annotations

import csv
import hashlib
import json
import posixpath
import re
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml
from lxml import etree

from neurosem.models import MANIFEST_COLUMNS, Workspace, load_models
from neurosem.schemas import AnalysisWindow, ConcreteProtocol, ExecConfig, StimulusComponent
from neurosem.simulators.base import OutputSpec
from neurosem.simulators.jneuroml import JNeuroML

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import curate_candidates as cc  # noqa: E402
import verify_candidates as vc  # noqa: E402

REPO_ROOT = HERE.parents[2]
CSV_PATH = REPO_ROOT / "data" / "model_candidates.csv"
CANDIDATES_ROOT = REPO_ROOT / "models" / "candidates"
EVIDENCE = HERE / "license_evidence.json"
NML = "{http://www.neuroml.org/schema/neuroml2}"
MIT_GRANT = "Permission is hereby granted, free of charge, to any person obtaining a copy"


def _rows() -> list[dict]:
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _evidence() -> dict:
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def _provenance(snapshot: str) -> dict:
    return json.loads((CANDIDATES_ROOT / snapshot / "PROVENANCE.json").read_text(encoding="utf-8"))


def _sim() -> JNeuroML:
    sim = JNeuroML()
    if not sim.available():
        pytest.skip("Java or jNeuroML jar not available")
    return sim


# ----------------------------------------------------------------------------- CSV and snapshots
def test_csv_has_manifest_columns_and_candidate_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == MANIFEST_COLUMNS
    rows = _rows()
    assert rows, "no candidate rows"
    ids = [r["model_id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert not set(ids) & set(load_models().keys()), "candidate ids collide with the reference manifest"
    assert all(r["inclusion"] == "candidate" for r in rows)
    # load_models() is the core loader; the candidate file must be readable by it unchanged.
    assert set(load_models(CSV_PATH)) == set(ids)


def test_rows_point_at_existing_pinned_files():
    for r in _rows():
        snap = CANDIDATES_ROOT / r["snapshot"]
        assert (snap / r["cell_file"]).is_file(), r["model_id"]
        if r["harness_lems"]:
            assert (snap / r["harness_lems"]).is_file(), r["model_id"]
        prov = _provenance(r["snapshot"])
        assert r["commit"] == prov["commit"] and len(r["commit"]) == 40
        assert r["snapshot"].endswith("@" + r["commit"][:8])
        assert r["commit"] in r["license_url"]
        assert r["source_url"] == prov["repository"]


def test_snapshot_files_match_sha256_and_git_blob():
    for snapshot in sorted({r["snapshot"] for r in _rows()}):
        prov = _provenance(snapshot)
        assert prov["files"], snapshot
        for rel, meta in prov["files"].items():
            data = (CANDIDATES_ROOT / snapshot / rel).read_bytes()
            assert hashlib.sha256(data).hexdigest() == meta["sha256"], rel
            assert hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() == meta["git_blob_sha1"], rel
            assert meta["url"].startswith(f"https://raw.githubusercontent.com/{prov['repository'][19:]}/{prov['commit']}/")


def test_candidate_cells_are_single_compartment():
    for r in _rows():
        root = etree.parse(str(CANDIDATES_ROOT / r["snapshot"] / r["cell_file"])).getroot()
        cells = [c for tag in ("cell", "cell2CaPools") for c in root.iter(f"{NML}{tag}") if c.get("id") == r["cell_id"]]
        assert len(cells) == 1, r["model_id"]
        assert len(cells[0].findall(f"{NML}morphology/{NML}segment")) == 1, r["model_id"]


# ----------------------------------------------------------------------------- licence gate
def test_license_gate_accepts_stored_osb_licence_texts():
    """The current fail-closed gate, re-applied to each LICENSE text retrieved at the pinned commit,
    reaches the stored verdict (same directory exceptions), so the fetch-stage recheck passes."""
    for e in _evidence()["sources"]:
        v = cc.license_verdict(e["license_at_commit_api"]["text"], e["commit_api"]["sha"] == e["sha"])
        assert v["license_verified"] is True, (e["snapshot"], v["review_reasons"])
        assert v["excluded_directories"] == e["license_verdict"]["excluded_directories"], e["snapshot"]


def _mit_text() -> str:
    return next(e for e in _evidence()["sources"] if e["snapshot"].startswith("PyloricNetwork@"))[
        "license_at_commit_api"]["text"]


@pytest.mark.parametrize("name, build, verified, dirs", [
    ("exception sentence ends the preamble at a line end",
     lambda mit: "The following license applies to all software in this repository apart from that in directory XPP.\n"
                 + mit, True, ["XPP"]),
    ("exception sentence at end of text, no MIT body",
     lambda mit: "The following license applies to all software in this repository apart from that in directory XPP.",
     False, ["XPP"]),
    ("'except' wording the regex does not parse",
     lambda mit: "This license applies to everything except the directory NEURON. Code\n" + mit, False, []),
    ("unknown preamble", lambda mit: "Some other terms apply to parts of this repository.\n" + mit, False, []),
    ("restriction appended after the disclaimer", lambda mit: mit + "\nNon-commercial use only.\n", False, []),
    ("MIT grant removed", lambda mit: mit.replace(MIT_GRANT, "Permission is granted to some people"), False, []),
])
def test_license_gate_fails_closed(name, build, verified, dirs):
    v = cc.license_verdict(build(_mit_text()))
    assert v["license_verified"] is verified, (name, v["review_reasons"])
    assert v["excluded_directories"] == dirs, name
    if not verified:
        assert v["review_reasons"] and v["spdx_for_candidate_files"] is None, name


# ----------------------------------------------------------------------------- include closure
@pytest.mark.parametrize("xml, expected", [
    (b'<neuroml xmlns="http://www.neuroml.org/schema/neuroml2"><include href="a.nml"/></neuroml>', ["a.nml"]),
    (b"<neuroml><include href='b.nml'/></neuroml>", ["b.nml"]),
    (b'<Lems><Include file="c.xml"/></Lems>', ["c.xml"]),
    (b'<neuroml><!-- <include href="commented.nml"/> --></neuroml>', []),
    (b'<neuroml><include href="http://example.org/remote.nml"/></neuroml>', []),
])
def test_xml_includes_parser(xml, expected):
    assert cc.xml_includes(xml, "probe.nml") == expected


def test_xml_includes_rejects_unparseable_file():
    with pytest.raises(SystemExit):
        cc.xml_includes(b'<neuroml><include href="a.nml"></neuroml>', "broken.nml")


def test_fetched_snapshots_equal_their_xml_include_closure():
    """Recomputing each closure from the pinned local files with the XML parser gives exactly the
    fetched file set: nothing missing, and no file pulled in only by a commented-out include."""
    for src in cc.SOURCES:
        snap = cc.snapshot_name(src["repo"], src["sha"])
        root = CANDIDATES_ROOT / snap
        prov = _provenance(snap)
        queue, seen, builtin = list(src["entries"]), set(), set()
        while queue:
            rel = posixpath.normpath(queue.pop(0))
            if rel in seen or rel in builtin:
                continue
            if not (root / rel).is_file():
                assert posixpath.basename(rel) in cc.BUILTIN_BASENAMES, (snap, rel)
                builtin.add(rel)
                continue
            seen.add(rel)
            if rel.endswith((".nml", ".xml")):
                queue += [posixpath.join(posixpath.dirname(rel), i) for i in cc.xml_includes((root / rel).read_bytes(), rel)]
        assert seen == set(prov["files"]), snap
        assert sorted(builtin) == prov["builtin_includes_not_fetched"], snap


# ----------------------------------------------------------------------------- sag screen
def _step_trace(pre_spike_at_ms: float | None) -> tuple[np.ndarray, np.ndarray]:
    """Baseline -60 mV; a 500 ms step from 300 ms whose trough (about -106 mV, near +77 ms) recovers
    towards about -88 mV, i.e. a sag shape with the trough well inside the late window."""
    t = np.arange(0.0, 1000.0, 0.1)
    v = np.full_like(t, -60.0)
    s = (t >= 300.0) & (t < 800.0)
    x = t[s] - 300.0
    v[s] = -80.0 - 37.5 * (np.exp(-x / 300.0) - np.exp(-x / 30.0))
    if pre_spike_at_ms is not None:
        sp = (t >= pre_spike_at_ms) & (t < pre_spike_at_ms + 1.0)
        v[sp] = 30.0
    return t, v


def test_sag_ratio_defined_for_clean_baseline():
    t, v = _step_trace(None)
    m = vc.subthreshold_metrics(t, v, 300.0, 800.0, 200.0)
    expected = (m["steady_mV"] - m["min_mV"]) / (-60.0 - m["min_mV"])
    assert m["pre_window_spikes"] == 0 and m["sag_ratio_undefined_reasons"] == []
    assert m["sag_ratio"] == pytest.approx(expected, abs=1e-3)
    assert m["recovery_late_mV"] == pytest.approx(m["steady_mV"] - m["min_late_mV"], abs=1e-3)


def test_sag_ratio_undefined_when_baseline_window_contains_a_spike():
    t, v = _step_trace(pre_spike_at_ms=280.0)
    m = vc.subthreshold_metrics(t, v, 300.0, 800.0, 200.0)
    assert m["pre_window_spikes"] == 1
    assert m["sag_ratio"] is None and m["sag_ratio_late"] is None
    assert any("pre-step" in r for r in m["sag_ratio_undefined_reasons"])
    assert m["recovery_late_mV"] is not None       # baseline-free quantity stays defined


# ----------------------------------------------------------------------------- Ih block
def test_block_ih_zeroes_only_the_h_density(tmp_path):
    snap = "GranCellLayer@cee86047"
    cell_rel = "NeuroML2/Golgi_98.cell.nml"
    shutil.copytree(CANDIDATES_ROOT / snap, tmp_path / "g")
    before = vc.structure(CANDIDATES_ROOT / snap / cell_rel, "Golgi_98")["channels"]
    changed = vc.block_ih(tmp_path / "g" / cell_rel, "Golgi_98")
    after = vc.structure(tmp_path / "g" / cell_rel, "Golgi_98")["channels"]
    assert [c["id"] for c in changed] == ["Golgi_H_CML_all"]
    assert changed[0]["condDensity_original"] == "0.171496 mS_per_cm2"
    assert changed[0]["condDensity_blocked"] == "0 mS_per_cm2"
    for b, a in zip(before, after, strict=True):
        assert a["condDensity"] == ("0 mS_per_cm2" if b["ion"] == "h" else b["condDensity"]), b["id"]
    # the pristine snapshot is untouched
    assert vc.structure(CANDIDATES_ROOT / snap / cell_rel, "Golgi_98")["channels"] == before
    # a cell without an h density is left alone
    shutil.copytree(CANDIDATES_ROOT / "SmithEtAl2013-L23DendriticSpikes@179c596e", tmp_path / "s")
    assert vc.block_ih(tmp_path / "s" / "NeuroML2/singleCompAllChans.cell.nml", "cell") == []


@pytest.mark.jnml
def test_ih_block_deepens_golgi_hyperpolarisation(tmp_path):
    """-0.1 nA for 300 ms at dt 0.01 ms (dt 0.025 ms aborts jLEMS on this step, build note item 7):
    removing Ih must leave the Golgi cell markedly more hyperpolarised at the end of the step."""
    sim = _sim()
    c = next(x for x in vc.CANDIDATES if x.model_id == "maex1998_golgi")
    proto = ConcreteProtocol("H01", "step", (StimulusComponent("pulse", 100.0, 300.0, -0.1),), 450.0,
                             AnalysisWindow(100.0, 400.0), ())
    steady = {}
    for label in ("control", "blocked"):
        shutil.copytree(CANDIDATES_ROOT / c.snapshot, tmp_path / label, ignore=shutil.ignore_patterns("PROVENANCE.json"))
        if label == "blocked":
            assert vc.block_ih(tmp_path / label / c.cell_file, c.cell_id)
        ws = Workspace(tmp_path / label, vc.model_record(c, c.cell_file, c.cell_id))
        metrics, _ = vc.run_battery(sim, ws, [proto], ExecConfig(dt_ms=0.01), "ihtest", [])
        assert metrics["H01"]["status"] == "ok", metrics["H01"]
        steady[label] = metrics["H01"]["steady_mV"]
    assert steady["blocked"] < steady["control"] - 5.0, steady


# ----------------------------------------------------------------------------- simulator
@pytest.mark.jnml
def test_candidate_cell_files_validate_with_jnml():
    sim = _sim()
    files = sorted({CANDIDATES_ROOT / r["snapshot"] / r["cell_file"] for r in _rows()})
    res = sim.validate(files)
    assert res.valid is True, res.messages


@pytest.mark.jnml
def test_shipped_migliore_harness_reproduces_omv_reference(tmp_path):
    """100 ms at dt 0.01 ms: both soma cells fire the spikes their OMV reference records."""
    sim = _sim()
    snap = "MiglioreEtAl14_OlfactoryBulb3D@eaad1c8f"
    ws = tmp_path / "mig"
    shutil.copytree(CANDIDATES_ROOT / snap, ws)
    test_dir = ws / "NeuroML2" / "Channels" / "test"
    res = sim.run_lems(test_dir / "LEMS_OlfactoryTest_12.xml",
                       [OutputSpec("CG_MT_soma_0.0.dat", {"mt": 1}), OutputSpec("CG_GC_soma_0.0.dat", {"gc": 1})],
                       timeout_s=600)
    assert res.status.value == "ok", res.message
    mep = yaml.safe_load((test_dir / ".test.12.mep").read_text(encoding="utf-8"))["experiments"]
    for name in ("mt", "gc"):
        tr = res.traces[name]
        above = tr.v_mV >= 0.0
        idx = np.flatnonzero(~above[:-1] & above[1:])
        observed = tr.t_ms[idx]
        expected = np.asarray(mep[name]["expected"]["spike times"])
        assert observed.size == expected.size, (name, observed, expected)
        assert np.max(np.abs(observed - expected)) < 1.0, (name, observed, expected)


# ----------------------------------------------------------------------------- evidence consistency
def test_evidence_license_recorded_before_download():
    """Consistency of stored evidence (not proof of historical order): verified licence, matching
    commit, shipped LICENSE equals the checked text, download stamp not earlier than evidence stamp,
    and no snapshot exists for an unlicensed repository."""
    ev = {e["snapshot"]: e for e in _evidence()["sources"]}
    for snapshot in sorted({r["snapshot"] for r in _rows()}):
        e = ev[snapshot]
        assert e["license_verdict"]["license_verified"] is True
        assert e["commit_api"]["sha"] == _provenance(snapshot)["commit"]
        assert MIT_GRANT in e["license_at_commit_api"]["text"]
        assert _provenance(snapshot)["downloaded_utc"] >= e["retrieved_utc"]
        shipped = (CANDIDATES_ROOT / snapshot / "LICENSE").read_text(encoding="utf-8")
        assert shipped.replace("\r\n", "\n") == e["license_at_commit_api"]["text"].replace("\r\n", "\n")
    for s in _evidence()["screened_no_license"]:
        assert not (CANDIDATES_ROOT / f"{s['repo'].split('/')[1]}@{s['sha'][:8]}").exists()


def test_evidence_citation_dois_come_from_crossref_records():
    ev = {e["snapshot"]: e for e in _evidence()["sources"]}
    for r in _rows():
        dois = [p["record"]["DOI"].lower() for p in ev[r["snapshot"]]["papers_crossref"]]
        assert any(f"doi:{d}" in r["citation"].lower() for d in dois), r["model_id"]


def _verification() -> dict:
    return json.loads((HERE / "verification.json").read_text(encoding="utf-8"))


def test_evidence_verification_json_is_one_code_state_and_covers_candidates():
    """Stored-record consistency only: every candidate has a record from a single run and code state,
    and an Ih-block control exists exactly for the cells with an ion="h" density."""
    doc = _verification()
    ver = doc["models"]
    recs = [ver[r["model_id"]] for r in _rows()]
    assert len({rec["run_id"] for rec in recs}) == 1
    assert len({rec["code_state_id"] for rec in recs}) == 1
    run = doc["runs"][recs[0]["run_id"]]
    assert run["code_state"]["state_id"] == recs[0]["code_state_id"]
    assert run["code_state_changed_during_run"] is False
    # The stored numbers must come from the verification script as it is now. Core modules are owned
    # elsewhere and may move on; drift there is reported as a warning (re-run before inclusion decisions).
    recorded = run["code_state"]["files_sha256"]
    script = "docs/m0_evidence/model_curation/verify_candidates.py"
    assert hashlib.sha256((REPO_ROOT / script).read_bytes()).hexdigest() == recorded[script]
    drift = [rel for rel, h in recorded.items() if hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest() != h]
    if drift:
        import warnings
        warnings.warn(f"core files changed since verification run {recs[0]['run_id']}: {drift}", stacklevel=1)
    for r, rec in zip(_rows(), recs, strict=True):
        assert rec["validate_cell"]["valid"] is True
        assert rec["structure"]["single_compartment"] is True
        assert rec["harness"]["status"] in ("ok", "not_shipped")
        has_h = any(ch["ion"] == "h" for ch in vc.structure(CANDIDATES_ROOT / r["snapshot"] / r["cell_file"],
                                                            r["cell_id"])["channels"])
        assert (rec["probes"].get("ih_block") is not None) == has_h, r["model_id"]


def test_evidence_csv_sag_numbers_exist_in_verification_json():
    """Every sag ratio quoted in the CSV (written 'sag ratio 0.24' or 'sag ratio (late) 0.24') must be a
    defined value in that model's stored battery or Ih-block records, so no untraceable number is quoted."""
    ver = _verification()["models"]
    pat = re.compile(r"sag ratio(?: \(late\))? (-?\d+\.\d+)")
    for r in _rows():
        quoted = pat.findall(r["expected_behavior"])
        if not quoted:
            continue
        probes = ver[r["model_id"]]["probes"]
        blocks = [probes["battery"]] + ([probes["ih_block"]["battery"]] if probes.get("ih_block") else [])
        values = {round(m[k], 2) for b in blocks for m in b.values()
                  for k in ("sag_ratio", "sag_ratio_late") if isinstance(m.get(k), float)}
        for q in quoted:
            assert round(float(q), 2) in values, (r["model_id"], q, sorted(values))
