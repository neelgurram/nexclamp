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

from neuraxis import config
from neuraxis.protocols.definitions import CANONICAL_ID
from neuraxis.provenance import REPO_ROOT, utc_now


def evaluate_heldout(campaign: str, selection_file: Path, reason: str, workers: int | None = None) -> Path:
    from neuraxis.analysis import bootstrap
    from neuraxis.experiments import campaign as cp
    from neuraxis.experiments import registry, strata
    from neuraxis.selection.splits import HeldoutGate

    # Pilot and discovery data never enter the confirmatory estimate (D-026); the campaign is
    # fresh, runs on the frozen configs/ only, and on one clean commit (D-025).
    if not (config.uses_default_config_dir() and config.uses_default_study_config()):
        raise registry.CampaignError(f"held-out evaluation must use configs/study.yaml (unset {config.CONFIG_DIR_ENV} "
                                     f"and {config.STUDY_CONFIG_ENV})")
    registry.assert_confirmatory_fresh(campaign, config.results_dir())
    gate = HeldoutGate(REPO_ROOT, REPO_ROOT / "configs" / "FROZEN.lock", reason)
    split = gate.split()
    selection = json.loads(Path(selection_file).read_text(encoding="utf-8"))
    ctx = cp.make_context(campaign, workers, role=registry.CONFIRMATORY_HELDOUT)
    refs = cp.reference_stage(ctx, list(split.heldout_models))
    tol = cp.calibrate_stage(ctx, refs)        # frozen RULE and constants; per-model refinement terms from references
    families = sorted(set(ctx.cfg["pilot"]["mutation_families"]) | set(split.heldout_families))
    variants = cp.generate_stage(ctx, refs, families, int(ctx.cfg["pilot"]["mutants_per_operator"]),
                                 int(ctx.cfg["pilot"]["transforms_per_operator"]), int(ctx.cfg["selection"]["seed"]))
    outcomes = cp.variant_stage(ctx, refs, tol, variants)
    summary = cp.aggregate(ctx, refs, outcomes)
    stray = sorted({o.variant.model_id for o in outcomes} - set(split.heldout_models))
    if stray:
        raise registry.CampaignError(f"non-held-out models in the confirmatory campaign: {stray}")
    code_commit = registry.check_single_clean_commit(ctx.rec.raw)

    # Primary semantic stratum only: numerical stress tests never enter the confirmatory denominator (D-030).
    adm = strata.primary_admissible(outcomes)
    sel = set(selection["selected_protocols"])
    import numpy as np

    battery = np.array([bool(sel & set(o.detecting_protocols)) for o in adm])
    canonical = np.array([CANONICAL_ID in o.detecting_protocols for o in adm])
    clusters = [o.variant.model_id for o in adm]
    acfg = ctx.cfg.get("analysis") or {}
    result = {
        "campaign": campaign, "campaign_role": registry.CONFIRMATORY_HELDOUT, "code_commit": code_commit,
        "created_utc": utc_now(), "reason": reason, "selection_file": str(selection_file),
        "n_heldout_admissible_mutants": int(len(adm)), "heldout_models": list(split.heldout_models),
        "heldout_families": list(split.heldout_families), "analysis_config": acfg,
        "primary_endpoint": (bootstrap.paired_comparison(battery, canonical, clusters, int(acfg.get("n_boot", 10000)),
                                                         int(acfg.get("n_perm", 10000)),
                                                         int(acfg.get("seed", ctx.cfg["selection"]["seed"])))
                             if len(adm) else None),
        "cascade": summary["cascade"],
    }
    out = ctx.processed / "heldout_evaluation.json"
    out.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    return out
