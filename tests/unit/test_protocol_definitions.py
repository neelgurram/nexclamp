"""Tests for nexclamp.protocols.definitions: template instantiation, timing grid and catalogue consistency."""

from __future__ import annotations

import dataclasses as dc
import math

import pytest

from nexclamp import config
from nexclamp.protocols.definitions import (
    CANONICAL_FEATURES,
    CANONICAL_ID,
    DEFAULT_TEMPLATES,
    ProtocolTemplate,
    batched,
    templates_from_config,
)
from nexclamp.schemas import AnalysisWindow, ConcreteProtocol, StimulusComponent

T = {t.protocol_id: t for t in DEFAULT_TEMPLATES}
IMPLEMENTED = [t for t in DEFAULT_TEMPLATES if t.implemented and t.kind != "rheobase"]
DT_LEVELS = [0.005, 0.0025, 0.00125, 0.025, 0.01]
RH = 0.1
SETTLE = 300.0


def _edges(p: ConcreteProtocol) -> list[float]:
    out = [p.total_ms, p.window.start_ms, p.window.end_ms]
    for c in p.components:
        out += [c.delay_ms, c.delay_ms + c.duration_ms]
    return out


# --------------------------------------------------------------------------------- catalogue
def test_catalogue_ids_follow_specification_numbering():
    assert [t.protocol_id for t in DEFAULT_TEMPLATES] == [
        "P01_baseline", "P02_weak_step", "P03_rheobase", "P04_step_2x", "P05_long_step", "P06_ramp",
        "P07_hyperpolarizing_step", "P08_rebound", "P09_short_pulse", "P10_paired_pulses", "P11_chirp",
        "P12_frozen_noise"]
    assert CANONICAL_ID == "P00_canonical"


def test_batched_excludes_rheobase_and_not_implemented():
    ids = [t.protocol_id for t in batched(DEFAULT_TEMPLATES)]
    assert ids == ["P01_baseline", "P02_weak_step", "P04_step_2x", "P05_long_step", "P06_ramp",
                   "P07_hyperpolarizing_step", "P08_rebound", "P09_short_pulse", "P10_paired_pulses"]
    extra = ProtocolTemplate("PX", "canonical", "", {}, ())
    assert batched([*DEFAULT_TEMPLATES, extra]) == batched(DEFAULT_TEMPLATES)


@pytest.mark.parametrize("pid", ["P11_chirp", "P12_frozen_noise"])
def test_not_implemented_templates_raise_with_reason(pid):
    t = T[pid]
    assert not t.implemented and t.not_implemented_reason
    with pytest.raises(NotImplementedError, match=pid):
        t.instantiate(RH, SETTLE)


def test_rheobase_template_is_not_instantiable_as_battery_protocol():
    with pytest.raises(ValueError, match="not a batched current-clamp protocol"):
        T["P03_rheobase"].instantiate(RH, SETTLE)


def test_unknown_kind_raises():
    with pytest.raises(ValueError, match="kind 'sine'"):
        ProtocolTemplate("PX", "sine", "", {}, ()).instantiate(RH, SETTLE)


def test_every_protocol_feature_is_defined_in_features_config():
    defined = set(config.features()["features"])
    for t in DEFAULT_TEMPLATES:
        assert set(t.features) <= defined, t.protocol_id
    assert set(CANONICAL_FEATURES) <= defined


def test_every_numeric_feature_has_a_tolerance():
    feats = config.features()["features"]
    tol = config.tolerances()
    numeric = {k for k, v in feats.items() if v.get("kind") != "categorical"}
    assert numeric <= set(tol["features"])
    assert set(tol["categorical"]) == {k for k, v in feats.items() if v.get("kind") == "categorical"}


def test_hyperpolarizing_only_features_are_used_with_negative_stimuli():
    feats = config.features()["features"]
    needs_neg = {k for k, v in feats.items() if v.get("requires") == "hyperpolarizing"}
    for t in IMPLEMENTED:
        if needs_neg & set(t.features):
            p = t.instantiate(RH, SETTLE)
            assert sum(c.amplitude_nA for c in p.components) < 0, t.protocol_id


# ------------------------------------------------------------------------------- instantiation
def test_baseline():
    p = T["P01_baseline"].instantiate(RH, SETTLE)
    assert p.components == (StimulusComponent("pulse", 300.0, 700, 0.0),)
    assert p.total_ms == 1000.0 and p.window == AnalysisWindow(300.0, 1000.0)
    assert p.rheobase_nA == RH and p.kind == "baseline"


def test_weak_step():
    p = T["P02_weak_step"].instantiate(RH, SETTLE)
    (c,) = p.components
    assert (c.kind, c.delay_ms, c.duration_ms) == ("pulse", 300.0, 500)
    assert c.amplitude_nA == pytest.approx(0.05, abs=1e-15)
    assert p.total_ms == 1000.0 and p.window == AnalysisWindow(300.0, 800.0)


@pytest.mark.parametrize("pid, amp, dur, total", [
    ("P04_step_2x", 0.2, 500, 1000.0),
    ("P05_long_step", 0.15, 2000, 2500.0),
    ("P07_hyperpolarizing_step", -0.1, 500, 1000.0),
])
def test_steps(pid, amp, dur, total):
    p = T[pid].instantiate(RH, SETTLE)
    (c,) = p.components
    assert c.kind == "pulse" and c.delay_ms == 300.0 and c.duration_ms == dur
    assert c.amplitude_nA == pytest.approx(amp, abs=1e-15)
    assert p.total_ms == total and p.window == AnalysisWindow(300.0, 300.0 + dur)


def test_ramp():
    p = T["P06_ramp"].instantiate(RH, SETTLE)
    (c,) = p.components
    assert c.kind == "ramp" and c.delay_ms == 300.0 and c.duration_ms == 1000
    assert c.start_nA == 0.0 and c.baseline_nA == 0.0 and c.amplitude_nA == 0.0
    assert c.finish_nA == pytest.approx(0.3, abs=1e-15)
    assert p.total_ms == 1500.0 and p.window == AnalysisWindow(300.0, 1300.0)


def test_rebound_window_follows_release():
    p = T["P08_rebound"].instantiate(RH, SETTLE)
    (c,) = p.components
    assert c.kind == "pulse" and c.delay_ms == 300.0 and c.duration_ms == 500
    assert c.amplitude_nA == pytest.approx(-0.2, abs=1e-15)
    assert p.window == AnalysisWindow(800.0, 1100.0) and p.total_ms == 1100.0


def test_rebound_is_hyperpolarizing_regardless_of_multiple_sign():
    t = dc.replace(T["P08_rebound"], params={**T["P08_rebound"].params, "multiple": -2.0})
    assert t.instantiate(RH, SETTLE).components[0].amplitude_nA == pytest.approx(-0.2)


def test_short_pulse():
    p = T["P09_short_pulse"].instantiate(RH, SETTLE)
    (c,) = p.components
    assert (c.delay_ms, c.duration_ms) == (300.0, 3)
    assert c.amplitude_nA == pytest.approx(1.0, abs=1e-15)
    assert p.window == AnalysisWindow(300.0, 360.0) and p.total_ms == 500.0


def test_paired_pulses_interval_is_offset_to_onset():
    p = T["P10_paired_pulses"].instantiate(RH, SETTLE)
    a, b = p.components
    assert (a.delay_ms, a.duration_ms) == (300.0, 3) and (b.delay_ms, b.duration_ms) == (323.0, 3)
    assert b.delay_ms - (a.delay_ms + a.duration_ms) == 20                 # 'interval' = gap between pulses
    assert a.amplitude_nA == b.amplitude_nA == pytest.approx(1.0, abs=1e-15)
    assert p.window == AnalysisWindow(300.0, 380.0) and p.total_ms == 500.0


def test_features_and_description_propagate():
    for t in IMPLEMENTED:
        p = t.instantiate(RH, SETTLE)
        assert p.protocol_id == t.protocol_id and p.features == t.features and p.description == t.description


# --------------------------------------------------------------------------------------- timing
@pytest.mark.parametrize("settle", [0, 100, 300, 1000])
def test_all_edges_on_integer_milliseconds(settle):
    for t in IMPLEMENTED:
        for e in _edges(t.instantiate(0.137, settle)):
            assert float(e).is_integer(), (t.protocol_id, e)


def test_edges_fall_on_every_refinement_grid():
    """Edges must be whole multiples of every dt level, otherwise refinement would move the stimulus."""
    for t in IMPLEMENTED:
        for e in _edges(t.instantiate(RH, SETTLE)):
            for dt in DT_LEVELS:
                n = e / dt
                assert math.isclose(n, round(n), rel_tol=0, abs_tol=1e-6), (t.protocol_id, e, dt)


def test_windows_lie_inside_simulation_and_stimuli_start_after_settle():
    for t in IMPLEMENTED:
        p = t.instantiate(RH, SETTLE)
        assert 0 <= p.window.start_ms < p.window.end_ms <= p.total_ms, t.protocol_id
        for c in p.components:
            assert c.delay_ms >= SETTLE and c.delay_ms + c.duration_ms <= p.total_ms, t.protocol_id


def test_timing_does_not_depend_on_rheobase_and_amplitudes_scale_linearly():
    for t in IMPLEMENTED:
        a, b = t.instantiate(0.1, SETTLE), t.instantiate(0.37, SETTLE)
        assert a.total_ms == b.total_ms and a.window == b.window
        for ca, cb in zip(a.components, b.components, strict=True):
            assert (ca.kind, ca.delay_ms, ca.duration_ms) == (cb.kind, cb.delay_ms, cb.duration_ms)
            for field in ("amplitude_nA", "start_nA", "finish_nA", "baseline_nA"):
                assert getattr(cb, field) == pytest.approx(getattr(ca, field) * 3.7, abs=1e-12), (t.protocol_id, field)
        assert b.rheobase_nA == 0.37


def test_settle_shifts_everything_rigidly():
    for t in IMPLEMENTED:
        a, b = t.instantiate(RH, 100), t.instantiate(RH, 350)
        assert b.total_ms - a.total_ms == 250
        assert [e - 250 for e in _edges(b)] == _edges(a)


def test_instantiate_coerces_to_float():
    p = T["P04_step_2x"].instantiate(1, 300)
    assert isinstance(p.total_ms, float) and isinstance(p.rheobase_nA, float)
    assert isinstance(p.components[0].delay_ms, float)


# ------------------------------------------------------------------------------ config overrides
def test_study_config_reproduces_default_catalogue():
    # The frozen confirmatory study selects a subset of the catalogue; every selected protocol
    # must still match its catalogue definition exactly, parameters and all.
    defaults = {t.protocol_id: t for t in DEFAULT_TEMPLATES}
    selected = templates_from_config(config.study()["protocols"])
    assert selected, "the study must select at least one protocol"
    for t in selected:
        base = defaults[t.protocol_id]
        assert t.kind == base.kind and t.params == base.params, t.protocol_id
    assert templates_from_config(None) == DEFAULT_TEMPLATES


@pytest.mark.parametrize("cfg", [None, []])
def test_empty_config_falls_back_to_defaults(cfg):
    assert templates_from_config(cfg) is DEFAULT_TEMPLATES


def test_config_merges_params_over_defaults():
    (t,) = templates_from_config([{"protocol_id": "P04_step_2x", "params": {"multiple": 3.0}}])
    assert t.params == {"multiple": 3.0, "duration_ms": 500, "post_ms": 200}
    assert t.kind == "step" and t.features == T["P04_step_2x"].features
    assert t.instantiate(RH, SETTLE).components[0].amplitude_nA == pytest.approx(0.3)
    assert T["P04_step_2x"].params["multiple"] == 2.0                   # default catalogue untouched


def test_config_can_define_new_protocol():
    (t,) = templates_from_config([{"protocol_id": "P13_big_step", "kind": "step", "description": "x",
                                   "params": {"multiple": 4.0, "duration_ms": 100, "post_ms": 50},
                                   "features": ["spike_count"]}])
    assert t.implemented and t.features == ("spike_count",)
    p = t.instantiate(0.25, 20)
    assert p.total_ms == 170.0 and p.components[0].amplitude_nA == 1.0


def test_config_can_disable_protocol():
    (t,) = templates_from_config([{"protocol_id": "P02_weak_step", "implemented": False,
                                   "not_implemented_reason": "excluded by preregistration"}])
    assert batched([t]) == []
    with pytest.raises(NotImplementedError, match="excluded by preregistration"):
        t.instantiate(RH, SETTLE)
