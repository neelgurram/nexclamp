"""Public checks for this task: validate the model files and run the shipped simulation.

Usage (from the task directory):  python public_tests/run_public_checks.py

What it does, as configured in public_tests/public_checks.json:
  1. runs `jnml -validate` (the jNeuroML jar bundled with pyNeuroML) on the listed files;
  2. runs the shipped LEMS simulation in a temporary copy of model/ (inside scratch/),
     reads the membrane-potential column of its output file and detects spikes as upward
     crossings of a threshold (linearly interpolated);
  3. if a reference is configured, compares spike count and spike times with the reference
     recorded from the model before it was edited.

Exit status: 0 = all checks passed, 1 = a check failed, 2 = Java/jNeuroML not available.
Java is found through NEUROSEM_JAVA, JAVA_HOME or PATH; the jar through NEUROSEM_JNML_JAR
or the installed pyNeuroML package.

This script is self-contained on purpose (standard library only, plus pyNeuroML to locate
the jar) so that it can run in an isolated task directory.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK_ROOT = HERE.parent
OUTPUT_FILE_RE = re.compile(r'<OutputFile\b[^>]*\bfileName\s*=\s*"([^"]+)"')


def find_java() -> str | None:
    exe = "java.exe" if os.name == "nt" else "java"
    candidates = []
    if os.environ.get("NEUROSEM_JAVA"):
        candidates.append(Path(os.environ["NEUROSEM_JAVA"]))
    if os.environ.get("JAVA_HOME"):
        candidates.append(Path(os.environ["JAVA_HOME"]) / "bin" / exe)
    which = shutil.which("java")
    if which:
        candidates.append(Path(which))
    for c in candidates:
        if c.is_file():
            return str(c)
    return None


def find_jar() -> str | None:
    if os.environ.get("NEUROSEM_JNML_JAR"):
        p = Path(os.environ["NEUROSEM_JNML_JAR"])
        return str(p) if p.is_file() else None
    try:
        from pyneuroml.utils.misc import get_path_to_jnml_jar
    except ImportError:
        return None
    p = Path(get_path_to_jnml_jar()).resolve()
    return str(p) if p.is_file() else None


def spike_times(t_ms: list[float], v_mV: list[float], threshold_mV: float) -> list[float]:
    """Upward threshold crossings, linearly interpolated between samples."""
    out = []
    for i in range(len(v_mV) - 1):
        if v_mV[i] < threshold_mV <= v_mV[i + 1]:
            out.append(t_ms[i] + (threshold_mV - v_mV[i]) * (t_ms[i + 1] - t_ms[i]) / (v_mV[i + 1] - v_mV[i]))
    return out


def read_output(path: Path, column: int) -> tuple[list[float], list[float]]:
    """Read a jLEMS output file (whitespace columns in SI units) as ms / mV."""
    t_ms, v_mV = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            t_ms.append(float(parts[0]) * 1e3)
            v_mV.append(float(parts[column]) * 1e3)
    return t_ms, v_mV


def run(cmd: list[str], cwd: Path, timeout_s: float) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return -1, f"timed out after {timeout_s} s"
    return proc.returncode, proc.stdout + proc.stderr


def check_validation(java: str, jar: str, files: list[str]) -> bool:
    paths = [TASK_ROOT / f for f in files]
    missing = [f for f, p in zip(files, paths) if not p.is_file()]
    if missing:
        print(f"[FAIL] validate: missing files {missing}")
        return False
    code, out = run([java, "-Xmx2G", "-Djava.awt.headless=true", "-jar", jar, "-validate",
                     *[str(p) for p in paths]], TASK_ROOT, 600)
    summary = re.search(r"Validated (\d+) files?: (.*)", out)
    ok = code == 0 and summary is not None and "All valid" in summary.group(2)
    print(f"[{'PASS' if ok else 'FAIL'}] validate {len(files)} file(s): "
          f"{summary.group(0) if summary else 'no validator summary'}")
    if not ok:
        for line in out.splitlines():
            if re.search(r"not valid|failed|cvc-|Error|Exception", line):
                print("        " + line.strip()[:300])
    return ok


def check_simulation(java: str, jar: str, spec: dict) -> bool:
    lems_rel = Path(spec["lems"])
    if lems_rel.parts[0] != "model":
        print("[FAIL] simulation: lems path must lie under model/")
        return False
    run_root = TASK_ROOT / "scratch" / ".public_run"
    if run_root.exists():
        shutil.rmtree(run_root)
    shutil.copytree(TASK_ROOT / "model", run_root / "model")
    lems = run_root / lems_rel
    if not lems.is_file():
        print(f"[FAIL] simulation: {spec['lems']} does not exist")
        return False
    for name in OUTPUT_FILE_RE.findall(lems.read_text(encoding="utf-8", errors="replace")):
        (lems.parent / name).parent.mkdir(parents=True, exist_ok=True)   # jLEMS does not create folders
    code, out = run([java, "-Xmx2G", "-Djava.awt.headless=true", "-jar", jar, lems.name, "-nogui"],
                    lems.parent, float(spec.get("timeout_s", 3600)))
    if code != 0:
        print(f"[FAIL] simulation {spec['lems']}: jNeuroML exited with status {code}")
        for line in out.strip().splitlines()[-15:]:
            print("        " + line[:300])
        return False
    dat = lems.parent / spec["output_file"]
    if not dat.is_file():
        print(f"[FAIL] simulation: output file {spec['output_file']} was not written")
        return False
    t_ms, v_mV = read_output(dat, int(spec["v_column"]))
    spikes = spike_times(t_ms, v_mV, float(spec["spike_threshold_mV"]))
    print(f"[PASS] simulation {spec['lems']} ran: {len(t_ms)} samples to {t_ms[-1]:.3f} ms, "
          f"{len(spikes)} spike(s) at {[round(s, 3) for s in spikes]} ms")
    if not spec.get("reference"):
        return True
    ref = json.loads((HERE / spec["reference"]).read_text(encoding="utf-8"))
    expected = ref["spike_times_ms"]
    tol = float(spec["spike_time_abs_tol_ms"])
    if len(spikes) != len(expected):
        print(f"[FAIL] canonical reference: {len(spikes)} spike(s), reference has {len(expected)}")
        return False
    worst = max((abs(a - b) for a, b in zip(spikes, expected)), default=0.0)
    ok = worst <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] canonical reference: largest spike-time difference "
          f"{worst:.3f} ms (tolerance {tol} ms)")
    return ok


def main() -> int:
    spec = json.loads((HERE / "public_checks.json").read_text(encoding="utf-8"))
    java, jar = find_java(), find_jar()
    if not (java and jar):
        print("[ERROR] Java or the jNeuroML jar was not found (set NEUROSEM_JAVA / NEUROSEM_JNML_JAR)")
        return 2
    ok = check_validation(java, jar, spec["validate"])
    ok = check_simulation(java, jar, spec["simulation"]) and ok
    print("ALL PUBLIC CHECKS PASSED" if ok else "SOME PUBLIC CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
