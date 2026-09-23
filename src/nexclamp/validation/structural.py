"""Structural validity (validation layer 1).

Oracle: ``jnml -validate`` (NeuroML v2.3.1 schema + jNeuroML's model tests), applied to
EVERY NeuroML file the model reads -- the cell file's include closure plus the NeuroML
files of the shipped harness -- one block per file in a single JVM call.

Two facts verified on the fixtures (2026-09-13) force a *relative* rule:

1. Validating a cell file does not schema-check the files it includes (a unit typo in
   an included channel file passed), so validating only the cell file would let invalid
   mutants through.
2. Upstream reference files may fail standalone schema validation by design: the LTS
   cell's ``IT.channel.nml`` and ``Ca.nml`` use custom LEMS ComponentTypes. Open Source
   Brain's own CI validates only the cell and network files, which pass.

Rule. A *reference* is structurally valid when its cell file and every harness network
file validate; any other failing file is recorded as a baseline error. A *variant* is
structurally valid when it passes the same cell/network requirement and produces no
validation error that its reference did not already have. libNeuroML's strict validation
is recorded for information only.
"""

from __future__ import annotations

import contextlib
import dataclasses as dc
import io
import re
from pathlib import Path

from nexclamp.models import Workspace
from nexclamp.schemas import ValidationResult
from nexclamp.simulators.base import Simulator

_INCLUDE_RE = re.compile(r'<Include\s+file\s*=\s*"([^"]+)"', re.IGNORECASE)
_BUILTIN = {"Cells.xml", "Networks.xml", "Simulation.xml", "Inputs.xml", "Channels.xml", "Synapses.xml", "PyNN.xml",
            "NeuroML2CoreTypes.xml", "NeuroMLCoreDimensions.xml", "NeuroMLCoreCompTypes.xml"}
_BLOCK_RE = re.compile(r"^Validating: (.+?)\s*$", re.MULTILINE)
_ERROR_LINE = re.compile(r"^\s*(cvc-[^\n]+|It must be [^\n]+|Test: [^\n]*failed[^\n]*|[^\n]*not found[^\n]*)$", re.MULTILINE)


@dc.dataclass
class StructuralResult:
    valid: bool | None
    jnml: ValidationResult
    libneuroml_strict: bool | None
    libneuroml_messages: list[str]
    files: list[str]
    per_file: dict[str, dict] = dc.field(default_factory=dict)       # rel path -> {"valid": bool, "errors": [...]}
    required_files: list[str] = dc.field(default_factory=list)       # cell file + harness network files
    baseline_invalid_files: list[str] = dc.field(default_factory=list)
    baseline_errors: list[str] = dc.field(default_factory=list)      # every normalised error in this workspace
    new_errors: list[str] = dc.field(default_factory=list)           # errors absent from the reference


def harness_nml_files(ws: Workspace) -> list[Path]:
    """NeuroML files included directly by the shipped harness LEMS file."""
    if not ws.harness_path.is_file():
        return []
    text = ws.harness_path.read_text(encoding="utf-8", errors="replace")
    out = []
    for inc in _INCLUDE_RE.findall(text):
        if Path(inc).name in _BUILTIN or inc.startswith("NeuroML2CoreTypes/"):
            continue
        p = (ws.harness_path.parent / inc).resolve()
        if p.suffix == ".nml" and p.is_file():
            out.append(p)
    return out


def model_nml_files(ws: Workspace) -> list[Path]:
    """Cell-file include closure plus harness NeuroML files (and their closures), cell file first."""
    from nexclamp.validation.execution import reachable_files

    ordered: dict[Path, None] = {ws.cell_path.resolve(): None}
    for entry in [ws.cell_path, *harness_nml_files(ws)]:
        for p in reachable_files(entry):
            if p.suffix == ".nml":
                ordered.setdefault(p, None)
    return list(ordered)


def _is_network_file(path: Path) -> bool:
    try:
        return re.search(r"<network\b", path.read_text(encoding="utf-8", errors="replace")) is not None
    except OSError:
        return False


def parse_blocks(raw: str) -> dict[str, dict]:
    """Split multi-file ``jnml -validate`` output into per-file verdicts and normalised errors."""
    out: dict[str, dict] = {}
    matches = list(_BLOCK_RE.finditer(raw))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        block = raw[m.end():end]
        block = block.split("\nValidated ", 1)[0]
        errors = sorted({ln.strip() for ln in _ERROR_LINE.findall(block)})
        valid = "Valid against schema and all tests" in block and not errors
        if not valid and not errors:
            errors = ["unclassified validation failure: " + " ".join(block.split())[:300]]
        out[str(Path(m.group(1)).resolve())] = {"valid": valid, "errors": errors}
    return out


def libneuroml_strict(path: Path) -> tuple[bool | None, list[str]]:
    try:
        from neuroml.utils import validate_neuroml2
    except ImportError:
        return None, ["libNeuroML not installed"]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            validate_neuroml2(str(path))
        return True, []
    except ValueError as exc:
        return False, [str(exc)[:1000]]
    except Exception as exc:  # parse errors, missing includes: still "not strictly valid"
        return False, [f"{type(exc).__name__}: {str(exc)[:1000]}"]


def check(ws: Workspace, sim: Simulator, reference: StructuralResult | None = None) -> StructuralResult:
    root = ws.root.resolve()

    def rel(p: Path) -> str:
        return p.relative_to(root).as_posix() if p.is_relative_to(root) else str(p)

    if not ws.cell_path.is_file():
        vr = ValidationResult(False, 1, [f"missing cell file: {ws.model.cell_file}"], "", "neurosem")
        return StructuralResult(False, vr, False, [], [ws.model.cell_file], new_errors=[f"missing cell file {ws.model.cell_file}"])
    files = model_nml_files(ws)
    required = [ws.cell_path.resolve()] + [p for p in harness_nml_files(ws) if _is_network_file(p)]
    vr = sim.validate(files)
    strict, strict_msgs = libneuroml_strict(ws.cell_path)
    if vr.valid is None:
        return StructuralResult(None, vr, strict, strict_msgs, [rel(p) for p in files])
    blocks = parse_blocks(vr.raw_output)
    per_file: dict[str, dict] = {}
    for p in files:
        b = blocks.get(str(p))
        per_file[rel(p)] = b if b is not None else {"valid": False, "errors": ["no validator output for file"]}
    all_errors = sorted({e for b in per_file.values() for e in b["errors"]})
    required_ok = all(per_file[rel(p)]["valid"] for p in dict.fromkeys(required))
    baseline_invalid = sorted(k for k, b in per_file.items() if not b["valid"])
    if reference is None:
        new_errors = [] if required_ok else sorted({e for p in required for e in per_file[rel(p)]["errors"]})
        valid = required_ok
    else:
        new_errors = sorted(set(all_errors) - set(reference.baseline_errors))
        valid = required_ok and not new_errors
    return StructuralResult(valid, vr, strict, strict_msgs, [rel(p) for p in files], per_file,
                            [rel(p) for p in dict.fromkeys(required)], baseline_invalid, all_errors, new_errors)
