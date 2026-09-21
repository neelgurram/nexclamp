"""Campaign roles, sealing, preservation and the exploratory/confirmatory firewall (D-026, D-027)."""

from __future__ import annotations

import json
import tarfile

import pytest

from neuraxis import config
from neuraxis.experiments import registry as reg


def _run(raw, name, commit="abc", dirty=False):
    d = raw / name
    d.mkdir(parents=True)
    (d / "run.json").write_text(json.dumps({"git_commit": commit, "git_dirty": dirty}), encoding="utf-8")


def test_register_is_idempotent_and_role_is_permanent(tmp_path):
    reg.register("pilot", reg.EXPLORATORY_PILOT, tmp_path, "first pilot")
    assert reg.register("pilot", reg.EXPLORATORY_PILOT, tmp_path)["note"] == "first pilot"
    with pytest.raises(reg.CampaignError, match="cannot be reused"):
        reg.register("pilot", reg.CONFIRMATORY_HELDOUT, tmp_path)
    with pytest.raises(ValueError):
        reg.register("x", "confirmatory-ish", tmp_path)


def test_sealed_campaign_is_read_only(tmp_path):
    reg.register("pilot", reg.EXPLORATORY_PILOT, tmp_path)
    reg.assert_writable("pilot", reg.EXPLORATORY_PILOT, tmp_path)
    (tmp_path / "processed" / "pilot").mkdir(parents=True)
    reg.seal("pilot", tmp_path, role=reg.EXPLORATORY_PILOT, code_commit="d323afa", note="done")
    with pytest.raises(reg.CampaignError, match="sealed"):
        reg.assert_writable("pilot", reg.EXPLORATORY_PILOT, tmp_path)
    with pytest.raises(reg.CampaignError, match="already sealed"):
        reg.seal("pilot", tmp_path, role=reg.EXPLORATORY_PILOT, code_commit="d323afa", note="again")


def test_role_mismatch_blocks_writes(tmp_path):
    reg.register("disc", reg.DISCOVERY, tmp_path)
    with pytest.raises(reg.CampaignError, match="registered as"):
        reg.assert_writable("disc", reg.CONFIRMATORY_HELDOUT, tmp_path)


def test_confirmatory_campaign_must_be_fresh_and_not_exploratory(tmp_path):
    reg.register("pilot", reg.EXPLORATORY_PILOT, tmp_path)
    with pytest.raises(reg.CampaignError, match="never enter"):
        reg.assert_confirmatory_fresh("pilot", tmp_path)
    _run(tmp_path / "raw" / "leftover", "r-1")
    with pytest.raises(reg.CampaignError, match="start fresh"):
        reg.assert_confirmatory_fresh("leftover", tmp_path)
    reg.assert_confirmatory_fresh("heldout-2027", tmp_path)


def test_confirmatory_campaign_is_never_pooled(tmp_path):
    reg.register("pilot", reg.EXPLORATORY_PILOT, tmp_path)
    reg.register("heldout", reg.CONFIRMATORY_HELDOUT, tmp_path)
    reg.assert_not_pooled(["heldout"], tmp_path)
    reg.assert_not_pooled(["pilot", "pilot-v2"], tmp_path)
    with pytest.raises(reg.CampaignError, match="pool"):
        reg.assert_not_pooled(["heldout", "pilot"], tmp_path)


def test_single_clean_commit_check(tmp_path):
    with pytest.raises(reg.CampaignError, match="no run records"):
        reg.check_single_clean_commit(tmp_path)
    _run(tmp_path, "r-1")
    _run(tmp_path, "r-2")
    assert reg.check_single_clean_commit(tmp_path) == "abc"
    _run(tmp_path, "r-3", dirty=True)
    with pytest.raises(reg.CampaignError, match="dirty"):
        reg.check_single_clean_commit(tmp_path)
    _run(tmp_path, "r-4", commit="def")
    with pytest.raises(reg.CampaignError, match="2 commits"):
        reg.check_single_clean_commit(tmp_path)


def test_config_change_requires_new_campaign(tmp_path):
    snap = {"campaign": "c", "configs": {"study.yaml": "aa"}, "simulator": {"jar_sha256": "j"}}
    reg.check_config_snapshot(tmp_path, snap)
    (tmp_path / "campaign_configs.json").write_text(json.dumps(snap), encoding="utf-8")
    reg.check_config_snapshot(tmp_path, {**snap, "created_utc": "later"})
    with pytest.raises(reg.CampaignError, match="new campaign name"):
        reg.check_config_snapshot(tmp_path, {**snap, "configs": {"study.yaml": "bb"}})


def test_config_snapshot_is_write_once(tmp_path):
    src = tmp_path / "study.yaml"
    src.write_text("a: 1\n", encoding="utf-8")
    processed = tmp_path / "processed"
    reg.snapshot_configs(processed, [config.load_yaml(src)])
    reg.snapshot_configs(processed, [config.load_yaml(src)])
    src.write_text("a: 2\n", encoding="utf-8")
    with pytest.raises(reg.CampaignError, match="differs"):
        reg.snapshot_configs(processed, [config.load_yaml(src)])


def test_manifest_and_archive_cover_ignored_files(tmp_path):
    raw = tmp_path / "raw"
    (raw / "r-1").mkdir(parents=True)
    (raw / "r-1" / "run.json").write_text("{}", encoding="utf-8")
    (raw / "r-1" / "traces.npz").write_bytes(b"\x00\x01")
    roots = {"raw": raw, "work_runs": tmp_path / "absent"}
    entries = reg.build_manifest(roots)
    assert [n for _, n in entries] == ["raw/r-1/run.json", "raw/r-1/traces.npz"]
    manifest = tmp_path / reg.ARCHIVE_MANIFEST
    reg.write_manifest(manifest, entries)
    assert reg.verify_manifest(manifest, roots) == []
    info = reg.write_archive(tmp_path / "a" / "c.tar", roots, manifest)
    with tarfile.open(tmp_path / "a" / info["file"]) as tf:
        assert set(tf.getnames()) == {reg.ARCHIVE_MANIFEST, "raw/r-1/run.json", "raw/r-1/traces.npz"}
    with pytest.raises(reg.CampaignError, match="write-once"):
        reg.write_archive(tmp_path / "a" / "c.tar", roots, manifest)
    (raw / "r-1" / "traces.npz").write_bytes(b"changed")
    assert reg.verify_manifest(manifest, roots) == ["raw/r-1/traces.npz"]


def test_config_dir_override(tmp_path, monkeypatch):
    assert config.uses_default_config_dir()
    (tmp_path / "study.yaml").write_text("study_id: alt\n", encoding="utf-8")
    monkeypatch.setenv(config.CONFIG_DIR_ENV, str(tmp_path))
    assert not config.uses_default_config_dir()
    assert config.study()["study_id"] == "alt"


def test_a_sealed_campaign_refuses_new_runs_from_any_writer(tmp_path):
    """X-27: a caller that builds a RunRecorder directly must not add runs to sealed data.

    assert_writable guards the pipeline, but the agent-study scorer constructs a recorder from the
    campaign name in its frozen config. Once a campaign is sealed, every writer is refused.
    """
    import pytest

    from neuraxis.experiments import registry
    from neuraxis.validation.execution import RunRecorder

    results = tmp_path / "results"
    (results / "processed" / "done").mkdir(parents=True)
    registry.register("done", registry.EXPLORATORY_PILOT, results)
    registry.seal("done", results, role=registry.EXPLORATORY_PILOT, code_commit="abc1234", note="finished")

    rec = RunRecorder("done", sim=None, results_root=results, work_root=tmp_path / "work")
    with pytest.raises(registry.CampaignError, match="sealed"):
        rec._refuse_sealed()

    open_rec = RunRecorder("still_open", sim=None, results_root=results, work_root=tmp_path / "work")
    open_rec._refuse_sealed()      # an unsealed campaign is writable
