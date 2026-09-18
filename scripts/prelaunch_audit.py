"""Pre-launch audit of the Pilot 2 evidence: inventory, kinetics overlap, and summary counts.

Read-only with respect to every existing artefact. It hashes and describes what is already on disk
and writes two new audit tables plus a JSON summary:

- ``results/audits/PILOT2_PRELAUNCH_EVIDENCE_INVENTORY.csv``
- ``results/audits/PILOT2_KINETICS_OVERLAP_AUDIT.csv``
- ``results/audits/PILOT2_PRELAUNCH_AUDIT_SUMMARY.json``

Nothing is deleted, moved, regenerated or sanitised, and no simulation is executed.

    python scripts/prelaunch_audit.py
"""

from __future__ import annotations

import concurrent.futures as cf
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis.provenance import REPO_ROOT, sha256_file, utc_now  # noqa: E402

PILOT2_MODELS = ("acnet2_pyr_soma", "migliore2014_mt_soma", "nml2_hh_example", "osb_hh2_477127614",
                 "pospischil2008_fs")
# Scope: everything connected to the Pilot 2 preparation, its gates and its partial execution.
SCOPE: dict[str, str] = {
    "results/audits/kinetics_pilot2": "kinetics_validation_pilot2_models",
    "results/audits/kinetics_validation": "kinetics_validation_fixtures",
    "results/audits/readiness": "readiness_run",
    "results/audits/smoke_test": "smoke_test",
    "results/audits/pilot2_authorization": "authorization_gate",
    "results/processed/pilot2": "pilot2_partial_execution",
    "results/raw/pilot2": "pilot2_partial_raw",
    "results/processed/pilot2-rehearsal": "rehearsal_processed",
    "results/raw/pilot2-rehearsal": "rehearsal_raw",
    "results/processed/curation-v3": "curation_v3_processed",
    "manifests": "frozen_matrix_or_manifest",
    "configs": "configuration",
    "docs/PILOT2_PROTOCOL.md": "frozen_protocol",
    "docs/MODEL_CURATION_FINAL_TABLE.md": "curation_report",
    "docs/KINETICS_OPERATOR_VALIDATION.md": "kinetics_documentation",
    "data/model_manifest.csv": "model_manifest",
}
# File contents that constitute a behavioural outcome rather than a description of one.
OUTCOME_HINTS = ("spikes_before_after", "max_abs_dv_mV", "spike_count", "detections", "feature",
                 "trace", "rheobase", "classification", "fingerprint")
TRACE_SUFFIX = (".npz", ".dat")


def git_commit_for(rel: str) -> str:
    out = subprocess.run(["git", "log", "-1", "--format=%h", "--", rel], cwd=REPO_ROOT,
                         capture_output=True, text=True, check=False).stdout.strip()
    return out or "untracked"


def describe(path: Path, category: str) -> dict:
    rel = path.relative_to(REPO_ROOT).as_posix()
    st = path.stat()
    head = ""
    if path.suffix in (".json", ".csv", ".md", ".txt", ".yaml", ".sha256", ".log"):
        try:
            head = path.read_text(encoding="utf-8", errors="replace")[:200_000]
        except OSError:
            head = ""
    models = sorted(m for m in PILOT2_MODELS if m in head or m in rel)
    outcome = (path.suffix in TRACE_SUFFIX or any(h in head for h in OUTCOME_HINTS)
               or "fingerprint" in path.name or "detections" in path.name)
    run_id = ""
    for part in path.parts:
        if part.startswith(("r-", "s-")) and len(part) > 8:
            run_id = part
    return {"path": rel, "category": category, "size_bytes": st.st_size,
            "modified_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds"),
            "sha256": sha256_file(path), "git_commit": git_commit_for(rel), "run_id": run_id,
            "contains_pilot2_model_id": "yes" if models else "no",
            "pilot2_models_named": ";".join(models),
            "contains_behavioural_outcome": "yes" if outcome else "no"}


def inventory() -> list[dict]:
    targets: list[tuple[Path, str]] = []
    for rel, category in SCOPE.items():
        p = REPO_ROOT / rel
        if p.is_file():
            targets.append((p, category))
        elif p.is_dir():
            targets += [(f, category) for f in sorted(p.rglob("*")) if f.is_file()]
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda t: describe(*t), targets))
    return sorted(rows, key=lambda r: r["path"])


def frozen_variant_index() -> dict[tuple[str, str], list[dict]]:
    """(model_id, operator) -> frozen variant rows, for comparing the exact edited parameters."""
    out: dict[tuple[str, str], list[dict]] = {}
    path = REPO_ROOT / "manifests" / "PILOT2_VARIANTS.csv"
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.setdefault((r["model_id"], r["operator"]), []).append(r)
    return out


def matrix_pairs() -> set[tuple[str, str]]:
    path = REPO_ROOT / "manifests" / "PILOT2_EXPERIMENT_MATRIX.csv"
    with open(path, newline="", encoding="utf-8") as f:
        return {(r["model_id"], r["protocol_id"]) for r in csv.DictReader(f)}


def site_key(params: dict) -> tuple:
    """What the edit actually is, independent of the variant id: channel, gate, magnitude."""
    return (params.get("channel", ""), params.get("gate", ""), params.get("mechanism", ""),
            params.get("delta_mV", params.get("shift_mV", params.get("factor", ""))))


def severity_of(params: dict) -> str:
    from neuraxis.mutations.severity import severity

    return severity(params)


def overlap_rows(inv: list[dict]) -> tuple[list[dict], dict]:
    k = json.loads((REPO_ROOT / "results" / "audits" / "kinetics_pilot2" /
                    "kinetics_validation.json").read_text(encoding="utf-8"))
    frozen = frozen_variant_index()
    pairs = matrix_pairs()
    created = k["created_utc"]
    commit = git_commit_for("results/audits/kinetics_pilot2/kinetics_validation.json")
    by_path = {r["path"]: r for r in inv}
    rows, stats = [], {"executions": 0, "exact_param_overlaps": 0, "same_model_operator_overlaps": 0,
                       "models": set(), "operators": set(), "protocols": set(), "outcomes_exposed": 0,
                       "unreconstructable": 0}
    for r in k["rows"]:
        model = r["fixture"]
        if model not in PILOT2_MODELS:
            continue
        if r.get("site") is None:
            rows.append({"model_id": model, "model_hash": "", "operator": r["operator"], "site": "",
                         "severity": "", "protocol_id": "P00_canonical", "run_id": "",
                         "run_timestamp": created, "git_commit": commit, "trace_hash": "", "feature_hash": "",
                         "in_frozen_variant_manifest": "no", "in_frozen_experiment_matrix": "no",
                         "outcome_generated": "no", "outcome_summarized": "yes",
                         "outcome_viewed_by_claude": "yes", "outcome_viewed_by_human": "yes",
                         "possible_design_influence": "yes",
                         "recommended_classification": "L1_static_contact_only (operator inapplicable; the "
                                                       "inapplicability reason was used in the protocol text)",
                         "evidence_paths": "results/audits/kinetics_pilot2/kinetics_validation.json",
                         "note": (r.get("inapplicable") or [{}])[0].get("reason", "no eligible site")})
        continue_row = r.get("site") is None
        if continue_row:
            continue
        stats["executions"] += 1
        stats["models"].add(model)
        stats["operators"].add(r["operator"])
        stats["protocols"].add("P00_canonical")
        params = r.get("params") or {}
        sev = severity_of(params)
        cands = frozen.get((model, r["operator"]), [])
        exact = [c for c in cands if site_key(json.loads(c["params"])) == site_key(params)]
        if exact:
            stats["exact_param_overlaps"] += 1
        if cands:
            stats["same_model_operator_overlaps"] += 1
        if r.get("simulation_status") == "ok":
            stats["outcomes_exposed"] += 1
        plot = f"results/audits/kinetics_pilot2/{r.get('plot', '')}" if r.get("plot") else ""
        rows.append({
            "model_id": model, "model_hash": "not recorded per site (workspace tree hash not stored)",
            "operator": r["operator"], "site": r["site"], "severity": sev, "protocol_id": "P00_canonical",
            "run_id": "not recorded in the validation table (runs are under results/audits/kinetics_pilot2/raw)",
            "run_timestamp": created, "git_commit": commit,
            "trace_hash": by_path.get(plot, {}).get("sha256", ""), "feature_hash": "",
            "in_frozen_variant_manifest": "yes" if exact else ("same model and operator, different site"
                                                               if cands else "no"),
            "in_frozen_experiment_matrix": "yes" if (model, "P00_canonical") in pairs else "no",
            "outcome_generated": "yes" if r.get("simulation_status") == "ok" else "uncertain",
            "outcome_summarized": "yes",          # printed as a table by the validation script
            "outcome_viewed_by_claude": "yes",    # read and quoted in the conversation
            "outcome_viewed_by_human": "yes",     # reported to Neel in the conversation
            "possible_design_influence": "yes",   # the protocol text was edited after this run
            "recommended_classification": "L4_outcome_exposure_with_possible_design_influence",
            "evidence_paths": ";".join(x for x in ["results/audits/kinetics_pilot2/kinetics_validation.json",
                                                   plot] if x),
            "note": f"spikes_before_after={r.get('spikes_before_after')}; max_abs_dv_mV={r.get('max_abs_dv_mV')}",
        })
    stats["models"] = sorted(stats["models"])
    stats["operators"] = sorted(stats["operators"])
    stats["protocols"] = sorted(stats["protocols"])
    return rows, stats


def partial_campaign_state() -> dict:
    p = REPO_ROOT / "results" / "processed" / "pilot2"
    raw = REPO_ROOT / "results" / "raw" / "pilot2"
    variants = sorted((p / "variants").glob("*")) if (p / "variants").is_dir() else []
    return {
        "raw_run_records": len(list(raw.glob("*"))) if raw.is_dir() else 0,
        "variant_directories": len(variants),
        "variants_with_h_fingerprint": sum(1 for v in variants if (v / "fingerprint_L1.json").is_file()),
        "variants_with_h2_fingerprint": sum(1 for v in variants if (v / "fingerprint_L2.json").is_file()),
        "variants_with_detection_files": sum(1 for v in variants if (v / "detections.csv").is_file()),
        "aggregate_classification_written": (p / "classification.csv").is_file(),
        "pilot_report_written": (p / "pilot_report.md").is_file(),
        "outputs_built": (p / "pilot_v2_outputs").is_dir(),
        "frozen_variants_total": 143,
    }


def main() -> int:
    out_dir = REPO_ROOT / "results" / "audits"
    out_dir.mkdir(parents=True, exist_ok=True)
    inv = inventory()
    inv_path = out_dir / "PILOT2_PRELAUNCH_EVIDENCE_INVENTORY.csv"
    names = list(inv[0]) if inv else ["path"]
    with open(inv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        w.writeheader()
        w.writerows(inv)

    rows, stats = overlap_rows(inv)
    ov_path = out_dir / "PILOT2_KINETICS_OVERLAP_AUDIT.csv"
    names = list(dict.fromkeys(k for r in rows for k in r))
    with open(ov_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    summary = {"created_utc": utc_now(), "inventory_files": len(inv),
               "inventory_files_naming_a_pilot2_model": sum(1 for r in inv if r["contains_pilot2_model_id"] == "yes"),
               "inventory_files_with_behavioural_outcome": sum(1 for r in inv
                                                               if r["contains_behavioural_outcome"] == "yes"),
               "kinetics_overlap": stats, "partial_campaign": partial_campaign_state()}
    (out_dir / "PILOT2_PRELAUNCH_AUDIT_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
