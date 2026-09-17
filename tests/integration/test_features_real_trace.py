"""Integration: features from a real jLEMS run of the Pospischil 2008 RS cell.

One short batched probe (a depolarising and a hyperpolarising step, 450 ms at dt 0.025 ms)
is simulated once per module. The checks are deliberately broad plausibility ranges for a
cortical regular-spiking cell, not reference values. They also cover the reproducibility
rule: the reported features are exactly what the stored float32 trace yields.
"""

from __future__ import annotations

import json
import math

import efel
import numpy as np
import pytest

from neuraxis.config import features as load_features_config
from neuraxis.features.efel_adapter import (
    DEFINED,
    extract_all,
    feature_table_from_json,
    feature_table_to_json,
)
from neuraxis.features.regimes import LABELS
from neuraxis.features.trace_metrics import is_uniform, pack_traces, stored_representation, unpack_traces
from neuraxis.models import materialize
from neuraxis.protocols.definitions import SPIKING
from neuraxis.protocols.generate import write_probe
from neuraxis.schemas import AnalysisWindow, ConcreteProtocol, ExecConfig, RunStatus, StimulusComponent

pytestmark = pytest.mark.jnml

DT = 0.025
SETTLE, STEP, POST = 100.0, 300.0, 50.0


def _step(pid: str, amplitude_nA: float, features: tuple[str, ...]) -> ConcreteProtocol:
    return ConcreteProtocol(pid, "step", (StimulusComponent("pulse", SETTLE, STEP, amplitude_nA),),
                            SETTLE + STEP + POST, AnalysisWindow(SETTLE, SETTLE + STEP), features)


PROTOCOLS = [
    _step("S_depol", 0.75, SPIKING + ("baseline_voltage", "steady_state_voltage", "maximum_voltage")),
    _step("S_hyper", -0.25, ("baseline_voltage", "steady_state_voltage", "voltage_deflection", "sag_ratio",
                             "minimum_voltage", "spike_count")),
]


@pytest.fixture(scope="module")
def cfg() -> dict:
    return load_features_config().data


@pytest.fixture(scope="module")
def rs_result(sim, models, tmp_path_factory):
    ws = materialize(models["pospischil2008_rs"], tmp_path_factory.mktemp("features_rs") / "rs")
    bundle = write_probe(ws, PROTOCOLS, ExecConfig(dt_ms=DT), tag="features_it")
    res = sim.run_lems(bundle.lems_file, [bundle.output], timeout_s=600)
    assert res.status is RunStatus.OK, res.message
    return res


def test_real_trace_is_uniform_and_storable(rs_result):
    data = pack_traces(rs_result.traces)
    back = unpack_traces(data)
    for p in PROTOCOLS:
        raw = rs_result.traces[p.protocol_id]
        assert is_uniform(raw.t_ms)
        assert raw.t_ms[-1] == pytest.approx(p.total_ms)
        np.testing.assert_array_equal(back[p.protocol_id].v_mV, raw.v_mV.astype(np.float32))
        np.testing.assert_allclose(back[p.protocol_id].t_ms, raw.t_ms, rtol=0, atol=1e-9)


def test_rs_features_are_physiologically_plausible(rs_result, cfg):
    log: list[str] = []
    tables = extract_all(unpack_traces(pack_traces(rs_result.traces)), PROTOCOLS, cfg, warnings=log)
    d, h = tables["S_depol"], tables["S_hyper"]
    for name in ("spike_count", "mean_frequency", "first_spike_latency", "ap_amplitude", "ap_half_width", "ahp_depth",
                 "first_isi", "last_isi", "baseline_voltage", "steady_state_voltage", "maximum_voltage"):
        assert d[name].state == DEFINED, (name, d[name], log)
    assert d["spike_count"].value >= 2
    assert -90.0 < d["baseline_voltage"].value < -50.0
    assert 50.0 < d["ap_amplitude"].value < 130.0                      # mV, onset to peak
    assert 0.2 < d["ap_half_width"].value < 3.0                       # ms
    assert 0.0 < d["maximum_voltage"].value < 60.0
    assert 0.0 < d["first_spike_latency"].value < STEP
    assert 1.0 < d["mean_frequency"].value < 300.0
    assert d["first_isi"].value <= d["last_isi"].value                # a regular-spiking cell does not accelerate
    assert d["firing_regime"].value in LABELS and d["firing_regime"].value not in ("silent", "single_spike")

    assert h["spike_count"].value == 0.0
    assert h["baseline_voltage"].value == pytest.approx(d["baseline_voltage"].value, abs=1e-9)   # identical pre-step
    assert h["voltage_deflection"].value < -1.0
    assert h["minimum_voltage"].value < h["baseline_voltage"].value
    assert h["sag_ratio"].state == DEFINED and 0.0 <= h["sag_ratio"].value < 0.5


def test_features_reproduce_from_the_packed_float32_trace(rs_result, cfg):
    data = pack_traces(rs_result.traces)
    reported = extract_all(unpack_traces(data), PROTOCOLS, cfg, warnings=[])
    stored_json = json.dumps({pid: feature_table_to_json(ft) for pid, ft in reported.items()}, sort_keys=True)

    # 1) re-reading the same bytes, with eFEL's global settings disturbed in between, gives identical numbers
    try:
        efel.set_setting("Threshold", 0.0)
        efel.set_setting("interp_step", 0.1)
        again = extract_all(unpack_traces(data), PROTOCOLS, cfg, warnings=[])
    finally:
        efel.reset()
    assert again == reported
    # 2) the JSON feature record round-trips exactly
    reloaded = {pid: feature_table_from_json(ft) for pid, ft in json.loads(stored_json).items()}
    assert reloaded == reported
    # 3) extracting before storage via stored_representation gives the same numbers as extracting after storage
    pre = extract_all({k: stored_representation(v) for k, v in rs_result.traces.items()}, PROTOCOLS, cfg, warnings=[])
    assert pre == reported

    # 4) the float64 trace read from jLEMS text output gives materially the same features;
    #    float32 storage must not move features by more than a small fraction of any tolerance floor.
    raw = extract_all(rs_result.traces, PROTOCOLS, cfg, warnings=[])
    interp_step = cfg["settings"]["interp_step"]
    for pid, ft in reported.items():
        for name, fv in ft.items():
            other = raw[pid][name]
            assert other.state == fv.state, (pid, name)
            if fv.value is None or isinstance(fv.value, str) or fv.unit == "1" and name in ("spike_count", "burst_count"):
                assert other.value == fv.value, (pid, name)
            elif fv.unit == "mV":
                assert math.isclose(other.value, fv.value, abs_tol=0.2), (pid, name, other.value, fv.value)
            elif fv.unit == "ms":
                assert math.isclose(other.value, fv.value, abs_tol=5 * interp_step), (pid, name)
            else:
                assert math.isclose(other.value, fv.value, rel_tol=1e-2, abs_tol=1e-3), (pid, name)
