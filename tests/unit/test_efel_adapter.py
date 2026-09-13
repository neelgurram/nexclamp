"""Unit tests for features.efel_adapter on synthetic traces, with real eFEL 5.7.34 calls."""

from __future__ import annotations

import copy
import json
import warnings
from concurrent.futures import ThreadPoolExecutor

import efel
import numpy as np
import pytest

from neurosem.config import features as load_features_config
from neurosem.features.efel_adapter import (
    DEFINED,
    NOT_APPLICABLE,
    UNDEFINED,
    FeatureConfigError,
    FeatureValue,
    effective_settings,
    efel_settings,
    extract,
    extract_all,
    feature_table_from_json,
    feature_table_to_json,
    is_hyperpolarizing,
)
from neurosem.features.regimes import LABELS
from neurosem.features.trace_metrics import pack_traces, stored_representation, uniform_grid, unpack_traces
from neurosem.protocols.definitions import SPIKING
from neurosem.schemas import AnalysisWindow, ConcreteProtocol, StimulusComponent, Trace

DT, S0, S1, TOTAL = 0.025, 200.0, 600.0, 700.0
SUBTHRESHOLD = ("baseline_voltage", "steady_state_voltage", "voltage_deflection", "sag_ratio", "minimum_voltage",
                "maximum_voltage")


@pytest.fixture(scope="module")
def cfg() -> dict:
    return load_features_config().data


def grid() -> np.ndarray:
    return uniform_grid(0.0, DT, int(round(TOTAL / DT)) + 1)


def spiking_trace(spike_ms: list[float], step_mV: float = 5.0, plateau_from: float | None = None) -> Trace:
    """Sine-lobe spikes on a current-step plateau.

    Each spike is a 1 ms half sine rising 100 mV above the plateau, followed by a 6 ms
    half-sine after-hyperpolarisation of 8 mV.
    """
    t = grid()
    v = np.full_like(t, -65.0)
    v[(t >= S0) & (t < S1)] += step_mV
    for ts in spike_ms:
        up = (t >= ts) & (t < ts + 1.0)
        v[up] += 100.0 * np.sin(np.pi * (t[up] - ts))
        down = (t >= ts + 1.0) & (t < ts + 7.0)
        v[down] -= 8.0 * np.sin(np.pi * (t[down] - ts - 1.0) / 6.0)
    if plateau_from is not None:
        v[t >= plateau_from] = -30.0
    return Trace(t, v)


def sag_trace() -> Trace:
    """Hyperpolarising response with a slow partial recovery (sag), as produced by an h-current."""
    t = grid()
    v = np.full_like(t, -65.0)
    m = (t >= S0) & (t < S1)
    x = t[m] - S0
    v[m] = -65.0 - 20.0 * (1.0 - np.exp(-x / 5.0)) + 7.0 * (1.0 - np.exp(-x / 40.0))
    after = t >= S1
    v[after] = -65.0 + (v[m][-1] + 65.0) * np.exp(-(t[after] - S1) / 5.0)
    return Trace(t, v)


def flat_trace() -> Trace:
    t = grid()
    return Trace(t, np.full_like(t, -65.0))


def protocol(amplitude_nA: float, features, pid: str = "P_test") -> ConcreteProtocol:
    return ConcreteProtocol(pid, "step", (StimulusComponent("pulse", S0, S1 - S0, amplitude_nA),), TOTAL,
                            AnalysisWindow(S0, S1), tuple(features))


def direct_efel(trace: Trace, names: list[str], cfg: dict) -> dict:
    """Plain eFEL call with the configured settings, used as the reference for aggregation checks."""
    efel.reset()
    try:
        for k, v in cfg["settings"].items():
            efel.set_setting(k, v)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return efel.get_feature_values([{"T": trace.t_ms, "V": trace.v_mV, "stim_start": [S0],
                                             "stim_end": [S1]}], names)[0]
    finally:
        efel.reset()


# ------------------------------------------------------------ settings
def test_efel_settings_validates_repo_config(cfg):
    settings = efel_settings(cfg)
    assert settings == cfg["settings"]
    assert isinstance(settings["Threshold"], float) and settings["strict_stiminterval"] is True
    assert efel_settings(load_features_config()) == settings           # LoadedConfig accepted too
    eff = effective_settings(cfg)
    assert eff["efel_version"] == efel.__version__ == cfg["efel_version"]
    assert eff["settings"]["interp_step"] == 0.01 and eff["settings"]["ignore_first_ISI"] is False
    assert "/" not in eff["settings"]["dependencyfile_path"] and "\\" not in eff["settings"]["dependencyfile_path"]


@pytest.mark.parametrize("name, value, match", [
    ("Treshold", -20.0, "unknown eFEL setting"),
    ("Threshold", "high", "expects float"),
    ("Threshold", True, "expects float"),
    ("Threshold", float("nan"), "expects float"),
    ("strict_stiminterval", 1, "expects bool"),
    ("max_spike_skip", 2.5, "expects int"),
    ("voltage_base_mode", 3, "expects str"),
])
def test_efel_settings_rejects_bad_names_and_types(cfg, name, value, match):
    bad = copy.deepcopy(cfg)
    bad["settings"][name] = value
    with pytest.raises(ValueError, match=match):
        efel_settings(bad)


def test_int_is_accepted_for_float_setting(cfg):
    c = copy.deepcopy(cfg)
    c["settings"]["Threshold"] = -20
    assert efel_settings(c)["Threshold"] == -20.0 and isinstance(efel_settings(c)["Threshold"], float)


def test_settings_are_reset_before_every_extraction(cfg):
    tr = spiking_trace([250.0, 300.0, 350.0, 400.0, 450.0])
    p = protocol(0.5, SPIKING)
    clean = extract(tr, p, cfg, warnings=[])
    try:
        efel.set_setting("Threshold", 80.0)          # would detect no spikes at all
        efel.set_setting("interp_step", 0.5)
        efel.set_setting("NotASetting", 1.0)
        polluted = extract(tr, p, cfg, warnings=[])
    finally:
        efel.reset()
    assert clean["spike_count"].value == 5.0
    assert polluted == clean


# ------------------------------------------------------ feature states
def test_no_spike_trace_counts_zero_and_gates_spike_features(cfg):
    log: list[str] = []
    ft = extract(spiking_trace([]), protocol(0.1, SPIKING + SUBTHRESHOLD), cfg, warnings=log)
    assert list(ft) == list(dict.fromkeys(SPIKING + SUBTHRESHOLD))
    assert ft["spike_count"] == FeatureValue("spike_count", 0.0, DEFINED, "1", "efel:spike_count_stimint[scalar]")
    for name in ("mean_frequency", "first_spike_latency", "ap_amplitude", "ap_half_width", "ahp_depth", "first_isi",
                 "last_isi", "adaptation_index", "burst_count"):
        assert ft[name].state == NOT_APPLICABLE and ft[name].value is None, name
    assert ft["sag_ratio"].state == NOT_APPLICABLE                      # depolarising step
    # voltage_base averages the interpolated grid up to stim_start, which touches the step edge
    assert ft["baseline_voltage"].value == pytest.approx(-65.0, abs=0.01)
    assert ft["steady_state_voltage"].value == pytest.approx(-60.0, abs=0.01)
    assert ft["voltage_deflection"].value == pytest.approx(5.0, abs=0.01)
    assert ft["firing_regime"] == FeatureValue("firing_regime", "silent", DEFINED, "", "neurosem:firing_regime")
    assert log == []            # not-applicable features are never computed, so eFEL has nothing to warn about


def test_spiking_trace_aggregation_matches_raw_efel_arrays(cfg):
    tr = spiking_trace([220.0, 240.0, 270.0, 310.0, 370.0, 450.0])          # lengthening ISIs
    ft = extract(tr, protocol(0.5, SPIKING), cfg, warnings=[])
    raw = direct_efel(tr, ["all_ISI_values", "AP_amplitude", "AP_duration_half_width", "AHP_depth",
                           "adaptation_index2", "strict_burst_number", "time_to_first_spike"], cfg)
    assert ft["spike_count"].value == 6.0
    assert ft["first_isi"].value == raw["all_ISI_values"][0] == pytest.approx(20.0, abs=0.02)
    assert ft["last_isi"].value == raw["all_ISI_values"][-1] == pytest.approx(80.0, abs=0.02)
    assert ft["first_isi"].source == "efel:all_ISI_values[first]" and ft["last_isi"].source.endswith("[last]")
    assert ft["ap_amplitude"].value == raw["AP_amplitude"][0] == pytest.approx(100.0, abs=1.0)
    assert ft["ap_half_width"].value == raw["AP_duration_half_width"][0] == pytest.approx(2.0 / 3.0, abs=0.03)
    assert ft["ahp_depth"].value == raw["AHP_depth"][0]
    assert ft["adaptation_index"].value == raw["adaptation_index2"][0] > 0.1
    assert ft["burst_count"].value == raw["strict_burst_number"][0]
    assert ft["first_spike_latency"].value == pytest.approx(20.5, abs=0.02)      # measured to the peak
    assert ft["firing_regime"].value == "adapting"
    assert all(isinstance(v.value, float) for k, v in ft.items() if k != "firing_regime")


def test_min_spikes_gating_overrides_numbers_efel_would_return(cfg):
    one = spiking_trace([300.0])
    assert direct_efel(one, ["mean_frequency"], cfg)["mean_frequency"] is not None     # eFEL returns a rate
    ft1 = extract(one, protocol(0.5, SPIKING), cfg, warnings=[])
    assert ft1["mean_frequency"].state == NOT_APPLICABLE
    assert ft1["ap_amplitude"].state == DEFINED and ft1["first_spike_latency"].state == DEFINED
    assert ft1["first_isi"].state == NOT_APPLICABLE
    assert ft1["ahp_depth"].state == DEFINED          # min_spikes 1 (DECISIONS D-021): eFEL defines AHP after one spike
    assert ft1["firing_regime"].value == "single_spike"
    ft3 = extract(spiking_trace([250.0, 300.0, 350.0]), protocol(0.5, SPIKING), cfg, warnings=[])
    assert ft3["first_isi"].state == DEFINED and ft3["mean_frequency"].state == DEFINED
    assert ft3["adaptation_index"].state == NOT_APPLICABLE and ft3["burst_count"].state == NOT_APPLICABLE
    ft4 = extract(spiking_trace([250.0, 300.0, 350.0, 400.0]), protocol(0.5, SPIKING), cfg, warnings=[])
    assert ft4["adaptation_index"].state == DEFINED and ft4["burst_count"].state == DEFINED


def test_undefined_efel_result_is_recorded_not_zeroed_and_warning_captured(cfg):
    p = protocol(-0.3, ("sag_ratio", "voltage_deflection", "spike_count"), pid="P_flat")
    log: list[str] = []
    ft = extract(flat_trace(), p, cfg, warnings=log)
    assert ft["sag_ratio"] == FeatureValue("sag_ratio", None, UNDEFINED, "1", "efel:sag_ratio1[scalar]")
    assert ft["voltage_deflection"].value == 0.0 and ft["voltage_deflection"].state == DEFINED
    assert any(m.startswith("P_flat: RuntimeWarning") and "sag_ratio1" in m for m in log)
    with pytest.warns(RuntimeWarning, match="sag_ratio1"):
        extract(flat_trace(), p, cfg)                                  # no list: warnings propagate


def test_sag_ratio_requires_a_hyperpolarizing_protocol(cfg):
    hyper = extract(sag_trace(), protocol(-0.3, SUBTHRESHOLD), cfg, warnings=[])
    assert hyper["sag_ratio"].state == DEFINED
    # (ss - min) / (baseline - min) for this shape: about 3.9 / 16.9
    assert hyper["sag_ratio"].value == pytest.approx(0.23, abs=0.02)
    assert hyper["minimum_voltage"].value < hyper["baseline_voltage"].value - 15.0
    assert hyper["voltage_deflection"].value == pytest.approx(-13.0, abs=0.1)
    depol = extract(sag_trace(), protocol(0.3, SUBTHRESHOLD), cfg, warnings=[])
    assert depol["sag_ratio"].state == NOT_APPLICABLE
    assert depol["minimum_voltage"] == hyper["minimum_voltage"]


def test_is_hyperpolarizing_uses_the_summed_amplitude():
    def proto(*components):
        return ConcreteProtocol("P", "x", tuple(components), 100.0, AnalysisWindow(10.0, 50.0), ())
    assert is_hyperpolarizing(proto(StimulusComponent("pulse", 10.0, 40.0, -0.1)))
    assert not is_hyperpolarizing(proto(StimulusComponent("pulse", 10.0, 40.0, 0.0)))
    assert is_hyperpolarizing(proto(StimulusComponent("pulse", 10.0, 5.0, 0.2), StimulusComponent("pulse", 20.0, 5.0, -0.3)))
    assert is_hyperpolarizing(proto(StimulusComponent("ramp", 10.0, 40.0, start_nA=0.0, finish_nA=-1.0)))
    assert not is_hyperpolarizing(proto(StimulusComponent("ramp", 10.0, 40.0, start_nA=-0.2, finish_nA=1.0)))


# ------------------------------------------------------- regime labels
@pytest.mark.parametrize("trace, label", [
    (spiking_trace([250.0, 300.0, 350.0, 400.0, 450.0]), "tonic"),
    (spiking_trace([220.0, 226.0, 232.0, 350.0, 356.0, 362.0, 480.0, 486.0, 492.0]), "bursting"),
    (spiking_trace([210.0, 230.0, 250.0], step_mV=0.0, plateau_from=262.0), "depolarization_block"),
])
def test_regime_labels_from_real_efel_outputs(cfg, trace, label):
    ft = extract(trace, protocol(0.5, ("firing_regime",)), cfg, warnings=[])
    assert list(ft) == ["firing_regime"] and ft["firing_regime"].value == label in LABELS


# ------------------------------------------------ protocol feature set
def test_only_protocol_features_are_returned_and_rheobase_is_left_out(cfg):
    ft = extract(spiking_trace([300.0, 350.0]), protocol(0.5, ("firing_regime", "ap_amplitude", "rheobase")), cfg,
                 warnings=[])
    assert list(ft) == ["firing_regime", "ap_amplitude"]
    with pytest.raises(FeatureConfigError, match="not defined"):
        extract(spiking_trace([]), protocol(0.5, ("spike_count", "input_resistance")), cfg)


def test_scalar_aggregation_requires_exactly_one_value(cfg):
    bad = copy.deepcopy(cfg)
    bad["features"]["ap_amplitude"]["agg"] = "scalar"
    with pytest.raises(FeatureConfigError, match="scalar"):
        extract(spiking_trace([250.0, 300.0, 350.0]), protocol(0.5, ("ap_amplitude",)), bad, warnings=[])


@pytest.mark.parametrize("path, value, match", [
    (("features", "ap_amplitude", "efel"), "AP_amplitudes", "not an eFEL"),
    (("features", "ap_amplitude", "agg"), "mean", "agg"),
    (("features", "sag_ratio", "requires"), "depolarizing", "requirement"),
    (("features", "first_isi", "min_spikes"), -1, "min_spikes"),
    (("features", "spike_count", "min_spikes"), 1, "spike_count"),
    (("efel_version",), "0.0.1", "pins eFEL"),
])
def test_invalid_feature_config_is_rejected(cfg, path, value, match):
    bad = copy.deepcopy(cfg)
    node = bad
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    with pytest.raises(FeatureConfigError, match=match):
        extract(spiking_trace([300.0]), protocol(0.5, ("spike_count",)), bad, warnings=[])


def test_trace_problems(cfg):
    tr = spiking_trace([300.0])
    v = tr.v_mV.copy()
    v[100] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        extract(Trace(tr.t_ms, v), protocol(0.5, ("spike_count",)), cfg)
    outside = ConcreteProtocol("P", "step", (), TOTAL, AnalysisWindow(800.0, 900.0), ("spike_count",))
    with pytest.raises(ValueError, match="outside"):
        extract(tr, outside, cfg)
    inside = ConcreteProtocol("P_inside", "step", (), TOTAL, AnalysisWindow(S0, TOTAL), ("spike_count",))
    log: list[str] = []
    assert extract(tr, inside, cfg, warnings=log)["spike_count"].value == 1.0 and log == []


@pytest.mark.parametrize("start, end, trace_from", [
    (S0, TOTAL + 150.0, 0.0),             # runs 150 ms past the end: spike counts over unrecorded time
    (S0, TOTAL + 1.5 * DT, 0.0),          # just over one step past the end
    (S0 - 50.0, S1, S0),                  # starts 50 ms before the trace: no pre-stimulus baseline exists
])
def test_window_overrunning_the_trace_by_more_than_one_step_is_refused(cfg, start, end, trace_from):
    tr = spiking_trace([300.0])
    keep = tr.t_ms >= trace_from
    p = ConcreteProtocol("P_over", "step", (), TOTAL, AnalysisWindow(start, end), ("spike_count", "baseline_voltage"))
    with pytest.raises(ValueError, match="more than one sample step"):
        extract(Trace(tr.t_ms[keep], tr.v_mV[keep]), p, cfg, warnings=[])


def test_window_overrunning_by_one_step_is_accepted_with_a_note(cfg):
    """Output sampling can drop the last sample; a one-step overrun is allowed and recorded."""
    tr = spiking_trace([300.0])
    p = ConcreteProtocol("P_edge", "step", (), TOTAL, AnalysisWindow(S0, TOTAL + DT), ("spike_count",))
    log: list[str] = []
    assert extract(tr, p, cfg, warnings=log)["spike_count"].value == 1.0
    assert any(m.startswith("P_edge: analysis window") and "less than one sample step" in m for m in log)


# ---------------------------------------------------- tables and JSON
def test_feature_value_invariants():
    with pytest.raises(ValueError):
        FeatureValue("x", None, DEFINED, "mV", "s")
    with pytest.raises(ValueError):
        FeatureValue("x", 1.0, UNDEFINED, "mV", "s")
    with pytest.raises(ValueError):
        FeatureValue("x", float("inf"), DEFINED, "mV", "s")
    with pytest.raises(ValueError):
        FeatureValue("x", 1.0, "missing", "mV", "s")
    fv = FeatureValue("x", np.int64(3), DEFINED, "1", "s")
    assert type(fv.value) is float and fv.value == 3.0


def test_json_round_trip_is_exact(cfg):
    tables = extract_all({"A": spiking_trace([220.0, 240.0, 270.0, 310.0, 370.0]), "B": flat_trace()},
                         [protocol(0.5, SPIKING, "A"), protocol(-0.3, SUBTHRESHOLD + ("spike_count",), "B")], cfg,
                         warnings=[])
    for ft in tables.values():
        blob = json.loads(json.dumps(feature_table_to_json(ft), sort_keys=True))
        assert feature_table_from_json(blob) == ft
    assert feature_table_to_json(tables["B"])["sag_ratio"]["value"] is None
    with pytest.raises(ValueError):
        feature_table_from_json({"x": {"name": "x", "value": 1.0, "state": "bogus", "unit": "", "source": ""}})
    with pytest.raises(ValueError):
        feature_table_from_json({"x": {"name": "y", "value": 1.0, "state": DEFINED, "unit": "", "source": ""}})


def test_extract_all_requires_a_trace_per_protocol(cfg):
    with pytest.raises(KeyError, match="P_missing"):
        extract_all({"A": flat_trace()}, [protocol(0.1, ("spike_count",), "A"), protocol(0.1, ("spike_count",),
                                                                                          "P_missing")], cfg)


# ------------------------------------------------------ reproducibility
def test_features_reproduce_exactly_from_the_stored_representation(cfg):
    raw = spiking_trace([220.0, 240.0, 270.0, 310.0, 370.0, 450.0])
    p = protocol(0.5, SPIKING + SUBTHRESHOLD)
    from_bytes = extract(unpack_traces(pack_traces({"P_test": raw}))["P_test"], p, cfg, warnings=[])
    assert extract(stored_representation(raw), p, cfg, warnings=[]) == from_bytes
    assert extract(unpack_traces(pack_traces({"P_test": raw}))["P_test"], p, cfg, warnings=[]) == from_bytes


def test_concurrent_extractions_do_not_share_settings(cfg):
    high = copy.deepcopy(cfg)
    high["settings"]["Threshold"] = 50.0          # the 35 mV spike peaks never reach it
    tr = spiking_trace([250.0, 300.0, 350.0, 400.0, 450.0], step_mV=0.0)
    p = protocol(0.5, ("spike_count", "ap_amplitude", "firing_regime"))
    expected = {"low": extract(tr, p, cfg, warnings=[]), "high": extract(tr, p, high, warnings=[])}
    assert expected["low"]["spike_count"].value == 5.0 and expected["high"]["spike_count"].value == 0.0
    jobs = ["low", "high"] * 8
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda k: extract(tr, p, cfg if k == "low" else high, warnings=[]), jobs))
    assert all(r == expected[k] for k, r in zip(jobs, results))
