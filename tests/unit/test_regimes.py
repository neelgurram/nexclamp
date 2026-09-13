"""Unit tests for features.regimes.firing_regime (label logic on hand-built feature tables)."""

from __future__ import annotations

import copy

import numpy as np
import pytest

from neurosem.config import features as load_features_config
from neurosem.features.efel_adapter import DEFINED, NOT_APPLICABLE, UNDEFINED, FeatureValue
from neurosem.features.regimes import LABELS, depolarization_block, firing_regime, regime_config
from neurosem.features.trace_metrics import uniform_grid
from neurosem.schemas import AnalysisWindow, Trace

WINDOW = AnalysisWindow(200.0, 600.0)


@pytest.fixture(scope="module")
def cfg() -> dict:
    return load_features_config().data


def spikes(times: list[float], plateau_from: float | None = None, plateau_mV: float = -30.0) -> Trace:
    """Half-sine spikes (-65 -> +35 mV, 1 ms) with an optional depolarised plateau."""
    t = uniform_grid(0.0, 0.025, 28001)
    v = np.full_like(t, -65.0)
    for ts in times:
        m = (t >= ts) & (t < ts + 1.0)
        v[m] += 100.0 * np.sin(np.pi * (t[m] - ts))
    if plateau_from is not None:
        v[t >= plateau_from] = plateau_mV
    return Trace(t, v)


def table(spike_count: float | None, burst_count: float | None = None, adaptation_index: float | None = None) -> dict:
    def fv(name: str, value: float | None, na: bool) -> FeatureValue:
        if value is not None:
            return FeatureValue(name, value, DEFINED, "1", "test")
        return FeatureValue(name, None, NOT_APPLICABLE if na else UNDEFINED, "1", "test")
    return {"spike_count": fv("spike_count", spike_count, False),
            "burst_count": fv("burst_count", burst_count, True),
            "adaptation_index": fv("adaptation_index", adaptation_index, True)}


def test_each_label(cfg):
    regular = spikes([250.0, 300.0, 350.0, 400.0, 450.0])
    assert firing_regime(spikes([]), WINDOW, table(0.0), cfg) == "silent"
    assert firing_regime(spikes([300.0]), WINDOW, table(1.0), cfg) == "single_spike"
    assert firing_regime(spikes([210.0, 230.0, 250.0], plateau_from=262.0), WINDOW, table(3.0), cfg) == \
        "depolarization_block"
    assert firing_regime(regular, WINDOW, table(8.0, burst_count=2.0, adaptation_index=0.0), cfg) == "bursting"
    assert firing_regime(regular, WINDOW, table(6.0, burst_count=1.0, adaptation_index=0.3), cfg) == "adapting"
    assert firing_regime(regular, WINDOW, table(5.0, burst_count=1.0, adaptation_index=0.0), cfg) == "tonic"


def test_thresholds_come_from_config(cfg):
    regular = spikes([250.0, 300.0, 350.0, 400.0, 450.0])
    # adapting_min_index is 0.1 and is a strict ">" comparison
    assert firing_regime(regular, WINDOW, table(5.0, 1.0, 0.1), cfg) == "tonic"
    assert firing_regime(regular, WINDOW, table(5.0, 1.0, 0.1001), cfg) == "adapting"
    stricter = copy.deepcopy(cfg)
    stricter["firing_regime"]["bursting_min_bursts"] = 3
    assert firing_regime(regular, WINDOW, table(8.0, 2.0, 0.0), stricter) == "tonic"


def test_first_match_wins_and_config_order_is_honoured(cfg):
    regular = spikes([250.0, 300.0, 350.0, 400.0, 450.0])
    both = table(8.0, burst_count=2.0, adaptation_index=0.5)
    assert firing_regime(regular, WINDOW, both, cfg) == "bursting"
    reordered = copy.deepcopy(cfg)
    labels = reordered["firing_regime"]["labels"]
    i, j = labels.index("bursting"), labels.index("adapting")
    labels[i], labels[j] = labels[j], labels[i]
    assert firing_regime(regular, WINDOW, both, reordered) == "adapting"
    # a single spike followed by a plateau is single_spike, because that label comes first
    assert firing_regime(spikes([210.0], plateau_from=220.0), WINDOW, table(1.0), cfg) == "single_spike"


def test_depolarization_block_needs_early_stop_and_depolarised_plateau(cfg):
    rc = regime_config(cfg)
    args = (WINDOW, rc["threshold_mV"], rc["gap_fraction"], rc["block_v_mV"])
    assert depolarization_block(spikes([210.0, 230.0, 250.0], plateau_from=262.0), *args)
    assert not depolarization_block(spikes([210.0, 230.0, 250.0]), *args)                 # repolarised: not block
    assert not depolarization_block(spikes([210.0, 230.0, 450.0], plateau_from=462.0), *args)   # late spike
    assert not depolarization_block(spikes([210.0, 230.0, 250.0], plateau_from=262.0, plateau_mV=-45.0), *args)
    lower = copy.deepcopy(cfg)
    lower["firing_regime"]["depolarization_block_v_mV"] = -20.0
    assert firing_regime(spikes([210.0, 230.0, 250.0], plateau_from=262.0), WINDOW, table(3.0), lower) == "tonic"


def test_spike_count_falls_back_to_window_crossings(cfg):
    tr = spikes([100.0, 300.0, 650.0])               # only 300 ms lies inside the 200-600 ms window
    assert firing_regime(tr, WINDOW, {}, cfg) == "single_spike"
    undefined = {"spike_count": FeatureValue("spike_count", None, UNDEFINED, "1", "test")}
    assert firing_regime(tr, WINDOW, undefined, cfg) == "single_spike"
    assert firing_regime(spikes([]), WINDOW, undefined, cfg) == "silent"


@pytest.mark.parametrize("trace, window", [
    (Trace(np.array([0.0, 1.0]), np.array([-65.0, -65.0])), WINDOW),                 # two samples
    (Trace(np.array([0.0]), np.array([-65.0])), WINDOW),                              # one sample
    (spikes([210.0, 230.0, 250.0], plateau_from=262.0), AnalysisWindow(200.0, 5000.0)),   # window beyond trace
    (spikes([210.0, 230.0]), AnalysisWindow(600.0, 200.0)),                            # reversed window
    (Trace(uniform_grid(0.0, 0.025, 100), np.full(100, np.nan)), WINDOW),               # NaN voltages
    (Trace(np.empty(0), np.empty(0)), WINDOW),                                         # empty
])
@pytest.mark.parametrize("ft", [{}, None, "table"])
def test_never_raises_for_short_or_odd_traces(cfg, trace, window, ft):
    ft_value = table(2.0, None, None) if ft == "table" else ft
    assert firing_regime(trace, window, ft_value, cfg) in LABELS


def test_invalid_config_raises(cfg):
    bad = copy.deepcopy(cfg)
    bad["firing_regime"]["labels"] = ["silent", "tonic"]
    with pytest.raises(ValueError, match="labels"):
        firing_regime(spikes([]), WINDOW, table(0.0), bad)
    missing = copy.deepcopy(cfg)
    del missing["firing_regime"]["adapting_min_index"]
    with pytest.raises(ValueError, match="adapting_min_index"):
        regime_config(missing)
    with pytest.raises(ValueError):
        regime_config({"settings": {}})
