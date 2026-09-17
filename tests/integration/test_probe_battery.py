"""Integration tests: the whole implemented protocol battery on the RS reference cell through jLEMS.

All populations are the same uncoupled cell from the same initial state, so before any
stimulus onset every trace must be bit-identical to the zero-current baseline trace; the
first sample that differs marks when the stimulus actually reached the cell. That turns
"the stimulus starts where the protocol says" into an exact, model-independent check.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pytest

from neuraxis import config
from neuraxis.models import materialize
from neuraxis.protocols.definitions import DEFAULT_TEMPLATES, batched
from neuraxis.protocols.generate import group_by_length, write_probe
from neuraxis.protocols.rheobase import make_step_counter
from neuraxis.schemas import ExecConfig, RunStatus, SimResult
from neuraxis.simulators.jneuroml import JNeuroML

pytestmark = pytest.mark.jnml

DT = 0.025
RHEOBASE = 0.1
SETTLE = float(config.study()["numerics"]["settle_ms"])


@pytest.fixture(scope="module")
def battery(tmp_path_factory, models):
    """Instantiate all implemented templates for RS, group by length, run each group once (in parallel)."""
    sim = JNeuroML()
    if not sim.available():
        pytest.skip("Java or jNeuroML jar not available")
    ws = materialize(models["pospischil2008_rs"], tmp_path_factory.mktemp("battery") / "rs")
    protos = [t.instantiate(RHEOBASE, SETTLE) for t in batched(DEFAULT_TEMPLATES)]
    groups = group_by_length(protos)
    bundles = [write_probe(ws, g, ExecConfig(DT), tag=f"battery_{int(g[0].total_ms)}") for g in groups]
    with ThreadPoolExecutor(max_workers=len(bundles)) as pool:
        results: list[SimResult] = list(pool.map(lambda b: sim.run_lems(b.lems_file, [b.output], timeout_s=900),
                                                 bundles))
    return {"ws": ws, "sim": sim, "protos": {p.protocol_id: p for p in protos}, "groups": groups,
            "bundles": bundles, "results": results}


def _trace(battery, pid):
    for g, r in zip(battery["groups"], battery["results"]):
        if pid in [p.protocol_id for p in g]:
            return r.traces[pid]
    raise KeyError(pid)


def _first_divergence_ms(a, b) -> float | None:
    diff = np.flatnonzero(a.v_mV != b.v_mV)
    return None if diff.size == 0 else float(a.t_ms[diff[0]])


# ------------------------------------------------------------------------------------ run level
def test_every_implemented_protocol_is_in_the_battery(battery):
    expected = {t.protocol_id for t in DEFAULT_TEMPLATES if t.implemented and t.kind != "rheobase"}
    assert set(battery["protos"]) == expected and len(expected) == 9
    assert [g[0].total_ms for g in battery["groups"]] == [500.0, 1000.0, 1100.0, 1500.0, 2500.0]


def test_every_group_runs_ok_and_returns_every_trace(battery):
    for g, b, r in zip(battery["groups"], battery["bundles"], battery["results"]):
        assert r.status is RunStatus.OK, (b.protocol_ids, r.message, r.output_tail[-500:])
        assert set(r.traces) == {p.protocol_id for p in g}
        assert b.cell_steps == round(g[0].total_ms / DT) * len(g)


def test_traces_span_the_protocol_on_the_requested_grid(battery):
    for pid, p in battery["protos"].items():
        tr = _trace(battery, pid)
        assert len(tr.t_ms) == round(p.total_ms / DT) + 1, pid
        assert tr.t_ms[0] == 0.0 and tr.t_ms[-1] == pytest.approx(p.total_ms, abs=1e-6), pid
        assert np.all(np.abs(np.diff(tr.t_ms) - DT) < 1e-6 * DT), pid
        assert np.all(np.isfinite(tr.v_mV)) and np.max(np.abs(tr.v_mV)) < 250.0, pid
        assert tr.v_mV[0] == pytest.approx(-70.0, abs=1e-9), pid


# ---------------------------------------------------------------------------------- stimulus timing
def test_zero_current_baseline_never_diverges_from_itself_across_groups(battery):
    """P01 runs in the 1000 ms group; the pre-onset part of every other group must match it exactly."""
    base = _trace(battery, "P01_baseline")
    for pid in battery["protos"]:
        tr = _trace(battery, pid)
        n = int(round(SETTLE / DT)) - 1
        assert np.array_equal(tr.v_mV[:n], base.v_mV[:n]), pid


@pytest.mark.parametrize("pid", ["P02_weak_step", "P04_step_2x", "P05_long_step", "P07_hyperpolarizing_step",
                                 "P08_rebound", "P09_short_pulse", "P10_paired_pulses"])
def test_pulse_onset_is_exactly_at_settle(battery, pid):
    base, tr = _trace(battery, "P01_baseline"), _trace(battery, pid)
    n = min(len(base.t_ms), len(tr.t_ms))
    onset = battery["protos"][pid].components[0].delay_ms
    assert onset == SETTLE
    t_div = _first_divergence_ms(type(tr)(tr.t_ms[:n], tr.v_mV[:n]), type(base)(base.t_ms[:n], base.v_mV[:n]))
    assert t_div is not None, pid
    assert onset < t_div <= onset + 2 * DT + 1e-9, (pid, t_div)


def test_ramp_onset_is_not_before_settle(battery):
    # A ramp starts from 0 nA, so its first visible effect lags the onset by a fraction of a millisecond
    # (the voltage change grows quadratically and must exceed the 7-significant-digit output resolution).
    base, tr = _trace(battery, "P01_baseline"), _trace(battery, "P06_ramp")
    n = len(base.t_ms)
    t_div = _first_divergence_ms(type(tr)(tr.t_ms[:n], tr.v_mV[:n]), base)
    assert t_div is not None and SETTLE < t_div <= SETTLE + 1.0, t_div


def test_deflection_direction_follows_stimulus_sign(battery):
    base = _trace(battery, "P01_baseline")
    k = int(round((SETTLE + 1.0) / DT))                     # 1 ms after onset
    for pid, sign in [("P02_weak_step", 1), ("P04_step_2x", 1), ("P09_short_pulse", 1),
                      ("P07_hyperpolarizing_step", -1), ("P08_rebound", -1)]:
        dv = _trace(battery, pid).v_mV[k] - base.v_mV[k]
        assert np.sign(dv) == sign and abs(dv) > 0.01, (pid, dv)
    k20 = int(round((SETTLE + 50.0) / DT))
    assert _trace(battery, "P06_ramp").v_mV[k20] - base.v_mV[k20] > 0.05


def test_second_paired_pulse_starts_where_protocol_says(battery):
    """P09 and P10 share the first pulse; they must stay identical until the second pulse of P10."""
    p09, p10 = _trace(battery, "P09_short_pulse"), _trace(battery, "P10_paired_pulses")
    second = battery["protos"]["P10_paired_pulses"].components[1].delay_ms
    assert second == SETTLE + 23.0
    t_div = _first_divergence_ms(p10, p09)
    assert t_div is not None and second < t_div <= second + 2 * DT + 1e-9, t_div


def test_steps_with_different_amplitude_diverge_at_onset(battery):
    p04, p05 = _trace(battery, "P04_step_2x"), _trace(battery, "P05_long_step")
    n = len(p04.t_ms)
    t_div = _first_divergence_ms(p04, type(p05)(p05.t_ms[:n], p05.v_mV[:n]))
    assert SETTLE < t_div <= SETTLE + 2 * DT + 1e-9


@pytest.mark.parametrize("pid", ["P07_hyperpolarizing_step", "P08_rebound"])
def test_hyperpolarizing_release_repolarizes(battery, pid):
    p = battery["protos"][pid]
    c = p.components[0]
    tr = _trace(battery, pid)
    end = c.delay_ms + c.duration_ms
    i_end = int(round(end / DT))
    assert tr.v_mV[i_end] < tr.v_mV[0] - 1.0                                   # hyperpolarised during the step
    assert tr.v_mV[i_end + int(round(20.0 / DT))] > tr.v_mV[i_end] + 1.0        # current removed at step end
    if pid == "P08_rebound":
        assert p.window.start_ms == end and p.window.end_ms == p.total_ms


def test_short_pulse_response_peaks_inside_window_then_decays(battery):
    """Only timing is asserted. Whether P09 fires depends on the true rheobase (this test scales by an assumed
    0.1 nA, at which 1 nA x 3 ms only depolarises RS by ~9 mV); see docs/build_notes/core.md#p09-charge."""
    p = battery["protos"]["P09_short_pulse"]
    tr = _trace(battery, "P09_short_pulse")
    c = p.components[0]
    i_peak = int(np.argmax(tr.v_mV))
    assert c.delay_ms < tr.t_ms[i_peak] <= p.window.end_ms                     # peak response after onset, in window
    assert tr.v_mV[i_peak] > tr.v_mV[int(round(SETTLE / DT)) - 1] + 5.0
    assert tr.v_mV[tr.t_ms < SETTLE].max() < -60.0                             # nothing happens before onset
    assert tr.v_mV[-1] < tr.v_mV[i_peak] - 5.0                                 # current off: response decays


# ------------------------------------------------------------------------------- generated network
def test_generated_pulse_only_network_passes_jnml_validation(battery):
    sim = battery["sim"]
    pulses_only = [b for b, g in zip(battery["bundles"], battery["groups"]) if all(p.kind != "ramp" for p in g)]
    assert pulses_only
    for b in pulses_only:
        r = sim.validate([b.net_file])
        assert r.valid is True, (b.net_file.name, r.messages)


def test_generated_ramp_network_passes_jnml_validation(battery):
    sim = battery["sim"]
    (b,) = [b for b, g in zip(battery["bundles"], battery["groups"]) if any(p.kind == "ramp" for p in g)]
    r = sim.validate([b.net_file])
    assert r.valid is True, r.messages


def test_one_file_full_battery_network_passes_jnml_validation(battery, tmp_path):
    ws = battery["ws"]
    b = write_probe(ws, list(battery["protos"].values()), ExecConfig(DT), tag="all_in_one")
    r = battery["sim"].validate([b.net_file])
    assert r.valid is True, r.messages[:2]


# ------------------------------------------------------------------------------ jLEMS integrator Meta
def test_meta_integrator_method_does_not_change_trace(battery, tmp_path):
    """Empirical jLEMS fact (jNeuroML 0.14.0 / jLEMS 0.12.0): a <Meta for="jlems" method=...> child of
    Simulation leaves core-type NeuroML traces byte-identical, whatever the method string."""
    ws, sim = battery["ws"], battery["sim"]
    protos = [battery["protos"]["P02_weak_step"], battery["protos"]["P04_step_2x"]]
    runs = {}
    for method in (None, "rk4", "eulertree", "not_a_method"):
        b = write_probe(ws, protos, ExecConfig(DT, integrator_method=method), tag=f"meta_{method}")
        assert ('<Meta for="jlems"' in b.lems_file.read_text()) == (method is not None)
        r = sim.run_lems(b.lems_file, [b.output], timeout_s=600)
        assert r.status is RunStatus.OK, (method, r.message)
        runs[method] = ((b.lems_file.parent / b.output.file).read_bytes(), r.traces)
    ref_bytes, ref = runs[None]
    for method in ("rk4", "eulertree", "not_a_method"):
        data, traces = runs[method]
        assert data == ref_bytes, method
        for pid in ref:
            assert np.array_equal(traces[pid].v_mV, ref[pid].v_mV), (method, pid)
    # the battery's own P04 trace (run in a 9-cell group) is identical to this 2-cell run: populations are uncoupled
    assert np.array_equal(ref["P04_step_2x"].v_mV, _trace(battery, "P04_step_2x").v_mV)


# ------------------------------------------------------------------------------ rheobase step counter
def test_make_step_counter_real_simulation(battery):
    ws, sim = battery["ws"], battery["sim"]
    cost: list[dict] = []
    counter = make_step_counter(sim, ws, ExecConfig(DT), settle_ms=50.0, step_ms=100.0,
                                threshold_mV=float(config.study()["rheobase"]["spike_threshold_mV"]),
                                timeout_s=600, tag="rheo_it", cost_log=cost)
    counts = counter([0.0, 2.0])
    assert counts is not None and len(counts) == 2
    assert counts[0] == 0 and counts[1] >= 1
    assert cost == [{"tag": "rheo_it_1", "cell_steps": 6000 * 2, "runtime_s": cost[0]["runtime_s"], "status": "ok"}]
    counts2 = counter([2.0])
    assert counts2 == [counts[1]]                           # same amplitude, same answer, in a different batch
    assert cost[1]["tag"] == "rheo_it_2"
