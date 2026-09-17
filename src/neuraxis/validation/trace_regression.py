"""Full-trace regression (validation level C on the canonical stimulus; part of level D elsewhere).

Complements the feature comparison with three checks of the complete recorded voltage trace of
each protocol, each with a threshold calibrated on the unedited reference at h and h/2
(PILOT_PROTOCOL_V2, "Validation levels"):

- ``trace_rmse``: root-mean-square voltage difference over the whole trace, detected when it
  exceeds tau_rmse = max(RMSE_FLOOR_MV, c * RMSE(ref_h, ref_h/2));
- ``spike_count``: any change in the number of spikes (a discrete firing outcome);
- ``spike_timing``: with equal counts, the largest shift of any spike time, detected when it exceeds
  tau_shift = max(SHIFT_FLOOR_MS, c * max |t_ref_h - t_ref_h/2|).

A protocol whose reference spike count differs between h and h/2 is numerically unresolved for
trace regression and is excluded (recorded, never silently dropped). As for features, a detection
counts only if it reproduces at h and at h/2.
"""

from __future__ import annotations

import dataclasses as dc
import json
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import numpy as np

from neuraxis.features import trace_metrics

RMSE_FLOOR_MV = 0.5
SHIFT_FLOOR_MS = 0.5
SPIKE_THRESHOLD_MV = -20.0
METRICS = ("trace_rmse", "spike_count", "spike_timing")


@dc.dataclass
class TraceTolerance:
    model_id: str
    protocol_id: str
    status: str                    # ok | excluded_spike_count_changes_under_refinement | missing
    ref_spike_count: int | None
    ref_rmse_h_h2: float | None
    ref_max_shift_h_h2: float | None
    tau_rmse: float | None
    tau_shift: float | None
    dt_ms: float | None


@dc.dataclass
class TraceDetection:
    variant_id: str
    model_id: str
    level_factor: int
    protocol_id: str
    metric: str
    ref_value: float | None
    var_value: float | None
    diff: float | None
    tau: float | None


def _dt(tr: Any) -> float:
    t = np.asarray(tr.t_ms, dtype=float)
    return float((t[-1] - t[0]) / (t.size - 1)) if t.size > 1 else math.nan


def spikes(tr: Any) -> np.ndarray:
    return trace_metrics.spike_times(tr, SPIKE_THRESHOLD_MV)


def calibrate(ref_h: Mapping[str, Any], ref_h2: Mapping[str, Any], model_id: str, c: float) -> dict[str, TraceTolerance]:
    """Per-protocol tolerances from the reference's traces at h and h/2 (dicts protocol_id -> Trace)."""
    out = {}
    for pid, a in ref_h.items():
        b = ref_h2.get(pid)
        if b is None:
            out[pid] = TraceTolerance(model_id, pid, "missing", None, None, None, None, None, None)
            continue
        dt = _dt(a)
        sa, sb = spikes(a), spikes(b)
        rm = trace_metrics.rmse(a, b, dt)
        if sa.size != sb.size:
            out[pid] = TraceTolerance(model_id, pid, "excluded_spike_count_changes_under_refinement", int(sa.size),
                                      rm, None, None, None, dt)
            continue
        shift = float(np.max(np.abs(sa - sb))) if sa.size else 0.0
        out[pid] = TraceTolerance(model_id, pid, "ok", int(sa.size), rm, shift, max(RMSE_FLOOR_MV, c * rm),
                                  max(SHIFT_FLOOR_MS, c * shift), dt)
    return out


def compare(ref: Mapping[str, Any], var: Mapping[str, Any], tol: Mapping[str, TraceTolerance], variant_id: str,
            model_id: str, level_factor: int) -> list[TraceDetection]:
    """Detections of ``var`` against ``ref`` (same refinement level) for every calibrated protocol."""
    dets = []
    for pid, t in sorted(tol.items()):
        if t.status != "ok" or pid not in ref or pid not in var:
            continue
        a, b = ref[pid], var[pid]
        common = dict(variant_id=variant_id, model_id=model_id, level_factor=level_factor, protocol_id=pid)
        rm = trace_metrics.rmse(a, b, _dt(a))
        if rm > t.tau_rmse:
            dets.append(TraceDetection(**common, metric="trace_rmse", ref_value=0.0, var_value=rm, diff=rm, tau=t.tau_rmse))
        sa, sb = spikes(a), spikes(b)
        if sa.size != sb.size:
            dets.append(TraceDetection(**common, metric="spike_count", ref_value=float(sa.size), var_value=float(sb.size),
                                       diff=float(abs(sa.size - sb.size)), tau=0.5))
        elif sa.size:
            shift = float(np.max(np.abs(sa - sb)))
            if shift > t.tau_shift:
                dets.append(TraceDetection(**common, metric="spike_timing", ref_value=None, var_value=None,
                                           diff=shift, tau=t.tau_shift))
    return dets


def reproducible(det_h: list[TraceDetection], det_h2: list[TraceDetection] | None) -> set[tuple[str, str]]:
    if det_h2 is None:
        return set()
    return {(d.protocol_id, d.metric) for d in det_h} & {(d.protocol_id, d.metric) for d in det_h2}


def save_tolerances(tol: Mapping[str, TraceTolerance], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({k: dc.asdict(v) for k, v in tol.items()}, indent=2) + "\n", encoding="utf-8")


def load_tolerances(path: Path) -> dict[str, TraceTolerance]:
    return {k: TraceTolerance(**v) for k, v in json.loads(Path(path).read_text(encoding="utf-8")).items()}


def load_traces(raw_dir: Path, run_ids: Mapping[str, str]) -> dict[str, Any]:
    """protocol_id -> Trace from stored ``traces.npz`` of the given runs (missing files are skipped)."""
    out, cache = {}, {}
    for pid, rid in run_ids.items():
        npz = Path(raw_dir) / str(rid) / "traces.npz"
        if not npz.is_file():
            continue
        if rid not in cache:
            cache[rid] = trace_metrics.unpack_traces(npz.read_bytes())
        if pid in cache[rid]:
            out[pid] = cache[rid][pid]
    return out


def write_detections(dets: list[TraceDetection], path: Path, extra: Mapping[str, str] | None = None) -> None:
    import csv

    extra = dict(extra or {})
    names = [*extra, *(f.name for f in dc.fields(TraceDetection))]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        w.writeheader()
        for d in dets:
            w.writerow({**extra, **{k: ("" if v is None else v) for k, v in dc.asdict(d).items()}})
