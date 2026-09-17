"""Execution with provenance (validation layer 2) -- every simulation goes through here.

Each run happens in a private staging copy of the variant workspace. Its ``run_id`` is
content-addressed from every file the simulator reads plus the execution settings and
the simulator build, so:

* identical inputs are never simulated twice (a stimulus-only mutant reuses the
  reference battery, because the files the battery reads are byte-identical);
* raw results are write-once (``provenance.write_immutable``); a rerun whose traces are
  missing locally is re-simulated and must reproduce the recorded trace hash exactly.

Traces are stored in the ARCHITECTURE.md section 2 format and features are extracted from
that stored representation, so derived tables reproduce exactly from raw files.
"""

from __future__ import annotations

import concurrent.futures as cf
import dataclasses as dc
import functools
import json
import re
import shutil
import threading
import traceback
import uuid
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from neuraxis import config
from neuraxis.models import Workspace, copy_workspace
from neuraxis.protocols import rheobase as rb
from neuraxis.protocols.generate import DEFAULT_SEED, canonical_output, group_by_length, harness_step_and_length, write_probe
from neuraxis.provenance import (environment_digest, git_state, relpath, sha256_bytes,
                                 sha256_file, sha256_json, utc_now, write_immutable, write_immutable_text)
from neuraxis.schemas import (ConcreteProtocol, ExecConfig, RunRecord, RunStatus, Trace, VariantKind, VariantRecord,
                              dumps)
from neuraxis.simulators.base import Simulator
from neuraxis import units

_INCLUDE_RE = re.compile(r'<(?:include\s+href|Include\s+file)\s*=\s*"([^"]+)"', re.IGNORECASE)
_BUILTIN = {"Cells.xml", "Networks.xml", "Simulation.xml", "Inputs.xml", "Channels.xml", "Synapses.xml", "PyNN.xml",
            "NeuroML2CoreTypes.xml", "NeuroMLCoreDimensions.xml", "NeuroMLCoreCompTypes.xml"}

# Worst-first ordering used to summarise several runs of one fingerprint.
STATUS_SEVERITY = [RunStatus.TOOL_FAILURE, RunStatus.INVALID, RunStatus.BUILD_ERROR, RunStatus.RUNTIME_ERROR,
                   RunStatus.TIMEOUT, RunStatus.UNSTABLE, RunStatus.OK]


class ReproducibilityError(RuntimeError):
    """A re-simulation produced different bytes than the immutable record."""


# Bumped whenever simulation generation changes in a way that could alter generated inputs or outcomes.
GENERATION_VERSION = 2          # 2: candidate temperature fields normalised (deviation X-19)
# Source files that write or read the simulator's inputs and outputs. A change here invalidates caches.
_GENERATION_SOURCES = ("protocols/generate.py", "protocols/definitions.py", "protocols/rheobase.py",
                       "simulators/jneuroml.py", "validation/canonical.py", "validation/execution.py")


@functools.lru_cache(maxsize=1)
def generation_code_digest() -> str:
    """Digest of the code that generates and runs simulations (never reuse a cache across such changes)."""
    root = Path(__file__).resolve().parents[1]
    return sha256_json({rel: sha256_file(root / rel) for rel in _GENERATION_SOURCES})


@functools.lru_cache(maxsize=1)
def feature_code_digest() -> str:
    """Digest of the feature-extraction source, so changed feature code never reuses stale features."""
    d = Path(__file__).resolve().parents[1] / "features"
    return sha256_json({p.name: sha256_file(p) for p in sorted(d.glob("*.py"))})


def worst_status(statuses: Sequence[RunStatus]) -> RunStatus:
    return min(statuses, key=STATUS_SEVERITY.index) if statuses else RunStatus.OK


def reachable_files(entry: Path) -> list[Path]:
    """``entry`` plus every local file reachable through NeuroML/LEMS include statements."""
    seen: dict[Path, None] = {}
    stack = [entry.resolve()]
    while stack:
        p = stack.pop()
        if p in seen or not p.is_file():
            continue
        seen[p] = None
        if p.suffix.lower() not in (".nml", ".xml"):
            continue
        for inc in _INCLUDE_RE.findall(p.read_text(encoding="utf-8", errors="replace")):
            if inc.startswith(("http://", "https://")) or Path(inc).name in _BUILTIN or inc.startswith("NeuroML2CoreTypes/"):
                continue
            stack.append((p.parent / inc).resolve())
    return sorted(seen)


def inputs_manifest(entry: Path, root: Path) -> dict[str, str]:
    root = root.resolve()
    return {f.relative_to(root).as_posix(): sha256_file(f) for f in reachable_files(entry) if f.is_relative_to(root)}


def apply_overrides(exec_cfg: ExecConfig, overrides: dict[str, Any]) -> ExecConfig:
    out = exec_cfg
    if "dt_factor" in overrides:
        out = dc.replace(out, dt_ms=out.dt_ms * float(overrides["dt_factor"]))
    if "integrator_method" in overrides:
        out = dc.replace(out, integrator_method=str(overrides["integrator_method"]))
    if "sample_every_ms" in overrides:
        out = dc.replace(out, sample_every_ms=float(overrides["sample_every_ms"]))
    return out


def effective_workspace(ws: Workspace, variant: VariantRecord) -> Workspace:
    if not variant.model_overrides:
        return ws
    allowed = {f.name for f in dc.fields(ws.model)}
    bad = set(variant.model_overrides) - allowed
    if bad:
        raise ValueError(f"unknown model overrides {sorted(bad)}")
    return Workspace(ws.root, dc.replace(ws.model, **variant.model_overrides))


@dc.dataclass
class RunOutput:
    status: RunStatus
    records: list[RunRecord]
    traces: dict[str, Trace]
    tables: dict[str, dict]            # protocol_id -> FeatureTable
    cached: bool
    messages: list[str]


@dc.dataclass
class RheobaseOutcome:
    result: rb.RheobaseResult
    status: RunStatus
    search_id: str
    record: dict
    cached: bool


class RunRecorder:
    def __init__(self, campaign: str, sim: Simulator, *, results_root: Path | None = None, work_root: Path | None = None,
                 features_cfg: dict | None = None, timeout_s: float | None = None, store_traces: bool = True) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", campaign):
            raise ValueError("campaign names may contain only letters, digits, '_', '.', '-'")
        self.campaign = campaign
        self.sim = sim
        self.raw = (results_root or config.results_dir()) / "raw" / campaign
        self.runs = (work_root or config.work_dir()) / "runs" / campaign
        self.features_cfg = features_cfg if features_cfg is not None else config.features().data
        study = config.study()
        self.meta = config.study_metadata(study)
        self.config_sha256 = config.config_set_sha256()
        self.timeout_s = timeout_s or float(study["numerics"]["timeout_s"])
        self.git_commit = git_state()[0]
        self.store_traces = store_traces
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()
        self._env: tuple[str, dict] | None = None

    # ------------------------------------------------------------ helpers
    def env(self) -> tuple[str, dict]:
        if self._env is None:
            digest, env = environment_digest(extra={"simulator": self.sim.version_info()})
            write_immutable_text(self.raw / "_environments" / f"{digest}.json", json.dumps(env, indent=2, sort_keys=True) + "\n")
            self._env = (digest, env)
        return self._env

    def _lock(self, key: str) -> threading.Lock:
        with self._locks_guard:
            return self._locks.setdefault(key, threading.Lock())

    def _stage(self, ws: Workspace) -> Workspace:
        dest = self.runs / "_staging" / uuid.uuid4().hex
        dest.parent.mkdir(parents=True, exist_ok=True)
        return copy_workspace(ws, dest)

    def _discard(self, stage: Workspace, run_id: str, failed: bool) -> None:
        if failed:
            target = self.runs / "failed" / run_id
            if target.exists():
                shutil.rmtree(target, ignore_errors=True)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(stage.root), str(target))
        else:
            shutil.rmtree(stage.root, ignore_errors=True)

    def _jar_sha(self) -> str:
        return self.sim.version_info().get("jar_sha256", "unknown")

    def cache_context(self) -> dict[str, Any]:
        """Everything besides the simulation inputs that a cached run must match before it is reused.

        A cached simulation is identified by the hash of its whole payload, so any difference here
        (generation code, simulator or Java build, configuration) yields a different run id and the
        run is repeated rather than reused.
        """
        v = self.sim.version_info()
        return {"generation_version": GENERATION_VERSION, "generation_code": generation_code_digest(),
                "simulator": self.sim.name, "simulator_version": self.sim.version_string(),
                "java_version": v.get("java_version", "unknown"), "jar_sha256": v.get("jar_sha256", "unknown"),
                "config_sha256": self.config_sha256}

    def _run_id(self, payload: dict) -> str:
        return "r-" + sha256_json(payload)[:20]

    def features_key(self, trace_sha: str) -> str:
        """Features depend on the stored trace, the feature config, the eFEL build and NeuroSem's feature code."""
        import efel

        return sha256_json({"trace_sha256": trace_sha, "features_cfg": self.features_cfg, "efel": efel.__version__,
                            "feature_code": feature_code_digest()})[:16]

    def _extract_and_store(self, run_dir: Path, trace_sha: str, traces: dict[str, Trace],
                           protocols: Sequence[ConcreteProtocol]) -> tuple[dict[str, dict], str, str, int]:
        import efel

        from neuraxis.features import efel_adapter

        key = self.features_key(trace_sha)
        warnings: list[str] = []
        tables = efel_adapter.extract_all(traces, list(protocols), self.features_cfg, warnings=warnings)
        payload = {"features_key": key, "trace_sha256": trace_sha, "efel_version": efel.__version__,
                   "feature_code_digest": feature_code_digest(), "features_cfg_sha256": sha256_json(self.features_cfg),
                   "tables": {pid: efel_adapter.feature_table_to_json(t) for pid, t in tables.items()}}
        path = run_dir / f"features_{key}.json"
        sha = write_immutable_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")
        if warnings:
            write_immutable_text(run_dir / f"efel_warnings_{key}.txt", "\n".join(warnings) + "\n")
        return tables, relpath(path), sha, len(warnings)

    def _load_cached(self, run_dir: Path, protocols: Sequence[ConcreteProtocol], need_traces: bool = False,
                     cache_key: str = "") -> RunOutput | None:
        """Return a cached run, or None when it must be (re-)simulated.

        Features for the current features key are loaded from Git-tracked JSON even when the
        (Git-ignored) traces are absent; traces are re-simulated only when needed, and must
        then reproduce the recorded hash.
        """
        from neuraxis.features import efel_adapter, trace_metrics

        rj = run_dir / "run.json"
        if not rj.is_file():
            return None
        rec = RunRecord(**json.loads(rj.read_text(encoding="utf-8")))
        if cache_key and rec.cache_key_sha256 and rec.cache_key_sha256 != cache_key:
            # Cannot happen while the run id is the payload hash; checked anyway before any reuse.
            raise ReproducibilityError(f"{rec.run_id}: cached run does not match the current cache key")
        if rec.status == RunStatus.TOOL_FAILURE.value:
            # Legacy record of a toolchain failure: preserve it beside the run and allow the retry.
            keep = run_dir / "_tool_failures" / f"legacy_run_{uuid.uuid4().hex}.json"
            keep.parent.mkdir(parents=True, exist_ok=True)
            rj.replace(keep)
            return None
        for name in ("stdout", "stderr"):
            path, sha = getattr(rec, f"{name}_path"), getattr(rec, f"{name}_sha256")
            if path and sha and sha256_file(run_dir / f"{name}.txt") != sha:
                raise ReproducibilityError(f"stored {name} for {rec.run_id} does not match its record")
        if rec.status != RunStatus.OK.value:
            return RunOutput(RunStatus(rec.status), [rec], {}, {}, True, [rec.message])
        npz = run_dir / "traces.npz"
        traces: dict[str, Trace] = {}
        if npz.is_file():
            if sha256_file(npz) != rec.trace_sha256:
                raise ReproducibilityError(f"stored traces for {rec.run_id} do not match their record")
            traces = trace_metrics.unpack_traces(npz.read_bytes())
        elif need_traces:
            return None
        fj = run_dir / f"features_{self.features_key(rec.trace_sha256)}.json"
        if fj.is_file():
            tables = {pid: efel_adapter.feature_table_from_json(t)
                      for pid, t in json.loads(fj.read_text(encoding="utf-8"))["tables"].items()}
            return RunOutput(RunStatus.OK, [rec], traces, tables, True, [])
        if traces:
            tables, _, _, _ = self._extract_and_store(run_dir, rec.trace_sha256, traces, protocols)
            return RunOutput(RunStatus.OK, [rec], traces, tables, True, [])
        return None

    def _finish(self, *, run_id: str, run_kind: str, stage: Workspace, variant: VariantRecord, protocols: Sequence[ConcreteProtocol],
                dt_ms: float, duration_ms: float, result, replicate: int, started_utc: str = "",
                cache_key: str = "") -> RunOutput:
        from neuraxis.features import trace_metrics

        run_dir = self.raw / run_id
        digest, _ = self.env()
        commit, dirty = git_state()
        prior = run_dir / "run.json"
        prior_rec = RunRecord(**json.loads(prior.read_text(encoding="utf-8"))) if prior.is_file() else None
        trace_path = feature_path = trace_sha = feature_sha = ""
        tables: dict[str, dict] = {}
        traces: dict[str, Trace] = {}
        n_warnings = 0
        status = result.status
        execution_id = uuid.uuid4().hex
        if status is RunStatus.TOOL_FAILURE:
            # The toolchain failed, not the model: keep the attempt, but never let it block a permitted retry.
            write_immutable_text(run_dir / "_tool_failures" / f"{execution_id}.json", json.dumps(
                {"run_id": run_id, "execution_id": execution_id, "start_time": started_utc, "end_time": utc_now(),
                 "message": result.message, "command": result.command, "git_commit": commit, "git_dirty": dirty},
                indent=2) + "\n")
            self._discard(stage, run_id, failed=True)
            return RunOutput(status, [], {}, {}, False, [result.message])
        streams = {"stdout": ("", ""), "stderr": ("", "")}
        if prior_rec is None:
            for name in streams:
                text = getattr(result, name, "") or ""
                streams[name] = (relpath(run_dir / f"{name}.txt"), write_immutable_text(run_dir / f"{name}.txt", text))
        elif prior_rec.stdout_path:
            streams = {n: (getattr(prior_rec, f"{n}_path"), getattr(prior_rec, f"{n}_sha256")) for n in streams}
        if result.traces and status in (RunStatus.OK, RunStatus.UNSTABLE):
            packed = trace_metrics.pack_traces(result.traces, finite_only=status is RunStatus.OK)
            trace_sha = sha256_bytes(packed)
            if prior_rec is not None and prior_rec.trace_sha256 and prior_rec.trace_sha256 != trace_sha:
                raise ReproducibilityError(f"{run_id}: re-simulation changed the trace hash "
                                           f"({prior_rec.trace_sha256[:12]} -> {trace_sha[:12]})")
            if self.store_traces:
                write_immutable(run_dir / "traces.npz", packed)
                trace_path = relpath(run_dir / "traces.npz")
            traces = trace_metrics.unpack_traces(packed)
            if status is RunStatus.OK:
                tables, feature_path, feature_sha, n_warnings = self._extract_and_store(run_dir, trace_sha, traces, protocols)
        message = result.message
        if n_warnings:
            message = (message + " | " if message else "") + f"{n_warnings} eFEL warnings"
        rec = prior_rec or RunRecord(
            run_id=run_id, campaign=self.campaign, run_kind=run_kind, model_id=variant.model_id,
            variant_id=variant.variant_id, variant_tree_sha256=variant.tree_sha256,
            protocol_ids=[p.protocol_id for p in protocols], dt_ms=dt_ms, duration_ms=duration_ms, seed=DEFAULT_SEED,
            simulator=self.sim.name, simulator_version=self.sim.version_string(), environment_digest=digest,
            status=status.value, runtime_s=round(result.runtime_s, 3), trace_path=trace_path, trace_sha256=trace_sha,
            feature_path=feature_path, feature_sha256=feature_sha, timestamp_utc=utc_now(), git_commit=commit,
            git_dirty=dirty, replicate=replicate, message=message[:2000],
            project_name=self.meta.get("project_name", ""), study_id=self.meta.get("study_id", ""),
            study_phase=self.meta.get("study_phase", ""),
            protocol_version=self.meta.get("protocol_version", ""), config_sha256=self.config_sha256,
            execution_id=execution_id, model_hash=variant.tree_sha256, base_model_hash=variant.parent_tree_sha256,
            mutation_id=variant.variant_id if variant.kind is VariantKind.MUTANT else None,
            transformation_id=(variant.variant_id if variant.kind in (VariantKind.VALID_TRANSFORM, VariantKind.NO_CHANGE)
                               else None),
            protocol_id=";".join(p.protocol_id for p in protocols), time_step_ms=dt_ms,
            configuration_hash=self.config_sha256, start_time=started_utc, end_time=utc_now(),
            cache_key_sha256=cache_key, generation_version=GENERATION_VERSION,
            generation_code_digest=generation_code_digest(), java_version=self.sim.version_info().get("java_version", ""),
            runtime_seconds=round(result.runtime_s, 3), stdout_path=streams["stdout"][0],
            stderr_path=streams["stderr"][0], stdout_sha256=streams["stdout"][1], stderr_sha256=streams["stderr"][1],
            trace_hash=trace_sha, feature_hash=feature_sha)
        if prior_rec is None:
            write_immutable_text(run_dir / "run.json", dumps(rec))
            if result.output_tail:
                write_immutable_text(run_dir / "simulator_output_tail.txt", result.output_tail + "\n")
        self._discard(stage, run_id, failed=status is not RunStatus.OK)
        return RunOutput(status, [rec], traces, tables, False, [message] if message else [])

    # ------------------------------------------------------------ public API
    def run_battery(self, ws: Workspace, variant: VariantRecord, protocols: Sequence[ConcreteProtocol],
                    level_exec: ExecConfig, replicate: int = 0, need_traces: bool = False) -> RunOutput:
        exec_eff = apply_overrides(level_exec, variant.exec_overrides)
        outs = [self._run_probe_group(ws, variant, group, exec_eff, replicate, need_traces)
                for group in group_by_length(protocols)]
        return RunOutput(worst_status([o.status for o in outs]), [r for o in outs for r in o.records],
                         {k: v for o in outs for k, v in o.traces.items()}, {k: v for o in outs for k, v in o.tables.items()},
                         all(o.cached for o in outs), [m for o in outs for m in o.messages])

    def _run_probe_group(self, ws: Workspace, variant: VariantRecord, group: Sequence[ConcreteProtocol],
                         exec_eff: ExecConfig, replicate: int, need_traces: bool = False) -> RunOutput:
        stage = self._stage(effective_workspace(ws, variant))
        bundle = write_probe(stage, group, exec_eff, tag=f"battery_{int(group[0].total_ms)}")
        payload = {"kind": "probe", "inputs": inputs_manifest(bundle.lems_file, stage.root),
                   "protocols": [dc.asdict(p) for p in group], "exec": dc.asdict(exec_eff), "jar": self._jar_sha(),
                   "replicate": replicate, "model_hash": variant.tree_sha256, "temperature": stage.model.temperature,
                   "recording": dc.asdict(bundle.output), "cache": self.cache_context()}
        run_id = self._run_id(payload)
        with self._lock(run_id):
            cached = self._load_cached(self.raw / run_id, group, need_traces, cache_key=sha256_json(payload))
            if cached is not None:
                shutil.rmtree(stage.root, ignore_errors=True)
                return cached
            try:
                started = utc_now()
                result = self.sim.run_lems(bundle.lems_file, [bundle.output], timeout_s=self.timeout_s,
                                           sample_every_ms=exec_eff.sample_every_ms)
                return self._finish(run_id=run_id, run_kind="probe", stage=stage, variant=variant, protocols=group,
                                    dt_ms=exec_eff.dt_ms, duration_ms=bundle.length_ms, result=result, replicate=replicate, started_utc=started,
                                    cache_key=sha256_json(payload))
            except Exception:
                if stage.root.exists():
                    self._discard(stage, run_id, failed=True)
                raise

    def run_canonical(self, ws: Workspace, variant: VariantRecord, canonical_proto: ConcreteProtocol,
                      level_factor: int = 1, replicate: int = 0, need_traces: bool = False) -> RunOutput:
        from neuraxis.validation.canonical import refine_harness_step

        stage = self._stage(ws)
        if level_factor != 1:
            refine_harness_step(stage.harness_path, float(level_factor))
        step, _length = harness_step_and_length(stage.harness_path.read_text(encoding="utf-8", errors="replace"))
        dt_ms = units.parse(step).to("ms").value
        sample_every = variant.exec_overrides.get("sample_every_ms")
        payload = {"kind": "canonical", "inputs": inputs_manifest(stage.harness_path, stage.root),
                   "protocol": dc.asdict(canonical_proto), "sample_every_ms": sample_every, "jar": self._jar_sha(),
                   "replicate": replicate, "model_hash": variant.tree_sha256, "temperature": stage.model.temperature,
                   "recording": dc.asdict(canonical_output(ws.model)), "level_factor": level_factor,
                   "cache": self.cache_context()}
        run_id = self._run_id(payload)
        with self._lock(run_id):
            cached = self._load_cached(self.raw / run_id, [canonical_proto], need_traces,
                                       cache_key=sha256_json(payload))
            if cached is not None:
                shutil.rmtree(stage.root, ignore_errors=True)
                return cached
            try:
                started = utc_now()
                result = self.sim.run_lems(stage.harness_path, [canonical_output(ws.model)], timeout_s=self.timeout_s,
                                           sample_every_ms=sample_every)
                return self._finish(run_id=run_id, run_kind="canonical", stage=stage, variant=variant,
                                    protocols=[canonical_proto], dt_ms=dt_ms, duration_ms=canonical_proto.total_ms,
                                    result=result, replicate=replicate, started_utc=started,
                                    cache_key=sha256_json(payload))
            except Exception:
                if stage.root.exists():
                    self._discard(stage, run_id, failed=True)
                raise

    def run_rheobase(self, ws: Workspace, variant: VariantRecord, level_exec: ExecConfig, rcfg: dict,
                     settle_ms: float) -> RheobaseOutcome:
        """Rheobase search. Only the per-amplitude spike counts are stored (not the traces):
        each search is dozens of cells and fully re-derivable from its content-addressed inputs."""
        exec_eff = apply_overrides(level_exec, variant.exec_overrides)
        stage = self._stage(effective_workspace(ws, variant))
        payload = {"kind": "rheobase", "inputs": inputs_manifest(stage.cell_path, stage.root),
                   "cell_id": stage.model.cell_id, "temperature": stage.model.temperature, "exec": dc.asdict(exec_eff),
                   "rheobase": dict(rcfg), "settle_ms": settle_ms, "jar": self._jar_sha(),
                   "model_hash": variant.tree_sha256, "cache": self.cache_context()}
        search_id = "s-" + sha256_json(payload)[:20]
        out_path = self.raw / search_id / "rheobase.json"
        with self._lock(search_id):
            if out_path.is_file():
                shutil.rmtree(stage.root, ignore_errors=True)
                d = json.loads(out_path.read_text(encoding="utf-8"))
                res = rb.RheobaseResult(**d["result"])
                return RheobaseOutcome(res, RunStatus(d["status"]), search_id, d, True)
            cost: list[dict] = []
            counter = rb.make_step_counter(self.sim, stage, exec_eff, settle_ms=settle_ms, step_ms=rcfg["step_duration_ms"],
                                           threshold_mV=rcfg["spike_threshold_mV"], timeout_s=self.timeout_s,
                                           cost_log=cost)
            started = utc_now()
            res = rb.search(counter, hi_nA=rcfg["initial_hi_nA"], grid=rcfg["grid"], rounds=rcfg["rounds"],
                            expand=rcfg["expand"], max_hi_nA=rcfg["max_hi_nA"])
            bad = [RunStatus(c["status"]) for c in cost if c["status"] != RunStatus.OK.value]
            status = worst_status(bad) if bad else RunStatus.OK
            digest, _ = self.env()
            commit, dirty = git_state()
            if status is RunStatus.TOOL_FAILURE:          # infrastructure failure: not recorded as a result
                self._discard(stage, search_id, failed=True)
                return RheobaseOutcome(res, status, search_id, {"cost": cost}, False)
            record = {"search_id": search_id, "execution_id": uuid.uuid4().hex, "start_time": started,
                      "end_time": utc_now(), "model_hash": variant.tree_sha256, "protocol_id": "P03_rheobase",
                      "configuration_hash": self.config_sha256, "cache_key_sha256": sha256_json(payload),
                      "generation_version": GENERATION_VERSION, "generation_code_digest": generation_code_digest(), "campaign": self.campaign, "model_id": variant.model_id,
                      "variant_id": variant.variant_id, "variant_tree_sha256": variant.tree_sha256, "status": status.value,
                      "result": dc.asdict(res), "cost": cost, "cell_steps": sum(c["cell_steps"] for c in cost),
                      "runtime_s": round(sum(c["runtime_s"] for c in cost), 3), "exec": dc.asdict(exec_eff),
                      "config": dict(rcfg), "settle_ms": settle_ms, "inputs_sha256": sha256_json(payload["inputs"]),
                      "simulator_version": self.sim.version_string(), "environment_digest": digest,
                      "timestamp_utc": utc_now(), "git_commit": commit, "git_dirty": dirty,
                      "config_sha256": self.config_sha256, **self.meta}
            write_immutable_text(out_path, json.dumps(record, indent=2, sort_keys=True) + "\n")
            self._discard(stage, search_id, failed=status is not RunStatus.OK)
            return RheobaseOutcome(res, status, search_id, record, False)


@dc.dataclass
class TaskError:
    error: str
    traceback: str


def run_parallel(tasks: Sequence[Callable[[], Any]], workers: int) -> list[Any]:
    """Run callables on a thread pool (each simulation is its own JVM process).

    Exceptions are captured as :class:`TaskError` in the result list; order is preserved.
    """
    results: list[Any] = [None] * len(tasks)
    with cf.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futs = {pool.submit(t): i for i, t in enumerate(tasks)}
        for fut in cf.as_completed(futs):
            i = futs[fut]
            try:
                results[i] = fut.result()
            except Exception as exc:  # noqa: BLE001 - captured for reporting
                results[i] = TaskError(f"{type(exc).__name__}: {exc}", traceback.format_exc())
    return results
