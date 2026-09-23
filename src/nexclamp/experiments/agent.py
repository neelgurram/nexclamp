"""Milestone 9 agent-study harness: task specs, clean trial export, hidden scoring, trial logs.

This module prepares and scores isolated Claude Code trials. It never launches Claude Code
or any other agent; a human runs trials by following ``docs/agent_study_protocol.md``.

What it provides
  * validated task definitions (``agent_study/tasks/<task_id>/task.yaml``) for the nine task
    types of the specification, with seeded faults expressed as mutation / transform
    operators *by name* and applied through a small lazy adapter;
  * ``prepare_trial``: a clean, self-contained trial directory (model copy with the seeded
    fault, frozen prompt, public checks) plus a private record kept outside it;
  * ``score_trial``: a structured, layer-by-layer score computed from the hidden,
    deterministic evaluator spec (``agent_study/hidden/<task_id>/hidden_checks.yaml``);
  * ``TrialLog``: the record of how one trial was run.

Isolation is the scientific point. The agent must see only public checks, so the export
uses hard-coded exclusions that configuration cannot relax, copies only named task files,
and finishes with a content scan for the hidden-evaluator sentinel. Scoring never treats a
missing evaluator or a tool failure as a pass: such a layer is ``error`` and the trial is
indeterminate. Passing every layer is evidence about a finite set of tests, not proof that
the edited model is equivalent to the intended one.
"""

from __future__ import annotations

import dataclasses as dc
import datetime as dt
import difflib
import enum
import functools
import importlib
import json
import math
import os
import posixpath
import re
import shutil
import stat
import subprocess
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any
from xml.sax.saxutils import escape as _xml_escape
from xml.sax.saxutils import unescape as _xml_unescape

import yaml
from lxml import etree

from nexclamp import units
from nexclamp.models import Workspace, load_models, materialize, snapshot_dir
from nexclamp.provenance import (REPO_ROOT, git_state, sha256_bytes, sha256_file, sha256_json, tree_manifest,
                                 utc_now, write_immutable_text)
from nexclamp.schemas import ModelRecord, RunStatus, VariantKind, VariantRecord, dumps, to_jsonable

# ----------------------------------------------------------------------------- constants
AGENT_STUDY_DIR = REPO_ROOT / "agent_study"
TASKS_DIR = AGENT_STUDY_DIR / "tasks"
HIDDEN_DIR = AGENT_STUDY_DIR / "hidden"
PUBLIC_COMMON_DIR = AGENT_STUDY_DIR / "public_common"
POLICY_PATH = REPO_ROOT / "configs" / "agent_policy.yaml"
# Private trial records (baseline copy + export record = answer key for seeded tasks) live
# here by default: inside the repository, which the isolated agent environment cannot read,
# and never next to a trial directory, where `cat ../<trial>.private/...` would reach them.
PRIVATE_REL = ("results", "agent_study", "private")
PRIVATE_ROOT = REPO_ROOT.joinpath(*PRIVATE_REL)
# Every exported file and directory gets this access/modification time. Otherwise the
# seeded file would be the only one rewritten at export time, and `ls -lt` would name it.
EXPORT_MTIME_UTC = "2000-01-01T00:00:00+00:00"
EXPORT_MTIME_EPOCH = 946684800

TASK_SCHEMA = "neurosem-agent-task/1"
HIDDEN_SCHEMA = "neurosem-hidden-checks/1"
PUBLIC_SCHEMA = "neurosem-public-checks/1"
POLICY_SCHEMA = "neurosem-agent-policy/1"
FROZEN_SCHEMA = "neurosem-agent-frozen/1"
EXPORT_FORMAT = "neurosem-trial-export/1"
REFERENCE_SCHEMA = "neurosem-public-reference/1"

HIDDEN_SENTINEL = "NEUROSEM-HIDDEN-EVALUATOR"
EXPORT_MANIFEST_NAME = "EXPORT_MANIFEST.json"
EXPORT_RECORD_NAME = "export_record.json"
TASK_PROMPT_NAME = "TASK.md"
PUBLIC_RUNNER = "run_public_checks.py"
PUBLIC_CHECKS_NAME = "public_checks.json"
HIDDEN_SPEC_NAME = "hidden_checks.yaml"
RESERVED_TRIAL_NAMES = (TASK_PROMPT_NAME, EXPORT_MANIFEST_NAME, "public_tests", "model", "scratch", "framework")

# The nine task types of the specification ("Claude Code experiment", Task types).
TASK_TYPES: dict[str, str] = {
    "repair_seeded_unit_error": "Repair a seeded unit error.",
    "restore_changed_stimulus": "Restore a changed stimulus protocol.",
    "rename_channel_safely": "Rename a channel safely.",
    "refactor_included_files": "Refactor included model files.",
    "equivalent_unit_conversion": "Convert a quantity to an equivalent unit.",
    "change_one_conductance": "Change one specified conductance while preserving all other parameters.",
    "repair_channel_reference": "Repair a channel reference.",
    "improve_runtime_preserving_outputs": "Improve runtime without changing tested outputs.",
    "diagnose_behaviour_change": "Diagnose why a schema-valid model changed firing behavior.",
}
# Task types that start from a seeded fault; the others start from the reference model.
SEEDED_TASK_TYPES = frozenset({"repair_seeded_unit_error", "restore_changed_stimulus", "repair_channel_reference",
                               "diagnose_behaviour_change"})
# The permitted claim is a fraction of *transformations*. A diagnosis task asks for an answer
# and forbids model edits, so its trials cannot contribute to that fraction.
ANSWER_ONLY_TASK_TYPES = frozenset({"diagnose_behaviour_change"})
TRANSFORMATION_TASK_TYPES = frozenset(TASK_TYPES) - ANSWER_ONLY_TASK_TYPES

# Operator names are binding (ARCHITECTURE.md sections 3.4 and 3.5).
MUTATION_OPERATORS = ("stim_amplitude", "stim_onset", "stim_duration", "sim_length", "record_wrong_variable",
                      "scale_conductance", "shift_reversal", "scale_capacitance", "scale_gate_time_constant",
                      "shift_initial_voltage", "wrong_segment_group", "wrong_channel", "omit_include",
                      "duplicate_conductance", "wrong_compatible_component", "increase_dt", "solver_config",
                      "reduce_spatial_discretization", "recording_resolution")
TRANSFORM_OPERATORS = ("unit_conversion", "xml_formatting", "add_comments", "numeric_literal_format",
                       "rename_identifier", "factor_file", "reorder_independent", "explicit_default")
REGISTRY_OPERATORS: dict[str, tuple[str, ...]] = {"mutations": MUTATION_OPERATORS, "transforms": TRANSFORM_OPERATORS}
# A seeded fault must be visible in the files the agent receives.
NO_FILE_EDIT_OPERATORS = frozenset({"recording_resolution"})

# Paths that are never exported, whatever the policy says. Held-out splits, results, the
# evaluator code, the hidden specs and the pristine model snapshots (which would let an agent
# diff its way to the answer) are all here.
# The harness module, under the current package name and the names it had before the renames.
HARNESS_MODULE_PATHS: tuple[str, ...] = ("src/nexclamp/experiments/agent.py",
                                         "src/neuraxis/experiments/agent.py",
                                         "src/neurosem/experiments/agent.py")

MANDATORY_EXCLUDES: tuple[str, ...] = (
    ".git/**", "**/.git/**", "agent_study/**", "docs/m0_evidence/**", "docs/handoff/**", "docs/build_notes/**",
    "docs/agent_study_protocol.md", "results/**", "work/**", "data/splits/**", "models/**", "tests/**", ".venv/**",
    ".tools/**", "**/__pycache__/**", "**/*.pyc", "**/.pytest_cache/**", "**/*.egg-info/**",
    "configs/agent_policy.yaml", "configs/FROZEN.lock", "src/nexclamp/experiments/agent.py", "AI_USE_LOG.md",
    "**/PROVENANCE.json",
)
LEAK_MARKERS: tuple[str, ...] = (HIDDEN_SENTINEL, "agent_study/hidden", HIDDEN_SPEC_NAME)
LEAK_FILENAMES = frozenset({"task.yaml", HIDDEN_SPEC_NAME, "PROVENANCE.json", EXPORT_RECORD_NAME})

CHANGE_KINDS = ("attribute_changed", "text_changed", "element_added", "element_removed", "file_added",
                "file_removed", "file_modified")
XML_SUFFIXES = (".nml", ".xml")
# Pseudo-attributes reported by the semantic diff: an element's namespace URI (recorded where it
# differs from its parent's) and its normalised tail text.
NAMESPACE_ATTRIBUTE = "{namespace}"
TAIL_ATTRIBUTE = "{tail}"
_NS_KEY = "neurosem-diff-namespace"          # internal attribute name while diffing
TASK_ID_RE = re.compile(r"^t\d{2}_[a-z0-9_]+$")
EXPORT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
PROTOCOL_ID_RE = re.compile(r"^P\d{2}_[A-Za-z0-9_]+$")


class AgentStudyError(RuntimeError):
    pass


class TaskSpecError(AgentStudyError):
    pass


class HiddenSpecError(AgentStudyError):
    pass


class PolicyError(AgentStudyError):
    pass


class ExportLeakError(AgentStudyError):
    pass


class OperatorsUnavailable(AgentStudyError):
    """The mutation or transform registry (or one operator) cannot be imported."""


class SeedError(AgentStudyError):
    pass


class FrozenConfigError(AgentStudyError):
    pass


# ----------------------------------------------------------------------------- paths and globs
@functools.lru_cache(maxsize=None)
def _glob_regex(pattern: str) -> re.Pattern[str]:
    """``**/`` = any number of directories, ``**`` = anything, ``*`` / ``?`` stay within one segment."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def glob_match(path: str, pattern: str) -> bool:
    return _glob_regex(pattern).match(path) is not None


def matches_any(path: str, patterns: Iterable[str]) -> bool:
    return any(glob_match(path, p) for p in patterns)


def _rel_posix(path: str, what: str) -> str:
    p = str(path).replace("\\", "/")
    if not p or p.startswith("/") or re.match(r"^[A-Za-z]:", p) or any(s in ("", "..", ".") for s in p.split("/")):
        raise ValueError(f"{what} must be a relative POSIX path without '.' or '..' segments: {path!r}")
    return p


def list_files(root: Path, ignore: Sequence[str] = ()) -> list[str]:
    """Relative POSIX paths of all regular files under ``root`` not matching ``ignore``."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            rel = (Path(dirpath) / name).relative_to(root).as_posix()
            if not matches_any(rel, ignore):
                out.append(rel)
    return sorted(out)


def _rmtree(path: Path) -> None:
    def onexc(func, p, _exc):  # immutable records are read-only
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onexc=onexc)


def _require_keys(d: Mapping, required: Iterable[str], allowed: Iterable[str], where: str,
                  err: type[Exception]) -> None:
    if not isinstance(d, Mapping):
        raise err(f"{where}: expected a mapping, got {type(d).__name__}")
    missing = [k for k in required if k not in d]
    unknown = sorted(set(d) - set(allowed))
    if missing:
        raise err(f"{where}: missing keys {missing}")
    if unknown:
        raise err(f"{where}: unknown keys {unknown}")


def _check_xpath(xp: str, where: str, err: type[Exception]) -> None:
    try:
        etree.XPath(xp)
    except etree.XPathSyntaxError as exc:
        raise err(f"{where}: invalid xpath {xp!r}: {exc}") from exc


# ----------------------------------------------------------------------------- policy
@dc.dataclass(frozen=True)
class AgentPolicy:
    data: Mapping[str, Any]
    path: Path
    sha256: str

    @property
    def permissions(self) -> Mapping[str, Any]:
        return self.data["permissions"]

    @property
    def permissions_sha256(self) -> str:
        return sha256_json(to_jsonable(self.permissions))

    @property
    def default_budget(self) -> dict[str, float]:
        return dict(self.data["budget"]["default"])

    @property
    def budget_limits(self) -> dict[str, float]:
        return dict(self.data["budget"]["limits"])

    @property
    def framework_include(self) -> tuple[str, ...]:
        return tuple(self.data["export"].get("framework_include") or ())

    @property
    def extra_excludes(self) -> tuple[str, ...]:
        return tuple(self.data["export"].get("mandatory_exclude") or ())

    @property
    def scratch_dir(self) -> str:
        return str(self.data["trial"]["scratch_dir"])

    @property
    def ignore_paths(self) -> tuple[str, ...]:
        return tuple(self.data["trial"].get("ignore_paths") or ())

    @property
    def public_checks(self) -> Mapping[str, Any]:
        return self.data["public_checks"]


BUDGET_KEYS = ("max_turns", "max_wall_clock_minutes", "max_cost_usd")


def load_policy(path: Path = POLICY_PATH) -> AgentPolicy:
    raw = Path(path).read_bytes()
    d = yaml.safe_load(raw)
    where = str(path)
    _require_keys(d, ("schema", "status", "agent", "permissions", "budget", "isolation", "export", "trial",
                      "public_checks", "scoring"),
                  ("schema", "status", "agent", "permissions", "budget", "isolation", "export", "trial",
                   "public_checks", "scoring"), where, PolicyError)
    if d["schema"] != POLICY_SCHEMA:
        raise PolicyError(f"{where}: schema must be {POLICY_SCHEMA!r}")
    for key in ("default", "limits"):
        b = d["budget"].get(key)
        _require_keys(b, BUDGET_KEYS, BUDGET_KEYS, f"{where}: budget.{key}", PolicyError)
        if any(not isinstance(b[k], (int, float)) or b[k] <= 0 for k in BUDGET_KEYS):
            raise PolicyError(f"{where}: budget.{key} values must be positive numbers")
    if any(d["budget"]["default"][k] > d["budget"]["limits"][k] for k in BUDGET_KEYS):
        raise PolicyError(f"{where}: default budget exceeds limits")
    declared = tuple(d["export"].get("mandatory_exclude") or ())
    missing = [p for p in MANDATORY_EXCLUDES if p not in declared and p not in HARNESS_MODULE_PATHS]
    # The harness module itself must be excluded under whichever package name the policy was
    # written with: configs/agent_policy.yaml is frozen and still names the pre-rename path.
    if not any(p in declared for p in HARNESS_MODULE_PATHS):
        missing.append(" or ".join(HARNESS_MODULE_PATHS))
    if missing:
        raise PolicyError(f"{where}: export.mandatory_exclude must document the harness exclusions; missing {missing}")
    for pat in d["export"].get("framework_include") or ():
        _rel_posix(pat, "framework_include pattern")
    if not str(d["trial"].get("scratch_dir", "")).strip():
        raise PolicyError(f"{where}: trial.scratch_dir is required")
    return AgentPolicy(d, Path(path), sha256_bytes(raw))


# ----------------------------------------------------------------------------- task specs
@dc.dataclass(frozen=True)
class SiteSelector:
    file: str                  # relative to the model workspace root
    locator_contains: str      # substring of the operator's site locator (e.g. an element id)


@dc.dataclass(frozen=True)
class OperatorStep:
    registry: str              # "mutations" | "transforms"
    operator: str              # ARCHITECTURE operator name
    site: SiteSelector
    params: Mapping[str, Any]  # values the chosen site's parameters (or its recorded changes) must contain
    operator_args: Mapping[str, Any] = dc.field(default_factory=dict)  # constructor arguments, e.g. {"factors": [0.1]}


@dc.dataclass(frozen=True)
class Expectation:
    """A declared post-condition on one attribute (checked after applying operator steps)."""

    file: str                  # relative to the model workspace root
    xpath: str                 # on the namespace-stripped document
    attribute: str
    si_value: float | None = None
    unit: str | None = None
    value: str | None = None


@dc.dataclass(frozen=True)
class SeededFault:
    description: str
    steps: tuple[OperatorStep, ...]
    expected_after: tuple[Expectation, ...]


@dc.dataclass(frozen=True)
class TaskSpec:
    task_id: str
    type: str
    base_model: str
    title: str
    seeded_fault: SeededFault | None
    allowed_files: tuple[str, ...]      # trial-relative globs the prompt allows the agent to edit
    answer_files: tuple[str, ...]       # trial-root files the agent must write (e.g. diagnosis.yaml)
    budget: Mapping[str, float]
    task_dir: Path
    sha256: str

    @property
    def prompt_path(self) -> Path:
        return self.task_dir / "prompt.md"

    @property
    def public_tests_dir(self) -> Path:
        return self.task_dir / "public_tests"


def _parse_step(d: Any, where: str, err: type[Exception]) -> OperatorStep:
    _require_keys(d, ("registry", "operator", "site"), ("registry", "operator", "site", "params", "operator_args"),
                  where, err)
    reg, op = d["registry"], d["operator"]
    if reg not in REGISTRY_OPERATORS:
        raise err(f"{where}: registry must be one of {sorted(REGISTRY_OPERATORS)}, got {reg!r}")
    if op not in REGISTRY_OPERATORS[reg]:
        raise err(f"{where}: {op!r} is not an ARCHITECTURE {reg} operator name")
    if op in NO_FILE_EDIT_OPERATORS:
        raise err(f"{where}: {op!r} does not edit files, so the agent could not see the fault")
    site = d["site"]
    _require_keys(site, ("file", "locator_contains"), ("file", "locator_contains"), f"{where}.site", err)
    try:
        f = _rel_posix(site["file"], "site.file")
    except ValueError as exc:
        raise err(f"{where}: {exc}") from exc
    if not str(site["locator_contains"]).strip():
        raise err(f"{where}: site.locator_contains must not be empty")
    params = d.get("params") or {}
    if not isinstance(params, Mapping):
        raise err(f"{where}: params must be a mapping")
    args = d.get("operator_args") or {}
    if not isinstance(args, Mapping):
        raise err(f"{where}: operator_args must be a mapping")
    return OperatorStep(reg, op, SiteSelector(f, str(site["locator_contains"])), dict(params), dict(args))


def _parse_expectation(d: Any, where: str, err: type[Exception]) -> Expectation:
    _require_keys(d, ("file", "xpath", "attribute"), ("file", "xpath", "attribute", "si_value", "unit", "value"),
                  where, err)
    if d.get("si_value") is None and d.get("value") is None:
        raise err(f"{where}: an expectation needs si_value or value")
    _check_xpath(d["xpath"], where, err)
    try:
        f = _rel_posix(d["file"], "file")
    except ValueError as exc:
        raise err(f"{where}: {exc}") from exc
    si = d.get("si_value")
    return Expectation(f, d["xpath"], d["attribute"], float(si) if si is not None else None, d.get("unit"),
                       None if d.get("value") is None else str(d["value"]))


TASK_KEYS = ("schema", "task_id", "type", "base_model", "title", "seeded_fault", "allowed_files", "answer_files",
             "budget")


def task_from_dict(d: Any, path: Path, *, policy: AgentPolicy | None = None,
                   model_ids: Iterable[str] | None = None) -> TaskSpec:
    """Validate one task definition. ``path`` is the task.yaml location (its folder name is the id)."""
    where = str(path)
    _require_keys(d, TASK_KEYS, TASK_KEYS, where, TaskSpecError)
    if d["schema"] != TASK_SCHEMA:
        raise TaskSpecError(f"{where}: schema must be {TASK_SCHEMA!r}")
    tid = d["task_id"]
    if not isinstance(tid, str) or not TASK_ID_RE.match(tid):
        raise TaskSpecError(f"{where}: task_id {tid!r} must look like t01_short_name")
    if path.parent.name != tid:
        raise TaskSpecError(f"{where}: task_id {tid!r} does not match its folder {path.parent.name!r}")
    if d["type"] not in TASK_TYPES:
        raise TaskSpecError(f"{where}: unknown task type {d['type']!r}")
    known = set(model_ids) if model_ids is not None else set(load_models())
    if d["base_model"] not in known:
        raise TaskSpecError(f"{where}: base_model {d['base_model']!r} is not in the model manifest")
    if not str(d["title"]).strip():
        raise TaskSpecError(f"{where}: title must not be empty")

    seeded = None
    if d["seeded_fault"] is not None:
        sf = d["seeded_fault"]
        _require_keys(sf, ("description", "steps", "expected_after"), ("description", "steps", "expected_after"),
                      f"{where}: seeded_fault", TaskSpecError)
        if not sf["steps"] or not sf["expected_after"]:
            raise TaskSpecError(f"{where}: seeded_fault needs at least one step and one expected_after entry")
        seeded = SeededFault(str(sf["description"]),
                             tuple(_parse_step(s, f"{where}: seeded_fault.steps[{i}]", TaskSpecError)
                                   for i, s in enumerate(sf["steps"])),
                             tuple(_parse_expectation(e, f"{where}: seeded_fault.expected_after[{i}]", TaskSpecError)
                                   for i, e in enumerate(sf["expected_after"])))
    if (d["type"] in SEEDED_TASK_TYPES) != (seeded is not None):
        need = "requires" if d["type"] in SEEDED_TASK_TYPES else "must not have"
        raise TaskSpecError(f"{where}: task type {d['type']!r} {need} a seeded fault")

    allowed, answers = d["allowed_files"] or [], d["answer_files"] or []
    if not isinstance(allowed, list) or not isinstance(answers, list):
        raise TaskSpecError(f"{where}: allowed_files and answer_files must be lists")
    for pat in allowed:
        try:
            p = _rel_posix(pat, "allowed_files entry")
        except ValueError as exc:
            raise TaskSpecError(f"{where}: {exc}") from exc
        if not p.startswith("model/"):
            raise TaskSpecError(f"{where}: allowed_files entries must lie under model/: {pat!r}")
    for name in answers:
        if not isinstance(name, str) or "/" in name or "\\" in name or name in RESERVED_TRIAL_NAMES or not name.strip():
            raise TaskSpecError(f"{where}: answer file {name!r} must be a plain, non-reserved file name")
    if not allowed and not answers:
        raise TaskSpecError(f"{where}: a task must allow some edit or require an answer file")
    if d["type"] == "diagnose_behaviour_change" and not answers:
        raise TaskSpecError(f"{where}: diagnosis tasks need an answer file")

    budget = d["budget"]
    _require_keys(budget, BUDGET_KEYS, BUDGET_KEYS, f"{where}: budget", TaskSpecError)
    if any(not isinstance(budget[k], (int, float)) or budget[k] <= 0 for k in BUDGET_KEYS):
        raise TaskSpecError(f"{where}: budget values must be positive numbers")
    if policy is not None:
        over = [k for k in BUDGET_KEYS if budget[k] > policy.budget_limits[k]]
        if over:
            raise TaskSpecError(f"{where}: budget exceeds policy limits for {over}")

    task_dir = path.parent
    prompt = task_dir / "prompt.md"
    if not prompt.is_file() or not prompt.read_text(encoding="utf-8").strip():
        raise TaskSpecError(f"{where}: missing or empty prompt.md")
    load_public_checks(task_dir / "public_tests")
    return TaskSpec(tid, d["type"], d["base_model"], str(d["title"]), seeded, tuple(allowed), tuple(answers),
                    dict(budget), task_dir, sha256_file(path))


def load_task(task_id: str, tasks_root: Path = TASKS_DIR, *, policy: AgentPolicy | None = None,
              model_ids: Iterable[str] | None = None) -> TaskSpec:
    path = Path(tasks_root) / task_id / "task.yaml"
    if not path.is_file():
        raise TaskSpecError(f"no task definition at {path}")
    with open(path, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    return task_from_dict(d, path, policy=policy, model_ids=model_ids)


def load_all_tasks(tasks_root: Path = TASKS_DIR, **kwargs: Any) -> dict[str, TaskSpec]:
    return {p.parent.name: load_task(p.parent.name, tasks_root, **kwargs)
            for p in sorted(Path(tasks_root).glob("*/task.yaml"))}


def load_public_checks(public_dir: Path) -> dict[str, Any]:
    path = Path(public_dir) / PUBLIC_CHECKS_NAME
    if not path.is_file():
        raise TaskSpecError(f"missing public checks {path}")
    d = json.loads(path.read_text(encoding="utf-8"))
    where = str(path)
    _require_keys(d, ("schema", "validate", "simulation"), ("schema", "validate", "simulation"), where, TaskSpecError)
    if d["schema"] != PUBLIC_SCHEMA:
        raise TaskSpecError(f"{where}: schema must be {PUBLIC_SCHEMA!r}")
    sim_keys = ("lems", "output_file", "v_column", "spike_threshold_mV", "reference", "spike_time_abs_tol_ms")
    _require_keys(d["simulation"], sim_keys, sim_keys + ("timeout_s",), f"{where}: simulation", TaskSpecError)
    for f in list(d["validate"]) + [d["simulation"]["lems"]]:
        if not str(f).startswith("model/"):
            raise TaskSpecError(f"{where}: public check paths must lie under model/: {f!r}")
    return d


def check_prompt_isolation(task: TaskSpec, text: str | None = None) -> list[str]:
    """Problems that would let the frozen prompt reveal the hidden evaluation (empty = ok)."""
    text = task.prompt_path.read_text(encoding="utf-8") if text is None else text
    low = text.lower()
    problems = []
    for word in (HIDDEN_SENTINEL.lower(), "hidden", "oracle", "evaluator", "answer key", "agent_study", "neurosem",
                 "perturbation", "fingerprint"):
        if word in low:
            problems.append(f"prompt mentions {word!r}")
    for name in MUTATION_OPERATORS + TRANSFORM_OPERATORS:
        if re.search(rf"\b{re.escape(name)}\b", text):
            problems.append(f"prompt names operator {name!r}")
    if re.search(r"\bP\d{2}_[A-Za-z]", text):
        problems.append("prompt names a protocol id")
    for entry in task.allowed_files + task.answer_files:
        if entry not in text:
            problems.append(f"prompt does not state the permitted file {entry!r}")
    return problems


# ----------------------------------------------------------------------------- hidden specs
@dc.dataclass(frozen=True)
class PermittedChange:
    """One rule saying which semantic changes the hidden evaluator accepts as authorized."""

    file: str                                  # trial-relative glob
    change: tuple[str, ...]                    # CHANGE_KINDS
    locator: str | None = None                 # regex searched in the before- or after-locator
    attributes: tuple[str, ...] | None = None  # attribute names (None = any)
    require_si_equal: bool = False             # the new value must denote the same physical quantity

    def matches(self, ch: "Change") -> bool:
        if not glob_match(ch.file, self.file) or ch.kind not in self.change:
            return False
        if self.locator is not None:
            locs = [loc for loc in (ch.locator, ch.after_locator) if loc]
            if not any(re.search(self.locator, loc) for loc in locs):
                return False
        if self.attributes is not None and ch.attribute not in self.attributes:
            return False
        return not (self.require_si_equal and ch.si_equal is not True)


ASSERTION_KINDS: dict[str, tuple[str, ...]] = {
    "quantity_equals": ("file", "xpath", "attribute", "expected"),
    "unit_is": ("file", "xpath", "attribute", "unit"),
    "attribute_equals": ("file", "xpath", "attribute", "expected"),
    "xpath_count": ("files", "xpath", "count"),
    "references_resolve": ("files", "ref_xpath", "ref_attribute", "target_xpath"),
    "flattened_equivalent": ("file",),
    "harness_steps_reduced": ("file", "min_factor"),
    "answer_equals": ("file", "field", "expected"),
}
ASSERTION_OPTIONAL = ("name", "note", "rel_tol", "normalize", "rename_map", "normalize_map", "exclude_tags")


@dc.dataclass(frozen=True)
class HiddenSpec:
    task_id: str
    status: str
    oracle_base: str                            # "pristine" (reference snapshot) | "seeded" (exported state)
    oracle_steps: tuple[OperatorStep, ...]
    oracle_expected: tuple[Expectation, ...]
    validate_files: tuple[str, ...]
    execution: Mapping[str, Any]                # lems, output_file, v_column
    canonical: Mapping[str, Any]                # applicable
    battery: Mapping[str, Any]                  # applicable, model_id, frozen_selection, additional_protocols, features
    assertions: tuple[Mapping[str, Any], ...]
    permitted_changes: tuple[PermittedChange, ...]
    ignore_paths: tuple[str, ...]
    representation_only_is_unauthorized: bool
    notes: str
    path: Path
    sha256: str


HIDDEN_KEYS = ("schema", "sentinel", "task_id", "status", "oracle", "structural", "execution", "canonical",
               "battery", "assertions", "permitted_changes")
HIDDEN_OPTIONAL = ("ignore_paths", "notes", "representation_only_is_unauthorized")


def _as_tuple(v: Any) -> tuple[str, ...]:
    return (v,) if isinstance(v, str) else tuple(v)


def hidden_from_dict(d: Any, path: Path, sha256: str = "") -> HiddenSpec:
    where = str(path)
    err = HiddenSpecError
    _require_keys(d, HIDDEN_KEYS, HIDDEN_KEYS + HIDDEN_OPTIONAL, where, err)
    if d["schema"] != HIDDEN_SCHEMA or d["sentinel"] != HIDDEN_SENTINEL:
        raise err(f"{where}: wrong schema or sentinel")
    if path.parent.name != d["task_id"]:
        raise err(f"{where}: task_id does not match its folder")
    o = d["oracle"]
    _require_keys(o, ("base", "steps"), ("base", "steps", "expected_after"), f"{where}: oracle", err)
    if o["base"] not in ("pristine", "seeded"):
        raise err(f"{where}: oracle.base must be 'pristine' or 'seeded'")
    steps = tuple(_parse_step(s, f"{where}: oracle.steps[{i}]", err) for i, s in enumerate(o["steps"] or []))
    expected = tuple(_parse_expectation(e, f"{where}: oracle.expected_after[{i}]", err)
                     for i, e in enumerate(o.get("expected_after") or []))
    if steps and not expected:
        raise err(f"{where}: oracle steps need expected_after post-conditions")
    s = d["structural"]
    _require_keys(s, ("validate",), ("validate",), f"{where}: structural", err)
    ex = d["execution"]
    _require_keys(ex, ("lems", "output_file", "v_column"), ("lems", "output_file", "v_column"), f"{where}: execution", err)
    for f in list(s["validate"]) + [ex["lems"]]:
        if not str(f).startswith("model/"):
            raise err(f"{where}: structural/execution paths must lie under model/: {f!r}")
    _require_keys(d["canonical"], ("applicable",), ("applicable",), f"{where}: canonical", err)
    b = d["battery"]
    _require_keys(b, ("applicable",), ("applicable", "model_id", "frozen_selection", "additional_protocols", "features"),
                  f"{where}: battery", err)
    if b["applicable"]:
        if not b.get("model_id"):
            raise err(f"{where}: an applicable battery needs model_id")
        bad = [p for p in b.get("additional_protocols") or [] if not PROTOCOL_ID_RE.match(str(p))]
        if bad:
            raise err(f"{where}: invalid protocol ids {bad}")
        if not b.get("frozen_selection") and not b.get("additional_protocols"):
            raise err(f"{where}: an applicable battery needs frozen_selection or additional_protocols")
        feats = b.get("features", "frozen")
        if feats != "frozen" and not (isinstance(feats, list) and feats):
            raise err(f"{where}: battery.features must be 'frozen' or a non-empty list")
    assertions = []
    for i, a in enumerate(d["assertions"] or []):
        kind = a.get("kind") if isinstance(a, Mapping) else None
        if kind not in ASSERTION_KINDS:
            raise err(f"{where}: assertions[{i}] has unknown kind {kind!r}")
        _require_keys(a, ("kind",) + ASSERTION_KINDS[kind], ("kind",) + ASSERTION_KINDS[kind] + ASSERTION_OPTIONAL,
                      f"{where}: assertions[{i}]", err)
        for key in ("xpath", "ref_xpath", "target_xpath"):
            if key in a:
                _check_xpath(a[key], f"{where}: assertions[{i}]", err)
        if kind == "answer_equals" and a.get("normalize", "exact") not in ("exact", "path"):
            raise err(f"{where}: assertions[{i}].normalize must be 'exact' or 'path'")
        assertions.append(dict(a))
    rules = []
    for i, r in enumerate(d["permitted_changes"] or []):
        _require_keys(r, ("file", "change"), ("file", "change", "locator", "attribute", "require_si_equal"),
                      f"{where}: permitted_changes[{i}]", err)
        kinds = _as_tuple(r["change"])
        if any(k not in CHANGE_KINDS for k in kinds):
            raise err(f"{where}: permitted_changes[{i}] has unknown change kinds {kinds}")
        if r.get("locator") is not None:
            try:
                re.compile(r["locator"])
            except re.error as exc:
                raise err(f"{where}: permitted_changes[{i}].locator is not a regex: {exc}") from exc
        attrs = None if r.get("attribute") in (None, "*") else _as_tuple(r["attribute"])
        rules.append(PermittedChange(str(r["file"]), kinds, r.get("locator"), attrs, bool(r.get("require_si_equal"))))
    return HiddenSpec(d["task_id"], str(d["status"]), o["base"], steps, expected, tuple(s["validate"]), dict(ex),
                      dict(d["canonical"]), dict(b), tuple(assertions), tuple(rules),
                      tuple(d.get("ignore_paths") or ()), bool(d.get("representation_only_is_unauthorized", False)),
                      str(d.get("notes") or ""), path, sha256)


def load_hidden_spec(task_id: str, hidden_root: Path = HIDDEN_DIR) -> HiddenSpec:
    path = Path(hidden_root) / task_id / HIDDEN_SPEC_NAME
    if not path.is_file():
        raise HiddenSpecError(f"no hidden spec at {path}")
    raw = path.read_bytes()
    return hidden_from_dict(yaml.safe_load(raw), path, sha256_bytes(raw))


def hidden_spec_hashes(hidden_root: Path = HIDDEN_DIR) -> dict[str, str]:
    """task_id -> SHA-256 of its hidden spec, for recording in the frozen agent-evaluation config."""
    return {p.parent.name: sha256_file(p) for p in sorted(Path(hidden_root).glob(f"*/{HIDDEN_SPEC_NAME}"))}


# ----------------------------------------------------------------------------- XML helpers
def _safe_parser() -> etree.XMLParser:
    return etree.XMLParser(remove_comments=True, remove_pis=True, resolve_entities=False, no_network=True)


def _strip_namespaces(root: etree._Element) -> etree._Element:
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        el.tag = etree.QName(el).localname
        for key in [k for k in el.attrib if k.startswith("{")]:
            value = el.attrib.pop(key)
            el.attrib[etree.QName(key).localname] = value
    etree.cleanup_namespaces(root)
    return root


def parse_xml(path: Path) -> etree._Element:
    """Parse without comments, entities or network access, with namespaces stripped to local names."""
    return _strip_namespaces(etree.fromstring(Path(path).read_bytes(), _safe_parser()))


def _parse_for_diff(data: bytes) -> etree._Element:
    """Like :func:`parse_xml`, but keeps each element's namespace as a pseudo-attribute.

    The namespace is recorded only where it differs from the parent's, so swapping a
    document's default namespace is one reported change on the root element, not one per element.
    """
    root = etree.fromstring(data, _safe_parser())
    marks = []
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        parent = el.getparent()
        ns = etree.QName(el).namespace
        parent_ns = etree.QName(parent).namespace if parent is not None else None
        if ns != parent_ns:
            marks.append((el, ns or ""))
    for el, ns in marks:
        el.set(_NS_KEY, ns)
    return _strip_namespaces(root)


def _select(root: etree._Element, xpath: str) -> list[etree._Element]:
    return [e for e in root.xpath(xpath) if isinstance(e, etree._Element)]


def _norm_text(t: str | None) -> str:
    return " ".join(t.split()) if t else ""


def _si_equal(a: str | None, b: str | None) -> bool | None:
    if a is None or b is None:
        return None
    try:
        return units.same_si(a, b)
    except ValueError:
        return None


def check_expectation(root: Path, exp: Expectation) -> tuple[bool, str]:
    path = Path(root) / exp.file
    try:
        els = _select(parse_xml(path), exp.xpath)
    except (OSError, etree.XMLSyntaxError) as exc:
        return False, f"{exp.file}: {exc}"
    if len(els) != 1:
        return False, f"{exp.file}{exp.xpath} matched {len(els)} elements"
    value = els[0].get(exp.attribute)
    if value is None:
        return False, f"{exp.file}{exp.xpath}@{exp.attribute} is missing"
    if exp.value is not None and value.strip() != exp.value:
        return False, f"{exp.attribute}={value!r}, expected {exp.value!r}"
    if exp.si_value is not None or exp.unit is not None:
        try:
            q = units.parse(value)
        except ValueError as exc:
            return False, str(exc)
        if exp.si_value is not None and not math.isclose(q.si, exp.si_value, rel_tol=1e-9, abs_tol=1e-300):
            return False, f"{exp.attribute}={value!r} has SI value {q.si!r}, expected {exp.si_value!r}"
        if exp.unit is not None and q.unit != exp.unit:
            return False, f"{exp.attribute}={value!r} has unit {q.unit!r}, expected {exp.unit!r}"
    return True, value


def flatten_includes(path: Path, _seen: set[Path] | None = None) -> tuple[list[tuple[Path, etree._Element]], list[str]]:
    """Documents reachable through NeuroML ``include/@href`` and LEMS ``Include/@file``.

    A NeuroML include that does not resolve is reported as missing. LEMS includes that are
    absent from the workspace (Cells.xml, Networks.xml, ...) are provided by the simulator.
    """
    seen = set() if _seen is None else _seen
    rp = Path(path).resolve()
    if rp in seen:
        return [], []
    seen.add(rp)
    root = parse_xml(path)
    docs, missing = [(Path(path), root)], []
    for inc in root.iter("include", "Include"):
        href = inc.get("href") if inc.tag == "include" else inc.get("file")
        if not href:
            continue
        target = Path(path).parent / href
        if target.is_file():
            d2, m2 = flatten_includes(target, seen)
            docs += d2
            missing += m2
        elif inc.tag == "include":
            missing.append(href)
    return docs, missing


# ----------------------------------------------------------------------------- semantic diff
@dc.dataclass(frozen=True)
class Change:
    """One semantic difference between the exported baseline and the finished trial."""

    kind: str
    file: str
    locator: str | None = None          # element locator in the baseline document
    after_locator: str | None = None    # element locator in the trial document
    attribute: str | None = None
    old: str | None = None
    new: str | None = None
    si_equal: bool | None = None


def _locator(parent: str, el: etree._Element, siblings: list[etree._Element]) -> str:
    eid = el.get("id")
    if eid is not None and "'" not in eid and sum(1 for s in siblings if s.get("id") == eid) == 1:
        return f"{parent}/{el.tag}[@id='{eid}']"
    return f"{parent}/{el.tag}[{next(i for i, s in enumerate(siblings) if s is el) + 1}]"


def _diff_elements(b: etree._Element, a: etree._Element, bloc: str, aloc: str, rel: str, out: list[Change],
                   origins: list[int | None] | None = None) -> None:
    """Append the semantic changes between two paired elements (recursively) to ``out``.

    ``origins``, when given, receives the baseline source line of the element behind each change
    (used to re-apply seeded attribute edits textually).
    """
    def add(ch: Change, el: etree._Element | None) -> None:
        out.append(ch)
        if origins is not None:
            origins.append(el.sourceline if el is not None else None)

    for key in sorted(set(b.attrib) | set(a.attrib)):
        ov, nv = b.get(key), a.get(key)
        if (ov is None) != (nv is None) or _norm_text(ov) != _norm_text(nv):
            if key == _NS_KEY:
                add(Change("attribute_changed", rel, bloc, aloc, NAMESPACE_ATTRIBUTE, ov, nv, None), b)
            else:
                add(Change("attribute_changed", rel, bloc, aloc, key, ov, nv, _si_equal(ov, nv)), b)
    if _norm_text(b.text) != _norm_text(a.text):
        add(Change("text_changed", rel, bloc, aloc, None, _norm_text(b.text), _norm_text(a.text)), b)
    bkids = [c for c in b if isinstance(c.tag, str)]
    akids = [c for c in a if isinstance(c.tag, str)]
    tags = list(dict.fromkeys([c.tag for c in bkids] + [c.tag for c in akids]))
    for tag in tags:
        bl = [c for c in bkids if c.tag == tag]
        al = [c for c in akids if c.tag == tag]
        # Pair children by id first, then the remaining ones in document order.
        a_by_id: dict[str, etree._Element] = {}
        for c in al:
            if c.get("id") is not None:
                a_by_id.setdefault(c.get("id"), c)
        pairs, used, unmatched_b = [], set(), []
        for c in bl:
            match = a_by_id.get(c.get("id")) if c.get("id") is not None else None
            if match is not None and id(match) not in used:
                pairs.append((c, match))
                used.add(id(match))
            else:
                unmatched_b.append(c)
        unmatched_a = [c for c in al if id(c) not in used]
        pairs += list(zip(unmatched_b, unmatched_a))
        for cb, ca in pairs:
            cbloc, caloc = _locator(bloc, cb, bl), _locator(aloc, ca, al)
            if _norm_text(cb.tail) != _norm_text(ca.tail):
                add(Change("text_changed", rel, cbloc, caloc, TAIL_ATTRIBUTE, _norm_text(cb.tail), _norm_text(ca.tail)),
                    cb)
            _diff_elements(cb, ca, cbloc, caloc, rel, out, origins)
        for cb in unmatched_b[len(unmatched_a):]:
            add(Change("element_removed", rel, _locator(bloc, cb, bl), None), cb)
        for ca in unmatched_a[len(unmatched_b):]:
            add(Change("element_added", rel, None, _locator(aloc, ca, al)), b)


def xml_bytes_changes(before: bytes, after: bytes, rel: str,
                      origins: list[int | None] | None = None) -> list[Change]:
    """Semantic changes between two XML documents given as bytes (raises lxml errors on malformed input)."""
    rb, ra = _parse_for_diff(before), _parse_for_diff(after)
    if rb.tag != ra.tag:
        if origins is not None:
            origins += [rb.sourceline, None]
        return [Change("element_removed", rel, f"/{rb.tag}"), Change("element_added", rel, None, f"/{ra.tag}")]
    out: list[Change] = []
    _diff_elements(rb, ra, f"/{rb.tag}", f"/{ra.tag}", rel, out, origins)
    return out


def file_changes(before: Path, after: Path, rel: str) -> list[Change]:
    """Semantic changes of one file present in both trees.

    Comments, processing instructions, insignificant whitespace and attribute order are ignored;
    element namespaces and tail text are compared.
    """
    if Path(rel).suffix.lower() in XML_SUFFIXES:
        try:
            return xml_bytes_changes(Path(before).read_bytes(), Path(after).read_bytes(), rel)
        except (OSError, etree.XMLSyntaxError, ValueError):
            return [Change("file_modified", rel)]
    return [Change("file_modified", rel)]


# (element, attribute) pairs in LEMS files that name files the simulator writes.
LEMS_OUTPUT_ATTRIBUTES = (("OutputFile", "fileName"), ("EventOutputFile", "fileName"), ("Target", "reportFile"),
                          ("Target", "timesFile"))


def declared_output_paths(roots: Sequence[Path], ignore: Sequence[str] = ()) -> set[str]:
    """Root-relative paths of the files that the LEMS simulations under ``roots`` declare as outputs.

    Running a shipped simulation in place writes these files; they are simulator output, not
    edits. Each name is resolved against its LEMS file's folder and against the root (the
    working directory an agent is likely to use). Nothing else is treated as simulator output.
    """
    out: set[str] = set()
    for root in roots:
        root = Path(root)
        for rel in list_files(root, ignore):
            if not rel.lower().endswith(".xml"):
                continue
            path = root / rel
            try:
                if b"Lems" not in path.read_bytes():
                    continue
                doc = parse_xml(path)
            except (OSError, etree.XMLSyntaxError, ValueError):
                continue
            if doc.tag != "Lems":
                continue
            folder = PurePosixPath(rel).parent
            for tag, attr in LEMS_OUTPUT_ATTRIBUTES:
                for el in doc.iter(tag):
                    name = (el.get(attr) or "").strip().replace("\\", "/")
                    if not name or name.startswith("/") or re.match(r"^[A-Za-z]:", name):
                        continue
                    for cand in (posixpath.normpath(str(folder / name)), posixpath.normpath(name)):
                        if cand not in (".", "..") and not cand.startswith("../"):
                            out.add(cand)
    return out


def compared_files(before_root: Path, after_root: Path, ignore: Sequence[str] = (), *,
                   ignore_declared_outputs: bool = True) -> tuple[set[str], set[str]]:
    """File sets to compare. Ignore patterns (and declared simulator outputs) only hide *new* files.

    A file present in the baseline is always compared, so no ignore pattern can hide an edit to,
    or the removal of, an exported file.
    """
    before = set(list_files(before_root))
    after_all = set(list_files(after_root))
    outputs = declared_output_paths((before_root, after_root), ignore) if ignore_declared_outputs else set()
    after = {p for p in after_all if p in before or not (matches_any(p, ignore) or p in outputs)}
    return before, after


def semantic_diff(before_root: Path, after_root: Path, ignore: Sequence[str] = (), *,
                  ignore_declared_outputs: bool = True) -> list[Change]:
    before_root, after_root = Path(before_root), Path(after_root)
    before, after = compared_files(before_root, after_root, ignore, ignore_declared_outputs=ignore_declared_outputs)
    after_all = set(list_files(after_root))
    changes: list[Change] = []
    for rel in sorted(before | after):
        if rel not in after_all:
            changes.append(Change("file_removed", rel))
        elif rel not in before:
            changes.append(Change("file_added", rel))
        elif sha256_file(before_root / rel) != sha256_file(after_root / rel):
            changes.extend(file_changes(before_root / rel, after_root / rel, rel))
    return changes


@dc.dataclass
class EditScopeResult:
    permitted: list[Change]
    representation_only: list[Change]    # unlisted edits that keep every physical value (e.g. "5.0" -> "5")
    unauthorized: list[Change]


def classify_changes(changes: Sequence[Change], rules: Sequence[PermittedChange], *,
                     representation_only_is_unauthorized: bool = False) -> EditScopeResult:
    res = EditScopeResult([], [], [])
    for ch in changes:
        if any(r.matches(ch) for r in rules):
            res.permitted.append(ch)
        elif (ch.kind == "attribute_changed" and ch.si_equal is True and ch.attribute != "id"
              and not representation_only_is_unauthorized):
            res.representation_only.append(ch)
        else:
            res.unauthorized.append(ch)
    return res


# ----------------------------------------------------------------------------- assertions
@dc.dataclass(frozen=True)
class AssertionResult:
    name: str
    kind: str
    passed: bool
    detail: str


def _trial_files(root: Path, patterns: Sequence[str]) -> list[Path]:
    return [root / rel for rel in list_files(root) if matches_any(rel, patterns)]


def _single(root: Path, a: Mapping[str, Any]) -> tuple[etree._Element | None, str]:
    els = _select(parse_xml(root / a["file"]), a["xpath"])
    if len(els) != 1:
        return None, f"{a['file']}{a['xpath']} matched {len(els)} elements"
    return els[0], ""


def _canonical_element(el: etree._Element, exclude: frozenset[str], rename: Mapping[str, str]) -> tuple:
    attrs = tuple(sorted((k, rename.get(_norm_text(v), _norm_text(v))) for k, v in el.attrib.items()))
    kids = tuple(_canonical_element(c, exclude, rename) for c in el if isinstance(c.tag, str) and c.tag not in exclude)
    return el.tag, attrs, _norm_text(el.text), kids


def component_multiset(path: Path, exclude: Iterable[str] = ("include", "Include", "notes", "annotation"),
                       rename: Mapping[str, str] | None = None) -> tuple[Counter, list[str]]:
    """Top-level components of a document and everything it includes, in canonical form.

    Where a component lives (inline or in an included file) is ignored, so a correct
    refactoring leaves the multiset unchanged; any change to a component's content does not.
    """
    ex = frozenset(exclude)
    docs, missing = flatten_includes(path)
    counts: Counter = Counter()
    for _p, root in docs:
        for child in root:
            if isinstance(child.tag, str) and child.tag not in ex:
                counts[_canonical_element(child, ex, rename or {})] += 1
    return counts, missing


def _harness_steps(path: Path) -> float:
    els = _select(parse_xml(path), "//Simulation | //Component[@type='Simulation']")
    if len(els) != 1:
        raise ValueError(f"{path.name}: expected one Simulation element, found {len(els)}")
    return units.parse(els[0].get("length", "")).si / units.parse(els[0].get("step", "")).si


def evaluate_assertion(a: Mapping[str, Any], trial_root: Path, baseline_root: Path) -> AssertionResult:
    """Evaluate one hidden assertion. Unreadable or malformed trial files count as failures."""
    kind = a["kind"]
    name = a.get("name") or f"{kind}:{a.get('file') or a.get('files')}"

    def result(ok: bool, detail: str) -> AssertionResult:
        return AssertionResult(name, kind, bool(ok), detail)

    try:
        if kind in ("quantity_equals", "unit_is", "attribute_equals"):
            el, why = _single(trial_root, a)
            if el is None:
                return result(False, why)
            value = el.get(a["attribute"])
            if value is None:
                return result(False, f"attribute {a['attribute']} missing")
            if kind == "attribute_equals":
                return result(value.strip() == str(a["expected"]), f"{a['attribute']}={value!r}")
            q = units.parse(value)
            if kind == "unit_is":
                return result(q.unit == a["unit"], f"{a['attribute']}={value!r}")
            ok = units.same_si(value, str(a["expected"]), rel=float(a.get("rel_tol", 1e-9)))
            return result(ok, f"{a['attribute']}={value!r}, expected {a['expected']!r}")
        if kind == "xpath_count":
            files = _trial_files(trial_root, _as_tuple(a["files"]))
            if not files:
                return result(False, "no files matched")
            n = sum(len(_select(parse_xml(f), a["xpath"])) for f in files)
            return result(n == int(a["count"]), f"{n} matches in {len(files)} files, expected {a['count']}")
        if kind == "references_resolve":
            files = _trial_files(trial_root, _as_tuple(a["files"]))
            if not files:
                return result(False, "no files matched")
            problems, n_refs = [], 0
            for f in files:
                docs, missing = flatten_includes(f)
                ids = {e.get("id") for _p, r in docs for e in _select(r, a["target_xpath"]) if e.get("id")}
                refs = [e.get(a["ref_attribute"]) for e in _select(docs[0][1], a["ref_xpath"])]
                n_refs += len(refs)
                rel = f.relative_to(trial_root).as_posix()
                problems += [f"{rel}: unresolved include {m}" for m in missing]
                problems += [f"{rel}: {a['ref_attribute']}={r!r} does not resolve" for r in refs if r not in ids]
            if n_refs == 0:
                problems.append("no references found")
            return result(not problems, "; ".join(problems) or f"{n_refs} references resolve")
        if kind == "flattened_equivalent":
            exclude = a.get("exclude_tags") or ("include", "Include", "notes", "annotation")
            # rename_map: the requested renaming, applied to the baseline only.
            # normalize_map: equivalent spellings accepted on both sides (e.g. optional extra renames).
            normalize = {str(k): str(v) for k, v in (a.get("normalize_map") or {}).items()}
            rename = {str(k): str(v) for k, v in (a.get("rename_map") or {}).items()}
            base_map = {**normalize, **{k: normalize.get(v, v) for k, v in rename.items()}}
            trial, t_missing = component_multiset(trial_root / a["file"], exclude, normalize)
            base, _ = component_multiset(baseline_root / a["file"], exclude, base_map)
            if t_missing:
                return result(False, f"unresolved includes {t_missing}")
            if trial == base:
                return result(True, f"{sum(trial.values())} components equivalent")
            lost = sorted((k[0], dict(k[1]).get("id")) for k in (base - trial))
            extra = sorted((k[0], dict(k[1]).get("id")) for k in (trial - base))
            return result(False, f"missing or changed: {lost}; unexpected: {extra}")
        if kind == "harness_steps_reduced":
            base, trial = _harness_steps(baseline_root / a["file"]), _harness_steps(trial_root / a["file"])
            factor = base / trial if trial > 0 else math.inf
            return result(factor >= float(a["min_factor"]),
                          f"integration steps {base:.0f} -> {trial:.0f} (factor {factor:.3g}, required {a['min_factor']})")
        if kind == "answer_equals":
            path = trial_root / a["file"]
            if not path.is_file():
                return result(False, f"{a['file']} was not written")
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, Mapping) or data.get(a["field"]) is None:
                return result(False, f"field {a['field']!r} missing")

            def norm(x: Any) -> str:
                s = str(x).strip()
                if a.get("normalize", "exact") == "path":
                    s = s.replace("\\", "/")
                    while s.startswith("./"):
                        s = s[2:]
                    s = s.removeprefix("model/")
                return s

            return result(norm(data[a["field"]]) == norm(a["expected"]), f"{a['field']}={data[a['field']]!r}")
    except (OSError, ValueError, ZeroDivisionError, etree.XMLSyntaxError, yaml.YAMLError) as exc:
        return result(False, f"{type(exc).__name__}: {exc}")
    raise HiddenSpecError(f"unknown assertion kind {kind!r}")


# ----------------------------------------------------------------------------- operator adapter
@dc.dataclass
class AppliedStep:
    registry: str
    operator: str
    file: str
    locator: str
    params: dict[str, Any]
    edits: list[Any]
    model_overrides: dict[str, Any]
    operator_args: dict[str, Any] = dc.field(default_factory=dict)


def load_operator_registry(registry: str) -> Mapping[str, Any]:
    """Import ``nexclamp.mutations`` / ``nexclamp.transforms`` lazily and return its ``REGISTRY``.

    Imported on demand because the registries are optional for loading tasks or scoring
    edit scope, and so that a missing registry is reported as unavailable, never guessed.
    """
    if registry not in REGISTRY_OPERATORS:
        raise ValueError(f"unknown registry {registry!r}")
    errors = []
    for modname in (f"neurosem.{registry}", f"neurosem.{registry}.base"):
        try:
            mod = importlib.import_module(modname)
        except Exception as exc:  # a registry that fails to import for any reason is unavailable, never guessed
            errors.append(f"{modname}: {type(exc).__name__}: {exc}")
            continue
        reg = getattr(mod, "REGISTRY", None)
        if isinstance(reg, Mapping):
            return reg
        errors.append(f"{modname}: no REGISTRY mapping")
    raise OperatorsUnavailable(f"{registry} registry unavailable ({'; '.join(errors)})")


def _site_has(params: Mapping[str, Any], key: str, value: Any) -> bool:
    if params.get(key) == value:
        return True
    return any(isinstance(c, Mapping) and c.get(key) == value for c in params.get("changes") or ())


def apply_operator_step(ws: Workspace, step: OperatorStep) -> AppliedStep:
    """Apply one named operator at the site selected by file, locator substring and parameters.

    The operator comes from its registry by name; ``operator_args`` re-instantiate the same
    operator class with explicit constructor arguments (e.g. conductance factors). Among its
    sites (deterministic order) the first whose parameters, or whose recorded attribute changes,
    contain every ``step.params`` value is used. Parameters are never imposed on a different
    site, because operators precompute each site's edit.
    """
    reg = load_operator_registry(step.registry)
    if step.operator not in reg:
        raise OperatorsUnavailable(f"operator {step.operator!r} is not registered in neurosem.{step.registry}")
    op = reg[step.operator]
    if step.operator_args:
        try:
            op = type(op)(**step.operator_args)
        except TypeError as exc:
            raise SeedError(f"{step.operator}: constructor rejected operator_args {dict(step.operator_args)}: {exc}") from exc
    sites = [s for s in op.sites(ws)
             if str(s.file).replace("\\", "/") == step.site.file and step.site.locator_contains in s.locator]
    if not sites:
        raise SeedError(f"{step.operator}: no site in {step.site.file} whose locator contains "
                        f"{step.site.locator_contains!r}")
    chosen = [s for s in sites if all(_site_has(s.params, k, v) for k, v in step.params.items())]
    if not chosen:
        available = [{k: v for k, v in s.params.items() if k != "changes"} for s in sites]
        raise SeedError(f"{step.operator}: no site at {step.site.file} ({step.site.locator_contains}) has parameters "
                        f"{dict(step.params)}; available: {available}")
    site = chosen[0]
    edits, exec_overrides, model_overrides = op.apply(ws, site)
    if exec_overrides:
        raise SeedError(f"{step.operator}: produced execution overrides {exec_overrides}; agent-study faults and "
                        "oracles must be file edits, because the agent and the harness run the files as shipped")
    return AppliedStep(step.registry, step.operator, site.file, site.locator, dict(site.params), list(edits),
                       dict(model_overrides or {}), dict(step.operator_args))


def _start_tag_end(data: bytes, pos: int) -> int | None:
    """Offset just past the ``>`` closing the start tag whose name ends at ``pos`` (quotes respected)."""
    quote = None
    for i in range(pos, len(data)):
        c = data[i]
        if quote is not None:
            if c == quote:
                quote = None
        elif c in (0x22, 0x27):
            quote = c
        elif c == 0x3E:
            return i + 1
    return None


def _attribute_value_span(data: bytes, line: int | None, tag: str, attribute: str, old: str) -> tuple[int, int, int]:
    """Byte span (start, end) of ``attribute``'s value in the start tag of ``tag`` around source ``line``.

    lxml reports the line on which a start tag *ends*, so a tag qualifies if it overlaps that line.
    Returns (start, end, quote byte). Raises SeedError unless exactly one candidate matches ``old``.
    """
    if line is None:
        raise SeedError(f"no source line for <{tag}>")
    line_starts = [0] + [m.end() for m in re.finditer(rb"\n", data)]
    if line > len(line_starts):
        raise SeedError(f"source line {line} is beyond the end of the document")
    ls = line_starts[line - 1]
    le = line_starts[line] if line < len(line_starts) else len(data)
    tag_re = re.compile(rb"<(?:[A-Za-z_][\w.\-]*:)?" + re.escape(tag.encode("utf-8")) + rb"(?=[\s/>])")
    attr_re = re.compile(rb"(?<=\s)" + re.escape(attribute.encode("utf-8")) + rb"\s*=\s*([\"'])(.*?)\1", re.S)
    found = []
    for m in tag_re.finditer(data):
        if m.start() >= le:
            break
        end = _start_tag_end(data, m.end())
        if end is None or end <= ls:
            continue
        for am in attr_re.finditer(data, m.end(), end):
            value = _xml_unescape(am.group(2).decode("utf-8"), {"&quot;": '"', "&apos;": "'"})
            if _norm_text(value) == _norm_text(old):
                found.append((am.start(2), am.end(2), am.group(1)[0]))
    if len(found) != 1:
        raise SeedError(f"found {len(found)} textual occurrences of {attribute}={old!r} on <{tag}> near line {line}")
    return found[0]


def minimal_attribute_rewrite(original: bytes, operator_output: bytes, rel: str) -> bytes:
    """Re-apply an operator's attribute edits to the original bytes, leaving every other byte as it was.

    Operators re-serialise whole documents (collapsing multi-line start tags, ``<notes></notes>``
    to ``<notes/>``). In an exported trial those artefacts would point at the seeded file and
    contradict "exactly one value was edited", so seeds are written textually instead. The result
    must be semantically identical to the operator's output; only attribute-value edits qualify.
    """
    try:
        encoding = (etree.fromstring(original, _safe_parser()).getroottree().docinfo.encoding or "UTF-8").lower()
        origins: list[int | None] = []
        changes = xml_bytes_changes(original, operator_output, rel, origins)
    except (etree.XMLSyntaxError, ValueError) as exc:
        raise SeedError(f"{rel}: cannot parse seeded document: {exc}") from exc
    if encoding not in ("utf-8", "ascii", "us-ascii"):
        raise SeedError(f"{rel}: textual seeding supports UTF-8/ASCII documents only, not {encoding}")
    bad = [c for c in changes if c.kind != "attribute_changed" or c.attribute in (NAMESPACE_ATTRIBUTE, TAIL_ATTRIBUTE)
           or c.old is None or c.new is None]
    if bad or not changes:
        raise SeedError(f"{rel}: seeded faults must change existing attribute values only; operator produced {bad}")
    spans = []
    for ch, line in zip(changes, origins):
        tag = (ch.locator or "").rsplit("/", 1)[-1].split("[", 1)[0]
        start, end, quote = _attribute_value_span(original, line, tag, str(ch.attribute), str(ch.old))
        entities = {'"': "&quot;"} if quote == 0x22 else {"'": "&apos;"}
        spans.append((start, end, _xml_escape(str(ch.new), entities).encode("utf-8")))
    spans.sort(reverse=True)
    for (s1, _e1, _n1), (_s2, e2, _n2) in zip(spans, spans[1:]):
        if e2 > s1:
            raise SeedError(f"{rel}: overlapping attribute edits")
    data = original
    for start, end, new in spans:
        data = data[:start] + new + data[end:]
    if xml_bytes_changes(data, operator_output, rel):
        raise SeedError(f"{rel}: textual re-application differs semantically from the operator output")
    return data


def apply_steps(ws: Workspace, steps: Sequence[OperatorStep], expected: Sequence[Expectation], *,
                minimal: bool = False) -> list[AppliedStep]:
    """Apply operator steps by name, then check the declared post-conditions.

    With ``minimal=True`` (used for faults seeded into agent-visible exports) no file may be
    added or removed, and each modified file is rewritten so that only the edited attribute
    values differ byte-for-byte from the original.
    """
    root = Path(ws.root)
    before = {rel: (root / rel).read_bytes() for rel in list_files(root)} if minimal else {}
    applied = []
    for step in steps:
        a = apply_operator_step(ws, step)
        if a.model_overrides:
            raise SeedError(f"{step.operator}: model overrides {a.model_overrides} are not supported in the agent study")
        applied.append(a)
    if minimal:
        after = set(list_files(root))
        if after != set(before):
            raise SeedError(f"seeding added {sorted(after - set(before))} or removed {sorted(set(before) - after)} files")
        for rel, old in before.items():
            new = (root / rel).read_bytes()
            if new != old:
                (root / rel).write_bytes(minimal_attribute_rewrite(old, new, rel))
    for exp in expected:
        ok, msg = check_expectation(ws.root, exp)
        if not ok:
            raise SeedError(f"operator steps did not produce the declared state: {msg}")
    return applied


# ----------------------------------------------------------------------------- export
def is_mandatory_excluded(rel: str, extra: Sequence[str] = ()) -> bool:
    return ".git" in rel.split("/") or matches_any(rel, MANDATORY_EXCLUDES) or matches_any(rel, extra)


def export_tree(src_root: Path, dest_root: Path, include: Sequence[str], exclude: Sequence[str] = ()) -> dict[str, str]:
    """Copy files matching ``include`` (and no exclusion) from ``src_root``; returns path -> SHA-256.

    ``MANDATORY_EXCLUDES`` and any ``.git`` path segment always win over ``include``, and
    symbolic links are never followed, so no configuration can export hidden material.
    """
    src_root, dest_root = Path(src_root), Path(dest_root)
    copied: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(src_root, followlinks=False):
        rel_dir = Path(dirpath).relative_to(src_root).as_posix()
        prefix = "" if rel_dir == "." else rel_dir + "/"
        dirnames[:] = sorted(d for d in dirnames
                             if not Path(dirpath, d).is_symlink() and not is_mandatory_excluded(f"{prefix}{d}/_", exclude))
        for name in sorted(filenames):
            rel = prefix + name
            src = Path(dirpath) / name
            if src.is_symlink() or is_mandatory_excluded(rel, exclude) or not matches_any(rel, include):
                continue
            target = dest_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
            copied[rel] = sha256_file(target)
    return copied


def scan_for_leaks(root: Path) -> list[str]:
    """Anything in an exported tree that could reveal hidden checks or the unedited originals."""
    problems = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        if ".git" in dirnames:
            problems.append(f"{rel_dir}/.git: version-control metadata")
        for name in filenames:
            p = Path(dirpath) / name
            rel = p.relative_to(root).as_posix()
            if name in LEAK_FILENAMES:
                problems.append(f"{rel}: forbidden file name")
            data = p.read_bytes()
            problems += [f"{rel}: contains marker {m!r}" for m in LEAK_MARKERS if m.encode("utf-8") in data]
    return problems


@dc.dataclass(frozen=True)
class TrialExport:
    task_id: str
    trial_dir: Path
    private_dir: Path
    content_sha256: str
    files: Mapping[str, str]
    seed: list[dict[str, Any]]
    development_only: bool = False


def normalize_tree_times(root: Path, epoch: float = EXPORT_MTIME_EPOCH) -> int:
    """Set the access and modification time of ``root`` and everything below it to ``epoch``.

    Returns the number of paths touched. Creation/inode-change times cannot be set portably; they
    reflect copy order, not which file the seed edited, and a transfer re-stamps them anyway.
    """
    root = Path(root)
    n = 0
    for dirpath, _dirnames, filenames in os.walk(root, topdown=False):
        for name in filenames:
            p = Path(dirpath) / name
            if not p.is_symlink():
                os.utime(p, (epoch, epoch))
                n += 1
        os.utime(dirpath, (epoch, epoch))
        n += 1
    return n


def tree_mtimes(root: Path) -> dict[str, float]:
    """Relative POSIX path ('.' for the root) -> modification time, for files and directories."""
    root = Path(root)
    out = {".": root.stat().st_mtime}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            p = Path(dirpath) / name
            out[p.relative_to(root).as_posix()] = p.stat().st_mtime
    return out


def check_export_times(trial_dir: Path, epoch: float = EXPORT_MTIME_EPOCH) -> list[str]:
    """Paths whose modification time differs from the normalised export time (empty = uniform)."""
    return [f"mtime differs: {rel}" for rel, t in sorted(tree_mtimes(trial_dir).items()) if abs(t - epoch) > 1.0]


def default_private_dir(trial_dir: Path, private_root: Path = PRIVATE_ROOT) -> Path:
    """Private record location for a trial: ``<private_root>/<trial directory name>``."""
    name = Path(trial_dir).name
    if not EXPORT_ID_RE.match(name):
        raise AgentStudyError(f"trial directory name {name!r} must match {EXPORT_ID_RE.pattern} (it is the export id)")
    return Path(private_root) / name


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def check_trial_locations(dest: Path, private_dir: Path, repo_root: Path = REPO_ROOT) -> None:
    """Refuse trial/private locations from which the agent could reach hidden material.

    The trial directory must be outside the repository. The private record must not overlap
    the trial directory and must not be reachable through the trial's parent directory
    (no sibling ``<trial>.private``). Inside the repository only the dedicated private root
    (``results/agent_study/private``) is allowed; the isolated environment cannot read the repository.
    """
    dest, private_dir, repo = Path(dest).resolve(), Path(private_dir).resolve(), Path(repo_root).resolve()
    if _inside(dest, repo):
        raise AgentStudyError(f"the trial directory must lie outside the NeuroSem repository ({repo}), "
                              "so the agent cannot browse to hidden material")
    allowed = repo.joinpath(*PRIVATE_REL)
    if _inside(private_dir, repo) and not (allowed in private_dir.parents):
        raise AgentStudyError(f"inside the repository, private records may only live below {allowed}")
    if _inside(private_dir, dest) or _inside(dest, private_dir):
        raise AgentStudyError("the private record directory must not overlap the trial directory")
    if _inside(private_dir, dest.parent):
        raise AgentStudyError(f"the private record directory {private_dir} must not lie under the trial's parent "
                              f"directory {dest.parent}; an agent could reach it with a relative path")


def source_state(repo_root: Path, paths: Sequence[Path]) -> dict[str, Any]:
    """Git commit and cleanliness of the inputs of an export or of the evaluator.

    Clean means: the tracked tree has no modifications, and none of ``paths`` has untracked or
    modified files. Paths outside the repository are not under version control and count as
    dirty. (Only read-only Git commands are run.)
    """
    repo = Path(repo_root).resolve()
    commit, tracked_dirty = git_state(repo)
    dirty: list[str] = []
    inside = []
    for p in paths:
        rp = Path(p).resolve()
        if _inside(rp, repo):
            inside.append(rp.relative_to(repo).as_posix() or ".")
        else:
            dirty.append(f"{rp}: outside the repository (not under version control)")
    if commit == "unknown":
        dirty.append("git state unknown")
    elif inside:
        try:
            proc = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", *inside], cwd=repo,
                                  capture_output=True, text=True, check=True)
            dirty += [ln[3:] for ln in proc.stdout.splitlines() if ln.strip()]
        except (OSError, subprocess.CalledProcessError) as exc:
            dirty.append(f"git status failed: {exc}")
    return {"commit": commit, "tracked_tree_dirty": bool(tracked_dirty), "dirty_paths": sorted(dirty),
            "clean": not tracked_dirty and not dirty}


def _content_manifest(root: Path) -> dict[str, str]:
    return tree_manifest(Path(root), exclude=(EXPORT_MANIFEST_NAME,))


def public_tests_sha256(public_tests_dir: Path) -> str:
    """Hash of a task's public_tests folder (every file, byte-exact; caches ignored)."""
    root = Path(public_tests_dir)
    return sha256_json({rel: sha256_file(root / rel)
                        for rel in list_files(root, ("**/__pycache__/**", "**/*.pyc"))})


def prepare_trial(task_id: str, dest: Path, *, private_dir: Path | None = None, private_root: Path = PRIVATE_ROOT,
                  repo_root: Path = REPO_ROOT, tasks_root: Path = TASKS_DIR, public_common: Path | None = None,
                  policy: AgentPolicy | None = None, models: Mapping[str, ModelRecord] | None = None,
                  overwrite: bool = False, allow_dirty: bool = False) -> TrialExport:
    """Export a clean trial directory for one task, and a private record kept away from it.

    Trial directory (what the agent sees)::

        TASK.md                 frozen prompt (byte copy of prompt.md)
        model/                  model snapshot with the seeded fault applied (no PROVENANCE.json)
        public_tests/           public checks + run_public_checks.py
        scratch/                agent scratch space (ignored by scoring)
        EXPORT_MANIFEST.json    content hashes of everything above

    Every file and directory in it has the same timestamp (``EXPORT_MTIME_UTC``). The private
    directory (default ``<private_root>/<trial directory name>``; never shown to the agent) holds
    ``baseline/`` (identical, identically timestamped copy of the export, used for the semantic
    diff and the patch) and ``export_record.json`` (seed edits = answer key, task, prompt,
    public-test and policy hashes, source Git state). The hidden spec is not read here.

    The export is refused when the repository inputs are not committed ("start every trial from
    the same clean commit"). ``allow_dirty=True`` exports anyway for harness development; such an
    export is marked ``development_only`` and a frozen evaluation config refuses to score it.
    """
    policy = policy or load_policy()
    models = dict(models) if models is not None else load_models()
    task = load_task(task_id, tasks_root, policy=policy, model_ids=models)
    problems = check_prompt_isolation(task)
    if problems:
        raise TaskSpecError(f"{task_id}: prompt fails isolation checks: {problems}")
    dest = Path(dest).resolve()
    private_dir = Path(private_dir).resolve() if private_dir is not None else default_private_dir(dest, private_root)
    repo = Path(repo_root).resolve()
    check_trial_locations(dest, private_dir, repo)
    common = Path(public_common) if public_common is not None else Path(tasks_root).parent / "public_common"
    model = models[task.base_model]
    state = source_state(repo, [task.task_dir, common, policy.path, repo / "src" / "nexclamp", snapshot_dir(model)])
    if not state["clean"] and not allow_dirty:
        raise AgentStudyError(f"{task_id}: refusing to export from uncommitted inputs {state['dirty_paths'][:20]} "
                              f"(tracked tree dirty: {state['tracked_tree_dirty']}); commit first, or pass "
                              "allow_dirty=True for a development-only export")
    development_only = not state["clean"]
    for p in (dest, private_dir):
        if p.exists():
            if not overwrite:
                raise FileExistsError(p)
            _rmtree(p)
    try:
        ws = materialize(model, dest / "model")
        applied = (apply_steps(ws, task.seeded_fault.steps, task.seeded_fault.expected_after, minimal=True)
                   if task.seeded_fault else [])
        shutil.copyfile(task.prompt_path, dest / TASK_PROMPT_NAME)
        export_tree(task.public_tests_dir, dest / "public_tests", include=("**",))
        shutil.copyfile(common / PUBLIC_RUNNER, dest / "public_tests" / PUBLIC_RUNNER)
        (dest / policy.scratch_dir).mkdir(parents=True, exist_ok=True)
        if policy.framework_include:
            export_tree(repo, dest / "framework", policy.framework_include, policy.extra_excludes)
        leaks = scan_for_leaks(dest)
        if leaks:
            raise ExportLeakError(f"{task_id}: export would leak: {leaks}")
        files = _content_manifest(dest)
        content = sha256_json(files)
        created = utc_now()
        manifest = {"format": EXPORT_FORMAT, "task_id": task.task_id, "export_id": dest.name, "created_utc": created,
                    "content_sha256": content, "files": files, "timestamps_normalized_to_utc": EXPORT_MTIME_UTC}
        (dest / EXPORT_MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        normalize_tree_times(dest)
        shutil.copytree(dest, private_dir / "baseline")
        normalize_tree_times(private_dir / "baseline")
        seed = [to_jsonable(dc.asdict(a)) for a in applied]
        record = {
            "format": EXPORT_FORMAT, "task_id": task.task_id, "task_type": task.type, "export_id": dest.name,
            "base_model": task.base_model, "snapshot": model.snapshot, "task_sha256": task.sha256,
            "prompt_sha256": sha256_file(task.prompt_path), "public_tests_sha256": public_tests_sha256(task.public_tests_dir),
            "public_runner_sha256": sha256_file(common / PUBLIC_RUNNER), "policy_sha256": policy.sha256,
            "content_sha256": content, "files": files, "seed": seed,
            "seeded_fault": task.seeded_fault.description if task.seeded_fault else None,
            "mandatory_exclude": list(MANDATORY_EXCLUDES), "policy_exclude": list(policy.extra_excludes),
            "framework_include": list(policy.framework_include), "source_git_commit": state["commit"],
            "source_git_dirty": development_only, "source_dirty_paths": state["dirty_paths"],
            "development_only": development_only, "timestamps_normalized_to_utc": EXPORT_MTIME_UTC,
            "created_utc": created,
        }
        write_immutable_text(private_dir / EXPORT_RECORD_NAME, json.dumps(to_jsonable(record), indent=2, sort_keys=True) + "\n")
    except BaseException:
        for p in (dest, private_dir):
            if p.exists():
                _rmtree(p)
        raise
    return TrialExport(task.task_id, dest, private_dir, content, files, seed, development_only)


def verify_export(trial_dir: Path) -> list[str]:
    """Content differences between a trial directory and its own export manifest (empty = untouched).

    Timestamps are checked separately by :func:`check_export_times`.
    """
    trial_dir = Path(trial_dir)
    manifest = json.loads((trial_dir / EXPORT_MANIFEST_NAME).read_text(encoding="utf-8"))
    now = _content_manifest(trial_dir)
    before = manifest["files"]
    problems = [f"missing: {p}" for p in sorted(set(before) - set(now))]
    problems += [f"added: {p}" for p in sorted(set(now) - set(before))]
    problems += [f"modified: {p}" for p in sorted(set(now) & set(before)) if now[p] != before[p]]
    if sha256_json(before) != manifest["content_sha256"]:
        problems.append("manifest content hash does not match its file list")
    return problems


def load_export_record(private_dir: Path) -> dict[str, Any]:
    """Read the private export record and check that the baseline copy is untouched."""
    private_dir = Path(private_dir)
    path = private_dir / EXPORT_RECORD_NAME
    if not path.is_file():
        raise AgentStudyError(f"no private export record at {path}; pass the trial's private_dir explicitly")
    record = json.loads(path.read_text(encoding="utf-8"))
    if _content_manifest(private_dir / "baseline") != record["files"]:
        raise AgentStudyError(f"{private_dir}/baseline no longer matches the export record")
    return record


def _text_lines(path: Path) -> list[str] | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
    return [ln if ln.endswith("\n") else ln + "\n" for ln in text.splitlines(keepends=True)]


def make_patch(baseline: Path, trial: Path, ignore: Sequence[str] = (), *, ignore_declared_outputs: bool = True) -> str:
    """Unified diff from the exported baseline to the finished trial (the agent's patch).

    Uses the same file selection as :func:`semantic_diff`: ignore patterns and declared simulator
    outputs hide only new files, never changes to exported ones.
    """
    baseline, trial = Path(baseline), Path(trial)
    before, after = compared_files(baseline, trial, ignore, ignore_declared_outputs=ignore_declared_outputs)
    after = after & set(list_files(trial))
    chunks: list[str] = []
    for rel in sorted(before | after):
        if rel in before and rel in after and sha256_file(baseline / rel) == sha256_file(trial / rel):
            continue
        old = _text_lines(baseline / rel) if rel in before else []
        new = _text_lines(trial / rel) if rel in after else []
        if old is None or new is None:
            chunks.append(f"Binary files a/{rel} and b/{rel} differ\n")
            continue
        chunks.extend(difflib.unified_diff(old, new, fromfile=f"a/{rel}" if rel in before else "/dev/null",
                                           tofile=f"b/{rel}" if rel in after else "/dev/null"))
    return "".join(chunks)


# ----------------------------------------------------------------------------- public references
def spike_times(t_ms: Sequence[float], v_mV: Sequence[float], threshold_mV: float) -> list[float]:
    """Upward threshold crossings, linearly interpolated (identical to the public runner)."""
    out = []
    for i in range(len(v_mV) - 1):
        if v_mV[i] < threshold_mV <= v_mV[i + 1]:
            out.append(float(t_ms[i] + (threshold_mV - v_mV[i]) * (t_ms[i + 1] - t_ms[i]) / (v_mV[i + 1] - v_mV[i])))
    return out


def build_public_reference(task_id: str, sim: Any, work_dir: Path, *, tasks_root: Path = TASKS_DIR,
                           models: Mapping[str, ModelRecord] | None = None,
                           cache: dict[tuple, dict] | None = None) -> Path | None:
    """Record the canonical spike times of the unedited model for a task's public check.

    This is the conventional regression reference the agent may use: the shipped simulation
    of the reference snapshot, run with the frozen jNeuroML. Returns the written path, or None
    when the task's public check has no reference (the requested change is meant to alter it).
    """
    from nexclamp.simulators.base import OutputSpec

    models = dict(models) if models is not None else load_models()
    task = load_task(task_id, tasks_root, model_ids=models)
    spec = load_public_checks(task.public_tests_dir)["simulation"]
    if not spec.get("reference"):
        return None
    key = (task.base_model, spec["lems"], spec["output_file"], int(spec["v_column"]), float(spec["spike_threshold_mV"]))
    if cache is not None and key in cache:
        ref = cache[key]
    else:
        ws = materialize(models[task.base_model], Path(work_dir) / task.base_model / "model", overwrite=True)
        lems = ws.root.parent / spec["lems"]
        res = sim.run_lems(lems, [OutputSpec(spec["output_file"], {"v": int(spec["v_column"])})])
        if res.status is not RunStatus.OK:
            raise AgentStudyError(f"{task_id}: reference simulation failed: {res.status.value} {res.message}")
        tr = res.traces["v"]
        ref = {
            "schema": REFERENCE_SCHEMA, "model_id": task.base_model, "snapshot": models[task.base_model].snapshot,
            "lems": spec["lems"], "output_file": spec["output_file"], "v_column": int(spec["v_column"]),
            "spike_threshold_mV": float(spec["spike_threshold_mV"]),
            "spike_times_ms": spike_times(tr.t_ms.tolist(), tr.v_mV.tolist(), float(spec["spike_threshold_mV"])),
            "n_samples": int(tr.t_ms.size), "t_end_ms": float(tr.t_ms[-1]),
            "simulator": sim.version_string() if hasattr(sim, "version_string") else getattr(sim, "name", ""),
            "generated_utc": utc_now(), "generated_from": "unedited reference snapshot",
        }
        if cache is not None:
            cache[key] = ref
    out = task.public_tests_dir / spec["reference"]
    out.write_text(json.dumps(ref, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


# ----------------------------------------------------------------------------- frozen evaluation config
FROZEN_KEYS = ("schema", "campaign", "results_root", "dt_ms", "timeout_s", "tolerance_table", "tolerance_table_sha256",
               "tolerance_multiplier", "selected_protocols", "reference_rheobase_nA", "hidden_spec_sha256", "configs",
               "policy_sha256", "evaluator_git_commit", "public_runner_sha256", "task_sha256", "prompt_sha256",
               "public_tests_sha256")
GIT_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def freeze_hashes(tasks_root: Path = TASKS_DIR, hidden_root: Path = HIDDEN_DIR, public_common: Path = PUBLIC_COMMON_DIR,
                  policy_path: Path = POLICY_PATH) -> dict[str, Any]:
    """Hashes of every agent-study input, for the frozen agent-evaluation config (protocol step 1).

    Covers the policy, the shared public runner, and per task its definition (seed), frozen
    prompt, public tests (including the canonical reference) and hidden evaluator spec.
    """
    tasks = sorted(p.parent.name for p in Path(tasks_root).glob("*/task.yaml"))
    return {
        "policy_sha256": sha256_file(policy_path),
        "public_runner_sha256": sha256_file(Path(public_common) / PUBLIC_RUNNER),
        "task_sha256": {t: sha256_file(Path(tasks_root) / t / "task.yaml") for t in tasks},
        "prompt_sha256": {t: sha256_file(Path(tasks_root) / t / "prompt.md") for t in tasks},
        "public_tests_sha256": {t: public_tests_sha256(Path(tasks_root) / t / "public_tests") for t in tasks},
        "hidden_spec_sha256": hidden_spec_hashes(hidden_root),
    }


@dc.dataclass(frozen=True)
class FrozenConfig:
    """Everything the hidden evaluator and the trial exports depend on, fixed (and hashed) before the first trial."""

    campaign: str
    results_root: Path
    dt_ms: float
    timeout_s: float
    tolerance_table: Path | None
    tolerance_table_sha256: str | None
    tolerance_multiplier: float
    selected_protocols: tuple[str, ...]
    reference_rheobase_nA: Mapping[str, float]
    hidden_spec_sha256: Mapping[str, str]
    cfgs: Mapping[str, Mapping[str, Any]]      # "study", "features", "tolerances" -> loaded YAML
    policy_sha256: str | None = None
    evaluator_git_commit: str | None = None
    public_runner_sha256: str | None = None
    task_sha256: Mapping[str, str] = dc.field(default_factory=dict)
    prompt_sha256: Mapping[str, str] = dc.field(default_factory=dict)
    public_tests_sha256: Mapping[str, str] = dc.field(default_factory=dict)
    provisional: bool = False
    source_path: Path | None = None
    sha256: str = ""

    @classmethod
    def development(cls, results_root: Path, campaign: str = "agent_dev", dt_ms: float = 0.005,
                    timeout_s: float = 3600.0) -> "FrozenConfig":
        """An unfrozen config for developing the harness. It skips every freeze check, behavioural
        layers cannot pass without a tolerance table and protocol selection, and every score is
        marked provisional (and excluded from the claim fraction). ``load_frozen_config`` never
        returns a provisional config."""
        return cls(campaign, Path(results_root), dt_ms, timeout_s, None, None, 1.0, (), {}, {}, {}, provisional=True)

    def check_hidden_spec(self, hidden: HiddenSpec) -> None:
        if self.provisional or self.hidden_spec_sha256.get(hidden.task_id) == hidden.sha256:
            return
        raise FrozenConfigError(f"hidden spec for {hidden.task_id} does not match the frozen hash; the evaluator "
                                "changed after freezing, so this trial cannot be scored under this config")

    def check_trial_inputs(self, task: TaskSpec, policy: AgentPolicy, record: Mapping[str, Any],
                           public_common: Path) -> None:
        """The export and the current task files must both match the frozen hashes.

        A prompt, seed, public reference or policy edited after freezing (or an export made from a
        different or uncommitted source) would otherwise be scored silently as if it were frozen.
        """
        if self.provisional:
            return
        tid = task.task_id
        checks = [
            ("task definition", self.task_sha256.get(tid), task.sha256, record.get("task_sha256")),
            ("prompt", self.prompt_sha256.get(tid), sha256_file(task.prompt_path), record.get("prompt_sha256")),
            ("public tests", self.public_tests_sha256.get(tid), public_tests_sha256(task.public_tests_dir),
             record.get("public_tests_sha256")),
            ("public runner", self.public_runner_sha256, sha256_file(Path(public_common) / PUBLIC_RUNNER),
             record.get("public_runner_sha256")),
            ("agent policy", self.policy_sha256, policy.sha256, record.get("policy_sha256")),
        ]
        problems = []
        for label, frozen, current, exported in checks:
            if not frozen:
                problems.append(f"{label}: no frozen hash for {tid}")
            elif current != frozen:
                problems.append(f"{label}: current file differs from the frozen hash")
            elif exported != frozen:
                problems.append(f"{label}: the trial was exported from a different version")
        if record.get("development_only") or record.get("source_git_dirty"):
            problems.append("the trial was exported from uncommitted inputs (development-only export)")
        if record.get("source_git_commit") != self.evaluator_git_commit:
            problems.append(f"the trial was exported from commit {record.get('source_git_commit')}, "
                            f"not the frozen commit {self.evaluator_git_commit}")
        if problems:
            raise FrozenConfigError(f"{tid}: trial cannot be scored under the frozen config: {'; '.join(problems)}")

    def check_evaluator_state(self, state: Mapping[str, Any]) -> None:
        """The evaluator code and agent-study files in use must be the frozen, committed ones."""
        if self.provisional:
            return
        if state.get("commit") != self.evaluator_git_commit or not state.get("clean"):
            raise FrozenConfigError(f"evaluator is at commit {state.get('commit')} (clean: {state.get('clean')}, "
                                    f"dirty: {list(state.get('dirty_paths') or [])[:10]}); frozen commit is "
                                    f"{self.evaluator_git_commit}")

    def tolerance_table_obj(self) -> Any:
        if self.tolerance_table is None:
            raise FrozenConfigError("no frozen tolerance table: behavioural layers cannot be scored")
        if self.tolerance_table_sha256 and sha256_file(self.tolerance_table) != self.tolerance_table_sha256:
            raise FrozenConfigError(f"{self.tolerance_table} does not match its frozen hash")
        from nexclamp.validation.convergence import ToleranceTable

        return ToleranceTable.from_csv(self.tolerance_table)


def load_frozen_config(path: Path, repo_root: Path = REPO_ROOT, *, tasks_root: Path | None = None,
                       hidden_root: Path | None = None, public_common: Path | None = None,
                       policy_path: Path | None = None) -> FrozenConfig:
    """Load and verify the frozen agent-evaluation config.

    Every hash is required and checked against the current files: tolerance table, configs,
    agent policy, public runner, and per task the definition, prompt, public tests and hidden
    spec. A ``provisional`` config is refused; only :meth:`FrozenConfig.development` bypasses freezing.
    """
    raw = Path(path).read_bytes()
    d = yaml.safe_load(raw)
    where = str(path)
    _require_keys(d, FROZEN_KEYS, FROZEN_KEYS + ("provisional", "notes"), where, FrozenConfigError)
    if d["schema"] != FROZEN_SCHEMA:
        raise FrozenConfigError(f"{where}: schema must be {FROZEN_SCHEMA!r}")
    if d.get("provisional"):
        raise FrozenConfigError(f"{where}: a frozen config cannot be provisional; use FrozenConfig.development() "
                                "for harness development")
    repo = Path(repo_root)
    tasks_root = Path(tasks_root) if tasks_root is not None else repo / "agent_study" / "tasks"
    hidden_root = Path(hidden_root) if hidden_root is not None else repo / "agent_study" / "hidden"
    public_common = Path(public_common) if public_common is not None else repo / "agent_study" / "public_common"
    policy_path = Path(policy_path) if policy_path is not None else repo / "configs" / "agent_policy.yaml"
    if not GIT_COMMIT_RE.match(str(d["evaluator_git_commit"])):
        raise FrozenConfigError(f"{where}: evaluator_git_commit must be a full 40-character commit hash")
    current = freeze_hashes(tasks_root, hidden_root, public_common, policy_path)
    load_policy(policy_path)
    mismatched = [k for k in ("policy_sha256", "public_runner_sha256") if d[k] != current[k]]
    for key in ("task_sha256", "prompt_sha256", "public_tests_sha256", "hidden_spec_sha256"):
        frozen_map = d[key]
        if not isinstance(frozen_map, Mapping) or not frozen_map:
            raise FrozenConfigError(f"{where}: {key} must be a non-empty task_id -> sha256 mapping")
        mismatched += [f"{key}[{t}]" for t, h in frozen_map.items() if current[key].get(t) != h]
    if set(d["task_sha256"]) != set(d["prompt_sha256"]) or set(d["task_sha256"]) != set(d["public_tests_sha256"]) \
            or set(d["task_sha256"]) != set(d["hidden_spec_sha256"]):
        raise FrozenConfigError(f"{where}: task_sha256, prompt_sha256, public_tests_sha256 and hidden_spec_sha256 "
                                "must cover the same tasks")
    if mismatched:
        raise FrozenConfigError(f"{where}: files changed after freezing: {mismatched}")

    def resolve(p: str) -> Path:
        q = Path(p)
        return q if q.is_absolute() else Path(repo_root) / q

    tol = resolve(d["tolerance_table"])
    if not tol.is_file() or sha256_file(tol) != d["tolerance_table_sha256"]:
        raise FrozenConfigError(f"{where}: tolerance table missing or hash mismatch")
    cfgs = {}
    for name in ("study", "features", "tolerances"):
        entry = d["configs"].get(name)
        _require_keys(entry, ("path", "sha256"), ("path", "sha256"), f"{where}: configs.{name}", FrozenConfigError)
        p = resolve(entry["path"])
        if not p.is_file() or sha256_file(p) != entry["sha256"]:
            raise FrozenConfigError(f"{where}: config {name} missing or hash mismatch")
        cfgs[name] = yaml.safe_load(p.read_text(encoding="utf-8"))
    bad = [p for p in d["selected_protocols"] if not PROTOCOL_ID_RE.match(str(p))]
    if bad:
        raise FrozenConfigError(f"{where}: invalid protocol ids {bad}")
    return FrozenConfig(
        campaign=str(d["campaign"]), results_root=resolve(d["results_root"]), dt_ms=float(d["dt_ms"]),
        timeout_s=float(d["timeout_s"]), tolerance_table=tol, tolerance_table_sha256=d["tolerance_table_sha256"],
        tolerance_multiplier=float(d["tolerance_multiplier"]), selected_protocols=tuple(d["selected_protocols"]),
        reference_rheobase_nA={k: float(v) for k, v in d["reference_rheobase_nA"].items()},
        hidden_spec_sha256=dict(d["hidden_spec_sha256"]), cfgs=cfgs, policy_sha256=str(d["policy_sha256"]),
        evaluator_git_commit=str(d["evaluator_git_commit"]), public_runner_sha256=str(d["public_runner_sha256"]),
        task_sha256=dict(d["task_sha256"]), prompt_sha256=dict(d["prompt_sha256"]),
        public_tests_sha256=dict(d["public_tests_sha256"]), provisional=False, source_path=Path(path),
        sha256=sha256_bytes(raw))


# ----------------------------------------------------------------------------- scores
class LayerStatus(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"                    # tool failure or unavailable evaluator: says nothing about the trial
    NOT_EVALUATED = "not_evaluated"    # an earlier cascade layer did not pass
    NOT_APPLICABLE = "not_applicable"


LAYERS = ("schema_valid", "executes", "canonical_passes", "hidden_battery_passes", "hidden_assertions_pass", "edit_scope")
CASCADE_LAYERS = LAYERS[:4]
BASIC_LAYERS = LAYERS[:3]
PASSING = (LayerStatus.PASS, LayerStatus.NOT_APPLICABLE)
CATEGORY_BY_LAYER = {
    "schema_valid": "structurally_invalid", "executes": "non_executable", "canonical_passes": "canonical_failure",
    "hidden_battery_passes": "hidden_battery_failure", "hidden_assertions_pass": "hidden_assertion_failure",
    "edit_scope": "unauthorized_edit",
}


@dc.dataclass
class LayerOutcome:
    layer: str
    status: LayerStatus
    details: dict[str, Any] = dc.field(default_factory=dict)


@dc.dataclass
class TrialScore:
    task_id: str
    trial_id: str
    layers: dict[str, LayerOutcome]
    basic_pass: bool | None                  # schema + execution + canonical ("basic validation")
    neurosem_pass: bool | None               # all layers, including hidden battery and edit scope
    basic_pass_battery_fail: bool | None     # the quantity of the permitted claim
    first_failed_layer: str | None
    category: str
    unauthorized_edits_detected: bool | None
    provisional: bool
    frozen_config_sha256: str
    hidden_spec_sha256: str
    export_content_sha256: str
    scored_utc: str
    task_type: str = ""
    model_changed: bool | None = None        # did the trial change anything under model/ (None = unknown)


def _tri(statuses: Sequence[LayerStatus]) -> bool | None:
    if any(s is LayerStatus.FAIL for s in statuses):
        return False
    if all(s in PASSING for s in statuses):
        return True
    return None


def aggregate(task_id: str, outcomes: Mapping[str, LayerOutcome], *, trial_id: str = "", provisional: bool = True,
              frozen_config_sha256: str = "", hidden_spec_sha256: str = "", export_content_sha256: str = "",
              task_type: str = "", model_changed: bool | None = None) -> TrialScore:
    """Combine layer outcomes into a trial score.

    Three-valued logic: any failing layer makes a result False; a result is True only if every
    layer passed or was not applicable; otherwise (errors, unevaluated layers) it is None and the
    trial is indeterminate rather than silently counted either way. The claim quantity
    ``basic_pass_battery_fail`` is determinate only when the battery actually ran (pass or fail)
    after a basic pass, or when basic validation failed; a battery that is not applicable says
    nothing about silent failures.
    """
    if set(outcomes) != set(LAYERS):
        raise ValueError(f"outcomes must cover exactly {LAYERS}; got {sorted(outcomes)}")
    for name, o in outcomes.items():
        if o.layer != name or not isinstance(o.status, LayerStatus):
            raise ValueError(f"malformed outcome for layer {name}")
    blocked = None
    for name in CASCADE_LAYERS:
        st = outcomes[name].status
        if blocked is not None and st not in (LayerStatus.NOT_EVALUATED, LayerStatus.NOT_APPLICABLE):
            raise ValueError(f"cascade violation: {name} is {st.value} although {blocked} did not pass")
        if blocked is None and st not in PASSING:
            blocked = name
    basic = _tri([outcomes[n].status for n in BASIC_LAYERS])
    neuro = _tri([outcomes[n].status for n in LAYERS])
    battery = outcomes["hidden_battery_passes"].status
    if basic is True:
        bpbf = (True if battery is LayerStatus.FAIL else False if battery is LayerStatus.PASS else None)
    else:
        bpbf = False if basic is False else None
    first_failed = next((n for n in LAYERS if outcomes[n].status is LayerStatus.FAIL), None)
    category = "success" if neuro is True else (CATEGORY_BY_LAYER[first_failed] if first_failed else "indeterminate")
    edit = outcomes["edit_scope"].status
    unauthorized = True if edit is LayerStatus.FAIL else (False if edit is LayerStatus.PASS else None)
    return TrialScore(task_id=task_id, trial_id=trial_id, layers=dict(outcomes), basic_pass=basic, neurosem_pass=neuro,
                      basic_pass_battery_fail=bpbf, first_failed_layer=first_failed, category=category,
                      unauthorized_edits_detected=unauthorized, provisional=provisional,
                      frozen_config_sha256=frozen_config_sha256, hidden_spec_sha256=hidden_spec_sha256,
                      export_content_sha256=export_content_sha256, scored_utc=utc_now(), task_type=task_type,
                      model_changed=model_changed)


def summarize_scores(scores: Sequence[TrialScore], invalid_trials: Iterable[str] = ()) -> dict[str, Any]:
    """Counts by category, layer and task type, and the fraction behind the permitted claim.

    The claim is about *transformations*, so its denominator contains only trials that are
    valid (no invalid log, e.g. a manual intervention), scored under a frozen config (not
    provisional), of a transformation task type (not answer-only diagnosis), that changed the
    model, and whose basic and battery outcomes are determinate. Every exclusion is counted, so
    the excluded groups plus the denominator add up to the number of valid trials.
    """
    invalid = set(invalid_trials)
    valid = [s for s in scores if s.trial_id not in invalid]
    frozen = [s for s in valid if not s.provisional]
    transform = [s for s in frozen if s.task_type in TRANSFORMATION_TASK_TYPES]
    changed = [s for s in transform if s.model_changed is True]
    determinate = [s for s in changed if s.basic_pass_battery_fail is not None]
    k = sum(1 for s in determinate if s.basic_pass_battery_fail)

    def eligible(s: TrialScore) -> bool:
        return (not s.provisional and s.task_type in TRANSFORMATION_TASK_TYPES and s.model_changed is True
                and s.basic_pass_battery_fail is not None)

    by_type: dict[str, dict[str, Any]] = {}
    for s in valid:
        row = by_type.setdefault(s.task_type or "unknown", {"n_trials": 0, "provisional": 0, "basic_pass": 0,
                                                            "neurosem_pass": 0, "claim_count": 0,
                                                            "claim_denominator": 0})
        row["n_trials"] += 1
        row["provisional"] += int(s.provisional)
        row["basic_pass"] += int(s.basic_pass is True)
        row["neurosem_pass"] += int(s.neurosem_pass is True)
        if eligible(s):
            row["claim_denominator"] += 1
            row["claim_count"] += int(bool(s.basic_pass_battery_fail))
    return {
        "n_trials_scored": len(scores),
        "n_trials_excluded_invalid": len(scores) - len(valid),
        "n_trials": len(valid),
        "provisional_scores": len(valid) - len(frozen),
        "by_category": dict(sorted(Counter(s.category for s in valid).items())),
        "by_task_type": dict(sorted(by_type.items())),
        "layer_status_counts": {n: dict(sorted(Counter(s.layers[n].status.value for s in valid).items())) for n in LAYERS},
        "basic_pass": sum(1 for s in valid if s.basic_pass is True),
        "neurosem_pass": sum(1 for s in valid if s.neurosem_pass is True),
        "unauthorized_edits_detected": sum(1 for s in valid if s.unauthorized_edits_detected is True),
        "basic_pass_battery_fail": {
            "count": k, "denominator": len(determinate),
            "fraction": (k / len(determinate)) if determinate else None,
            "excluded_provisional": len(valid) - len(frozen),
            "excluded_not_transformation_task": len(frozen) - len(transform),
            "excluded_no_model_change": sum(1 for s in transform if s.model_changed is False),
            "excluded_model_change_unknown": sum(1 for s in transform if s.model_changed is None),
            "excluded_indeterminate": len(changed) - len(determinate),
        },
    }


def write_score(score: TrialScore, path: Path) -> str:
    return write_immutable_text(Path(path), dumps(score))


# ----------------------------------------------------------------------------- scoring
@dc.dataclass
class ScoringContext:
    task: TaskSpec
    hidden: HiddenSpec
    frozen: FrozenConfig
    trial_dir: Path
    baseline_dir: Path
    work_dir: Path
    model: ModelRecord
    trial_id: str
    ignore_paths: tuple[str, ...]
    _run_copy: Path | None = None
    _oracle: Path | None = None
    _recorder: Any = None

    def run_copy(self) -> Path:
        """Simulations write output files, so they run in a copy and the trial stays as the agent left it."""
        if self._run_copy is None:
            dest = self.work_dir / "trial_run"
            if dest.exists():
                _rmtree(dest)
            shutil.copytree(self.trial_dir, dest)
            self._run_copy = dest
        return self._run_copy

    def oracle_root(self) -> Path:
        """The expected-behaviour model: pristine snapshot or exported state, plus hidden oracle steps."""
        if self._oracle is None:
            dest = self.work_dir / "oracle"
            if dest.exists():
                _rmtree(dest)
            if self.hidden.oracle_base == "pristine":
                ws = materialize(self.model, dest / "model")
            else:
                shutil.copytree(self.baseline_dir / "model", dest / "model")
                ws = Workspace(dest / "model", self.model)
            apply_steps(ws, self.hidden.oracle_steps, self.hidden.oracle_expected)
            self._oracle = dest
        return self._oracle

    def variant(self, label: str, root: Path) -> tuple[Workspace, VariantRecord]:
        ws = Workspace(root / "model", self.model)
        reference = label == "oracle" and self.hidden.oracle_base == "pristine" and not self.hidden.oracle_steps
        raw_id = f"agent-{self.task.task_id}-oracle" if label == "oracle" else f"agent-{self.task.task_id}-{self.trial_id}"
        return ws, VariantRecord(
            variant_id=re.sub(r"[^A-Za-z0-9_.-]", "_", raw_id), model_id=self.model.model_id,
            kind=VariantKind.REFERENCE if reference else VariantKind.MUTANT, family="agent_study",
            operator="oracle" if label == "oracle" else "agent_patch",
            description=f"agent study {self.task.task_id} {label}", tree_sha256=ws.tree_sha256(), created_utc=utc_now())

    def recorder(self, sim: Any) -> Any:
        if self._recorder is None:
            from nexclamp.validation.execution import RunRecorder

            self._recorder = RunRecorder(self.frozen.campaign, sim, results_root=self.frozen.results_root,
                                         work_root=self.work_dir / "runs",
                                         features_cfg=dict(self.frozen.cfgs["features"]) if "features" in self.frozen.cfgs
                                         else None, timeout_s=self.frozen.timeout_s)
        return self._recorder


class DefaultEvaluators:
    """Deterministic layer evaluators. Each method takes a :class:`ScoringContext`."""

    def __init__(self, sim: Any) -> None:
        self.sim = sim

    def schema_valid(self, ctx: ScoringContext) -> LayerOutcome:
        files = [ctx.trial_dir / f for f in ctx.hidden.validate_files]
        missing = [f for f, p in zip(ctx.hidden.validate_files, files) if not p.is_file()]
        if missing:
            return LayerOutcome("schema_valid", LayerStatus.FAIL, {"missing_files": missing})
        res = self.sim.validate(files)
        status = {True: LayerStatus.PASS, False: LayerStatus.FAIL}.get(res.valid, LayerStatus.ERROR)
        return LayerOutcome("schema_valid", status, {"validator": res.validator, "returncode": res.returncode,
                                                      "messages": res.messages[:50]})

    def executes(self, ctx: ScoringContext) -> LayerOutcome:
        from nexclamp.simulators.base import OutputSpec

        ex = ctx.hidden.execution
        lems = ctx.run_copy() / ex["lems"]
        if not lems.is_file():
            return LayerOutcome("executes", LayerStatus.FAIL, {"reason": f"{ex['lems']} does not exist"})
        res = self.sim.run_lems(lems, [OutputSpec(ex["output_file"], {"v": int(ex["v_column"])})],
                                timeout_s=ctx.frozen.timeout_s)
        status = (LayerStatus.PASS if res.status is RunStatus.OK
                  else LayerStatus.ERROR if res.status is RunStatus.TOOL_FAILURE else LayerStatus.FAIL)
        return LayerOutcome("executes", status, {"run_status": res.status.value, "runtime_s": round(res.runtime_s, 3),
                                                  "message": res.message, "output_tail": res.output_tail[-2000:]})

    def canonical_passes(self, ctx: ScoringContext) -> LayerOutcome:
        name = "canonical_passes"
        if not ctx.hidden.canonical.get("applicable", True):
            return LayerOutcome(name, LayerStatus.NOT_APPLICABLE)
        try:
            from nexclamp.protocols.definitions import CANONICAL_ID
            from nexclamp.validation.canonical import canonical_protocol
            from nexclamp.validation.fingerprint import Fingerprint, compare
        except ImportError as exc:
            return LayerOutcome(name, LayerStatus.ERROR, {"reason": f"canonical evaluator unavailable: {exc}"})
        tol = ctx.frozen.tolerance_table_obj()
        rec = ctx.recorder(self.sim)
        fps, run_ids = {}, {}
        for label, root in (("oracle", ctx.oracle_root()), ("trial", ctx.run_copy())):
            ws, variant = ctx.variant(label, root)
            out = rec.run_canonical(ws, variant, canonical_protocol(ws))
            run_ids[label] = [r.run_id for r in out.records]
            table = out.tables.get(CANONICAL_ID)
            if out.status is not RunStatus.OK or not table:
                if label == "oracle" or out.status is RunStatus.TOOL_FAILURE or out.status is RunStatus.OK:
                    return LayerOutcome(name, LayerStatus.ERROR, {"reason": f"{label} canonical run gave {out.status.value} "
                                                                  "without features", "messages": out.messages})
                return LayerOutcome(name, LayerStatus.FAIL, {"reason": f"trial canonical run {out.status.value}",
                                                             "messages": out.messages})
            fps[label] = Fingerprint(ctx.model.model_id, variant.variant_id, 1, ctx.frozen.dt_ms, out.status, None,
                                     {CANONICAL_ID: table}, {CANONICAL_ID: run_ids[label][0] if run_ids[label] else ""})
        dets = compare(fps["oracle"], fps["trial"], tol, ctx.frozen.tolerance_multiplier)
        return LayerOutcome(name, LayerStatus.FAIL if dets else LayerStatus.PASS,
                            {"detections": to_jsonable(dets), "run_ids": run_ids})

    def hidden_battery_passes(self, ctx: ScoringContext) -> LayerOutcome:
        name = "hidden_battery_passes"
        b = ctx.hidden.battery
        if not b.get("applicable"):
            return LayerOutcome(name, LayerStatus.NOT_APPLICABLE)
        try:
            from nexclamp.protocols.definitions import CANONICAL_ID, templates_from_config
            from nexclamp.schemas import ExecConfig
            from nexclamp.validation.canonical import canonical_protocol
            from nexclamp.validation.fingerprint import RHEOBASE_ID, build_fingerprint, compare
        except ImportError as exc:
            return LayerOutcome(name, LayerStatus.ERROR, {"reason": f"battery evaluator unavailable: {exc}"})
        if b["model_id"] != ctx.model.model_id:
            raise HiddenSpecError(f"battery model {b['model_id']} is not the task's base model {ctx.model.model_id}")
        wanted = list(dict.fromkeys((list(ctx.frozen.selected_protocols) if b.get("frozen_selection") else [])
                                    + list(b.get("additional_protocols") or [])))
        rheobase = ctx.frozen.reference_rheobase_nA.get(ctx.model.model_id)
        study = ctx.frozen.cfgs.get("study")
        if not wanted or rheobase is None or not study:
            return LayerOutcome(name, LayerStatus.ERROR, {"reason": "frozen config lacks protocol selection, reference "
                                                          "rheobase or study config"})
        templates = {t.protocol_id: t for t in templates_from_config(study.get("protocols"))}
        settle = float(study["numerics"]["settle_ms"])
        probe_ids = [p for p in wanted if p not in (CANONICAL_ID, RHEOBASE_ID)]
        unusable = [p for p in probe_ids if p not in templates or not templates[p].implemented]
        if unusable:
            return LayerOutcome(name, LayerStatus.ERROR, {"reason": f"protocols not available: {unusable}"})
        protos = [templates[p].instantiate(rheobase, settle) for p in probe_ids]
        tol = ctx.frozen.tolerance_table_obj()
        rec = ctx.recorder(self.sim)
        nominal = ExecConfig(dt_ms=ctx.frozen.dt_ms)
        fps = {}
        for label, root in (("oracle", ctx.oracle_root()), ("trial", ctx.run_copy())):
            ws, variant = ctx.variant(label, root)
            fps[label] = build_fingerprint(rec, ws, variant, protos, canonical_protocol(ws), nominal, 1,
                                           dict(study["rheobase"]), settle, include_rheobase=RHEOBASE_ID in wanted,
                                           include_canonical=CANONICAL_ID in wanted)
        if fps["oracle"].status is not RunStatus.OK:
            return LayerOutcome(name, LayerStatus.ERROR, {"reason": f"oracle battery {fps['oracle'].status.value}",
                                                          "messages": fps["oracle"].messages})
        if fps["trial"].status is not RunStatus.OK:
            return LayerOutcome(name, LayerStatus.FAIL, {"reason": f"trial battery {fps['trial'].status.value}",
                                                         "messages": fps["trial"].messages})
        feats = b.get("features", "frozen")
        dets = [d for d in compare(fps["oracle"], fps["trial"], tol, ctx.frozen.tolerance_multiplier)
                if d.protocol_id in wanted and (feats == "frozen" or d.feature in feats)]
        return LayerOutcome(name, LayerStatus.FAIL if dets else LayerStatus.PASS,
                            {"protocols": wanted, "detections": to_jsonable(dets),
                             "run_ids": {k: fp.run_ids for k, fp in fps.items()}})

    def hidden_assertions_pass(self, ctx: ScoringContext) -> LayerOutcome:
        results = [evaluate_assertion(a, ctx.trial_dir, ctx.baseline_dir) for a in ctx.hidden.assertions]
        if not results:
            return LayerOutcome("hidden_assertions_pass", LayerStatus.NOT_APPLICABLE)
        status = LayerStatus.PASS if all(r.passed for r in results) else LayerStatus.FAIL
        return LayerOutcome("hidden_assertions_pass", status, {"assertions": to_jsonable(results)})

    def edit_scope(self, ctx: ScoringContext) -> LayerOutcome:
        changes = semantic_diff(ctx.baseline_dir, ctx.trial_dir, ctx.ignore_paths)
        res = classify_changes(changes, ctx.hidden.permitted_changes,
                               representation_only_is_unauthorized=ctx.hidden.representation_only_is_unauthorized)
        return LayerOutcome("edit_scope", LayerStatus.FAIL if res.unauthorized else LayerStatus.PASS,
                            {"n_changes": len(changes),
                             "n_model_changes": sum(1 for c in changes if c.file.startswith("model/")),
                             "permitted": to_jsonable(res.permitted),
                             "representation_only": to_jsonable(res.representation_only),
                             "unauthorized": to_jsonable(res.unauthorized)})


def _model_changed(outcome: LayerOutcome) -> bool | None:
    n = outcome.details.get("n_model_changes") if outcome.status in (LayerStatus.PASS, LayerStatus.FAIL) else None
    return None if n is None else n > 0


def score_trial(task_id: str, trial_dir: Path, frozen_config: FrozenConfig | Path | str, *,
                private_dir: Path | None = None, private_root: Path = PRIVATE_ROOT, evaluators: Any = None,
                sim: Any = None, policy: AgentPolicy | None = None, tasks_root: Path = TASKS_DIR,
                hidden_root: Path = HIDDEN_DIR, public_common: Path | None = None, repo_root: Path = REPO_ROOT,
                models: Mapping[str, ModelRecord] | None = None, trial_id: str | None = None) -> TrialScore:
    """Score a finished trial layer by layer with the hidden evaluator.

    ``frozen_config`` is a :class:`FrozenConfig` or the path of a frozen config file (loaded with
    :func:`load_frozen_config`). The private record defaults to ``<private_root>/<trial dir name>``.
    Under a frozen (non-provisional) config the hidden spec, the current task files and policy,
    the export record and the evaluator's Git state must all match the freeze.

    Edit scope and hidden assertions are always evaluated. Schema validity, execution,
    canonical regression and the hidden battery form a cascade: a layer runs only if every
    earlier one passed or was not applicable. An evaluator that raises yields ``error`` for its
    layer (never ``pass`` or ``fail``), so unexpected tool problems make the trial indeterminate.
    """
    if frozen_config is None:
        raise FrozenConfigError("score_trial needs a frozen evaluation config (a FrozenConfig or the path of "
                                "frozen_agent_eval.yaml); use FrozenConfig.development() only for harness development")
    if isinstance(frozen_config, (str, Path)):
        frozen_config = load_frozen_config(Path(frozen_config), repo_root, tasks_root=tasks_root,
                                           hidden_root=hidden_root, public_common=public_common)
    if not isinstance(frozen_config, FrozenConfig):
        raise FrozenConfigError(f"frozen_config must be a FrozenConfig or a path, not {type(frozen_config).__name__}")
    policy = policy or load_policy()
    models = dict(models) if models is not None else load_models()
    task = load_task(task_id, tasks_root, policy=policy, model_ids=models)
    hidden = load_hidden_spec(task_id, hidden_root)
    frozen_config.check_hidden_spec(hidden)
    trial_dir = Path(trial_dir).resolve()
    private_dir = (Path(private_dir).resolve() if private_dir is not None
                   else default_private_dir(trial_dir, private_root).resolve())
    record = load_export_record(private_dir)
    if record["task_id"] != task_id:
        raise AgentStudyError(f"{trial_dir} was exported for {record['task_id']}, not {task_id}")
    common = Path(public_common) if public_common is not None else Path(tasks_root).parent / "public_common"
    frozen_config.check_trial_inputs(task, policy, record, common)
    if not frozen_config.provisional:
        repo = Path(repo_root)
        frozen_config.check_evaluator_state(source_state(repo, [repo / "src" / "nexclamp", repo / "agent_study",
                                                                repo / "configs"]))
    work = private_dir / "scoring_work"
    if work.exists():
        _rmtree(work)
    work.mkdir(parents=True)
    ctx = ScoringContext(task, hidden, frozen_config, trial_dir, private_dir / "baseline", work,
                         models[task.base_model], trial_id or trial_dir.name,
                         tuple(policy.ignore_paths) + tuple(hidden.ignore_paths))
    if evaluators is None:
        from nexclamp.simulators.jneuroml import JNeuroML

        evaluators = DefaultEvaluators(sim or JNeuroML())

    def run(layer: str) -> LayerOutcome:
        try:
            outcome = getattr(evaluators, layer)(ctx)
        except Exception as exc:  # any evaluator failure is recorded as an error, never as a verdict
            return LayerOutcome(layer, LayerStatus.ERROR, {"reason": f"{type(exc).__name__}: {exc}"})
        if outcome.layer != layer:
            raise AgentStudyError(f"evaluator for {layer} returned an outcome for {outcome.layer}")
        return outcome

    outcomes = {"edit_scope": run("edit_scope"), "hidden_assertions_pass": run("hidden_assertions_pass")}
    blocked = None
    for layer in CASCADE_LAYERS:
        if blocked is not None:
            outcomes[layer] = LayerOutcome(layer, LayerStatus.NOT_EVALUATED, {"reason": f"{blocked} did not pass"})
            continue
        outcomes[layer] = run(layer)
        if outcomes[layer].status not in PASSING:
            blocked = layer
    return aggregate(task_id, outcomes, trial_id=ctx.trial_id, provisional=frozen_config.provisional,
                     frozen_config_sha256=frozen_config.sha256, hidden_spec_sha256=hidden.sha256,
                     export_content_sha256=record["content_sha256"], task_type=task.type,
                     model_changed=_model_changed(outcomes["edit_scope"]))


# ----------------------------------------------------------------------------- trial log
TRIAL_LOG_FORMAT = "neurosem-trial-log/1"
TERMINATIONS = ("completed", "budget_exhausted", "wall_clock_limit", "agent_error", "tool_failure")
COST_KEYS = ("usd", "input_tokens", "output_tokens", "source")
SESSION_KEYS = ("fresh_session", "resumed", "command_line", "environment_id")


@dc.dataclass
class TrialLog:
    """How one trial was run (spec: version, model id, access date, permissions, budget, prompt,
    transcript, patch, logs, costs; manual intervention is prohibited)."""

    trial_id: str
    task_id: str
    claude_code_version: str           # exactly as reported by the CLI
    model_identifier: str              # exactly as reported by the session
    access_date: str                   # YYYY-MM-DD
    permissions: dict[str, Any]        # the policy permissions block in force
    permissions_sha256: str
    budget: dict[str, float]
    prompt_sha256: str
    transcript_path: str
    transcript_sha256: str
    patch_path: str
    patch_sha256: str
    logs: list[dict[str, Any]]         # [{path, sha256}] tool/session logs collected after the trial (may be [])
    costs: dict[str, Any]              # usd, input_tokens, output_tokens (None if unreported) and their source
    human_interventions: list[dict[str, Any]]   # must be empty
    export_content_sha256: str
    session: dict[str, Any]            # fresh_session, resumed, command_line, environment_id
    started_utc: str
    ended_utc: str
    termination: str
    notes: str = ""
    format: str = TRIAL_LOG_FORMAT


def _valid_iso_date(s: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(s)):
        return False
    try:
        dt.date.fromisoformat(str(s))
    except ValueError:
        return False
    return True


def validate_trial_log(log: TrialLog, *, task: TaskSpec | None = None, policy: AgentPolicy | None = None,
                       export_record: Mapping[str, Any] | None = None, root: Path | None = None,
                       private_dir: Path | None = None, trial_dir: Path | None = None) -> list[str]:
    """Problems that make a trial invalid or its log incomplete (empty = valid).

    With ``root`` (the folder relative paths in the log resolve against) the transcript, patch
    and log files are re-hashed. With ``private_dir`` and ``trial_dir`` the recorded patch must equal
    :func:`make_patch` of the private baseline and the returned trial (policy ignore paths applied).
    """
    problems = []
    for name in ("trial_id", "task_id", "claude_code_version", "model_identifier", "prompt_sha256", "transcript_path",
                 "transcript_sha256", "patch_path", "patch_sha256", "export_content_sha256", "started_utc", "ended_utc"):
        if not str(getattr(log, name)).strip():
            problems.append(f"{name} is empty")
    if log.format != TRIAL_LOG_FORMAT:
        problems.append(f"format must be {TRIAL_LOG_FORMAT}")
    if not _valid_iso_date(log.access_date):
        problems.append("access_date must be a real calendar date written YYYY-MM-DD")
    if not isinstance(log.logs, list) or any(not isinstance(e, Mapping) or not str(e.get("path", "")).strip()
                                             or not str(e.get("sha256", "")).strip() for e in log.logs):
        problems.append("logs must be a list of {path, sha256} entries")

    def resolve(p: str) -> Path:
        q = Path(p)
        return q if q.is_absolute() or root is None else Path(root) / q

    if root is not None:
        entries = [("transcript", log.transcript_path, log.transcript_sha256), ("patch", log.patch_path, log.patch_sha256)]
        entries += [(f"log {e.get('path')}", str(e.get("path", "")), str(e.get("sha256", "")))
                    for e in (log.logs if isinstance(log.logs, list) else []) if isinstance(e, Mapping)]
        for label, p, digest in entries:
            f = resolve(p)
            if not str(p).strip() or not f.is_file():
                problems.append(f"{label} file {p!r} not found")
            elif sha256_file(f) != digest:
                problems.append(f"{label} sha256 does not match the file")
    if private_dir is not None and trial_dir is not None:
        f = resolve(log.patch_path)
        expected = make_patch(Path(private_dir) / "baseline", Path(trial_dir), policy.ignore_paths if policy else ())
        if not f.is_file() or f.read_text(encoding="utf-8") != expected:
            problems.append("patch file differs from make_patch(baseline, trial)")
    if log.termination not in TERMINATIONS:
        problems.append(f"termination must be one of {TERMINATIONS}")
    if log.human_interventions:
        problems.append(f"{len(log.human_interventions)} human intervention(s) recorded: manual intervention during an "
                        "autonomous trial is prohibited, so this trial is invalid")
    problems += [f"costs.{k} not recorded" for k in COST_KEYS if k not in log.costs]
    problems += [f"session.{k} not recorded" for k in SESSION_KEYS if k not in log.session]
    if log.session.get("fresh_session") is not True or log.session.get("resumed") is not False:
        problems.append("trial did not run in a fresh, non-resumed session")
    if log.permissions_sha256 != sha256_json(to_jsonable(log.permissions)):
        problems.append("permissions_sha256 does not match the recorded permissions")
    if policy is not None:
        if log.permissions_sha256 != policy.permissions_sha256:
            problems.append("permissions differ from the frozen agent policy")
    if task is not None:
        if log.task_id != task.task_id:
            problems.append("task_id does not match the task")
        if log.prompt_sha256 != sha256_file(task.prompt_path):
            problems.append("prompt hash differs from the frozen prompt")
        if {k: float(v) for k, v in log.budget.items()} != {k: float(v) for k, v in task.budget.items()}:
            problems.append("budget differs from the task budget")
    if export_record is not None and log.export_content_sha256 != export_record["content_sha256"]:
        problems.append("trial did not start from the recorded clean export")
    return problems


def write_trial_log(log: TrialLog, path: Path) -> str:
    """Write the log once (raw results are immutable); returns its SHA-256."""
    return write_immutable_text(Path(path), dumps(log))


def read_trial_log(path: Path) -> TrialLog:
    return TrialLog(**json.loads(Path(path).read_text(encoding="utf-8")))
