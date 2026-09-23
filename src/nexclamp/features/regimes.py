"""Qualitative firing regime (spec feature "Qualitative firing regime").

eFEL has no single regime feature. NeuroSem labels a trace from three eFEL outputs
(spike count, strict burst count, adaptation index) plus one check on the trace itself,
in the order given in ``configs/features.yaml``. The first label whose condition holds
wins. The label is categorical: a changed label is a detection whatever the numeric
tolerances say.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

import numpy as np

from nexclamp.features.trace_metrics import spike_times
from nexclamp.schemas import AnalysisWindow, Trace

if TYPE_CHECKING:
    from nexclamp.features.efel_adapter import FeatureTable

LABELS = ("silent", "single_spike", "depolarization_block", "bursting", "adapting", "tonic")
DEFAULT_THRESHOLD_MV = -20.0        # eFEL's default spike Threshold
DEFAULT_BLOCK_V_MV = -40.0          # see docs/build_notes/features.md: only stated in a features.yaml comment


def regime_config(cfg: Any) -> dict[str, Any]:
    """Validated regime parameters from the feature config (a dict or ``LoadedConfig``)."""
    data = getattr(cfg, "data", cfg)
    if not isinstance(data, Mapping) or not isinstance(data.get("firing_regime"), Mapping):
        raise ValueError("feature config has no 'firing_regime' section")
    section = data["firing_regime"]
    labels = tuple(section.get("labels", LABELS))
    if len(set(labels)) != len(labels) or set(labels) != set(LABELS):
        raise ValueError(f"firing_regime labels must be an ordering of {LABELS}, got {labels}")
    settings = data.get("settings") or {}
    try:
        out = {
            "labels": labels,
            "threshold_mV": float(settings.get("Threshold", DEFAULT_THRESHOLD_MV)),
            "gap_fraction": float(section["depolarization_block_min_gap_fraction"]),
            "block_v_mV": float(section.get("depolarization_block_v_mV", DEFAULT_BLOCK_V_MV)),
            "min_bursts": float(section["bursting_min_bursts"]),
            "adapting_min_index": float(section["adapting_min_index"]),
        }
    except KeyError as exc:
        raise ValueError(f"firing_regime config lacks {exc.args[0]!r}") from None
    if not 0.0 < out["gap_fraction"] <= 1.0:
        raise ValueError("depolarization_block_min_gap_fraction must lie in (0, 1]")
    return out


def _defined_number(ft: Mapping[str, Any] | None, name: str) -> float | None:
    fv = ft.get(name) if ft else None
    if fv is None or getattr(fv, "state", None) != "defined":
        return None
    value = getattr(fv, "value", None)
    if isinstance(value, bool) or not isinstance(value, (int, float, np.number)):
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def _window_spike_times(trace: Trace, window: AnalysisWindow, threshold_mV: float) -> np.ndarray:
    try:
        times = spike_times(trace, threshold_mV)
    except (TypeError, ValueError):
        return np.empty(0, dtype=np.float64)
    return times[(times >= window.start_ms) & (times <= window.end_ms)]


def depolarization_block(trace: Trace, window: AnalysisWindow, threshold_mV: float, gap_fraction: float,
                         block_v_mV: float) -> bool:
    """Spiking stopped early in the window while the membrane stayed depolarised.

    In depolarisation block a cell stops firing because its sodium channels stay
    inactivated at a depolarised plateau. A cell that simply adapts into silence
    repolarises instead. The two cases are told apart by the lowest voltage over the late
    part of the window, which starts ``gap_fraction`` of the way through it.
    """
    try:
        t = np.asarray(trace.t_ms, dtype=np.float64)
        v = np.asarray(trace.v_mV, dtype=np.float64)
    except (TypeError, ValueError):
        return False
    duration = window.end_ms - window.start_ms
    if t.ndim != 1 or t.shape != v.shape or t.size < 2 or not duration > 0:
        return False
    cut = window.start_ms + gap_fraction * duration
    times = _window_spike_times(trace, window, threshold_mV)
    if times.size == 0 or times[-1] >= cut:
        return False
    late = (t >= cut) & (t <= window.end_ms)
    if not np.any(late) or not np.all(np.isfinite(v[late])):
        return False
    return bool(np.min(v[late]) > block_v_mV)


def firing_regime(trace: Trace, window: AnalysisWindow, ft: FeatureTable, cfg: Any) -> str:
    """One of :data:`LABELS`. Never raises for short or odd traces (config errors do raise).

    ``ft`` supplies ``spike_count``, ``burst_count`` and ``adaptation_index``. A missing,
    undefined or not-applicable entry means that condition does not hold. If the spike
    count itself is unavailable, upward threshold crossings inside the window are counted
    instead.
    """
    rc = regime_config(cfg)
    n = _defined_number(ft, "spike_count")
    n_spikes = int(round(n)) if n is not None and n >= 0 else int(_window_spike_times(trace, window,
                                                                                      rc["threshold_mV"]).size)
    bursts = _defined_number(ft, "burst_count")
    adaptation = _defined_number(ft, "adaptation_index")
    checks = {
        "silent": lambda: n_spikes == 0,
        "single_spike": lambda: n_spikes == 1,
        "depolarization_block": lambda: n_spikes >= 1 and depolarization_block(
            trace, window, rc["threshold_mV"], rc["gap_fraction"], rc["block_v_mV"]),
        "bursting": lambda: bursts is not None and bursts >= rc["min_bursts"],
        "adapting": lambda: adaptation is not None and adaptation > rc["adapting_min_index"],
        "tonic": lambda: True,
    }
    for label in rc["labels"]:
        if checks[label]():
            return label
    return "tonic"
