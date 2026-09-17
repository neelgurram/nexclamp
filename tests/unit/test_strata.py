"""Semantic versus numerical strata, identical numerics, and primary/secondary feature panels (D-029, D-030)."""

from __future__ import annotations

from types import SimpleNamespace as NS

import pytest

from neuraxis import mutations
from neuraxis.experiments import strata
from neuraxis.protocols.definitions import templates_from_config
from neuraxis.schemas import Edit, MutantClass, VariantKind, VariantRecord


def _v(family="biophysical", operator="scale_conductance", kind=VariantKind.MUTANT, **kw):
    return VariantRecord(variant_id=f"v-{operator}", model_id="m", kind=kind, family=family, operator=operator, **kw)


def _o(v, klass):
    return NS(variant=v, klass=klass)


def test_every_registered_numerical_operator_is_outside_the_primary_stratum():
    for name, op in mutations.REGISTRY.items():
        fam = getattr(op.family, "value", op.family)
        s = strata.stratum(VariantKind.MUTANT, fam, name)
        if fam == "numerical" or name in strata.NUMERICAL_OPERATORS:
            assert s == strata.NUMERICAL, name
        if s == strata.SEMANTIC:
            assert name not in strata.NUMERICAL_OPERATORS and fam in strata.SEMANTIC_FAMILIES


def test_numerical_operator_name_wins_over_a_wrong_family_label():
    assert strata.stratum(VariantKind.MUTANT, "biophysical", "increase_dt") == strata.NUMERICAL
    assert strata.stratum(VariantKind.VALID_TRANSFORM, "formatting", "xml_formatting") == strata.CONTROL
    with pytest.raises(strata.StratumError):
        strata.stratum(VariantKind.MUTANT, "mystery", "op")


def test_numerical_mutants_never_enter_the_primary_denominator():
    outcomes = [
        _o(_v(), MutantClass.NON_EQUIVALENT),
        _o(_v("reference", "wrong_channel"), MutantClass.SILENT),
        _o(_v("numerical", "increase_dt", exec_overrides={"dt_factor": 4}), MutantClass.SILENT),
        _o(_v("numerical", "recording_resolution", exec_overrides={"sample_every_ms": 0.25}), MutantClass.NON_EQUIVALENT),
        _o(_v("", "xml_formatting", kind=VariantKind.VALID_TRANSFORM), MutantClass.NON_EQUIVALENT),
        _o(_v("biophysical", "shift_reversal"), MutantClass.EQUIVALENT),
    ]
    got = strata.primary_admissible(outcomes)
    assert [o.variant.operator for o in got] == ["scale_conductance", "wrong_channel"]
    with pytest.raises(strata.StratumError, match="non-semantic"):
        strata.assert_primary_denominator([_v("numerical", "increase_dt")])
    with pytest.raises(strata.StratumError, match="non-semantic"):
        strata.assert_primary_denominator([_v("", "add_comments", kind=VariantKind.NO_CHANGE)])


def test_primary_variants_must_use_identical_numerics():
    with pytest.raises(strata.StratumError, match="execution overrides"):
        strata.check_identical_numerics(_v(exec_overrides={"dt_factor": 4}))
    step = Edit(file="LEMS.xml", locator="Simulation", attribute="step", old="0.01ms", new="0.04ms")
    with pytest.raises(strata.StratumError, match="step"):
        strata.check_identical_numerics(_v(edits=[step]))
    with pytest.raises(strata.StratumError, match="step"):
        strata.check_identical_numerics(_v("", "unit_conversion", kind=VariantKind.VALID_TRANSFORM, edits=[step]))
    same = Edit(file="LEMS.xml", locator="Simulation", attribute="step", old="0.01ms", new="0.00001s")
    strata.check_identical_numerics(_v("", "unit_conversion", kind=VariantKind.VALID_TRANSFORM, edits=[same]))
    strata.check_identical_numerics(_v("numerical", "increase_dt", exec_overrides={"dt_factor": 4}, edits=[step]))


def test_numerical_results_are_never_labelled_semantic_drift():
    for k in MutantClass:
        label = strata.interpretation(strata.NUMERICAL, k)
        assert label != MutantClass.SILENT.value and "6_silent" not in label
    assert "not semantic drift" in strata.interpretation(strata.NUMERICAL, MutantClass.SILENT)
    assert strata.interpretation(strata.SEMANTIC, MutantClass.SILENT) == MutantClass.SILENT.value


def test_operator_exclusion():
    ops = strata.select_mutation_operators(["biophysical", "reference", "numerical"], ["wrong_segment_group"])
    assert "wrong_segment_group" not in ops and "increase_dt" in ops and "scale_conductance" in ops
    with pytest.raises(strata.StratumError, match="unknown"):
        strata.select_mutation_operators(["biophysical"], ["no_such_operator"])


def test_secondary_features_never_decide_primary_detections():
    d = [NS(protocol_id="P04_step_2x", feature="spike_count"), NS(protocol_id="P04_step_2x", feature="first_isi"),
         NS(protocol_id="P99_unlisted", feature="anything")]
    prim, sec = strata.split_primary(d, {"P04_step_2x": frozenset({"spike_count"})})
    assert [x.feature for x in prim] == ["spike_count", "anything"]
    assert [x.feature for x in sec] == ["first_isi"]


def test_templates_extract_primary_and_secondary_features():
    [t] = templates_from_config([{"protocol_id": "P09_short_pulse", "features": ["spike_count", "ahp_depth"],
                                  "secondary_features": ["ap_half_width"]}])
    assert t.features == ("spike_count", "ahp_depth") and t.secondary_features == ("ap_half_width",)
    assert t.instantiate(0.5, 300).features == ("spike_count", "ahp_depth", "ap_half_width")
    with pytest.raises(ValueError, match="both primary and secondary"):
        templates_from_config([{"protocol_id": "P09_short_pulse", "features": ["spike_count"],
                                "secondary_features": ["spike_count"]}])


def _fp(values):
    return NS(tables={"P04": {f: NS(value=v, state="defined" if v is not None else "undefined")
                              for f, v in values.items()}})


def test_numerical_robustness_compares_against_reference_discretisation_error():
    ref = {1: _fp({"isi": 10.0, "amp": 80.0}), 2: _fp({"isi": 10.4, "amp": 80.1}), 4: _fp({"isi": 10.6, "amp": 80.15})}
    var = {1: _fp({"isi": 11.0, "amp": 80.05})}
    rows = {r["feature"]: r for r in strata.numerical_robustness_rows(ref, var, _v("numerical", "increase_dt"))}
    assert rows["isi"]["ref_error_h"] == pytest.approx(0.4)
    assert rows["isi"]["ref_observed_order"] == pytest.approx(1.0)
    assert rows["isi"]["label"] == "within_reference_discretization_error"      # 1.0 <= 3 * 0.4
    assert rows["amp"]["label"] == "within_reference_discretization_error"
    var2 = {1: _fp({"isi": 12.0, "amp": None})}
    rows2 = {r["feature"]: r for r in strata.numerical_robustness_rows(ref, var2, _v("numerical", "increase_dt"))}
    assert rows2["isi"]["label"] == "exceeds_reference_discretization_error"
    assert rows2["amp"]["label"] == "definedness_change"
