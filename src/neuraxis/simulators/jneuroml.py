"""jNeuroML / jLEMS adapter.

NeuroSem calls the jNeuroML jar bundled with pyNeuroML directly, with an argument list
(no shell), instead of pyNeuroML's runner helpers. Reasons, from the Milestone 0 audit
(docs/DEPENDENCY_AUDIT.md): those helpers return a bare ``False`` both for an invalid model
and for a missing Java runtime, some paths call ``sys.exit``, and they build commands
with ``shell=True`` and a colon-joined include path that is fragile on Windows.

Behaviour verified on this machine (Temurin 21.0.12.1, jNeuroML 0.14.0 / jLEMS 0.12.0):
``-validate`` exits 0 and prints "All valid" for valid files, exits 1 with schema or
"Test: ... failed" messages otherwise; LEMS runs exit 1 with ``ContentError`` for
unresolvable components; OutputFile columns are SI (s, V).
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np
import pandas as pd

from neuraxis.provenance import REPO_ROOT, env_var, sha256_file
from neuraxis.schemas import RunStatus, SimResult, Trace, ValidationResult
from neuraxis.simulators.base import PHYSICAL_V_BOUND_MV, OutputSpec

_OUTPUT_FILE_RE = re.compile(r'<OutputFile\b[^>]*\bfileName\s*=\s*"([^"]+)"')
_DT_HINT = re.compile(r"caused by too large a time step|NaN|Infinity", re.IGNORECASE)


class ToolUnavailable(RuntimeError):
    pass


def find_java() -> Path | None:
    candidates: list[Path] = []
    if env := env_var("JAVA"):
        candidates.append(Path(env))
    exe = "java.exe" if os.name == "nt" else "java"
    candidates += sorted((REPO_ROOT / ".tools").glob(f"jdk-*/bin/{exe}"), reverse=True)
    candidates += sorted((REPO_ROOT / ".tools").glob(f"jdk-*/Contents/Home/bin/{exe}"), reverse=True)   # macOS layout
    if home := os.environ.get("JAVA_HOME"):
        candidates.append(Path(home) / "bin" / exe)
    if which := shutil.which("java"):
        candidates.append(Path(which))
    return next((c for c in candidates if c.is_file()), None)


def find_jar() -> Path | None:
    if env := env_var("JNML_JAR"):
        p = Path(env)
        return p if p.is_file() else None
    try:
        from pyneuroml.utils.misc import get_path_to_jnml_jar
    except ImportError:
        return None
    p = Path(get_path_to_jnml_jar()).resolve()
    return p if p.is_file() else None


class JNeuroML:
    name = "jNeuroML"

    def __init__(self, java: Path | None = None, jar: Path | None = None, max_memory: str = "2G") -> None:
        self.java = java or find_java()
        self.jar = jar or find_jar()
        self.max_memory = max_memory
        self._version: dict[str, str] | None = None

    # ------------------------------------------------------------------ facts
    def available(self) -> bool:
        return bool(self.java and self.jar)

    def _require(self) -> tuple[Path, Path]:
        if not self.java:
            raise ToolUnavailable("Java runtime not found (set NEURAXIS_JAVA or run scripts/bootstrap_java.py)")
        if not self.jar:
            raise ToolUnavailable("jNeuroML jar not found (pip install pyneuroml==1.3.22)")
        return self.java, self.jar

    def version_info(self) -> dict[str, str]:
        if self._version is not None:
            return self._version
        java, jar = self._require()
        jv = subprocess.run([str(java), "-version"], capture_output=True, text=True, timeout=60)
        java_version = (jv.stderr or jv.stdout).strip().splitlines()
        jn = subprocess.run([str(java), "-jar", str(jar), "-v"], capture_output=True, text=True, timeout=120)
        versions = dict(re.findall(r"^\s*(jNeuroML|org\.neuroml\.\w+|jLEMS)\s+v(\S+)", jn.stdout, re.MULTILINE))
        self._version = {
            "simulator": "jNeuroML",
            "jneuroml_version": versions.get("jNeuroML", "unknown"),
            "jlems_version": versions.get("jLEMS", "unknown"),
            "org_neuroml_export_version": versions.get("org.neuroml.export", "unknown"),
            "java_version": " | ".join(java_version),
            "jar_path": jar.name,
            "jar_sha256": sha256_file(jar),
        }
        return self._version

    def version_string(self) -> str:
        v = self.version_info()
        return f"jNeuroML {v['jneuroml_version']} / jLEMS {v['jlems_version']}"

    # ------------------------------------------------------------- validation
    def validate(self, files: list[Path], timeout_s: float = 600.0) -> ValidationResult:
        missing = [str(f) for f in files if not Path(f).is_file()]
        if missing:   # a caller error, not a tool failure and not a model property
            raise FileNotFoundError(f"cannot validate missing files: {missing}")
        if not self.available():
            return ValidationResult(None, -1, ["tool unavailable: Java or jNeuroML jar missing"], "", self.name)
        java, jar = self._require()
        cmd = [str(java), f"-Xmx{self.max_memory}", "-Djava.awt.headless=true", "-jar", str(jar), "-validate",
               *[str(Path(f).resolve()) for f in files]]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
        except subprocess.TimeoutExpired:
            return ValidationResult(None, -1, ["validation timed out"], "", self.name)
        except OSError as exc:
            return ValidationResult(None, -1, [f"tool failure: {exc}"], "", self.name)
        out = proc.stdout + proc.stderr
        summary = re.search(r"Validated (\d+) files?: (.*)", out)
        if summary is None:
            exc = re.search(r"^\s*(?:Exception in thread .*|[\w.$]+(?:Exception|Error)\b.*)$", out, re.MULTILINE)
            if exc and "java" in out.lower():
                # jNeuroML crashed while loading an existing file (e.g. a malformed include): a model defect.
                return ValidationResult(False, proc.returncode, [f"validator crashed while loading the model: "
                                                                 f"{exc.group(0).strip()[:300]}"], out, self.name)
            return ValidationResult(None, proc.returncode, ["unrecognised validator output"], out, self.name)
        # Warnings (e.g. "1 passed with warnings", exit 0) are not validity failures.
        valid = proc.returncode == 0 and re.search(r"\b[1-9]\d* failed", summary.group(2)) is None
        msgs = [ln.strip() for ln in out.splitlines()
                if re.search(r"not valid|failed|cvc-|Error|Exception|Warning", ln) and "No warnings" not in ln]
        return ValidationResult(valid, proc.returncode, msgs, out, f"{self.name} -validate")

    # ------------------------------------------------------------ simulation
    def run_lems(self, lems_file: Path, outputs: list[OutputSpec], timeout_s: float = 3600.0,
                 sample_every_ms: float | None = None) -> SimResult:
        lems_file = Path(lems_file).resolve()
        cwd = lems_file.parent
        if not self.available():
            return SimResult(RunStatus.TOOL_FAILURE, -1, 0.0, {}, [], "Java or jNeuroML jar missing")
        java, jar = self._require()
        text = lems_file.read_text(encoding="utf-8", errors="replace")
        for name in _OUTPUT_FILE_RE.findall(text):           # jLEMS does not create output folders
            target = cwd / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                target.unlink()
        cmd = [str(java), f"-Xmx{self.max_memory}", "-Djava.awt.headless=true", "-jar", str(jar), lems_file.name,
               "-nogui"]
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout_s)
        except subprocess.TimeoutExpired:
            return SimResult(RunStatus.TIMEOUT, -1, time.perf_counter() - t0, {}, cmd, f"timeout after {timeout_s}s")
        except OSError as exc:
            return SimResult(RunStatus.TOOL_FAILURE, -1, time.perf_counter() - t0, {}, cmd, str(exc))
        runtime = time.perf_counter() - t0
        out = proc.stdout + proc.stderr
        tail = "\n".join(out.strip().splitlines()[-25:])
        started = re.search(r"Finished \d+ steps", out) is not None or "simulation started" in out
        if proc.returncode != 0:
            # jLEMS reports errors raised while stepping with "simulation started (t = ...)" and, when
            # the failure may stem from the step size, an explicit hint (verified 2026-09-13: a x20 dt
            # mutant overflowed HH rate expressions mid-run). Such runs executed and then diverged:
            # spec class 3 (numerically unstable), not class 2 (non-executable).
            if started and _DT_HINT.search(out):
                status = RunStatus.UNSTABLE
            elif started:
                status = RunStatus.RUNTIME_ERROR
            else:
                status = RunStatus.BUILD_ERROR
            return SimResult(status, proc.returncode, runtime, {}, cmd, _first_error(out), tail, proc.stdout, proc.stderr)
        try:
            traces = {}
            for spec in outputs:
                traces.update(load_dat(cwd / spec.file, spec.columns, sample_every_ms))
        except (FileNotFoundError, ValueError, IndexError) as exc:
            return SimResult(RunStatus.RUNTIME_ERROR, proc.returncode, runtime, {}, cmd, f"output unreadable: {exc}", tail, proc.stdout, proc.stderr)
        for name, tr in traces.items():
            if not np.all(np.isfinite(tr.v_mV)) or np.max(np.abs(tr.v_mV)) > PHYSICAL_V_BOUND_MV:
                return SimResult(RunStatus.UNSTABLE, proc.returncode, runtime, traces, cmd,
                                 f"non-finite or out-of-bound voltage in {name}", tail, proc.stdout, proc.stderr)
        return SimResult(RunStatus.OK, proc.returncode, runtime, traces, cmd, "", tail, proc.stdout, proc.stderr)


def _first_error(out: str) -> str:
    for ln in out.splitlines():
        if re.search(r"ContentError|ParseError|Exception|Error:|not found", ln):
            return ln.strip()[:500]
    return "simulator exited with a non-zero status"


MAX_TIME_LABEL_JITTER = 0.25   # fraction of one step


def regularize_time(t_ms: np.ndarray, name: str = "") -> np.ndarray:
    """Replace jLEMS's printed time labels by the exact uniform grid they encode.

    jLEMS prints time with about 8 significant digits of an accumulated floating-point
    clock (verified 2026-09-13: at dt = 0.001 ms over 1000 ms, labels deviate by up to 3% of
    a step, e.g. 0.51097697 s). The integration itself uses a fixed step, so the ideal grid
    t0 + i*dt is the true sample time. Deviations above MAX_TIME_LABEL_JITTER of a step mean
    the output is not a fixed-step recording and are rejected.
    """
    n = t_ms.size
    if n < 2:
        return t_ms
    dt = (t_ms[-1] - t_ms[0]) / (n - 1)
    if not dt > 0:
        raise ValueError(f"{name}: non-increasing time column")
    ideal = t_ms[0] + np.arange(n) * dt
    dev = float(np.max(np.abs(t_ms - ideal)) / dt)
    if dev > MAX_TIME_LABEL_JITTER:
        raise ValueError(f"{name}: time column is not a fixed-step grid (max deviation {dev:.3f} steps)")
    return ideal


def load_dat(path: Path, columns: dict[str, int], sample_every_ms: float | None = None) -> dict[str, Trace]:
    """Read a jLEMS OutputFile (whitespace columns, SI units) into ms/mV traces."""
    if not path.is_file():
        raise FileNotFoundError(path)
    df = pd.read_csv(path, sep=r"\s+", header=None, engine="c", dtype=np.float64)
    arr = df.to_numpy()
    t_ms = regularize_time(arr[:, 0] * 1e3, path.name)
    stride = 1
    if sample_every_ms:
        native = float(np.median(np.diff(t_ms[: min(len(t_ms), 1000)])))
        stride = max(1, int(round(sample_every_ms / native)))
    out = {}
    for name, col in columns.items():
        if col >= arr.shape[1]:
            raise IndexError(f"column {col} not in {path.name} ({arr.shape[1]} columns)")
        out[name] = Trace(t_ms[::stride].copy(), arr[::stride, col] * 1e3)
    return out
