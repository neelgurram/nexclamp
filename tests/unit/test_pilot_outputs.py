"""Prespecified pilot outputs on a synthetic campaign; study metadata on records and tables."""

from __future__ import annotations

import csv
import json

from nexclamp import config
from nexclamp.experiments import pilot_outputs as po
from nexclamp.schemas import RunRecord
from nexclamp.validation.fingerprint import Detection, write_detections

META = {"project_name": "Neuraxis", "study_phase": "development_pilot", "protocol_version": "PILOT_PROTOCOL_V1",
        "designation": "development study informed by Pilot 1"}


def _write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _cls(vid, model, kind, family, operator, klass, stratum, dprot="", valid="True"):
    return {"variant_id": vid, "model_id": model, "kind": kind, "family": family, "operator": operator, "params": "{}",
            "class": klass, "stratum": stratum, "interpretation": "", "structural_valid": valid,
            "detecting_protocols": dprot, "runtime_s": "1.5"}


def _det(vid, model, level, pid, feat):
    return {"variant_id": vid, "model_id": model, "level_factor": level, "protocol_id": pid, "feature": feat,
            "reason": "exceeds", "ref_value": 1, "var_value": 2, "diff": 1, "tau": 0.5, "ref_run_id": "", "var_run_id": ""}


def _campaign(tmp_path):
    p = tmp_path / "processed" / "pilot-v2"
    _write(p / "classification.csv", [
        _cls("m1", "rs", "mutant", "biophysical", "scale_conductance", "6_silent_under_canonical", "primary_semantic", "P05_long_step"),
        _cls("m2", "wb", "mutant", "biophysical", "shift_reversal", "5_non_equivalent", "primary_semantic", "P00_canonical"),
        _cls("m3", "wb", "mutant", "reference", "wrong_channel", "5_non_equivalent", "primary_semantic",
             "P00_canonical;P04_step_2x;P05_long_step"),
        _cls("m4", "hh", "mutant", "biophysical", "scale_capacitance", "4_equivalent_within_tested_domain", "primary_semantic"),
        _cls("m5", "rs", "mutant", "reference", "omit_include", "1_structurally_invalid", "primary_semantic", valid="False"),
        _cls("n1", "rs", "mutant", "numerical", "increase_dt", "6_silent_under_canonical", "numerical_robustness", "P04_step_2x"),
        _cls("t1", "hh", "valid_transform", "", "xml_formatting", "4_equivalent_within_tested_domain", "control"),
    ])
    _write(p / "detections.csv", [_det("m1", "rs", 1, "P05_long_step", "last_isi"), _det("m1", "rs", 2, "P05_long_step", "last_isi"),
                                  _det("m3", "wb", 1, "P04_step_2x", "spike_count"), _det("m3", "wb", 2, "P04_step_2x", "spike_count"),
                                  _det("t1", "hh", 1, "P07_hyperpolarizing_step", "steady_state_voltage")])
    _write(p / "detections_secondary.csv", [_det("m4", "hh", 1, "P09_short_pulse", "ap_half_width"),
                                            _det("m4", "hh", 2, "P09_short_pulse", "ap_half_width")])
    _write(p / "protocol_costs.csv", [{"protocol_id": x, "mean_cell_steps": 1} for x in
                                      ("P00_canonical", "P04_step_2x", "P05_long_step", "P09_short_pulse", "P03_rheobase")])
    _write(p / "numerical_robustness.csv", [{"variant_id": "n1", "model_id": "rs", "operator": "increase_dt", "exec_overrides": "{}",
                                             "label": "exceeds_reference_discretization_error", "deviation_over_ref_error_h": "5",
                                             "deviation_h": "3", "deviation_h2": "2", "deviation_h4": "1"}])
    _write(p / "mutant_audit_sheet.csv", [{"variant_id": "m1", "operator": "scale_conductance", "human_auditor": ""}])
    return p


def test_flow_cases_matrices_and_metadata(tmp_path):
    p = _campaign(tmp_path)
    out = po.build_outputs(p, tmp_path / "raw", tmp_path / "work_variants", tmp_path / "runs", tmp_path / "figs",
                           ["rs"], ["wb", "hh"], META)
    flow = {r["group"]: r for r in po.read_csv(out / "02_flow_counts.csv")}
    sem = flow["model_mutants__all_models"]
    assert (sem["generated"], sem["structurally_valid"], sem["executable"]) == ("5", "4", "4")
    assert (sem["canonical_detected"], sem["battery_detected"], sem["battery_only"], sem["canonical_only"]) == ("2", "2", "1", "1")
    assert flow["model_mutants__new_independent_source_models"]["generated"] == "3"
    assert flow["numerical_stress_tests__all_models"]["battery_only"] == "1"      # never mixed into model mutants
    a = po.read_csv(out / "04a_canonical_passed_battery_detected.csv")
    assert [r["variant_id"] for r in a] == ["m1"] and a[0]["model_set"] == po.REPEATED
    assert [r["variant_id"] for r in po.read_csv(out / "04b_canonical_detected_battery_missed.csv")] == ["m2"]
    c = po.read_csv(out / "04c_control_primary_feature_triggers.csv")
    assert [r["variant_id"] for r in c] == ["t1"] and c[0]["reproducible_false_positive"] == "False"
    d = po.read_csv(out / "04d_secondary_detected_primary_missed.csv")
    assert [r["variant_id"] for r in d] == ["m4"] and d[0]["primary_class_equivalent_but_secondary_detected"] == "True"
    pm = {r["variant_id"]: r for r in po.read_csv(out / "05_protocol_by_mutant_matrix.csv")}
    assert pm["m1"]["P05_long_step"] == "1" and pm["m1"]["P04_step_2x"] == "0" and pm["m5"]["P05_long_step"] == "NA"
    fm = {r["variant_id"]: r for r in po.read_csv(out / "06_feature_by_mutant_matrix.csv")}
    assert fm["m4"]["ap_half_width"] == "secondary:P09_short_pulse" and fm["m1"]["last_isi"] == "primary:P05_long_step"
    plots = po.read_csv(out / "07_candidate_case_trace_plots.csv")
    assert plots[0]["status"] == "fingerprint_missing"
    conv = po.read_csv(out / "08_numerical_convergence_summary.csv")
    assert conv[0]["n_deviation_non_increasing_under_refinement"] == "1"
    audit = po.read_csv(out / "10_mutant_audit_sheet_completed.csv")
    assert audit[0]["automated_single_documented_change_check"] == "variant_workspace_missing"
    p05 = {r["subset"]: r for r in po.read_csv(out / "11_p05_dominance_summary.csv")}
    assert p05["all_models"]["detected_only_by_P05"] == "1" and p05["all_models"]["battery_union_detected"] == "2"
    for f in out.glob("*.csv"):
        rows = po.read_csv(f)
        assert rows and all(r["study_phase"] == "development_pilot" and r["project_name"] == "Neuraxis" for r in rows), f
    assert json.loads((out / "summary.json").read_text())["reporting"]["findings"].startswith("exploratory")


def test_run_record_and_detections_carry_study_metadata(tmp_path):
    rec = RunRecord(run_id="r", campaign="c", run_kind="probe", model_id="m", variant_id="v", variant_tree_sha256="t",
                    protocol_ids=[], dt_ms=0.005, duration_ms=1, seed=0, simulator="s", simulator_version="1",
                    environment_digest="e", status="ok", runtime_s=0, trace_path="", trace_sha256="", feature_path="",
                    feature_sha256="", timestamp_utc="now", git_commit="abc", git_dirty=False)
    assert rec.study_phase == "" and rec.config_sha256 == ""           # older records still load
    write_detections([Detection("v", "m", 1, "P04", "spike_count", "exceeds", 1, 2, 1, 0.5, "a", "b")],
                     tmp_path / "d.csv", extra={"study_phase": "development_pilot"})
    row = po.read_csv(tmp_path / "d.csv")[0]
    assert row["study_phase"] == "development_pilot" and row["feature"] == "spike_count"


def test_study_metadata_from_config(tmp_path, monkeypatch):
    (tmp_path / "study.yaml").write_text("study_metadata:\n  project_name: Neuraxis\n  study_phase: development_pilot\n",
                                         encoding="utf-8")
    monkeypatch.setenv(config.CONFIG_DIR_ENV, str(tmp_path))
    assert config.study_metadata() == {"project_name": "Neuraxis", "study_phase": "development_pilot"}
    assert "Neuraxis" in config.designation_text()
