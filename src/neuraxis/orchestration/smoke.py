"""Infrastructure smoke test (execution plan, "Infrastructure smoke test").

Demonstrates, on two small fixture models, that the pipeline can:
1. load the models; 2. validate them; 3. run current-clamp simulations; 4. save complete voltage
traces; 5. extract spike count, first-spike latency and mean firing frequency; 6. draw stimulus
and voltage diagnostic plots; 7. repeat the run and reproduce the outputs within numerical
tolerance; 8. write complete provenance records; 9. run the automated unit and integration tests.

Everything is written under ``--out`` (never into study results). Any failed step fails the
smoke test, which blocks scaled data collection.
"""

from __future__ import annotations

import dataclasses as dc
import json
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

from neuraxis import config
from neuraxis.models import load_models, materialize
from neuraxis.protocols.definitions import templates_from_config
from neuraxis.provenance import REPO_ROOT, git_state, utc_now
from neuraxis.schemas import RUN_RECORD_REQUIRED_FIELDS, RunStatus, VariantKind, VariantRecord

FIXTURES = ("pospischil2008_rs", "nml2_hh_example")
SMOKE_FEATURES = ("spike_count", "first_spike_latency", "mean_frequency")
REPRO_TOLERANCE_MV = 1e-6


def _plot(model_id: str, protocol: Any, trace: Any, path: Path, designation: str) -> None:
    from matplotlib.figure import Figure

    fig = Figure(figsize=(7.5, 4.2))
    ax_i, ax_v = fig.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [1, 3]})
    t = np.asarray(trace.t_ms)
    i = np.zeros_like(t)
    for c in protocol.components:
        on = (t >= c.delay_ms) & (t < c.delay_ms + c.duration_ms)
        if c.kind == "ramp":
            i[on] += c.start_nA + (c.finish_nA - c.start_nA) * (t[on] - c.delay_ms) / c.duration_ms
        else:
            i[on] += c.amplitude_nA
    ax_i.plot(t, i, color="#0072B2", lw=0.8)
    ax_i.set_ylabel("I (nA)", fontsize=7)
    ax_v.plot(t, trace.v_mV, color="#000000", lw=0.6)
    ax_v.axvspan(protocol.window.start_ms, protocol.window.end_ms, color="#E69F00", alpha=0.12, lw=0)
    ax_v.set_ylabel("V (mV)", fontsize=7)
    ax_v.set_xlabel("t (ms)", fontsize=7)
    for ax in (ax_i, ax_v):
        ax.tick_params(labelsize=6)
    fig.suptitle(f"Smoke test: {model_id}, {protocol.protocol_id} (shaded: analysis window)", fontsize=8)
    fig.text(0.005, 0.002, designation, fontsize=5, color="#555555")
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)


def run_smoke(out_dir: Path, fixtures: Sequence[str] = FIXTURES, protocol_ids: Sequence[str] = ("P04_step_2x",),
              run_tests: bool = True, pytest_args: Sequence[str] = ("-q", "-p", "no:cacheprovider")) -> dict[str, Any]:
    from neuraxis.simulators.jneuroml import JNeuroML
    from neuraxis.validation import structural
    from neuraxis.validation.execution import RunRecorder

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = config.study()
    designation = config.designation_text(cfg) or "Neuraxis infrastructure smoke test"
    sim = JNeuroML(max_memory=cfg["numerics"]["java_max_memory"])
    steps: dict[str, dict[str, Any]] = {}
    report: dict[str, Any] = {"created_utc": utc_now(), "git": dict(zip(("commit", "dirty"), git_state())),
                              "python": sys.version.split()[0], "executable": sys.executable,
                              "simulator": sim.version_info() if sim.available() else None, "fixtures": list(fixtures),
                              "steps": steps}

    def step(name: str, ok: bool, **detail: Any) -> None:
        steps.setdefault(name, {"ok": True, "detail": {}})
        steps[name]["ok"] = steps[name]["ok"] and bool(ok)
        steps[name]["detail"].update(detail)

    models = load_models()
    templates = {t.protocol_id: t for t in templates_from_config(cfg["protocols"])}
    with tempfile.TemporaryDirectory(prefix="neuraxis_smoke_") as tmp:
        rec = RunRecorder("smoke", sim, results_root=out_dir, work_root=Path(tmp))
        for mid in fixtures:
            model = models.get(mid)
            step("1_load_models", model is not None, **{mid: "loaded" if model else "missing from manifest"})
            if model is None:
                continue
            ws = materialize(model, Path(tmp) / "ws" / mid)
            st = structural.check(ws, sim)
            step("2_validate", bool(st.valid), **{mid: {"valid": st.valid, "files": st.files}})
            variant = VariantRecord(variant_id=f"{mid}__reference", model_id=mid, kind=VariantKind.REFERENCE,
                                    tree_sha256=ws.tree_sha256(), parent_tree_sha256=ws.tree_sha256(),
                                    description="smoke-test reference", created_utc=utc_now())
            rh = rec.run_rheobase(ws, variant, config.nominal_exec(cfg), dict(cfg["rheobase"]),
                                  float(cfg["numerics"]["settle_ms"]))
            amp = rh.result.rheobase_nA if rh.result.status == "ok" else float(cfg["rheobase"]["fallback_rheobase_nA"])
            protocols = [templates[p].instantiate(amp, float(cfg["numerics"]["settle_ms"])) for p in protocol_ids]
            run0 = rec.run_battery(ws, variant, protocols, config.nominal_exec(cfg), replicate=0, need_traces=True)
            step("3_current_clamp", run0.status is RunStatus.OK, **{mid: {"status": run0.status.value,
                                                                          "rheobase_nA": amp}})
            saved = [r for r in run0.records if r.trace_path and (REPO_ROOT / r.trace_path).is_file()
                     or (out_dir / "raw" / "smoke" / r.run_id / "traces.npz").is_file()]
            full = all(len(run0.traces[p.protocol_id].t_ms) >= int(p.total_ms / config.nominal_exec(cfg).dt_ms)
                       for p in protocols if p.protocol_id in run0.traces)
            step("4_traces_saved", len(saved) == len(run0.records) and full,
                 **{mid: {"trace_files": [r.run_id for r in saved], "complete_length": full}})
            feats = {p.protocol_id: {f: (dc.asdict(run0.tables[p.protocol_id][f])
                                         if f in run0.tables.get(p.protocol_id, {}) else None) for f in SMOKE_FEATURES}
                     for p in protocols}
            step("5_features", all(v is not None for t in feats.values() for v in t.values()), **{mid: feats})
            for p in protocols:
                path = out_dir / "plots" / f"{mid}_{p.protocol_id}.png"
                if p.protocol_id in run0.traces:
                    _plot(mid, p, run0.traces[p.protocol_id], path, designation)
                step("6_diagnostic_plots", path.is_file(), **{f"{mid}:{p.protocol_id}": str(path)})
            run1 = rec.run_battery(ws, variant, protocols, config.nominal_exec(cfg), replicate=1, need_traces=True)
            diffs = {k: float(np.max(np.abs(np.asarray(run0.traces[k].v_mV) - np.asarray(run1.traces[k].v_mV))))
                     for k in run0.traces if k in run1.traces}
            step("7_reproducible", run1.status is RunStatus.OK and len(diffs) == len(run0.traces)
                 and all(d <= REPRO_TOLERANCE_MV for d in diffs.values()),
                 **{mid: {"max_abs_diff_mV": diffs, "tolerance_mV": REPRO_TOLERANCE_MV,
                          "distinct_run_ids": [r.run_id for r in run0.records + run1.records]}})
            for r in run0.records + run1.records:
                data = json.loads((out_dir / "raw" / "smoke" / r.run_id / "run.json").read_text(encoding="utf-8"))
                missing = [f for f in RUN_RECORD_REQUIRED_FIELDS if data.get(f) in (None, "")]
                step("8_provenance", not missing, **{r.run_id: {"missing_fields": missing}})
    if run_tests:
        proc = subprocess.run([sys.executable, "-m", "pytest", *pytest_args, "tests/unit", "tests/integration"],
                              cwd=REPO_ROOT, capture_output=True, text=True)
        (out_dir / "pytest.log").write_text(proc.stdout + proc.stderr, encoding="utf-8")
        tail = [ln for ln in proc.stdout.splitlines() if "passed" in ln or "failed" in ln][-1:]
        step("9_tests", proc.returncode == 0, exit_code=proc.returncode, summary=tail)
    else:
        step("9_tests", False, skipped="run_tests=False")
    report["passed"] = all(s["ok"] for s in steps.values()) and len(steps) == 9
    (out_dir / "smoke_report.json").write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    lines = [f"# Infrastructure smoke test: {'PASSED' if report['passed'] else 'FAILED'}", "",
             f"*{designation}*", "", f"- created: {report['created_utc']}; commit {report['git']['commit']} "
             f"(dirty: {report['git']['dirty']}); Python {report['python']} at `{report['executable']}`", "",
             "| step | result |", "|---|---|"]
    lines += [f"| {k} | {'pass' if v['ok'] else 'FAIL'} |" for k, v in sorted(steps.items())]
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report
