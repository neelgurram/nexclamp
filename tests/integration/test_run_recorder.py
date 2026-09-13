"""RunRecorder on real jNeuroML runs: content-addressed caching, immutability, reproducibility, feature keying."""

from __future__ import annotations

import copy
import json

import pytest

from neurosem.protocols.definitions import DEFAULT_TEMPLATES
from neurosem.schemas import ExecConfig, RunStatus, VariantKind, VariantRecord
from neurosem.validation.execution import RunRecorder

pytestmark = pytest.mark.jnml


def _setup(tmp_path, sim, rs_ws):
    from neurosem import config

    fcfg = config.features().data
    rec = RunRecorder("t", sim, results_root=tmp_path / "results", work_root=tmp_path / "work", features_cfg=fcfg,
                      timeout_s=600)
    by_id = {t.protocol_id: t for t in DEFAULT_TEMPLATES}
    protos = [by_id["P02_weak_step"].instantiate(0.56, 100.0), by_id["P04_step_2x"].instantiate(0.56, 100.0)]
    ref = VariantRecord("rs__reference", rs_ws.model.model_id, VariantKind.REFERENCE, tree_sha256=rs_ws.tree_sha256())
    return rec, protos, ref, fcfg


def test_cache_immutability_reproducibility_and_feature_rekeying(tmp_path, sim, rs_ws):
    rec, protos, ref, fcfg = _setup(tmp_path, sim, rs_ws)
    ex = ExecConfig(0.025)

    first = rec.run_battery(rs_ws, ref, protos, ex)
    assert first.status is RunStatus.OK and not first.cached
    assert set(first.tables) == {"P02_weak_step", "P04_step_2x"}
    assert first.tables["P04_step_2x"]["spike_count"].value > 0
    (r,) = first.records
    run_dir = tmp_path / "results" / "raw" / "t" / r.run_id
    assert (run_dir / "run.json").is_file() and (run_dir / "traces.npz").is_file()

    second = rec.run_battery(rs_ws, ref, protos, ex)
    assert second.cached and second.records[0].run_id == r.run_id
    assert second.tables["P04_step_2x"]["spike_count"].value == first.tables["P04_step_2x"]["spike_count"].value

    # Traces missing (e.g. fresh clone): features still load from the tracked JSON without simulating ...
    (run_dir / "traces.npz").chmod(0o644)
    (run_dir / "traces.npz").unlink()
    third = rec.run_battery(rs_ws, ref, protos, ex)
    assert third.cached and not third.traces
    # ... and when traces are required the run is re-simulated and must reproduce the recorded hash.
    fourth = rec.run_battery(rs_ws, ref, protos, ex, need_traces=True)
    assert not fourth.cached and (run_dir / "traces.npz").is_file()
    assert json.loads((run_dir / "run.json").read_text())["trace_sha256"] == fourth.records[0].trace_sha256

    # A different feature configuration re-extracts from stored traces without re-simulating.
    cfg2 = copy.deepcopy(fcfg)
    cfg2["settings"]["Threshold"] = -30.0
    rec2 = RunRecorder("t", sim, results_root=tmp_path / "results", work_root=tmp_path / "work", features_cfg=cfg2)
    fifth = rec2.run_battery(rs_ws, ref, protos, ex)
    assert fifth.cached
    assert len(list(run_dir.glob("features_*.json"))) == 2

    # Changing any file the simulation reads changes the run id.
    leak = rs_ws.root / "NeuroML2/channels/Leak/Leak.channel.nml"
    leak.write_text(leak.read_text(encoding="utf-8") + "\n<!-- formatting only -->\n", encoding="utf-8")
    sixth = rec.run_battery(rs_ws, ref, protos, ex)
    assert sixth.records[0].run_id != r.run_id and not sixth.cached


def test_build_error_is_recorded_and_not_retried(tmp_path, sim, rs_ws):
    rec, protos, ref, _ = _setup(tmp_path, sim, rs_ws)
    cell = rs_ws.cell_path
    cell.write_text(cell.read_text(encoding="utf-8").replace('ionChannel="Kd"', 'ionChannel="Kdx"'), encoding="utf-8")
    bad = VariantRecord("rs__bad", rs_ws.model.model_id, VariantKind.MUTANT)
    out = rec.run_battery(rs_ws, bad, protos, ExecConfig(0.025))
    assert out.status is RunStatus.BUILD_ERROR and not out.tables
    again = rec.run_battery(rs_ws, bad, protos, ExecConfig(0.025))
    assert again.cached and again.status is RunStatus.BUILD_ERROR
