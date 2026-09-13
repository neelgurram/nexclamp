"""Rheobase search (spec protocol 3).

Rheobase is the smallest amplitude of a fixed-duration current step that evokes at
least one spike. eFEL has no rheobase feature and pyNeuroML's f-I helper only reports
the lowest tested amplitude that spiked, so NeuroSem performs a bracketing grid search:
each round simulates a grid of amplitudes in one batched run and narrows the bracket
to the interval between the last silent and the first spiking amplitude.

The result is reported as the first spiking amplitude plus the final bracket width
(the resolution). Its cost -- simulations and cell-steps -- is recorded so that
runtime-matched baselines can charge for it.
"""

from __future__ import annotations

import dataclasses as dc
from collections.abc import Callable, Sequence

import numpy as np

# Maps a list of amplitudes (nA) to spike counts in the step window, or None on failure.
SpikeCounter = Callable[[Sequence[float]], Sequence[int] | None]


@dc.dataclass
class RheobaseResult:
    rheobase_nA: float | None
    status: str                  # ok | spontaneous | not_found | error
    lower_nA: float | None
    upper_nA: float | None
    n_simulations: int
    history: list[dict]

    @property
    def resolution_nA(self) -> float | None:
        if self.lower_nA is None or self.upper_nA is None:
            return None
        return self.upper_nA - self.lower_nA


def count_upward_crossings(v_mV: np.ndarray, threshold_mV: float) -> int:
    above = v_mV >= threshold_mV
    return int(np.count_nonzero(~above[:-1] & above[1:]))


def make_step_counter(sim, ws, exec_cfg, *, settle_ms: float, step_ms: float, threshold_mV: float,
                      timeout_s: float = 7200.0, tag: str = "rheo", cost_log: list | None = None) -> SpikeCounter:
    """Bind the search to a simulator: each call runs one batched probe of steps.

    ``sim`` is a :class:`neurosem.simulators.base.Simulator`, ``ws`` a model workspace.
    ``cost_log`` (if given) receives one dict per simulation with cell-steps and runtime.
    """
    from neurosem.protocols.generate import write_probe
    from neurosem.schemas import AnalysisWindow, ConcreteProtocol, RunStatus, StimulusComponent

    calls = {"n": 0}

    def counter(amps: Sequence[float]) -> Sequence[int] | None:
        calls["n"] += 1
        protos = [
            ConcreteProtocol(f"R{i:02d}", "step", (StimulusComponent("pulse", settle_ms, step_ms, a),),
                             settle_ms + step_ms, AnalysisWindow(settle_ms, settle_ms + step_ms), ())
            for i, a in enumerate(amps)
        ]
        bundle = write_probe(ws, protos, exec_cfg, tag=f"{tag}_{calls['n']}")
        res = sim.run_lems(bundle.lems_file, [bundle.output], timeout_s=timeout_s)
        if cost_log is not None:
            cost_log.append({"tag": f"{tag}_{calls['n']}", "cell_steps": bundle.cell_steps,
                             "runtime_s": res.runtime_s, "status": res.status.value})
        if res.status is not RunStatus.OK:
            return None
        out = []
        for p in protos:
            tr = res.traces[p.protocol_id]
            m = (tr.t_ms >= settle_ms) & (tr.t_ms <= settle_ms + step_ms)
            out.append(count_upward_crossings(tr.v_mV[m], threshold_mV))
        return out

    return counter


def search(count_spikes: SpikeCounter, *, hi_nA: float = 0.5, grid: int = 12, rounds: int = 4,
           expand: float = 4.0, max_hi_nA: float = 32.0) -> RheobaseResult:
    if grid < 3 or rounds < 1:
        raise ValueError("grid must be >= 3 and rounds >= 1")
    history: list[dict] = []
    n_sims = 0

    def run(amps: np.ndarray) -> np.ndarray | None:
        nonlocal n_sims
        n_sims += 1
        counts = count_spikes([float(a) for a in amps])
        if counts is None:
            history.append({"amplitudes_nA": amps.tolist(), "counts": None})
            return None
        counts = np.asarray(counts, dtype=int)
        history.append({"amplitudes_nA": amps.tolist(), "counts": counts.tolist()})
        return counts

    lo, hi = 0.0, float(hi_nA)
    # Bracketing phase: find an upper amplitude that spikes.
    while True:
        amps = np.linspace(lo, hi, grid)
        counts = run(amps)
        if counts is None:
            return RheobaseResult(None, "error", None, None, n_sims, history)
        if lo == 0.0 and counts[0] > 0:
            return RheobaseResult(0.0, "spontaneous", 0.0, 0.0, n_sims, history)
        idx = np.flatnonzero(counts > 0)
        if idx.size:
            i = int(idx[0])
            lo, hi = float(amps[i - 1]), float(amps[i])
            break
        if hi >= max_hi_nA:
            return RheobaseResult(None, "not_found", hi, None, n_sims, history)
        lo, hi = hi, min(hi * expand, max_hi_nA)

    # Refinement phase.
    for _ in range(rounds - 1):
        amps = np.linspace(lo, hi, grid)
        counts = run(amps)
        if counts is None:
            return RheobaseResult(None, "error", lo, hi, n_sims, history)
        idx = np.flatnonzero(counts > 0)
        if not idx.size:          # non-monotonic response inside the bracket: keep previous bracket
            history[-1]["note"] = "no spiking amplitude in refined grid; bracket kept"
            break
        i = int(idx[0])
        if i == 0:
            history[-1]["note"] = "lower bracket edge spiked; bracket kept"
            break
        lo, hi = float(amps[i - 1]), float(amps[i])
    return RheobaseResult(hi, "ok", lo, hi, n_sims, history)
