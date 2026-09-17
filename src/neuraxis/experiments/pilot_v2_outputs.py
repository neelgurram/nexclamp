"""Prespecified Pilot 2 outputs and branch classification (docs/PILOT2_PROTOCOL.md sections 9-10).

Reads a finished campaign run with ``validation_levels.enabled``. It simulates nothing and changes no
threshold, exclusion or class. Validation levels:
- A basic validation;
- B canonical feature regression;
- C canonical full-trace regression;
- D multi-protocol perturbation testing;
- E full candidate battery.

B and C are always kept separate. Every table carries the study metadata columns.
"""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from neuraxis.experiments import pilot_outputs as po
from neuraxis.experiments import strata

LEVELS = ("A_basic_pass", "B_canonical_feature", "C_canonical_trace", "D_multi_protocol", "E_full_battery")
BRANCH_RULES: dict[str, Any] = {  # prespecified before Pilot 2 data (PILOT2_PROTOCOL section 10)
    "control_false_positive_rate_max": 0.10,
    "unconfirmed_survivor_fraction_max": 0.50,
    "refinement_excluded_fraction_max": 0.25,
    "hidden_drift_min_confirmed_full_trace_survivors": 2,
    "hidden_drift_min_models": 2,
    "feature_insufficiency_min_cases": 2,
    "canonical_adequacy_min_detection": 0.95,
    "audit_sample_size": 20,
}


def _flag(r: Mapping[str, str], name: str) -> bool:
    return po.truthy(r.get(f"level_{name}", ""))


def _groups(c: po.CampaignView) -> list[tuple[str, Any]]:
    out = list(c.groups())
    for m in sorted({r["model_id"] for r in c.cls}):
        for s, label in ((strata.SEMANTIC, "model_mutants"), (strata.CONTROL, "harmless_controls"),
                         (strata.NUMERICAL, "numerical_stress_tests")):
            out.append((f"{label}__model__{m}", lambda r, s=s, m=m: c.stratum(r) == s and r["model_id"] == m))
    return out


def level_counts(c: po.CampaignView) -> list[dict]:
    rows = []
    for name, pred in _groups(c):
        sel = [r for r in c.cls if pred(r)]
        if not sel:
            continue
        rows.append({"group": name, "n_generated": len(sel), **{lv: sum(_flag(r, lv) for r in sel) for lv in LEVELS},
                     "feature_level_canonical_survivors": sum(_flag(r, "feature_level_canonical_survivor") for r in sel),
                     "full_trace_canonical_survivors": sum(_flag(r, "full_trace_canonical_survivor") for r in sel),
                     "feature_survivors_confirmed_h4": sum(po.truthy(r.get("survivor_confirmed_h4")) for r in sel),
                     "full_trace_survivors_confirmed_h4": sum(po.truthy(r.get("full_trace_survivor_confirmed_h4"))
                                                              for r in sel)})
    return rows


def _rows(c: po.CampaignView, pred) -> list[dict]:
    return [r for r in c.cls if pred(r)]


def case_table(c: po.CampaignView, rows: Sequence[Mapping[str, str]], checks: Mapping[str, Any]) -> list[dict]:
    out = []
    for r in rows:
        base = c.base(r)
        out.append({**base, "analysis_family": r.get("analysis_family", ""), "severity": r.get("severity", ""),
                    **{lv: _flag(r, lv) for lv in LEVELS},
                    "trace_reproducible": r.get("trace_reproducible", ""),
                    "secondary_reproducible": r.get("secondary_reproducible", ""),
                    "survivor_confirmed_h4": r.get("survivor_confirmed_h4", ""),
                    "full_trace_survivor_confirmed_h4": r.get("full_trace_survivor_confirmed_h4", ""),
                    "h4_check": json.dumps(checks.get(r["variant_id"], {}))})
    return out


def rates_by(c: po.CampaignView, key: str) -> list[dict]:
    groups: dict[tuple, list] = defaultdict(list)
    for r in c.cls:
        if c.stratum(r) == strata.SEMANTIC:
            groups[tuple(r.get(k, "") for k in key.split("+"))].append(r)
    out = []
    for k, rs in sorted(groups.items()):
        adm = [r for r in rs if _flag(r, "E_full_battery") and _flag(r, "A_basic_pass")]
        row = dict(zip(key.split("+"), k))
        row.update({"n_generated": len(rs), "n_basic_pass": sum(_flag(r, "A_basic_pass") for r in rs),
                    "n_E_admissible": len(adm)})
        for lv in LEVELS[1:4]:
            row[f"{lv}_detected"] = sum(_flag(r, lv) for r in adm)
            row[f"{lv}_rate"] = (row[f"{lv}_detected"] / len(adm)) if adm else None
        row["canonical_B_or_C_rate"] = (sum(_flag(r, "B_canonical_feature") or _flag(r, "C_canonical_trace")
                                            for r in adm) / len(adm)) if adm else None
        out.append(row)
    return out


def complete_matrix(c: po.CampaignView, trace_rep: Mapping[str, set]) -> list[dict]:
    cols = sorted({f"{p}:feature_primary" for p in c.protocols} | {f"{p}:feature_secondary" for p in c.protocols}
                  | {f"{p}:trace" for p in c.protocols if p != "P03_rheobase"})
    rows = []
    for r in c.cls:
        vid = r["variant_id"]
        stable = c.flags(r)["stable"]
        row = {k: v for k, v in c.base(r).items() if k not in ("params", "reproducible_primary")}
        row["analysis_family"], row["severity"] = r.get("analysis_family", ""), r.get("severity", "")
        prim = {p for p, _ in c.rep.get(vid, set())}
        sec = {p for p, _ in c.rep_sec.get(vid, set())}
        trc = {p for p, _ in trace_rep.get(vid, set())}
        for col in cols:
            p, m = col.split(":")
            hit = p in (prim if m == "feature_primary" else sec if m == "feature_secondary" else trc)
            row[col] = int(hit) if stable else "NA"
        rows.append(row)
    return rows


def trace_reproducible(processed: Path) -> dict[str, set]:
    rows = po.read_csv(processed / "detections_trace.csv")
    levels: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for d in rows:
        if "variant_id" in d and d.get("metric"):
            levels[d["variant_id"]][str(d["level_factor"])].add((d["protocol_id"], d["metric"]))
    return {v: lv.get("1", set()) & lv.get("2", set()) for v, lv in levels.items()}


def convergence_rows(processed: Path) -> list[dict]:
    out = []
    tol = po.read_csv(processed / "tolerances.csv")
    for m in sorted({t["model_id"] for t in tol if "model_id" in t}):
        mt = [t for t in tol if t.get("model_id") == m]
        out.append({"kind": "feature_tolerances", "model_id": m, "n_entries": len(mt),
                    **{f"limited_by_{k}": v for k, v in sorted(Counter(t["limiting"] for t in mt).items())}})
    for f in sorted((processed / "references").glob("*/trace_tolerances.json")):
        for pid, t in json.loads(f.read_text(encoding="utf-8")).items():
            out.append({"kind": "trace_tolerance", "model_id": t["model_id"], "protocol_id": pid, "status": t["status"],
                        "ref_spike_count": t["ref_spike_count"], "ref_rmse_h_h2": t["ref_rmse_h_h2"],
                        "ref_max_shift_h_h2": t["ref_max_shift_h_h2"], "tau_rmse": t["tau_rmse"],
                        "tau_shift": t["tau_shift"]})
    return out


def unique_protocol_contribution(c: po.CampaignView, trace_rep: Mapping[str, set]) -> list[dict]:
    """Per protocol: the admissible primary-semantic mutants that **only** it detected.

    A variant counts for a protocol when that protocol is the single protocol with a reproducible
    detection of it, by a primary feature or by full-trace regression. Secondary features are
    reported separately and never enter this table.
    """
    detectors: dict[str, set[str]] = defaultdict(set)
    for r in c.cls:
        if c.stratum(r) != strata.SEMANTIC or r["kind"] != "mutant" or not c.flags(r)["admissible"]:
            continue
        vid = r["variant_id"]
        prot = {p for p, _ in c.rep.get(vid, set())} | {p for p, _ in trace_rep.get(vid, set())}
        if len(prot) == 1:
            detectors[next(iter(prot))].add(vid)
    rows = []
    for pid in c.protocols:
        only = sorted(detectors.get(pid, set()))
        rows.append({"protocol_id": pid, "is_canonical": pid == po.CANONICAL_ID,
                     "n_detected_only_by_this_protocol": len(only),
                     "models": ";".join(sorted({c.by_id[v]["model_id"] for v in only})),
                     "analysis_families": ";".join(sorted({c.by_id[v].get("analysis_family", "") for v in only})),
                     "variant_ids": ";".join(only)})
    return rows


def kinetics_atomic_vs_compound(c: po.CampaignView, trace_rep: Mapping[str, set],
                                checks: Mapping[str, Any]) -> list[dict]:
    """Kinetics variants split into atomic and compound edits; the two are never pooled.

    Atomic: one rate expression of one gate. Compound: several expressions of one gate, or a
    channel-level shift. The split comes from the recorded edits in ``mutation_manifest.csv``.
    """
    edits = {r["variant_id"]: r.get("edits", "") for r in po.read_csv(c.processed / "mutation_manifest.csv")}
    rows = []
    for r in c.cls:
        if r.get("family") != "kinetics":
            continue
        vid = r["variant_id"]
        try:
            n_edits = len(json.loads(edits.get(vid) or "[]"))
        except (ValueError, TypeError):
            n_edits = 0
        kind = "atomic" if n_edits == 1 else ("compound" if n_edits > 1 else "unrecorded")
        rows.append({**c.base(r), "analysis_family": r.get("analysis_family", ""), "severity": r.get("severity", ""),
                     "edit_kind": kind, "n_edits": n_edits,
                     **{lv: _flag(r, lv) for lv in LEVELS},
                     "reproducible_trace": ";".join(sorted(f"{p}:{m}" for p, m in trace_rep.get(vid, set()))),
                     "survivor_confirmed_h4": checks.get(vid, {}).get("confirmed", ""),
                     "note": "atomic and compound kinetics results are reported separately, never pooled"})
    return rows


def uncertain_cases(c: po.CampaignView, trace_rep: Mapping[str, set], checks: Mapping[str, Any]) -> list[dict]:
    """Cases that must not be forced into a class, listed explicitly with the reason."""
    rows = []
    for r in c.cls:
        vid, reasons = r["variant_id"], []
        f = c.flags(r)
        if r["kind"] == "mutant" and not f["stable"]:
            reasons.append(f"not analysable: class {r['class']}")
        if po.truthy(r.get("canonical_runs_but_battery_failed")):
            reasons.append("canonical ran but the battery failed (split fate)")
        if _flag(r, "feature_level_canonical_survivor") and not po.truthy(r.get("survivor_confirmed_h4")):
            reasons.append("apparent canonical survivor not confirmed at h/4")
        if int(r.get("n_detections_h") or 0) and not (c.rep.get(vid) or trace_rep.get(vid)):
            reasons.append("detected at h but not reproduced at h/2")
        if c.stratum(r) == strata.CONTROL and f["admissible"]:
            reasons.append("valid transformation classified non-equivalent (false positive)")
        if reasons:
            rows.append({**c.base(r), "analysis_family": r.get("analysis_family", ""),
                         "severity": r.get("severity", ""), "uncertainty": "; ".join(reasons),
                         "refinement_check": json.dumps(checks.get(vid, {}), default=str)})
    return rows


def classify_branch(c: po.CampaignView, processed: Path, rules: Mapping[str, Any] = BRANCH_RULES) -> dict:
    sem = [r for r in c.cls if c.stratum(r) == strata.SEMANTIC and r["kind"] == "mutant"]
    ctl = [r for r in c.cls if c.stratum(r) == strata.CONTROL]
    adm = [r for r in sem if _flag(r, "A_basic_pass") and _flag(r, "E_full_battery")]
    fp = [r for r in ctl if _flag(r, "E_full_battery")]
    broken_controls = [r for r in ctl if not _flag(r, "A_basic_pass")]
    feat_surv = [r for r in sem if _flag(r, "feature_level_canonical_survivor")]
    unconfirmed = [r for r in feat_surv if not po.truthy(r.get("survivor_confirmed_h4"))]
    full_conf = [r for r in sem if _flag(r, "full_trace_canonical_survivor")
                 and po.truthy(r.get("full_trace_survivor_confirmed_h4"))]
    feat_insuff = [r for r in feat_surv if _flag(r, "C_canonical_trace") and po.truthy(r.get("survivor_confirmed_h4"))]
    tol = po.read_csv(processed / "tolerances.csv")
    excluded = [t for t in tol if t.get("limiting") in ("excluded_definedness", "excluded_regime")]
    canon = sum(_flag(r, "B_canonical_feature") or _flag(r, "C_canonical_trace") for r in adm)
    ev = {"n_semantic_mutants": len(sem), "n_E_admissible": len(adm), "n_controls": len(ctl),
          "control_false_positives": len(fp), "control_false_positive_rate": len(fp) / len(ctl) if ctl else None,
          "controls_not_passing_basic_validation": len(broken_controls),
          "feature_level_survivors": len(feat_surv), "feature_survivors_unconfirmed_h4": len(unconfirmed),
          "confirmed_full_trace_survivors": len(full_conf),
          "confirmed_full_trace_survivor_models": sorted({r["model_id"] for r in full_conf}),
          "feature_survivors_detected_by_canonical_trace": len(feat_insuff),
          "refinement_excluded_fraction": len(excluded) / len(tol) if tol else None,
          "canonical_B_or_C_detection_rate": canon / len(adm) if adm else None}
    flags = {
        "D_pipeline_uncertainty": bool(
            (ev["control_false_positive_rate"] or 0) > rules["control_false_positive_rate_max"]
            or broken_controls
            or (feat_surv and len(unconfirmed) / len(feat_surv) > rules["unconfirmed_survivor_fraction_max"])
            or (ev["refinement_excluded_fraction"] or 0) >= rules["refinement_excluded_fraction_max"]),
        "A_hidden_drift_supported": (len(full_conf) >= int(rules["hidden_drift_min_confirmed_full_trace_survivors"])
                                     and len(set(r["model_id"] for r in full_conf)) >= int(rules["hidden_drift_min_models"])),
        "B_feature_level_insufficiency": len(feat_insuff) >= int(rules["feature_insufficiency_min_cases"]),
        "C_canonical_adequacy": (ev["canonical_B_or_C_detection_rate"] is not None
                                 and ev["canonical_B_or_C_detection_rate"] >= rules["canonical_adequacy_min_detection"]),
    }
    order = ["D_pipeline_uncertainty", "A_hidden_drift_supported", "B_feature_level_insufficiency", "C_canonical_adequacy"]
    primary = next((k for k in order if flags[k]), "indeterminate")
    return {"primary_branch": primary, "flags": flags, "evidence": ev, "rules": dict(rules),
            "precedence": order + ["indeterminate"],
            "note": "Rules fixed in PILOT2_PROTOCOL before data; branch A is never forced."}


def build(processed: Path, raw_dir: Path, work_variants_dir: Path, work_runs_dir: Path, figures_dir: Path,
          meta: Mapping[str, str], seed: int, deviations_file: Path | None = None) -> Path:
    meta = dict(meta)
    c = po.CampaignView(processed, [], [])
    out = Path(processed) / "pilot_v2_outputs"
    t = lambda name, rows: po.write_table(out / name, rows, meta)  # noqa: E731
    checks = json.loads((processed / "survivor_checks.json").read_text(encoding="utf-8")) \
        if (processed / "survivor_checks.json").is_file() else {}
    trace_rep = trace_reproducible(processed)
    sem = lambda r: c.stratum(r) == strata.SEMANTIC and r["kind"] == "mutant"  # noqa: E731
    ctl = lambda r: c.stratum(r) == strata.CONTROL  # noqa: E731

    t("01_validation_level_counts.csv", level_counts(c))
    feat_surv = _rows(c, lambda r: sem(r) and _flag(r, "feature_level_canonical_survivor"))
    t("02_feature_level_canonical_survivors.csv", case_table(c, feat_surv, checks))
    t("03_full_trace_canonical_survivors.csv",
      case_table(c, _rows(c, lambda r: sem(r) and _flag(r, "full_trace_canonical_survivor")), checks))
    t("04_multi_protocol_detections.csv", case_table(c, _rows(c, lambda r: sem(r) and _flag(r, "D_multi_protocol")), checks))
    t("05_detection_by_model.csv", rates_by(c, "model_id"))
    t("06_detection_by_family.csv", rates_by(c, "analysis_family"))
    t("06_detection_by_family_and_severity.csv", rates_by(c, "analysis_family+severity"))
    t("07_valid_transformation_false_positives.csv",
      case_table(c, _rows(c, lambda r: ctl(r) and _flag(r, "E_full_battery")), checks))
    t("08_convergence.csv", convergence_rows(processed))
    t("08_survivor_refinement_checks.csv", [{"variant_id": k, **{kk: json.dumps(vv) if isinstance(vv, list) else vv
                                                                   for kk, vv in v.items()}} for k, v in checks.items()])
    status_rows, time_rows, failures, prov = po.runtime_rows(c, raw_dir, work_runs_dir)
    t("09_run_status_counts.csv", status_rows)
    t("09_runtime.csv", time_rows)
    t("09_failed_runs.csv", failures)
    t("10_detection_matrix_complete.csv", complete_matrix(c, trace_rep))
    rng = random.Random(seed)
    pool = sorted(r["variant_id"] for r in c.cls)
    sample = set(rng.sample(pool, min(int(BRANCH_RULES["audit_sample_size"]), len(pool))))
    audit = {r["variant_id"]: r for r in po.audit_rows(c, work_variants_dir)}
    t("11_random_audit_cases.csv", [{**case_table(c, [c.by_id[v]], checks)[0],
                                     **{k: audit.get(v, {}).get(k, "") for k in
                                        ("edits", "exec_overrides", "automated_single_documented_change_check",
                                         "automated_identical_numerics_check")},
                                     "ai_assisted_review": "", "human_audit_status": "pending"}
                                    for v in sorted(sample)])
    t("12_canonical_survival_cases.csv", case_table(c, feat_surv, checks))
    plots = po.plot_cases(c, [{**c.base(r)} for r in feat_surv], raw_dir, Path(figures_dir) / "canonical_survivors",
                          " | ".join(f"{k}: {v}" for k, v in meta.items()))
    t("12_canonical_survival_trace_plots.csv", plots)
    failed_ctl = _rows(c, lambda r: ctl(r) and (_flag(r, "E_full_battery") or not _flag(r, "A_basic_pass")))
    t("13_failed_valid_transformations.csv", case_table(c, failed_ctl, checks))
    t("14_unique_protocol_contribution.csv", unique_protocol_contribution(c, trace_rep))
    t("15_kinetics_atomic_vs_compound.csv", kinetics_atomic_vs_compound(c, trace_rep, checks))
    t("16_uncertain_cases.csv", uncertain_cases(c, trace_rep, checks))
    branch = classify_branch(c, processed)
    deviations = (Path(deviations_file).read_text(encoding="utf-8").strip()
                  if deviations_file and Path(deviations_file).is_file() else "No deviation log file found.")
    summary = {"study_metadata": meta, "branch": branch, "provenance": prov, "audit_sample": sorted(sample),
               "reporting": {"findings": "exploratory (development pilot); none confirmatory",
                             "analyses_prespecified": "yes: PILOT2_PROTOCOL sections 9-10, fixed before data",
                             "deviations": deviations}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    return out
