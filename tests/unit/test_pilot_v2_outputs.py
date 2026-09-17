"""Pilot 2 outputs: validation levels kept separate, survivors, false positives, branch rules."""

from __future__ import annotations

import csv
import json

from neuraxis.experiments import pilot_outputs as po
from neuraxis.experiments import pilot_v2_outputs as p2

META = {"project_name": "Neuraxis", "study_phase": "development_pilot", "protocol_version": "PILOT_PROTOCOL_V2"}


def _write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    names = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names)
        w.writeheader()
        w.writerows(rows)


def _row(vid, model, kind, fam, op, klass, stratum, a=True, b=False, c=False, d=False, e=False, conf="", tconf="",
         af="maximal_conductance", sev="mild"):
    fs = a and d and not b
    return {"variant_id": vid, "model_id": model, "kind": kind, "family": fam, "operator": op, "params": "{}",
            "class": klass, "stratum": stratum, "structural_valid": "True", "detecting_protocols": "",
            "analysis_family": af, "severity": sev, "level_A_basic_pass": a, "level_B_canonical_feature": b,
            "level_C_canonical_trace": c, "level_D_multi_protocol": d, "level_E_full_battery": e,
            "level_feature_level_canonical_survivor": fs, "level_full_trace_canonical_survivor": fs and not c,
            "survivor_confirmed_h4": conf, "full_trace_survivor_confirmed_h4": tconf, "runtime_s": "1"}


def _campaign(tmp_path, rows, tol_limits=("relative",) * 8):
    p = tmp_path / "processed" / "pilot2"
    _write(p / "classification.csv", rows)
    _write(p / "detections.csv", [{"variant_id": "x", "level_factor": 1, "protocol_id": "P04", "feature": "f"}])
    _write(p / "tolerances.csv", [{"model_id": "m1", "protocol_id": "P04", "feature": f"f{i}", "limiting": l}
                                  for i, l in enumerate(tol_limits)])
    _write(p / "protocol_costs.csv", [{"protocol_id": x} for x in ("P00_canonical", "P04_step_2x", "P03_rheobase")])
    return p


SEM = ("mutant", "biophysical", "scale_conductance", "5_non_equivalent", "primary_semantic")
CTL = ("valid_transform", "", "xml_formatting", "4_equivalent_within_tested_domain", "control")


def test_hidden_drift_needs_confirmed_full_trace_survivors_on_two_models(tmp_path):
    rows = [_row("s1", "m1", *SEM, d=True, e=True, conf="True", tconf="True"),
            _row("s2", "m2", *SEM, d=True, e=True, conf="True", tconf="True"),
            _row("k1", "m1", *SEM, b=True, d=True, e=True), _row("t1", "m1", *CTL)]
    br = p2.classify_branch(po.CampaignView(_campaign(tmp_path, rows), [], []), _campaign(tmp_path, rows))
    assert br["primary_branch"] == "A_hidden_drift_supported" and br["evidence"]["confirmed_full_trace_survivors"] == 2


def test_feature_level_insufficiency_and_adequacy_and_uncertainty(tmp_path):
    rows = [_row("f1", "m1", *SEM, c=True, d=True, e=True, conf="True"),
            _row("f2", "m2", *SEM, c=True, d=True, e=True, conf="True"),
            _row("k1", "m1", *SEM, b=True, e=True), _row("t1", "m1", *CTL)]
    p = _campaign(tmp_path, rows)
    br = p2.classify_branch(po.CampaignView(p, [], []), p)
    assert br["primary_branch"] == "B_feature_level_insufficiency" and br["flags"]["C_canonical_adequacy"]
    adequate = [_row(f"k{i}", "m1", *SEM, b=True, d=True, e=True) for i in range(20)] + [_row("t1", "m1", *CTL)]
    p = _campaign(tmp_path / "b", adequate)
    assert p2.classify_branch(po.CampaignView(p, [], []), p)["primary_branch"] == "C_canonical_adequacy"
    noisy = adequate + [_row(f"t{i}", "m1", *CTL, e=True) for i in range(2, 5)]
    p = _campaign(tmp_path / "c", noisy)
    assert p2.classify_branch(po.CampaignView(p, [], []), p)["primary_branch"] == "D_pipeline_uncertainty"
    unstable = adequate + [_row("u1", "m1", *SEM, d=True, e=True, conf="False")]
    p = _campaign(tmp_path / "d", unstable)
    assert p2.classify_branch(po.CampaignView(p, [], []), p)["flags"]["D_pipeline_uncertainty"]


def test_outputs_keep_b_and_c_separate_and_are_labelled(tmp_path):
    rows = [_row("f1", "m1", *SEM, c=True, d=True, e=True, conf="True"), _row("k1", "m1", *SEM, b=True, e=True),
            _row("t1", "m1", *CTL, e=True)] + [_row(f"x{i}", "m1", *SEM) for i in range(25)]
    p = _campaign(tmp_path, rows)
    out = p2.build(p, tmp_path / "raw", tmp_path / "wv", tmp_path / "wr", tmp_path / "fig", META, seed=1)
    counts = {r["group"]: r for r in po.read_csv(out / "01_validation_level_counts.csv")}
    allm = counts["model_mutants__all_models"]
    assert (allm["B_canonical_feature"], allm["C_canonical_trace"], allm["feature_level_canonical_survivors"]) == ("1", "1", "1")
    assert [r["variant_id"] for r in po.read_csv(out / "07_valid_transformation_false_positives.csv")] == ["t1"]
    assert len(po.read_csv(out / "11_random_audit_cases.csv")) == 20
    assert all(r["protocol_version"] == "PILOT_PROTOCOL_V2" for f in out.glob("*.csv") for r in po.read_csv(f))
    assert json.loads((out / "summary.json").read_text())["branch"]["primary_branch"] in (
        "B_feature_level_insufficiency", "C_canonical_adequacy", "D_pipeline_uncertainty", "indeterminate")
