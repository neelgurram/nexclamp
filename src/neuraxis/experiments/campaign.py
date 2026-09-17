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

from neuraxis import config
from neuraxis.experiments import registry, strata
from neuraxis.models import Workspace, load_models, materialize
from neuraxis.protocols.definitions import CANONICAL_FEATURES, CANONICAL_ID, batched, templates_from_config
from neuraxis.provenance import utc_now
from neuraxis.schemas import (ConcreteProtocol, MutantClass, RunStatus, VariantKind, VariantRecord, dumps, to_jsonable,
                              variant_from_dict)
from neuraxis.simulators.jneuroml import JNeuroML
from neuraxis.validation import structural
from neuraxis.validation.canonical import canonical_protocol
from neuraxis.validation.convergence import ToleranceTable, calibrate, convergence_report
from neuraxis.validation import trace_regression as tr
from neuraxis.validation.execution import RunRecorder, TaskError, run_parallel
from neuraxis.validation.fingerprint import (RHEOBASE_ID, Detection, Fingerprint, ToolFailure, build_fingerprint, classify,
                                             compare, detecting_protocols, load_fingerprint, reproducible_keys,
                                             save_fingerprint, write_detections)


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
    def canonical_features(self) -> tuple[str, ...]:
        """Features extracted on the canonical harness: primary ``canonical.features`` (default
        CANONICAL_FEATURES) followed by exploratory ``canonical.secondary_features``."""
        c = self.cfg.get("canonical") or {}
        return tuple(dict.fromkeys([*(c.get("features") or CANONICAL_FEATURES), *(c.get("secondary_features") or ())]))

    @property
    def levels_enabled(self) -> bool:
        """Validation levels A-E with full-trace regression (``validation_levels.enabled``; PILOT2_PROTOCOL)."""
        return bool((self.cfg.get("validation_levels") or {}).get("enabled"))

    @property
    def meta(self) -> dict[str, str]:
        """Study metadata stamped on every table, report and run record (empty if not configured)."""
        return config.study_metadata(self.cfg)

    @property
    def primary_panel(self) -> dict[str, frozenset[str]]:
        """protocol_id -> primary features. Only these decide classifications (D-029)."""
        c = self.cfg.get("canonical") or {}
        panel = {t.protocol_id: frozenset(t.features) for t in templates_from_config(self.cfg["protocols"])}
        panel[CANONICAL_ID] = frozenset(c.get("features") or CANONICAL_FEATURES)
        return panel

    @property
    def settle(self) -> float:
        return float(self.cfg["numerics"]["settle_ms"])


def make_context(campaign: str, workers: int | None = None, role: str = registry.EXPLORATORY_PILOT) -> Context:
    """Open ``campaign`` for writing under ``role``.

    Refuses sealed campaigns, a role different from the registered one, and a configuration
    or simulator different from the one the campaign was created with (a revision is a new
    campaign name, so every campaign's data stay reportable; DECISIONS D-027).
    """
    cfg = config.study()
    results = config.results_dir(cfg)
    registry.assert_writable(campaign, role, results)
    sim = JNeuroML(max_memory=cfg["numerics"]["java_max_memory"])
    if not sim.available():
        raise ToolFailure("Java/jNeuroML unavailable: run scripts/bootstrap_java.py")
    fcfg, tcfg = config.features(), config.tolerances()
    processed = results / "processed" / campaign
    snap = {"campaign": campaign, "role": role, "created_utc": utc_now(), "study_metadata": config.study_metadata(cfg),
            "configs": {p.path.name: p.sha256 for p in (cfg, fcfg, tcfg)}, "simulator": sim.version_info()}
    registry.check_config_snapshot(processed, snap)
    processed.mkdir(parents=True, exist_ok=True)
    registry.register(campaign, role, results)
    registry.snapshot_configs(processed, (cfg, fcfg, tcfg))
    snap_file = processed / "campaign_configs.json"
    if not snap_file.is_file():
        snap_file.write_text(json.dumps(snap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    meta = config.study_metadata(cfg)
    if meta:
        md_file = processed / "STUDY_METADATA.json"
        md = {**meta, "campaign": campaign, "campaign_role": role, "config_set_sha256": config.config_set_sha256()}
        if md_file.is_file() and json.loads(md_file.read_text(encoding="utf-8")) != md:
            raise registry.CampaignError(f"study metadata of campaign {campaign!r} changed ({md_file}); "
                                         "start a new campaign name")
        md_file.write_text(json.dumps(md, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
    trace_tol: dict = dc.field(default_factory=dict)   # protocol_id -> TraceTolerance


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
    canonical = canonical_protocol(ws, ctx.canonical_features)
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

    trace_tol = {}
    if ctx.levels_enabled:
        trace_tol = tr.calibrate(tr.load_traces(ctx.rec.raw, fps[1].run_ids), tr.load_traces(ctx.rec.raw, fps[2].run_ids),
                                 model_id, float(ctx.tcfg["c_refinement"]))

    # Deterministic re-execution (M2 exit criterion): replicate the nominal battery and canonical runs.
    rep = ctx.rec.run_battery(ws, variant, protocols, ctx.nominal, replicate=1, need_traces=True)
    base = ctx.rec.run_battery(ws, variant, protocols, ctx.nominal, replicate=0, need_traces=True)
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
    if trace_tol:
        tr.save_tolerances(trace_tol, out / "trace_tolerances.json")
    return RefState(ws, variant, st, canonical, protocols, rheobase, rh.result.status, fps, determinism, trace_tol)


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
    _write_table(ctx.meta, ctx.processed / "convergence.csv", report)
    return table


# --------------------------------------------------------------------------- variants
def generate_stage(ctx: Context, refs: dict[str, RefState], families: Sequence[str], n_mutants: int,
                   n_transforms: int, seed: int) -> list[VariantRecord]:
    from neuraxis import mutations, transforms

    excluded = list((ctx.cfg.get("pilot") or {}).get("exclude_operators") or [])
    mut_ops = strata.select_mutation_operators(families, excluded)
    tr_ops = list(transforms.REGISTRY)
    (ctx.processed / "generation.json").write_text(json.dumps(
        {"families": list(families), "operators": mut_ops, "excluded_operators": excluded, "n_per_operator": n_mutants,
         "transform_operators": tr_ops, "n_per_transform": n_transforms, "seed": seed, "study_metadata": ctx.meta,
         "severity_levels": (ctx.cfg.get("pilot") or {}).get("severity_levels"),
         "sites_per_severity": (ctx.cfg.get("pilot") or {}).get("sites_per_severity")},
        indent=2) + "\n",
        encoding="utf-8")
    pcfg = ctx.cfg.get("pilot") or {}
    selector = None
    if pcfg.get("severity_levels"):
        from neuraxis.mutations.severity import select_sites

        levels = list(pcfg["severity_levels"])
        per = dict(pcfg.get("sites_per_severity") or {})
        without = int(pcfg.get("sites_without_severity", 1))

        def selector(op, sites):  # noqa: ANN001, ANN202
            return select_sites(sites, op.name, seed, levels, int(per.get(op.name, per.get("default", 1))), without)
    records: list[VariantRecord] = []
    for mid in refs:
        model = refs[mid].ws.model
        # Both generators write to root/<model_id>/<variant_id>/.
        records += mutations.generate_mutants(model, mut_ops, n_mutants, seed, ctx.variants_root / "mutants",
                                              selector=selector)
        records += transforms.generate_transforms(model, tr_ops, n_transforms, seed, ctx.variants_root / "transforms")
    mutants = [r for r in records if r.kind is VariantKind.MUTANT]
    trans = [r for r in records if r.kind is not VariantKind.MUTANT]
    mutations.write_manifest(mutants, ctx.processed / "mutation_manifest.csv")
    transforms.write_manifest(trans, ctx.processed / "valid_transforms.csv")
    return records


def variant_dir(ctx: Context, v: VariantRecord) -> Path:
    sub = "mutants" if v.kind is VariantKind.MUTANT else "transforms"
    return ctx.variants_root / sub / v.model_id / v.variant_id


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
    canonical_runs_battery_failed: bool = False   # shipped harness runs, but the model fails when reused
    stratum: str = ""
    secondary_h: list[Detection] = dc.field(default_factory=list)          # exploratory features (D-029)
    secondary_h2: list[Detection] | None = None
    secondary_reproducible: list[str] = dc.field(default_factory=list)     # "protocol:feature"
    trace_h: list = dc.field(default_factory=list)                          # full-trace regression (level C/D)
    trace_h2: list | None = None
    trace_reproducible: list[str] = dc.field(default_factory=list)          # "protocol:metric"
    levels: dict = dc.field(default_factory=dict)                           # validation levels A-E and survivors
    survivor_check: dict = dc.field(default_factory=dict)                   # h/4 confirmation of canonical survivors


def _variant_one(ctx: Context, ref: RefState, tol: ToleranceTable, v: VariantRecord) -> VariantOutcome:
    from neuraxis.mutations import load_variant

    ws, loaded = load_variant(variant_dir(ctx, v))
    if loaded.variant_id != v.variant_id or loaded.tree_sha256 != ws.tree_sha256():
        raise RuntimeError(f"variant workspace {v.variant_id} does not match its record (edited after generation?)")
    out = ctx.processed / "variants" / v.variant_id
    out.mkdir(parents=True, exist_ok=True)
    st = structural.check(ws, ctx.sim, reference=ref.structural)
    if st.valid is None:
        raise ToolFailure(f"validator unavailable for {v.variant_id}")
    (out / "structural.json").write_text(json.dumps(to_jsonable(st), indent=2) + "\n", encoding="utf-8")
    s = strata.variant_stratum(v)
    strata.check_identical_numerics(v)       # primary semantic mutants and controls: reference numerics only
    if not st.valid:
        k = classify(False, None, None, [], None)
        return VariantOutcome(v, False, st.libneuroml_strict, "not_run", k, [], None, [], False, 0.0, stratum=s)
    panel = ctx.primary_panel

    def level(f: int) -> tuple[Fingerprint, list[Detection], list[Detection]]:
        fp = build_fingerprint(ctx.rec, ws, v, ref.protocols, ref.canonical, ctx.nominal, f, ctx.rcfg, ctx.settle)
        save_fingerprint(fp, out / f"fingerprint_L{f}.json")
        prim, sec = strata.split_primary(compare(ref.fps[f], fp, tol) if fp.status is RunStatus.OK else [], panel)
        return fp, prim, sec

    def trace_level(fp: Fingerprint | None, f: int) -> list:
        if not (ctx.levels_enabled and ref.trace_tol and fp is not None and fp.status is RunStatus.OK):
            return []
        return tr.compare(tr.load_traces(ctx.rec.raw, ref.fps[f].run_ids), tr.load_traces(ctx.rec.raw, fp.run_ids),
                          ref.trace_tol, v.variant_id, v.model_id, f)

    fp_h, det_h, sec_h = level(1)
    tr_h = trace_level(fp_h, 1)
    runtime = fp_h.runtime_s
    fp_h2 = det_h2 = sec_h2 = None
    tr_h2 = None
    # h/2 confirms reproducibility. It also runs when only secondary features detect (for their report) and for
    # every numerical stress test (convergence workflow); neither can change the primary class, which uses the
    # h/2 fingerprint only when the PRIMARY panel detected at h -- exactly the original rule.
    if fp_h.status is RunStatus.OK and (det_h or sec_h or tr_h or s == strata.NUMERICAL):
        fp_h2, det_h2, sec_h2 = level(2)
        tr_h2 = trace_level(fp_h2, 2)
        runtime += fp_h2.runtime_s
        if s == strata.NUMERICAL and fp_h2.status is RunStatus.OK and 4 in ref.fps:
            runtime += level(4)[0].runtime_s
    k = classify(True, fp_h, fp_h2 if det_h else None, det_h, det_h2 if det_h else None)
    write_detections(det_h + ((det_h2 or []) if det_h else []), out / "detections.csv", extra=ctx.meta)
    write_detections(sec_h + (sec_h2 or []), out / "detections_secondary.csv", extra=ctx.meta)
    dprot = sorted(detecting_protocols(det_h, det_h2 if det_h else None)) if k.admissible else []
    split_fate = (fp_h.status is not RunStatus.OK and CANONICAL_ID in fp_h.tables
                  and bool(fp_h.tables[CANONICAL_ID]))
    sec_keys = sorted(f"{p}:{f}" for p, f in reproducible_keys(sec_h, sec_h2))
    levels, survivor_check, tr_extra = {}, {}, []
    tr_keys = tr.reproducible(tr_h, tr_h2)
    if ctx.levels_enabled:
        prim_keys = reproducible_keys(det_h, det_h2)
        all_keys = prim_keys | reproducible_keys(sec_h, sec_h2) | tr_keys
        basic = k not in (MutantClass.STRUCTURALLY_INVALID, MutantClass.NON_EXECUTABLE, MutantClass.NUMERICALLY_UNSTABLE)
        b = any(p == CANONICAL_ID for p, _ in prim_keys)
        c = any(p == CANONICAL_ID for p, _ in tr_keys)
        d = any(p != CANONICAL_ID for p, _ in prim_keys | tr_keys)
        levels = {"A_basic_pass": basic, "B_canonical_feature": b, "C_canonical_trace": c, "D_multi_protocol": d,
                  "E_full_battery": bool(all_keys), "feature_level_canonical_survivor": basic and d and not b,
                  "full_trace_canonical_survivor": basic and d and not b and not c}
        if levels["feature_level_canonical_survivor"] and 4 in ref.fps:
            # Every apparent canonical survivor is re-checked one refinement level further (h/4).
            fp_h4, det_h4, _ = level(4)
            tr_extra = trace_level(fp_h4, 4)
            runtime += fp_h4.runtime_s
            keys4 = {(x.protocol_id, x.feature) for x in det_h4} | {(x.protocol_id, x.metric) for x in tr_extra}
            battery = {kk for kk in prim_keys | tr_keys if kk[0] != CANONICAL_ID}
            persist = sorted(f"{a}:{m}" for a, m in battery & keys4)
            can_f4 = any(x.protocol_id == CANONICAL_ID for x in det_h4)
            can_t4 = any(x.protocol_id == CANONICAL_ID for x in tr_extra)
            ok4 = fp_h4.status is RunStatus.OK
            survivor_check = {"h4_status": fp_h4.status.value, "battery_detections_persisting_at_h4": persist,
                              "canonical_feature_detects_at_h4": can_f4, "canonical_trace_detects_at_h4": can_t4,
                              "feature_survivor_confirmed": ok4 and bool(persist) and not can_f4,
                              "full_trace_survivor_confirmed": (ok4 and bool(persist) and not can_f4 and not can_t4
                                                                and levels["full_trace_canonical_survivor"])}
    tr.write_detections(tr_h + (tr_h2 or []) + tr_extra, out / "detections_trace.csv", ctx.meta)
    outcome = VariantOutcome(v, True, st.libneuroml_strict, fp_h.status.value, k, det_h, det_h2 if det_h else None,
                             dprot, any(d.protocol_id == CANONICAL_ID for d in det_h), round(runtime, 3), split_fate,
                             stratum=s, secondary_h=sec_h, secondary_h2=sec_h2, secondary_reproducible=sec_keys,
                             trace_h=tr_h + tr_extra, trace_h2=tr_h2,
                             trace_reproducible=sorted(f"{p}:{m}" for p, m in tr_keys), levels=levels,
                             survivor_check=survivor_check)
    _write_diagnostic(ctx, outcome, fp_h, fp_h2, out / "diagnostic.md")
    return outcome


def variant_stage(ctx: Context, refs: dict[str, RefState], tol: ToleranceTable,
                  variants: Sequence[VariantRecord]) -> list[VariantOutcome]:
    tasks = [lambda v=v: _variant_one(ctx, refs[v.model_id], tol, v) for v in variants]
    return _unwrap(run_parallel(tasks, ctx.workers), "variant")


def load_variant_records(ctx: Context) -> list[VariantRecord]:
    recs = []
    for p in sorted([*ctx.variants_root.glob("mutants/*/*/variant.json"), *ctx.variants_root.glob("transforms/*/*/variant.json")]):
        recs.append(variant_from_dict(json.loads(p.read_text(encoding="utf-8"))))
    return recs


# --------------------------------------------------------------------------- aggregation
def _cascade(mutants: Sequence[VariantOutcome]) -> dict[str, int]:
    return {
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


def _severity(v: VariantRecord) -> str:
    from neuraxis.mutations.severity import NOT_APPLICABLE, severity

    return severity(v.params) if v.kind is VariantKind.MUTANT else NOT_APPLICABLE


def _stratum(o: VariantOutcome) -> str:
    return o.stratum or strata.variant_stratum(o.variant)


def aggregate(ctx: Context, refs: dict[str, RefState], outcomes: Sequence[VariantOutcome]) -> dict[str, Any]:
    """Write campaign tables. The primary tables (classification cascade, detection matrix, silent list)
    cover the semantic stratum only; numerical stress tests and secondary features get their own files."""
    p = ctx.processed
    rows = []
    for o in outcomes:
        v = o.variant
        rows.append({"variant_id": v.variant_id, "model_id": v.model_id, "kind": v.kind.value, "family": v.family,
                     "stratum": _stratum(o), "interpretation": strata.interpretation(_stratum(o), o.klass),
                     "analysis_family": strata.analysis_family(v.operator, v.family),
                     "severity": _severity(v), **{f"level_{kk}": vv for kk, vv in o.levels.items()},
                     "survivor_confirmed_h4": o.survivor_check.get("feature_survivor_confirmed", ""),
                     "full_trace_survivor_confirmed_h4": o.survivor_check.get("full_trace_survivor_confirmed", ""),
                     "trace_reproducible": ";".join(o.trace_reproducible),
                     "secondary_reproducible": ";".join(o.secondary_reproducible),
                     "operator": v.operator, "params": json.dumps(v.params, sort_keys=True), "class": o.klass.value,
                     "admissible": o.klass.admissible, "structural_valid": o.structural_valid,
                     "libneuroml_strict": o.libneuroml_strict, "status_h": o.status_h,
                     "n_detections_h": len(o.detections_h),
                     "n_detections_h2": "" if o.detections_h2 is None else len(o.detections_h2),
                     "canonical_detected_h": o.canonical_detected,
                     "canonical_detected_reproducible": CANONICAL_ID in o.detecting_protocols,
                     "detecting_protocols": ";".join(o.detecting_protocols),
                     "canonical_runs_but_battery_failed": o.canonical_runs_battery_failed,
                     "runtime_s": o.runtime_s})
    _write_table(ctx.meta, p /"classification.csv", rows)
    write_detections([d for o in outcomes for d in o.detections_h + (o.detections_h2 or [])], p / "detections.csv", extra=ctx.meta)
    write_detections([d for o in outcomes for d in o.secondary_h + (o.secondary_h2 or [])],
                     p / "detections_secondary.csv", extra=ctx.meta)
    if ctx.levels_enabled:
        tr.write_detections([d for o in outcomes for d in o.trace_h + (o.trace_h2 or [])], p / "detections_trace.csv",
                            ctx.meta)
        (p / "survivor_checks.json").write_text(json.dumps(
            {o.variant.variant_id: o.survivor_check for o in outcomes if o.survivor_check}, indent=2) + "\n",
            encoding="utf-8")

    # Detection matrix over admissible PRIMARY SEMANTIC mutants; columns = canonical + battery + rheobase.
    first_ref = next(iter(refs.values()))
    protocol_ids = [CANONICAL_ID] + [q.protocol_id for q in first_ref.protocols] + [RHEOBASE_ID]
    cost = {pid: float(np.mean([r.fps[1].cell_steps.get(pid, 0) for r in refs.values()])) for pid in protocol_ids}
    from neuraxis.selection.matrix import DetectionMatrix

    def write_matrix(adm: Sequence[VariantOutcome], path: Path) -> None:
        DetectionMatrix.from_detected_sets(
            [o.variant.variant_id for o in adm], protocol_ids,
            {o.variant.variant_id: set(o.detecting_protocols) for o in adm},
            {o.variant.variant_id: o.variant.model_id for o in adm},
            {o.variant.variant_id: o.variant.family for o in adm}, cost).to_csv(path)

    write_matrix(strata.primary_admissible(outcomes), p / "detection_matrix.csv")
    mutants_all = [o for o in outcomes if o.variant.kind is VariantKind.MUTANT]
    numerical = [o for o in mutants_all if _stratum(o) == strata.NUMERICAL]
    if any(o.klass.admissible for o in numerical):
        write_matrix([o for o in numerical if o.klass.admissible], p / "detection_matrix_numerical_robustness.csv")
    _write_table(ctx.meta, p /"protocol_costs.csv", [{"protocol_id": k, "mean_cell_steps": v} for k, v in cost.items()])

    mutants = [o for o in mutants_all if _stratum(o) == strata.SEMANTIC]
    cascade = _cascade(mutants)
    cascade_num = _cascade(numerical)
    (p / "validation_cascade.json").write_text(json.dumps({**cascade, "study_metadata": ctx.meta}, indent=2) + "\n",
                                               encoding="utf-8")
    (p / "validation_cascade_numerical_robustness.json").write_text(
        json.dumps({**cascade_num, "study_metadata": ctx.meta}, indent=2) + "\n", encoding="utf-8")

    # Numerical robustness and convergence stress tests: deviation vs the reference's discretisation error.
    nr_rows: list[dict] = []
    for o in numerical:
        vdir = p / "variants" / o.variant.variant_id
        var_fps = {f: load_fingerprint(vdir / f"fingerprint_L{f}.json") for f in (1, 2, 4)
                   if (vdir / f"fingerprint_L{f}.json").is_file()}
        if var_fps:
            nr_rows += strata.numerical_robustness_rows(refs[o.variant.model_id].fps, var_fps, o.variant,
                                                        float(ctx.tcfg["c_refinement"]))
    _write_table(ctx.meta, p /"numerical_robustness.csv", nr_rows)

    # Secondary exploratory features: reported, never used to change a primary class (D-029).
    sec_rows = [{"variant_id": o.variant.variant_id, "model_id": o.variant.model_id, "stratum": _stratum(o),
                 "operator": o.variant.operator, "primary_class": o.klass.value, "primary_admissible": o.klass.admissible,
                 "primary_detecting_protocols": ";".join(o.detecting_protocols),
                 "secondary_reproducible": ";".join(o.secondary_reproducible),
                 "secondary_features": ";".join(sorted({k.split(":", 1)[1] for k in o.secondary_reproducible})),
                 "secondary_detects_primary_miss": o.klass is MutantClass.EQUIVALENT and bool(o.secondary_reproducible),
                 "canonical_secondary_only": (CANONICAL_ID not in o.detecting_protocols and
                                              any(k.startswith(CANONICAL_ID + ":") for k in o.secondary_reproducible))}
                for o in mutants_all]
    _write_table(ctx.meta, p /"secondary_feature_report.csv", sec_rows)

    transforms_ = [o for o in outcomes if o.variant.kind is not VariantKind.MUTANT]
    fp_rows = [{"variant_id": o.variant.variant_id, "model_id": o.variant.model_id, "kind": o.variant.kind.value,
                "operator": o.variant.operator, "class": o.klass.value, "false_positive": o.klass.admissible,
                "detected_at_h_only": bool(o.detections_h) and not o.klass.admissible,
                "detections": ";".join(sorted({f"{d.protocol_id}:{d.feature}" for d in o.detections_h}))}
               for o in transforms_]
    _write_table(ctx.meta, p /"false_positives.csv", fp_rows)

    audit = [{"variant_id": o.variant.variant_id, "operator": o.variant.operator, "family": o.variant.family,
              "stratum": _stratum(o), "edits": json.dumps([dc.asdict(e) for e in o.variant.edits]),
              "exec_overrides": json.dumps(o.variant.exec_overrides), "assigned_class": o.klass.value,
              "detecting_protocols": ";".join(o.detecting_protocols),
              "human_auditor": "", "edit_matches_label (yes/no)": "", "class_plausible (yes/no)": "", "notes": ""}
             for o in mutants_all]
    _write_table(ctx.meta, p /"mutant_audit_sheet.csv", audit)
    by_stratum: dict[str, Counter] = {}
    for o in outcomes:
        by_stratum.setdefault(_stratum(o), Counter())[o.klass.value] += 1
    return {"cascade": cascade, "cascade_numerical_robustness": cascade_num,
            "classes": Counter(o.klass.value for o in outcomes), "classes_by_stratum": by_stratum,
            "false_positives": sum(r["false_positive"] for r in fp_rows), "n_transforms": len(fp_rows),
            "silent": [o.variant.variant_id for o in mutants if o.klass is MutantClass.SILENT],
            "numerical_missed_by_canonical": [o.variant.variant_id for o in numerical if o.klass is MutantClass.SILENT],
            "secondary_primary_miss": [r["variant_id"] for r in sec_rows if r["secondary_detects_primary_miss"]],
            "n_semantic_mutants": len(mutants), "n_numerical_mutants": len(numerical),
            "n_numerical_robustness_rows": len(nr_rows)}


def _write_rows(path: Path, rows: Sequence[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = fieldnames or (list(rows[0].keys()) if rows else ["empty"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})


def _write_table(meta: dict[str, str], path: Path, rows: Sequence[dict]) -> None:
    """Result table with the study metadata as leading columns (an empty table keeps one metadata row)."""
    if meta:
        rows = [{**meta, **r} for r in rows] if rows else [{**meta, "rows": 0}]
    _write_rows(path, rows)


def _write_diagnostic(ctx: Context, o: VariantOutcome, fp_h: Fingerprint, fp_h2: Fingerprint | None, path: Path) -> None:
    """Per-mutant diagnostic (M5 exit criterion): every detection -> protocol, feature, threshold, evidence."""
    lines = [f"# {o.variant.variant_id}", ""]
    if ctx.meta:
        lines += [f"*{config.designation_text(ctx.cfg)}*", ""]
    lines += [f"- model: `{o.variant.model_id}`", f"- stratum: {o.stratum}", f"- kind/family/operator: "
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
