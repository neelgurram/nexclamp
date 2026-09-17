"""Tests for neuraxis.models (manifest, workspaces) and neuraxis.config (hashed YAML configuration).

Manifest rows are checked against the pinned snapshot files themselves, so a typo in a
cell id, harness path or output column name fails here rather than deep inside a run.
"""

from __future__ import annotations

import csv
import dataclasses as dc
import re
import stat

import pytest
from lxml import etree

from neuraxis import config
from neuraxis.models import (
    MANIFEST_COLUMNS,
    MODEL_MANIFEST,
    RAW_MODELS,
    Workspace,
    copy_workspace,
    load_models,
    materialize,
    snapshot_dir,
    write_models,
)
from neuraxis.provenance import REPO_ROOT, sha256_file, tree_manifest, tree_sha256, write_immutable
from neuraxis.schemas import ExecConfig, ModelRecord
from neuraxis.units import parse

EXPECTED_IDS = {"pospischil2008_rs", "pospischil2008_lts", "pospischil2008_fs", "pospischil2008_ib",
                "nml2_hh_example", "wangbuzsaki1996_wb"}


@pytest.fixture(scope="module")
def all_models() -> dict[str, ModelRecord]:
    return load_models()


def _present(models: dict[str, ModelRecord]) -> list[ModelRecord]:
    return [m for m in models.values() if snapshot_dir(m).is_dir()]


# ------------------------------------------------------------------------------------- manifest
def test_manifest_columns_match_dataclass():
    with open(MODEL_MANIFEST, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == MANIFEST_COLUMNS == [f.name for f in dc.fields(ModelRecord)]


def test_load_models_ids_and_inclusion(all_models):
    assert set(all_models) == EXPECTED_IDS
    included = load_models(include_only=True)
    assert set(included) == {"pospischil2008_rs", "pospischil2008_lts"}
    assert all(m.inclusion in {"include", "exclude", "candidate"} for m in all_models.values())
    assert all(m.inclusion_reason.strip() for m in all_models.values())


def test_manifest_provenance_fields(all_models):
    for m in all_models.values():
        assert re.fullmatch(r"[0-9a-f]{40}", m.commit), m.model_id
        name, short = m.snapshot.split("@")
        assert m.commit.startswith(short) and name, m.model_id
        assert m.source_url.startswith("https://github.com/") and m.license and m.license_url.startswith("https://")
        assert re.fullmatch(r"\d{4}-\d\d-\d\d", m.download_date)
        assert m.simulator == "jNeuroML"
        assert int(m.harness_v_column) >= 1
        if m.temperature.strip():
            assert parse(m.temperature).dimension == "temperature"


def test_all_snapshots_present(all_models):
    assert len(_present(all_models)) == len(all_models)


def test_manifest_paths_resolve_in_snapshots(all_models):
    for m in _present(all_models):
        root = snapshot_dir(m)
        assert (root / m.cell_file).is_file(), m.model_id
        assert (root / m.harness_lems).is_file(), m.model_id


def test_cell_id_defined_in_cell_file(all_models):
    for m in _present(all_models):
        tree = etree.parse(str(snapshot_dir(m) / m.cell_file))
        ids = {el.get("id") for el in tree.iter() if isinstance(el.tag, str)}
        assert m.cell_id in ids, m.model_id


def test_harness_output_file_and_column_exist(all_models):
    for m in _present(all_models):
        tree = etree.parse(str(snapshot_dir(m) / m.harness_lems))
        outs = [el for el in tree.iter() if isinstance(el.tag, str) and el.tag.split("}")[-1] == "OutputFile"]
        match = [o for o in outs if o.get("fileName") == m.harness_output_file]
        assert match, (m.model_id, [o.get("fileName") for o in outs])
        cols = [c for c in match[0] if isinstance(c.tag, str) and c.tag.split("}")[-1] == "OutputColumn"]
        col = int(m.harness_v_column)
        assert col <= len(cols), m.model_id
        assert cols[col - 1].get("quantity").endswith("/v"), (m.model_id, cols[col - 1].get("quantity"))


def test_write_models_round_trip(tmp_path, all_models):
    p = tmp_path / "sub" / "manifest.csv"
    write_models(list(all_models.values()), p)
    assert load_models(p) == all_models
    assert b"\r\n" not in p.read_bytes()


def test_write_models_reproduces_tracked_manifest_bytes(tmp_path, all_models):
    p = tmp_path / "manifest.csv"
    write_models(list(all_models.values()), p)
    assert p.read_bytes() == MODEL_MANIFEST.read_bytes()


def test_load_models_rejects_missing_column(tmp_path, all_models):
    p = tmp_path / "m.csv"
    write_models(list(all_models.values()), p)
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    cols = [c for c in MANIFEST_COLUMNS if c != "cell_id"]
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    with pytest.raises(ValueError, match="cell_id"):
        load_models(p)


def test_header_only_manifest_with_wrong_columns_is_rejected(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text("model_id,name\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_models(p)


def test_duplicate_model_ids_are_rejected(tmp_path, all_models):
    rs = all_models["pospischil2008_rs"]
    p = tmp_path / "m.csv"
    write_models([rs, dc.replace(rs, name="silently different")], p)
    with pytest.raises(ValueError):
        load_models(p)


# ----------------------------------------------------------------------------------- workspaces
def test_materialize_is_byte_exact_copy_without_provenance(tmp_path, all_models):
    m = all_models["pospischil2008_rs"]
    ws = materialize(m, tmp_path / "rs")
    src = snapshot_dir(m)
    assert (src / "PROVENANCE.json").is_file()
    assert not (ws.root / "PROVENANCE.json").exists()
    assert ws.tree_sha256() == tree_sha256(src)
    assert tree_manifest(ws.root) == tree_manifest(src)


def test_materialized_files_are_writable(tmp_path, all_models):
    ws = materialize(all_models["pospischil2008_rs"], tmp_path / "rs")
    for p in ws.root.rglob("*"):
        if p.is_file():
            assert p.stat().st_mode & stat.S_IWRITE, p


def test_workspace_paths(tmp_path, all_models):
    m = all_models["pospischil2008_rs"]
    ws = materialize(m, tmp_path / "rs")
    assert isinstance(ws, Workspace) and ws.model is m
    assert ws.cell_path == tmp_path / "rs" / "NeuroML2/cells/RS/RS.cell.nml" and ws.cell_path.is_file()
    assert ws.harness_path == tmp_path / "rs" / "NeuroML2/cells/RS/LEMS_RS.xml" and ws.harness_path.is_file()
    assert ws.path("NeuroML2/channels/Na/Na.channel.nml").is_file()


def test_editing_workspace_never_touches_snapshot(tmp_path, all_models):
    m = all_models["pospischil2008_rs"]
    raw_before = tree_sha256(snapshot_dir(m))
    ws = materialize(m, tmp_path / "rs")
    ws.cell_path.write_text(ws.cell_path.read_text().replace("5.0 mS_per_cm2", "2.5 mS_per_cm2"))
    assert ws.tree_sha256() != raw_before
    assert tree_sha256(snapshot_dir(m)) == raw_before


def test_materialize_refuses_existing_destination(tmp_path, all_models):
    m = all_models["nml2_hh_example"]
    materialize(m, tmp_path / "hh")
    with pytest.raises(FileExistsError):
        materialize(m, tmp_path / "hh")


def test_materialize_overwrite_replaces_read_only_content(tmp_path, all_models):
    m = all_models["nml2_hh_example"]
    ws = materialize(m, tmp_path / "hh")
    write_immutable(ws.root / "results" / "run.json", b"{}")         # read-only file inside the workspace
    ws.cell_path.write_text("corrupted")
    ws2 = materialize(m, tmp_path / "hh", overwrite=True)
    assert ws2.tree_sha256() == tree_sha256(snapshot_dir(m))
    assert not (ws2.root / "results" / "run.json").exists()


def test_materialize_missing_snapshot(tmp_path, all_models):
    bogus = dc.replace(all_models["pospischil2008_rs"], snapshot="NoSuchRepo@deadbeef")
    with pytest.raises(FileNotFoundError, match="snapshot not found"):
        materialize(bogus, tmp_path / "x")
    assert not (tmp_path / "x").exists()


def test_copy_workspace(tmp_path, all_models):
    ws = materialize(all_models["pospischil2008_rs"], tmp_path / "rs")
    (ws.root / "variant.json").write_text("{}")
    cp = copy_workspace(ws, tmp_path / "rs_copy")
    assert cp.model is ws.model and cp.tree_sha256() == ws.tree_sha256()
    assert (cp.root / "variant.json").is_file()
    cp.cell_path.write_text("changed")
    assert cp.tree_sha256() != ws.tree_sha256()
    with pytest.raises(FileExistsError):
        copy_workspace(ws, tmp_path / "rs_copy")
    cp2 = copy_workspace(ws, tmp_path / "rs_copy", overwrite=True)
    assert cp2.tree_sha256() == ws.tree_sha256()


def test_raw_models_location():
    assert RAW_MODELS == REPO_ROOT / "models" / "raw"
    assert MODEL_MANIFEST == REPO_ROOT / "data" / "model_manifest.csv"


# ------------------------------------------------------------------------------------ config
def test_load_yaml_relative_to_config_dir_and_hashed():
    c = config.load_yaml("study.yaml")
    assert c.path == config.CONFIG_DIR / "study.yaml"
    assert c.sha256 == sha256_file(config.CONFIG_DIR / "study.yaml")
    assert c["study_id"] == "neurosem" and c.get("missing", 7) == 7


def test_named_loaders():
    assert config.study().path.name == "study.yaml"
    assert "Threshold" in config.features()["settings"]
    assert "c_refinement" in config.tolerances().data


def test_load_yaml_absolute_and_empty(tmp_path):
    p = tmp_path / "empty.yaml"
    p.write_text("# nothing\n", encoding="utf-8")
    c = config.load_yaml(p)
    assert c.data == {} and c.path == p and c.sha256 == sha256_file(p)
    with pytest.raises(KeyError):
        c["anything"]


def test_config_hash_changes_with_content(tmp_path):
    p = tmp_path / "a.yaml"
    p.write_text("x: 1\n", encoding="utf-8")
    h1 = config.load_yaml(p).sha256
    p.write_text("x: 1  # same data, different bytes\n", encoding="utf-8")
    c2 = config.load_yaml(p)
    assert c2.data == {"x": 1} and c2.sha256 != h1


def test_numerics_from_study_config():
    assert config.nominal_exec() == ExecConfig(dt_ms=0.005)
    assert config.refinement_levels() == [0.005, 0.0025, 0.00125]


def test_numerics_from_custom_config(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text("numerics: {dt_nominal_ms: 0.02, refinement_factors: [1, 2]}\npaths: {work: w, results: r}\n")
    c = config.load_yaml(p)
    assert config.nominal_exec(c).dt_ms == 0.02
    assert config.refinement_levels(c) == [0.02, 0.01]
    assert config.work_dir(c) == REPO_ROOT / "w" and config.results_dir(c) == REPO_ROOT / "r"


def test_study_config_numerics_consistent_with_features():
    s, f = config.study(), config.features()
    assert s["rheobase"]["spike_threshold_mV"] == f["settings"]["Threshold"]
    assert float(s["numerics"]["settle_ms"]).is_integer()
    assert config.work_dir() == REPO_ROOT / "work" and config.results_dir() == REPO_ROOT / "results"
