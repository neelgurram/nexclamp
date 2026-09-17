"""Trace-level utilities: uniform grids, alignment, trace distances, spike times and storage.

Traces are stored as float32 millivolts on a uniform time grid (ARCHITECTURE section 2).
The grid is stored as the triple ``[t0_ms, dt_ms, n]`` rather than as an explicit time
vector. That is only faithful if the grid really is uniform, so storage refuses anything
else. Features are extracted from the stored representation, so every derived number can
be reproduced exactly from the raw ``traces.npz`` bytes.
"""

from __future__ import annotations

import io
import math
import zipfile
from collections.abc import Mapping

import numpy as np

from neuraxis.schemas import AnalysisWindow, Trace

UNIFORM_REL_TOL = 1e-6          # max |step - mean step| / mean step for a grid to count as uniform
V_SUFFIX = "__v"                 # float32 mV samples
T_SUFFIX = "__t"                 # float64 [t0_ms, dt_ms, n]
_ZIP_DATE = (1980, 1, 1, 0, 0, 0)   # fixed entry timestamp: identical traces give identical bytes
_ZIP_UNIX = 3                        # fixed "created by" system so bytes do not depend on the OS


def uniform_grid(t0_ms: float, dt_ms: float, n: int) -> np.ndarray:
    """``t0 + k * dt`` for ``k = 0 .. n-1`` as float64.

    The multiplicative form (not a cumulative sum) makes the grid a pure function of the
    stored triple, with no accumulated round-off.
    """
    if not (math.isfinite(t0_ms) and math.isfinite(dt_ms)) or dt_ms <= 0:
        raise ValueError(f"invalid grid: t0={t0_ms!r} ms, dt={dt_ms!r} ms")
    if isinstance(n, bool) or int(n) != n or n < 0:
        raise ValueError(f"invalid sample count {n!r}")
    return float(t0_ms) + float(dt_ms) * np.arange(int(n), dtype=np.float64)


def _as_1d(x: np.ndarray, what: str) -> np.ndarray:
    a = np.asarray(x, dtype=np.float64)
    if a.ndim != 1:
        raise ValueError(f"{what} must be one-dimensional")
    return a


def _grid_deviation(t: np.ndarray) -> tuple[float, float]:
    """``(step, position)`` deviation from the mean-step grid, both as fractions of that step.

    ``step`` is the largest ``|t[k+1] - t[k] - dt|``. ``position`` is the largest
    ``|t[k] - (t0 + k * dt)|``, the distance a sample moves when the grid is stored as
    ``[t0, dt, n]``. Small step errors that all lean the same way add up along the trace,
    so a bounded step error alone does not bound the position error.
    """
    dt = (t[-1] - t[0]) / (t.size - 1)
    if not dt > 0:
        return math.inf, math.inf
    step = float(np.max(np.abs(np.diff(t) - dt)) / dt)
    position = float(np.max(np.abs(t - uniform_grid(float(t[0]), float(dt), t.size))) / dt)
    return step, position


def is_uniform(t_ms: np.ndarray, rel_tol: float = UNIFORM_REL_TOL) -> bool:
    """True if every step, and every sample position, lies within ``rel_tol`` steps of the mean-step grid.

    A grid needs at least two finite samples to have a step at all.
    """
    t = np.asarray(t_ms, dtype=np.float64)
    if t.ndim != 1 or t.size < 2 or not np.all(np.isfinite(t)):
        return False
    return max(_grid_deviation(t)) <= rel_tol


def grid_params(t_ms: np.ndarray, rel_tol: float = UNIFORM_REL_TOL) -> tuple[float, float, int]:
    """``(t0_ms, dt_ms, n)`` of a uniform time vector; ``ValueError`` if it is not uniform.

    ``dt`` is the mean step ``(t[-1] - t[0]) / (n - 1)``, so the reconstructed grid hits
    both end points of the original, and no sample moves by more than ``rel_tol`` steps.
    """
    t = np.asarray(t_ms, dtype=np.float64)
    if not is_uniform(t, rel_tol):
        detail = ""
        if t.ndim == 1 and t.size >= 2 and np.all(np.isfinite(t)):
            step, position = _grid_deviation(t)
            detail = f" (step deviation {step:.3g}, position deviation {position:.3g} steps; limit {rel_tol:g})"
        raise ValueError(f"time grid is not uniform{detail}")
    return float(t[0]), float((t[-1] - t[0]) / (t.size - 1)), int(t.size)


def _interp(t: np.ndarray, v: np.ndarray, grid: np.ndarray, slack_ms: float) -> np.ndarray:
    if t.size < 2 or t.shape != v.shape:
        raise ValueError("need at least two samples, with t and v of equal length, to interpolate")
    if not np.all(np.diff(t) > 0):
        raise ValueError("trace time must be strictly increasing")
    if grid.size == 0:
        return np.empty(0, dtype=np.float64)
    if not np.all(np.isfinite(grid)):
        raise ValueError("grid contains non-finite times")
    if grid[0] < t[0] - slack_ms or grid.max() > t[-1] + slack_ms or grid.min() < t[0] - slack_ms:
        raise ValueError(f"grid [{grid.min()}, {grid.max()}] ms lies outside the trace [{t[0]}, {t[-1]}] ms; "
                         "extrapolation is refused")
    return np.interp(grid, t, v)


def resample(trace: Trace, grid_ms: np.ndarray) -> np.ndarray:
    """Linear interpolation of ``trace`` onto ``grid_ms`` (float64). Refuses to extrapolate."""
    t, v = _as_1d(trace.t_ms, "t_ms"), _as_1d(trace.v_mV, "v_mV")
    g = _as_1d(grid_ms, "grid_ms")
    if t.size < 2:
        raise ValueError("need at least two samples to interpolate")
    slack = UNIFORM_REL_TOL * (t[-1] - t[0]) / (t.size - 1)
    return _interp(t, v, g, slack)


def align(a: Trace, b: Trace, dt_ms: float,
          window: AnalysisWindow | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Put two traces on one common uniform grid (spec, tolerance calibration step 4).

    The grid starts at the later of the two start times (or at the window start) and
    covers only the span both traces, and the window, share. That way traces recorded at
    different steps (h, h/2, h/4) are compared at the same instants, and nothing is
    extrapolated. Returns ``(grid_ms, v_a, v_b)``.
    """
    if not (math.isfinite(dt_ms) and dt_ms > 0):
        raise ValueError(f"invalid alignment step {dt_ms!r} ms")
    ta, va = _as_1d(a.t_ms, "a.t_ms"), _as_1d(a.v_mV, "a.v_mV")
    tb, vb = _as_1d(b.t_ms, "b.t_ms"), _as_1d(b.v_mV, "b.v_mV")
    if ta.size < 2 or tb.size < 2:
        raise ValueError("need at least two samples per trace to align")
    start, end = max(ta[0], tb[0]), min(ta[-1], tb[-1])
    if window is not None:
        start, end = max(start, window.start_ms), min(end, window.end_ms)
    if not end >= start:
        raise ValueError("the traces (and window) do not overlap")
    n = int(math.floor((end - start) / dt_ms + UNIFORM_REL_TOL)) + 1
    grid = uniform_grid(start, dt_ms, n)
    slack = UNIFORM_REL_TOL * dt_ms
    return grid, _interp(ta, va, grid, slack), _interp(tb, vb, grid, slack)


def rmse(a: Trace, b: Trace, dt_ms: float, window: AnalysisWindow | None = None) -> float:
    """Root-mean-square voltage difference (mV) on the common grid of :func:`align`."""
    _, va, vb = align(a, b, dt_ms, window)
    return float(np.sqrt(np.mean((va - vb) ** 2)))


def max_abs_diff(a: Trace, b: Trace, dt_ms: float, window: AnalysisWindow | None = None) -> float:
    """Largest absolute voltage difference (mV) on the common grid of :func:`align`."""
    _, va, vb = align(a, b, dt_ms, window)
    return float(np.max(np.abs(va - vb)))


def spike_times(trace: Trace, threshold_mV: float) -> np.ndarray:
    """Times (ms) of upward threshold crossings, linearly interpolated between samples.

    A crossing is a sample below the threshold followed by one at or above it, which is
    the same rule as ``protocols.rheobase.count_upward_crossings``. A trace that starts
    above threshold therefore has no crossing at its first sample, and NaN samples never
    produce crossings.
    """
    t, v = _as_1d(trace.t_ms, "t_ms"), _as_1d(trace.v_mV, "v_mV")
    if t.size < 2:
        return np.empty(0, dtype=np.float64)
    idx = np.flatnonzero((v[:-1] < threshold_mV) & (v[1:] >= threshold_mV))
    v0, v1 = v[idx], v[idx + 1]
    frac = (threshold_mV - v0) / (v1 - v0)          # v1 >= threshold > v0, so v1 - v0 > 0
    return t[idx] + frac * (t[idx + 1] - t[idx])


def decimate(trace: Trace, every_ms: float) -> Trace:
    """Keep every k-th sample so the output step is ``every_ms`` (recording resolution).

    ``every_ms`` must be a whole multiple of the native step. Rounding silently would
    record at a resolution nobody asked for.
    """
    _, dt, _ = grid_params(trace.t_ms)
    if not (math.isfinite(every_ms) and every_ms > 0):
        raise ValueError(f"invalid sampling interval {every_ms!r} ms")
    ratio = every_ms / dt
    stride = int(round(ratio))
    if stride < 1 or abs(ratio - stride) > UNIFORM_REL_TOL * ratio:
        raise ValueError(f"sampling interval {every_ms} ms is not a whole multiple of the step {dt} ms")
    return Trace(np.asarray(trace.t_ms)[::stride].copy(), np.asarray(trace.v_mV)[::stride].copy())


def _check_name(name: object) -> str:
    if not isinstance(name, str) or not name or "/" in name or "\\" in name:
        raise ValueError(f"invalid trace name {name!r}")
    return name


def _stored_arrays(name: str, trace: Trace, finite_only: bool = False) -> tuple[np.ndarray, np.ndarray]:
    try:
        t0, dt, n = grid_params(trace.t_ms)
    except ValueError as exc:
        raise ValueError(f"trace {name!r}: {exc}; only uniform grids can be stored") from None
    v = np.asarray(trace.v_mV, dtype=np.float64)
    if v.ndim != 1 or v.size != n:
        raise ValueError(f"trace {name!r}: voltage must be one-dimensional with one value per time sample")
    with np.errstate(over="ignore"):              # overflow is detected explicitly below
        v32 = v.astype("<f4")
    finite = np.isfinite(v)
    overflow = int(np.count_nonzero(finite & ~np.isfinite(v32)))
    if finite_only and not np.all(finite):
        raise ValueError(f"trace {name!r}: {v.size - int(np.count_nonzero(finite))} non-finite voltage samples; "
                         "finite_only storage refuses them")
    if finite_only and overflow:
        raise ValueError(f"trace {name!r}: {overflow} voltage samples exceed the float32 range "
                         f"(|v| > {float(np.finfo(np.float32).max):.4g} mV) and cannot be stored faithfully")
    return np.array([t0, dt, float(n)], dtype="<f8"), v32


def pack_traces(traces: Mapping[str, Trace], compress: bool = False, finite_only: bool = False) -> bytes:
    """Serialise traces to ``.npz`` bytes: ``<name>__v`` float32 mV and ``<name>__t`` = [t0, dt, n].

    Entries are written in sorted order with a fixed timestamp and host system, so the
    same traces always give the same bytes and the same SHA-256 in ``run.json``. By
    default entries are stored uncompressed, so the bytes do not depend on the zlib
    version. ``compress=True`` deflates them to save disk space. ``numpy.load`` reads
    both forms.

    Non-finite voltages. ``validation.execution`` also stores the traces of runs the
    simulator adapter classified ``UNSTABLE`` (any non-finite sample, or |V| above the
    250 mV physical bound), so they can be inspected. By default NaN and +/-inf are
    stored as they are, since float32 holds them exactly. A finite sample beyond the
    float32 range (about 3.4e38 mV, only reachable in such a diverged run) is stored as
    an infinity of the same sign. That is the one case where the stored trace differs
    from its input, and it keeps the trace non-finite, which ``extract`` refuses, so it
    can never produce features. ``finite_only=True`` raises ``ValueError`` for any
    non-finite or out-of-range sample instead, for traces that must be stored exactly.
    """
    if not traces:
        raise ValueError("no traces to pack")
    method = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=method, allowZip64=True) as zf:
        for name in sorted(traces, key=_check_name):
            t_arr, v_arr = _stored_arrays(name, traces[name], finite_only)
            for key, arr in ((name + T_SUFFIX, t_arr), (name + V_SUFFIX, v_arr)):
                info = zipfile.ZipInfo(key + ".npy", date_time=_ZIP_DATE)
                info.compress_type = method
                info.create_system = _ZIP_UNIX
                info.external_attr = 0o100644 << 16
                with zf.open(info, "w", force_zip64=True) as fh:
                    np.lib.format.write_array(fh, arr, allow_pickle=False)
    return buf.getvalue()


def unpack_traces(data: bytes) -> dict[str, Trace]:
    """Inverse of :func:`pack_traces`.

    Voltages are returned as float64 arrays holding exactly the stored float32 values
    (every float32 is exactly representable as float64). Times are rebuilt with
    :func:`uniform_grid`.
    """
    out: dict[str, Trace] = {}
    with np.load(io.BytesIO(data), allow_pickle=False) as npz:
        parts: dict[str, set[str]] = {}
        for key in npz.files:
            if key.endswith(V_SUFFIX) or key.endswith(T_SUFFIX):
                parts.setdefault(key[: -len(V_SUFFIX)], set()).add(key[-len(V_SUFFIX):])
            else:
                raise ValueError(f"unexpected array {key!r} in trace archive")
        for name in sorted(parts):
            if parts[name] != {V_SUFFIX, T_SUFFIX}:
                raise ValueError(f"trace {name!r} lacks its {'time' if T_SUFFIX not in parts[name] else 'voltage'} array")
            tt, v = npz[name + T_SUFFIX], npz[name + V_SUFFIX]
            if tt.dtype.kind != "f" or tt.dtype.itemsize != 8 or tt.shape != (3,):
                raise ValueError(f"trace {name!r}: time entry must be float64 [t0_ms, dt_ms, n]")
            if v.dtype.kind != "f" or v.dtype.itemsize != 4 or v.ndim != 1:
                raise ValueError(f"trace {name!r}: voltage entry must be a one-dimensional float32 array")
            t0, dt, n_float = (float(x) for x in tt)
            if not math.isfinite(n_float) or n_float < 0 or n_float != math.floor(n_float) or int(n_float) != v.size:
                raise ValueError(f"trace {name!r}: sample count {n_float} does not match {v.size} voltages")
            out[name] = Trace(uniform_grid(t0, dt, int(n_float)), v.astype(np.float64))
    return out


def stored_representation(trace: Trace, finite_only: bool = False) -> Trace:
    """The trace exactly as ``unpack_traces(pack_traces({name: trace}, finite_only=...))[name]`` returns it.

    Use it to extract features before the trace is written, without changing the numbers.
    """
    t_arr, v_arr = _stored_arrays("trace", trace, finite_only)
    return Trace(uniform_grid(t_arr[0], t_arr[1], int(t_arr[2])), v_arr.astype(np.float64))
