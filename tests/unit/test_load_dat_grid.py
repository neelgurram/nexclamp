"""jLEMS time-label regularisation (printed time has ~8 significant digits of an accumulated clock)."""

from __future__ import annotations

import numpy as np
import pytest

from nexclamp.simulators.jneuroml import load_dat, regularize_time


def test_label_jitter_is_replaced_by_exact_grid(tmp_path):
    n, dt_s = 20001, 1e-6
    t = np.round(np.arange(n) * dt_s + 0.51, 8)          # emulate 8-significant-digit printing
    t = np.array([float(f"{x:.8g}") for x in t])
    v = -0.07 + 0.001 * np.sin(np.arange(n) / 50.0)
    p = tmp_path / "x.dat"
    np.savetxt(p, np.column_stack([t, v]), delimiter="\t", fmt="%.8g")
    (tr,) = load_dat(p, {"v": 1}).values()
    d = np.diff(tr.t_ms)
    assert np.max(np.abs(d - d.mean())) / d.mean() < 1e-6
    assert tr.t_ms[0] == pytest.approx(510.0) and tr.v_mV[0] == pytest.approx(-70.0)


def test_genuinely_non_uniform_time_is_rejected():
    t = np.cumsum(np.r_[0.0, np.full(99, 0.01), np.full(100, 0.02)])
    with pytest.raises(ValueError):
        regularize_time(t, "bad")
    with pytest.raises(ValueError):
        regularize_time(np.array([0.0, 0.0, 0.0]), "flat")
