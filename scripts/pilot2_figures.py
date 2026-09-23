"""Paper figures for a finished campaign, built from recorded outputs only.

The central exhibit of this study is not the pooled detection rate: it is the **spread across
models**. A pooled 0.92 hides that the shipped regression test caught everything on two simple
point neurons and missed a third of the faults on the two most complex cells. Amendment S-01
requires per-model values beside any pooled figure, and these figures enforce that visually.

Figures written to ``results/figures/<campaign>/``:

- ``f1_per_model_detection`` - canonical detection rate per model, with the pooled value marked and
  the unexposed-subset value beside each bar (S-01 sections 11.1 and 11.3);
- ``f2_attrition`` - exact counts from generated variants down to admissible faults (S-01 11.4);
- ``f3_canonical_vs_battery`` - what canonical features, canonical trace and the battery each
  detected, per model, including the model where level C could not be calibrated;
- ``f4_unique_contribution`` - faults detected by exactly one protocol.

Every number is read from the campaign's own tables; nothing is recomputed or smoothed.

    python scripts/pilot2_figures.py --campaign pilot2
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

BLUE, ORANGE, GREEN, VERM, GREY = (OKABE_ITO["blue"], OKABE_ITO["orange"], OKABE_ITO["bluish_green"],
                                   OKABE_ITO["vermillion"], "#8A8A8A")


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def flag(r: dict, name: str) -> bool:
    return str(r.get(f"level_{name}", "")).strip().lower() in ("true", "1", "yes")


def short(model_id: str) -> str:
    """Readable axis labels; the full ids stay in the tables."""
    return {"acnet2_pyr_soma": "ACnet2\npyramidal", "migliore2014_mt_soma": "Migliore\nmitral",
            "nml2_hh_example": "Hodgkin–\nHuxley", "osb_hh2_477127614": "Allen\nHH2",
            "pospischil2008_fs": "Pospischil\nfast-spiking"}.get(model_id, model_id.replace("_", "\n"))


def per_model_rows(cls: list[dict], exposed: set[str]) -> list[dict]:
    out = []
    for mid in sorted({r["model_id"] for r in cls}):
        sem = [r for r in cls if r["model_id"] == mid and r["stratum"] == "primary_semantic"
               and r["kind"] == "mutant"]
        adm = [r for r in sem if flag(r, "A_basic_pass") and flag(r, "E_full_battery")]
        det = [r for r in adm if flag(r, "B_canonical_feature") or flag(r, "C_canonical_trace")]
        unexp = [r for r in adm if r["variant_id"] not in exposed]
        det_unexp = [r for r in unexp if flag(r, "B_canonical_feature") or flag(r, "C_canonical_trace")]
        out.append({"model_id": mid, "admissible": len(adm), "detected": len(det),
                    "rate": len(det) / len(adm) if adm else float("nan"),
                    "n_unexposed": len(unexp),
                    "rate_unexposed": len(det_unexp) / len(unexp) if unexp else float("nan"),
                    "b_only": sum(1 for r in adm if flag(r, "B_canonical_feature")),
                    "c_only": sum(1 for r in adm if flag(r, "C_canonical_trace")),
                    "battery": sum(1 for r in adm if flag(r, "D_multi_protocol"))})
    return out


def f1_per_model_detection(rows: list[dict], pooled: float, out: Path) -> list[Path]:
    fig = Figure(figsize=(7.2, 4.0))
    ax = fig.subplots()
    x = np.arange(len(rows))
    rates = [r["rate"] for r in rows]
    colours = [VERM if r < 0.8 else ORANGE if r < 0.95 else BLUE for r in rates]
    ax.bar(x, rates, width=0.58, color=colours, edgecolor="black", linewidth=0.5, zorder=3)
    ax.plot(x, [r["rate_unexposed"] for r in rows], linestyle="none", marker="_", markersize=22,
            markeredgewidth=1.8, color="black", zorder=5, label="excluding pre-exposed faults")
    ax.axhline(pooled, color=GREY, linestyle="--", linewidth=1.2, zorder=2,
               label=f"pooled across models = {pooled:.3f}")
    ax.axhline(0.95, color=GREEN, linestyle=":", linewidth=1.2, zorder=2, label="adequacy threshold = 0.95")
    # Counts sit with the rate above each bar: a legend box over the bars hid them before.
    for i, r in enumerate(rows):
        ax.text(i, r["rate"] + 0.02, f"{r['rate']:.3f}\n{r['detected']}/{r['admissible']}",
                ha="center", va="bottom", fontsize=8.2, linespacing=1.3)
    ax.set_xticks(x)
    ax.set_xticklabels([short(r["model_id"]) for r in rows], fontsize=8)
    ax.set_ylim(0, 1.24)
    ax.set_ylabel("faults detected by the shipped\nregression test (fraction)", fontsize=9)
    ax.set_title("A pooled rate hides the spread: the shipped test is complete on simple cells\n"
                 "and misses a third of the faults on the most complex one", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3,
              frameon=False, handlelength=1.8)
    ax.grid(axis="y", alpha=0.25, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return _save(fig, out)


def f2_attrition(cls: list[dict], out: Path) -> list[Path]:
    sem = [r for r in cls if r["stratum"] == "primary_semantic" and r["kind"] == "mutant"]
    ex = [r for r in sem if r["class"] not in ("1_structurally_invalid", "2_non_executable")]
    st = [r for r in ex if r["class"] != "3_numerically_unstable"]
    adm = [r for r in st if r["class"] in ("5_non_equivalent", "6_silent_under_canonical")]
    stages = [("generated", len(sem)), ("schema valid\nand executable", len(ex)),
              ("numerically\nstable", len(st)), ("admissible\n(behaviour changed)", len(adm))]
    fig = Figure(figsize=(6.4, 3.4))
    ax = fig.subplots()
    y = np.arange(len(stages))[::-1]
    ax.barh(y, [n for _, n in stages], color=[BLUE, BLUE, BLUE, GREEN], height=0.55,
            edgecolor="black", linewidth=0.5, zorder=3)
    for yi, (_, n) in zip(y, stages):
        ax.text(n + 0.8, yi, str(n), va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels([s for s, _ in stages], fontsize=8.5)
    ax.set_xlabel("primary semantic faults", fontsize=9)
    ax.set_xlim(0, max(n for _, n in stages) * 1.12)
    ax.set_title("Attrition: every stage reported with its exact count", fontsize=9.5)
    ax.grid(axis="x", alpha=0.25, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return _save(fig, out)


def f3_canonical_vs_battery(rows: list[dict], no_trace: set[str], out: Path) -> list[Path]:
    fig = Figure(figsize=(7.2, 4.0))
    ax = fig.subplots()
    x = np.arange(len(rows))
    w = 0.26
    ax.bar(x - w, [r["b_only"] for r in rows], w, label="canonical, features", color=BLUE,
           edgecolor="black", linewidth=0.5, zorder=3)
    ax.bar(x, [r["c_only"] for r in rows], w, label="canonical, full trace", color=ORANGE,
           edgecolor="black", linewidth=0.5, zorder=3)
    ax.bar(x + w, [r["battery"] for r in rows], w, label="perturbation battery", color=GREEN,
           edgecolor="black", linewidth=0.5, zorder=3)
    for i, r in enumerate(rows):
        ax.plot([i - w - 0.13, i + w + 0.13], [r["admissible"]] * 2, color="black", linewidth=1.1,
                linestyle="--", zorder=4)
        if r["model_id"] in no_trace:
            ax.text(i, 0.35, "level C not\ncalibrated", ha="center", va="bottom", fontsize=6.8,
                    color=VERM, fontweight="bold", zorder=6)
    ax.set_xticks(x)
    ax.set_xticklabels([short(r["model_id"]) for r in rows], fontsize=8)
    ax.set_ylabel("admissible faults detected", fontsize=9)
    ax.set_title("What each validation strategy caught (dashed line = admissible faults available)",
                 fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return _save(fig, out)


def f4_unique_contribution(unique: list[dict], out: Path) -> list[Path]:
    rows = [r for r in unique if r.get("protocol_id")]
    fig = Figure(figsize=(6.6, 3.6))
    ax = fig.subplots()
    names = [r["protocol_id"].replace("_", " ") for r in rows]
    vals = [int(r["n_detected_only_by_this_protocol"] or 0) for r in rows]
    y = np.arange(len(rows))[::-1]
    ax.barh(y, vals, color=[ORANGE if v else GREY for v in vals], height=0.6,
            edgecolor="black", linewidth=0.5, zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 0.03, yi, str(v), va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("faults this protocol alone detected", fontsize=9)
    ax.set_xlim(0, max(max(vals), 1) * 1.25)
    ax.set_title("No added protocol was ever the only detector: the extra battery\n"
                 "found nothing the others missed", fontsize=9.5)
    ax.grid(axis="x", alpha=0.25, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return _save(fig, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    processed = config.results_dir() / "processed" / a.campaign
    outputs = processed / "pilot_v2_outputs"
    cls = read_csv(processed / "classification.csv")
    if not cls:
        print(f"no classification.csv under {processed}")
        return 1
    meta = {}
    if (processed / "STUDY_METADATA.json").is_file():
        meta = json.loads((processed / "STUDY_METADATA.json").read_text(encoding="utf-8"))
    set_designation(" | ".join(f"{k}: {v}" for k, v in meta.items() if k in
                               ("study_phase", "protocol_version", "designation")))
    exposed = {r["variant_id"] for r in read_csv(REPO_ROOT / "manifests" / "PILOT2_EXPOSED_VARIANTS.csv")}
    rows = per_model_rows(cls, exposed)
    summary = json.loads((outputs / "summary.json").read_text(encoding="utf-8")) \
        if (outputs / "summary.json").is_file() else {}
    ev = summary.get("branch", {}).get("evidence", {})
    pooled = ev.get("canonical_B_or_C_detection_rate") or (
        sum(r["detected"] for r in rows) / max(1, sum(r["admissible"] for r in rows)))
    no_trace = set(ev.get("models_without_canonical_trace") or [])

    figs = config.results_dir() / "figures" / a.campaign
    written = []
    written += f1_per_model_detection(rows, float(pooled), figs / "f1_per_model_detection")
    written += f2_attrition(cls, figs / "f2_attrition")
    written += f3_canonical_vs_battery(rows, no_trace, figs / "f3_canonical_vs_battery")
    unique = read_csv(outputs / "14_unique_protocol_contribution.csv")
    if unique:
        written += f4_unique_contribution(unique, figs / "f4_unique_contribution")
    for p in written:
        print(f"  {p.relative_to(REPO_ROOT).as_posix()}")
    print(f"\n{len(written)} files; pooled canonical detection {float(pooled):.4f}; "
          f"models without level C: {sorted(no_trace) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
