"""Figure for a fault the feature panel called equivalent and full-trace comparison caught.

This is the study's clearest single case. Every summary feature - spike count, latency, ISIs,
adaptation, AP amplitude, AHP - stays inside its calibrated tolerance on every protocol, so the
frozen classification records the fault as ``4_equivalent_within_tested_domain``: no change. Yet
comparing the recorded voltage traces detects it reproducibly at h, h/2 and h/4.

The figure shows the reference and the mutant on the same axes, the difference beneath, and the
measured feature values that stayed inside tolerance. It reads only recorded runs.

    python scripts/trace_only_figure.py --campaign pilot2 --variant m-shift_reversal-7be708c601
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from nexclamp import config  # noqa: E402
from nexclamp.analysis.figures import OKABE_ITO, _save, set_designation  # noqa: E402
from nexclamp.provenance import REPO_ROOT  # noqa: E402

REF_COLOUR, VAR_COLOUR, DIFF_COLOUR = "#000000", OKABE_ITO["vermillion"], OKABE_ITO["blue"]


def load_trace(raw: Path, run_id: str, protocol: str):
    """Voltage trace of one protocol from a recorded run (time axis stored as start, step, count)."""
    f = raw / run_id / "traces.npz"
    if not f.is_file():
        return None
    z = np.load(f)
    tk, vk = f"{protocol}__t", f"{protocol}__v"
    if vk not in z.files:
        return None
    v = z[vk]
    d = z[tk]
    t = np.arange(len(v)) * float(d[1]) + float(d[0]) if len(d) == 3 else d
    return t, v


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--protocol", default="P05_long_step")
    a = ap.parse_args(argv)

    processed = config.results_dir() / "processed" / a.campaign
    raw = config.results_dir() / "raw" / a.campaign
    vdir = processed / "variants" / a.variant
    if not vdir.is_dir():
        print(f"no variant directory {vdir}")
        return 1
    row = next((r for r in read_csv(processed / "classification.csv") if r["variant_id"] == a.variant), None)
    if row is None:
        print(f"{a.variant} not in classification.csv")
        return 1
    model = row["model_id"]
    var_runs = json.loads((vdir / "fingerprint_L1.json").read_text(encoding="utf-8")).get("run_ids", {})
    ref_runs = json.loads((processed / "references" / model / "fingerprint_L1.json")
                          .read_text(encoding="utf-8")).get("run_ids", {})
    ref = load_trace(raw, ref_runs.get(a.protocol, ""), a.protocol)
    var = load_trace(raw, var_runs.get(a.protocol, ""), a.protocol)
    if ref is None or var is None:
        print(f"missing trace for {a.protocol}")
        return 1
    # Both runs use the same protocol and step, so the reference time axis serves both.
    (tr, vr), (_, vv) = ref, var
    n = min(len(vr), len(vv))
    tr, vr, vv = tr[:n], vr[:n], vv[:n]
    diff = vv - vr
    rmse = float(np.sqrt(np.mean(diff ** 2)))

    trace_dets = [r for r in read_csv(vdir / "detections_trace.csv") if r.get("metric")]
    protos = sorted({r["protocol_id"] for r in trace_dets})
    levels = sorted({r["level_factor"] for r in trace_dets})

    set_designation("Exploratory development data; never pooled with the confirmatory held-out estimate")
    fig = Figure(figsize=(7.4, 5.2))
    top, bot = fig.subplots(2, 1, height_ratios=[2.4, 1], sharex=True)
    step = max(1, n // 4000)
    top.plot(tr[::step], vr[::step], color=REF_COLOUR, linewidth=0.8, label="reference (unedited model)")
    top.plot(tr[::step], vv[::step], color=VAR_COLOUR, linewidth=0.8, linestyle="--",
             label="after the edit")
    top.set_ylabel("membrane potential (mV)", fontsize=9)
    top.legend(fontsize=8, loc="upper right", framealpha=0.95)
    top.set_title(f"Every summary feature called this unchanged; the trace did not\n"
                  f"{model} - {row.get('operator', '')} - frozen class: {row['class']}", fontsize=9.5)
    top.grid(alpha=0.2)
    top.spines[["top", "right"]].set_visible(False)

    bot.plot(tr[::step], diff[::step], color=DIFF_COLOUR, linewidth=0.7)
    bot.axhline(0, color="#999999", linewidth=0.8)
    bot.set_ylabel("difference (mV)", fontsize=9)
    bot.set_xlabel("time (ms)", fontsize=9)
    bot.grid(alpha=0.2)
    bot.spines[["top", "right"]].set_visible(False)
    bot.text(0.995, 0.06, f"trace RMSE {rmse:.2f} mV   ·   detected on {len(protos)} protocols "
                          f"at refinement levels {', '.join('h' if x == '1' else f'h/{x}' for x in levels)}",
             transform=bot.transAxes, ha="right", fontsize=7.6, color="#333333")
    fig.tight_layout()
    out = config.results_dir() / "figures" / a.campaign / f"f5_trace_only_{a.variant}"
    written = _save(fig, out)
    for p in written:
        print(f"  {p.relative_to(REPO_ROOT).as_posix()}")
    print(f"\n{a.protocol}: RMSE {rmse:.3f} mV, peak |difference| {np.max(np.abs(diff)):.2f} mV; "
          f"{len(trace_dets)} trace detections across {protos}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
