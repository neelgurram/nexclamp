"""Stimulation-protocol catalogue (spec: "Protocol battery").

Protocols are *templates* whose depolarising amplitudes are multiples of the
reference model's rheobase, so the same test means the same thing across models.
A template is instantiated once per reference model; every variant of that model
receives exactly the same concrete stimulus.

All timing is in whole milliseconds so stimulus edges fall on the grid of every
refinement level (h, h/2, h/4) -- otherwise refinement itself would move the stimulus.
"""

from __future__ import annotations

import dataclasses as dc
from collections.abc import Mapping, Sequence
from typing import Any

from neurosem.schemas import AnalysisWindow, ConcreteProtocol, StimulusComponent

SPIKING = ("spike_count", "mean_frequency", "first_spike_latency", "ap_amplitude", "ap_half_width",
           "ahp_depth", "first_isi", "last_isi", "adaptation_index", "burst_count", "firing_regime")
SUBTHRESHOLD = ("baseline_voltage", "steady_state_voltage", "voltage_deflection", "spike_count")


@dc.dataclass(frozen=True)
class ProtocolTemplate:
    protocol_id: str
    kind: str
    description: str
    params: Mapping[str, float]
    features: tuple[str, ...]
    implemented: bool = True
    not_implemented_reason: str = ""

    def instantiate(self, rheobase_nA: float, settle_ms: float) -> ConcreteProtocol:
        if not self.implemented:
            raise NotImplementedError(f"{self.protocol_id}: {self.not_implemented_reason}")
        if not float(settle_ms).is_integer():
            raise ValueError("settle_ms must be a whole number of ms so stimulus edges stay on every refinement grid")
        p, s, rh = self.params, float(settle_ms), float(rheobase_nA)
        comps: list[StimulusComponent]
        if self.kind == "baseline":
            dur = p["duration_ms"]
            comps = [StimulusComponent("pulse", s, dur, 0.0)]
            total, window = s + dur, AnalysisWindow(s, s + dur)
        elif self.kind == "step":
            dur = p["duration_ms"]
            comps = [StimulusComponent("pulse", s, dur, p["multiple"] * rh)]
            total, window = s + dur + p["post_ms"], AnalysisWindow(s, s + dur)
        elif self.kind == "ramp":
            dur = p["duration_ms"]
            comps = [StimulusComponent("ramp", s, dur, start_nA=0.0, finish_nA=p["finish_multiple"] * rh)]
            total, window = s + dur + p["post_ms"], AnalysisWindow(s, s + dur)
        elif self.kind == "rebound":
            dur = p["duration_ms"]
            comps = [StimulusComponent("pulse", s, dur, -abs(p["multiple"]) * rh)]
            release = s + dur
            total, window = release + p["post_window_ms"], AnalysisWindow(release, release + p["post_window_ms"])
        elif self.kind == "short_pulse":
            comps = [StimulusComponent("pulse", s, p["pulse_ms"], p["multiple"] * rh)]
            total, window = s + p["window_ms"] + p["post_ms"], AnalysisWindow(s, s + p["window_ms"])
        elif self.kind == "paired_pulse":
            second = s + p["pulse_ms"] + p["interval_ms"]
            comps = [StimulusComponent("pulse", s, p["pulse_ms"], p["multiple"] * rh),
                     StimulusComponent("pulse", second, p["pulse_ms"], p["multiple"] * rh)]
            total, window = s + p["window_ms"] + p["post_ms"], AnalysisWindow(s, s + p["window_ms"])
        else:
            raise ValueError(f"{self.protocol_id}: kind {self.kind!r} is not a batched current-clamp protocol")
        return ConcreteProtocol(self.protocol_id, self.kind, tuple(comps), float(total), window,
                                self.features, rheobase_nA=rh, description=self.description)


# Default catalogue, numbered as in the specification. Parameters are provisional
# until frozen in configs/study.yaml (see DECISIONS.md).
DEFAULT_TEMPLATES: tuple[ProtocolTemplate, ...] = (
    ProtocolTemplate("P01_baseline", "baseline", "Zero-current baseline", {"duration_ms": 700},
                     ("baseline_voltage", "steady_state_voltage", "spike_count", "firing_regime")),
    ProtocolTemplate("P02_weak_step", "step", "Weak depolarising step (0.5 x rheobase)",
                     {"multiple": 0.5, "duration_ms": 500, "post_ms": 200},
                     ("baseline_voltage", "steady_state_voltage", "voltage_deflection", "spike_count")),
    ProtocolTemplate("P03_rheobase", "rheobase", "Rheobase search (500 ms steps, bracketing grid)",
                     {"duration_ms": 500, "post_ms": 0}, ("rheobase",)),
    ProtocolTemplate("P04_step_2x", "step", "Step at 2 x rheobase", {"multiple": 2.0, "duration_ms": 500, "post_ms": 200},
                     SPIKING),
    ProtocolTemplate("P05_long_step", "step", "Long suprathreshold step (1.5 x rheobase, 2 s)",
                     {"multiple": 1.5, "duration_ms": 2000, "post_ms": 200}, SPIKING),
    ProtocolTemplate("P06_ramp", "ramp", "Depolarising ramp 0 -> 3 x rheobase over 1 s",
                     {"finish_multiple": 3.0, "duration_ms": 1000, "post_ms": 200},
                     ("spike_count", "first_spike_latency", "mean_frequency", "firing_regime")),
    ProtocolTemplate("P07_hyperpolarizing_step", "step", "Hyperpolarising step (-1 x rheobase)",
                     {"multiple": -1.0, "duration_ms": 500, "post_ms": 200},
                     ("baseline_voltage", "steady_state_voltage", "voltage_deflection", "sag_ratio", "minimum_voltage")),
    ProtocolTemplate("P08_rebound", "rebound", "Hyperpolarisation (-2 x rheobase, 500 ms) then release",
                     {"multiple": 2.0, "duration_ms": 500, "post_window_ms": 300},
                     ("spike_count", "first_spike_latency", "maximum_voltage", "firing_regime")),
    ProtocolTemplate("P09_short_pulse", "short_pulse", "Short suprathreshold pulse (3 ms, 10 x rheobase)",
                     {"multiple": 10.0, "pulse_ms": 3, "window_ms": 60, "post_ms": 140},
                     ("spike_count", "first_spike_latency", "ap_amplitude", "ap_half_width", "ahp_depth")),
    ProtocolTemplate("P10_paired_pulses", "paired_pulse", "Paired pulses (3 ms, 10 x rheobase, 20 ms apart)",
                     {"multiple": 10.0, "pulse_ms": 3, "interval_ms": 20, "window_ms": 80, "post_ms": 120},
                     ("spike_count", "first_spike_latency", "first_isi", "ap_amplitude")),
    ProtocolTemplate("P11_chirp", "chirp", "Deterministic chirp", {}, (), implemented=False,
                     not_implemented_reason="NeuroML v2.3.1 core inputs have no chirp type (sineGenerator has a fixed "
                                            "period); deferred as the specification allows"),
    ProtocolTemplate("P12_frozen_noise", "frozen_noise", "Frozen pseudo-random waveform", {}, (), implemented=False,
                     not_implemented_reason="no core arbitrary-waveform input; later extension per specification"),
)

CANONICAL_ID = "P00_canonical"
CANONICAL_FEATURES = ("baseline_voltage", "spike_count", "mean_frequency", "first_spike_latency", "ap_amplitude",
                      "ap_half_width", "ahp_depth", "first_isi", "last_isi", "adaptation_index", "firing_regime")


def templates_from_config(cfg: Sequence[Mapping[str, Any]] | None) -> tuple[ProtocolTemplate, ...]:
    """Build templates from ``configs/study.yaml`` (falls back to the defaults)."""
    if not cfg:
        return DEFAULT_TEMPLATES
    out = []
    defaults = {t.protocol_id: t for t in DEFAULT_TEMPLATES}
    for entry in cfg:
        base = defaults.get(entry["protocol_id"])
        out.append(ProtocolTemplate(
            protocol_id=entry["protocol_id"],
            kind=entry.get("kind", base.kind if base else ""),
            description=entry.get("description", base.description if base else ""),
            params={**(base.params if base else {}), **entry.get("params", {})},
            features=tuple(entry.get("features", base.features if base else ())),
            implemented=entry.get("implemented", base.implemented if base else True),
            not_implemented_reason=entry.get("not_implemented_reason", base.not_implemented_reason if base else ""),
        ))
    return tuple(out)


def batched(templates: Sequence[ProtocolTemplate]) -> list[ProtocolTemplate]:
    """Templates that run as one population each in a batched probe simulation."""
    return [t for t in templates if t.implemented and t.kind not in ("rheobase", "canonical")]
