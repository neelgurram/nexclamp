"""Held-out evaluation (Milestone 8). Deliberately gated.

This code path is the ONLY one allowed to read held-out split files, and only through
``selection.splits.HeldoutGate``, which requires ``configs/FROZEN.lock`` (hashes of the
preregistered configuration, tolerance rule, splits and the frozen protocol selection) to
match the current files, and appends every access to ``results/heldout_access.log``.

It must not be run during development. Nothing in the pilot calls it.
"""

from __future__ import annotations

import json
from pathlib import Path

from neurosem import config
from neurosem.protocols.definitions import CANONICAL_ID
from neurosem.provenance import REPO_ROOT, utc_now


def evaluate_heldout(campaign: str, selection_file: Path, reason: str, workers: int | None = None) -> Path:
    from neurosem.analysis import bootstrap, metrics
    from neurosem.experiments import campaign as cp
    from neurosem.schemas import VariantKind
    from neurosem.selection.splits import HeldoutGate

    gate = HeldoutGate(REPO_ROOT, REPO_ROOT / "configs" / "FROZEN.lock", reason)
    split = gate.split()
    selection = json.loads(Path(selection_file).read_text(encoding="utf-8"))
    ctx = cp.make_context(campaign, workers)
    refs = cp.reference_stage(ctx, list(split.heldout_models))
    tol = cp.calibrate_stage(ctx, refs)        # frozen RULE and constants; per-model refinement terms from references
    families = sorted(set(ctx.cfg["pilot"]["mutation_families"]) | set(split.heldout_families))
    variants = cp.generate_stage(ctx, refs, families, int(ctx.cfg["pilot"]["mutants_per_operator"]),
                                 int(ctx.cfg["pilot"]["transforms_per_operator"]), int(ctx.cfg["selection"]["seed"]))
    outcomes = cp.variant_stage(ctx, refs, tol, variants)
    summary = cp.aggregate(ctx, refs, outcomes)

    adm = [o for o in outcomes if o.variant.kind is VariantKind.MUTANT and o.klass.admissible]
    sel = set(selection["selected_protocols"])
    import numpy as np

    battery = np.array([bool(sel & set(o.detecting_protocols)) for o in adm])
    canonical = np.array([CANONICAL_ID in o.detecting_protocols for o in adm])
    clusters = np.array([o.variant.model_id for o in adm])
    result = {
        "campaign": campaign, "created_utc": utc_now(), "reason": reason, "selection_file": str(selection_file),
        "n_heldout_admissible_mutants": int(len(adm)), "heldout_models": list(split.heldout_models),
        "heldout_families": list(split.heldout_families),
        "paired_counts": metrics.paired_counts(battery, canonical),
        "rate_selected": float(battery.mean()) if len(adm) else None,
        "rate_canonical": float(canonical.mean()) if len(adm) else None,
        "cluster_bootstrap": bootstrap.cluster_bootstrap_diff(battery, canonical, clusters, 10000,
                                                              int(ctx.cfg["selection"]["seed"])) if len(adm) else None,
        "cascade": summary["cascade"],
    }
    pc = result["paired_counts"]
    result["exact_mcnemar_p"] = bootstrap.exact_mcnemar(pc["only_a"], pc["only_b"]) if len(adm) else None
    out = ctx.processed / "heldout_evaluation.json"
    out.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    return out
