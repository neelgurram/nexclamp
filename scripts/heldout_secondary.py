"""Secondary analyses of the sealed held-out campaign, exactly as listed in the analysis plan.

Every number here is computed from the campaign's recorded outputs; nothing is simulated and
nothing inside ``results/processed/<campaign>`` is written (the campaign is sealed). Output goes
to ``results/tables/<campaign>/``. The primary endpoint is not recomputed here: it is the one in
``heldout_evaluation.json``, produced by the frozen pipeline.

Analyses (docs/STATISTICAL_ANALYSIS_PLAN.md sections 5-7):

- S1  random count-matched and runtime-matched batteries (same candidates and seeds as selection)
- S2  silent-survival rate after canonical testing, overall / per model / per family
- S3  false-positive rate on valid transformations, per strategy
- S4  detection by mutation family, with the held-out kinetics family reported on its own
- S5  coverage versus number of protocols, frozen greedy order applied to held-out mutants
- S6  cost (cell-steps) per detected mutant, per strategy
- canonical level B (features) versus level C (full trace), never merged
- unique contribution per protocol
- tolerance sensitivity (x0.5, 1, 2, 4)

    python scripts/heldout_secondary.py --campaign heldout-v1
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402

from neuraxis import config  # noqa: E402
from neuraxis.analysis import bootstrap, metrics  # noqa: E402
from neuraxis.experiments import pilot_outputs as po  # noqa: E402
from neuraxis.experiments import pilot_v2_outputs as p2  # noqa: E402
from neuraxis.experiments import strata  # noqa: E402
from neuraxis.provenance import REPO_ROOT, git_state, sha256_file, utc_now  # noqa: E402
from neuraxis.selection import greedy  # noqa: E402
from neuraxis.selection.matrix import DetectionMatrix  # noqa: E402

CANONICAL = "P00_canonical"
HELDOUT_FAMILY = "kinetics"


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cols: list[str] = []
    for r in rows:
        cols += [k for k in r if k not in cols]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def rate(k: int, n: int) -> float | None:
    return k / n if n else None


def ci(k: int, n: int) -> tuple[float | None, float | None]:
    return metrics.proportion_ci(k, n) if n else (None, None)


def random_baselines(m: DetectionMatrix, selected: list[str], draws: int, seed: int) -> dict:
    """S1. Same candidate pool (canonical excluded) and seeds as the discovery selection."""
    cands = [p for p in m.protocol_ids if p != CANONICAL]
    sel_rate = m.rate(selected)
    # Count-matched: the pool is small, so every k-subset is enumerated (plan section 6).
    exact = np.array([m.rate(list(s)) for s in itertools.combinations(sorted(cands), len(selected))])
    budget = float(sum(m.cost[p] for p in selected))
    rt = greedy.random_runtime_matched(m, budget, draws, seed + 1, cands)

    def dist(x: np.ndarray, enumerated: bool) -> dict:
        x = np.asarray(x, dtype=float)
        return {"n_sets": int(x.size), "enumerated": enumerated, "mean": float(x.mean()),
                "median": float(np.median(x)), "p2_5": float(np.quantile(x, 0.025)),
                "p97_5": float(np.quantile(x, 0.975)),
                "selected_percentile_rank": float((x < sel_rate).mean() + 0.5 * (x == sel_rate).mean()),
                "p_rand": float((x >= sel_rate).mean()) if enumerated
                else float((1 + (x >= sel_rate).sum()) / (1 + x.size))}

    return {"selected_rate": sel_rate, "selected_cost_cell_steps": budget, "candidates": cands,
            "count_matched": dist(exact, True), "runtime_matched": dist(rt, False),
            "exhaustive_rate": m.rate(m.protocol_ids), "canonical_rate": m.rate([CANONICAL])}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--selection", default="results/processed/pilot2/selection_k4.json")
    a = ap.parse_args(argv)

    cfg = config.study()
    seed = int(cfg["selection"]["seed"])
    draws = int(cfg["selection"]["random_draws"])
    n_boot = int(cfg.get("analysis", {}).get("n_boot", 10000))
    proc = config.results_dir() / "processed" / a.campaign
    out = config.results_dir() / "tables" / a.campaign
    selection = json.loads((REPO_ROOT / a.selection).read_text(encoding="utf-8"))
    selected = list(selection["selected_protocols"])
    ev = json.loads((proc / "heldout_evaluation.json").read_text(encoding="utf-8"))

    c = po.CampaignView(proc, [], [])
    m = DetectionMatrix.from_csv(proc / "detection_matrix.csv")
    det = {mid: {p for p in m.protocol_ids if m.covered([p])[i]} for i, mid in enumerate(m.mutant_ids)}
    sem = [r for r in c.cls if c.stratum(r) == strata.SEMANTIC and r["kind"] == "mutant"]
    adm = [r for r in sem if r["variant_id"] in det]
    assert len(adm) == m.n_mutants == ev["n_heldout_admissible_mutants"], "admissible sets disagree"
    ctl = [r for r in c.cls if c.stratum(r) == strata.CONTROL]
    summary: dict = {"campaign": a.campaign, "created_utc": utc_now(), "selected_protocols": selected,
                     "n_admissible": len(adm), "n_controls": len(ctl), "seed": seed,
                     "detection_matrix_sha256": sha256_file(proc / "detection_matrix.csv"),
                     "primary_endpoint_source": "heldout_evaluation.json (frozen pipeline; not recomputed)"}

    def hit(r: dict, strategy: str) -> bool:
        d = det[r["variant_id"]]
        return {"canonical": CANONICAL in d, "selected": bool(d & set(selected)),
                "exhaustive": bool(d)}[strategy]

    # S1 random baselines
    summary["S1_random_baselines"] = random_baselines(m, selected, draws, seed)

    # S2 silent survival: class 6 / (class 5 + class 6), same reproducible canonical rule
    s2_rows = []
    for key in ("all", "model_id", "family"):
        groups: dict[str, list] = defaultdict(list)
        for r in adm:
            groups["all" if key == "all" else r[key]].append(r)
        for g, rs in sorted(groups.items()):
            n6 = sum(r["class"].startswith("6") for r in rs)
            n5 = sum(r["class"].startswith("5") for r in rs)
            lo, hi = ci(n6, n5 + n6)
            s2_rows.append({"grouping": key, "group": g, "silent_class6": n6, "non_equivalent_class5": n5,
                            "silent_survival_rate": rate(n6, n5 + n6), "ci_low_exact": lo, "ci_high_exact": hi})
    x6 = np.array([r["class"].startswith("6") for r in adm])
    boot = bootstrap.cluster_bootstrap_rate(x6, [r["model_id"] for r in adm], n_boot, seed)
    summary["S2_silent_survival"] = {"rate": boot["rate"], "cluster_ci": [boot["ci_low"], boot["ci_high"]],
                                     "canonical_detected_at_h_only": sum(
                                         po.truthy(r["canonical_detected_h"]) and not po.truthy(
                                             r["canonical_detected_reproducible"]) for r in adm)}
    write_csv(out / "S2_silent_survival.csv", s2_rows)

    # S3 false positives on valid transformations, per strategy
    fp_rows = []
    for strategy_name, lv in (("canonical_feature", "B_canonical_feature"), ("canonical_trace", "C_canonical_trace"),
                              ("any_protocol_features_or_trace", "E_full_battery")):
        k = sum(p2._flag(r, lv) for r in ctl)
        lo, hi = ci(k, len(ctl))
        fp_rows.append({"strategy": strategy_name, "false_positives": k, "controls": len(ctl),
                        "rate": rate(k, len(ctl)), "ci_low_exact": lo, "ci_high_exact": hi})
    by_op: dict[str, list] = defaultdict(list)
    for r in ctl:
        by_op[r["operator"]].append(r)
    for op, rs in sorted(by_op.items()):
        fp_rows.append({"strategy": f"any_protocol | transform {op}",
                        "false_positives": sum(p2._flag(r, "E_full_battery") for r in rs), "controls": len(rs)})
    write_csv(out / "S3_false_positives.csv", fp_rows)
    summary["S3_false_positive_rate_any_protocol"] = fp_rows[2]

    # S4 by family (kinetics = held-out family, reported on its own) and by model / severity
    s4 = []
    for key in ("family", "analysis_family", "model_id", "severity"):
        groups = defaultdict(list)
        for r in adm:
            groups[r[key]].append(r)
        for g, rs in sorted(groups.items()):
            row = {"grouping": key, "group": g, "n": len(rs)}
            for s in ("canonical", "selected", "exhaustive"):
                row[f"{s}_detected"] = sum(hit(r, s) for r in rs)
                row[f"{s}_rate"] = rate(row[f"{s}_detected"], len(rs))
            s4.append(row)
    write_csv(out / "S4_detection_by_group.csv", s4)
    kin = [r for r in adm if r["family"] == HELDOUT_FAMILY]
    non = [r for r in adm if r["family"] != HELDOUT_FAMILY]
    summary["S4_heldout_family"] = {}
    for label, rs in (("kinetics_unseen_family", kin), ("families_seen_in_development", non)):
        if not rs:
            continue
        can = np.array([hit(r, "canonical") for r in rs])
        sel = np.array([hit(r, "selected") for r in rs])
        pc = bootstrap.paired_comparison(sel, can, [r["model_id"] for r in rs], n_boot, n_boot, seed)
        summary["S4_heldout_family"][label] = {
            "n": len(rs), "canonical_rate": float(can.mean()), "selected_rate": float(sel.mean()),
            "diff": float(sel.mean() - can.mean()), "counts": pc["counts"],
            "cluster_ci": [pc["cluster_bootstrap"]["ci_low"], pc["cluster_bootstrap"]["ci_high"]],
            "reliable": pc["reliable"]}

    # S5 coverage versus number of protocols (frozen discovery order, then the rest by id)
    order = selected + sorted(p for p in m.protocol_ids if p not in selected and p != CANONICAL)
    X = np.array([[p in det[r["variant_id"]] for p in m.protocol_ids] for r in adm])
    curve = metrics.coverage_curve(X, m.protocol_ids, order, m.cost)
    write_csv(out / "S5_coverage_curve.csv", curve.to_dict("records"))
    summary["S5_protocols_to_reach"] = metrics.protocols_to_reach(curve).to_dict("records")

    # S6 cost per detected mutant (cell-steps of one pass of each strategy's protocols, h only)
    s6 = []
    for s, prots in (("canonical", [CANONICAL]), ("selected", selected), ("exhaustive", list(m.protocol_ids))):
        cost = float(sum(m.cost[p] for p in prots))
        k = sum(hit(r, s) for r in adm)
        s6.append({"strategy": s, "protocols": ";".join(prots), "cell_steps_per_variant": cost,
                   "detected": k, "n": len(adm), "cell_steps_per_detection": cost * len(adm) / k if k else None})
    write_csv(out / "S6_cost_per_detection.csv", s6)

    # Sensitivity: cluster by source family instead of base model. The AsPredicted registration
    # clusters on base model (the primary analysis); the internal plan also named source family
    # where models share a paper, so both are reported. Two pairs of held-out models share one.
    fam = {r["model_id"]: r["source_family"] for r in po.read_csv(REPO_ROOT / "data" / "model_manifest.csv")}
    pc = bootstrap.paired_comparison(m.covered(selected), m.covered([CANONICAL]),
                                     [fam[m.model_of[i]] for i in m.mutant_ids], n_boot, n_boot, seed)
    summary["sensitivity_cluster_by_source_family"] = {
        "clusters": sorted({fam[m.model_of[i]] for i in m.mutant_ids}), "diff": pc["cluster_bootstrap"]["diff"],
        "cluster_ci": [pc["cluster_bootstrap"]["ci_low"], pc["cluster_bootstrap"]["ci_high"]],
        "bootstrap_reliable": pc["cluster_bootstrap"]["reliable"], "warning": pc["cluster_bootstrap"]["warning"],
        "permutation_p": pc["cluster_permutation"]["p_value"],
        "permutation_min_attainable_p": pc["cluster_permutation"]["min_attainable_p"]}

    # Canonical level B versus level C, never merged (on the E-admissible set, as in Pilot 2)
    e_adm = [r for r in sem if p2._flag(r, "A_basic_pass") and p2._flag(r, "E_full_battery")]
    b = [p2._flag(r, "B_canonical_feature") for r in e_adm]
    cc = [p2._flag(r, "C_canonical_trace") for r in e_adm]
    summary["canonical_levels"] = {
        "denominator": "A_basic_pass and E_full_battery (features or trace, any protocol)",
        "n": len(e_adm), "B_features": sum(b), "C_full_trace": sum(cc),
        "B_only": sum(x and not y for x, y in zip(b, cc)), "C_only": sum(y and not x for x, y in zip(b, cc)),
        "B_or_C": sum(x or y for x, y in zip(b, cc)), "neither": sum(not (x or y) for x, y in zip(b, cc)),
        "B_or_C_rate": rate(sum(x or y for x, y in zip(b, cc)), len(e_adm))}
    summary["branch_classification"] = p2.classify_branch(c, proc)

    # Unique contribution per protocol (feature and trace reproducible detections)
    write_csv(out / "unique_protocol_contribution.csv", p2.unique_protocol_contribution(c, p2.trace_reproducible(proc)))

    # Tolerance sensitivity
    from neuraxis.experiments.analyze import reclassify, tolerance_sensitivity
    recl = reclassify(a.campaign, list(config.tolerances()["sensitivity_multipliers"]))
    recl.to_csv(out / "reclassification_by_tolerance.csv", index=False)
    sens, notes = tolerance_sensitivity(recl)
    sens.to_csv(out / "tolerance_sensitivity.csv", index=False)
    summary["tolerance_sensitivity"] = sens.to_dict("records")
    summary["tolerance_sensitivity_not_evaluable"] = {k: len(v) if hasattr(v, "__len__") else v
                                                      for k, v in notes.items()}

    commit, dirty = git_state()
    summary["git_commit"], summary["git_dirty"] = commit, dirty
    (out / "secondary_summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT).as_posix()}/ (commit {commit[:8]}, dirty {dirty})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
