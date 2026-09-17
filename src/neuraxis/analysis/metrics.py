"""Descriptive evaluation metrics (ARCHITECTURE.md section 3.8; spec "Secondary endpoints").

Every function here is a deterministic function of per-unit binary outcomes (one unit =
one mutant or one valid transformation). The binomial intervals in this module treat
units as independent and say so in their ``ci_method`` label. Mutants of one base model
are correlated, so inference for the primary comparison must use the cluster-aware
procedures in :mod:`neuraxis.analysis.bootstrap`; these intervals are descriptive.

Empty denominators return ``nan`` rather than raising, so that tables stay rectangular
and an undefined rate is visibly undefined instead of silently zero.
"""

from __future__ import annotations

import enum
import math
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from neuraxis.schemas import MutantClass

CI_METHODS = ("clopper_pearson", "wilson")

CASCADE_STAGES = (
    "total",
    "schema_valid",
    "executable",
    "numerically_stable",
    "canonical_survivors",
    "perturbation_detected",
    "missed_by_battery",
    "unresolved_survivors",
)


# --------------------------------------------------------------------------- helpers


def as_label(value: Any) -> str:
    """String form of a group label (family, category, base-model id).

    Enum members are replaced by their ``value`` first: on Python >= 3.11 ``str()`` of a
    ``(str, Enum)`` member is ``'MutationFamily.BIOPHYSICAL'``, not ``'biophysical'``, which
    would leak class-qualified names into tables and figures.
    """
    if isinstance(value, enum.Enum):
        value = value.value
    return str(value)


def _label_kind(value: Any) -> str:
    if isinstance(value, enum.Enum):
        value = value.value
    if isinstance(value, (bool, np.bool_)):
        return "bool"
    if isinstance(value, str):
        return "str"
    if isinstance(value, (int, np.integer)):
        return "int"
    return type(value).__name__


def as_labels(values: Sequence[Any], name: str = "labels") -> list[str]:
    """:func:`as_label` applied element-wise, refusing labels of mixed types.

    Labels are compared as strings, so ``1`` and ``'1'`` would silently become one group;
    mixing kinds (e.g. int and str ids) is therefore rejected rather than guessed at.
    """
    vals = list(values)
    kinds = {_label_kind(v) for v in vals}
    if len(kinds) > 1:
        raise TypeError(f"{name} mix label types {sorted(kinds)}; use one type (e.g. all str) for group ids")
    return [as_label(v) for v in vals]


def as_count(value: Any, name: str = "count") -> int:
    """Return ``value`` as a non-negative ``int``, rejecting anything that is not a whole number.

    Strings, booleans and non-integer floats are refused instead of being truncated, because
    a silently rounded count changes an interval or p-value without any visible error.
    """
    if isinstance(value, (bool, np.bool_)):
        raise TypeError(f"{name} must be an integer count (got bool)")
    if isinstance(value, (int, np.integer)):
        out = int(value)
    elif isinstance(value, (float, np.floating)):
        if not math.isfinite(float(value)) or not float(value).is_integer():
            raise ValueError(f"{name} must be an integer count (got {value!r})")
        out = int(value)
    else:
        raise TypeError(f"{name} must be an integer count (got {type(value).__name__})")
    if out < 0:
        raise ValueError(f"{name} must be non-negative (got {out})")
    return out


def _is_missing(v: Any) -> bool:
    if v is None or v is pd.NA or v is pd.NaT:
        return True
    return isinstance(v, (float, np.floating)) and not math.isfinite(float(v))


def as_binary(x: Any, name: str = "outcome") -> np.ndarray:
    """Return ``x`` as a 1-D boolean array, rejecting anything that is not clearly 0/1.

    NaN is rejected on purpose: an undefined outcome (e.g. a crashed run) must be resolved
    by the classification rules before it reaches a rate, never coerced to "not detected".
    Object arrays (as produced by ``pd.concat`` or CSV round-trips) are accepted when every
    element is a boolean or a number equal to 0 or 1.
    """
    arr = np.asarray(x)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional (got shape {arr.shape})")
    if arr.dtype == bool:
        return arr
    if arr.size == 0:
        return np.zeros(0, dtype=bool)
    if arr.dtype.kind in "iuf":
        if arr.dtype.kind == "f" and not np.all(np.isfinite(arr)):
            raise ValueError(f"{name} contains NaN or infinite values; resolve undefined outcomes first")
        if not np.all((arr == 0) | (arr == 1)):
            raise ValueError(f"{name} must contain only booleans or 0/1 values")
        return arr.astype(bool)
    if arr.dtype == object:
        out = np.empty(arr.size, dtype=bool)
        for i, v in enumerate(arr):
            if isinstance(v, (bool, np.bool_)):
                out[i] = bool(v)
            elif _is_missing(v):
                raise ValueError(f"{name} contains missing values; resolve undefined outcomes first")
            elif isinstance(v, (int, np.integer, float, np.floating)) and v in (0, 1):
                out[i] = v == 1
            elif isinstance(v, (int, np.integer, float, np.floating)):
                raise ValueError(f"{name} must contain only booleans or 0/1 values (got {v!r})")
            else:
                raise TypeError(f"{name} must be boolean or 0/1 numeric (got element of type {type(v).__name__})")
        return out
    raise TypeError(f"{name} must be boolean or 0/1 numeric (got dtype {arr.dtype})")


def _as_classes(classes: Sequence[MutantClass | str]) -> list[MutantClass]:
    out = []
    for c in classes:
        if isinstance(c, MutantClass):
            out.append(c)
            continue
        try:
            out.append(MutantClass(c))
        except ValueError:
            try:
                out.append(MutantClass[str(c)])
            except KeyError:
                raise ValueError(f"unknown mutant class {c!r}") from None
    return out


def _rate(k: int, n: int) -> float:
    return float(k) / n if n > 0 else float("nan")


# --------------------------------------------------------------------------- counts and rates


def paired_counts(a: np.ndarray, b: np.ndarray) -> dict[str, int]:
    """Paired 2x2 table for two strategies evaluated on the same units.

    Returns ``both``, ``only_a``, ``only_b``, ``neither`` and ``n``. The spec asks for these
    transparent counts to be reported alongside any aggregate difference.
    """
    a = as_binary(a, "a")
    b = as_binary(b, "b")
    if a.shape != b.shape:
        raise ValueError(f"a and b must have the same length ({a.size} != {b.size})")
    return {
        "both": int(np.sum(a & b)),
        "only_a": int(np.sum(a & ~b)),
        "only_b": int(np.sum(~a & b)),
        "neither": int(np.sum(~a & ~b)),
        "n": int(a.size),
    }


def detection_rate(detected_any: np.ndarray) -> float:
    """Fraction of units detected. ``detected_any[i]`` is True when any protocol-feature test
    of the evaluated battery detected unit ``i``. The caller chooses the denominator (for the
    primary endpoint: admissible mutants only, i.e. classes NON_EQUIVALENT and SILENT)."""
    d = as_binary(detected_any, "detected_any")
    return _rate(int(d.sum()), d.size)


def class_counts(classes: Sequence[MutantClass | str]) -> dict[MutantClass, int]:
    """Counts for all six classes in enum order (zeros included)."""
    cls = _as_classes(classes)
    return {c: sum(1 for x in cls if x is c) for c in MutantClass}


def silent_survival_rate(classes: Sequence[MutantClass | str]) -> float:
    """Silent-survival rate after canonical testing = SILENT / (NON_EQUIVALENT + SILENT).

    The denominator is the admissible non-equivalent mutants (reproducible divergence
    somewhere in the exhaustive battery), matching RQ1 and the MutantClass docstring.
    Invalid, non-executable, unstable and equivalent-within-tested-domain mutants are
    excluded because canonical survival is only meaningful for mutants that are known to
    differ; including equivalent mutants would inflate the rate with changes no test
    could detect.
    """
    counts = class_counts(classes)
    silent = counts[MutantClass.SILENT]
    admissible = silent + counts[MutantClass.NON_EQUIVALENT]
    return _rate(silent, admissible)


def false_positive_rate(transform_detected: np.ndarray) -> float:
    """Fraction of valid transformations (or no-change controls) flagged as detected.

    These variants are constructed to preserve tested behaviour, so every detection is a
    false positive of the validator at the calibrated tolerances.
    """
    d = as_binary(transform_detected, "transform_detected")
    return _rate(int(d.sum()), d.size)


def proportion_ci(k: int, n: int, confidence: float = 0.95, method: str = "clopper_pearson") -> tuple[float, float]:
    """Two-sided confidence interval for a binomial proportion ``k / n``.

    ``clopper_pearson`` (default): exact interval from beta quantiles
    (Clopper CJ, Pearson ES, 1934, Biometrika 26(4):404-413). Its coverage is guaranteed to
    be at least the nominal level for every true proportion, at the price of being
    conservative. That guarantee is why it is the default for false-positive rates: the
    claim of interest is an upper bound ("false positives are low") on counts that are
    expected to be near zero with 24-40 transformations, where approximate intervals can
    under-cover, and when k = 0 it gives the exact one-sided-style bound 1 - (alpha/2)^(1/n).

    ``wilson``: score interval (Wilson EB, 1927, JASA 22(158):209-212), recommended by
    Brown, Cai & DasGupta (2001, Statistical Science 16(2):101-133) for its closer-to-nominal
    average coverage; offered for sensitivity analyses.

    Both assume independent units. Returns ``(nan, nan)`` when ``n == 0``. ``k`` and ``n``
    must be whole numbers (see :func:`as_count`).
    """
    k, n = as_count(k, "k"), as_count(n, "n")
    if k > n:
        raise ValueError(f"need 0 <= k <= n (got k={k}, n={n})")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    if n == 0:
        return float("nan"), float("nan")
    alpha = 1.0 - confidence
    if method == "clopper_pearson":
        lo = 0.0 if k == 0 else float(stats.beta.ppf(alpha / 2, k, n - k + 1))
        hi = 1.0 if k == n else float(stats.beta.ppf(1 - alpha / 2, k + 1, n - k))
        return lo, hi
    if method == "wilson":
        z = float(stats.norm.ppf(1 - alpha / 2))
        p = k / n
        denom = 1.0 + z * z / n
        centre = (p + z * z / (2 * n)) / denom
        half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
        return max(0.0, centre - half), min(1.0, centre + half)
    raise ValueError(f"method must be one of {CI_METHODS} (got {method!r})")


def false_positive_summary(
    transform_detected: np.ndarray,
    clusters: Sequence[str] | None = None,
    confidence: float = 0.95,
    method: str = "clopper_pearson",
) -> dict[str, Any]:
    """False-positive count, rate and binomial interval (see :func:`proportion_ci`).

    ``n_clusters`` is reported when base-model ids are given, as a reminder that the
    interval assumes independence; use ``bootstrap.cluster_bootstrap_rate`` for a
    cluster-aware interval when enough base models exist.
    """
    d = as_binary(transform_detected, "transform_detected")
    k, n = int(d.sum()), int(d.size)
    lo, hi = proportion_ci(k, n, confidence, method)
    out: dict[str, Any] = {
        "n": n,
        "n_detected": k,
        "rate": _rate(k, n),
        "ci_low": lo,
        "ci_high": hi,
        "ci_level": confidence,
        "ci_method": f"{method} (units treated as independent)",
    }
    if clusters is not None:
        if len(clusters) != n:
            raise ValueError("clusters must have one entry per transformation")
        out["n_clusters"] = len(set(as_labels(clusters, "clusters")))
    return out


# --------------------------------------------------------------------------- breakdowns


def validation_cascade(
    classes: Sequence[MutantClass | str], battery_detected: np.ndarray | None = None
) -> pd.DataFrame:
    """Counts for the validation-cascade figure (spec "Required figures" 2).

    Stages (each a subset of its ``parent``):
      total -> schema_valid (not class 1) -> executable (not classes 1-2)
      -> numerically_stable (not classes 1-3)
      -> canonical_survivors (classes 4 and 6: no canonical detection)
      which is partitioned into
        perturbation_detected  SILENT and detected by the illustrated battery
        missed_by_battery      SILENT but not detected by the illustrated battery
        unresolved_survivors   EQUIVALENT (no reproducible divergence anywhere in the
                               exhaustive battery)

    ``numerically_stable`` is listed separately from ``executable`` so unstable mutants
    are visible instead of being folded into another stage. ``battery_detected`` is the
    per-mutant detection by the battery being illustrated; when None, the exhaustive
    battery is implied, so every SILENT mutant counts as perturbation-detected and
    ``missed_by_battery`` is 0. ``missed_by_battery`` is kept apart from
    ``unresolved_survivors`` because those mutants are known to be non-equivalent: merging
    them would label reproducibly divergent mutants "equivalent". Unresolved survivors are
    equivalent *within the tested domain* only, not proven equivalent.

    Returns columns ``stage, parent, count, fraction_of_total``.
    """
    cls = _as_classes(classes)
    n = len(cls)
    if battery_detected is None:
        det = np.array([c is MutantClass.SILENT for c in cls], dtype=bool)
    else:
        det = as_binary(battery_detected, "battery_detected")
        if det.size != n:
            raise ValueError("battery_detected must have one entry per mutant")
        bad = [i for i, c in enumerate(cls) if c is MutantClass.EQUIVALENT and det[i]]
        if bad:
            raise ValueError(
                f"{len(bad)} mutant(s) classified EQUIVALENT are marked detected by the battery; "
                "classification and detection inputs are inconsistent"
            )
    invalid = {MutantClass.STRUCTURALLY_INVALID}
    nonexec = invalid | {MutantClass.NON_EXECUTABLE}
    unstable = nonexec | {MutantClass.NUMERICALLY_UNSTABLE}
    silent = np.array([c is MutantClass.SILENT for c in cls], dtype=bool)
    equivalent = np.array([c is MutantClass.EQUIVALENT for c in cls], dtype=bool)
    counts = {
        "total": n,
        "schema_valid": sum(c not in invalid for c in cls),
        "executable": sum(c not in nonexec for c in cls),
        "numerically_stable": sum(c not in unstable for c in cls),
        "canonical_survivors": int(np.sum(silent | equivalent)),
        "perturbation_detected": int(np.sum(silent & det)),
        "missed_by_battery": int(np.sum(silent & ~det)),
        "unresolved_survivors": int(equivalent.sum()),
    }
    parents = {
        "total": "",
        "schema_valid": "total",
        "executable": "schema_valid",
        "numerically_stable": "executable",
        "canonical_survivors": "numerically_stable",
        "perturbation_detected": "canonical_survivors",
        "missed_by_battery": "canonical_survivors",
        "unresolved_survivors": "canonical_survivors",
    }
    return pd.DataFrame(
        {
            "stage": list(CASCADE_STAGES),
            "parent": [parents[s] for s in CASCADE_STAGES],
            "count": [counts[s] for s in CASCADE_STAGES],
            "fraction_of_total": [_rate(counts[s], n) for s in CASCADE_STAGES],
        }
    )


def by_family(
    outcomes: Mapping[str, np.ndarray],
    families: Sequence[str],
    clusters: Sequence[str] | None = None,
    confidence: float = 0.95,
    method: str = "clopper_pearson",
    include_all: bool = True,
) -> pd.DataFrame:
    """Detection (or false-positive) rate per family for one or more strategies.

    ``outcomes`` maps a strategy name (e.g. ``canonical``, ``selected``) to per-unit
    detection booleans aligned with ``families`` (mutation family or transform category).
    Returns one row per (strategy, family) with columns
    ``strategy, family, n, n_detected, rate, ci_low, ci_high, ci_method, n_clusters``;
    ``family == "all"`` rows pool every unit when ``include_all``. ``n_clusters`` counts
    distinct base models in the family (``nan`` when ``clusters`` is None): families
    represented by few base models deserve cautious reading regardless of ``n``. Enum
    labels are written by value (see :func:`as_labels`).
    """
    fam = np.asarray(as_labels(families, "families"), dtype=object)
    cl = None if clusters is None else np.asarray(as_labels(clusters, "clusters"), dtype=object)
    if cl is not None and cl.size != fam.size:
        raise ValueError("clusters must align with families")
    order = list(dict.fromkeys(fam.tolist()))
    groups = [(f, fam == f) for f in order]
    if include_all:
        if "all" in order:
            raise ValueError("'all' is reserved for the pooled row; rename that family")
        groups.append(("all", np.ones(fam.size, dtype=bool)))
    rows = []
    for strategy, det in outcomes.items():
        d = as_binary(det, f"outcomes[{strategy!r}]")
        if d.size != fam.size:
            raise ValueError(f"outcomes[{strategy!r}] must align with families")
        for f, mask in groups:
            k, n = int(d[mask].sum()), int(mask.sum())
            lo, hi = proportion_ci(k, n, confidence, method)
            rows.append(
                {
                    "strategy": strategy,
                    "family": f,
                    "n": n,
                    "n_detected": k,
                    "rate": _rate(k, n),
                    "ci_low": lo,
                    "ci_high": hi,
                    "ci_method": f"{method} (units treated as independent)",
                    "n_clusters": float("nan") if cl is None else len(set(cl[mask].tolist())),
                }
            )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- curves and cost


def coverage_curve(
    detected: np.ndarray,
    protocol_ids: Sequence[str],
    order: Sequence[str],
    cost: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """Cumulative detection as protocols are added in ``order`` (e.g. a greedy selection).

    ``detected`` is the boolean matrix ``[n_units, n_protocols]`` with columns named by
    ``protocol_ids``; the rows define the denominator (normally admissible mutants).
    Returns one row per battery size starting at 0 with columns
    ``n_protocols, protocol_id, n_detected, n_new, detection_rate, exhaustive_coverage,
    cumulative_cost``. ``exhaustive_coverage`` is relative to the units detected by *all*
    columns of ``detected`` (the exhaustive battery), which is the "protocols required to
    reach increasing levels of exhaustive-battery coverage" endpoint. ``cumulative_cost`` is
    ``nan`` when ``cost`` is None; its unit is whatever ``cost`` uses (cell-steps in the
    detection matrix).
    """
    m = np.asarray(detected)
    if m.ndim != 2:
        raise ValueError("detected must be a 2-D [units, protocols] matrix")
    if m.dtype != bool:
        m = as_binary(m.ravel(), "detected").reshape(m.shape)
    pids = list(protocol_ids)
    if len(pids) != m.shape[1] or len(set(pids)) != len(pids):
        raise ValueError("protocol_ids must be unique and match the number of columns")
    if len(set(order)) != len(order):
        raise ValueError("order contains duplicate protocols")
    unknown = [p for p in order if p not in pids]
    if unknown:
        raise ValueError(f"order contains unknown protocols: {unknown}")
    if cost is not None:
        missing = [p for p in order if p not in cost]
        if missing:
            raise ValueError(f"cost missing for protocols: {missing}")
    n_units = m.shape[0]
    n_exhaustive = int(m.any(axis=1).sum()) if m.shape[1] else 0
    covered = np.zeros(n_units, dtype=bool)
    total_cost = 0.0 if cost is not None else float("nan")
    rows = [
        {
            "n_protocols": 0,
            "protocol_id": "",
            "n_detected": 0,
            "n_new": 0,
            "detection_rate": _rate(0, n_units),
            "exhaustive_coverage": _rate(0, n_exhaustive),
            "cumulative_cost": total_cost,
        }
    ]
    for i, p in enumerate(order, start=1):
        col = m[:, pids.index(p)]
        new = int(np.sum(col & ~covered))
        covered |= col
        if cost is not None:
            total_cost += float(cost[p])
        k = int(covered.sum())
        rows.append(
            {
                "n_protocols": i,
                "protocol_id": p,
                "n_detected": k,
                "n_new": new,
                "detection_rate": _rate(k, n_units),
                "exhaustive_coverage": _rate(k, n_exhaustive),
                "cumulative_cost": total_cost,
            }
        )
    return pd.DataFrame(rows)


def protocols_to_reach(curve: pd.DataFrame, levels: Sequence[float] = (0.5, 0.8, 0.9, 0.95, 1.0)) -> pd.DataFrame:
    """Smallest battery size in ``curve`` whose exhaustive coverage reaches each level.

    For a greedy ``order`` this is the greedy battery size, an upper bound on the minimum
    number of protocols (minimum set cover is NP-hard). Levels never reached get ``nan``.
    Returns columns ``level, n_protocols, cumulative_cost``.
    """
    rows = []
    cov = curve["exhaustive_coverage"].to_numpy(dtype=float)
    for level in levels:
        hit = np.flatnonzero(cov >= float(level) - 1e-12)
        if hit.size:
            r = curve.iloc[int(hit[0])]
            rows.append({"level": float(level), "n_protocols": float(r["n_protocols"]),
                         "cumulative_cost": float(r["cumulative_cost"])})
        else:
            rows.append({"level": float(level), "n_protocols": float("nan"), "cumulative_cost": float("nan")})
    return pd.DataFrame(rows)


def runtime_per_detection(
    runtime_s: np.ndarray | float,
    detected_any: np.ndarray,
    n_simulations: np.ndarray | int | None = None,
) -> dict[str, float]:
    """Runtime (and simulations) spent per detected unit.

    ``runtime_s`` and ``n_simulations`` are either per-unit arrays aligned with
    ``detected_any`` or scalar totals. All units count toward the cost, detected or not,
    because a validator pays for every mutant it examines. The per-detection value is
    ``inf`` when cost was spent but nothing was detected, and ``nan`` when nothing was
    spent and nothing detected.
    """
    d = as_binary(detected_any, "detected_any")
    k = int(d.sum())

    def total(x: np.ndarray | float, name: str) -> float:
        arr = np.asarray(x, dtype=float)
        if arr.ndim == 1 and arr.size != d.size:
            raise ValueError(f"{name} must be a scalar total or align with detected_any")
        if arr.ndim > 1:
            raise ValueError(f"{name} must be a scalar or 1-D")
        if not np.all(np.isfinite(arr)) or np.any(arr < 0):
            raise ValueError(f"{name} must be finite and non-negative")
        return float(arr.sum())

    def per(t: float) -> float:
        if k > 0:
            return t / k
        return float("inf") if t > 0 else float("nan")

    rt = total(runtime_s, "runtime_s")
    out = {"n_units": float(d.size), "n_detected": float(k), "total_runtime_s": rt, "runtime_s_per_detected": per(rt)}
    if n_simulations is not None:
        ns = total(n_simulations, "n_simulations")
        out["total_simulations"] = ns
        out["simulations_per_detected"] = per(ns)
    return out


def summarize_draws(
    rates: np.ndarray,
    strategy: str,
    n_protocols: float = float("nan"),
    cost: float = float("nan"),
    interval: float = 0.95,
) -> dict[str, Any]:
    """Collapse random-battery draws (``selection.greedy.random_*``) to one tidy row.

    ``detection_rate`` is the mean over draws (the expected rate of a random battery);
    ``lower``/``upper`` are central percentiles of the draws. That band describes the spread
    of individual random batteries, not a confidence interval for the mean.
    """
    r = np.asarray(rates, dtype=float)
    if r.ndim != 1 or r.size == 0 or not np.all(np.isfinite(r)):
        raise ValueError("rates must be a non-empty 1-D array of finite values")
    if not 0.0 < interval < 1.0:
        raise ValueError("interval must lie in (0, 1)")
    q = (1.0 - interval) / 2.0
    return {
        "strategy": strategy,
        "n_protocols": float(n_protocols),
        "cost": float(cost),
        "detection_rate": float(r.mean()),
        "median": float(np.median(r)),
        "lower": float(np.quantile(r, q)),
        "upper": float(np.quantile(r, 1.0 - q)),
        "n_draws": int(r.size),
    }
