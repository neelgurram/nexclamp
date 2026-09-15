"""Prespecified pilot outputs (``docs/PILOT_PROTOCOL_V1.md``, section "Planned analyses").

Reads a finished campaign. It simulates nothing and changes no threshold, exclusion or
classification. Every table carries the study metadata columns; every plot carries the
designation footer. Narrative items (executive summary wording, the P05 assessment and the
continue / redesign / stop recommendation) are written by the researcher from these outputs.
"""

from __future__ import annotations

import csv
import json
import statistics
import tempfile
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from neurosem.experiments import strata
from neurosem.protocols.definitions import CANONICAL_ID
from neurosem.schemas import MutantClass

RHEOBASE_ID = "P03_rheobase"
P05 = "P05_long_step"
REPEATED = "repeated_pilot1_model"
NEW = "new_independent_source_model"
OTHER = "other_model"
ADMISSIBLE = (MutantClass.NON_EQUIVALENT.value, MutantClass.SILENT.value)
NOT_EXECUTABLE = (MutantClass.STRUCTURALLY_INVALID.value, MutantClass.NON_EXECUTABLE.value)
NOT_STABLE = (*NOT_EXECUTABLE, MutantClass.NUMERICALLY_UNSTABLE.value)


# --------------------------------------------------------------------------- io
def read_csv(path: Path) -> list[dict[str, str]]:
    if not Path(path).is_file():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def truthy(x: Any) -> bool:
    return str(x).strip().lower() in ("true", "1", "yes")


def split_list(s: Any) -> list[str]:
    return [x for x in str(s or "").split(";") if x]


def write_table(path: Path, rows: Sequence[Mapping[str, Any]], meta: Mapping[str, str]) -> Path:
    """CSV with the study metadata as leading columns; an empty table keeps one metadata row."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stamped = [{**meta, **r} for r in rows] if rows else [{**meta, "rows": 0}]
    names = list(dict.fromkeys(k for r in stamped for k in r))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        w.writeheader()
        for r in stamped:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    return path


def reproducible_keys(rows: Sequence[Mapping[str, str]]) -> dict[str, set[tuple[str, str]]]:
    """variant_id -> (protocol, feature) detected at h AND h/2 (the classification rule)."""
    levels: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for d in rows:
        levels[d["variant_id"]][str(d["level_factor"])].add((d["protocol_id"], d["feature"]))
    return {v: lv.get("1", set()) & lv.get("2", set()) for v, lv in levels.items()}


# --------------------------------------------------------------------------- campaign view
class CampaignView:
    def __init__(self, processed: Path, repeated: Sequence[str], new: Sequence[str]) -> None:
        self.processed = Path(processed)
        self.cls = read_csv(self.processed / "classification.csv")
        if not self.cls:
            raise FileNotFoundError(f"{self.processed / 'classification.csv'} missing or empty")
        self.by_id = {r["variant_id"]: r for r in self.cls}
        self.det = read_csv(self.processed / "detections.csv")
        self.sec = read_csv(self.processed / "detections_secondary.csv")
        self.rep = reproducible_keys(self.det)
        self.rep_sec = reproducible_keys(self.sec)
        self.repeated, self.new = set(repeated), set(new)
        costs = read_csv(self.processed / "protocol_costs.csv")
        self.protocols = [r["protocol_id"] for r in costs] or sorted({d["protocol_id"] for d in self.det})
        self.battery = [p for p in self.protocols if p != CANONICAL_ID]

    def model_set(self, model_id: str) -> str:
        return REPEATED if model_id in self.repeated else NEW if model_id in self.new else OTHER

    @staticmethod
    def stratum(r: Mapping[str, str]) -> str:
        return r.get("stratum") or strata.stratum(r["kind"], r.get("family", ""), r.get("operator", ""))

    def flags(self, r: Mapping[str, str]) -> dict[str, bool]:
        k = r["class"]
        admissible = k in ADMISSIBLE
        dprot = split_list(r.get("detecting_protocols"))
        return {"valid": truthy(r.get("structural_valid")), "executable": k not in NOT_EXECUTABLE,
                "stable": k not in NOT_STABLE, "equivalent": k == MutantClass.EQUIVALENT.value,
                "admissible": admissible, "canonical": admissible and CANONICAL_ID in dprot,
                "battery": admissible and any(p != CANONICAL_ID for p in dprot)}

    def base(self, r: Mapping[str, str]) -> dict[str, Any]:
        return {"variant_id": r["variant_id"], "model_id": r["model_id"], "model_set": self.model_set(r["model_id"]),
                "stratum": self.stratum(r), "kind": r["kind"], "family": r.get("family", ""),
                "operator": r.get("operator", ""), "params": r.get("params", ""), "class": r["class"],
                "interpretation": r.get("interpretation", ""), "detecting_protocols": r.get("detecting_protocols", ""),
                "reproducible_primary": ";".join(sorted(f"{p}:{f}" for p, f in self.rep.get(r["variant_id"], set())))}

    def groups(self) -> list[tuple[str, Callable[[Mapping[str, str]], bool]]]:
        def pred(s: str, mset: str | None) -> Callable[[Mapping[str, str]], bool]:
            return lambda r: self.stratum(r) == s and (mset is None or self.model_set(r["model_id"]) == mset)

        out = []
        for s, label in ((strata.SEMANTIC, "model_mutants"), (strata.NUMERICAL, "numerical_stress_tests"),
                         (strata.CONTROL, "harmless_controls")):
            out += [(f"{label}__all_models", pred(s, None)), (f"{label}__repeated_pilot1_models", pred(s, REPEATED)),
                    (f"{label}__new_independent_source_models", pred(s, NEW))]
        return out


# --------------------------------------------------------------------------- 2-3 flow and group results
def flow_rows(c: CampaignView) -> list[dict[str, Any]]:
    rows = []
    for name, pred in c.groups():
        f = [c.flags(r) for r in c.cls if pred(r)]
        st = [x for x in f if x["stable"]]
        rows.append({
            "group": name, "generated": len(f), "structurally_valid": sum(x["valid"] for x in f),
            "executable": sum(x["executable"] for x in f), "numerically_stable": len(st),
            "equivalent_within_tested_domain": sum(x["equivalent"] for x in f),
            "non_equivalent_reproducible": sum(x["admissible"] for x in f),
            "canonical_detected": sum(x["canonical"] for x in st), "canonical_undetected": sum(not x["canonical"] for x in st),
            "battery_detected": sum(x["battery"] for x in st), "battery_undetected": sum(not x["battery"] for x in st),
            "both_detected": sum(x["canonical"] and x["battery"] for x in st),
            "canonical_only": sum(x["canonical"] and not x["battery"] for x in st),
            "battery_only": sum(x["battery"] and not x["canonical"] for x in st),
            "neither": sum(not x["canonical"] and not x["battery"] for x in st),
        })
    return rows


def class_rows(c: CampaignView) -> tuple[list[dict], list[dict]]:
    by_group = [{"group": name, "class": k, "count": n}
                for name, pred in c.groups() for k, n in sorted(Counter(r["class"] for r in c.cls if pred(r)).items())]
    per_model = [{"model_id": m, "model_set": c.model_set(m), "stratum": s, "class": k, "count": n}
                 for (m, s, k), n in sorted(Counter((r["model_id"], c.stratum(r), r["class"]) for r in c.cls).items())]
    return by_group, per_model


# --------------------------------------------------------------------------- 4 case lists
def case_rows(c: CampaignView) -> dict[str, list[dict]]:
    canon_pass_battery_detect, canon_detect_battery_miss, control_triggers, secondary_miss = [], [], [], []
    numerical_canon_pass = []
    dets_by = defaultdict(list)
    for d in c.det:
        dets_by[d["variant_id"]].append(d)
    for r in c.cls:
        f = c.flags(r)
        mutant = r["kind"] == "mutant"
        semantic = mutant and c.stratum(r) == strata.SEMANTIC        # model mutations only; numerical kept apart
        if semantic and f["admissible"] and f["battery"] and not f["canonical"]:
            canon_pass_battery_detect.append(c.base(r))
        if semantic and f["admissible"] and f["canonical"] and not f["battery"]:
            canon_detect_battery_miss.append(c.base(r))
        if mutant and c.stratum(r) == strata.NUMERICAL and f["admissible"] and f["battery"] and not f["canonical"]:
            numerical_canon_pass.append(c.base(r))
        if not mutant and dets_by.get(r["variant_id"]):
            ds = dets_by[r["variant_id"]]
            control_triggers.append({**c.base(r), "levels": ";".join(sorted({str(d["level_factor"]) for d in ds})),
                                     "primary_detections": ";".join(sorted({f"{d['protocol_id']}:{d['feature']}@L"
                                                                            f"{d['level_factor']}" for d in ds})),
                                     "reproducible_false_positive": f["admissible"]})
        sec = c.rep_sec.get(r["variant_id"], set())
        if sec:
            primary_protocols = set(split_list(r.get("detecting_protocols")))
            only_secondary = sorted({p for p, _ in sec} - primary_protocols)
            primary_equivalent = mutant and f["equivalent"]
            if primary_equivalent or only_secondary or not mutant:
                secondary_miss.append({**c.base(r), "secondary_reproducible": ";".join(sorted(f"{p}:{x}" for p, x in sec)),
                                       "primary_class_equivalent_but_secondary_detected": primary_equivalent,
                                       "protocols_detecting_only_via_secondary": ";".join(only_secondary),
                                       "canonical_secondary_only": CANONICAL_ID in only_secondary,
                                       "is_control": not mutant})
    return {"canonical_passed_battery_detected": canon_pass_battery_detect,
            "canonical_detected_battery_missed": canon_detect_battery_miss,
            "control_primary_feature_triggers": control_triggers,
            "secondary_detected_primary_missed": secondary_miss,
            "numerical_stress_canonical_passed_battery_detected_not_semantic_drift": numerical_canon_pass}


# --------------------------------------------------------------------------- 5-6 matrices
def protocol_matrix(c: CampaignView, kinds: Callable[[Mapping[str, str]], bool]) -> list[dict]:
    rows = []
    for r in c.cls:
        if not kinds(r):
            continue
        keys = c.rep.get(r["variant_id"], set())
        stable = c.flags(r)["stable"]
        row = {k: v for k, v in c.base(r).items() if k not in ("params", "reproducible_primary")}
        for p in c.protocols:
            row[p] = int(any(pp == p for pp, _ in keys)) if stable else "NA"
        rows.append(row)
    return rows


def feature_matrix(c: CampaignView, kinds: Callable[[Mapping[str, str]], bool]) -> tuple[list[dict], list[dict]]:
    features = sorted({f for keys in (*c.rep.values(), *c.rep_sec.values()) for _, f in keys})
    wide, long = [], []
    for r in c.cls:
        if not kinds(r):
            continue
        vid = r["variant_id"]
        stable = c.flags(r)["stable"]
        row = {k: v for k, v in c.base(r).items() if k not in ("params", "reproducible_primary")}
        for feat in features:
            cells = sorted([f"primary:{p}" for p, f in c.rep.get(vid, set()) if f == feat] +
                           [f"secondary:{p}" for p, f in c.rep_sec.get(vid, set()) if f == feat])
            row[feat] = ";".join(cells) if stable else "NA"
        wide.append(row)
        for panel, keys in (("primary", c.rep.get(vid, set())), ("secondary", c.rep_sec.get(vid, set()))):
            long += [{"variant_id": vid, "model_id": r["model_id"], "stratum": c.stratum(r), "panel": panel,
                      "protocol_id": p, "feature": f} for p, f in sorted(keys)]
    return wide, long


# --------------------------------------------------------------------------- 7 trace plots
def plot_cases(c: CampaignView, cases: Sequence[Mapping[str, Any]], raw_dir: Path, out_dir: Path,
               designation: str) -> list[dict]:
    from matplotlib.figure import Figure

    from neurosem.features import trace_metrics
    from neurosem.validation.fingerprint import load_fingerprint

    index = []
    for case in cases:
        vid, mid = case["variant_id"], case["model_id"]
        protos = [CANONICAL_ID] + [p for p in split_list(case["detecting_protocols"]) if p not in (CANONICAL_ID, RHEOBASE_ID)]
        ref_f = c.processed / "references" / mid / "fingerprint_L1.json"
        var_f = c.processed / "variants" / vid / "fingerprint_L1.json"
        entry = {"variant_id": vid, "model_id": mid, "stratum": case["stratum"], "protocols": ";".join(protos)}
        if not (ref_f.is_file() and var_f.is_file()):
            index.append({**entry, "status": "fingerprint_missing", "plot": ""})
            continue
        fps = {"reference": load_fingerprint(ref_f), "variant": load_fingerprint(var_f)}
        traces: dict[tuple[str, str], Any] = {}
        missing = []
        for role, fp in fps.items():
            for pid in protos:
                run_id = fp.run_ids.get(pid)
                npz = Path(raw_dir) / str(run_id) / "traces.npz"
                tr = trace_metrics.unpack_traces(npz.read_bytes()).get(pid) if run_id and npz.is_file() else None
                if tr is None:
                    missing.append(f"{role}:{pid}")
                traces[(role, pid)] = tr
        if missing:
            index.append({**entry, "status": "trace_missing: " + ";".join(missing), "plot": ""})
            continue
        keys = c.rep.get(vid, set())
        fig = Figure(figsize=(8.0, 2.1 * len(protos) + 0.6))
        axes = fig.subplots(len(protos), 1, squeeze=False)
        for ax, pid in zip(axes[:, 0], protos):
            for role, style in (("reference", {"color": "#000000", "lw": 0.7}),
                                ("variant", {"color": "#E69F00", "lw": 0.7, "ls": "--"})):
                tr = traces[(role, pid)]
                step = max(1, len(tr.t_ms) // 20000)
                ax.plot(tr.t_ms[::step], tr.v_mV[::step], label=role, **style)
            feats = sorted(f for p, f in keys if p == pid)
            ax.set_title(f"{pid}: reproducible primary detections: {', '.join(feats) or 'none'}", fontsize=7)
            ax.set_ylabel("V (mV)", fontsize=7)
            ax.tick_params(labelsize=6)
        axes[-1, 0].set_xlabel("t (ms)", fontsize=7)
        axes[0, 0].legend(fontsize=6, loc="upper right")
        fig.suptitle(f"{vid} ({mid}; {case.get('operator', '')}; {case['stratum']})", fontsize=8)
        fig.text(0.005, 0.002, designation, fontsize=5, ha="left", va="bottom", color="#555555")
        fig.tight_layout(rect=(0, 0.02, 1, 0.97))
        out = Path(out_dir) / case["stratum"] / f"{vid}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, dpi=150)
        index.append({**entry, "status": "plotted", "plot": out.as_posix()})
    return index


# --------------------------------------------------------------------------- 8 convergence
def _f(x: Any) -> float | None:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v == v and v not in (float("inf"), float("-inf")) else None


def convergence_rows(c: CampaignView) -> list[dict]:
    by = defaultdict(list)
    for r in read_csv(c.processed / "numerical_robustness.csv"):
        if "variant_id" in r:
            by[r["variant_id"]].append(r)
    rows = []
    for vid, rs in sorted(by.items()):
        labels = Counter(r["label"] for r in rs)
        ratios = [x for x in (_f(r.get("deviation_over_ref_error_h")) for r in rs) if x is not None]
        triples = [(_f(r.get("deviation_h")), _f(r.get("deviation_h2")), _f(r.get("deviation_h4"))) for r in rs]
        full = [t for t in triples if None not in t]
        rows.append({"variant_id": vid, "model_id": rs[0].get("model_id", ""), "model_set": c.model_set(rs[0].get("model_id", "")),
                     "operator": rs[0].get("operator", ""), "exec_overrides": rs[0].get("exec_overrides", ""),
                     "class": c.by_id.get(vid, {}).get("class", ""), "n_protocol_feature_entries": len(rs),
                     **{f"n_{k}": v for k, v in sorted(labels.items())},
                     "median_deviation_over_ref_error_h": statistics.median(ratios) if ratios else None,
                     "max_deviation_over_ref_error_h": max(ratios) if ratios else None,
                     "n_entries_with_h_h2_h4": len(full),
                     "n_deviation_non_increasing_under_refinement": sum(1 for a, b, d in full if d <= b <= a)})
    return rows


# --------------------------------------------------------------------------- 9 runtime and failures
def runtime_rows(c: CampaignView, raw_dir: Path, work_runs_dir: Path) -> tuple[list[dict], list[dict], list[dict], dict]:
    status, runtime = Counter(), defaultdict(float)
    failures, commits, phases, dirty = [], Counter(), Counter(), 0
    for f in sorted(Path(raw_dir).glob("*/run.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        status[(j.get("run_kind"), j.get("status"))] += 1
        runtime[(j.get("model_id"), j.get("run_kind"))] += float(j.get("runtime_s") or 0.0)
        commits[j.get("git_commit")] += 1
        dirty += bool(j.get("git_dirty"))
        phases[(j.get("project_name", ""), j.get("study_phase", ""), j.get("protocol_version", ""))] += 1
        if j.get("status") != "ok":
            failures.append({"run_id": j.get("run_id"), "run_kind": j.get("run_kind"), "model_id": j.get("model_id"),
                             "variant_id": j.get("variant_id"), "status": j.get("status"),
                             "message": str(j.get("message", ""))[:300]})
    failed_dirs = sorted(p.name for p in (Path(work_runs_dir) / "failed").glob("*")) if work_runs_dir else []
    status_rows = [{"run_kind": k, "status": s, "n_runs": n} for (k, s), n in sorted(status.items(), key=str)]
    time_rows = [{"model_id": m, "model_set": c.model_set(str(m)), "run_kind": k, "simulator_runtime_s": round(t, 3)}
                 for (m, k), t in sorted(runtime.items(), key=str)]
    strat = defaultdict(float)
    for r in c.cls:
        strat[(c.stratum(r), c.model_set(r["model_id"]))] += _f(r.get("runtime_s")) or 0.0
    time_rows += [{"model_id": "", "model_set": ms, "run_kind": f"variant_total:{s}", "simulator_runtime_s": round(t, 3)}
                  for (s, ms), t in sorted(strat.items())]
    prov = {"run_records": sum(status.values()), "git_commits": dict(commits), "runs_with_dirty_tree": dirty,
            "metadata_combinations": {" | ".join(k): v for k, v in phases.items()}, "failed_run_scratch_dirs": failed_dirs}
    return status_rows, time_rows, failures, prov


# --------------------------------------------------------------------------- 10 audit sheet
def audit_rows(c: CampaignView, work_variants_dir: Path) -> list[dict]:
    from neurosem.models import load_models, materialize
    from neurosem.mutations import load_variant
    from neurosem.mutations.base import enforce_single_operator

    sheet = read_csv(c.processed / "mutant_audit_sheet.csv")
    models = None
    refs: dict[str, Any] = {}
    out = []
    with tempfile.TemporaryDirectory(prefix="neurosem_audit_") as tmp:
        for row in sheet:
            vid = row["variant_id"]
            cr = c.by_id.get(vid, {})
            mid = cr.get("model_id", "")
            vdir = Path(work_variants_dir) / "mutants" / mid / vid
            single = numerics = "not_checked"
            if not vdir.is_dir():
                single = "variant_workspace_missing"
            else:
                try:
                    models = models or load_models()
                    ws, rec = load_variant(vdir, models)
                    if mid not in refs:
                        refs[mid] = materialize(models[mid], Path(tmp) / mid)
                    enforce_single_operator(refs[mid], ws, rec)
                    single = "pass"
                    if c.stratum(cr) == strata.SEMANTIC:
                        strata.check_identical_numerics(rec)
                        numerics = "pass"
                    else:
                        numerics = "not_applicable (numerical stress test)"
                except Exception as exc:  # recorded, not raised: the audit reports every failure
                    msg = f"fail: {type(exc).__name__}: {exc}"[:400]
                    single = msg if single == "not_checked" else single
                    numerics = msg if single == "pass" else numerics
            out.append({"variant_id": vid, "model_id": mid, "model_set": c.model_set(mid), "stratum": c.stratum(cr) if cr else "",
                        **{k: v for k, v in row.items() if k != "variant_id"},
                        "automated_single_documented_change_check": single,
                        "automated_identical_numerics_check": numerics,
                        "ai_assisted_review": "", "human_audit_status": "pending (human audit not yet done)"})
    return out


# --------------------------------------------------------------------------- 11 P05 dominance
def p05_rows(c: CampaignView) -> tuple[list[dict], list[dict]]:
    per_protocol, summary = [], []
    subsets = (("all_models", None), ("repeated_pilot1_models", REPEATED), ("new_independent_source_models", NEW))
    for label, mset in subsets:
        adm = [r for r in c.cls if r["kind"] == "mutant" and c.stratum(r) == strata.SEMANTIC and r["class"] in ADMISSIBLE
               and (mset is None or c.model_set(r["model_id"]) == mset)]
        det = {p: {r["variant_id"] for r in adm if p in split_list(r.get("detecting_protocols"))} for p in c.battery}
        union = set().union(*det.values()) if det else set()
        p05 = det.get(P05, set())
        for p in c.battery:
            others = set().union(*(det[q] for q in c.battery if q != p)) if len(c.battery) > 1 else set()
            per_protocol.append({"subset": label, "protocol_id": p, "n_admissible_model_mutants": len(adm),
                                 "n_detected": len(det[p]), "n_detected_by_no_other_battery_protocol": len(det[p] - others),
                                 "detections_subset_of_P05": det[p] <= p05 if p != P05 else ""})
        order, covered = [], set()
        while True:
            gains = [(len(det[p] - covered), -c.battery.index(p), p) for p in c.battery if p not in order]
            if not gains or max(gains)[0] == 0:
                break
            _, _, best = max(gains)
            order.append(best)
            covered |= det[best]
        without = set().union(*(det[q] for q in c.battery if q != P05)) if c.battery else set()
        summary.append({"subset": label, "n_admissible_model_mutants": len(adm), "battery_union_detected": len(union),
                        "P05_detected": len(p05), "P05_share_of_battery_union": (len(p05) / len(union)) if union else None,
                        "detected_only_by_P05": len(p05 - without), "battery_union_without_P05": len(without),
                        "greedy_coverage_order": ";".join(order)})
    return per_protocol, summary


# --------------------------------------------------------------------------- driver
def build_outputs(processed: Path, raw_dir: Path, work_variants_dir: Path, work_runs_dir: Path | None, figures_dir: Path,
                  repeated: Sequence[str], new: Sequence[str], meta: Mapping[str, str],
                  deviations_file: Path | None = None) -> Path:
    meta = dict(meta)
    designation = " | ".join(f"{k}: {v}" for k, v in meta.items())
    c = CampaignView(processed, repeated, new)
    out = Path(processed) / "pilot_outputs"
    t = lambda name, rows: write_table(out / name, rows, meta)  # noqa: E731

    flow = flow_rows(c)
    t("02_flow_counts.csv", flow)
    by_group, per_model = class_rows(c)
    t("03_classes_by_group.csv", by_group)
    t("03_classes_by_model.csv", per_model)
    cases = case_rows(c)
    for i, (name, rows) in enumerate(cases.items(), start=1):
        t(f"04{chr(96 + i)}_{name}.csv", rows)
    t("05_protocol_by_mutant_matrix.csv", protocol_matrix(c, lambda r: r["kind"] == "mutant"))
    t("05_protocol_by_control_matrix.csv", protocol_matrix(c, lambda r: r["kind"] != "mutant"))
    fwide, flong = feature_matrix(c, lambda r: r["kind"] == "mutant")
    t("06_feature_by_mutant_matrix.csv", fwide)
    t("06_feature_detections_long.csv", flong)
    plots = plot_cases(c, cases["canonical_passed_battery_detected"], raw_dir, Path(figures_dir) / "candidate_cases",
                       designation)
    t("07_candidate_case_trace_plots.csv", plots)
    conv = convergence_rows(c)
    t("08_numerical_convergence_summary.csv", conv)
    status_rows, time_rows, failures, prov = runtime_rows(c, raw_dir, work_runs_dir)
    t("09_run_status_counts.csv", status_rows)
    t("09_runtime.csv", time_rows)
    t("09_failed_runs.csv", failures)
    t("10_mutant_audit_sheet_completed.csv", audit_rows(c, work_variants_dir))
    p05_per, p05_sum = p05_rows(c)
    t("11_p05_dominance_by_protocol.csv", p05_per)
    t("11_p05_dominance_summary.csv", p05_sum)

    deviations = (Path(deviations_file).read_text(encoding="utf-8").strip()
                  if deviations_file and Path(deviations_file).is_file() else "No deviation log file found.")
    summary = {"study_metadata": meta, "provenance": prov, "flow": flow, "case_counts": {k: len(v) for k, v in cases.items()},
               "p05_summary": p05_sum, "plots": Counter(p["status"].split(":")[0] for p in plots),
               "reporting": {"findings": "exploratory (development pilot); none confirmatory",
                             "analyses_prespecified": "yes: listed in the pilot protocol before data were generated",
                             "deviations": deviations}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    lines = [f"# Pilot outputs: `{Path(processed).name}`", "", f"*{designation}*", "",
             "- Findings: **exploratory (development pilot); none confirmatory.**",
             "- Analyses: specified in the pilot protocol before the data were generated.",
             f"- Software commits in run records: {prov['git_commits']}; runs with a dirty tree: {prov['runs_with_dirty_tree']}",
             f"- Deviations: {deviations}", "",
             "Files are numbered by the protocol's output list (2 flow counts ... 11 P05 dominance). The executive "
             "summary and recommendation are written separately by the researcher.", ""]
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return out
