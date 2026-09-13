"""Campaign orchestration shared by the pilot, discovery and held-out stages.

A *campaign* is one self-consistent set of runs under one configuration snapshot. Stages
are idempotent: simulations are content-addressed and cached by the RunRecorder, so
re-running a stage only costs feature loading.

Stages
  1. reference_stage   validate references, find rheobase, instantiate protocols, fingerprint at h, h/2, h/4,
                       and check deterministic re-execution
  2. calibrate_stage   tolerance table from reference refinement (discovery/reference data only)
  3. generate_stage    mutants and valid transformations (deterministic, seeded), manifests
  4. variant_stage     structural -> fingerprint(h) -> compare -> [fingerprint(h/2) -> compare] -> classify
  5. aggregate         classification, detections, detection matrix, validation cascade, costs, audit sheet
"""

from __future__ import annotations

import csv
import dataclasses as dc
import json
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

from neurosem import config
from neurosem.models import Workspace, load_models, materialize
from neurosem.protocols.definitions import CANONICAL_ID, batched, templates_from_config
from neurosem.provenance import REPO_ROOT, utc_now
from neurosem.schemas import (ConcreteProtocol, MutantClass, RunStatus, VariantKind, VariantRecord, dumps, to_jsonable,
                              variant_from_dict)
from neurosem.simulators.jneuroml import JNeuroML
from neurosem.validation import structural
from neurosem.validation.canonical import canonical_protocol
from neurosem.validation.convergence import ToleranceTable, calibrate, convergence_report
from neurosem.validation.execution import RunRecorder, TaskError, run_parallel
from neurosem.validation.fingerprint import (RHEOBASE_ID, Detection, Fingerprint, ToolFailure, build_fingerprint, classify,
                                             compare, detecting_protocols, save_fingerprint, write_detections)


@dc.dataclass
class Context:
    campaign: str
    cfg: config.LoadedConfig
    fcfg: dict
    tcfg: dict
    sim: JNeuroML
    rec: RunRecorder
    workers: int
    processed: Path
    variants_root: Path

    @property
    def nominal(self):
        return config.nominal_exec(self.cfg)

    @property
    def factors(self) -> list[int]:
        return [int(f) for f in self.cfg["numerics"]["refinement_factors"]]

    @property
    def rcfg(self) -> dict:
        return dict(self.cfg["rheobase"])

    @property
    def settle(self) -> float:
        return float(self.cfg["numerics"]["settle_ms"])


def make_context(campaign: str, workers: int | None = None) -> Context:
    cfg = config.study()
    sim = JNeuroML(max_memory=cfg["numerics"]["java_max_memory"])
    if not sim.available():
        raise ToolFailure("Java/jNeuroML unavailable: run scripts/bootstrap_java.py")
    fcfg, tcfg = config.features(), config.tolerances()
    processed = config.results_dir(cfg) / "processed" / campaign
    processed.mkdir(parents=True, exist_ok=True)
    snap = {"campaign": campaign, "created_utc": utc_now(),
            "configs": {p.path.name: p.sha256 for p in (cfg, fcfg, tcfg)}, "simulator": sim.version_info()}
    (processed / "campaign_configs.json").write_text(json.dumps(snap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return Context(campaign, cfg, fcfg.data, tcfg.data, sim, RunRecorder(campaign, sim, features_cfg=fcfg.data),
                   workers or int(cfg["execution"]["workers"]), processed,
                   config.work_dir(cfg) / "variants" / campaign)


def _unwrap(results: list[Any], what: str) -> list[Any]:
    errors = [r for r in results if isinstance(r, TaskError)]
    if errors:
        raise RuntimeError(f"{len(errors)} {what} task(s) failed; first:\n{errors[0].traceback}")
    return results


# --------------------------------------------------------------------------- references
@dc.dataclass
class RefState:
    ws: Workspace
    variant: VariantRecord
    structural: structural.StructuralResult
    canonical: ConcreteProtocol
    protocols: list[ConcreteProtocol]
    rheobase_nA: float
    rheobase_status: str
    fps: dict[int, Fingerprint]
    determinism: dict


def reference_variant(ws: Workspace) -> VariantRecord:
    tree = ws.tree_sha256()
    return VariantRecord(variant_id=f"{ws.model.model_id}__reference", model_id=ws.model.model_id,
                         kind=VariantKind.REFERENCE, description="unmodified reference snapshot",
                         parent_tree_sha256=tree, tree_sha256=tree, created_utc=utc_now())


def _reference_one(ctx: Context, model_id: str) -> RefState:
    model = load_models()[model_id]
    ws = materialize(model, ctx.variants_root / model_id / "reference", overwrite=True)
    variant = reference_variant(ws)
    (ws.root / "variant.json").write_text(dumps(variant), encoding="utf-8")
    st = structural.check(ws, ctx.sim)
    if st.valid is None:
        raise ToolFailure(f"cannot validate reference {model_id}")
    if not st.valid:
        raise ValueError(f"reference model {model_id} is not structurally valid: {st.jnml.messages}")
    canonical = canonical_protocol(ws)
    rh = ctx.rec.run_rheobase(ws, variant, ctx.nominal, ctx.rcfg, ctx.settle)
    if rh.status is not RunStatus.OK:
        raise RuntimeError(f"reference rheobase search failed for {model_id}: {rh.record.get('cost')}")
    rheobase = rh.result.rheobase_nA if rh.result.status == "ok" else float(ctx.rcfg["fallback_rheobase_nA"])
    templates = batched(templates_from_config(ctx.cfg["protocols"]))
    protocols = [t.instantiate(rheobase, ctx.settle) for t in templates]

    def fp(factor: int) -> Fingerprint:
        return build_fingerprint(ctx.rec, ws, variant, protocols, canonical, ctx.nominal, factor, ctx.rcfg, ctx.settle)

    fps = dict(zip(ctx.factors, _unwrap(run_parallel([lambda f=f: fp(f) for f in ctx.factors], len(ctx.factors)),
                                        "reference fingerprint")))
    for f, v in fps.items():
        if v.status is not RunStatus.OK:
            raise RuntimeError(f"reference {model_id} failed at refinement factor {f}: {v.status} {v.messages}")

    # Deterministic re-execution (M2 exit criterion): replicate the nominal battery and canonical runs.
    rep = ctx.rec.run_battery(ws, variant, protocols, ctx.nominal, replicate=1)
    base = ctx.rec.run_battery(ws, variant, protocols, ctx.nominal, replicate=0)
    identical = all(np.array_equal(base.traces[k].v_mV, rep.traces[k].v_mV) for k in base.traces) and \
        set(base.traces) == set(rep.traces)
    determinism = {"model_id": model_id, "bitwise_identical_battery_traces": bool(identical),
                   "replicate_run_ids": [r.run_id for r in rep.records], "base_run_ids": [r.run_id for r in base.records]}

    out = ctx.processed / "references" / model_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "protocols.json").write_text(json.dumps(to_jsonable(protocols), indent=2) + "\n", encoding="utf-8")
    (out / "canonical_protocol.json").write_text(json.dumps(to_jsonable(canonical), indent=2) + "\n", encoding="utf-8")
    (out / "structural.json").write_text(json.dumps(to_jsonable(st), indent=2) + "\n", encoding="utf-8")
    (out / "determinism.json").write_text(json.dumps(determinism, indent=2) + "\n", encoding="utf-8")
    (out / "rheobase_search.json").write_text(json.dumps(rh.record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for f, v in fps.items():
        save_fingerprint(v, out / f"fingerprint_L{f}.json")
    return RefState(ws, variant, st, canonical, protocols, rheobase, rh.result.status, fps, determinism)


def reference_stage(ctx: Context, model_ids: Sequence[str]) -> dict[str, RefState]:
    states = _unwrap(run_parallel([lambda m=m: _reference_one(ctx, m) for m in model_ids], min(ctx.workers, len(model_ids))),
                     "reference")
    return {s.variant.model_id: s for s in states}


# --------------------------------------------------------------------------- tolerances
def calibrate_stage(ctx: Context, refs: dict[str, RefState]) -> ToleranceTable:
    entries, report = [], []
    for mid, ref in refs.items():
        entries += calibrate(ref.fps, mid, ctx.tcfg, ctx.fcfg)
        report += convergence_report(ref.fps)
    table = ToleranceTable(entries)
    table.to_csv(ctx.processed / "tolerances.csv")
    _write_rows(ctx.processed / "convergence.csv", report)
    return table


# --------------------------------------------------------------------------- variants
def generate_stage(ctx: Context, refs: dict[str, RefState], families: Sequence[str], n_mutants: int,
                   n_transforms: int, seed: int) -> list[VariantRecord]:
    from neurosem import mutations, transforms

    mut_ops = [name for name, op in mutations.REGISTRY.items() if getattr(op.family, "value", op.family) in families]
    tr_ops = list(transforms.REGISTRY)
    records: list[VariantRecord] = []
    for mid in refs:
        model = refs[mid].ws.model
        records += mutations.generate_mutants(model, mut_ops, n_mutants, seed, ctx.variants_root / mid / "mutants")
        records += transforms.generate_transforms(model, tr_ops, n_transforms, seed, ctx.variants_root / mid / "transforms")
    mutants = [r for r in records if r.kind is VariantKind.MUTANT]
    trans = [r for r in records if r.kind is not VariantKind.MUTANT]
    mutations.write_manifest(mutants, ctx.processed / "mutation_manifest.csv")
    mutations.write_manifest(trans, ctx.processed / "valid_transforms.csv")
    return records


def variant_dir(ctx: Context, v: VariantRecord) -> Path:
    sub = "mutants" if v.kind is VariantKind.MUTANT else "transforms"
    return ctx.variants_root / v.model_id / sub / v.variant_id


@dc.dataclass
class VariantOutcome:
    variant: VariantRecord
    structural_valid: bool | None
    libneuroml_strict: bool | None
    status_h: str
    klass: MutantClass
    detections_h: list[Detection]
    detections_h2: list[Detection] | None
    detecting_protocols: list[str]
    canonical_detected: bool
    runtime_s: float


def _variant_one(ctx: Context, ref: RefState, tol: ToleranceTable, v: VariantRecord) -> VariantOutcome:
    ws = Workspace(variant_dir(ctx, v), ref.ws.model)
    out = ctx.processed / "variants" / v.variant_id
    out.mkdir(parents=True, exist_ok=True)
    st = structural.check(ws, ctx.sim, reference=ref.structural)
    if st.valid is None:
        raise ToolFailure(f"validator unavailable for {v.variant_id}")
    (out / "structural.json").write_text(json.dumps(to_jsonable(st), indent=2) + "\n", encoding="utf-8")
    if not st.valid:
        k = classify(False, None, None, [], None)
        return VariantOutcome(v, False, st.libneuroml_strict, "not_run", k, [], None, [], False, 0.0)
    fp_h = build_fingerprint(ctx.rec, ws, v, ref.protocols, ref.canonical, ctx.nominal, 1, ctx.rcfg, ctx.settle)
    save_fingerprint(fp_h, out / "fingerprint_L1.json")
    runtime = fp_h.runtime_s
    det_h = compare(ref.fps[1], fp_h, tol) if fp_h.status is RunStatus.OK else []
    fp_h2 = det_h2 = None
    if fp_h.status is RunStatus.OK and det_h:
        fp_h2 = build_fingerprint(ctx.rec, ws, v, ref.protocols, ref.canonical, ctx.nominal, 2, ctx.rcfg, ctx.settle)
        save_fingerprint(fp_h2, out / "fingerprint_L2.json")
        runtime += fp_h2.runtime_s
        det_h2 = compare(ref.fps[2], fp_h2, tol) if fp_h2.status is RunStatus.OK else []
    k = classify(True, fp_h, fp_h2, det_h, det_h2)
    write_detections(det_h + (det_h2 or []), out / "detections.csv")
    dprot = sorted(detecting_protocols(det_h, det_h2)) if k.admissible else []
    outcome = VariantOutcome(v, True, st.libneuroml_strict, fp_h.status.value, k, det_h, det_h2, dprot,
                             any(d.protocol_id == CANONICAL_ID for d in det_h), round(runtime, 3))
    _write_diagnostic(ctx, outcome, fp_h, fp_h2, out / "diagnostic.md")
    return outcome


def variant_stage(ctx: Context, refs: dict[str, RefState], tol: ToleranceTable,
                  variants: Sequence[VariantRecord]) -> list[VariantOutcome]:
    tasks = [lambda v=v: _variant_one(ctx, refs[v.model_id], tol, v) for v in variants]
    return _unwrap(run_parallel(tasks, ctx.workers), "variant")


def load_variant_records(ctx: Context) -> list[VariantRecord]:
    recs = []
    for p in sorted(ctx.variants_root.glob("*/*/*/variant.json")):
        recs.append(variant_from_dict(json.loads(p.read_text(encoding="utf-8"))))
    return recs


# --------------------------------------------------------------------------- aggregation
def aggregate(ctx: Context, refs: dict[str, RefState], outcomes: Sequence[VariantOutcome]) -> dict[str, Any]:
    p = ctx.processed
    rows = []
    for o in outcomes:
        v = o.variant
        rows.append({"variant_id": v.variant_id, "model_id": v.model_id, "kind": v.kind.value, "family": v.family,
                     "operator": v.operator, "params": json.dumps(v.params, sort_keys=True), "class": o.klass.value,
                     "admissible": o.klass.admissible, "structural_valid": o.structural_valid,
                     "libneuroml_strict": o.libneuroml_strict, "status_h": o.status_h,
                     "n_detections_h": len(o.detections_h),
                     "n_detections_h2": "" if o.detections_h2 is None else len(o.detections_h2),
                     "canonical_detected_h": o.canonical_detected, "detecting_protocols": ";".join(o.detecting_protocols),
                     "runtime_s": o.runtime_s})
    _write_rows(p / "classification.csv", rows)
    write_detections([d for o in outcomes for d in o.detections_h + (o.detections_h2 or [])], p / "detections.csv")

    # Detection matrix over admissible MUTANTS; columns = canonical + battery + rheobase.
    first_ref = next(iter(refs.values()))
    protocol_ids = [CANONICAL_ID] + [q.protocol_id for q in first_ref.protocols] + [RHEOBASE_ID]
    cost = {pid: float(np.mean([r.fps[1].cell_steps.get(pid, 0) for r in refs.values()])) for pid in protocol_ids}
    adm = [o for o in outcomes if o.variant.kind is VariantKind.MUTANT and o.klass.admissible]
    mat_rows = []
    for o in adm:
        row = {"mutant_id": o.variant.variant_id, "model_id": o.variant.model_id, "family": o.variant.family}
        row.update({pid: int(pid in o.detecting_protocols) for pid in protocol_ids})
        mat_rows.append(row)
    _write_rows(p / "detection_matrix.csv", mat_rows, fieldnames=["mutant_id", "model_id", "family"] + protocol_ids)
    _write_rows(p / "protocol_costs.csv", [{"protocol_id": k, "mean_cell_steps": v} for k, v in cost.items()])

    mutants = [o for o in outcomes if o.variant.kind is VariantKind.MUTANT]
    cascade = {
        "total_mutants": len(mutants),
        "schema_valid": sum(1 for o in mutants if o.structural_valid),
        "executable": sum(1 for o in mutants if o.klass not in (MutantClass.STRUCTURALLY_INVALID, MutantClass.NON_EXECUTABLE)),
        "numerically_stable": sum(1 for o in mutants if o.klass not in (MutantClass.STRUCTURALLY_INVALID,
                                                                         MutantClass.NON_EXECUTABLE,
                                                                         MutantClass.NUMERICALLY_UNSTABLE)),
        "non_equivalent": sum(1 for o in mutants if o.klass.admissible),
        "canonical_survivors_detected_elsewhere": sum(1 for o in mutants if o.klass is MutantClass.SILENT),
        "equivalent_within_tested_domain": sum(1 for o in mutants if o.klass is MutantClass.EQUIVALENT),
    }
    (p / "validation_cascade.json").write_text(json.dumps(cascade, indent=2) + "\n", encoding="utf-8")

    transforms_ = [o for o in outcomes if o.variant.kind is not VariantKind.MUTANT]
    fp_rows = [{"variant_id": o.variant.variant_id, "model_id": o.variant.model_id, "kind": o.variant.kind.value,
                "operator": o.variant.operator, "class": o.klass.value, "false_positive": o.klass.admissible,
                "detected_at_h_only": bool(o.detections_h) and not o.klass.admissible,
                "detections": ";".join(sorted({f"{d.protocol_id}:{d.feature}" for d in o.detections_h}))}
               for o in transforms_]
    _write_rows(p / "false_positives.csv", fp_rows)

    audit = [{"variant_id": o.variant.variant_id, "operator": o.variant.operator, "family": o.variant.family,
              "edits": json.dumps([dc.asdict(e) for e in o.variant.edits]),
              "exec_overrides": json.dumps(o.variant.exec_overrides), "assigned_class": o.klass.value,
              "detecting_protocols": ";".join(o.detecting_protocols),
              "human_auditor": "", "edit_matches_label (yes/no)": "", "class_plausible (yes/no)": "", "notes": ""}
             for o in mutants]
    _write_rows(p / "mutant_audit_sheet.csv", audit)
    return {"cascade": cascade, "classes": Counter(o.klass.value for o in outcomes),
            "false_positives": sum(r["false_positive"] for r in fp_rows), "n_transforms": len(fp_rows),
            "silent": [o.variant.variant_id for o in mutants if o.klass is MutantClass.SILENT]}


def _write_rows(path: Path, rows: Sequence[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or (list(rows[0].keys()) if rows else ["empty"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})


def _write_diagnostic(ctx: Context, o: VariantOutcome, fp_h: Fingerprint, fp_h2: Fingerprint | None, path: Path) -> None:
    """Per-mutant diagnostic (M5 exit criterion): every detection -> protocol, feature, threshold, evidence."""
    lines = [f"# {o.variant.variant_id}", "", f"- model: `{o.variant.model_id}`", f"- kind/family/operator: "
             f"{o.variant.kind.value} / {o.variant.family} / {o.variant.operator}",
             f"- parameters: `{json.dumps(o.variant.params, sort_keys=True)}`",
             f"- recorded edits: `{json.dumps([dc.asdict(e) for e in o.variant.edits])}`",
             f"- execution overrides: `{json.dumps(o.variant.exec_overrides)}`", f"- class: **{o.klass.value}**",
             f"- nominal-level status: {o.status_h}; runtime {o.runtime_s} s", "",
             "| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for d in o.detections_h + (o.detections_h2 or []):
        lines.append(f"| h/{d.level_factor} | {d.protocol_id} | {d.feature} | {d.reason} | {d.ref_value} | {d.var_value} | "
                     f"{'' if d.diff is None else f'{d.diff:.6g}'} | {'' if d.tau is None else f'{d.tau:.6g}'} | "
                     f"`{d.ref_run_id}` | `{d.var_run_id}` |")
    lines += ["", "Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the "
              "matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature "
              "are detected at h/1 and h/2."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
