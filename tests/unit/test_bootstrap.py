"""Unit tests for nexclamp.analysis.bootstrap: exactness against scipy, cluster-level
resampling, determinism, small-cluster flags and calibration under clustered nulls."""

from __future__ import annotations

import itertools
import math
import warnings

import numpy as np
import pytest
from scipy.stats import binomtest

from nexclamp.analysis import bootstrap as B
from nexclamp.analysis.bootstrap import SmallClusterWarning


def _units(per_cluster: list[list[tuple[int, int]]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build (a, b, clusters) from per-cluster lists of (a_i, b_i) pairs."""
    a, b, cl = [], [], []
    for g, pairs in enumerate(per_cluster):
        for ai, bi in pairs:
            a.append(ai)
            b.append(bi)
            cl.append(f"model_{g:02d}")
    return np.array(a, dtype=bool), np.array(b, dtype=bool), np.array(cl)


def _clustered_null(rng: np.random.Generator, n_clusters: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Null data with strong within-model correlation of the paired difference.

    Each model has a baseline detection probability and a model-specific shift +-delta that
    favours A or B for all its mutants; the shift is symmetric across models, so the
    expected pooled difference is zero but mutants within a model are far from independent.
    """
    a, b, cl = [], [], []
    for g in range(n_clusters):
        n = int(rng.integers(3, 13))
        base = rng.uniform(0.3, 0.7)
        delta = rng.choice([-0.25, 0.25])
        a.append(rng.random(n) < base + delta)
        b.append(rng.random(n) < base - delta)
        cl += [f"m{g}"] * n
    return np.concatenate(a), np.concatenate(b), np.array(cl)


# --------------------------------------------------------------------------- exact McNemar


def test_exact_mcnemar_matches_scipy_binomtest_grid():
    for only_a in range(31):
        for only_b in range(31):
            n = only_a + only_b
            ref = 1.0 if n == 0 else binomtest(only_a, n, 0.5, alternative="two-sided").pvalue
            assert B.exact_mcnemar(only_a, only_b) == pytest.approx(ref, rel=1e-9, abs=1e-300), (only_a, only_b)


@pytest.mark.parametrize("only_a,only_b", [(120, 80), (3, 250), (500, 480), (0, 1)])
def test_exact_mcnemar_matches_scipy_large_counts(only_a, only_b):
    ref = binomtest(only_a, only_a + only_b, 0.5).pvalue
    assert B.exact_mcnemar(only_a, only_b) == pytest.approx(ref, rel=1e-9)


def test_exact_mcnemar_known_values_and_validation():
    assert B.exact_mcnemar(0, 5) == pytest.approx(0.0625)      # 2 * 0.5**5
    assert B.exact_mcnemar(5, 5) == 1.0
    assert B.exact_mcnemar(0, 0) == 1.0
    assert B.exact_mcnemar(2, 9) == B.exact_mcnemar(9, 2)
    assert B.exact_mcnemar(np.int64(3), np.int64(1)) == B.exact_mcnemar(3, 1)
    assert B.exact_mcnemar(3.0, 1) == B.exact_mcnemar(3, 1)
    with pytest.raises(ValueError):
        B.exact_mcnemar(-1, 3)
    with pytest.raises(ValueError):
        B.exact_mcnemar(2.5, 3)
    with pytest.raises(TypeError):
        B.exact_mcnemar("3", 1)
    with pytest.raises(TypeError):
        B.exact_mcnemar(True, 1)


# --------------------------------------------------------------------------- cluster bootstrap


def test_bootstrap_point_estimate_is_pooled_paired_difference():
    rng = np.random.default_rng(1)
    a, b, cl = _clustered_null(rng, 8)
    res = B.cluster_bootstrap_diff(a, b, cl, n_boot=500, seed=3)
    assert res["diff"] == pytest.approx(a.mean() - b.mean())
    assert res["rate_a"] == pytest.approx(a.mean()) and res["rate_b"] == pytest.approx(b.mean())
    assert res["n_mutants"] == a.size and res["n_clusters"] == 8
    assert sum(res["cluster_sizes"].values()) == a.size
    assert res["ci_low"] <= res["ci_high"]
    assert res["reliable"] and res["warning"] == ""
    assert "boot_diffs" not in res


def test_bootstrap_resamples_base_models_not_mutants():
    # Model A: 10 mutants detected only by A; model B: 10 mutants detected by neither.
    a, b, cl = _units([[(1, 0)] * 10, [(0, 0)] * 10])
    with pytest.warns(SmallClusterWarning):
        res = B.cluster_bootstrap_diff(a, b, cl, n_boot=20000, seed=7, keep_distribution=True)
    values, counts = np.unique(res["boot_diffs"], return_counts=True)
    # Only three resamples exist: {A,A} -> 1, {A,B} -> 0.5, {B,B} -> 0 (a mutant-level
    # bootstrap would produce many intermediate values).
    assert values.tolist() == pytest.approx([0.0, 0.5, 1.0])
    assert (counts / counts.sum()).tolist() == pytest.approx([0.25, 0.5, 0.25], abs=0.015)
    assert res["n_distinct_resamples"] == 3 and not res["reliable"]


def test_bootstrap_pools_mutants_of_unequal_models():
    # Model A: 2 mutants, both only_a; model B: 8 mutants, no discordance. Mixed resample = 2/10.
    a, b, cl = _units([[(1, 0)] * 2, [(1, 1)] * 8])
    with pytest.warns(SmallClusterWarning):
        res = B.cluster_bootstrap_diff(a, b, cl, n_boot=4000, seed=11, keep_distribution=True)
    assert np.unique(res["boot_diffs"]).tolist() == pytest.approx([0.0, 0.2, 1.0])
    assert res["diff"] == pytest.approx(0.2)


def test_bootstrap_deterministic_and_row_order_invariant():
    rng = np.random.default_rng(5)
    a, b, cl = _clustered_null(rng, 7)
    r1 = B.cluster_bootstrap_diff(a, b, cl, n_boot=3000, seed=42, keep_distribution=True)
    r2 = B.cluster_bootstrap_diff(a, b, cl, n_boot=3000, seed=42, keep_distribution=True)
    perm = rng.permutation(a.size)
    r3 = B.cluster_bootstrap_diff(a[perm], b[perm], cl[perm], n_boot=3000, seed=42, keep_distribution=True)
    r4 = B.cluster_bootstrap_diff(a, b, cl, n_boot=3000, seed=43, keep_distribution=True)
    np.testing.assert_array_equal(r1["boot_diffs"], r2["boot_diffs"])
    np.testing.assert_allclose(r1["boot_diffs"], r3["boot_diffs"], rtol=0, atol=1e-12)
    assert not np.array_equal(r1["boot_diffs"], r4["boot_diffs"])


def test_bootstrap_chunking_does_not_change_results(monkeypatch):
    rng = np.random.default_rng(8)
    a, b, cl = _clustered_null(rng, 6)
    assert 1000 < B._CHUNK_ROWS                     # reference run: one batch
    ref = B.cluster_bootstrap_diff(a, b, cl, n_boot=1000, seed=1, keep_distribution=True)
    monkeypatch.setattr(B, "_CHUNK_ROWS", 7)        # 143 batches, the last one partial
    chunked = B.cluster_bootstrap_diff(a, b, cl, n_boot=1000, seed=1, keep_distribution=True)
    np.testing.assert_array_equal(ref["boot_diffs"], chunked["boot_diffs"])


def test_permutation_monte_carlo_chunking_does_not_change_results(monkeypatch):
    rng = np.random.default_rng(9)
    a, b, cl = _clustered_null(rng, 14)
    assert 1999 < B._CHUNK_ROWS
    ref = B.cluster_permutation_details(a, b, cl, n_perm=1999, seed=4, exact=False)
    monkeypatch.setattr(B, "_CHUNK_ROWS", 7)
    chunked = B.cluster_permutation_details(a, b, cl, n_perm=1999, seed=4, exact=False)
    assert not ref["exact"] and chunked["p_value"] == ref["p_value"]


def test_small_cluster_flag_threshold():
    four = _units([[(1, 0), (0, 0)]] * 4)
    with pytest.warns(SmallClusterWarning, match="only 4"):
        res = B.cluster_bootstrap_diff(*four, n_boot=200, seed=0)
    assert not res["reliable"] and res["n_distinct_resamples"] == math.comb(7, 4)
    five = _units([[(1, 0), (0, 0)]] * 5)
    with warnings.catch_warnings():
        warnings.simplefilter("error", SmallClusterWarning)
        res5 = B.cluster_bootstrap_diff(*five, n_boot=200, seed=0)
    assert res5["reliable"] and res5["n_clusters"] == B.MIN_RELIABLE_CLUSTERS


def test_bootstrap_ci_coverage_under_clustered_null():
    """Cluster percentile intervals should cover the true difference (0) near nominally when
    there are many base models, and much better than a bootstrap that ignores clustering."""
    rng = np.random.default_rng(20260913)
    n_sims, n_boot = 200, 800
    cover_cluster = cover_naive = 0
    for s in range(n_sims):
        a, b, cl = _clustered_null(rng, 30)
        res = B.cluster_bootstrap_diff(a, b, cl, n_boot=n_boot, seed=s)
        cover_cluster += res["ci_low"] <= 0.0 <= res["ci_high"]
        naive = B.cluster_bootstrap_diff(a, b, np.arange(a.size), n_boot=n_boot, seed=s)   # every mutant its own cluster
        cover_naive += naive["ci_low"] <= 0.0 <= naive["ci_high"]
    assert 0.88 <= cover_cluster / n_sims <= 0.99
    assert cover_naive < cover_cluster


def test_cluster_bootstrap_rate():
    a, _, cl = _units([[(1, 0)] * 3 + [(0, 0)]] * 6)
    res = B.cluster_bootstrap_rate(a, cl, n_boot=500, seed=2, keep_distribution=True)
    assert res["rate"] == pytest.approx(0.75)
    # every model has the same rate, so every resample reproduces it exactly
    assert np.allclose(res["boot_rates"], 0.75) and res["ci_low"] == pytest.approx(0.75)
    assert res["n_units"] == 24 and res["n_clusters"] == 6


def test_bootstrap_input_validation():
    a, b, cl = _units([[(1, 0)]] * 6)
    with pytest.raises(ValueError):
        B.cluster_bootstrap_diff(a, b, cl[:-1], n_boot=10, seed=0)
    with pytest.raises(ValueError):
        B.cluster_bootstrap_diff(a, b, cl, n_boot=0, seed=0)
    with pytest.raises(ValueError):
        B.cluster_bootstrap_diff(a, b, cl, n_boot=10, seed=0, ci=1.0)
    with pytest.raises(ValueError):
        B.cluster_bootstrap_diff(a[:-1], b, cl, n_boot=10, seed=0)
    with pytest.raises(ValueError):
        B.cluster_bootstrap_diff(a, b, cl, n_boot=10.5, seed=0)


@pytest.mark.parametrize("seed", [None, 1.5, "1", True, -1])
def test_seeded_functions_require_integer_seed(seed):
    a, b, cl = _units([[(1, 0), (0, 0)]] * 6)
    for call in (
        lambda: B.cluster_bootstrap_diff(a, b, cl, n_boot=10, seed=seed),
        lambda: B.cluster_bootstrap_rate(a, cl, n_boot=10, seed=seed),
        lambda: B.cluster_permutation_details(a, b, cl, n_perm=10, seed=seed),
        lambda: B.cluster_permutation_test(a, b, cl, n_perm=10, seed=seed),
        lambda: B.paired_comparison(a, b, cl, n_boot=10, n_perm=10, seed=seed),
    ):
        with pytest.raises((TypeError, ValueError), match="seed"):
            call()
    assert B.cluster_bootstrap_diff(a, b, cl, n_boot=10, seed=np.int64(3))["seed"] == 3


def test_cluster_labels_enum_by_value_and_mixed_types_rejected():
    from nexclamp.schemas import MutationFamily as MF

    a, b, _ = _units([[(1, 0)]] * 6)
    enum_cl = [MF.BIOPHYSICAL, MF.REFERENCE, MF.NUMERICAL, MF.STIMULUS, MF.BIOPHYSICAL, MF.REFERENCE]
    with pytest.warns(SmallClusterWarning):
        res = B.cluster_bootstrap_diff(a, b, enum_cl, n_boot=10, seed=0)
    assert sorted(res["cluster_sizes"]) == ["biophysical", "numerical", "reference", "stimulus"]
    with pytest.raises(TypeError, match="mix"):
        B.cluster_bootstrap_diff(a, b, [1, "1", 2, "2", 3, "3"], n_boot=10, seed=0)
    with pytest.raises(TypeError, match="mix"):
        B.cluster_permutation_details(a, b, [1, "1", 2, "2", 3, "3"], n_perm=10, seed=0)


# --------------------------------------------------------------------------- cluster permutation


def _brute_force_sign_flip(d: np.ndarray) -> float:
    t = abs(int(d.sum()))
    hits = sum(abs(int(np.dot(s, d))) >= t for s in itertools.product((-1, 1), repeat=d.size))
    return hits / 2**d.size


def test_permutation_exact_hand_computed():
    # D = [2, 1, 1]: sign-flip sums {+-4, +-2, +-2, 0, 0}; |T*| >= 4 for 2 of 8 patterns.
    a, b, cl = _units([[(1, 0), (1, 0)], [(1, 0), (1, 1)], [(0, 0), (1, 0)]])
    with pytest.warns(SmallClusterWarning):
        det = B.cluster_permutation_details(a, b, cl, n_perm=1000, seed=0)
    assert det["p_value"] == pytest.approx(0.25)
    assert det["exact"] and det["n_perm"] == 8 and det["statistic"] == 4
    assert det["min_attainable_p"] == pytest.approx(0.25)
    assert det["per_cluster_difference"] == {"model_00": 2, "model_01": 1, "model_02": 1}


@pytest.mark.filterwarnings("ignore::nexclamp.analysis.bootstrap.SmallClusterWarning")
def test_permutation_matches_brute_force_enumeration():
    rng = np.random.default_rng(99)
    for _ in range(20):
        per_cluster = []
        for _g in range(8):
            n = int(rng.integers(1, 6))
            per_cluster.append([(int(rng.random() < 0.6), int(rng.random() < 0.4)) for _ in range(n)])
        a, b, cl = _units(per_cluster)
        d = np.array([sum(x - y for x, y in pairs) for pairs in per_cluster])
        p = B.cluster_permutation_test(a, b, cl, n_perm=10**6, seed=0)
        assert p == pytest.approx(_brute_force_sign_flip(d), abs=1e-12)


def test_permutation_monte_carlo_agrees_with_exact():
    rng = np.random.default_rng(3)
    a, b, cl = _clustered_null(rng, 12)
    exact = B.cluster_permutation_details(a, b, cl, n_perm=10, seed=0, exact=True)
    mc = B.cluster_permutation_details(a, b, cl, n_perm=2000, seed=0, exact=False)
    assert exact["exact"] and not mc["exact"] and mc["n_perm"] == 2000
    assert mc["p_value"] >= 1 / 2001
    assert abs(mc["p_value"] - exact["p_value"]) < 0.03
    g_inf = exact["n_informative_clusters"]
    assert exact["min_attainable_p"] == pytest.approx(2.0 ** (1 - g_inf))
    assert mc["min_attainable_p"] == pytest.approx(max(2.0 ** (1 - g_inf), 1 / 2001))


def test_monte_carlo_min_attainable_p_reflects_n_perm():
    a, b, cl = _units([[(1, 0)]] * 20)                 # 20 informative clusters, all D_g = +1
    mc = B.cluster_permutation_details(a, b, cl, n_perm=999, seed=0)
    assert not mc["exact"]
    assert mc["min_attainable_p"] == pytest.approx(1 / 1000)      # not 2**-19
    assert mc["p_value"] >= mc["min_attainable_p"]


def test_permutation_reliability_counts_informative_clusters():
    # 12 base models, but only 2 carry any discordant mutant: p can never go below 0.5.
    per_cluster = [[(1, 0), (1, 0)]] * 2 + [[(1, 1), (0, 0)]] * 10
    a, b, cl = _units(per_cluster)
    with pytest.warns(SmallClusterWarning, match="only 2 of 12"):
        det = B.cluster_permutation_details(a, b, cl, n_perm=1000, seed=0)
    assert det["n_clusters"] == 12 and det["n_informative_clusters"] == 2
    assert det["p_value"] == pytest.approx(0.5) and det["min_attainable_p"] == pytest.approx(0.5)
    assert not det["reliable"]
    with pytest.warns(SmallClusterWarning, match="only 2 of 12"):
        rep = B.paired_comparison(a, b, cl, n_boot=200, n_perm=1000, seed=0)
    assert rep["cluster_bootstrap"]["reliable"] and not rep["reliable"]
    assert rep["n_informative_clusters"] == 2


def test_sign_flip_is_at_cluster_level():
    # 100 mutants detected only by A, but from just two models: the cluster test cannot
    # go below 2**(1-2) = 0.5, whereas McNemar (independence) gives a tiny p-value.
    a, b, cl = _units([[(1, 0)] * 50, [(1, 0)] * 50])
    with pytest.warns(SmallClusterWarning):
        p = B.cluster_permutation_test(a, b, cl, n_perm=1000, seed=0)
    assert p == pytest.approx(0.5)
    assert B.exact_mcnemar(100, 0) < 1e-25


def test_permutation_no_discordance_and_all_positive():
    a, b, cl = _units([[(1, 1), (0, 0)]] * 6)
    with pytest.warns(SmallClusterWarning, match="only 0 of 6"):
        assert B.cluster_permutation_test(a, b, cl, n_perm=100, seed=0) == 1.0
    a2, b2, cl2 = _units([[(1, 0)]] * 12)
    with warnings.catch_warnings():
        warnings.simplefilter("error", SmallClusterWarning)
        det = B.cluster_permutation_details(a2, b2, cl2, n_perm=5000, seed=0)
    assert det["exact"] and det["p_value"] == pytest.approx(2 / 4096)
    assert det["p_value"] == pytest.approx(det["min_attainable_p"]) and det["reliable"]


@pytest.mark.filterwarnings("ignore::nexclamp.analysis.bootstrap.SmallClusterWarning")
def test_permutation_type_one_error_under_clustered_null():
    rng = np.random.default_rng(12345)
    n_sims, rejections = 300, 0
    for _ in range(n_sims):
        a, b, cl = _clustered_null(rng, 10)
        rejections += B.cluster_permutation_test(a, b, cl, n_perm=2048, seed=0) <= 0.05
    assert rejections / n_sims <= 0.07


# --------------------------------------------------------------------------- combined report


def test_paired_comparison_report_is_consistent():
    rng = np.random.default_rng(17)
    a, b, cl = _clustered_null(rng, 9)
    rep = B.paired_comparison(a, b, cl, n_boot=1000, n_perm=4096, seed=5)
    c = rep["counts"]
    assert rep["diff"] == pytest.approx(rep["cluster_bootstrap"]["diff"])
    assert rep["exact_mcnemar_p"] == B.exact_mcnemar(c["only_a"], c["only_b"])
    assert rep["cluster_permutation"]["statistic"] == c["only_a"] - c["only_b"]
    assert rep["n_clusters"] == 9 and rep["reliable"]
    small = _units([[(1, 0), (0, 1), (1, 0)]] * 3)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        B.paired_comparison(*small, n_boot=100, n_perm=100, seed=0)
    assert sum(issubclass(w.category, SmallClusterWarning) for w in caught) == 1
