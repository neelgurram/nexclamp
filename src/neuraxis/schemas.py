"""Typed records shared by every NeuroSem stage.

Plain dataclasses keep the records transparent and serialisable. Anything that is
written to disk goes through :func:`to_jsonable` so JSON output is stable (sorted
keys, enums as values, tuples as lists).
"""

from __future__ import annotations

import dataclasses as dc
import enum
import json
from pathlib import Path
from typing import Any

import numpy as np


class RunStatus(str, enum.Enum):
    """Outcome of one simulator invocation."""

    OK = "ok"
    INVALID = "structurally_invalid"      # schema / NeuroML validity failure
    BUILD_ERROR = "build_error"            # simulator could not build the model (bad reference, missing include)
    RUNTIME_ERROR = "runtime_error"        # simulator started but failed, or produced no output
    TIMEOUT = "timeout"
    UNSTABLE = "numerically_unstable"      # NaN/inf or voltages outside the physical bound
    TOOL_FAILURE = "tool_failure"          # Java/jar missing etc. -- never a property of the model


class MutantClass(str, enum.Enum):
    """The six-way classification required by the specification.

    Only NON_EQUIVALENT and SILENT enter the main detection-rate denominator.
    SILENT is the subset of non-equivalent mutants that pass structural validation,
    execute, and pass the canonical regression test.
    """

    STRUCTURALLY_INVALID = "1_structurally_invalid"
    NON_EXECUTABLE = "2_non_executable"
    NUMERICALLY_UNSTABLE = "3_numerically_unstable"
    EQUIVALENT = "4_equivalent_within_tested_domain"
    NON_EQUIVALENT = "5_non_equivalent"
    SILENT = "6_silent_under_canonical"

    @property
    def admissible(self) -> bool:
        return self in (MutantClass.NON_EQUIVALENT, MutantClass.SILENT)


class VariantKind(str, enum.Enum):
    REFERENCE = "reference"
    MUTANT = "mutant"
    VALID_TRANSFORM = "valid_transform"
    NO_CHANGE = "no_change_control"


class MutationFamily(str, enum.Enum):
    STIMULUS = "stimulus"
    BIOPHYSICAL = "biophysical"
    REFERENCE = "reference"
    NUMERICAL = "numerical"
    KINETICS = "kinetics"          # ion-channel kinetics (D-037); excluded from protocol selection


@dc.dataclass(frozen=True)
class ModelRecord:
    """One reference model. Loaded from ``data/model_manifest.csv``.

    Paths are relative to ``models/raw/<snapshot>``. ``harness_*`` fields describe the
    simulation shipped with the model, which is the *canonical protocol*.
    """

    model_id: str
    name: str
    snapshot: str
    cell_file: str
    cell_id: str
    harness_lems: str
    harness_output_file: str
    harness_v_column: str
    temperature: str
    source_family: str           # models sharing a family are correlated (same paper/repo)
    citation: str
    source_url: str
    commit: str
    license: str
    license_url: str
    download_date: str
    simulator: str
    expected_behavior: str
    inclusion: str               # "include" | "exclude" | "candidate"
    inclusion_reason: str


@dc.dataclass(frozen=True)
class Edit:
    """One recorded change to one file of a model snapshot."""

    file: str                     # relative to the snapshot root
    locator: str                  # human-readable XPath-like locator of the element
    attribute: str | None
    old: str | None
    new: str | None
    action: str = "set"           # set | insert | remove | text
    note: str = ""


@dc.dataclass(frozen=True)
class ExecConfig:
    """Execution configuration applied to every NeuroSem-generated run of a variant."""

    dt_ms: float
    sample_every_ms: float | None = None     # post-hoc output sampling (recording resolution)
    integrator_method: str | None = None     # LEMS <Meta method=...>; None = simulator default

    def with_dt(self, dt_ms: float) -> "ExecConfig":
        return dc.replace(self, dt_ms=dt_ms)


@dc.dataclass
class VariantRecord:
    """A reference, mutant, valid transformation or no-change control of one model."""

    variant_id: str
    model_id: str
    kind: VariantKind
    family: str = ""                          # MutationFamily value or transform category
    operator: str = ""
    params: dict[str, Any] = dc.field(default_factory=dict)
    edits: list[Edit] = dc.field(default_factory=list)
    exec_overrides: dict[str, Any] = dc.field(default_factory=dict)   # e.g. {"dt_factor": 4}
    model_overrides: dict[str, str] = dc.field(default_factory=dict)  # e.g. {"cell_id": "RS_renamed"} after a rename
    description: str = ""
    parent_tree_sha256: str = ""
    tree_sha256: str = ""
    created_utc: str = ""


@dc.dataclass(frozen=True)
class StimulusComponent:
    """A concrete current-clamp input component (maps 1:1 to a NeuroML core input)."""

    kind: str                      # "pulse" | "ramp"
    delay_ms: float
    duration_ms: float
    amplitude_nA: float = 0.0      # pulse
    start_nA: float = 0.0          # ramp
    finish_nA: float = 0.0         # ramp
    baseline_nA: float = 0.0       # ramp


@dc.dataclass(frozen=True)
class AnalysisWindow:
    """The window passed to eFEL as stim_start / stim_end."""

    start_ms: float
    end_ms: float


@dc.dataclass(frozen=True)
class ConcreteProtocol:
    """A protocol instantiated for one reference model (amplitudes in nA)."""

    protocol_id: str
    kind: str
    components: tuple[StimulusComponent, ...]
    total_ms: float
    window: AnalysisWindow
    features: tuple[str, ...]
    rheobase_nA: float | None = None
    description: str = ""


@dc.dataclass
class Trace:
    t_ms: np.ndarray
    v_mV: np.ndarray

    def __post_init__(self) -> None:
        if self.t_ms.shape != self.v_mV.shape:
            raise ValueError("t and v must have the same shape")


@dc.dataclass
class ValidationResult:
    valid: bool | None             # None = tool failure (cannot judge the model)
    returncode: int
    messages: list[str]
    raw_output: str
    validator: str


@dc.dataclass
class SimResult:
    status: RunStatus
    returncode: int
    runtime_s: float
    traces: dict[str, Trace]
    command: list[str]
    message: str = ""
    output_tail: str = ""
    stdout: str = ""
    stderr: str = ""


@dc.dataclass
class RunRecord:
    """Provenance record written for every simulation (spec: 'Data requirements')."""

    run_id: str
    campaign: str
    run_kind: str                  # probe | canonical | rheobase
    model_id: str
    variant_id: str
    variant_tree_sha256: str
    protocol_ids: list[str]
    dt_ms: float
    duration_ms: float
    seed: int | None
    simulator: str
    simulator_version: str
    environment_digest: str
    status: str
    runtime_s: float
    trace_path: str
    trace_sha256: str
    feature_path: str
    feature_sha256: str
    timestamp_utc: str
    git_commit: str
    git_dirty: bool
    replicate: int = 0
    message: str = ""
    project_name: str = ""         # study metadata from the campaign config (empty for records made before it existed)
    study_id: str = ""             # internal study identifier, independent of branding
    study_phase: str = ""          # e.g. "development_pilot"
    protocol_version: str = ""     # e.g. "PILOT_PROTOCOL_V1"
    config_sha256: str = ""        # hash of the study, feature and tolerance config files used
    # Execution-plan run-record fields ("Provenance and immutability"). ``run_id`` identifies the
    # simulation's complete inputs (content address); ``execution_id`` identifies this one execution.
    execution_id: str = ""
    model_hash: str = ""           # tree hash of the model files actually simulated
    base_model_hash: str = ""      # tree hash of the unmodified reference snapshot
    mutation_id: str | None = None
    transformation_id: str | None = None
    protocol_id: str = ""          # ";"-joined protocol ids of a batched run
    time_step_ms: float | None = None
    configuration_hash: str = ""
    start_time: str = ""
    end_time: str = ""
    runtime_seconds: float | None = None
    stdout_path: str = ""
    stderr_path: str = ""
    stdout_sha256: str = ""
    stderr_sha256: str = ""
    trace_hash: str = ""
    feature_hash: str = ""


# Fields every successful run record must carry (checked by the infrastructure smoke test).
RUN_RECORD_REQUIRED_FIELDS = (
    "run_id", "execution_id", "project_name", "study_phase", "model_id", "model_hash", "protocol_id", "simulator",
    "simulator_version", "time_step_ms", "configuration_hash", "git_commit", "environment_digest", "start_time",
    "end_time", "status", "runtime_seconds", "stdout_path", "stderr_path", "trace_path", "trace_hash",
    "feature_path", "feature_hash",
)


def to_jsonable(obj: Any) -> Any:
    if dc.is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: to_jsonable(getattr(obj, f.name)) for f in dc.fields(obj)}
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, Path):
        return obj.as_posix()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, float) and not np.isfinite(obj):
        return None if np.isnan(obj) else ("inf" if obj > 0 else "-inf")
    return obj


def dumps(obj: Any) -> str:
    return json.dumps(to_jsonable(obj), indent=2, sort_keys=True) + "\n"


def edit_from_dict(d: dict[str, Any]) -> Edit:
    return Edit(**d)


def variant_from_dict(d: dict[str, Any]) -> VariantRecord:
    d = dict(d)
    d["kind"] = VariantKind(d["kind"])
    d["edits"] = [edit_from_dict(e) for e in d.get("edits", [])]
    return VariantRecord(**d)
