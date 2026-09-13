"""Protocol selection on a discovery detection matrix, and the random baselines.

Greedy maximum coverage is the specification's transparent baseline: repeatedly add the
protocol that detects the most not-yet-detected mutants. It is deterministic (ties go to
the cheaper protocol, then to the lexicographically smaller protocol id) so the frozen
battery can be regenerated bit-for-bit from the matrix. The random baselines answer
"does optimisation add anything?" by drawing protocol sets with the same count, or with
a comparable simulation cost, from the same candidates.

This module works only on a :class:`DetectionMatrix` handed to it. It never reads split
files; restricting the matrix to discovery rows is the job of
``neurosem.selection.splits.DiscoveryView.filter_matrix``.
"""

from __future__ import annotations

import dataclasses as dc
import math
import operator
from collections.abc import Mapping, Sequence
from fractions import Fraction
from typing import Any

import numpy as np

from neurosem.selection.matrix import DetectionMatrix

# Relative slack when comparing a running cost total with a budget. Costs are sums of
# floats; the same set summed in a different order can exceed the exact budget by one
# ulp, which must not make the greedy battery itself "over budget".
BUDGET_REL_TOL = 1e-9
TIE_BREAK = ("cost", "protocol_id")


@dc.dataclass
class Selection:
    """A selected protocol battery and how it was reached.

    ``coverage_curve[i]`` and ``costs[i]`` are cumulative: the fraction of all matrix rows
    detected, and the total cost in cell-steps, after adding ``protocols[: i + 1]``.
    ``gains[i]`` is the number of newly detected mutants at step ``i`` and
    ``tie_breaks[i]`` records whether that choice was unique or decided by cost or id.

    ``shortfall`` (maximum coverage only) is ``k - len(protocols)``: how many budget slots
    stayed empty because nothing coverable remained. When it is positive, a count-matched
    random baseline must draw ``len(protocols)`` protocols, not ``k``, or the random battery
    would get more protocols than the selected one.
    """

    protocols: list[str]
    coverage_curve: list[float]
    costs: list[float]
    tie_breaks: list[str]
    gains: list[int] = dc.field(default_factory=list)
    objective: str = "max_coverage"
    stop_reason: str = ""
    n_mutants: int = 0
    k: int | None = None
    cost_budget: float | None = None
    candidates: list[str] = dc.field(default_factory=list)
    shortfall: int | None = None


def _as_int(value: Any, name: str) -> int:
    """``value`` as a Python int; floats, strings and bools are rejected, not truncated.

    ``k``, ``draws`` and ``seed`` define a reproducible baseline, so a malformed config
    value (``2.5``, ``"4"``, ``True``) must fail loudly instead of silently becoming another number.
    """
    if isinstance(value, bool):
        raise TypeError(f"{name} must be an integer, got bool {value!r}")
    try:
        return operator.index(value)
    except TypeError:
        raise TypeError(f"{name} must be an integer, got {type(value).__name__} {value!r}") from None


@dc.dataclass(frozen=True)
class SelectionSettings:
    budget_k: int
    random_draws: int
    seed: int
    tie_break: tuple[str, ...]


def selection_settings(study_cfg: Mapping[str, Any] | Any) -> SelectionSettings:
    """Read the ``selection`` block of ``configs/study.yaml``.

    The tie-break rule is implemented, not configured; a config that asks for a different
    rule is rejected rather than silently ignored.
    """
    sel = study_cfg["selection"]
    tie = tuple(sel.get("tie_break", TIE_BREAK))
    if tie != TIE_BREAK:
        raise ValueError(f"tie_break {list(tie)} is not implemented; greedy selection uses {list(TIE_BREAK)}")
    s = SelectionSettings(_as_int(sel["budget_k"], "budget_k"), _as_int(sel["random_draws"], "random_draws"),
                          _as_int(sel["seed"], "seed"), tie)
    if s.budget_k < 1 or s.random_draws < 1:
        raise ValueError("budget_k and random_draws must be >= 1")
    if s.seed < 0:
        raise ValueError("seed must be a non-negative integer")
    return s


def _candidates(m: DetectionMatrix, candidates: Sequence[str] | None) -> list[str]:
    """Validated candidate ids, sorted by protocol id so results never depend on column order."""
    cands = list(m.protocol_ids if candidates is None else candidates)
    if len(set(cands)) != len(cands):
        raise ValueError("duplicate candidate protocols")
    m.column_indices(cands)            # KeyError for unknown ids
    if not cands:
        raise ValueError("no candidate protocols")
    return sorted(cands)


def _require_rows(m: DetectionMatrix) -> None:
    if m.n_mutants == 0:
        raise ValueError("selection needs at least one mutant row")


def _pick(scores: Mapping[str, Any], cost: Mapping[str, float], label: str) -> tuple[str, str]:
    """Best candidate by (higher score, lower cost, smaller id) and a tie-break note.

    Scores must compare exactly (ints, ``Fraction`` or tuples of them); a tie is equality.
    """
    best_score = max(scores.values())
    tied = [p for p, s in scores.items() if s == best_score]
    if len(tied) == 1:
        return tied[0], "unique"
    best_cost = min(cost[p] for p in tied)
    cheapest = sorted(p for p in tied if cost[p] == best_cost)
    chosen = cheapest[0]
    others = ", ".join(sorted(p for p in tied if p != chosen))
    if len(cheapest) == 1:
        return chosen, f"cost: {chosen} (cost {best_cost!r}) over {others} at equal {label}"
    return chosen, f"protocol_id: {chosen} over {others} at equal {label} and cost {best_cost!r}"


def greedy_max_coverage(m: DetectionMatrix, k: int, candidates: Sequence[str] | None = None) -> Selection:
    """Greedy maximum coverage with budget ``k`` protocols.

    Stops before ``k`` only when nothing coverable remains: either every mutant is already
    detected (``all_mutants_covered``) or no remaining candidate detects any undetected
    mutant (``no_remaining_gain``; the shortfall stays visible as a final coverage < 1).
    Both cases are the same situation for the greedy rule (every remaining candidate has
    zero marginal gain), and a zero-gain protocol would be chosen only by the cost/id
    tie-break, changing the battery without any evidence from the discovery data, so it is
    not added. Any empty slots are recorded in ``Selection.shortfall``. Greedy coverage is
    within a factor (1 - 1/e) of the best k-set (Nemhauser, Wolsey and Fisher 1978).
    """
    k = _as_int(k, "k")
    if k < 1:
        raise ValueError("k must be >= 1")
    _require_rows(m)
    cands = _candidates(m, candidates)
    sel = Selection([], [], [], [], objective="max_coverage", n_mutants=m.n_mutants, k=k,
                    candidates=list(cands))
    covered = np.zeros(m.n_mutants, dtype=bool)
    remaining = list(cands)
    sel.stop_reason = "budget_reached"
    while len(sel.protocols) < k:
        if not remaining:
            sel.stop_reason = "candidates_exhausted"
            break
        if covered.all():
            sel.stop_reason = "all_mutants_covered"
            break
        gains = m.detected[np.ix_(~covered, m.column_indices(remaining))].sum(axis=0)
        scores = {p: int(g) for p, g in zip(remaining, gains)}
        if max(scores.values()) == 0:
            sel.stop_reason = "no_remaining_gain"
            break
        chosen, note = _pick(scores, m.cost, "gain")
        _add(sel, m, chosen, note, scores[chosen], covered)
        remaining.remove(chosen)
    sel.shortfall = k - len(sel.protocols)
    return sel


def _ratio_rank(gain: int, cost: float) -> tuple[int, Fraction]:
    """Exact rank of gain per cell-step, compared without floating-point division.

    Costs are compared as the exact rationals of their stored binary values, so unequal
    ratios never collapse into a false tie through rounding. Zero-cost protocols with
    positive gain rank above every paid one and among themselves by gain (their ratio
    would be infinite, which cannot tell a large free gain from a small one).
    """
    if cost == 0:
        return (1, Fraction(gain))
    return (0, Fraction(gain) / Fraction(cost))


def _add(sel: Selection, m: DetectionMatrix, pid: str, note: str, gain: int, covered: np.ndarray) -> None:
    covered |= m.detected[:, m.column_indices([pid])[0]]
    sel.protocols.append(pid)
    sel.gains.append(int(gain))
    sel.tie_breaks.append(note)
    sel.coverage_curve.append(float(covered.mean()))
    sel.costs.append(m.total_cost(sel.protocols))


def _within(total: float, budget: float) -> bool:
    return total <= budget * (1.0 + BUDGET_REL_TOL)


def greedy_cost_sensitive(m: DetectionMatrix, cost_budget: float,
                          candidates: Sequence[str] | None = None) -> Selection:
    """Budgeted maximum coverage: best gain per cell-step while the total cost fits the budget.

    Plain ratio greedy can be arbitrarily bad when one expensive protocol detects far more
    than many cheap ones, so, following Khuller, Moss and Naor (1999, Inf. Process. Lett.
    70:39-45), the result is compared with the best single affordable protocol and the
    better of the two is returned (ties keep the ratio-greedy battery). Zero-cost
    protocols with positive gain rank first. Ties: lower cost, then protocol id.
    """
    if not (math.isfinite(cost_budget) and cost_budget >= 0):
        raise ValueError("cost_budget must be finite and non-negative")
    _require_rows(m)
    cands = _candidates(m, candidates)
    affordable = [p for p in cands if _within(m.cost[p], cost_budget)]
    if not affordable:
        raise ValueError(f"cost_budget {cost_budget!r} is below the cheapest candidate protocol")
    sel = Selection([], [], [], [], objective="cost_sensitive_ratio", n_mutants=m.n_mutants,
                    cost_budget=float(cost_budget), candidates=list(cands))
    covered = np.zeros(m.n_mutants, dtype=bool)
    remaining = list(cands)
    sel.stop_reason = "candidates_exhausted"
    while remaining:
        spent = sel.costs[-1] if sel.costs else 0.0
        fits = [p for p in remaining if _within(spent + m.cost[p], cost_budget)]
        if not fits:
            sel.stop_reason = "budget_reached"
            break
        if covered.all():
            sel.stop_reason = "all_mutants_covered"
            break
        gains = m.detected[np.ix_(~covered, m.column_indices(fits))].sum(axis=0)
        positive = {p: int(g) for p, g in zip(fits, gains) if g > 0}
        if not positive:
            sel.stop_reason = "no_remaining_gain"
            break
        ratios = {p: _ratio_rank(g, m.cost[p]) for p, g in positive.items()}
        chosen, note = _pick(ratios, m.cost, "gain/cost")
        _add(sel, m, chosen, note, positive[chosen], covered)
        remaining.remove(chosen)

    single_cov = {p: int(m.detected[:, m.column_indices([p])[0]].sum()) for p in affordable}
    best_single, single_note = _pick(single_cov, m.cost, "coverage")
    greedy_count = int(covered.sum())
    if single_cov[best_single] > greedy_count:
        alt = Selection([], [], [], [], objective="cost_sensitive_best_single", n_mutants=m.n_mutants,
                        cost_budget=float(cost_budget), candidates=list(cands))
        note = (f"khuller_moss_naor: single protocol {best_single} detects {single_cov[best_single]} > "
                f"ratio-greedy {greedy_count} ({'; '.join(sel.protocols) or 'empty'}); {single_note}")
        _add(alt, m, best_single, note, single_cov[best_single], np.zeros(m.n_mutants, dtype=bool))
        alt.stop_reason = "best_single_protocol"
        return alt
    return sel


# ---------------------------------------------------------------------- random baselines
def _check_draws(draws: int, seed: int) -> tuple[int, int]:
    draws, seed = _as_int(draws, "draws"), _as_int(seed, "seed")
    if draws < 1:
        raise ValueError("draws must be >= 1")
    if seed < 0:
        raise ValueError("seed must be a non-negative integer")
    return draws, seed


def count_matched_sets(m: DetectionMatrix, k: int, draws: int, seed: int,
                       candidates: Sequence[str] | None = None) -> list[tuple[str, ...]]:
    """``draws`` uniformly random k-subsets of the candidates.

    Sampling rule: candidates are sorted by protocol id, a ``numpy.random.default_rng(seed)``
    generator draws ``k`` distinct indices per draw with ``Generator.choice(n, k,
    replace=False)``. Each returned set is sorted by protocol id. Reproducible for a fixed
    seed and NumPy version (the version is part of the environment digest).
    """
    draws, seed = _check_draws(draws, seed)
    k = _as_int(k, "k")
    cands = _candidates(m, candidates)
    if not 1 <= k <= len(cands):
        raise ValueError(f"k must be between 1 and the number of candidates ({len(cands)})")
    rng = np.random.default_rng(seed)
    return [tuple(sorted(cands[i] for i in rng.choice(len(cands), size=k, replace=False)))
            for _ in range(draws)]


def runtime_matched_sets(m: DetectionMatrix, cost_budget: float, draws: int, seed: int,
                         candidates: Sequence[str] | None = None) -> list[tuple[str, ...]]:
    """``draws`` random protocol sets whose total cost stays within ``cost_budget``.

    Sampling rule (random-order first fit): candidates are sorted by protocol id; for each
    draw ``numpy.random.default_rng(seed).permutation(n)`` gives a random order; walking
    that order, a protocol is added whenever the running total plus its cost is still
    within the budget (relative slack ``BUDGET_REL_TOL``), otherwise it is skipped and the
    walk continues. Every set is therefore maximal: no unselected candidate would still
    fit. Skipping instead of stopping at the first protocol that does not fit keeps the
    mean cost close to the budget, so the random battery is not handicapped by getting
    less simulation time than the battery it is compared with.
    """
    draws, seed = _check_draws(draws, seed)
    if not (math.isfinite(cost_budget) and cost_budget >= 0):
        raise ValueError("cost_budget must be finite and non-negative")
    cands = _candidates(m, candidates)
    costs = [m.cost[p] for p in cands]
    if not any(_within(c, cost_budget) for c in costs):
        raise ValueError(f"cost_budget {cost_budget!r} is below the cheapest candidate protocol")
    rng = np.random.default_rng(seed)
    out: list[tuple[str, ...]] = []
    for _ in range(draws):
        total, chosen = 0.0, []
        for i in rng.permutation(len(cands)):
            if _within(total + costs[i], cost_budget):
                total += costs[i]
                chosen.append(cands[i])
        out.append(tuple(sorted(chosen)))
    return out


def _rates(m: DetectionMatrix, sets: Sequence[tuple[str, ...]]) -> np.ndarray:
    _require_rows(m)
    det = m.detected
    return np.array([det[:, m.column_indices(s)].any(axis=1).mean() for s in sets], dtype=float)


def random_count_matched(m: DetectionMatrix, k: int, draws: int, seed: int,
                         candidates: Sequence[str] | None = None) -> np.ndarray:
    """Detection rate of each :func:`count_matched_sets` draw (same seed, same sets)."""
    _require_rows(m)
    return _rates(m, count_matched_sets(m, k, draws, seed, candidates))


def random_runtime_matched(m: DetectionMatrix, cost_budget: float, draws: int, seed: int,
                           candidates: Sequence[str] | None = None) -> np.ndarray:
    """Detection rate of each :func:`runtime_matched_sets` draw (same seed, same sets)."""
    _require_rows(m)
    return _rates(m, runtime_matched_sets(m, cost_budget, draws, seed, candidates))
