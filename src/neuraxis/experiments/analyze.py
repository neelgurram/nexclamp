"""Analysis stage: tables, figures, tolerance sensitivity and reproduction checks.

Everything here reads ``results/processed/<campaign>/`` (and, for trace figures, the raw
trace files when present). Nothing is simulated. Results computed on a discovery/pilot
campaign are *in-sample and descriptive*: the same mutants define admissibility and, when
greedy ordering is used, the battery order. Only the gated held-out evaluation tests the
study hypothesis. Statistical outputs on few base models are flagged unreliable by the
analysis functions themselves.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from neuraxis import config
from neuraxis.protocols.definitions import CANONICAL_ID
from neuraxis.provenance import REPO_ROOT, sha256_file, utc_now
from neuraxis.schemas import MutantClass


def _paths(campaign: str) -> tuple[Path, Path, Path]:
    res = config.results_dir()
    proc, tables, figs = res / "processed" / campaign, res / "tables" / campaign, res / "figures" / campaign
    if not (proc / "classification.csv").is_file():
        raise FileNotFoundError(f"{proc / 'classification.csv'} missing: run the campaign first")
    tables.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)
    return proc, tables, figs


# --------------------------------------------------------------------------- re-classification
def reclassify(campaign: str, multipliers: list[float]) -> pd.DataFrame:
    """Re-derive every variant's class from saved fingerprints at several tolerance multipliers.

    A variant whose h/2 fingerprint was never simulated (no detection at the calibrated
    tolerance) cannot be classified at a smaller multiplier that newly detects something at h;
    it is reported as ``not_evaluable`` rather than guessed.
    """
    from neuraxis.validation.convergence import ToleranceTable
    from neuraxis.validation.fingerprint import classify, compare, load_fingerprint

    proc = config.results_dir() / "processed" / campaign
    cls = pd.read_csv(proc / "classification.csv")
    tol = ToleranceTable.from_csv(proc / "tolerances.csv")
    refs: dict[str, dict[int, Any]] = {}
    for mid in cls["model_id"].unique():
        rdir = proc / "references" / mid
        refs[mid] = {f: load_fingerprint(rdir / f"fingerprint_L{f}.json") for f in (1, 2) if (rdir / f"fingerprint_L{f}.json").is_file()}
    rows = []
    for _, r in cls.iterrows():
        vdir = proc / "variants" / r["variant_id"]
        st = json.loads((vdir / "structural.json").read_text(encoding="utf-8"))
        fp1 = load_fingerprint(vdir / "fingerprint_L1.json") if (vdir / "fingerprint_L1.json").is_file() else None
        fp2 = load_fingerprint(vdir / "fingerprint_L2.json") if (vdir / "fingerprint_L2.json").is_file() else None
        for mult in multipliers:
            if not st["valid"] or fp1 is None:
                klass = classify(bool(st["valid"]), fp1, fp2, [], None).value if not st["valid"] else "not_run"
            else:
                d1 = compare(refs[r["model_id"]][1], fp1, tol, mult) if fp1.status.value == "ok" else []
                if d1 and fp2 is None:
                    klass = "not_evaluable"
                else:
                    d2 = compare(refs[r["model_id"]][2], fp2, tol, mult) if (fp2 is not None and fp2.status.value == "ok") else ([] if d1 else None)
                    klass = classify(True, fp1, fp2, d1, d2).value
            rows.append({"variant_id": r["variant_id"], "model_id": r["model_id"], "kind": r["kind"],
                         "operator": r["operator"], "family": r["family"], "tolerance_multiplier": mult, "class": klass})
    return pd.DataFrame(rows)


def tolerance_sensitivity(recl: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    adm = {MutantClass.NON_EQUIVALENT.value, MutantClass.SILENT.value}
    rows, notes = [], {}
    for mult, g in recl.groupby("tolerance_multiplier"):
        ev = g[g["class"] != "not_evaluable"]
        notes[str(mult)] = {"not_evaluable": int((g["class"] == "not_evaluable").sum())}
        tr = ev[ev["kind"] != "mutant"]
        mu = ev[ev["kind"] == "mutant"]
        if len(tr):
            rows.append({"tolerance_multiplier": mult, "series": "false_positive_rate", "rate": float(tr["class"].isin(adm).mean())})
        if len(mu):
            rows.append({"tolerance_multiplier": mult, "series": "admissible_fraction_of_mutants",
                         "rate": float(mu["class"].isin(adm).mean())})
            rows.append({"tolerance_multiplier": mult, "series": "silent_fraction_of_mutants",
                         "rate": float((mu["class"] == MutantClass.SILENT.value).mean())})
    return pd.DataFrame(rows), notes


# --------------------------------------------------------------------------- traces for figures
def _load_trace(campaign: str, run_id: str, name: str):
    from neuraxis.features import trace_metrics

    npz = config.results_dir() / "raw" / campaign / run_id / "traces.npz"
    if not npz.is_file():
        return None
    return trace_metrics.unpack_traces(npz.read_bytes()).get(name)


def case_traces(campaign: str, variant_id: str, model_id: str, protocols: list[str]) -> pd.DataFrame | None:
    from neuraxis.validation.fingerprint import load_fingerprint

    proc = config.results_dir() / "processed" / campaign
    ref = load_fingerprint(proc / "references" / model_id / "fingerprint_L1.json")
    var = load_fingerprint(proc / "variants" / variant_id / "fingerprint_L1.json")
    frames = []
    for pid in protocols:
        for role, fp in (("reference", ref), ("variant", var)):
            run_id = fp.run_ids.get(pid)
            tr = _load_trace(campaign, run_id, pid) if run_id else None
            if tr is None:
                return None
            step = max(1, len(tr.t_ms) // 20000)          # plotting only; stored data are untouched
            frames.append(pd.DataFrame({"protocol_id": pid, "role": role, "t_ms": tr.t_ms[::step], "v_mV": tr.v_mV[::step]}))
    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------------------------------- main entry points
def analyze_campaign(campaign: str, n_boot: int = 2000, n_perm: int = 2000, draws: int | None = None) -> Path:
    from neuraxis.analysis import bootstrap, figures, metrics
    from neuraxis.selection import greedy
    from neuraxis.selection.matrix import DetectionMatrix

    cfg = config.study()
    figures.set_designation(config.designation_text(cfg))
    seed = int(cfg["selection"]["seed"])
    draws = int(draws or min(int(cfg["selection"]["random_draws"]), 5000))
    proc, tables, figs = _paths(campaign)
    from neuraxis.experiments import strata

    cls = pd.read_csv(proc / "classification.csv")
    if "stratum" not in cls:                 # campaigns aggregated before the semantic/numerical split (D-030)
        cls["stratum"] = [strata.stratum(k, "" if pd.isna(f) else str(f), "" if pd.isna(o) else str(o))
                          for k, f, o in zip(cls["kind"], cls["family"], cls["operator"])]
    # Primary tables and figures cover the semantic stratum only; numerical stress tests are analysed separately.
    mut = cls[(cls["kind"] == "mutant") & (cls["stratum"] == strata.SEMANTIC)]
    summary: dict[str, Any] = {"campaign": campaign, "created_utc": utc_now(), "in_sample_note": __doc__.split("\n\n")[1],
                               "classes": dict(Counter(cls["class"]))}
    made: list[str] = []

    casc = metrics.validation_cascade(mut["class"].tolist())
    casc.to_csv(tables / "validation_cascade.csv", index=False)
    made += [str(p) for p in figures.fig2_validation_cascade(casc, figs / "fig2_validation_cascade", battery="exhaustive battery")]

    m_all = DetectionMatrix.from_csv(proc / "detection_matrix.csv")
    m = m_all.take_rows([i for i, mid in enumerate(m_all.mutant_ids) if m_all.family_of[mid] in strata.SEMANTIC_FAMILIES])
    summary["n_admissible_mutants"] = m.n_mutants
    summary["n_non_semantic_rows_excluded_from_primary_matrix"] = m_all.n_mutants - m.n_mutants
    if m.n_mutants:
        long = pd.DataFrame([{"mutant_id": mid, "model_id": m.model_of[mid], "family": m.family_of[mid], "protocol_id": pid,
                              "detected": bool(m.detected[i, j])}
                             for i, mid in enumerate(m.mutant_ids) for j, pid in enumerate(m.protocol_ids)])
        long.to_csv(tables / "detection_long.csv", index=False)
        made += [str(p) for p in figures.fig3_detection_heatmap(long, figs / "fig3_detection_heatmap", m.protocol_ids)]

        battery = [p for p in m.protocol_ids if p != CANONICAL_ID]
        order = greedy.greedy_max_coverage(m, len(battery), battery).protocols
        cc = metrics.coverage_curve(m.detected[:, m.column_indices(battery)], battery, order, cost=m.cost)
        cc.to_csv(tables / "coverage_curve_in_sample_greedy.csv", index=False)
        curves = [{"strategy": "selected", "n_protocols": r.n_protocols, "cost": r.cumulative_cost, "detection_rate": r.detection_rate}
                  for r in cc.itertuples() if r.n_protocols > 0]
        curves.append({"strategy": "canonical", "n_protocols": 1, "cost": m.cost[CANONICAL_ID], "detection_rate": m.rate([CANONICAL_ID])})
        curves.append({"strategy": "exhaustive", "n_protocols": len(m.protocol_ids), "cost": m.total_cost(m.protocol_ids),
                       "detection_rate": m.rate(m.protocol_ids)})
        for k in range(1, len(battery) + 1):
            curves.append(metrics.summarize_draws(greedy.random_count_matched(m, k, draws, seed + k, battery),
                                                  "random_count_matched", n_protocols=k))
        for r in cc.itertuples():
            if r.n_protocols > 0:
                curves.append(metrics.summarize_draws(
                    greedy.random_runtime_matched(m, float(r.cumulative_cost), draws, seed + 1000 + int(r.n_protocols), battery),
                    "random_runtime_matched", cost=float(r.cumulative_cost)))
        curves_df = pd.DataFrame(curves)
        curves_df.to_csv(tables / "efficiency_curves_in_sample.csv", index=False)
        made += [str(p) for p in figures.fig4_efficiency_curve(curves_df, figs / "fig4_efficiency_curve")]

        can = m.covered([CANONICAL_ID])
        bat = m.covered(battery)
        clusters = [m.model_of[i] for i in m.mutant_ids]
        fams = [m.family_of[i] for i in m.mutant_ids]
        fam = metrics.by_family({"canonical": can, "battery_excluding_canonical": bat}, fams, clusters)
        fam.to_csv(tables / "detection_by_family.csv", index=False)
        summary["paired_battery_vs_canonical_in_sample"] = bootstrap.paired_comparison(bat, can, clusters, n_boot, n_perm, seed)

    fp = pd.read_csv(proc / "false_positives.csv") if (proc / "false_positives.csv").is_file() else pd.DataFrame()
    recl = reclassify(campaign, list(config.tolerances()["sensitivity_multipliers"]))
    recl.to_csv(tables / "reclassification_by_tolerance.csv", index=False)
    sens, notes = tolerance_sensitivity(recl)
    sens.to_csv(tables / "tolerance_sensitivity.csv", index=False)
    summary["tolerance_sensitivity_not_evaluable"] = notes
    if len(fp) and len(sens):
        rows = []
        for op, g in fp.groupby("operator"):
            k, n = int(g["false_positive"].astype(bool).sum()), int(len(g))
            lo, hi = metrics.proportion_ci(k, n)
            rows.append({"category": op, "n": n, "n_detected": k, "rate": k / n, "ci_low": lo, "ci_high": hi})
        fp_cat = pd.DataFrame(rows)
        fp_cat.to_csv(tables / "false_positives_by_transform.csv", index=False)
        summary["false_positives"] = metrics.false_positive_summary(fp["false_positive"].astype(bool).to_numpy(),
                                                                    fp["model_id"].tolist())
        made += [str(p) for p in figures.fig6_false_positives(fp_cat, sens, figs / "fig6_false_positives")]

    silent = cls[(cls["class"] == MutantClass.SILENT.value) & (cls["stratum"] == strata.SEMANTIC)]
    cases = []
    for r in silent.head(3).itertuples():
        det = [p for p in str(r.detecting_protocols).split(";") if p and p != CANONICAL_ID]
        if not det:
            continue
        tr = case_traces(campaign, r.variant_id, r.model_id, [CANONICAL_ID, det[0]])
        if tr is None:
            continue
        tr.insert(0, "case_id", r.variant_id)
        tr["case_label"] = f"{r.operator} {r.params}"
        cases.append(tr)
    if cases:
        made += [str(p) for p in figures.fig1_concept(cases[0].drop(columns=["case_id", "case_label"]), figs / "fig1_concept")]
        made += [str(p) for p in figures.fig7_case_studies(pd.concat(cases, ignore_index=True), figs / "fig7_case_studies")]
    else:
        summary["case_study_note"] = ("no silent mutant with locally stored traces; figures 1 and 7 not drawn "
                                      "(raw traces are Git-ignored and can be regenerated by re-running the campaign)")
    summary["figures"] = sorted({Path(p).relative_to(REPO_ROOT).as_posix() for p in made})
    out = proc / "analysis_summary.json"
    out.write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    return out


def reproduce_paper(campaign: str) -> Path:
    """Verify raw-record integrity, re-derive classifications from saved fingerprints, rebuild outputs."""
    proc = config.results_dir() / "processed" / campaign
    raw = config.results_dir() / "raw" / campaign
    report: dict[str, Any] = {"campaign": campaign, "created_utc": utc_now(), "runs": 0, "trace_files_verified": 0,
                              "trace_files_missing": 0, "feature_files_verified": 0, "integrity_errors": []}
    for rj in sorted(raw.glob("r-*/run.json")):
        rec = json.loads(rj.read_text(encoding="utf-8"))
        report["runs"] += 1
        npz = rj.parent / "traces.npz"
        if npz.is_file():
            if sha256_file(npz) != rec["trace_sha256"]:
                report["integrity_errors"].append(f"trace hash mismatch {rec['run_id']}")
            else:
                report["trace_files_verified"] += 1
        elif rec["trace_sha256"]:
            report["trace_files_missing"] += 1
        fpath = REPO_ROOT / rec["feature_path"] if rec.get("feature_path") else None
        if fpath is not None and fpath.is_file():
            if sha256_file(fpath) != rec["feature_sha256"]:
                report["integrity_errors"].append(f"feature file hash mismatch {rec['run_id']}")
            else:
                report["feature_files_verified"] += 1
    recl = reclassify(campaign, [1.0])
    cls = pd.read_csv(proc / "classification.csv").set_index("variant_id")["class"]
    mism = [(v, cls[v], c) for v, c in zip(recl["variant_id"], recl["class"]) if c not in ("not_run",) and cls[v] != c]
    report["classification_mismatches"] = mism
    report["analysis_summary"] = str(analyze_campaign(campaign).relative_to(REPO_ROOT).as_posix())
    report["ok"] = not report["integrity_errors"] and not mism
    out = proc / "reproduction_report.json"
    out.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    return out
