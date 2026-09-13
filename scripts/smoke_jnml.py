"""End-to-end smoke check of the simulation core on real fixtures (developer tool).

Validates each included model, runs its shipped harness, finds rheobase, and runs a
batched probe of the implemented protocols at the nominal time step. Prints timings.
Scratch output goes to work/smoke/ (git-ignored). This is plumbing verification, not
a scientific result.
"""

from __future__ import annotations

import sys
import time

import numpy as np

from neurosem import config
from neurosem.models import load_models, materialize
from neurosem.protocols import rheobase as rb
from neurosem.protocols.definitions import batched, templates_from_config
from neurosem.protocols.generate import canonical_output, group_by_length, write_probe
from neurosem.simulators.jneuroml import JNeuroML


def main(model_ids: list[str]) -> int:
    cfg = config.study()
    sim = JNeuroML(max_memory=cfg["numerics"]["java_max_memory"])
    print("simulator:", sim.version_info())
    models = load_models()
    exec_cfg = config.nominal_exec(cfg)
    templates = batched(templates_from_config(cfg["protocols"]))
    for mid in model_ids:
        m = models[mid]
        ws = materialize(m, config.work_dir(cfg) / "smoke" / mid, overwrite=True)
        v = sim.validate([ws.cell_path])
        print(f"\n[{mid}] validate: {v.valid} {v.messages[:2]}")
        t0 = time.perf_counter()
        can = sim.run_lems(ws.harness_path, [canonical_output(m)])
        tr = can.traces.get("P00_canonical")
        n = rb.count_upward_crossings(tr.v_mV, -20.0) if tr is not None else None
        print(f"[{mid}] canonical: {can.status.value} {can.runtime_s:.1f}s spikes={n} {can.message}")
        rcfg = cfg["rheobase"]
        cost: list[dict] = []
        counter = rb.make_step_counter(sim, ws, exec_cfg, settle_ms=cfg["numerics"]["settle_ms"],
                                       step_ms=rcfg["step_duration_ms"], threshold_mV=rcfg["spike_threshold_mV"],
                                       cost_log=cost)
        r = rb.search(counter, hi_nA=rcfg["initial_hi_nA"], grid=rcfg["grid"], rounds=rcfg["rounds"],
                      expand=rcfg["expand"], max_hi_nA=rcfg["max_hi_nA"])
        print(f"[{mid}] rheobase: {r.status} {r.rheobase_nA} nA (bracket {r.lower_nA}-{r.upper_nA}), "
              f"{r.n_simulations} sims, {sum(c['runtime_s'] for c in cost):.1f}s")
        rh = r.rheobase_nA if r.status == "ok" else rcfg["fallback_rheobase_nA"]
        protos = [t.instantiate(rh, cfg["numerics"]["settle_ms"]) for t in templates]
        for group in group_by_length(protos):
            b = write_probe(ws, group, exec_cfg, tag=f"battery_{int(group[0].total_ms)}")
            res = sim.run_lems(b.lems_file, [b.output])
            print(f"[{mid}] probe {int(b.length_ms)} ms x {len(group)} cells: {res.status.value} "
                  f"{res.runtime_s:.1f}s ({res.runtime_s / b.cell_steps * 1e6:.2f} us/cell-step) {res.message}")
            for p in group:
                tr = res.traces.get(p.protocol_id)
                if tr is None:
                    continue
                w = (tr.t_ms >= p.window.start_ms) & (tr.t_ms <= p.window.end_ms)
                print(f"     {p.protocol_id:26s} spikes_in_window={rb.count_upward_crossings(tr.v_mV[w], -20.0):3d} "
                      f"v[min,max]=[{np.min(tr.v_mV):.1f},{np.max(tr.v_mV):.1f}] mV")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["pospischil2008_rs", "pospischil2008_lts"]))
