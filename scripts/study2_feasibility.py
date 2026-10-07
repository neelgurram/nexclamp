"""Feasibility probe for the Study 2 NEURON replication: can the battery run in NEURON, and how long?

This measures the cost and the failure modes of putting the preregistered battery through NEURON.
It computes **no detection and no feature difference**, and it reads the sealed Study 1 records
read-only (only to reuse each base model's frozen rheobase, so that the probe does not pay for a
rheobase search). Nothing here touches a campaign.

For each base model: materialise it, instantiate the three selected battery protocols at the frozen
rheobase, then run the same probe LEMS through jLEMS and through NEURON, and record the wall-clock
cost of the export, the mechanism build and the run, together with the spike count each simulator
produces per protocol. Spike counts are descriptive here: they say whether NEURON produced a usable
trace, not whether anything was detected.

    python scripts/study2_feasibility.py --models smith2013_singlecomp
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp import config
from nexclamp.models import load_models, materialize
from nexclamp.protocols import rheobase as rb
from nexclamp.protocols.definitions import batched, templates_from_config
from nexclamp.protocols.generate import group_by_length, write_probe
from nexclamp.provenance import REPO_ROOT, git_state, utc_now
from nexclamp.simulators.jneuroml import JNeuroML
from nexclamp.simulators.neuron import NeuronSimulator

CAMPAIGN = "heldout-v1"
BATTERY = json.loads((REPO_ROOT / "results/processed/pilot2/selection_k4.json").read_text(
    encoding="utf-8"))["selected_protocols"]
HELDOUT = ["smith2013_singlecomp", "traub2005_testseg2", "traub2005_testseg_all",
           "migliore2005_ca1_soma", "hay2011_soma", "bbp2015_soma"]


def frozen_rheobase(model_id: str) -> float | None:
    """The rheobase the sealed campaign recorded for this base model. Read-only."""
    for path in sorted((REPO_ROOT / "results/raw" / CAMPAIGN).glob("*/rheobase.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if rec.get("model_id") == model_id and rec.get("variant_id") == f"{model_id}__reference":
            result = rec.get("result", {})
            return result.get("rheobase_nA") if result.get("status") == "ok" else None
    return None


def spike_counts(result, protocols) -> dict:
    out = {}
    for p in protocols:
        tr = result.traces.get(p.protocol_id)
        out[p.protocol_id] = (None if tr is None
                              else int(rb.count_upward_crossings(tr.v_mV, -20.0)))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--models", nargs="*", default=["smith2013_singlecomp"], choices=HELDOUT)
    ap.add_argument("--timeout-s", type=float, default=7200.0)
    a = ap.parse_args(argv)

    cfg = config.study()
    exec_cfg = config.nominal_exec(cfg)
    templates = [t for t in batched(templates_from_config(cfg["protocols"]))
                 if t.protocol_id in BATTERY]
    if len(templates) != len(BATTERY):
        print(f"expected {BATTERY}, resolved {[t.protocol_id for t in templates]}")
        return 2
    jlems = JNeuroML(max_memory=cfg["numerics"]["java_max_memory"])
    neuron = NeuronSimulator()
    commit, dirty = git_state()
    stamp = utc_now().replace(":", "").replace("-", "")[:15]
    out_dir = REPO_ROOT / "results/audits/study2_feasibility" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"written_utc": utc_now(), "git_commit": commit, "git_dirty": dirty,
              "purpose": "timing and toolchain feasibility only; no detection is computed",
              "battery": BATTERY, "jlems_version": jlems.version_info(),
              "neuron_version": neuron.version_info(), "models": {}}

    for mid in a.models:
        rec: dict = {"model_id": mid}
        rh = frozen_rheobase(mid)
        rec["frozen_rheobase_nA"] = rh
        if rh is None:
            rec["skipped"] = "no ok rheobase in the sealed campaign record"
            report["models"][mid] = rec
            continue
        ws = materialize(load_models()[mid], config.work_dir(cfg) / "study2_probe" / mid, overwrite=True)
        protos = [t.instantiate(rh, cfg["numerics"]["settle_ms"]) for t in templates]
        rec["groups"] = []
        for group in group_by_length(protos):
            bundle = write_probe(ws, group, exec_cfg, tag=f"s2_battery_{int(group[0].total_ms)}")
            g: dict = {"protocols": [p.protocol_id for p in group], "length_ms": bundle.length_ms,
                       "cell_steps": bundle.cell_steps}
            t0 = time.perf_counter()
            jr = jlems.run_lems(bundle.lems_file, [bundle.output], timeout_s=a.timeout_s)
            g["jlems"] = {"status": jr.status.value, "seconds": round(time.perf_counter() - t0, 1),
                          "spikes": spike_counts(jr, group), "message": jr.message[:300]}
            t0 = time.perf_counter()
            nr = neuron.run_lems(bundle.lems_file, [bundle.output], timeout_s=a.timeout_s)
            g["neuron"] = {"status": nr.status.value, "seconds": round(time.perf_counter() - t0, 1),
                           "spikes": spike_counts(nr, group), "message": nr.message[:1200]}
            rec["groups"].append(g)
            print(f"[{mid}] {g['protocols']}: jLEMS {g['jlems']['status']} {g['jlems']['seconds']}s | "
                  f"NEURON {g['neuron']['status']} {g['neuron']['seconds']}s")
            if nr.status.value != "ok":
                print(f"    NEURON says: {nr.message[:400]}")
        report["models"][mid] = rec

    (out_dir / "feasibility.json").write_text(json.dumps(report, indent=2) + "\n",
                                              encoding="utf-8", newline="\n")
    print(f"wrote {(out_dir / 'feasibility.json').relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
