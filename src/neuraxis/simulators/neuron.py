"""NEURON adapter: cross-simulator execution of the same NeuroML model (N-08).

The specification calls cross-simulator agreement "optional but valuable". It matters here for one
specific reason: every detection in this study comes from jLEMS's fixed-step forward Euler
integrator. A reviewer is entitled to ask whether a "behaviour change" is a property of the model or
of that integrator. Running the identical NeuroML through NEURON's own integrator answers it.

How it works
------------
1. **Export.** ``jnml <LEMS file> -neuron`` translates the LEMS simulation into NEURON sources: one
   ``.mod`` mechanism per ion channel and input, a ``.hoc`` cell definition, and a
   ``<stem>_nrn.py`` runner. This needs only Java and the jNeuroML jar, so it works wherever the
   rest of the study works, **even with no NEURON runtime installed**.
2. **Compile.** ``nrnivmodl`` builds the mechanisms into a loadable library.
3. **Run.** The generated runner executes under a NEURON-enabled Python and writes the same
   ``OutputFile`` columns the jLEMS run writes, so the traces feed the identical feature and
   trace-comparison code with no special-casing downstream.

What this adapter deliberately does not do
------------------------------------------
It defines no cross-simulator *detection* threshold. Tolerances in this study are calibrated against
one integrator's own discretisation error (h versus h/2). Two different integrators differ for
reasons that have nothing to do with a mutation, so a cross-simulator comparison is reported as a
**descriptive agreement measurement** (spike counts, first-spike latency, spike-time differences,
trace RMSE), never as a pass or fail. Making it a detection rule would need its own calibration
study, which is out of scope and recorded as such.

Availability
------------
``available()`` is true only when the NEURON Python module **and** ``nrnivmodl`` are both present.
``export_available()`` is true whenever Java and the jNeuroML jar are present. The two are separate
on purpose: half of the evidence -- that the model translates to another simulator at all -- is
collectable on any machine, and the cross-simulator report then says "exported, not executed"
instead of silently skipping.
"""

from __future__ import annotations

import dataclasses as dc
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from neuraxis.schemas import RunStatus, SimResult, ValidationResult
from neuraxis.simulators.base import PHYSICAL_V_BOUND_MV, OutputSpec
from neuraxis.simulators.jneuroml import find_jar, find_java, load_dat

MOD_SUFFIXES = (".mod", ".hoc", ".py")


@dc.dataclass(frozen=True)
class ExportResult:
    """Outcome of ``jnml -neuron`` on one LEMS file."""

    ok: bool
    returncode: int
    runner: Path | None                 # the generated <stem>_nrn.py
    mod_files: tuple[Path, ...]
    hoc_files: tuple[Path, ...]
    duration_s: float
    output: str

    @property
    def files(self) -> tuple[Path, ...]:
        return (*(f for f in (self.runner,) if f is not None), *self.mod_files, *self.hoc_files)


def export_to_neuron(lems_file: Path, java: Path | None = None, jar: Path | None = None,
                     timeout_s: float = 900.0, max_memory: str = "2G") -> ExportResult:
    """Translate a LEMS simulation into NEURON sources with ``jnml -neuron``.

    Needs Java and the jNeuroML jar only. Generated files land beside the LEMS file, which in this
    study is always a private workspace copy and never a stored model snapshot.
    """
    lems_file = Path(lems_file).resolve()
    java, jar = java or find_java(), jar or find_jar()
    if not (java and jar):
        return ExportResult(False, -1, None, (), (), 0.0, "Java or jNeuroML jar missing")
    root = lems_file.parent
    before = {p for p in root.rglob("*") if p.suffix in MOD_SUFFIXES}
    cmd = [str(java), f"-Xmx{max_memory}", "-Djava.awt.headless=true", "-jar", str(jar), str(lems_file), "-neuron"]
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=root)
    except subprocess.TimeoutExpired:
        return ExportResult(False, -1, None, (), (), time.perf_counter() - t0, f"export timed out after {timeout_s}s")
    except OSError as exc:
        return ExportResult(False, -1, None, (), (), time.perf_counter() - t0, f"tool failure: {exc}")
    made = sorted({p for p in root.rglob("*") if p.suffix in MOD_SUFFIXES} - before)
    runner = next((p for p in made if p.name.endswith("_nrn.py")), None)
    return ExportResult(proc.returncode == 0 and runner is not None, proc.returncode, runner,
                        tuple(p for p in made if p.suffix == ".mod"), tuple(p for p in made if p.suffix == ".hoc"),
                        time.perf_counter() - t0, (proc.stdout + proc.stderr)[-4000:])


class NeuronSimulator:
    """Runs a NeuroML model through NEURON by way of the jNeuroML NEURON export."""

    name = "NEURON"

    def __init__(self, python: Path | None = None, nrnivmodl: Path | None = None) -> None:
        self.python = Path(python) if python else Path(sys.executable)
        found = shutil.which("nrnivmodl")
        self.nrnivmodl = Path(nrnivmodl) if nrnivmodl else (Path(found) if found else None)
        self._version: str | None = None
        self._probed = False

    # ------------------------------------------------------------------ facts
    def export_available(self) -> bool:
        """True when the model can be translated to NEURON sources, runtime present or not."""
        return bool(find_java() and find_jar())

    def _module_version(self) -> str | None:
        if self._probed:
            return self._version
        self._probed = True
        probe = "import neuron, sys; sys.stdout.write(neuron.__version__)"
        try:
            proc = subprocess.run([str(self.python), "-c", probe], capture_output=True, text=True, timeout=180)
        except (OSError, subprocess.TimeoutExpired):
            return None
        self._version = proc.stdout.strip() or None if proc.returncode == 0 else None
        return self._version

    def available(self) -> bool:
        return self._module_version() is not None and self.nrnivmodl is not None

    def version_info(self) -> dict[str, str]:
        v = self._module_version()
        if v is None:
            return {"simulator": "NEURON", "status": "not installed",
                    "export_available": str(self.export_available()),
                    "note": "NeuroML-to-NEURON export still works; only execution needs the runtime"}
        return {"simulator": "NEURON", "neuron_version": v, "python": str(self.python),
                "nrnivmodl": str(self.nrnivmodl), "export_available": str(self.export_available())}

    def version_string(self) -> str:
        v = self._module_version()
        return f"NEURON {v}" if v else "NEURON (not installed)"

    def validate(self, files: list[Path]) -> ValidationResult:
        """NEURON has no NeuroML validator; validity stays jNeuroML's answer (the relative oracle, D-006)."""
        return ValidationResult(None, -1, ["NEURON does not validate NeuroML; use jNeuroML"], "", self.name)

    # --------------------------------------------------------------- execution
    def compile_mechanisms(self, directory: Path, timeout_s: float = 900.0) -> tuple[bool, str]:
        """Build the exported ``.mod`` files. A failure here is a tool failure, never a model property."""
        directory = Path(directory).resolve()
        if not any(directory.glob("*.mod")):
            return True, "no .mod files to compile"
        if self.nrnivmodl is None:
            return False, "nrnivmodl not found on PATH"
        try:
            proc = subprocess.run([str(self.nrnivmodl)], capture_output=True, text=True,
                                  timeout=timeout_s, cwd=directory)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"nrnivmodl failed to start or timed out: {exc}"
        return proc.returncode == 0, (proc.stdout + proc.stderr)[-4000:]

    def run_lems(self, lems_file: Path, outputs: list[OutputSpec], timeout_s: float = 3600.0,
                 sample_every_ms: float | None = None) -> SimResult:
        """Export, compile and run, then read the same output columns the jLEMS run reads."""
        lems_file = Path(lems_file).resolve()
        t0 = time.perf_counter()
        if not self.export_available():
            return SimResult(RunStatus.TOOL_FAILURE, -1, 0.0, {}, [], "Java or jNeuroML jar missing for the export")
        exported = export_to_neuron(lems_file, timeout_s=min(timeout_s, 900.0))
        if not exported.ok or exported.runner is None:
            return SimResult(RunStatus.TOOL_FAILURE, exported.returncode, time.perf_counter() - t0, {}, [],
                             f"jnml -neuron export failed: {exported.output[-600:]}")
        if not self.available():
            return SimResult(RunStatus.TOOL_FAILURE, -1, time.perf_counter() - t0, {}, [],
                             "NEURON runtime not installed: the model exported successfully but cannot be executed "
                             "here. Install NEURON (pip install neuron on Linux or macOS, or the official Windows "
                             "installer) and re-run; the export artefacts are already recorded.")
        work = exported.runner.parent
        built, build_log = self.compile_mechanisms(work, timeout_s=min(timeout_s, 900.0))
        if not built:
            return SimResult(RunStatus.TOOL_FAILURE, -1, time.perf_counter() - t0, {}, [],
                             f"nrnivmodl could not build the exported mechanisms: {build_log[-600:]}")
        cmd = [str(self.python), exported.runner.name]
        env = {**os.environ, "NEURON_MODULE_OPTIONS": "-nogui"}
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, cwd=work, env=env)
        except subprocess.TimeoutExpired:
            return SimResult(RunStatus.TIMEOUT, -1, time.perf_counter() - t0, {}, cmd,
                             f"NEURON run exceeded {timeout_s}s")
        except OSError as exc:
            return SimResult(RunStatus.TOOL_FAILURE, -1, time.perf_counter() - t0, {}, cmd, f"tool failure: {exc}")
        runtime = time.perf_counter() - t0
        out = proc.stdout + proc.stderr
        tail = "\n".join(out.strip().splitlines()[-25:])
        if proc.returncode != 0:
            return SimResult(RunStatus.RUNTIME_ERROR, proc.returncode, runtime, {}, cmd, tail[-500:], tail,
                             proc.stdout[-4000:], proc.stderr[-4000:])
        try:
            traces: dict = {}
            for spec in outputs:
                traces.update(load_dat(work / spec.file, spec.columns, sample_every_ms))
        except (FileNotFoundError, ValueError, IndexError) as exc:
            return SimResult(RunStatus.RUNTIME_ERROR, proc.returncode, runtime, {}, cmd,
                             f"output unreadable: {exc}", tail, proc.stdout[-4000:], proc.stderr[-4000:])
        for name, tr in traces.items():
            if not np.all(np.isfinite(tr.v_mV)) or np.max(np.abs(tr.v_mV)) > PHYSICAL_V_BOUND_MV:
                return SimResult(RunStatus.UNSTABLE, proc.returncode, runtime, traces, cmd,
                                 f"non-finite or out-of-bound voltage in {name}", tail,
                                 proc.stdout[-4000:], proc.stderr[-4000:])
        return SimResult(RunStatus.OK, proc.returncode, runtime, traces, cmd, "", tail,
                         proc.stdout[-4000:], proc.stderr[-4000:])
