"""Paired inference for two validation strategies evaluated on the same mutants.

The specification ("Statistical analysis") requires paired counts, the paired difference
in detection rate, a confidence interval obtained by resampling at the base-model level,
and an exact paired test where assumptions support it. Mutants derived from one base
model share its channels, harness and numerics, so their outcomes are correlated: the
effective sample size is closer to the number of base models than to the number of
mutants. Three complementary procedures are therefore provided:

* :func:`exact_mcnemar` -- the transparent exact paired test on discordant pairs. It
  treats mutants as independent, which clustering violates, so it is reported but never
  used alone.
* :func:`cluster_bootstrap_diff` -- percentile confidence interval from resampling base
  models with replacement.
* :func:`cluster_permutation_test` -- sign-flip test on per-model discordant differences.

Every procedure reports the number of clusters. With fewer than
``MIN_RELIABLE_CLUSTERS`` base models the cluster methods have very few distinct
resamples / sign patterns, so results are flagged unreliable and a
:class:`SmallClusterWarning` is emitted.
"""

from __future__ import annotations

import math
import warnings
from collections.abc import Sequence
from typing import Any

import numpy as np
from scipy import stats

from nexclamp.analysis.metrics import as_binary, as_count, as_labels, paired_counts

MIN_RELIABLE_CLUSTERS = 5
_CHUNK_ROWS = 8192          # resampling rows generated per batch (bounds memory only)
_MAX_EXACT_CLUSTERS = 24    # 2**24 sign patterns is the largest exact enumeration allowed


class SmallClusterWarning(UserWarning):
    """Too few base models for cluster-level resampling to be trustworthy."""


# --------------------------------------------------------------------------- helpers


def _factorize(clusters: Sequence[Any], n: int) -> tuple[np.ndarray, list[str]]:
    """Integer codes for cluster labels, in sorted label order (so results do not depend on row order).

    Labels are compared as strings after enum members are replaced by their values; mixed
    label types (e.g. int ``1`` and str ``'1'``) are rejected rather than merged.
    """
    labels = np.asarray(as_labels(clusters, "clusters"), dtype=str)
    if labels.ndim != 1 or labels.size != n:
        raise ValueError(f"clusters must have one label per unit (got {labels.size}, expected {n})")
    uniq, codes = np.unique(labels, return_inverse=True)
    return codes.astype(np.int64), uniq.tolist()


def _prepare(a: Any, b: Any, clusters: Sequence[Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    a = as_binary(a, "a")
    b = as_binary(b, "b")
    if a.size != b.size:
        raise ValueError(f"a and b must have the same length ({a.size} != {b.size})")
    if a.size == 0:
        raise ValueError("no units to analyse")
    codes, labels = _factorize(clusters, a.size)
    return a, b, codes, labels


def _check_ci(ci: float) -> None:
    if not 0.0 < ci < 1.0:
        raise ValueError("ci must lie in (0, 1)")


def _check_seed(seed: Any) -> int:
    """Require an explicit non-negative integer seed.

    ``default_rng(None)`` would draw fresh OS entropy and silently make an interval or
    p-value irreproducible, so ``None`` (and anything that is not a whole number) is refused.
    """
    if seed is None or isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)):
        raise TypeError(f"seed must be a non-negative integer for reproducibility (got {seed!r})")
    if int(seed) < 0:
        raise ValueError(f"seed must be non-negative (got {seed})")
    return int(seed)


def _check_positive(value: Any, name: str) -> int:
    out = as_count(value, name)
    if out < 1:
        raise ValueError(f"{name} must be >= 1")
    return out


def _small_cluster_message(n_clusters: int, what: str) -> str:
    if n_clusters >= MIN_RELIABLE_CLUSTERS:
        return ""
    return (
        f"only {n_clusters} base-model cluster(s) (< {MIN_RELIABLE_CLUSTERS}): {what}"
    )


def _resample_weights(rng: np.random.Generator, n_clusters: int, n_boot: int):
    """Yield multiplicity matrices ``W[r, g]`` = times cluster g was drawn in resample r.

    Each resample draws ``n_clusters`` base models uniformly with replacement; all mutants
    of a drawn model enter the resample, as many times as the model was drawn.
    """
    done = 0
    while done < n_boot:
        rows = min(_CHUNK_ROWS, n_boot - done)
        idx = rng.integers(0, n_clusters, size=(rows, n_clusters))
        flat = idx + (np.arange(rows, dtype=np.int64) * n_clusters)[:, None]
        yield np.bincount(flat.ravel(), minlength=rows * n_clusters).reshape(rows, n_clusters)
        done += rows


def _percentile(values: np.ndarray, ci: float) -> tuple[float, float]:
    q = (1.0 - ci) / 2.0
    lo, hi = np.quantile(values, [q, 1.0 - q])     # numpy default 'linear' interpolation
    return float(lo), float(hi)


# --------------------------------------------------------------------------- bootstrap


def cluster_bootstrap_diff(
    a: np.ndarray,
    b: np.ndarray,
    clusters: Sequence[Any],
    n_boot: int,
    seed: int,
    ci: float = 0.95,
    keep_distribution: bool = False,
) -> dict[str, Any]:
    """Cluster (base-model) bootstrap for the paired difference in detection rate ``a - b``.

    ``a[i]``/``b[i]`` say whether strategies A and B detect mutant ``i``; ``clusters[i]`` is
    its base model. The statistic is the pooled difference
    ``sum_i (a_i - b_i) / n_mutants``. Each of ``n_boot`` resamples draws the observed number
    of base models with replacement, pools all mutants of the drawn models (with
    multiplicity) and recomputes the pooled difference, so within-model correlation is
    carried into the resamples intact. Larger models therefore weigh more, exactly as in
    the point estimate. The interval is the percentile interval of the resampled
    differences (numpy 'linear' quantiles).

    With G clusters there are at most C(2G-1, G) distinct resamples
    (``n_distinct_resamples``); percentile intervals from few clusters are typically too
    narrow, so ``reliable`` is False and a :class:`SmallClusterWarning` is emitted when
    G < ``MIN_RELIABLE_CLUSTERS``. The resampling is deterministic given ``seed`` (a
    required non-negative integer; numpy PCG64 via ``default_rng``) and invariant to the row
    order of the inputs.
    """
    n_boot = _check_positive(n_boot, "n_boot")
    seed = _check_seed(seed)
    _check_ci(ci)
    a, b, codes, labels = _prepare(a, b, clusters)
    g = len(labels)
    size_g = np.bincount(codes, minlength=g).astype(float)
    a_g = np.bincount(codes, weights=a.astype(float), minlength=g)
    b_g = np.bincount(codes, weights=b.astype(float), minlength=g)

    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot)
    ra = np.empty(n_boot)
    rb = np.empty(n_boot)
    pos = 0
    for w in _resample_weights(rng, g, n_boot):
        denom = w @ size_g                     # >= 1: every drawn cluster holds >= 1 mutant
        sa, sb = w @ a_g, w @ b_g
        end = pos + w.shape[0]
        ra[pos:end] = sa / denom
        rb[pos:end] = sb / denom
        diffs[pos:end] = (sa - sb) / denom
        pos = end

    n = a.size
    rate_a, rate_b = float(a.sum()) / n, float(b.sum()) / n
    lo, hi = _percentile(diffs, ci)
    message = _small_cluster_message(
        g, "the cluster bootstrap has few distinct resamples and its percentile interval is unreliable"
    )
    if message:
        warnings.warn(message, SmallClusterWarning, stacklevel=2)
    out: dict[str, Any] = {
        "statistic": "pooled paired difference in detection rate (a - b)",
        "diff": rate_a - rate_b,
        "rate_a": rate_a,
        "rate_b": rate_b,
        "ci_low": lo,
        "ci_high": hi,
        "rate_a_ci": list(_percentile(ra, ci)),
        "rate_b_ci": list(_percentile(rb, ci)),
        "ci_level": ci,
        "ci_method": "cluster percentile bootstrap (base models resampled with replacement)",
        "boot_se": float(np.std(diffs, ddof=1)) if diffs.size > 1 else float("nan"),
        "n_boot": n_boot,
        "seed": seed,
        "n_mutants": int(n),
        "n_clusters": g,
        "cluster_sizes": {lab: int(s) for lab, s in zip(labels, size_g)},
        "n_distinct_resamples": math.comb(2 * g - 1, g),
        "reliable": g >= MIN_RELIABLE_CLUSTERS,
        "warning": message,
    }
    if keep_distribution:
        out["boot_diffs"] = diffs
    return out


def cluster_bootstrap_rate(
    x: np.ndarray,
    clusters: Sequence[Any],
    n_boot: int,
    seed: int,
    ci: float = 0.95,
    keep_distribution: bool = False,
) -> dict[str, Any]:
    """Cluster bootstrap percentile interval for a single pooled rate (e.g. a detection or
    false-positive rate), using the same base-model resampling as :func:`cluster_bootstrap_diff`."""
    x = as_binary(x, "x")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = cluster_bootstrap_diff(x, np.zeros(x.size, dtype=bool), clusters, n_boot, seed, ci, True)
    for w in caught:                                   # re-emit from the caller's frame
        warnings.warn(w.message, w.category, stacklevel=2)
    out = {
        "statistic": "pooled rate",
        "rate": res["rate_a"],
        "ci_low": res["rate_a_ci"][0],
        "ci_high": res["rate_a_ci"][1],
        **{k: res[k] for k in ("ci_level", "ci_method", "n_boot", "seed", "n_mutants", "n_clusters",
                               "cluster_sizes", "n_distinct_resamples", "reliable", "warning")},
    }
    out["n_units"] = out.pop("n_mutants")
    if keep_distribution:
        out["boot_rates"] = res["boot_diffs"]          # b is all-zero, so the difference is the rate
    return out


# --------------------------------------------------------------------------- exact paired test


def exact_mcnemar(only_a: int, only_b: int) -> float:
    """Exact McNemar test: two-sided exact binomial test on the discordant pairs.

    Under H0 (equal marginal detection probabilities) each discordant mutant is equally
    likely to be ``only_a`` or ``only_b``, so ``only_a ~ Binomial(only_a + only_b, 1/2)``.
    Because that null distribution is symmetric, the two-sided p-value is
    ``min(1, 2 * P(X <= min(only_a, only_b)))``, identical to
    ``scipy.stats.binomtest(only_a, only_a + only_b, 0.5).pvalue``. Returns 1.0 when there
    are no discordant pairs. The test assumes independent mutants; see the module docstring.
    Counts must be whole numbers; strings, booleans and fractional values are refused.
    """
    k_a, k_b = as_count(only_a, "only_a"), as_count(only_b, "only_b")
    n = k_a + k_b
    if n == 0:
        return 1.0
    return float(min(1.0, 2.0 * stats.binom.cdf(min(k_a, k_b), n, 0.5)))


# --------------------------------------------------------------------------- permutation test


def cluster_permutation_details(
    a: np.ndarray,
    b: np.ndarray,
    clusters: Sequence[Any],
    n_perm: int,
    seed: int,
    exact: bool | None = None,
) -> dict[str, Any]:
    """Cluster sign-flip permutation test of equal detection rates, with diagnostics.

    For base model g let ``D_g = only_a_g - only_b_g`` (its discordant difference). The
    statistic is ``T = sum_g D_g`` (``n_mutants`` times the pooled paired difference), and
    the two-sided p-value is the fraction of sign assignments ``s_g in {-1, +1}`` with
    ``|sum_g s_g D_g| >= |T|``.

    Exchangeability assumption: base models are independent, and under H0 swapping the
    labels A and B for *all* mutants of one model at once leaves the distribution of that
    model's outcomes unchanged, i.e. each ``D_g`` is symmetric about zero. Labels are never
    swapped for individual mutants, so within-model correlation is respected. This is a
    null of symmetry per model (slightly stronger than equal pooled rates); clusters with
    ``D_g = 0`` cannot change ``T`` and are dropped from the enumeration.

    With ``G_inf`` informative clusters the exact test cannot give a p-value below
    ``2 ** (1 - G_inf)`` (the identity and the global flip always tie). The test is exact
    (full enumeration of 2**G_inf patterns) when ``exact`` is True, or when ``exact`` is None
    and ``2**G_inf <= n_perm``; otherwise ``n_perm`` random sign patterns give
    ``p = (1 + #{|T*| >= |T|}) / (1 + n_perm)`` (Phipson B, Smyth GK, 2010, Stat Appl Genet
    Mol Biol 9(1):39), which is never zero and never below ``1 / (1 + n_perm)``.
    ``min_attainable_p`` is the floor for the mode actually used: ``2 ** (1 - G_inf)`` when
    exact, ``max(2 ** (1 - G_inf), 1 / (1 + n_perm))`` for Monte Carlo.

    ``reliable`` requires at least ``MIN_RELIABLE_CLUSTERS`` base models *and* at least that
    many informative ones: clusters with ``D_g = 0`` add nothing to the sign-flip
    distribution, so twelve models of which two are discordant give a test that can never
    go below p = 0.5. ``seed`` must be a non-negative integer even when the test is exact,
    so that a call's reproducibility does not depend on which mode was chosen.
    """
    n_perm = _check_positive(n_perm, "n_perm")
    seed = _check_seed(seed)
    a, b, codes, labels = _prepare(a, b, clusters)
    g = len(labels)
    d_all = np.bincount(codes, weights=(a.astype(np.int64) - b.astype(np.int64)), minlength=g)
    d_all = np.rint(d_all).astype(np.int64)
    d = d_all[d_all != 0]
    g_inf = int(d.size)
    t_obs = int(d_all.sum())
    abs_t = abs(t_obs)

    use_exact = exact if exact is not None else (g_inf <= _MAX_EXACT_CLUSTERS and 2**g_inf <= n_perm)
    if use_exact and g_inf > _MAX_EXACT_CLUSTERS:
        raise ValueError(f"exact enumeration limited to {_MAX_EXACT_CLUSTERS} informative clusters (got {g_inf})")

    if g_inf == 0:
        p, used = 1.0, 0
    elif use_exact:
        total = 2**g_inf
        count = 0
        bits = np.arange(g_inf, dtype=np.int64)
        for start in range(0, total, 1 << 16):
            codes_ = np.arange(start, min(total, start + (1 << 16)), dtype=np.int64)
            signs = 1 - 2 * ((codes_[:, None] >> bits) & 1)
            count += int(np.sum(np.abs(signs @ d) >= abs_t))
        p, used = count / total, total
    else:
        rng = np.random.default_rng(seed)
        count = 0
        done = 0
        while done < n_perm:
            rows = min(_CHUNK_ROWS, n_perm - done)
            signs = 1 - 2 * rng.integers(0, 2, size=(rows, g_inf), dtype=np.int64)
            count += int(np.sum(np.abs(signs @ d) >= abs_t))
            done += rows
        p, used = (1 + count) / (1 + n_perm), n_perm

    if g_inf == 0:
        min_p = 1.0
    else:
        min_p = min(1.0, 2.0 ** (1 - g_inf))
        if not use_exact:
            min_p = max(min_p, 1.0 / (1 + n_perm))
    message = _small_cluster_message(
        g, "the sign-flip test has few distinct sign patterns and low attainable significance"
    )
    if not message and g_inf < MIN_RELIABLE_CLUSTERS:
        message = (
            f"only {g_inf} of {g} base-model clusters have a non-zero discordant difference "
            f"(< {MIN_RELIABLE_CLUSTERS}): the sign-flip test cannot give p below {min_p:.3g}"
        )
    if message:
        warnings.warn(message, SmallClusterWarning, stacklevel=2)
    return {
        "p_value": float(p),
        "statistic": t_obs,
        "statistic_definition": "sum over base models of (only_a - only_b)",
        "per_cluster_difference": {lab: int(v) for lab, v in zip(labels, d_all)},
        "n_clusters": g,
        "n_informative_clusters": g_inf,
        "exact": bool(use_exact) if g_inf else True,
        "n_perm": used,
        "seed": seed,
        "min_attainable_p": min_p,
        "reliable": g >= MIN_RELIABLE_CLUSTERS and g_inf >= MIN_RELIABLE_CLUSTERS,
        "warning": message,
        "assumption": "independent base models; per-model discordant difference symmetric about 0 under H0",
    }


def cluster_permutation_test(
    a: np.ndarray,
    b: np.ndarray,
    clusters: Sequence[Any],
    n_perm: int,
    seed: int,
    exact: bool | None = None,
) -> float:
    """Two-sided p-value of the cluster sign-flip test (see :func:`cluster_permutation_details`)."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        p = cluster_permutation_details(a, b, clusters, n_perm, seed, exact)["p_value"]
    for w in caught:
        warnings.warn(w.message, w.category, stacklevel=2)
    return p


# --------------------------------------------------------------------------- combined report


def paired_comparison(
    a: np.ndarray,
    b: np.ndarray,
    clusters: Sequence[Any],
    n_boot: int,
    n_perm: int,
    seed: int,
    ci: float = 0.95,
) -> dict[str, Any]:
    """All paired statistics for strategies A and B on the same mutants, in one JSON-able dict.

    Contains the paired counts, both rates and their difference, the exact McNemar p-value
    (mutants treated as independent), the cluster bootstrap interval and the cluster
    sign-flip p-value. The permutation stream uses ``seed + 1`` so the two procedures do not
    share random numbers. At most one :class:`SmallClusterWarning` is emitted. The top-level
    ``reliable`` is True only when both cluster procedures are reliable (enough base models,
    and enough of them with discordant mutants for the sign-flip test).
    """
    seed = _check_seed(seed)
    counts = paired_counts(a, b)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        boot = cluster_bootstrap_diff(a, b, clusters, n_boot, seed, ci)
        perm = cluster_permutation_details(a, b, clusters, n_perm, seed + 1)
    small_emitted = False
    for w in caught:
        if issubclass(w.category, SmallClusterWarning):
            if small_emitted:
                continue
            small_emitted = True
        warnings.warn(w.message, w.category, stacklevel=2)
    n = counts["n"]
    return {
        "counts": counts,
        "rate_a": (counts["both"] + counts["only_a"]) / n,
        "rate_b": (counts["both"] + counts["only_b"]) / n,
        "diff": (counts["only_a"] - counts["only_b"]) / n,
        "exact_mcnemar_p": exact_mcnemar(counts["only_a"], counts["only_b"]),
        "exact_mcnemar_note": "two-sided exact binomial on discordant pairs; assumes independent mutants",
        "cluster_bootstrap": boot,
        "cluster_permutation": perm,
        "n_clusters": boot["n_clusters"],
        "n_informative_clusters": perm["n_informative_clusters"],
        "reliable": bool(boot["reliable"] and perm["reliable"]),
    }
