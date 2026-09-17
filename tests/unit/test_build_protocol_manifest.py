"""Tests for scripts/build_protocol_manifest.py and the committed data/protocol_manifest.csv."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from neuraxis import config
from neuraxis.protocols.definitions import DEFAULT_TEMPLATES, ProtocolTemplate, batched, templates_from_config

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "build_protocol_manifest.py"
MANIFEST = REPO / "data" / "protocol_manifest.csv"
ARCH_COLUMNS = "protocol_id,kind,description,params_json,features,implemented,not_implemented_reason"


@pytest.fixture(scope="module")
def bpm():
    spec = importlib.util.spec_from_file_location("build_protocol_manifest", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def templates():
    return templates_from_config(config.study().get("protocols"))


def test_columns_match_architecture(bpm):
    assert ",".join(bpm.COLUMNS) == ARCH_COLUMNS
    header = bpm.manifest_text().splitlines()[0]
    assert header == ARCH_COLUMNS


def test_one_row_per_template_in_config_order(bpm, templates):
    rows = bpm.parse_csv(bpm.manifest_text())
    assert [r["protocol_id"] for r in rows] == [t.protocol_id for t in templates]


def test_rows_round_trip_template_content(bpm, templates):
    rows = {r["protocol_id"]: r for r in bpm.parse_csv(bpm.manifest_text())}
    for t in templates:
        r = rows[t.protocol_id]
        assert r["kind"] == t.kind
        assert r["description"] == t.description
        assert json.loads(r["params_json"]) == dict(t.params)
        assert tuple(filter(None, r["features"].split(";"))) == t.features
        assert r["implemented"] == ("true" if t.implemented else "false")
        assert r["not_implemented_reason"] == t.not_implemented_reason


def test_deferred_protocols_are_marked_with_reason(bpm):
    rows = {r["protocol_id"]: r for r in bpm.parse_csv(bpm.manifest_text())}
    for pid in ("P11_chirp", "P12_frozen_noise"):
        assert rows[pid]["implemented"] == "false"
        assert rows[pid]["not_implemented_reason"].strip()
        assert rows[pid]["features"] == ""
    for pid, r in rows.items():
        if r["implemented"] == "true":
            assert r["not_implemented_reason"] == "", pid
            assert r["features"], pid


def test_params_json_is_deterministic(bpm):
    assert bpm.manifest_text() == bpm.manifest_text()
    row = bpm.template_row(DEFAULT_TEMPLATES[1])
    assert row["params_json"] == json.dumps(dict(DEFAULT_TEMPLATES[1].params), sort_keys=True, separators=(",", ":"))


def test_duplicate_ids_rejected(bpm):
    with pytest.raises(ValueError):
        bpm.build_rows([DEFAULT_TEMPLATES[0], DEFAULT_TEMPLATES[0]])


def test_committed_manifest_is_up_to_date(bpm):
    assert MANIFEST.is_file(), "run scripts/build_protocol_manifest.py"
    assert bpm.main(["--check", "--output", str(MANIFEST)]) == 0


def test_write_then_check_and_detect_stale(bpm, tmp_path):
    out = tmp_path / "pm.csv"
    assert bpm.main(["--check", "--output", str(out)]) == 1          # missing file is stale
    assert bpm.main(["--output", str(out)]) == 0
    assert bpm.main(["--check", "--output", str(out)]) == 0
    text = out.read_text(encoding="utf-8").replace("P04_step_2x", "P04_step_3x")
    out.write_text(text, encoding="utf-8")
    assert bpm.main(["--check", "--output", str(out)]) == 1


def test_relative_study_path_resolves_against_cwd(bpm, tmp_path, monkeypatch):
    (tmp_path / "study.yaml").write_text("protocols:\n  - protocol_id: P02_weak_step\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    rows = bpm.parse_csv(bpm.manifest_text(Path("study.yaml")))
    assert [r["protocol_id"] for r in rows] == ["P02_weak_step"]
    out = tmp_path / "pm.csv"
    assert bpm.main(["--study", "study.yaml", "--output", str(out)]) == 0
    assert bpm.main(["--study", "study.yaml", "--output", str(out), "--check"]) == 0


def test_unknown_protocol_without_kind_rejected(bpm, tmp_path):
    study = tmp_path / "bogus.yaml"
    study.write_text("protocols:\n  - protocol_id: P99_bogus\n", encoding="utf-8")
    with pytest.raises(ValueError, match="P99_bogus"):
        bpm.manifest_text(study)


def test_unrunnable_kind_rejected(bpm):
    t = ProtocolTemplate("P98_chirp_on", "chirp", "chirp marked implemented", {}, ("spike_count",))
    with pytest.raises(ValueError, match="kind"):
        bpm.build_rows([t])
    # The exclusion reflects the code: instantiate() cannot build this kind.
    with pytest.raises(ValueError):
        t.instantiate(1.0, 300.0)


def test_implemented_template_without_features_rejected(bpm):
    with pytest.raises(ValueError, match="features"):
        bpm.build_rows([ProtocolTemplate("P97_step", "step", "a step", {"multiple": 1.0}, ())])


def test_deferred_template_without_reason_rejected(bpm):
    with pytest.raises(ValueError, match="not_implemented_reason"):
        bpm.build_rows([ProtocolTemplate("P96_noise", "frozen_noise", "noise", {}, (), implemented=False)])


def test_implemented_kinds_match_code(bpm):
    implemented = [t for t in DEFAULT_TEMPLATES if t.implemented]
    assert {t.kind for t in implemented} == set(bpm.IMPLEMENTED_KINDS)
    for t in batched(implemented):
        t.instantiate(1.0, 300.0)       # every batched kind in the set is buildable


def test_study_override_changes_manifest(bpm, tmp_path):
    study = tmp_path / "study.yaml"
    study.write_text("protocols:\n  - protocol_id: P04_step_2x\n    params: {multiple: 3.0}\n", encoding="utf-8")
    rows = bpm.parse_csv(bpm.manifest_text(study))
    assert [r["protocol_id"] for r in rows] == ["P04_step_2x"]
    assert json.loads(rows[0]["params_json"])["multiple"] == 3.0
