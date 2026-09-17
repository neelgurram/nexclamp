"""Unit tests for features.trace_metrics: grids, alignment, distances, spike times, npz storage."""

from __future__ import annotations

import io
import zipfile

import numpy as np
import pytest

from neuraxis.features.trace_metrics import (
    align,
    decimate,
    grid_params,
    is_uniform,
    max_abs_diff,
    pack_traces,
    resample,
    rmse,
    spike_times,
    stored_representation,
    uniform_grid,
    unpack_traces,
)
from neuraxis.protocols.rheobase import count_upward_crossings
from neuraxis.schemas import AnalysisWindow, Trace


def sine_trace(dt: float, total: float = 100.0, freq_hz: float = 20.0, amp: float = 50.0, offset: float = -20.0,
               t0: float = 0.0) -> Trace:
    """Sine wave whose upward zero-offset crossings are at known times k / f."""
    t = uniform_grid(t0, dt, int(round(total / dt)) + 1)
    return Trace(t, offset + amp * np.sin(2 * np.pi * freq_hz * t / 1000.0))


# ---------------------------------------------------------------- grids
def test_uniform_grid_values_and_validation():
    g = uniform_grid(10.0, 0.25, 5)
    assert g.dtype == np.float64
    np.testing.assert_array_equal(g, [10.0, 10.25, 10.5, 10.75, 11.0])
    assert uniform_grid(0.0, 0.1, 0).size == 0
    for bad in [(0.0, 0.0, 3), (0.0, -1.0, 3), (float("nan"), 0.1, 3), (0.0, 0.1, -1), (0.0, 0.1, 2.5), (0.0, 0.1, True)]:
        with pytest.raises(ValueError):
            uniform_grid(*bad)


def test_is_uniform_detects_jitter_order_and_degenerate_input():
    t = uniform_grid(0.0, 0.025, 20001)
    assert is_uniform(t)
    jittered = t.copy()
    jittered[5000] += 0.025 * 1e-3            # 1e-3 relative jitter on one sample
    assert not is_uniform(jittered)
    tiny = t.copy()
    tiny[5000] += 0.025 * 1e-9
    assert is_uniform(tiny)
    assert not is_uniform(t[::-1])
    assert not is_uniform(np.array([1.0]))
    assert not is_uniform(np.array([0.0, 1.0, np.nan]))
    assert not is_uniform(np.zeros((2, 2)))


def test_is_uniform_bounds_accumulated_position_drift():
    """Step errors that all lean one way add up: every step passes, yet samples drift far off the grid."""
    n, dt, eps = 480001, 0.005, 0.9e-6
    half = (n - 1) // 2
    steps = np.concatenate([np.full(half, dt * (1 + eps)), np.full(n - 1 - half, dt * (1 - eps))])
    t = np.concatenate([[0.0], np.cumsum(steps)])
    ideal = uniform_grid(t[0], (t[-1] - t[0]) / (n - 1), n)
    assert np.max(np.abs(np.diff(t) - dt)) / dt < 1e-6                  # each step is within tolerance
    assert np.max(np.abs(t - ideal)) > 0.2 * dt                          # but samples drift ~22% of a step
    assert not is_uniform(t)
    with pytest.raises(ValueError, match="position deviation"):
        grid_params(t)


def test_grid_params_round_trip_and_refusal():
    t = uniform_grid(300.0, 0.005, 1001)
    t0, dt, n = grid_params(t)
    assert (t0, n) == (300.0, 1001)
    assert dt == pytest.approx(0.005, rel=1e-12)
    np.testing.assert_allclose(uniform_grid(t0, dt, n), t, rtol=0, atol=1e-12)
    with pytest.raises(ValueError, match="not uniform"):
        grid_params(np.array([0.0, 0.1, 0.3]))


# ---------------------------------------------------------- resampling
def test_resample_is_exact_for_linear_signals_and_refuses_extrapolation():
    t = uniform_grid(0.0, 0.1, 101)
    tr = Trace(t, 3.0 * t - 70.0)
    g = np.array([0.0, 0.05, 3.333, 9.99, 10.0])
    np.testing.assert_allclose(resample(tr, g), 3.0 * g - 70.0, rtol=0, atol=1e-10)
    with pytest.raises(ValueError, match="extrapolation"):
        resample(tr, np.array([10.5]))
    with pytest.raises(ValueError, match="extrapolation"):
        resample(tr, np.array([-0.1]))
    with pytest.raises(ValueError):
        resample(Trace(np.array([0.0, 0.0]), np.array([1.0, 2.0])), np.array([0.0]))


def test_align_puts_different_steps_on_one_grid_within_overlap_and_window():
    a = sine_trace(0.01, total=100.0)
    b = sine_trace(0.025, total=80.0, t0=5.0)           # starts later, ends earlier (85 ms)
    grid, va, vb = align(a, b, 0.05)
    assert grid[0] == 5.0 and grid[-1] == pytest.approx(85.0)
    assert np.allclose(np.diff(grid), 0.05)
    exact = -20.0 + 50.0 * np.sin(2 * np.pi * 20.0 * grid / 1000.0)
    # linear interpolation error bound: amp * (2 pi f)^2 * dt^2 / 8
    assert np.max(np.abs(va - exact)) < 50.0 * (2 * np.pi * 0.02) ** 2 * 0.01 ** 2 / 8 * 1.01
    assert np.max(np.abs(vb - exact)) < 50.0 * (2 * np.pi * 0.02) ** 2 * 0.025 ** 2 / 8 * 1.01
    grid_w, _, _ = align(a, b, 0.05, AnalysisWindow(20.0, 30.0))
    assert grid_w[0] == 20.0 and grid_w[-1] == pytest.approx(30.0) and grid_w.size == 201
    with pytest.raises(ValueError, match="overlap"):
        align(a, b, 0.05, AnalysisWindow(90.0, 95.0))
    with pytest.raises(ValueError):
        align(a, b, 0.0)


def test_rmse_and_max_abs_diff():
    a = sine_trace(0.01)
    shifted = Trace(a.t_ms, a.v_mV + 2.0)
    assert rmse(a, a, 0.05) == 0.0
    assert max_abs_diff(a, a, 0.05) == 0.0
    assert rmse(a, shifted, 0.05) == pytest.approx(2.0, abs=1e-9)
    assert max_abs_diff(a, shifted, 0.05) == pytest.approx(2.0, abs=1e-9)
    bump = a.v_mV.copy()
    bump[(a.t_ms >= 40.0) & (a.t_ms <= 41.0)] += 10.0
    bumped = Trace(a.t_ms, bump)
    assert max_abs_diff(a, bumped, 0.01) == pytest.approx(10.0)
    assert max_abs_diff(a, bumped, 0.01, AnalysisWindow(0.0, 30.0)) == 0.0
    # 101 of 10001 grid points differ by 10 mV
    assert rmse(a, bumped, 0.01) == pytest.approx(np.sqrt(101 * 100.0 / 10001), rel=1e-9)


# ---------------------------------------------------------- spike times
def test_spike_times_are_interpolated_upward_crossings():
    tr = sine_trace(0.01, total=190.0, freq_hz=20.0)   # upward crossings of -20 mV at 0, 50, 100, 150 ms
    times = spike_times(tr, -20.0)
    # t = 0 starts exactly at threshold (not below it), so it is not a crossing.
    np.testing.assert_allclose(times, [50.0, 100.0, 150.0], atol=1e-6)
    assert times.size == count_upward_crossings(tr.v_mV, -20.0)
    # an off-centre threshold: sin(2 pi f t) = 0.5 -> t = 1/12 period after each zero crossing
    np.testing.assert_allclose(spike_times(tr, 5.0), 50.0 * np.arange(4) + 50.0 / 12, atol=1e-4)


def test_spike_times_edge_cases():
    t = uniform_grid(0.0, 1.0, 5)
    assert spike_times(Trace(t, np.array([10.0, -50.0, 10.0, 10.0, -50.0])), 0.0).tolist() == [1.0 + 50.0 / 60.0]
    assert spike_times(Trace(t, np.full(5, 10.0)), 0.0).size == 0          # starts above: no crossing
    assert spike_times(Trace(t, np.array([-1.0, np.nan, 1.0, -1.0, 1.0])), 0.0).tolist() == [3.5]
    assert spike_times(Trace(t[:1], np.array([0.0])), 0.0).size == 0
    assert spike_times(Trace(t, np.array([-1.0, 0.0, -1.0, 0.0, 0.0])), 0.0).tolist() == [1.0, 3.0]


# ------------------------------------------------------------ decimate
def test_decimate_requires_whole_multiples():
    tr = sine_trace(0.025, total=10.0)
    d = decimate(tr, 0.1)
    np.testing.assert_array_equal(d.t_ms, tr.t_ms[::4])
    np.testing.assert_array_equal(d.v_mV, tr.v_mV[::4])
    assert decimate(tr, 0.025).t_ms.size == tr.t_ms.size
    with pytest.raises(ValueError, match="multiple"):
        decimate(tr, 0.06)
    with pytest.raises(ValueError):
        decimate(tr, 0.01)
    with pytest.raises(ValueError):
        decimate(tr, -0.1)


# --------------------------------------------------------- pack/unpack
def test_pack_unpack_round_trip_matches_the_npz_format():
    traces = {"P04_step_2x": sine_trace(0.005, total=50.0), "P01_baseline": sine_trace(0.025, total=30.0, t0=2.0)}
    data = pack_traces(traces)
    with np.load(io.BytesIO(data), allow_pickle=False) as npz:
        assert sorted(npz.files) == ["P01_baseline__t", "P01_baseline__v", "P04_step_2x__t", "P04_step_2x__v"]
        assert npz["P04_step_2x__v"].dtype == np.float32
        assert npz["P04_step_2x__t"].dtype == np.float64
        t0, dt, n = npz["P01_baseline__t"]
        assert t0 == 2.0 and dt == pytest.approx(0.025) and n == 1201
    back = unpack_traces(data)
    assert set(back) == set(traces)
    for name, tr in traces.items():
        np.testing.assert_array_equal(back[name].v_mV, tr.v_mV.astype(np.float32))
        np.testing.assert_allclose(back[name].t_ms, tr.t_ms, rtol=0, atol=1e-10)
        assert back[name].v_mV.dtype == np.float64
    # stored_representation is exactly the unpacked trace
    for name, tr in traces.items():
        s = stored_representation(tr)
        np.testing.assert_array_equal(s.t_ms, back[name].t_ms)
        np.testing.assert_array_equal(s.v_mV, back[name].v_mV)
    # float32 is a fixed point: re-packing the unpacked voltages stores the same samples
    again = unpack_traces(pack_traces(back))
    for name in traces:
        np.testing.assert_array_equal(again[name].v_mV, back[name].v_mV)


def test_pack_is_byte_deterministic_and_compress_option_round_trips():
    traces = {"a": sine_trace(0.025, total=20.0), "b": sine_trace(0.05, total=20.0)}
    data = pack_traces(traces)
    assert data == pack_traces(dict(reversed(list(traces.items()))))
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for info in zf.infolist():
            assert info.date_time == (1980, 1, 1, 0, 0, 0)
            assert info.create_system == 3
            assert info.compress_type == zipfile.ZIP_STORED
    flat = {"flat": Trace(uniform_grid(0.0, 0.025, 40001), np.full(40001, -65.0))}
    packed = pack_traces(flat, compress=True)
    assert len(packed) < len(pack_traces(flat)) / 10
    np.testing.assert_array_equal(unpack_traces(packed)["flat"].v_mV, flat["flat"].v_mV)


def test_pack_refuses_non_uniform_grids_and_bad_input():
    t = uniform_grid(0.0, 0.1, 100)
    t[50] += 0.01
    with pytest.raises(ValueError, match="uniform"):
        pack_traces({"x": Trace(t, np.zeros(100))})
    with pytest.raises(ValueError):
        pack_traces({"x": Trace(np.array([0.0]), np.array([0.0]))})
    with pytest.raises(ValueError):
        pack_traces({})
    with pytest.raises(ValueError, match="name"):
        pack_traces({"a/b": sine_trace(0.1, total=5.0)})


def test_unpack_rejects_malformed_archives():
    buf = io.BytesIO()
    np.savez(buf, x__v=np.zeros(3, dtype=np.float32))                      # missing time entry
    with pytest.raises(ValueError, match="time"):
        unpack_traces(buf.getvalue())
    buf = io.BytesIO()
    np.savez(buf, x__v=np.zeros(3, dtype=np.float64), x__t=np.array([0.0, 0.1, 3.0]))   # wrong voltage dtype
    with pytest.raises(ValueError, match="float32"):
        unpack_traces(buf.getvalue())
    buf = io.BytesIO()
    np.savez(buf, x__v=np.zeros(3, dtype=np.float32), x__t=np.array([0.0, 0.1, 4.0]))   # count mismatch
    with pytest.raises(ValueError, match="count"):
        unpack_traces(buf.getvalue())
    buf = io.BytesIO()
    np.savez(buf, other=np.zeros(3))
    with pytest.raises(ValueError, match="unexpected"):
        unpack_traces(buf.getvalue())
    for count in (np.inf, np.nan, -3.0, 2.5):                                  # corrupt sample counts
        buf = io.BytesIO()
        np.savez(buf, x__v=np.zeros(3, dtype=np.float32), x__t=np.array([0.0, 0.1, count]))
        with pytest.raises(ValueError, match="count"):
            unpack_traces(buf.getvalue())


def test_non_finite_and_out_of_range_voltages_are_stored_explicitly():
    """UNSTABLE runs are stored too: NaN/inf are kept, float32 overflow becomes a signed inf, never silently."""
    t = uniform_grid(0.0, 0.1, 6)
    v = np.array([-65.0, np.nan, np.inf, -np.inf, 1e39, -1e39])
    with np.errstate(all="raise"):                     # the float32 cast no longer emits a stray numpy warning
        back = unpack_traces(pack_traces({"u": Trace(t, v)}))["u"]
    assert back.v_mV[0] == -65.0 and np.isnan(back.v_mV[1])
    np.testing.assert_array_equal(back.v_mV[2:], [np.inf, -np.inf, np.inf, -np.inf])
    np.testing.assert_array_equal(stored_representation(Trace(t, v)).v_mV, back.v_mV)
    t3 = uniform_grid(0.0, 0.1, 3)
    for bad, match in (([-65.0, np.nan, -60.0], "non-finite"), ([-65.0, -np.inf, -60.0], "non-finite"),
                       ([-65.0, 1e39, -60.0], "float32 range")):
        with pytest.raises(ValueError, match=match):
            pack_traces({"u": Trace(t3, np.array(bad))}, finite_only=True)
        with pytest.raises(ValueError, match=match):
            stored_representation(Trace(t3, np.array(bad)), finite_only=True)
    ok = Trace(t3, np.array([-65.0, 3.0e38, -60.0]))                            # large but inside float32 range
    np.testing.assert_array_equal(unpack_traces(pack_traces({"u": ok}, finite_only=True))["u"].v_mV,
                                  ok.v_mV.astype(np.float32))
