"""Model curation against the execution plan's inclusion and exclusion criteria.

Every candidate reference model is checked once, in the same way, before any evaluation split
is assigned. Only the unmodified reference model is simulated (no mutant is run), so curation
cannot reveal a detection outcome. Every criterion is mechanical and recorded with its evidence;
no criterion depends on whether a model would help the study's hypothesis. Criteria that need
human judgement return ``None`` and put the model in the "review" state.
"""

from __future__ import annotations

import csv
import dataclasses as dc
import json
import math
import re
import tempfile
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from neuraxis.models import MANIFEST_COLUMNS, materialize
from neuraxis.protocols.definitions import CANONICAL_ID, batched, templates_from_config
from neuraxis.provenance import git_state, utc_now
from neuraxis.schemas import ModelRecord, RunStatus

CRITERIA: dict[str, str] = {
    "C01_provenance": "identifiable scientific provenance (citation, source URL and pinned commit recorded)",
    "C02_reuse_rights": "documented reuse rights (licence recorded, not unclear)",
    "C03_files_present": "required files present (cell file and shipped simulation file)",
    "C04_validation": "passes NeuroML validation (cell and harness network files; relative oracle, D-006)",
    "C05_executes": "shipped simulation executes without manual intervention",
    "C06_trace_interpretable": "membrane-voltage trace finite and within -130..+80 mV",
    "C07_recording_location": "recording location resolved (harness output column read)",
    "C08_responds_to_current": "responds to current injection (rheobase found; at least one spike at 2x rheobase)",
    "C09_deterministic": "deterministic re-execution (bitwise-identical battery traces)",
    "C10_refinement_stable": "features stable under refinement (under 25% of reference entries excluded between h and h/2)",
    "C11_runtime": "estimated per-variant runtime within the budget",
    "C12_operators": "supports several mutation operators (at least 3 semantic operators with a site)",
    "C13_protocols_compatible": "every configured protocol runs and yields a feature table",
}
EXCLUSION_THRESHOLD = 0.25
MIN_SEMANTIC_OPERATORS = 3
V_RANGE_MV = (-130.0, 80.0)
BEHAVIOUR_COLUMNS = ["firing_regime_P05", "spikes_P05", "rebound_spikes_P08", "sag_ratio_P07", "rheobase_nA",
                     "ion_channels"]


def read_candidates(paths: Iterable[Path]) -> list[ModelRecord]:
    """ModelRecords from manifest-format CSVs (extra columns ignored; first occurrence of an id wins)."""
    out: dict[str, ModelRecord] = {}
    for path in paths:
        path = Path(path)
        if not path.is_file():
            continue
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("model_id") and row["model_id"] not in out:
                    fields = {k: (row.get(k) or "").strip() for k in MANIFEST_COLUMNS}
                    col = re.match(r"\d+", fields["harness_v_column"])   # some sweep rows append a note
                    fields["harness_v_column"] = col.group(0) if col else fields["harness_v_column"]
                    temp = re.match(r"\s*([-+]?\d+(?:\.\d+)?\s*degC)", fields["temperature"])
                    fields["temperature"] = temp.group(1) if temp else fields["temperature"]
                    out[row["model_id"]] = ModelRecord(**fields)
    return list(out.values())


def ion_channels(cell_file: Path) -> list[str]:
    text = cell_file.read_text(encoding="utf-8", errors="replace") if cell_file.is_file() else ""
    return sorted(set(re.findall(r'ionChannel="([^"]+)"', text)))


def _feature(fp: Any, pid: str, feat: str) -> Any:
    fv = (fp.tables.get(pid) or {}).get(feat) if fp is not None else None
    return fv.value if fv is not None and fv.state == "defined" else None


def decide(results: dict[str, bool | None]) -> tuple[str, list[str]]:
    failed = [k for k, v in results.items() if v is False]
    review = [k for k, v in results.items() if v is None]
    if failed:
        return "exclude", failed
    if review:
        return "review", review
    return "include_eligible", []


def curate_one(ctx: Any, model: ModelRecord, *, budget_s: float, seed: int,
               semantic_families: Sequence[str] = ("biophysical", "reference")) -> dict[str, Any]:
    """Check one reference model. ``ctx`` is a campaign Context (role ``model_curation``)."""
    from neuraxis import mutations
    from neuraxis.experiments import campaign as cp
    from neuraxis.validation import structural
    from neuraxis.validation.canonical import canonical_protocol
    from neuraxis.validation.convergence import EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME, calibrate
    from neuraxis.validation.fingerprint import build_fingerprint

    r: dict[str, bool | None] = {k: None for k in CRITERIA}
    ev: dict[str, Any] = {"model_id": model.model_id, "snapshot": model.snapshot}
    r["C01_provenance"] = bool(model.citation and model.source_url and model.commit)
    r["C02_reuse_rights"] = bool(model.license) and "unclear" not in model.license.lower()
    try:
        ws = materialize(model, ctx.variants_root / model.model_id / "reference", overwrite=True)
    except FileNotFoundError as exc:
        r["C03_files_present"] = False
        ev["error"] = str(exc)
        return _finish(model, r, ev)
    r["C03_files_present"] = ws.cell_path.is_file() and ws.harness_path.is_file()
    ev["ion_channels"] = ion_channels(ws.cell_path)
    if not r["C03_files_present"]:
        return _finish(model, r, ev)

    st = structural.check(ws, ctx.sim)
    r["C04_validation"] = None if st.valid is None else bool(st.valid)
    ev["validation_errors"] = [m for m in st.jnml.messages if "valid" in m.lower() or "error" in m.lower()][:6]
    variant = cp.reference_variant(ws)
    canonical = canonical_protocol(ws, ctx.canonical_features)
    can = ctx.rec.run_canonical(ws, variant, canonical, need_traces=True)
    r["C05_executes"] = can.status is RunStatus.OK
    ev["canonical_status"] = can.status.value
    tr = can.traces.get(CANONICAL_ID)
    r["C07_recording_location"] = tr is not None if r["C05_executes"] else False
    if tr is not None:
        v = np.asarray(tr.v_mV, dtype=float)
        ev["canonical_v_range_mV"] = [float(np.nanmin(v)), float(np.nanmax(v))]
        r["C06_trace_interpretable"] = bool(np.all(np.isfinite(v)) and V_RANGE_MV[0] <= np.min(v)
                                            and np.max(v) <= V_RANGE_MV[1])
    else:
        r["C06_trace_interpretable"] = False
    if not r["C05_executes"]:
        return _finish(model, r, ev)

    rh = ctx.rec.run_rheobase(ws, variant, ctx.nominal, ctx.rcfg, ctx.settle)
    ev["rheobase_status"] = rh.result.status
    ev["rheobase_nA"] = rh.result.rheobase_nA
    if rh.status is not RunStatus.OK or rh.result.status not in ("ok", "spontaneous"):
        r["C08_responds_to_current"] = False
        return _finish(model, r, ev)
    rheobase = rh.result.rheobase_nA if rh.result.status == "ok" else float(ctx.rcfg["fallback_rheobase_nA"])
    protocols = [t.instantiate(rheobase, ctx.settle) for t in batched(templates_from_config(ctx.cfg["protocols"]))]
    fp1 = build_fingerprint(ctx.rec, ws, variant, protocols, canonical, ctx.nominal, 1, ctx.rcfg, ctx.settle)
    fp2 = build_fingerprint(ctx.rec, ws, variant, protocols, canonical, ctx.nominal, 2, ctx.rcfg, ctx.settle)
    ev["fingerprint_status"] = [fp1.status.value, fp2.status.value]
    r["C13_protocols_compatible"] = (fp1.status is RunStatus.OK and fp2.status is RunStatus.OK
                                     and all(p.protocol_id in fp1.tables for p in protocols))
    spikes_p04 = _feature(fp1, "P04_step_2x", "spike_count")
    ev.update({"spikes_P04": spikes_p04, "spikes_P05": _feature(fp1, "P05_long_step", "spike_count"),
               "firing_regime_P05": _feature(fp1, "P05_long_step", "firing_regime"),
               "rebound_spikes_P08": _feature(fp1, "P08_rebound", "spike_count"),
               "sag_ratio_P07": _feature(fp1, "P07_hyperpolarizing_step", "sag_ratio")})
    if rh.result.status == "spontaneous":
        r["C08_responds_to_current"] = None
        ev["C08_note"] = "spontaneously active: needs human judgement"
    else:
        r["C08_responds_to_current"] = bool(spikes_p04 and spikes_p04 >= 1)

    base = ctx.rec.run_battery(ws, variant, protocols, ctx.nominal, replicate=0, need_traces=True)
    rep = ctx.rec.run_battery(ws, variant, protocols, ctx.nominal, replicate=1, need_traces=True)
    r["C09_deterministic"] = (set(base.traces) == set(rep.traces) and
                              all(np.array_equal(base.traces[k].v_mV, rep.traces[k].v_mV) for k in base.traces))

    if r["C13_protocols_compatible"]:
        entries = calibrate({1: fp1, 2: fp2}, model.model_id, ctx.tcfg, ctx.fcfg)
        excluded = [e for e in entries if e.limiting in (EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME)]
        ev["refinement_excluded"] = f"{len(excluded)}/{len(entries)}"
        r["C10_refinement_stable"] = bool(entries) and len(excluded) / len(entries) < EXCLUSION_THRESHOLD
    else:
        r["C10_refinement_stable"] = False
    # A variant costs about one nominal fingerprint plus, when detected, one at h/2 (twice the steps).
    est = fp1.runtime_s + fp2.runtime_s
    ev["estimated_variant_runtime_s"] = round(est, 1)
    r["C11_runtime"] = est <= budget_s

    ops = [n for n, op in mutations.REGISTRY.items() if getattr(op.family, "value", op.family) in semantic_families]
    with tempfile.TemporaryDirectory(prefix="neuraxis_curation_") as tmp:
        recs = mutations.generate_mutants(model, ops, 1, seed, Path(tmp))
    ev["semantic_operators_with_site"] = sorted({x.operator for x in recs})
    r["C12_operators"] = len(ev["semantic_operators_with_site"]) >= MIN_SEMANTIC_OPERATORS
    return _finish(model, r, ev)


def _finish(model: ModelRecord, r: dict[str, bool | None], ev: dict[str, Any]) -> dict[str, Any]:
    decision, reasons = decide(r)
    return {"model": dc.asdict(model), "criteria": r, "decision": decision, "reasons": reasons, "evidence": ev}


def row(result: dict[str, Any], meta: dict[str, str], curated_utc: str, commit: str) -> dict[str, Any]:
    m, ev = result["model"], result["evidence"]
    out = {**meta, "model_id": m["model_id"], "name": m["name"], "source_family": m["source_family"],
           "snapshot": m["snapshot"], "license": m["license"], "citation": m["citation"],
           "decision": result["decision"], "reasons": ";".join(result["reasons"])}
    for k, v in result["criteria"].items():
        out[k] = "" if v is None else ("pass" if v else "fail")
    for k in BEHAVIOUR_COLUMNS:
        val = ev.get(k)
        out[k] = ";".join(val) if isinstance(val, list) else ("" if val is None else val)
    out.update({"estimated_variant_runtime_s": ev.get("estimated_variant_runtime_s", ""),
                "refinement_excluded": ev.get("refinement_excluded", ""),
                "semantic_operators_with_site": ";".join(ev.get("semantic_operators_with_site", [])),
                "validation_errors": " | ".join(ev.get("validation_errors", []))[:500],
                "curated_utc": curated_utc, "git_commit": commit})
    return out


def run_curation(campaign: str, sources: Sequence[Path], out_csv: Path, *, budget_s: float = 1800.0,
                 models: Sequence[str] | None = None, workers: int | None = None) -> Path:
    from neuraxis.experiments import campaign as cp
    from neuraxis.experiments import registry
    from neuraxis.validation.execution import run_parallel

    ctx = cp.make_context(campaign, workers, role=registry.MODEL_CURATION)
    seed = int(ctx.cfg["selection"]["seed"])
    candidates = [m for m in read_candidates(sources) if not models or m.model_id in models]
    tasks = [lambda m=m: curate_one(ctx, m, budget_s=budget_s, seed=seed) for m in candidates]
    results = run_parallel(tasks, min(ctx.workers, max(1, len(tasks))))
    commit, dirty = git_state()
    stamp = utc_now()
    rows, evidence_dir = [], ctx.processed / "curation"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for m, res in zip(candidates, results):
        if not isinstance(res, dict):              # TaskError: tool or code failure; recorded, never silent
            res = {"model": dc.asdict(m), "criteria": {k: None for k in CRITERIA}, "decision": "review",
                   "reasons": ["curation_error"], "evidence": {"error": str(getattr(res, "traceback", res))[-2000:]}}
        (evidence_dir / f"{m.model_id}.json").write_text(json.dumps(res, indent=2, default=str) + "\n", encoding="utf-8")
        rows.append(row(res, ctx.meta, stamp, f"{commit}{'+dirty' if dirty else ''}"))
    out_csv = Path(out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    names = list(dict.fromkeys(k for r_ in rows for k in r_))
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    write_report(rows, out_csv.parent.parent / "docs" / "MODEL_CURATION_REPORT.md", campaign, stamp, budget_s)
    return out_csv


def write_report(rows: Sequence[dict], path: Path, campaign: str, stamp: str, budget_s: float) -> None:
    from collections import Counter

    counts = Counter(r["decision"] for r in rows)
    fam = Counter(r["source_family"] for r in rows if r["decision"] == "include_eligible")
    lines = ["# Model curation report", "",
             f"*Generated by `neuraxis curate-models` (campaign `{campaign}`, {stamp}). Only reference models were "
             "simulated; no mutant was run, so no detection outcome was seen. Criteria are mechanical and "
             "decided before any split (`src/neuraxis/orchestration/curation.py`).*", "",
             "## In plain English", "",
             f"- {len(rows)} candidate models were checked against {len(CRITERIA)} rules.",
             f"- {counts.get('include_eligible', 0)} passed every rule, {counts.get('exclude', 0)} failed at least one, "
             f"{counts.get('review', 0)} need a human judgement.",
             f"- Eligible models come from {len(fam)} distinct sources: {', '.join(sorted(fam)) or 'none'}.", "",
             "## Criteria", "", "| id | rule |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in CRITERIA.items()]
    lines += ["", f"Runtime budget per variant: {budget_s:.0f} s (nominal plus h/2 fingerprint).", "",
              "## Results", "", "| model | source | decision | failed or open criteria | P05 regime | rebound spikes (P08) | "
              "sag ratio (P07) | rheobase nA | est. s/variant |", "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (x["decision"], x["source_family"], x["model_id"])):
        lines.append(f"| `{r['model_id']}` | {r['source_family']} | {r['decision']} | {r['reasons'] or '-'} | "
                     f"{r['firing_regime_P05']} | {r['rebound_spikes_P08']} | {_fmt(r['sag_ratio_P07'])} | "
                     f"{_fmt(r['rheobase_nA'])} | {r['estimated_variant_runtime_s']} |")
    lines += ["", "Full evidence per model: `results/processed/<campaign>/curation/<model_id>.json`; table: "
              "`manifests/models.csv`.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _fmt(x: Any) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x or "")
    return "" if math.isnan(v) else f"{v:.4g}"
