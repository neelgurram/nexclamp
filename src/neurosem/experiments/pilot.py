"""Milestone 6 pilot (spec "Solo-feasible scope: Pilot" and "Milestone 6: Pilot decision").

Runs the full pipeline on the pilot models and writes ``pilot_report.md``, which checks
the specification's three pilot success criteria against the data -- and says so plainly
when a criterion is not met. It never manufactures drift: if no silent mutant exists, the
report recommends reframing or stopping, as the specification requires.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from neurosem.experiments import campaign as cp
from neurosem.validation.convergence import EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME


def run_pilot(campaign: str = "pilot", model_ids: list[str] | None = None, workers: int | None = None,
              seed: int | None = None, n_mutants: int | None = None, n_transforms: int | None = None) -> Path:
    ctx = cp.make_context(campaign, workers)
    pcfg = ctx.cfg["pilot"]
    model_ids = model_ids or list(pcfg["models"])
    seed = int(seed if seed is not None else ctx.cfg["selection"]["seed"])
    refs = cp.reference_stage(ctx, model_ids)
    tol = cp.calibrate_stage(ctx, refs)
    variants = cp.generate_stage(ctx, refs, pcfg["mutation_families"],
                                 int(n_mutants if n_mutants is not None else pcfg["mutants_per_operator"]),
                                 int(n_transforms if n_transforms is not None else pcfg["transforms_per_operator"]), seed)
    outcomes = cp.variant_stage(ctx, refs, tol, variants)
    summary = cp.aggregate(ctx, refs, outcomes)
    return write_report(ctx, refs, tol, outcomes, summary, seed)


def write_report(ctx, refs, tol, outcomes, summary, seed) -> Path:
    entries = tol.entries
    n = len(entries)
    excluded = [e for e in entries if e.limiting in (EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME)]
    limited = Counter(e.limiting for e in entries)
    determinism = {m: r.determinism["bitwise_identical_battery_traces"] for m, r in refs.items()}
    silent = summary["silent"]
    fp, nt = summary["false_positives"], summary["n_transforms"]

    crit1 = len(silent) >= 1
    crit2 = all(determinism.values()) and (len(excluded) / n < 0.25 if n else False)
    crit3 = nt > 0 and fp / nt <= 0.1
    lines = [
        f"# Pilot report: campaign `{ctx.campaign}`", "",
        "*Generated automatically from `results/processed/{0}/`. Development-stage pilot on discovery models; "
        "not a confirmatory result. Thresholds used below for the pilot decision are provisional and must be "
        "reviewed by Neel.*".format(ctx.campaign), "",
        "## Setup", "",
        f"- models: {', '.join(refs)}",
        f"- nominal dt: {ctx.nominal.dt_ms} ms; refinement factors {ctx.factors}",
        f"- mutation families: {', '.join(ctx.cfg['pilot']['mutation_families'])}; seed {seed}",
        f"- variants: {len(outcomes)} ({summary['cascade']['total_mutants']} mutants, {nt} valid transformations / "
        "no-change controls)",
    ]
    for mid, r in refs.items():
        m_entries = [e for e in entries if e.model_id == mid]
        undefined = sum(1 for e in m_entries if e.limiting == "both_undefined")
        silent_protocols = sorted({e.protocol_id for e in m_entries if e.feature == "spike_count" and e.f_h == 0})
        lines.append(f"- `{mid}` rheobase ({r.rheobase_status}): {r.rheobase_nA:.6g} nA; libNeuroML strict valid: "
                     f"{r.structural.libneuroml_strict}; {undefined} of {len(m_entries)} reference (protocol, feature) "
                     f"entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero "
                     f"reference spikes: {', '.join(silent_protocols) or 'none'}")
    lines += ["", "## Validation cascade (mutants)", "", "```", json.dumps(summary["cascade"], indent=2), "```", "",
              "## Classes (all variants)", "", "| class | count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(summary["classes"].items())]
    lines += ["", "## Pilot success criteria (specification)", "",
              f"1. **At least one admissible mutation passes the canonical protocol and is reproducibly detected by "
              f"another protocol:** {'MET' if crit1 else 'NOT MET'} ({len(silent)} silent mutant(s)"
              f"{': ' + ', '.join(silent) if silent else ''}).",
              f"2. **Feature extraction stable under numerical refinement:** {'MET' if crit2 else 'NOT MET'} -- "
              f"deterministic re-execution {determinism}; {len(excluded)} of {n} reference (protocol, feature) "
              f"tolerance entries excluded because their state or category changed between h and h/2; tolerance "
              f"limited by: {dict(limited)}. (Provisional pilot threshold: fewer than 25% excluded.)",
              f"3. **Valid transformations do not trigger widespread false positives:** {'MET' if crit3 else 'NOT MET'} -- "
              f"{fp} of {nt} valid transformations/no-change controls were classified non-equivalent. "
              "(Provisional pilot threshold: at most 10%.)", "",
              "## Decision guidance", ""]
    if crit1 and crit2 and crit3:
        lines.append("All three pilot criteria are met on these data. Per Milestone 6 the study may continue to "
                     "Milestone 7 after Neel reviews the audit sheet, the diagnostics of the silent mutants and the "
                     "tolerance table.")
    else:
        lines.append("Not all pilot criteria are met. Per the specification: do not manufacture drift. Review the "
                     "failing criterion; if hidden drift does not exist, reframe as an empirical evaluation of existing "
                     "validation adequacy or stop.")
    lines += ["", "## Files", "",
              "- `classification.csv`, `detections.csv`, `detection_matrix.csv`, `protocol_costs.csv`",
              "- `tolerances.csv`, `convergence.csv`, `validation_cascade.json`, `false_positives.csv`",
              "- `mutant_audit_sheet.csv` (Milestone 4 exit criterion: a human must audit at least 20 mutants)",
              "- `variants/<variant_id>/diagnostic.md` (Milestone 5 exit criterion: evidence for every detection)",
              "- `references/<model>/` (protocols, canonical window, rheobase search, fingerprints, determinism)"]
    path = ctx.processed / "pilot_report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
