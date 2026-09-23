"""Cross-simulator check: export every model to NEURON, and run it too when a runtime exists (N-08).

Two levels of evidence, reported separately and never merged:

**Level 1 - portability (always collectable).** ``jnml <LEMS> -neuron`` translates each model's
shipped simulation into NEURON sources. A model that exports cleanly is expressed in NeuroML
faithfully enough for a second, independently written simulator to consume it. A model that fails to
export is a finding about that model, recorded with the exact error.

**Level 2 - agreement (needs a NEURON runtime).** The exported model is compiled and run, and its
canonical trace is compared with the jLEMS trace: spike counts, first-spike latency, spike-time
differences and trace RMSE. These are **descriptive** numbers. No pass/fail threshold is applied,
because the study's tolerances are calibrated against one integrator's own discretisation error and
say nothing about the gap between two different integrators.

Outputs land in ``results/audits/cross_simulator/<stamp>/``: a JSON record, a CSV table and a short
Markdown summary. Nothing here touches a campaign, and no study result depends on it.

    python scripts/cross_simulator_check.py                       # all included models
    python scripts/cross_simulator_check.py --models nml2_hh_example
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402

from nexclamp.models import load_models, materialize  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, sha256_file, utc_now  # noqa: E402
from nexclamp.schemas import RunStatus  # noqa: E402
from nexclamp.simulators.jneuroml import JNeuroML  # noqa: E402
from nexclamp.simulators.neuron import NeuronSimulator, export_to_neuron  # noqa: E402
from nexclamp.protocols.generate import canonical_output  # noqa: E402
from nexclamp.validation.trace_regression import SPIKE_THRESHOLD_MV, spikes  # noqa: E402

COLUMNS = ["model_id", "source_family", "export_ok", "export_returncode", "mod_files", "hoc_files", "runner",
           "export_seconds", "export_error", "neuron_runtime", "neuron_status", "jlems_spikes", "neuron_spikes",
           "jlems_first_spike_ms", "neuron_first_spike_ms", "max_spike_time_diff_ms", "trace_rmse_mV",
           "agreement_note", "neuron_message"]


def compare_traces(a, b) -> dict:
    """Descriptive agreement between two traces of the same protocol. Never a pass or a fail."""
    if a is None or b is None:
        return {"jlems_spikes": "", "neuron_spikes": "", "jlems_first_spike_ms": "", "neuron_first_spike_ms": "",
                "max_spike_time_diff_ms": "", "trace_rmse_mV": "",
                "agreement_note": "one simulator produced no trace"}
    sa, sb = spikes(a), spikes(b)
    note = []
    diff = ""
    if sa.size and sb.size and sa.size == sb.size:
        diff = float(np.max(np.abs(sa - sb)))
    elif sa.size != sb.size:
        note.append(f"spike count differs ({sa.size} vs {sb.size})")
    # Compare on the shared time grid: the two simulators need not sample identically.
    n = min(a.v_mV.size, b.v_mV.size)
    rmse = float(np.sqrt(np.mean((np.asarray(a.v_mV[:n]) - np.asarray(b.v_mV[:n])) ** 2))) if n else ""
    if a.v_mV.size != b.v_mV.size:
        note.append(f"sample counts differ ({a.v_mV.size} vs {b.v_mV.size}); RMSE over the first {n}")
    return {"jlems_spikes": int(sa.size), "neuron_spikes": int(sb.size),
            "jlems_first_spike_ms": float(sa[0]) if sa.size else "",
            "neuron_first_spike_ms": float(sb[0]) if sb.size else "",
            "max_spike_time_diff_ms": diff, "trace_rmse_mV": rmse,
            "agreement_note": "; ".join(note) or "same spike count; see the numeric columns"}


def check_model(model, jl: JNeuroML, nrn: NeuronSimulator, out_dir: Path, run_neuron: bool) -> dict:
    row = {"model_id": model.model_id, "source_family": model.source_family, "neuron_runtime": str(nrn.available())}
    tmp = Path(tempfile.mkdtemp(prefix=f"xsim_{model.model_id}_"))
    try:
        ws = materialize(model, tmp / "ws")
        exported = export_to_neuron(ws.harness_path)
        row.update({"export_ok": "yes" if exported.ok else "no", "export_returncode": exported.returncode,
                    "mod_files": len(exported.mod_files), "hoc_files": len(exported.hoc_files),
                    "runner": exported.runner.name if exported.runner else "",
                    "export_seconds": round(exported.duration_s, 1),
                    "export_error": "" if exported.ok else exported.output[-400:].replace("\n", " ")})
        # Record what was generated, with hashes, so the artefacts are provable later.
        store = out_dir / "exports" / model.model_id
        store.mkdir(parents=True, exist_ok=True)
        manifest = []
        for f in exported.files:
            shutil.copy2(f, store / f.name)
            manifest.append({"file": f.name, "sha256": sha256_file(f), "bytes": f.stat().st_size})
        (store / "export_manifest.json").write_text(
            json.dumps({"model_id": model.model_id, "generated": manifest,
                        "jnml_output_tail": exported.output[-2000:]}, indent=2) + "\n", encoding="utf-8")

        if not (exported.ok and run_neuron and nrn.available()):
            row.update(compare_traces(None, None))
            row["neuron_status"] = "not executed (no NEURON runtime)" if exported.ok else "export failed"
            return row

        spec = canonical_output(model)
        jl_res = jl.run_lems(ws.harness_path, [spec])
        nrn_res = nrn.run_lems(ws.harness_path, [spec])
        row["neuron_status"] = nrn_res.status.value
        row["neuron_message"] = (nrn_res.message or "")[:400].replace("\n", " ")
        key = next(iter(spec.columns))
        a = jl_res.traces.get(key) if jl_res.status is RunStatus.OK else None
        b = nrn_res.traces.get(key) if nrn_res.status is RunStatus.OK else None
        row.update(compare_traces(a, b))
        return row
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--models", nargs="*", help="model ids (default: every model marked include)")
    ap.add_argument("--export-only", action="store_true", help="never attempt a NEURON run")
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    models = load_models()
    ids = a.models or [m for m, rec in models.items() if rec.inclusion == "include"]
    stamp = utc_now().replace("-", "").replace(":", "")[:15] + "Z"
    out_dir = Path(a.out) if a.out else REPO_ROOT / "results" / "audits" / "cross_simulator" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    jl, nrn = JNeuroML(), NeuronSimulator()
    commit, dirty = git_state()
    rows = [check_model(models[m], jl, nrn, out_dir, not a.export_only) for m in ids]

    with open(out_dir / "cross_simulator.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    record = {"created_utc": utc_now(), "commit": commit, "tree_dirty": dirty,
              "jneuroml": jl.version_info(), "neuron": nrn.version_info(),
              "spike_threshold_mV": SPIKE_THRESHOLD_MV, "models": rows,
              "level_1_exported": sum(1 for r in rows if r.get("export_ok") == "yes"),
              "level_2_executed": sum(1 for r in rows if r.get("neuron_status") == "ok"),
              "note": "Level 1 is portability evidence. Level 2 is descriptive agreement, never a detection rule: "
                      "the study's tolerances are calibrated within one integrator and do not apply across two."}
    (out_dir / "cross_simulator.json").write_text(json.dumps(record, indent=2, default=str) + "\n",
                                                  encoding="utf-8", newline="\n")

    lines = ["# Cross-simulator check", "",
             f"*{utc_now()}; commit `{commit}` (tree dirty: {dirty}). {jl.version_string()}; {nrn.version_string()}.*",
             "", f"- models checked: **{len(rows)}**",
             f"- exported to NEURON sources: **{record['level_1_exported']} of {len(rows)}**",
             f"- executed under NEURON: **{record['level_2_executed']} of {len(rows)}**", "",
             "| model | export | .mod | runner | NEURON run | jLEMS spikes | NEURON spikes | max spike-time diff (ms) | trace RMSE (mV) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['model_id']}` | {r.get('export_ok', '')} | {r.get('mod_files', '')} | "
                     f"{r.get('runner', '') or '-'} | {r.get('neuron_status', '')} | {r.get('jlems_spikes', '')} | "
                     f"{r.get('neuron_spikes', '')} | {r.get('max_spike_time_diff_ms', '')} | "
                     f"{r.get('trace_rmse_mV', '')} |")
    lines += ["", "Level 1 (export) is portability evidence: the model is expressed faithfully enough for a second, "
                  "independently written simulator to consume it. Level 2 (agreement) is descriptive only. No "
                  "cross-simulator threshold is defined, because this study's tolerances are calibrated against one "
                  "integrator's own discretisation error and say nothing about the gap between two integrators.", ""]
    (out_dir / "cross_simulator.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines[:8]))
    shown = out_dir.resolve()
    try:
        shown = shown.relative_to(REPO_ROOT)
    except ValueError:
        pass
    print(f"\nwrote {shown.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
