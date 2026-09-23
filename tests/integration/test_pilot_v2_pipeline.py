"""End-to-end PILOT2_PROTOCOL pipeline on a tiny matrix (one Pilot 1 development model, temporary results).

Exercises reference trace calibration, validation levels A-E, severity-stratified generation, survivor
re-checks and the Pilot 2 output builder. It writes only under pytest's temporary directory.
"""

from __future__ import annotations

import json
import shutil

import pytest
import yaml

from nexclamp import config
from nexclamp.provenance import REPO_ROOT


@pytest.mark.jnml
@pytest.mark.slow
def test_pilot_v2_pipeline_end_to_end(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "cfg"
    cfg_dir.mkdir()
    for name in ("features.yaml", "tolerances.yaml", "agent_policy.yaml"):
        shutil.copyfile(REPO_ROOT / "configs" / name, cfg_dir / name)
    study = yaml.safe_load((REPO_ROOT / "configs" / "study.yaml").read_text(encoding="utf-8"))
    study["study_metadata"] = {"study_id": "neuron_model_behavioral_validation", "project_name": "test",
                               "study_phase": "test", "protocol_version": "TEST_V2", "designation": "integration test"}
    study["validation_levels"] = {"enabled": True}
    study["paths"] = {"work": str(tmp_path / "work"), "results": str(tmp_path / "results")}
    study["protocols"] = [{"protocol_id": "P04_step_2x", "features": ["spike_count", "first_spike_latency", "firing_regime"]}]
    study["canonical"]["features"] = ["spike_count", "first_spike_latency", "firing_regime"]
    study["pilot"] = {"models": ["pospischil2008_rs"], "mutation_families": ["biophysical"],
                      "exclude_operators": ["scale_conductance", "shift_reversal", "shift_initial_voltage",
                                            "wrong_segment_group", "scale_gate_time_constant"],
                      "severity_levels": ["mild", "strong"], "sites_per_severity": {"default": 1},
                      "mutants_per_operator": 1, "transforms_per_operator": 1}
    (cfg_dir / "study.yaml").write_text(yaml.safe_dump(study, sort_keys=False), encoding="utf-8")
    monkeypatch.setenv(config.CONFIG_DIR_ENV, str(cfg_dir))

    from nexclamp.experiments import pilot_v2_outputs as p2
    from nexclamp.experiments.pilot import run_pilot

    report = run_pilot("v2-e2e", workers=4, n_transforms=1)
    processed = tmp_path / "results" / "processed" / "v2-e2e"
    assert report.is_file() and "Validation levels" in report.read_text(encoding="utf-8")
    assert json.loads((processed / "references" / "pospischil2008_rs" / "trace_tolerances.json").read_text())
    gen = json.loads((processed / "generation.json").read_text())
    assert gen["operators"] == ["scale_capacitance"] and gen["severity_levels"] == ["mild", "strong"]
    out = p2.build(processed, tmp_path / "results" / "raw" / "v2-e2e", tmp_path / "work" / "variants" / "v2-e2e",
                   tmp_path / "work" / "runs" / "v2-e2e", tmp_path / "fig", {"study_id": "x"}, seed=1)
    import csv

    with open(processed / "classification.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    mutants = [r for r in rows if r["kind"] == "mutant"]
    assert sorted(r["severity"] for r in mutants) == ["mild", "strong"]
    assert all("level_C_canonical_trace" in r and r["study_id"] == "neuron_model_behavioral_validation" for r in rows)
    summary = json.loads((out / "summary.json").read_text())
    assert summary["branch"]["primary_branch"] in ("A_hidden_drift_supported", "B_feature_level_insufficiency",
                                                   "C_canonical_adequacy", "D_pipeline_uncertainty", "indeterminate")
    run = next((tmp_path / "results" / "raw" / "v2-e2e").glob("r-*/run.json"))
    rec = json.loads(run.read_text())
    assert rec["study_id"] == "neuron_model_behavioral_validation" and rec["execution_id"] and rec["stdout_path"]
