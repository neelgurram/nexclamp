"""Extract a self-contained human-audit kit for people without access to the repository.

For every fault in the audit sheets this writes, under
``results/tables/<campaign>/audit/kit/build/``:

- ``kit.json``: the fault's identity, the change in plain words, the exact before/after lines of
  the edited model file (a text diff against the unmodified model), the assigned class, and every
  recorded detection (feature and full-trace) at each step size;
- ``fig_<n>.png``: the original and edited model's voltage under the canonical test and under the
  protocol that detected the change (or the canonical test alone when nothing did).

The kit deliberately omits the automated re-check (``AUTOMATED_CHECK.md``) so the auditors judge
independently. ``scripts/build_audit_kit.js`` turns the build folder into the Word packet and the
Excel answer sheet.

    python scripts/build_audit_kit.py --campaign heldout-v1
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from nexclamp import config  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

MODEL_NAMES = {
    "hay2011_soma": "Hay et al. 2011 layer-5 pyramidal cell (soma only)",
    "bbp2015_soma": "Blue Brain Project 2015 cortical cell (soma only)",
    "traub2005_testseg2": "Traub et al. 2005 test cell 2 (sodium/potassium channels)",
    "traub2005_testseg_all": "Traub et al. 2005 test cell with almost all channels",
    "smith2013_singlecomp": "Smith et al. 2013 layer-2/3 pyramidal cell (one compartment)",
    "migliore2005_ca1_soma": "Migliore et al. 2005 hippocampal CA1 pyramidal cell (soma only)",
}
PROTOCOLS = {
    "P00_canonical": "the canonical test: the simulation shipped with the model",
    "P02_weak_step": "weak step: a small current step at half the firing threshold",
    "P03_rheobase": "rheobase search: finds the smallest current step that makes the cell fire",
    "P04_step_2x": "2x step: a current step at twice the firing threshold, 0.5 s",
    "P05_long_step": "long step: a current step at 1.5x the firing threshold, held for 2 s",
    "P06_ramp": "ramp: current rising steadily from 0 to 3x the firing threshold over 1 s",
    "P07_hyperpolarizing_step": "hyperpolarising step: a negative current step",
    "P08_rebound": "rebound: a negative step, then release",
    "P09_short_pulse": "short pulse: a 3 ms strong pulse",
}
OPERATORS = {
    "scale_conductance": "multiply one ion channel's maximal conductance (how many channels there are) by a factor",
    "shift_reversal": "shift one channel's reversal potential (the voltage its current pushes toward) by a few mV",
    "scale_capacitance": "multiply the membrane capacitance by a factor",
    "scale_gate_time_constant": "make one channel gate open and close faster or slower (scale its time constant)",
    "shift_gate_midpoint": "shift the voltage at which one channel gate is half open",
    "scale_gate_slope": "make one channel gate's voltage dependence steeper or shallower",
    "shift_forward_rate_midpoint": "shift the voltage dependence of one gate's opening rate",
    "wrong_channel": "point a channel density at a different channel type",
    "wrong_compatible_component": "swap a channel for another channel of the same ion",
    "omit_include": "delete one line that includes a channel definition file",
    "duplicate_conductance": "add a second copy of one channel (roughly doubles it)",
    "increase_dt": "make the simulation time step larger (a numerical stress test, not a model fault)",
    "solver_config": "change the numerical integration method (a numerical stress test)",
    "recording_resolution": "record the voltage less often (a numerical stress test)",
}
CLASSES = {
    "1_structurally_invalid": "the edited model file is no longer valid NeuroML",
    "2_non_executable": "the edited model would not run",
    "3_numerically_unstable": "the edited model ran but its numbers blew up",
    "4_equivalent_within_tested_domain": "no reproducible change in any summary feature (behaviour looks unchanged)",
    "5_non_equivalent": "behaviour changed, and the canonical test caught it",
    "6_silent_under_canonical": "behaviour changed, but the canonical test missed it (another protocol caught it)",
}


def read_csv(p: Path) -> list[dict]:
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def file_diff(ref: Path, var: Path, max_lines: int = 40) -> list[dict]:
    """Unified text diff of every changed file (context 2), trimmed for print."""
    out = []
    ref_files = {p.relative_to(ref).as_posix() for p in ref.rglob("*") if p.is_file()} - {"variant.json"}
    var_files = {p.relative_to(var).as_posix() for p in var.rglob("*") if p.is_file()} - {"variant.json"}
    for f in sorted(ref_files | var_files):
        a = (ref / f).read_text(encoding="utf-8", errors="replace").splitlines() if f in ref_files else []
        b = (var / f).read_text(encoding="utf-8", errors="replace").splitlines() if f in var_files else []
        if a == b:
            continue
        lines = [ln for ln in difflib.unified_diff(a, b, lineterm="", n=2)][2:]
        trimmed = [ln.strip()[:220] if not ln.startswith(("+", "-")) else ln[0] + " " + ln[1:].strip()[:220]
                   for ln in lines]
        out.append({"file": f, "lines": trimmed[:max_lines], "truncated": len(trimmed) > max_lines})
    return out


def trace(raw: Path, run_id: str | None, protocol: str):
    if not run_id:
        return None
    f = raw / run_id / "traces.npz"
    if not f.is_file():
        return None
    z = np.load(f)
    if f"{protocol}__v" not in z.files:
        return None
    v = z[f"{protocol}__v"]
    t = z[f"{protocol}__t"]
    t = np.arange(len(v)) * float(t[1]) + float(t[0]) if len(t) == 3 else t
    return t, v


def plot(n: int, vid: str, model: str, protocols: list[str], ref_runs: dict, var_runs: dict, raw: Path,
         out: Path) -> str | None:
    panels = [p for p in protocols if trace(raw, ref_runs.get(p), p) is not None]
    if not panels:
        return None
    fig = Figure(figsize=(7.2, 2.3 * len(panels)))
    axes = fig.subplots(len(panels), 1, squeeze=False)[:, 0]
    for ax, p in zip(axes, panels):
        r, v = trace(raw, ref_runs.get(p), p), trace(raw, var_runs.get(p), p)
        step = max(1, len(r[0]) // 6000)
        ax.plot(r[0][::step], r[1][::step], color="black", lw=0.8, label="original model")
        if v is not None:
            ax.plot(v[0][::step], v[1][::step], color="#D55E00", lw=0.8, ls="--", label="edited model")
        ax.set_title(PROTOCOLS.get(p, p), fontsize=8.5)
        ax.set_ylabel("voltage (mV)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(fontsize=7, loc="upper right")
    axes[-1].set_xlabel("time (ms)", fontsize=8)
    fig.suptitle(f"Fault {n}: {vid} on {model}", fontsize=9)
    fig.tight_layout()
    name = f"fig_{n:02d}.png"
    fig.savefig(out / name, dpi=150)
    return name


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    proc = config.results_dir() / "processed" / a.campaign
    raw = config.results_dir() / "raw" / a.campaign
    work = REPO_ROOT / "work" / "variants" / a.campaign
    audit = config.results_dir() / "tables" / a.campaign / "audit"
    out = audit / "kit" / "build"
    out.mkdir(parents=True, exist_ok=True)
    cls = {r["variant_id"]: r for r in read_csv(proc / "classification.csv")}

    membership: dict[str, list[str]] = {}
    order: list[str] = []
    for pack, label in (("canonical_survivors", "key fault (headline claim)"), ("random20", "random sample")):
        for r in read_csv(audit / pack / "AUDIT_SHEET.csv"):
            if r["variant_id"] not in membership:
                order.append(r["variant_id"])
            membership.setdefault(r["variant_id"], []).append(label)

    faults = []
    for n, vid in enumerate(order, 1):
        c = cls[vid]
        model = c["model_id"]
        vdir = proc / "variants" / vid
        det = read_csv(vdir / "detections.csv") if (vdir / "detections.csv").is_file() else []
        tdet = [d for d in read_csv(vdir / "detections_trace.csv") if d.get("metric")] \
            if (vdir / "detections_trace.csv").is_file() else []
        ref_runs = json.loads((proc / "references" / model / "fingerprint_L1.json").read_text(encoding="utf-8"))["run_ids"]
        var_runs = json.loads((vdir / "fingerprint_L1.json").read_text(encoding="utf-8"))["run_ids"] \
            if (vdir / "fingerprint_L1.json").is_file() else {}
        detecting = [p for p in (c["detecting_protocols"] or "").split(";") if p]
        trace_protos = sorted({d["protocol_id"] for d in tdet})
        shown = ["P00_canonical"] + [p for p in (detecting + trace_protos)
                                     if p not in ("P00_canonical", "P03_rheobase")][:1]
        fig = plot(n, vid, model, list(dict.fromkeys(shown)), ref_runs, var_runs, raw, out)
        params = json.loads(c["params"] or "{}")
        faults.append({
            "n": n, "variant_id": vid, "membership": membership[vid], "model_id": model,
            "model_name": MODEL_NAMES.get(model, model), "operator": c["operator"],
            "operator_meaning": OPERATORS.get(c["operator"], c["operator"]),
            "stratum": c["stratum"], "family": c["family"], "severity": c["severity"],
            "factor": params.get("factor"), "delta_mV": params.get("delta_mV"),
            "assigned_class": c["class"], "class_meaning": CLASSES.get(c["class"], ""),
            "run_status": c["status_h"], "detecting_protocols": detecting,
            "diff": file_diff(work / model / "reference", work / "mutants" / model / vid),
            "feature_detections": [{k: d[k] for k in ("level_factor", "protocol_id", "feature", "ref_value",
                                                      "var_value", "diff", "tau")} for d in det],
            "trace_detections": [{k: d[k] for k in ("level_factor", "protocol_id", "metric", "ref_value",
                                                    "var_value", "diff", "tau")} for d in tdet],
            "figure": fig, "figure_protocols": list(dict.fromkeys(shown)) if fig else [],
        })
    commit, dirty = git_state()
    meta = {"campaign": a.campaign, "generated_utc": utc_now(), "git_commit": commit, "git_dirty": dirty,
            "n_faults": len(faults), "protocols": PROTOCOLS, "classes": CLASSES}
    (out / "kit.json").write_text(json.dumps({"meta": meta, "faults": faults}, indent=1), encoding="utf-8")
    print(f"{len(faults)} faults, {sum(1 for f in faults if f['figure'])} figures -> {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
