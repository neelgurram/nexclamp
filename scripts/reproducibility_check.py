"""Prespecified deterministic reproducibility check for a finished, unsealed pilot campaign.

Selects variants deterministically (SHA-256 of "<seed>:<variant_id>", smallest first) among
executable variants: ``--n-mutants`` mutants and ``--n-controls`` controls. Each is re-simulated
as replicate 1 at the nominal step (battery and canonical harness), and its traces are compared
bit for bit with replicate 0. New runs get new run IDs; nothing is overwritten. The result goes
to ``results/processed/<campaign>/reproducibility_check.json``.

    NEUROSEM_CONFIG_DIR=configs/pilot_protocol_v1 python scripts/reproducibility_check.py --campaign pilot-v2
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis.experiments import campaign as cp  # noqa: E402
from neuraxis.experiments import registry  # noqa: E402
from neuraxis.provenance import git_state, utc_now  # noqa: E402

NOT_EXECUTABLE = ("1_structurally_invalid", "2_non_executable", "3_numerically_unstable")


def _same(a, b) -> bool:
    return set(a.traces) == set(b.traces) and all(np.array_equal(a.traces[k].v_mV, b.traces[k].v_mV) and
                                                   np.array_equal(a.traces[k].t_ms, b.traces[k].t_ms) for k in a.traces)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--n-mutants", type=int, default=6)
    ap.add_argument("--n-controls", type=int, default=2)
    a = ap.parse_args(argv)
    from neuraxis.mutations import load_variant

    ctx = cp.make_context(a.campaign, role=registry.EXPLORATORY_PILOT)
    seed = int(ctx.cfg["selection"]["seed"])
    with open(ctx.processed / "classification.csv", encoding="utf-8", newline="") as f:
        cls = [r for r in csv.DictReader(f) if r["class"] not in NOT_EXECUTABLE]
    key = lambda r: hashlib.sha256(f"{seed}:{r['variant_id']}".encode()).hexdigest()  # noqa: E731
    chosen = (sorted((r for r in cls if r["kind"] == "mutant"), key=key)[:a.n_mutants] +
              sorted((r for r in cls if r["kind"] != "mutant"), key=key)[:a.n_controls])
    models = sorted({r["model_id"] for r in chosen})
    refs = cp.reference_stage(ctx, models)          # content-addressed: reuses the campaign's reference runs
    records = {v.variant_id: v for v in cp.load_variant_records(ctx)}
    rows = []
    for r in chosen:
        v = records[r["variant_id"]]
        ws, rec = load_variant(cp.variant_dir(ctx, v))
        ref = refs[v.model_id]
        b0 = ctx.rec.run_battery(ws, rec, ref.protocols, ctx.nominal, replicate=0, need_traces=True)
        b1 = ctx.rec.run_battery(ws, rec, ref.protocols, ctx.nominal, replicate=1, need_traces=True)
        c0 = ctx.rec.run_canonical(ws, rec, ref.canonical, replicate=0, need_traces=True)
        c1 = ctx.rec.run_canonical(ws, rec, ref.canonical, replicate=1, need_traces=True)
        rows.append({"variant_id": v.variant_id, "model_id": v.model_id, "kind": v.kind.value, "class": r["class"],
                     "battery_status": [b0.status.value, b1.status.value], "canonical_status": [c0.status.value, c1.status.value],
                     "battery_bitwise_identical": _same(b0, b1), "canonical_bitwise_identical": _same(c0, c1),
                     "replicate1_run_ids": [x.run_id for x in b1.records + c1.records]})
    commit, dirty = git_state()
    out = {"campaign": a.campaign, "created_utc": utc_now(), "study_metadata": ctx.meta, "git_commit": commit,
           "git_dirty": dirty, "selection_rule": f"sha256('{seed}:<variant_id>') ascending; {a.n_mutants} mutants, "
           f"{a.n_controls} controls among executable variants", "variants": rows,
           "all_identical": all(x["battery_bitwise_identical"] and x["canonical_bitwise_identical"] for x in rows)}
    path = ctx.processed / "reproducibility_check.json"
    path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_identical": out["all_identical"], "n": len(rows)}))
    return 0 if out["all_identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
