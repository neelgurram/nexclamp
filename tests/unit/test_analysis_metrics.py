"""Unit tests for neurosem.analysis.metrics (hand-computed values and scipy cross-checks)."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest
from scipy.stats import binomtest

from neurosem.analysis import metrics as M
from neurosem.schemas import MutantClass as MC

# --------------------------------------------------------------------------- paired counts / rates


def test_paired_counts_table():
    a = np.array([1, 1, 0, 0, 1, 0], dtype=bool)
    b = np.array([1, 0, 1, 0, 0, 0], dtype=bool)
    assert M.paired_counts(a, b) == {"both": 1, "only_a": 2, "only_b": 1, "neither": 2, "n": 6}


def test_paired_counts_accepts_01_and_rejects_bad_input():
    assert M.paired_counts([1, 0], [0, 0])["only_a"] == 1
    with pytest.raises(ValueError):
        M.paired_counts([1, 0], [1])
    with pytest.raises(ValueError):
        M.paired_counts([1, 2], [1, 0])
    with pytest.raises(ValueError):
        M.paired_counts([1.0, np.nan], [1, 0])
    with pytest.raises(ValueError):
        M.paired_counts(np.ones((2, 2)), np.ones((2, 2)))
    with pytest.raises(TypeError):
        M.paired_counts(["yes", "no"], [1, 0])


def test_as_binary_accepts_object_dtype_01_columns():
    # pd.concat of bool and int frames, or a CSV round-trip, yields object-dtype 0/1 columns
    obj = pd.concat([pd.Series([True, False]), pd.Series([1, 0])], ignore_index=True).astype(object)
    assert obj.dtype == object
    assert M.as_binary(obj).tolist() == [True, False, True, False]
    assert M.as_binary(pd.Series([1, 0], dtype=object)).tolist() == [True, False]
    assert M.as_binary(np.array([np.int64(1), 0.0, np.bool_(True)], dtype=object)).tolist() == [True, False, True]
    with pytest.raises(ValueError, match="missing"):
        M.as_binary(pd.Series([1, None], dtype=object))
    with pytest.raises(ValueError, match="missing"):
        M.as_binary(pd.array([True, None], dtype="boolean"))
    with pytest.raises(ValueError):
        M.as_binary(np.array([1, 2], dtype=object))
    with pytest.raises(TypeError):
        M.as_binary(np.array([1, "1"], dtype=object))


def test_detection_rate_and_empty_denominator():
    assert M.detection_rate(np.array([True, False, True, True])) == 0.75
    assert math.isnan(M.detection_rate(np.array([], dtype=bool)))


def test_silent_survival_rate_uses_admissible_denominator():
    classes = [MC.SILENT, MC.SILENT, MC.NON_EQUIVALENT, MC.EQUIVALENT, MC.STRUCTURALLY_INVALID,
               MC.NON_EXECUTABLE, MC.NUMERICALLY_UNSTABLE]
    assert M.silent_survival_rate(classes) == pytest.approx(2 / 3)
    assert M.silent_survival_rate([c.value for c in classes]) == pytest.approx(2 / 3)
    assert M.silent_survival_rate([c.name for c in classes]) == pytest.approx(2 / 3)
    assert math.isnan(M.silent_survival_rate([MC.EQUIVALENT, MC.STRUCTURALLY_INVALID]))
    with pytest.raises(ValueError):
        M.silent_survival_rate(["bogus"])


def test_class_counts_include_zero_classes():
    counts = M.class_counts([MC.SILENT, MC.SILENT])
    assert list(counts) == list(MC)
    assert counts[MC.SILENT] == 2 and counts[MC.EQUIVALENT] == 0


# --------------------------------------------------------------------------- binomial intervals


@pytest.mark.parametrize("method,scipy_method", [("clopper_pearson", "exact"), ("wilson", "wilson")])
def test_proportion_ci_matches_scipy_binomtest(method, scipy_method):
    for n in (1, 2, 5, 10, 24, 40, 137):
        for k in sorted({0, 1, n // 3, n // 2, n - 1, n}):
            for conf in (0.9, 0.95, 0.99):
                lo, hi = M.proportion_ci(k, n, conf, method)
                ref = binomtest(k, n).proportion_ci(confidence_level=conf, method=scipy_method)
                assert lo == pytest.approx(ref.low, abs=1e-10), (k, n, conf)
                assert hi == pytest.approx(ref.high, abs=1e-10), (k, n, conf)


def test_clopper_pearson_zero_events_bound():
    n = 30
    lo, hi = M.proportion_ci(0, n, 0.95)
    assert lo == 0.0
    assert hi == pytest.approx(1 - 0.025 ** (1 / n), rel=1e-10)


def test_proportion_ci_edge_cases():
    assert all(math.isnan(v) for v in M.proportion_ci(0, 0))
    with pytest.raises(ValueError):
        M.proportion_ci(3, 2)
    with pytest.raises(ValueError):
        M.proportion_ci(1, 2, method="wald")
    with pytest.raises(ValueError):
        M.proportion_ci(1, 2, confidence=1.0)
    assert M.proportion_ci(3.0, np.int64(10)) == M.proportion_ci(3, 10)     # whole-number floats are fine
    with pytest.raises(ValueError, match="integer"):
        M.proportion_ci(2.7, 10)                                              # would silently truncate to 2
    with pytest.raises(TypeError):
        M.proportion_ci("3", 10)
    with pytest.raises(TypeError):
        M.proportion_ci(True, 10)
    with pytest.raises(ValueError):
        M.proportion_ci(-1, 10)


def test_false_positive_rate_and_summary():
    d = np.array([0] * 29 + [1], dtype=bool)
    assert M.false_positive_rate(d) == pytest.approx(1 / 30)
    s = M.false_positive_summary(d, clusters=["m1"] * 15 + ["m2"] * 15)
    ref = binomtest(1, 30).proportion_ci(method="exact")
    assert (s["n"], s["n_detected"], s["n_clusters"]) == (30, 1, 2)
    assert s["ci_low"] == pytest.approx(ref.low) and s["ci_high"] == pytest.approx(ref.high)
    assert "independent" in s["ci_method"]
    with pytest.raises(ValueError):
        M.false_positive_summary(d, clusters=["m1"])
    with pytest.raises(TypeError, match="mix"):
        M.false_positive_summary(d, clusters=[1] * 15 + ["1"] * 15)          # would merge into one cluster


# --------------------------------------------------------------------------- cascade / family


def _classes():
    return ([MC.STRUCTURALLY_INVALID] * 2 + [MC.NON_EXECUTABLE] + [MC.NUMERICALLY_UNSTABLE]
            + [MC.EQUIVALENT] * 3 + [MC.NON_EQUIVALENT] * 2 + [MC.SILENT] * 4)


def test_validation_cascade_counts_exhaustive_battery():
    df = M.validation_cascade(_classes())
    counts = dict(zip(df["stage"], df["count"]))
    assert counts == {"total": 13, "schema_valid": 11, "executable": 10, "numerically_stable": 9,
                      "canonical_survivors": 7, "perturbation_detected": 4, "missed_by_battery": 0,
                      "unresolved_survivors": 3}
    assert list(df["stage"]) == list(M.CASCADE_STAGES)
    parents = dict(zip(df["stage"], df["parent"]))
    for stage, parent in parents.items():
        if parent:
            assert counts[stage] <= counts[parent]
    children = [s for s, p in parents.items() if p == "canonical_survivors"]
    assert sum(counts[s] for s in children) == counts["canonical_survivors"]
    assert df["fraction_of_total"].iloc[0] == 1.0


def test_validation_cascade_with_selected_battery_and_inconsistency():
    classes = _classes()
    det = np.zeros(len(classes), dtype=bool)
    det[-4:-2] = True                   # two of four silent mutants detected by the smaller battery
    det[7] = True                       # a NON_EQUIVALENT mutant (not a canonical survivor): ignored
    counts = dict(zip(*M.validation_cascade(classes, det)[["stage", "count"]].T.values))
    # The two missed SILENT mutants are non-equivalent: they must not join the equivalent stage.
    assert counts["perturbation_detected"] == 2 and counts["missed_by_battery"] == 2
    assert counts["unresolved_survivors"] == classes.count(MC.EQUIVALENT) == 3
    assert counts["perturbation_detected"] + counts["missed_by_battery"] + counts["unresolved_survivors"] == 7
    bad = np.zeros(len(classes), dtype=bool)
    bad[4] = True                       # an EQUIVALENT mutant cannot be detected
    with pytest.raises(ValueError, match="inconsistent"):
        M.validation_cascade(classes, bad)


def test_by_family_counts_and_intervals():
    families = ["bio"] * 4 + ["ref"] * 3
    clusters = ["m1", "m1", "m2", "m3", "m1", "m1", "m1"]
    outcomes = {
        "canonical": np.array([1, 0, 0, 0, 1, 0, 0], dtype=bool),
        "selected": np.array([1, 1, 1, 0, 1, 1, 0], dtype=bool),
    }
    df = M.by_family(outcomes, families, clusters=clusters)
    assert len(df) == 6
    row = df[(df.strategy == "selected") & (df.family == "bio")].iloc[0]
    assert (row.n, row.n_detected, row.n_clusters) == (4, 3, 3)
    assert row.rate == pytest.approx(0.75)
    lo, hi = M.proportion_ci(3, 4)
    assert (row.ci_low, row.ci_high) == pytest.approx((lo, hi))
    pooled = df[(df.strategy == "canonical") & (df.family == "all")].iloc[0]
    assert (pooled.n, pooled.n_detected) == (7, 2)
    assert df[(df.family == "ref")].n_clusters.unique().tolist() == [1]
    with pytest.raises(ValueError):
        M.by_family({"x": np.array([1, 0], dtype=bool)}, ["a"])


def test_by_family_writes_enum_labels_by_value():
    from neurosem.schemas import MutationFamily as MF

    fams = [MF.BIOPHYSICAL, MF.BIOPHYSICAL, MF.REFERENCE]
    df = M.by_family({"selected": np.array([1, 0, 1], dtype=bool)}, fams, clusters=["m1", "m2", "m1"])
    assert df["family"].tolist() == ["biophysical", "reference", "all"]
    assert M.as_label(MF.NUMERICAL) == "numerical" and M.as_label(3) == "3"
    with pytest.raises(TypeError, match="mix"):
        M.as_labels([1, "1"])


# --------------------------------------------------------------------------- curves and cost

_DET = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]], dtype=bool)
_PIDS = ["P1", "P2", "P3"]
_COST = {"P1": 1.0, "P2": 2.0, "P3": 4.0}


def test_coverage_curve_hand_computed():
    df = M.coverage_curve(_DET, _PIDS, ["P2", "P1", "P3"], _COST)
    assert df["n_protocols"].tolist() == [0, 1, 2, 3]
    assert df["protocol_id"].tolist() == ["", "P2", "P1", "P3"]
    assert df["n_detected"].tolist() == [0, 2, 3, 4]
    assert df["n_new"].tolist() == [0, 2, 1, 1]
    assert df["detection_rate"].tolist() == pytest.approx([0.0, 0.4, 0.6, 0.8])
    assert df["exhaustive_coverage"].tolist() == pytest.approx([0.0, 0.5, 0.75, 1.0])
    assert df["cumulative_cost"].tolist() == pytest.approx([0.0, 2.0, 3.0, 7.0])
    no_cost = M.coverage_curve(_DET.astype(int), _PIDS, ["P1"])
    assert no_cost["cumulative_cost"].isna().all()


def test_coverage_curve_rejects_bad_order_and_cost():
    with pytest.raises(ValueError):
        M.coverage_curve(_DET, _PIDS, ["P9"])
    with pytest.raises(ValueError):
        M.coverage_curve(_DET, _PIDS, ["P1", "P1"])
    with pytest.raises(ValueError):
        M.coverage_curve(_DET, _PIDS, ["P1"], {"P2": 1.0})
    with pytest.raises(ValueError):
        M.coverage_curve(_DET[:, 0], _PIDS, ["P1"])


def test_protocols_to_reach_levels():
    curve = M.coverage_curve(_DET, _PIDS, ["P2", "P1", "P3"], _COST)
    reach = M.protocols_to_reach(curve, levels=(0.5, 0.75, 0.8, 1.0))
    assert reach["n_protocols"].tolist() == [1, 2, 3, 3]
    assert reach["cumulative_cost"].tolist() == pytest.approx([2.0, 3.0, 7.0, 7.0])
    partial = M.protocols_to_reach(M.coverage_curve(_DET, _PIDS, ["P2"]), levels=(0.5, 1.0))
    assert partial["n_protocols"].iloc[0] == 1 and math.isnan(partial["n_protocols"].iloc[1])


def test_runtime_per_detection():
    det = np.array([1, 0, 1, 0], dtype=bool)
    out = M.runtime_per_detection(np.array([10.0, 20.0, 30.0, 40.0]), det, n_simulations=8)
    assert out["total_runtime_s"] == 100.0 and out["runtime_s_per_detected"] == 50.0
    assert out["simulations_per_detected"] == 4.0
    assert M.runtime_per_detection(5.0, np.zeros(3, dtype=bool))["runtime_s_per_detected"] == math.inf
    assert math.isnan(M.runtime_per_detection(0.0, np.zeros(3, dtype=bool))["runtime_s_per_detected"])
    with pytest.raises(ValueError):
        M.runtime_per_detection(np.array([1.0, -1.0]), np.array([1, 0], dtype=bool))
    with pytest.raises(ValueError):
        M.runtime_per_detection(np.array([1.0, 2.0, 3.0]), np.array([1, 0], dtype=bool))


def test_summarize_draws():
    rates = np.linspace(0.0, 1.0, 101)
    row = M.summarize_draws(rates, "random_count_matched", n_protocols=3)
    assert row["detection_rate"] == pytest.approx(0.5)
    assert row["lower"] == pytest.approx(0.025) and row["upper"] == pytest.approx(0.975)
    assert row["n_draws"] == 101 and math.isnan(row["cost"])
    pd.DataFrame([row])                          # tidy row
    with pytest.raises(ValueError):
        M.summarize_draws(np.array([]), "x")
