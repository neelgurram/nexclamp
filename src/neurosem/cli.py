"""NeuroSem command-line interface (spec "Suggested commands").

Every command is a thin wrapper around ``neurosem.experiments``. Commands never touch
held-out data except ``evaluate-heldout``, which is gated by ``configs/FROZEN.lock``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _models_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--models", nargs="*", help="model ids (default: pilot models from configs/study.yaml)")


def _campaign_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--campaign", default="pilot", help="campaign name (results/processed/<campaign>)")
    p.add_argument("--workers", type=int, default=None)


def cmd_fetch_models(a) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    import fetch_models

    return fetch_models.main(["--dest", a.dest])


def cmd_validate_models(a) -> int:
    from neurosem import config
    from neurosem.models import load_models, materialize
    from neurosem.simulators.jneuroml import JNeuroML
    from neurosem.validation import structural

    sim = JNeuroML()
    models = load_models()
    ids = a.models or [m for m, r in models.items() if r.inclusion in ("include", "candidate")]
    ok = True
    for mid in ids:
        ws = materialize(models[mid], config.work_dir() / "validate" / mid, overwrite=True)
        r = structural.check(ws, sim)
        ok &= bool(r.valid)
        print(f"{mid:28s} jnml_valid={r.valid!s:5s} libneuroml_strict={r.libneuroml_strict!s:5s} files={r.files}")
        for m in r.jnml.messages[:5]:
            print("    ", m)
    return 0 if ok else 1


def cmd_run_reference(a) -> int:
    from neurosem.experiments import campaign as cp

    ctx = cp.make_context(a.campaign, a.workers)
    refs = cp.reference_stage(ctx, a.models or list(ctx.cfg["pilot"]["models"]))
    for mid, r in refs.items():
        print(f"{mid}: rheobase {r.rheobase_nA:.6g} nA ({r.rheobase_status}); determinism {r.determinism}")
    return 0


def cmd_calibrate(a) -> int:
    from neurosem.experiments import campaign as cp

    ctx = cp.make_context(a.campaign, a.workers)
    refs = cp.reference_stage(ctx, a.models or list(ctx.cfg["pilot"]["models"]))
    tol = cp.calibrate_stage(ctx, refs)
    print(f"wrote {ctx.processed / 'tolerances.csv'} ({len(tol.entries)} entries)")
    return 0


def cmd_generate(a) -> int:
    from neurosem.experiments import campaign as cp

    ctx = cp.make_context(a.campaign, a.workers)
    refs = cp.reference_stage(ctx, a.models or list(ctx.cfg["pilot"]["models"]))
    fams = a.families or list(ctx.cfg["pilot"]["mutation_families"])
    recs = cp.generate_stage(ctx, refs, fams, a.n_mutants or int(ctx.cfg["pilot"]["mutants_per_operator"]),
                             a.n_transforms or int(ctx.cfg["pilot"]["transforms_per_operator"]),
                             a.seed if a.seed is not None else int(ctx.cfg["selection"]["seed"]))
    print(f"generated {len(recs)} variants")
    return 0


def cmd_classify(a, fingerprints_only: bool = False) -> int:
    from neurosem.experiments import campaign as cp

    ctx = cp.make_context(a.campaign, a.workers)
    refs = cp.reference_stage(ctx, a.models or list(ctx.cfg["pilot"]["models"]))
    tol = cp.calibrate_stage(ctx, refs)
    variants = [v for v in cp.load_variant_records(ctx) if v.model_id in refs]
    outcomes = cp.variant_stage(ctx, refs, tol, variants)
    summary = cp.aggregate(ctx, refs, outcomes)
    print(json.dumps({k: v for k, v in summary.items()}, indent=2, default=str))
    return 0


def cmd_select(a) -> int:
    from neurosem.experiments.discovery import select_protocols

    print(select_protocols(a.campaign, a.budget, a.draws, a.seed))
    return 0


def cmd_heldout(a) -> int:
    from neurosem.experiments.heldout import evaluate_heldout

    print(evaluate_heldout(a.campaign, Path(a.selection), a.reason, a.workers))
    return 0


def cmd_agent(a) -> int:
    from neurosem.experiments import agent

    score = agent.score_trial(a.task, Path(a.trial_dir), Path(a.frozen_config) if a.frozen_config else None)
    print(json.dumps(score, indent=2, default=str))
    return 0


def cmd_analyze(a) -> int:
    from neurosem.experiments.analyze import analyze_campaign

    print(analyze_campaign(a.campaign))
    return 0


def cmd_reproduce(a) -> int:
    from neurosem.experiments.analyze import reproduce_paper

    print(reproduce_paper(a.campaign))
    return 0


def cmd_pilot(a) -> int:
    from neurosem.experiments.pilot import run_pilot

    print(run_pilot(a.campaign, a.models, a.workers, a.seed, a.n_mutants, a.n_transforms))
    return 0


def cmd_smoke(a) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    import smoke_jnml

    return smoke_jnml.main(a.models or ["pospischil2008_rs", "pospischil2008_lts"])


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="neurosem", description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("fetch-models", help="download commit-pinned model snapshots with provenance")
    p.add_argument("--dest", default="models/raw")
    p.set_defaults(fn=cmd_fetch_models)

    p = sub.add_parser("validate-models", help="structural validation of manifest models")
    _models_arg(p)
    p.set_defaults(fn=cmd_validate_models)

    for name, fn, helptext in [("run-reference", cmd_run_reference, "reference fingerprints at h, h/2, h/4 + determinism"),
                               ("calibrate-tolerances", cmd_calibrate, "tolerance table from reference refinement")]:
        p = sub.add_parser(name, help=helptext)
        _campaign_arg(p)
        _models_arg(p)
        p.set_defaults(fn=fn)

    p = sub.add_parser("generate-mutants", help="mutants and valid transformations")
    _campaign_arg(p)
    _models_arg(p)
    p.add_argument("--families", nargs="*")
    p.add_argument("--n-mutants", type=int, default=None, help="sites per mutation operator")
    p.add_argument("--n-transforms", type=int, default=None, help="sites per transform operator")
    p.add_argument("--seed", type=int, default=None)
    p.set_defaults(fn=cmd_generate)

    for name in ("classify-mutants", "build-fingerprints"):
        p = sub.add_parser(name, help="fingerprint, compare and classify generated variants")
        _campaign_arg(p)
        _models_arg(p)
        p.set_defaults(fn=cmd_classify)

    p = sub.add_parser("select-protocols", help="greedy selection + random baselines on the discovery split")
    _campaign_arg(p)
    p.add_argument("--budget", type=int, default=None)
    p.add_argument("--draws", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.set_defaults(fn=cmd_select)

    p = sub.add_parser("evaluate-heldout", help="GATED held-out evaluation (requires configs/FROZEN.lock)")
    _campaign_arg(p)
    p.add_argument("--selection", required=True, help="frozen selection JSON")
    p.add_argument("--reason", required=True, help="logged justification for accessing held-out data")
    p.set_defaults(fn=cmd_heldout)

    p = sub.add_parser("evaluate-agent", help="score one agent trial with hidden deterministic evaluators")
    p.add_argument("--task", required=True)
    p.add_argument("--trial-dir", required=True)
    p.add_argument("--frozen-config", default=None)
    p.set_defaults(fn=cmd_agent)

    p = sub.add_parser("analyze", help="metrics, statistics and figures from processed results")
    _campaign_arg(p)
    p.set_defaults(fn=cmd_analyze)

    p = sub.add_parser("reproduce-paper", help="rebuild all tables and figures from raw/processed results")
    _campaign_arg(p)
    p.set_defaults(fn=cmd_reproduce)

    p = sub.add_parser("pilot", help="run the Milestone 6 pilot end to end")
    _campaign_arg(p)
    _models_arg(p)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--n-mutants", type=int, default=None)
    p.add_argument("--n-transforms", type=int, default=None)
    p.set_defaults(fn=cmd_pilot)

    p = sub.add_parser("smoke", help="quick end-to-end simulator smoke check")
    _models_arg(p)
    p.set_defaults(fn=cmd_smoke)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.fn(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
