"""Execution-plan run records: required fields, output streams, and retry-safe tool failures."""

from __future__ import annotations

import json

import numpy as np

from neuraxis.schemas import RUN_RECORD_REQUIRED_FIELDS, RunStatus, SimResult, Trace, VariantKind, VariantRecord
from neuraxis.validation.canonical import canonical_protocol
from neuraxis.validation.execution import RunRecorder


class FakeSim:
    name = "fake"

    def __init__(self, statuses):
        self.statuses = list(statuses)
        self.calls = 0

    def available(self):
        return True

    def version_info(self):
        return {"jar_sha256": "fake-jar", "simulator": "fake"}

    def version_string(self):
        return "fake 1.0"

    def run_lems(self, lems_file, outputs, timeout_s=0, sample_every_ms=None):
        status = self.statuses[min(self.calls, len(self.statuses) - 1)]
        self.calls += 1
        if status is RunStatus.TOOL_FAILURE:
            return SimResult(status, -1, 0.0, {}, ["java"], "java crashed")
        t = np.arange(0.0, 300.0, 0.01)
        v = -65.0 + 100.0 * (np.sin(t / 3.0) > 0.995)
        traces = {name: Trace(t, v) for spec in outputs for name in spec.columns}
        return SimResult(status, 0, 0.5, traces, ["java"], "", "tail", "sim stdout\n", "")


def _variant(ws, kind=VariantKind.MUTANT):
    tree = ws.tree_sha256()
    return VariantRecord("m-test", ws.model.model_id, kind, "biophysical", "scale_conductance",
                         tree_sha256=tree, parent_tree_sha256="parent-hash")


def test_tool_failure_is_kept_but_never_blocks_the_retry(hh_ws, tmp_path):
    sim = FakeSim([RunStatus.TOOL_FAILURE, RunStatus.OK])
    rec = RunRecorder("c", sim, results_root=tmp_path / "res", work_root=tmp_path / "work")
    proto = canonical_protocol(hh_ws)
    first = rec.run_canonical(hh_ws, _variant(hh_ws), proto)
    assert first.status is RunStatus.TOOL_FAILURE and not first.records
    run_dirs = list((tmp_path / "res" / "raw" / "c").glob("r-*"))
    assert len(run_dirs) == 1 and not (run_dirs[0] / "run.json").exists()
    assert len(list((run_dirs[0] / "_tool_failures").glob("*.json"))) == 1
    second = rec.run_canonical(hh_ws, _variant(hh_ws), proto)
    assert second.status is RunStatus.OK and sim.calls == 2
    data = json.loads((run_dirs[0] / "run.json").read_text(encoding="utf-8"))
    assert data["run_id"] == run_dirs[0].name


def test_successful_record_carries_every_required_field(hh_ws, tmp_path, monkeypatch):
    from neuraxis import config

    (tmp_path / "cfg").mkdir()
    for name in ("study.yaml", "features.yaml", "tolerances.yaml"):
        (tmp_path / "cfg" / name).write_bytes((config.CONFIG_DIR / name).read_bytes())
    monkeypatch.setenv(config.CONFIG_DIR_ENV, str(tmp_path / "cfg"))
    sim = FakeSim([RunStatus.OK])
    rec = RunRecorder("c", sim, results_root=tmp_path / "res", work_root=tmp_path / "work")
    out = rec.run_canonical(hh_ws, _variant(hh_ws), canonical_protocol(hh_ws))
    assert out.status is RunStatus.OK
    run_dir = tmp_path / "res" / "raw" / "c" / out.records[0].run_id
    data = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    missing = [f for f in RUN_RECORD_REQUIRED_FIELDS if data.get(f) in (None, "")]
    assert not missing, missing
    assert data["mutation_id"] == "m-test" and data["transformation_id"] is None
    assert data["base_model_hash"] == "parent-hash" and data["project_name"] == "Neuraxis"
    assert (run_dir / "stdout.txt").read_text(encoding="utf-8") == "sim stdout\n"
    # a cached reload verifies the stored streams against the record
    again = rec.run_canonical(hh_ws, _variant(hh_ws), canonical_protocol(hh_ws))
    assert again.cached and sim.calls == 1
