"""Tests for neurosem.protocols.rheobase.search and count_upward_crossings on fake spike counters.

Expected brackets are derived by hand with a grid of 11 points (10 intervals) so every
refinement divides the bracket by exactly 10 and the decimal boundaries are obvious:
threshold 0.34565 nA -> [0.3, 0.4] -> [0.34, 0.35] -> [0.345, 0.346] -> [0.3456, 0.3457].
Thresholds are chosen off-grid so floating-point ties cannot decide the answer.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pytest

from neurosem.protocols.rheobase import RheobaseResult, count_upward_crossings, search

ABS = 1e-12


class ThresholdCounter:
    """Deterministic monotonic cell: one spike iff amplitude >= threshold. Records every call."""

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.calls: list[list[float]] = []

    def __call__(self, amps: Sequence[float]) -> list[int]:
        self.calls.append(list(amps))
        return [1 if a >= self.threshold else 0 for a in amps]


class ScriptedCounter:
    """Returns responses from a script, one per call (models a non-reproducible simulator)."""

    def __init__(self, *responses) -> None:
        self.responses = list(responses)
        self.n = 0

    def __call__(self, amps: Sequence[float]):
        r = self.responses[min(self.n, len(self.responses) - 1)]
        self.n += 1
        return r(amps) if callable(r) else r


def _bracket(r: RheobaseResult) -> tuple[float, float]:
    assert r.lower_nA is not None and r.upper_nA is not None
    return r.lower_nA, r.upper_nA


# ------------------------------------------------------------------------------------ monotonic
def test_monotonic_exact_brackets_each_round():
    c = ThresholdCounter(0.34565)
    r = search(c, hi_nA=1.0, grid=11, rounds=4)
    assert r.status == "ok"
    lo, hi = _bracket(r)
    assert lo == pytest.approx(0.3456, abs=ABS) and hi == pytest.approx(0.3457, abs=ABS)
    assert r.rheobase_nA == hi                                    # reported value = first spiking amplitude
    assert r.resolution_nA == pytest.approx(1e-4, abs=ABS)
    assert r.n_simulations == 4 and len(r.history) == 4 and len(c.calls) == 4
    expected_grids = [(0.0, 1.0), (0.3, 0.4), (0.34, 0.35), (0.345, 0.346)]
    for h, (a, b) in zip(r.history, expected_grids):
        amps = h["amplitudes_nA"]
        assert len(amps) == 11
        assert amps[0] == pytest.approx(a, abs=ABS) and amps[-1] == pytest.approx(b, abs=ABS)
        assert h["counts"] == [1 if x >= 0.34565 else 0 for x in amps]
        assert "note" not in h


def test_amplitudes_passed_as_python_floats():
    c = ThresholdCounter(0.2)
    search(c, rounds=1)
    assert all(type(a) is float for a in c.calls[0])


def test_rounds_one_gives_coarse_bracket():
    r = search(ThresholdCounter(0.34565), hi_nA=1.0, grid=11, rounds=1)
    assert r.status == "ok" and r.n_simulations == 1
    assert _bracket(r) == (pytest.approx(0.3, abs=ABS), pytest.approx(0.4, abs=ABS))


def test_default_parameters_bracket_width():
    """With the study defaults (hi 0.5 nA, 12 points, 4 rounds) the final width is 0.5 / 11**4 nA."""
    for threshold in (0.0137, 0.2, 0.4999):
        r = search(ThresholdCounter(threshold))
        lo, hi = _bracket(r)
        assert r.status == "ok" and lo < threshold <= hi
        assert r.resolution_nA == pytest.approx(0.5 / 11**4, rel=1e-9)
        assert r.n_simulations == 4


@pytest.mark.parametrize("threshold", np.random.default_rng(7).uniform(0.001, 31.9, 25).tolist())
def test_bracket_always_contains_threshold(threshold):
    r = search(ThresholdCounter(threshold))
    lo, hi = _bracket(r)
    assert r.status == "ok"
    assert lo < threshold <= hi
    assert 0 < r.resolution_nA < 0.5                               # refined well below the coarse step


# ------------------------------------------------------------------------------------ expansion
def test_expansion_exact_brackets():
    # [0,1] silent -> expand to [1,4]: grid 1.0,1.3,...,2.5,2.8 -> bracket [2.5, 2.8]
    # then [2.53, 2.56] -> [2.548, 2.551] -> [2.5498, 2.5501]
    c = ThresholdCounter(2.55)
    r = search(c, hi_nA=1.0, grid=11, rounds=4, expand=4.0)
    assert r.status == "ok"
    lo, hi = _bracket(r)
    assert lo == pytest.approx(2.5498, abs=ABS) and hi == pytest.approx(2.5501, abs=ABS)
    # expansion simulations do not consume refinement rounds
    assert r.n_simulations == 5
    grids = [(h["amplitudes_nA"][0], h["amplitudes_nA"][-1]) for h in r.history]
    expected = [(0.0, 1.0), (1.0, 4.0), (2.5, 2.8), (2.53, 2.56), (2.548, 2.551)]
    for (a, b), (ea, eb) in zip(grids, expected):
        assert a == pytest.approx(ea, abs=ABS) and b == pytest.approx(eb, abs=ABS)


def test_not_found_reports_highest_silent_amplitude():
    c = ThresholdCounter(1e9)
    r = search(c)
    assert r.status == "not_found" and r.rheobase_nA is None
    assert r.lower_nA == 32.0 and r.upper_nA is None and r.resolution_nA is None
    assert r.n_simulations == 4
    ranges = [(h["amplitudes_nA"][0], h["amplitudes_nA"][-1]) for h in r.history]
    assert ranges == [(0.0, 0.5), (0.5, 2.0), (2.0, 8.0), (8.0, 32.0)]


def test_expansion_is_clamped_to_max_hi():
    r = search(ThresholdCounter(1e9), hi_nA=0.5, expand=4.0, max_hi_nA=10.0)
    ranges = [(h["amplitudes_nA"][0], h["amplitudes_nA"][-1]) for h in r.history]
    assert ranges == [(0.0, 0.5), (0.5, 2.0), (2.0, 8.0), (8.0, 10.0)]
    assert r.status == "not_found" and r.lower_nA == 10.0


def test_threshold_at_max_hi_is_found():
    r = search(ThresholdCounter(31.9))
    lo, hi = _bracket(r)
    assert r.status == "ok" and lo < 31.9 <= hi <= 32.0


# ---------------------------------------------------------------------------------- spontaneous
def test_spontaneous_activity_at_zero_current():
    c = ScriptedCounter(lambda amps: [3] * len(amps))
    r = search(c)
    assert r.status == "spontaneous"
    assert r.rheobase_nA == 0.0 and r.lower_nA == 0.0 and r.upper_nA == 0.0 and r.resolution_nA == 0.0
    assert r.n_simulations == 1


def test_spiking_only_at_zero_is_still_spontaneous():
    r = search(ScriptedCounter(lambda amps: [1] + [0] * (len(amps) - 1)))
    assert r.status == "spontaneous"


# ------------------------------------------------------------------------------- non-monotonic
def test_deterministic_island_below_grid_is_missed():
    """A spiking island narrower than the coarse step is invisible to a grid search (documented limitation)."""
    def island(amps):
        return [1 if (0.15 <= a < 0.17) or a >= 0.55537 else 0 for a in amps]

    r = search(island, hi_nA=1.0, grid=11, rounds=4)
    lo, hi = _bracket(r)
    assert r.status == "ok"
    assert lo == pytest.approx(0.5553, abs=ABS) and hi == pytest.approx(0.5554, abs=ABS)


def test_refined_grid_without_spikes_keeps_previous_bracket():
    first = ThresholdCounter(0.34565)
    c = ScriptedCounter(first, lambda amps: [0] * len(amps))
    r = search(c, hi_nA=1.0, grid=11, rounds=4)
    assert r.status == "ok" and r.n_simulations == 2
    assert _bracket(r) == (pytest.approx(0.3, abs=ABS), pytest.approx(0.4, abs=ABS))
    assert r.rheobase_nA == pytest.approx(0.4, abs=ABS)
    assert "bracket kept" in r.history[-1]["note"]
    assert "no spiking amplitude" in r.history[-1]["note"]


def test_lower_edge_spiking_in_refinement_keeps_previous_bracket():
    c = ScriptedCounter(ThresholdCounter(0.34565), lambda amps: [1] * len(amps))
    r = search(c, hi_nA=1.0, grid=11, rounds=4)
    assert r.status == "ok" and r.n_simulations == 2
    assert _bracket(r) == (pytest.approx(0.3, abs=ABS), pytest.approx(0.4, abs=ABS))
    assert "lower bracket edge spiked" in r.history[-1]["note"]


def test_lower_edge_spiking_after_expansion_never_returns_inverted_bracket():
    """First grid [0, 0.5] silent; the expanded grid [0.5, 2] spikes already at 0.5, which was silent before.

    The response is non-reproducible, so an 'ok' result must at least be a proper bracket (lower < upper).
    """
    c = ScriptedCounter(lambda amps: [0] * len(amps), lambda amps: [1] * len(amps))
    r = search(c, hi_nA=0.5, grid=11, rounds=4)
    if r.status == "ok":
        lo, hi = _bracket(r)
        assert lo < hi and r.resolution_nA > 0
    else:
        assert r.rheobase_nA is None


# ---------------------------------------------------------------------------------------- errors
def test_counter_failure_in_bracketing_phase():
    # The initial grid is retried with hi / expand up to max_shrink (3) times before giving up.
    r = search(ScriptedCounter(None, None, None, None))
    assert r.status == "error" and r.rheobase_nA is None
    assert r.lower_nA is None and r.upper_nA is None and r.n_simulations == 4
    assert [h["amplitudes_nA"][-1] for h in r.history] == pytest.approx([0.5, 0.125, 0.03125, 0.0078125])
    assert all(h["counts"] is None for h in r.history)


def test_initial_grid_failure_then_success_after_shrinking():
    # A small cell whose simulation fails at large amplitudes: first grid fails, the shrunk grid runs.
    r = search(ScriptedCounter(None, ThresholdCounter(0.05), ThresholdCounter(0.05), ThresholdCounter(0.05),
                               ThresholdCounter(0.05)), hi_nA=0.5, grid=11, rounds=3)
    assert r.status == "ok" and r.lower_nA < 0.05 <= r.upper_nA
    assert r.history[0]["counts"] is None and "retrying" in r.history[0]["note"]


def test_counter_failure_in_refinement_keeps_bracket():
    c = ScriptedCounter(ThresholdCounter(0.34565), None)
    r = search(c, hi_nA=1.0, grid=11, rounds=4)
    assert r.status == "error" and r.rheobase_nA is None and r.n_simulations == 2
    assert _bracket(r) == (pytest.approx(0.3, abs=ABS), pytest.approx(0.4, abs=ABS))
    assert r.history[-1]["counts"] is None


@pytest.mark.parametrize("kwargs", [{"grid": 2}, {"grid": 0}, {"rounds": 0}, {"rounds": -1}])
def test_invalid_search_parameters(kwargs):
    with pytest.raises(ValueError, match="grid must be >= 3 and rounds >= 1"):
        search(ThresholdCounter(0.2), **kwargs)


def test_counts_as_numpy_array_accepted():
    r = search(lambda amps: np.array([1 if a >= 0.34565 else 0 for a in amps]), hi_nA=1.0, grid=11, rounds=2)
    assert _bracket(r) == (pytest.approx(0.34, abs=ABS), pytest.approx(0.35, abs=ABS))


def test_resolution_property():
    assert RheobaseResult(0.2, "ok", 0.15, 0.2, 1, []).resolution_nA == pytest.approx(0.05)
    assert RheobaseResult(None, "not_found", 32.0, None, 4, []).resolution_nA is None


# --------------------------------------------------------------------------- upward crossings
@pytest.mark.parametrize("v, thr, expected", [
    ([-70, -10, 30, -60, 0, -70], -20.0, 2),
    ([-21.0, -20.0], -20.0, 1),                 # reaching the threshold counts (>=)
    ([0.0, 10.0, -30.0], -20.0, 0),             # a trace that starts above threshold is not a new spike
    ([-70.0, -20.0, -20.0, -70.0, -19.0], -20.0, 2),
    ([-70.0], -20.0, 0),
    ([], -20.0, 0),
    ([-70, 40, -70, 40, -70, 40], 0.0, 3),
])
def test_count_upward_crossings(v, thr, expected):
    assert count_upward_crossings(np.asarray(v, dtype=float), thr) == expected


def test_count_upward_crossings_ignores_nan_as_below():
    v = np.array([-70.0, np.nan, 10.0, -70.0])
    assert count_upward_crossings(v, -20.0) == 1
