"""Perturbation fingerprints, detections and the six-way mutant classification.

A *fingerprint* is the table of features a model produces across every protocol at one
refinement level: F(m) = { f(m, p) : p in P, f in E } (spec "Fingerprint definition"),
plus rheobase and the canonical (shipped) protocol.

A *detection* is one (protocol, feature) whose variant value differs from the reference
by more than the calibrated tolerance, or whose defined/undefined state or category
changes. Every detection carries both run ids, so the evidence traces can be inspected.

Non-equivalence requires reproducibility: the same (protocol, feature) must be detected
at the nominal step h AND at h/2. A difference that vanishes under refinement is treated
as solver error, not as behavioural drift (spec pivot criterion).
"""

from __future__ import annotations

import csv
import dataclasses as dc
import json
import math
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from neurosem.models import Workspace
from neurosem.protocols.definitions import CANONICAL_ID
from neurosem.schemas import ConcreteProtocol, ExecConfig, MutantClass, RunStatus, VariantRecord, to_jsonable
from neurosem.validation.convergence import ToleranceTable
from neurosem.validation.execution import RunRecorder, worst_status

RHEOBASE_ID = "P03_rheobase"


class ToolFailure(RuntimeError):
    """The toolchain (not the model) failed; results must not be classified."""


@dc.dataclass
class Fingerprint:
    model_id: str
    variant_id: str
    level_factor: int
    dt_ms: float
    status: RunStatus
    rheobase: dict | None
    tables: dict[str, dict]                 # protocol_id -> FeatureTable
    run_ids: dict[str, str]                 # protocol_id -> run_id (or rheobase search id)
    messages: list[str] = dc.field(default_factory=list)
    runtime_s: float = 0.0
    cell_steps: dict[str, int] = dc.field(default_factory=dict)   # protocol_id -> simulated cell-steps (cost)


@dc.dataclass
class Detection:
    variant_id: str
    model_id: str
    level_factor: int
    protocol_id: str
    feature: str
    reason: str                              # exceeds | definedness | categorical
    ref_value: float | str | None
    var_value: float | str | None
    diff: float | None
    tau: float | None
    ref_run_id: str
    var_run_id: str


def build_fingerprint(rec: RunRecorder, ws: Workspace, variant: VariantRecord, protocols: Sequence[ConcreteProtocol],
                      canonical_proto: ConcreteProtocol, nominal: ExecConfig, level_factor: int, rcfg: dict,
                      settle_ms: float, *, include_rheobase: bool = True, include_canonical: bool = True,
                      replicate: int = 0) -> Fingerprint:
    from neurosem.features.efel_adapter import FeatureValue

    level_exec = nominal.with_dt(nominal.dt_ms / level_factor)
    tables: dict[str, dict] = {}
    run_ids: dict[str, str] = {}
    statuses: list[RunStatus] = []
    messages: list[str] = []
    runtime = 0.0
    cost: dict[str, int] = {}

    battery = rec.run_battery(ws, variant, protocols, level_exec, replicate=replicate)
    statuses.append(battery.status)
    messages += battery.messages
    tables.update(battery.tables)
    for r in battery.records:
        runtime += r.runtime_s
        steps = int(round(r.duration_ms / r.dt_ms))
        for pid in r.protocol_ids:
            run_ids[pid] = r.run_id
            cost[pid] = steps

    if include_canonical:
        can = rec.run_canonical(ws, variant, canonical_proto, level_factor=level_factor, replicate=replicate)
        statuses.append(can.status)
        messages += can.messages
        tables.update(can.tables)
        for r in can.records:
            runtime += r.runtime_s
            run_ids[CANONICAL_ID] = r.run_id
            cost[CANONICAL_ID] = int(round(r.duration_ms / r.dt_ms))

    rheo = None
    if include_rheobase:
        out = rec.run_rheobase(ws, variant, level_exec, rcfg, settle_ms)
        statuses.append(out.status)
        rheo = dc.asdict(out.result)
        run_ids[RHEOBASE_ID] = out.search_id
        runtime += out.record.get("runtime_s", 0.0)
        cost[RHEOBASE_ID] = int(out.record.get("cell_steps", 0))
        r = out.result
        if out.status is RunStatus.OK and r.status in ("ok", "spontaneous"):
            fv = FeatureValue("rheobase", float(r.rheobase_nA), "defined", "nA", f"neurosem:rheobase[{r.status}]")
        else:
            fv = FeatureValue("rheobase", None, "undefined", "nA", f"neurosem:rheobase[{r.status}]")
        tables[RHEOBASE_ID] = {"rheobase": fv}

    status = worst_status(statuses)
    if status is RunStatus.TOOL_FAILURE:
        raise ToolFailure(f"toolchain failure while fingerprinting {variant.variant_id}: {messages}")
    return Fingerprint(variant.model_id, variant.variant_id, level_factor, level_exec.dt_ms, status, rheo, tables,
                       run_ids, messages, round(runtime, 3), cost)


def compare(ref: Fingerprint, var: Fingerprint, tol: ToleranceTable, multiplier: float = 1.0) -> list[Detection]:
    if ref.model_id != var.model_id:
        raise ValueError("fingerprints belong to different models")
    out: list[Detection] = []
    for pid, table in sorted(ref.tables.items()):
        vtable = var.tables.get(pid)
        if vtable is None:
            continue                         # protocol did not run for the variant; reflected in its status
        for feat, rv in sorted(table.items()):
            entry = tol.get(ref.model_id, pid, feat)
            if entry is None or entry.excluded:
                continue
            vv = vtable.get(feat)
            if vv is None:
                continue
            common = dict(variant_id=var.variant_id, model_id=var.model_id, level_factor=var.level_factor,
                          protocol_id=pid, feature=feat, ref_value=rv.value, var_value=vv.value,
                          ref_run_id=ref.run_ids.get(pid, ""), var_run_id=var.run_ids.get(pid, ""))
            r_def, v_def = rv.state == "defined", vv.state == "defined"
            if r_def != v_def:
                out.append(Detection(**common, reason="definedness", diff=None, tau=entry.tau))
                continue
            if not r_def:
                continue
            if entry.kind == "categorical":
                if rv.value != vv.value:
                    out.append(Detection(**common, reason="categorical", diff=None, tau=None))
                continue
            diff = abs(float(vv.value) - float(rv.value))
            tau = entry.tau * multiplier if entry.tau is not None and math.isfinite(entry.tau) else entry.tau
            if tau is not None and diff > tau:
                out.append(Detection(**common, reason="exceeds", diff=diff, tau=tau))
    return out


def reproducible_keys(det_h: Sequence[Detection], det_h2: Sequence[Detection] | None) -> set[tuple[str, str]]:
    if det_h2 is None:
        return set()
    return {(d.protocol_id, d.feature) for d in det_h} & {(d.protocol_id, d.feature) for d in det_h2}


def classify(structural_valid: bool | None, fp_h: Fingerprint | None, fp_h2: Fingerprint | None,
             det_h: Sequence[Detection], det_h2: Sequence[Detection] | None) -> MutantClass:
    """Spec "Mutant classification".

    One detection rule everywhere: a protocol "detects" a mutant only if some feature is
    detected at h AND at h/2. This applies to the canonical protocol too, so SILENT (class 6)
    uses exactly the canonical rule of the detection matrix and the primary endpoint.
    """
    if structural_valid is None:
        raise ToolFailure("structural validation could not be performed")
    if structural_valid is False:
        return MutantClass.STRUCTURALLY_INVALID
    for fp in (fp_h, fp_h2):
        if fp is None:
            continue
        if fp.status in (RunStatus.BUILD_ERROR, RunStatus.RUNTIME_ERROR, RunStatus.TIMEOUT, RunStatus.INVALID):
            return MutantClass.NON_EXECUTABLE
        if fp.status is RunStatus.UNSTABLE:
            return MutantClass.NUMERICALLY_UNSTABLE
    if fp_h is None:
        raise ValueError("nominal fingerprint required")
    keys = reproducible_keys(det_h, det_h2)
    if not keys:
        return MutantClass.EQUIVALENT
    canonical_detects = any(pid == CANONICAL_ID for pid, _ in keys)
    battery_detects = any(pid != CANONICAL_ID for pid, _ in keys)
    if not canonical_detects and battery_detects:
        return MutantClass.SILENT
    return MutantClass.NON_EQUIVALENT


def detecting_protocols(det_h: Sequence[Detection], det_h2: Sequence[Detection] | None) -> set[str]:
    """Protocols with at least one reproducible detection (a detection-matrix row)."""
    return {pid for pid, _ in reproducible_keys(det_h, det_h2)}


# ------------------------------------------------------------------ serialisation
def fingerprint_to_json(fp: Fingerprint) -> dict[str, Any]:
    from neurosem.features.efel_adapter import feature_table_to_json

    d = to_jsonable(dc.replace(fp, tables={}))
    d["tables"] = {pid: feature_table_to_json(t) for pid, t in fp.tables.items()}
    return d


def fingerprint_from_json(d: dict[str, Any]) -> Fingerprint:
    from neurosem.features.efel_adapter import feature_table_from_json

    d = dict(d)
    d["status"] = RunStatus(d["status"])
    d["tables"] = {pid: feature_table_from_json(t) for pid, t in d["tables"].items()}
    return Fingerprint(**d)


def save_fingerprint(fp: Fingerprint, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fingerprint_to_json(fp), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_fingerprint(path: Path) -> Fingerprint:
    return fingerprint_from_json(json.loads(path.read_text(encoding="utf-8")))


DETECTION_COLUMNS = [f.name for f in dc.fields(Detection)]


def write_detections(dets: Sequence[Detection], path: Path, extra: dict[str, str] | None = None) -> None:
    """Detections CSV; ``extra`` adds constant leading columns (study metadata)."""
    extra = dict(extra or {})
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[*extra, *DETECTION_COLUMNS], lineterminator="\n")
        w.writeheader()
        for d in dets:
            w.writerow({**extra, **{k: ("" if v is None else v) for k, v in dc.asdict(d).items()}})
