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

from nexclamp.experiments import campaign as cp
from nexclamp.experiments import registry
from nexclamp.validation.convergence import EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME


def run_pilot(campaign: str = "pilot", model_ids: list[str] | None = None, workers: int | None = None,
              seed: int | None = None, n_mutants: int | None = None, n_transforms: int | None = None) -> Path:
    ctx = cp.make_context(campaign, workers, role=registry.EXPLORATORY_PILOT)
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
    # Pilot criteria use the primary feature panel only; secondary features never change the result (D-029).
    panel = ctx.primary_panel
    entries = [e for e in tol.entries if e.feature in panel.get(e.protocol_id, frozenset({e.feature}))]
    n = len(entries)
    excluded = [e for e in entries if e.limiting in (EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME)]
    limited = Counter(e.limiting for e in entries)
    determinism = {m: r.determinism["bitwise_identical_battery_traces"] for m, r in refs.items()}
    silent = summary["silent"]
    fp, nt = summary["false_positives"], summary["n_transforms"]

    crit1 = len(silent) >= 1
    crit2 = all(determinism.values()) and (len(excluded) / n < 0.25 if n else False)
    crit3 = nt > 0 and fp / nt <= 0.1
    from nexclamp import config
    from nexclamp.provenance import git_state

    meta = ctx.meta
    commit, dirty = git_state()
    lines = [f"# Pilot report: campaign `{ctx.campaign}`", ""]
    if meta:
        lines += [
            f"- project: **{meta.get('project_name', '')}**; study phase: **{meta.get('study_phase', '')}**; protocol "
            f"version: **{meta.get('protocol_version', '')}**",
            f"- designation: {meta.get('designation', '')}",
            "- findings in this report: **all exploratory; none confirmatory**",
            f"- analyses specified before the data were generated: yes, in `docs/{meta.get('protocol_version', '')}.md`",
            f"- software commit at report time: `{commit}` (tree dirty: {dirty}); per-run commits are in each `run.json`",
            f"- deviations: see `docs/pilot/{meta.get('protocol_version', '')}_DEVIATIONS.md`",
            f"- config set SHA-256: `{config.config_set_sha256()}`", ""]
    lines += [
        "**EXPLORATORY / DEVELOPMENTAL DATA.** Never pooled with the held-out data for the primary confirmatory "
        "estimate (DECISIONS D-026).", "",
        "*Generated automatically from `results/processed/{0}/`. Development-stage pilot; "
        "not a confirmatory result. Thresholds used below for the pilot decision are provisional and must be "
        "reviewed by Neel.*".format(ctx.campaign), "",
        "## Setup", "",
        f"- models: {', '.join(refs)}",
        f"- nominal dt: {ctx.nominal.dt_ms} ms; refinement factors {ctx.factors}",
        f"- mutation families: {', '.join(ctx.cfg['pilot']['mutation_families'])}; seed {seed}",
        f"- variants: {len(outcomes)} ({summary['n_semantic_mutants']} primary semantic mutants, "
        f"{summary['n_numerical_mutants']} numerical robustness stress tests, {nt} valid transformations / "
        "no-change controls)",
        f"- excluded operators: {', '.join((ctx.cfg.get('pilot') or {}).get('exclude_operators') or []) or 'none'}",
        f"- primary feature panel: {sorted(set().union(*panel.values()))}",
    ]
    for mid, r in refs.items():
        m_entries = [e for e in entries if e.model_id == mid]
        undefined = sum(1 for e in m_entries if e.limiting == "both_undefined")
        silent_protocols = sorted({e.protocol_id for e in m_entries if e.feature == "spike_count" and e.f_h == 0})
        lines.append(f"- `{mid}` rheobase ({r.rheobase_status}): {r.rheobase_nA:.6g} nA; libNeuroML strict valid: "
                     f"{r.structural.libneuroml_strict}; {undefined} of {len(m_entries)} reference (protocol, feature) "
                     f"entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero "
                     f"reference spikes: {', '.join(silent_protocols) or 'none'}")
    lines += ["", "## Validation cascade (primary semantic mutants)", "", "```", json.dumps(summary["cascade"], indent=2),
              "```", "", "## Classes by stratum", "", "| stratum | class | count |", "|---|---|---|"]
    lines += [f"| {s} | {k} | {v} |" for s, c in sorted(summary["classes_by_stratum"].items()) for k, v in sorted(c.items())]
    lines += ["", "## Pilot success criteria (specification; primary semantic stratum and primary feature panel)", "",
              f"1. **At least one admissible semantic mutation passes the canonical protocol and is reproducibly "
              f"detected by another protocol:** {'MET' if crit1 else 'NOT MET'} ({len(silent)} silent mutant(s)"
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
    if ctx.levels_enabled:
        lv = [o.levels for o in outcomes if o.levels and o.stratum == "primary_semantic"]
        keys = ("A_basic_pass", "B_canonical_feature", "C_canonical_trace", "D_multi_protocol", "E_full_battery",
                "feature_level_canonical_survivor", "full_trace_canonical_survivor")
        lines += ["", "## Validation levels (model mutants; B and C kept separate)", "", "| level | count |", "|---|---|"]
        lines += [f"| {k} | {sum(bool(x.get(k)) for x in lv)} of {len(lv)} |" for k in keys]
        lines += ["", "Branch classification and all prespecified outputs: `pilot_v2_outputs/` "
                      "(`scripts/pilot_v2_outputs.py`)."]
    num_missed = summary["numerical_missed_by_canonical"]
    lines += ["", "## Numerical robustness and convergence stress tests (separate analysis; never semantic drift)", "",
              f"- {summary['n_numerical_mutants']} numerical mutants; cascade: "
              f"`{json.dumps(summary['cascade_numerical_robustness'])}`",
              f"- missed by canonical but detected elsewhere: {len(num_missed)}"
              f"{' (' + ', '.join(num_missed) + ')' if num_missed else ''}. These are numerical sensitivities, "
              "not hidden semantic drift.",
              f"- per-feature deviation versus the reference's own h / h/2 / h/4 discretisation error: "
              f"`numerical_robustness.csv` ({summary['n_numerical_robustness_rows']} rows)",
              "", "## Secondary exploratory features (reported only; do not change the result above)", "",
              f"- mutants the primary panel classed as equivalent but a secondary feature detected reproducibly: "
              f"{len(summary['secondary_primary_miss'])}"
              f"{' (' + ', '.join(summary['secondary_primary_miss']) + ')' if summary['secondary_primary_miss'] else ''}",
              "- details: `secondary_feature_report.csv`, `detections_secondary.csv`"]
    lines += ["", "## Files", "",
              "- `classification.csv` (with `stratum` and `interpretation`), `detections.csv`, `detection_matrix.csv` "
              "(primary semantic only), `protocol_costs.csv`, `generation.json`",
              "- `tolerances.csv`, `convergence.csv`, `validation_cascade.json`, `false_positives.csv`",
              "- `mutant_audit_sheet.csv` (Milestone 4 exit criterion: a human must audit at least 20 mutants)",
              "- `variants/<variant_id>/diagnostic.md` (Milestone 5 exit criterion: evidence for every detection)",
              "- `references/<model>/` (protocols, canonical window, rheobase search, fingerprints, determinism)"]
    path = ctx.processed / "pilot_report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
