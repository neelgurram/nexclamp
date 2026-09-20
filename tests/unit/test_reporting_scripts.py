"""Tests for the reporting and audit scripts added for the publication path.

These scripts decide nothing scientific: they read recorded outputs and lay them out. What must hold
is that they never invent a number, never silently drop a stage, and never fill in a human verdict.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def results_draft():
    return load("build_results_draft")


@pytest.fixture(scope="module")
def exposed():
    return load("pilot2_exposed_variants")


@pytest.fixture(scope="module")
def audit():
    return load("audit_pack")


@pytest.fixture(scope="module")
def agent_run():
    return load("agent_study_run")


@pytest.fixture(scope="module")
def xsim():
    return load("cross_simulator_check")


# --------------------------------------------------------------------------- attrition
def _mutant(vid, klass, model="m1", stratum="primary_semantic", detect="", *, b=False, c=False):
    """A classification row. `b`/`c` are the canonical feature / canonical full-trace level flags,
    which are what "canonical detected this" means everywhere (branch rule and reporting alike)."""
    admissible = klass in ("5_non_equivalent", "6_silent_under_canonical")
    return {"variant_id": vid, "model_id": model, "kind": "mutant", "stratum": stratum, "class": klass,
            "detecting_protocols": detect,
            "level_A_basic_pass": str(klass not in ("1_structurally_invalid", "2_non_executable",
                                                    "3_numerically_unstable")),
            "level_E_full_battery": str(admissible),
            "level_B_canonical_feature": str(bool(b)), "level_C_canonical_trace": str(bool(c))}


def test_attrition_counts_every_stage_and_never_skips_one(results_draft):
    cls = [_mutant("a", "5_non_equivalent", detect="P00_canonical"),
           _mutant("b", "6_silent_under_canonical", detect="P04_step_2x"),
           _mutant("c", "4_equivalent_within_tested_domain"),
           _mutant("d", "2_non_executable"),
           _mutant("e", "3_numerically_unstable"),
           _mutant("f", "1_structurally_invalid"),
           {"variant_id": "t1", "model_id": "m1", "kind": "valid_transform", "stratum": "control",
            "class": "4_equivalent_within_tested_domain", "detecting_protocols": ""}]
    stages = dict(results_draft.attrition(cls))
    assert stages["variants generated (all strata)"] == 7
    assert stages["primary semantic mutants"] == 6
    assert stages["structurally valid and executable"] == 4      # invalid and non-executable removed
    assert stages["numerically stable"] == 3                     # unstable removed
    assert stages["admissible (non-equivalent or silent)"] == 2
    assert stages["equivalent within the tested domain"] == 1


def test_per_model_reports_exposed_and_unexposed_separately(results_draft):
    """Amendment S-01: every primary figure is shown over all mutants and over the unexposed ones."""
    cls = [_mutant("x1", "5_non_equivalent", b=True),
           _mutant("x2", "5_non_equivalent", detect="P04_step_2x"),
           _mutant("x3", "5_non_equivalent", c=True)]      # canonical trace counts too, not only features
    rows = results_draft.per_model(cls, exposed={"x1"})
    assert len(rows) == 1
    r = rows[0]
    assert r["admissible"] == 3 and r["canonical_detected"] == 2 and r["canonical_rate"] == "0.667"
    # x1 was exposed, so the unexposed view drops it from both numerator and denominator
    assert r["admissible_unexposed"] == 2 and r["canonical_detected_unexposed"] == 1
    assert r["canonical_rate_unexposed"] == "0.500"


def test_per_model_never_divides_by_zero(results_draft):
    rows = results_draft.per_model([_mutant("e1", "4_equivalent_within_tested_domain")], exposed=set())
    assert rows[0]["admissible"] == 0 and rows[0]["canonical_rate"] == ""


# --------------------------------------------------------------------------- exposure matching
def test_exposure_matches_on_the_edit_never_on_an_outcome(exposed):
    """The site key is channel, gate, mechanism and magnitude - nothing about what the model did."""
    a = {"channel": "naChan", "gate": "m", "mechanism": "rates", "delta_mV": -10.0, "spikes": 7}
    b = {"channel": "naChan", "gate": "m", "mechanism": "rates", "delta_mV": -10.0, "spikes": 30}
    assert exposed.site_key(a) == exposed.site_key(b)          # same edit, different outcome
    c = {"channel": "naChan", "gate": "h", "mechanism": "rates", "delta_mV": -10.0}
    assert exposed.site_key(a) != exposed.site_key(c)          # different gate is a different site
    d = {"channel": "kChan", "factor": 1.25, "mechanism": "rates"}
    assert exposed.site_key(d)[3] == 1.25                      # multiplicative magnitudes also key


# --------------------------------------------------------------------------- audit pack
def test_audit_pack_renders_an_edit_a_person_can_check(audit):
    line = audit.describe_edits(json.dumps([{"file": "RS.cell.nml", "locator": "/x/y", "attribute": "condDensity",
                                             "old": "0.07 mS_per_cm2", "new": "0.14 mS_per_cm2"}]))[0]
    for part in ("RS.cell.nml", "condDensity", "0.07 mS_per_cm2", "0.14 mS_per_cm2"):
        assert part in line


def test_audit_pack_survives_an_unparsable_edit_record(audit):
    assert "unparsed" in audit.describe_edits("{not json")[0]
    assert audit.describe_edits("[]") == ["no edit recorded"]


def test_audit_sheet_columns_are_left_empty_for_the_human(audit):
    assert "human_auditor" in audit.VERDICT_COLUMNS
    assert "edit_matches_label_yes_no" in audit.VERDICT_COLUMNS
    assert "class_plausible_yes_no" in audit.VERDICT_COLUMNS


# --------------------------------------------------------------------------- agent study
def test_layer_status_reports_absent_and_unevaluated_layers_distinctly(agent_run):
    class Outcome:
        def __init__(self, value):
            self.status = type("S", (), {"value": value})()

    class Score:
        layers = {"edit_scope": Outcome("pass"), "hidden_battery_passes": Outcome("not_evaluated")}

    s = Score()
    assert agent_run.layer_status(s, "edit_scope") == "pass"
    assert agent_run.layer_status(s, "hidden_battery_passes") == "not_evaluated"
    assert agent_run.layer_status(s, "canonical_passes") == ""          # absent, not assumed to pass
    assert agent_run.LAYERS[0] == "edit_scope" and agent_run.LAYERS[-1] == "hidden_battery_passes"


# --------------------------------------------------------------------------- cross-simulator
def test_cross_simulator_comparison_is_descriptive_and_flags_count_mismatch(xsim):
    import numpy as np

    class Trace:
        def __init__(self, v):
            self.t_ms = np.arange(len(v), dtype=float) * 0.1
            self.v_mV = np.asarray(v, dtype=float)

    flat = Trace([-65.0] * 50)
    spiky = Trace([-65.0] * 24 + [10.0] + [-65.0] * 25)
    out = xsim.compare_traces(flat, spiky)
    assert out["jlems_spikes"] == 0 and out["neuron_spikes"] == 1
    assert "spike count differs" in out["agreement_note"]
    assert out["trace_rmse_mV"] > 0
    # No pass/fail verdict is produced anywhere in the row.
    assert not any(k in out for k in ("passed", "detected", "verdict"))


def test_cross_simulator_handles_a_missing_trace_without_inventing_numbers(xsim):
    out = xsim.compare_traces(None, None)
    assert out["jlems_spikes"] == "" and out["trace_rmse_mV"] == ""
    assert "no trace" in out["agreement_note"]
