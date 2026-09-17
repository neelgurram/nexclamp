"""Greedy protocol selection and the seeded random baselines."""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np
import pytest

from neuraxis.config import study
from neuraxis.selection.greedy import (
    BUDGET_REL_TOL,
    count_matched_sets,
    greedy_cost_sensitive,
    greedy_max_coverage,
    random_count_matched,
    random_runtime_matched,
    runtime_matched_sets,
    selection_settings,
)
from neuraxis.selection.matrix import DetectionMatrix


def mk(rows_by_protocol: dict[str, set[int]], n: int, cost: dict[str, float] | None = None) -> DetectionMatrix:
    pids = list(rows_by_protocol)
    det = np.zeros((n, len(pids)), dtype=bool)
    for j, p in enumerate(pids):
        det[sorted(rows_by_protocol[p]), j] = True
    ids = [f"m{i:02d}" for i in range(n)]
    return DetectionMatrix(ids, pids, det, {i: "model" for i in ids}, {i: "biophysical" for i in ids},
                           cost or {p: 1.0 for p in pids})


def random_matrix(rng: np.random.Generator, n: int, p: int, density: float, cost_levels=(1.0, 2.0)) -> DetectionMatrix:
    det = rng.random((n, p)) < density
    ids = [f"m{i:03d}" for i in range(n)]
    pids = [f"P{j:02d}" for j in range(p)]
    cost = {q: float(rng.choice(cost_levels)) for q in pids}
    return DetectionMatrix(ids, pids, det, {i: "model" for i in ids}, {i: "reference" for i in ids}, cost)


def n_covered(m: DetectionMatrix, protocols) -> int:
    return int(m.covered(list(protocols)).sum())


# ---------------------------------------------------------------------- greedy max coverage
def classic() -> DetectionMatrix:
    return mk({"P1": {0, 1, 2, 3, 4}, "P2": {5, 6, 7}, "P3": {0, 1, 2, 5}, "P4": {8}}, n=10,
              cost={"P1": 10.0, "P2": 20.0, "P3": 5.0, "P4": 1.0})


def test_greedy_sequence_curve_and_costs():
    sel = greedy_max_coverage(classic(), k=4)
    assert sel.protocols == ["P1", "P2", "P4"]
    assert sel.gains == [5, 3, 1]
    assert sel.coverage_curve == pytest.approx([0.5, 0.8, 0.9])
    assert sel.costs == pytest.approx([10.0, 30.0, 31.0])        # cumulative
    assert sel.stop_reason == "no_remaining_gain"                 # row 9 is undetectable, P3 adds nothing
    assert sel.shortfall == 1 and sel.k == 4                      # the empty slot is recorded, not hidden
    assert sel.tie_breaks == ["unique", "unique", "unique"]
    m = classic()
    for i in range(len(sel.protocols)):
        assert sel.coverage_curve[i] == m.rate(sel.protocols[: i + 1])


def test_greedy_budget_reached():
    sel = greedy_max_coverage(classic(), k=2)
    assert sel.protocols == ["P1", "P2"]
    assert sel.stop_reason == "budget_reached"
    assert sel.k == 2 and sel.n_mutants == 10 and sel.shortfall == 0


def test_greedy_stops_early_only_when_everything_is_covered():
    m = mk({"A": {0, 1, 2}, "B": {3, 4}, "C": {0, 3}, "D": {1}}, n=5)
    sel = greedy_max_coverage(m, k=4)
    assert sel.protocols == ["A", "B"]
    assert sel.coverage_curve[-1] == 1.0
    assert sel.stop_reason == "all_mutants_covered"
    assert sel.shortfall == 2


def test_tie_break_lower_cost_then_protocol_id():
    by_cost = mk({"P_a": {0, 1}, "P_b": {2, 3}}, n=4, cost={"P_a": 5.0, "P_b": 2.0})
    sel = greedy_max_coverage(by_cost, k=1)
    assert sel.protocols == ["P_b"]
    assert sel.tie_breaks[0].startswith("cost: P_b")
    by_id = mk({"P_z": {0, 1}, "P_a": {2, 3}}, n=4, cost={"P_z": 2.0, "P_a": 2.0})
    sel = greedy_max_coverage(by_id, k=2)
    assert sel.protocols == ["P_a", "P_z"]
    assert sel.tie_breaks[0].startswith("protocol_id: P_a over P_z")
    assert sel.tie_breaks[1] == "unique"


def test_greedy_is_independent_of_column_order():
    rng = np.random.default_rng(3)
    for _ in range(20):
        m = random_matrix(rng, 60, 12, 0.1)
        perm = rng.permutation(m.n_protocols)
        pids = [m.protocol_ids[j] for j in perm]
        shuffled = DetectionMatrix(m.mutant_ids, pids, m.detected[:, perm], m.model_of, m.family_of, m.cost)
        a, b = greedy_max_coverage(m, 5), greedy_max_coverage(shuffled, 5)
        assert (a.protocols, a.coverage_curve, a.tie_breaks) == (b.protocols, b.coverage_curve, b.tie_breaks)


def test_greedy_candidates_and_argument_errors():
    m = classic()
    sel = greedy_max_coverage(m, k=3, candidates=["P3", "P4"])
    assert sel.protocols == ["P3", "P4"] and sel.stop_reason == "candidates_exhausted"
    with pytest.raises(KeyError):
        greedy_max_coverage(m, 2, candidates=["P9"])
    with pytest.raises(ValueError):
        greedy_max_coverage(m, 2, candidates=["P1", "P1"])
    with pytest.raises(ValueError):
        greedy_max_coverage(m, 0)
    assert greedy_max_coverage(m, np.int64(2)).protocols == ["P1", "P2"]
    empty =DetectionMatrix([], ["P1"], np.zeros((0, 1), dtype=bool), {}, {}, {"P1": 1.0})
    with pytest.raises(ValueError):
        greedy_max_coverage(empty, 1)


@pytest.mark.parametrize("bad", [2.5, 2.0, "2", True, None])
def test_non_integer_k_draws_and_seed_are_rejected(bad):
    """A malformed config value must fail, not be truncated into a different baseline."""
    m = classic()
    with pytest.raises(TypeError):
        greedy_max_coverage(m, bad)
    with pytest.raises(TypeError):
        count_matched_sets(m, bad, 5, 0)
    with pytest.raises(TypeError):
        count_matched_sets(m, 2, bad, 0)
    with pytest.raises(TypeError):
        random_count_matched(m, 2, 5, bad)
    with pytest.raises(TypeError):
        runtime_matched_sets(m, 30.0, bad, 0)
    with pytest.raises(TypeError):
        random_runtime_matched(m, 30.0, 5, bad)
    with pytest.raises(TypeError):
        selection_settings({"selection": {"budget_k": bad, "random_draws": 10, "seed": 1}})
    with pytest.raises(TypeError):
        selection_settings({"selection": {"budget_k": 4, "random_draws": 10, "seed": bad}})


def test_greedy_meets_the_1_minus_1_over_e_guarantee():
    """Brute force on small instances: greedy coverage >= (1 - 1/e) x optimum (Nemhauser et al. 1978)."""
    rng = np.random.default_rng(11)
    worst = 1.0
    for _ in range(150):
        m = random_matrix(rng, 14, 7, float(rng.uniform(0.1, 0.5)))
        k = int(rng.integers(1, 5))
        sel = greedy_max_coverage(m, k)
        best = max(n_covered(m, c) for c in itertools.combinations(m.protocol_ids, k))
        got = n_covered(m, sel.protocols)
        assert got <= best
        if best:
            worst = min(worst, got / best)
            assert got >= (1 - 1 / math.e) * best - 1e-12
    assert worst <= 1.0


# ---------------------------------------------------------------------- cost-sensitive
def test_cost_sensitive_prefers_gain_per_cost_within_budget():
    m = mk({"big": {0, 1, 2, 3, 4, 5}, "cheap1": {0, 1, 2}, "cheap2": {6, 7}}, n=8,
           cost={"big": 6.0, "cheap1": 1.0, "cheap2": 1.0})
    sel = greedy_cost_sensitive(m, cost_budget=2.0)
    assert sel.protocols == ["cheap1", "cheap2"]
    assert sel.costs[-1] <= 2.0
    assert sel.objective == "cost_sensitive_ratio"


def test_cost_sensitive_falls_back_to_best_single_protocol():
    m = mk({"big": set(range(10)), "tiny": {10}}, n=11, cost={"big": 10.0, "tiny": 0.5})
    sel = greedy_cost_sensitive(m, cost_budget=10.0)
    assert sel.protocols == ["big"]
    assert sel.objective == "cost_sensitive_best_single"
    assert sel.tie_breaks[0].startswith("khuller_moss_naor")


def test_cost_sensitive_zero_cost_and_errors():
    m = mk({"free": {0}, "paid": {1, 2, 3}}, n=4, cost={"free": 0.0, "paid": 1.0})
    assert greedy_cost_sensitive(m, 1.0).protocols == ["free", "paid"]
    with pytest.raises(ValueError):
        greedy_cost_sensitive(mk({"a": {0}}, 1, {"a": 5.0}), 4.0)
    with pytest.raises(ValueError):
        greedy_cost_sensitive(m, float("inf"))


def test_cost_sensitive_orders_free_protocols_by_gain():
    """Two zero-cost protocols both have an 'infinite' ratio; the larger free gain must win, not the smaller id."""
    m = mk({"a_free_small": {0}, "b_free_big": {1, 2, 3, 4}, "paid": {5}}, n=6,
           cost={"a_free_small": 0.0, "b_free_big": 0.0, "paid": 1.0})
    sel = greedy_cost_sensitive(m, 0.0)
    assert sel.protocols == ["b_free_big", "a_free_small"]
    assert sel.gains == [4, 1] and sel.tie_breaks == ["unique", "unique"]
    sel = greedy_cost_sensitive(m, 1.0)
    assert sel.protocols == ["b_free_big", "a_free_small", "paid"]


def test_cost_sensitive_ratios_are_compared_exactly():
    """Float division can round two different gain/cost ratios to the same double (a false tie).

    The stored doubles 0.1 and 0.3 are not in ratio 1:3: exactly, 3/0.3 > 1/0.1, yet both
    quotients round to 10.0. A float comparison sees a tie and hands the step to the cost
    tie-break (the cheaper A). The exact comparison must pick B as a unique best, while
    exactly proportional costs must still tie and go to the cheaper protocol.
    """
    c_a, c_b = 0.1, 0.3
    assert 3 / c_b == 1 / c_a == 10.0                                  # the false float tie
    assert Fraction(3) / Fraction(c_b) > Fraction(1) / Fraction(c_a)  # exact order: B is better
    n = 30
    det = np.zeros((n, 2), dtype=bool)
    det[:1, 0] = True
    det[1:4, 1] = True
    ids = [f"m{i}" for i in range(n)]
    m = DetectionMatrix(ids, ["A_cheap", "B_dear"], det, {i: "x" for i in ids}, {i: "biophysical" for i in ids},
                        {"A_cheap": c_a, "B_dear": c_b})
    sel = greedy_cost_sensitive(m, 10.0)
    assert sel.protocols[0] == "B_dear" and sel.tie_breaks[0] == "unique"
    # exactly proportional integer costs (the real cell-step case) do tie and go to the cheaper protocol
    m2 = mk({"P_z": {0}, "P_a": {1, 2, 3}}, n=4, cost={"P_z": 20000.0, "P_a": 60000.0})
    sel2 = greedy_cost_sensitive(m2, 1e6)
    assert sel2.protocols == ["P_z", "P_a"] and sel2.tie_breaks[0].startswith("cost: P_z")


def test_cost_sensitive_budget_and_approximation_bound():
    """Brute force: never over budget, and within (1 - 1/e)/2 of the best feasible set (Khuller et al. 1999)."""
    rng = np.random.default_rng(5)
    for _ in range(120):
        m = random_matrix(rng, 14, 7, float(rng.uniform(0.1, 0.5)), cost_levels=(1.0, 2.0, 3.0, 5.0))
        budget = float(rng.uniform(min(m.cost.values()), sum(m.cost.values())))
        sel = greedy_cost_sensitive(m, budget)
        assert m.total_cost(sel.protocols) <= budget * (1 + BUDGET_REL_TOL)
        best = 0
        for r in range(1, m.n_protocols + 1):
            for c in itertools.combinations(m.protocol_ids, r):
                if m.total_cost(c) <= budget * (1 + BUDGET_REL_TOL):
                    best = max(best, n_covered(m, c))
        assert n_covered(m, sel.protocols) >= 0.5 * (1 - 1 / math.e) * best - 1e-12


# ---------------------------------------------------------------------- random baselines
def test_count_matched_is_seeded_and_reproducible():
    rng = np.random.default_rng(1)
    m = random_matrix(rng, 50, 10, 0.2)
    a = random_count_matched(m, 3, 400, seed=20260913)
    b = random_count_matched(m, 3, 400, seed=20260913)
    c = random_count_matched(m, 3, 400, seed=1)
    assert a.shape == (400,) and np.array_equal(a, b) and not np.array_equal(a, c)
    assert ((a >= 0) & (a <= 1)).all()
    sets = count_matched_sets(m, 3, 400, seed=20260913)
    assert all(len(s) == 3 and len(set(s)) == 3 and set(s) <= set(m.protocol_ids) for s in sets)
    assert np.array_equal(a, np.array([m.rate(s) for s in sets]))
    with pytest.raises(ValueError):
        random_count_matched(m, 11, 10, seed=0)
    with pytest.raises(ValueError):
        random_count_matched(m, 2, 0, seed=0)


def test_count_matched_mean_matches_exact_expectation():
    rng = np.random.default_rng(2)
    m = random_matrix(rng, 40, 8, 0.15)
    all_rates = np.array([m.rate(c) for c in itertools.combinations(m.protocol_ids, 3)])
    draws = 20000
    sample = random_count_matched(m, 3, draws, seed=99)
    se = all_rates.std() / math.sqrt(draws)
    assert abs(sample.mean() - all_rates.mean()) < 5 * se


def test_count_matched_is_independent_of_column_order():
    rng = np.random.default_rng(4)
    m = random_matrix(rng, 30, 9, 0.2)
    perm = rng.permutation(m.n_protocols)
    shuffled = DetectionMatrix(m.mutant_ids, [m.protocol_ids[j] for j in perm], m.detected[:, perm],
                               m.model_of, m.family_of, m.cost)
    assert np.array_equal(random_count_matched(m, 4, 300, 8), random_count_matched(shuffled, 4, 300, 8))


def test_runtime_matched_sets_fit_budget_and_are_maximal():
    rng = np.random.default_rng(6)
    m = random_matrix(rng, 30, 12, 0.2, cost_levels=(1e5, 2.5e5, 4e5, 7e5))
    budget = 1.2e6
    sets = runtime_matched_sets(m, budget, 2000, seed=12)
    for s in sets:
        total = m.total_cost(s)
        assert total <= budget * (1 + BUDGET_REL_TOL)
        assert all(total + m.cost[p] > budget * (1 + BUDGET_REL_TOL) for p in m.protocol_ids if p not in s)
    rates = random_runtime_matched(m, budget, 2000, seed=12)
    assert np.array_equal(rates, np.array([m.rate(s) for s in sets]))
    assert np.array_equal(rates, random_runtime_matched(m, budget, 2000, seed=12))
    with pytest.raises(ValueError):
        random_runtime_matched(m, 5e4, 10, seed=0)


def test_runtime_matched_mean_cost_is_close_to_budget():
    """20 protocols of 0.5-1.5 x 1e5 cell-steps, budget of about ten protocols."""
    rng = np.random.default_rng(8)
    pids = [f"P{j:02d}" for j in range(20)]
    cost = {p: float(c) for p, c in zip(pids, rng.uniform(0.5e5, 1.5e5, size=20))}
    m = DetectionMatrix(["m0"], pids, np.ones((1, 20), dtype=bool), {"m0": "x"}, {"m0": "numerical"}, cost)
    budget = 1.0e6
    totals = np.array([m.total_cost(s) for s in runtime_matched_sets(m, budget, 5000, seed=20260913)])
    assert totals.max() <= budget * (1 + BUDGET_REL_TOL)
    assert totals.mean() == pytest.approx(budget, rel=0.05)
    assert totals.mean() > 0.95 * budget


def test_greedy_battery_is_itself_runtime_feasible():
    """Float summation order must not push the greedy battery's own cost over its budget."""
    m = mk({"a": {0}, "b": {1}, "c": {2}}, n=3, cost={"a": 0.1, "b": 0.2, "c": 0.3})
    sel = greedy_max_coverage(m, 3)
    budget = m.total_cost(sel.protocols)
    assert 0.1 + 0.2 + 0.3 > budget                      # naive running sum overshoots by one ulp
    assert all(s == ("a", "b", "c") for s in runtime_matched_sets(m, budget, 200, seed=3))


def test_selection_settings_from_study_config():
    s = selection_settings(study())
    assert s.tie_break == ("cost", "protocol_id")
    assert s.budget_k >= 1 and s.random_draws >= 1 and s.seed >= 0
    with pytest.raises(ValueError):
        selection_settings({"selection": {"budget_k": 4, "random_draws": 10, "seed": 1,
                                          "tie_break": ["protocol_id", "cost"]}})
