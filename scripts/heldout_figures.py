"""Paper figures for the sealed held-out campaign, one per preregistered claim.

Reads only recorded outputs (``heldout_evaluation.json``, the detection matrix, the classification,
and ``results/tables/<campaign>/secondary_summary.json`` from ``heldout_secondary.py``). Every
figure uses the primary endpoint's definitions unless its title says otherwise:

- h1  per-model detection, canonical versus selected battery (primary definition, 82 faults)
- h2  paired difference: pooled estimate with its cluster interval, per-model differences, and
      the preregistered 0.10 material threshold
- h3  canonical features versus canonical full trace versus battery (validation-level view)
- h4  random count-matched and runtime-matched batteries against the selected one
- h5  attrition (reuses the Pilot 2 figure; the definitions are identical)

    python scripts/heldout_figures.py --campaign heldout-v1
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import itertools  # noqa: E402

import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from neuraxis import config  # noqa: E402
from neuraxis.analysis.figures import OKABE_ITO, _save, set_designation  # noqa: E402
from neuraxis.provenance import REPO_ROOT  # noqa: E402
from neuraxis.selection import greedy  # noqa: E402
from neuraxis.selection.matrix import DetectionMatrix  # noqa: E402
from pilot2_figures import f2_attrition, flag, read_csv, short  # noqa: E402

BLUE, ORANGE, GREEN, VERM, GREY = (OKABE_ITO["blue"], OKABE_ITO["orange"], OKABE_ITO["bluish_green"],
                                   OKABE_ITO["vermillion"], "#8A8A8A")
CANONICAL = "P00_canonical"


def _style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)


def per_model(m: DetectionMatrix, selected: list[str]) -> list[dict]:
    can, sel = m.covered([CANONICAL]), m.covered(selected)
    rows: dict[str, dict] = defaultdict(lambda: {"n": 0, "can": 0, "sel": 0})
    for i, mid in enumerate(m.mutant_ids):
        r = rows[m.model_of[mid]]
        r["n"] += 1
        r["can"] += int(can[i])
        r["sel"] += int(sel[i])
    return [{"model": k, **v} for k, v in sorted(rows.items())]


def h1_per_model(rows: list[dict], pe: dict, out: Path) -> list[Path]:
    fig = Figure(figsize=(8.2, 4.4))
    ax = fig.subplots()
    x = np.arange(len(rows))
    w = 0.38
    for off, key, colour, label in ((-w / 2, "can", BLUE, "canonical regression test"),
                                    (w / 2, "sel", GREEN, "selected 3-protocol battery")):
        vals = [r[key] / r["n"] for r in rows]
        ax.bar(x + off, vals, w, color=colour, edgecolor="black", linewidth=0.6, label=label)
        for xi, r, v in zip(x, rows, vals):
            ax.text(xi + off, v + 0.015, f"{r[key]}/{r['n']}", ha="center", fontsize=7.5)
    cb = pe["cluster_bootstrap"]
    ax.axhline(pe["rate_b"], color=BLUE, linestyle="--", linewidth=1,
               label=f"canonical pooled {pe['rate_b']:.3f} [{cb['rate_b_ci'][0]:.2f}, {cb['rate_b_ci'][1]:.2f}]")
    ax.axhline(pe["rate_a"], color=GREEN, linestyle="--", linewidth=1,
               label=f"battery pooled {pe['rate_a']:.3f} [{cb['rate_a_ci'][0]:.2f}, {cb['rate_a_ci'][1]:.2f}]")
    ax.axhline(0.95, color=GREY, linestyle=":", linewidth=1.2, label="preregistered adequacy threshold 0.95")
    ax.set_xticks(x, [short(r["model"]) for r in rows], fontsize=8)
    ax.set_ylim(0, 1.42)
    ax.set_ylabel("admissible faults detected (fraction)", fontsize=9)
    ax.set_title(f"Held-out models: the canonical test detects {pe['rate_b']:.0%} of behaviour-changing faults, "
                 f"the battery {pe['rate_a']:.0%}\n(n = {pe['counts']['n']} faults on 6 models never used in "
                 "development; detection reproducible at h and h/2)", fontsize=9.5)
    ax.legend(fontsize=7, loc="upper center", ncol=2, framealpha=0.95)
    _style(ax)
    fig.tight_layout()
    return _save(fig, out)


def h2_difference(rows: list[dict], pe: dict, out: Path) -> list[Path]:
    cb = pe["cluster_bootstrap"]
    fig = Figure(figsize=(8.2, 4.6))
    ax = fig.subplots()
    labels = [short(r["model"]).replace("\n", " ") for r in rows] + ["pooled (6 models)"]
    diffs = [(r["sel"] - r["can"]) / r["n"] for r in rows] + [pe["diff"]]
    y = np.arange(len(labels))[::-1]
    ax.scatter(diffs[:-1], y[:-1], color=GREY, edgecolor="black", zorder=3, s=36, label="per model")
    ax.errorbar([pe["diff"]], [y[-1]], xerr=[[pe["diff"] - cb["ci_low"]], [cb["ci_high"] - pe["diff"]]],
                fmt="D", color=GREEN, markeredgecolor="black", capsize=4, markersize=8, zorder=4,
                label=f"pooled {pe['diff']:+.3f}, 95% cluster CI [{cb['ci_low']:+.3f}, {cb['ci_high']:+.3f}]")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.axvline(0.10, color=VERM, linestyle="--", linewidth=1.1, label="preregistered material difference 0.10")
    ax.set_yticks(y, labels, fontsize=8)
    ax.set_xlabel("detection rate: battery minus canonical", fontsize=9)
    ax.set_title("Primary endpoint: the interval excludes 0; its lower end lies below the 0.10 material threshold\n"
                 f"exact McNemar p = {pe['exact_mcnemar_p']:.3f} (treats mutants as independent)\n"
                 f"cluster permutation p = {pe['cluster_permutation']['p_value']:.3f} (6 models; smallest attainable "
                 f"p = {pe['cluster_permutation']['min_attainable_p']:.3f})", fontsize=8.6)
    ax.legend(fontsize=7.2, loc="upper left", framealpha=0.95)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    return _save(fig, out)


def h3_levels(cls: list[dict], out: Path) -> list[Path]:
    sem = [r for r in cls if r["kind"] == "mutant" and r["stratum"] == "primary_semantic"
           and flag(r, "A_basic_pass") and flag(r, "E_full_battery")]
    by: dict[str, list] = defaultdict(list)
    for r in sem:
        by[r["model_id"]].append(r)
    models = sorted(by)
    x = np.arange(len(models))
    w = 0.26
    fig = Figure(figsize=(8.2, 4.4))
    ax = fig.subplots()
    series = (("B_canonical_feature", BLUE, "canonical test, summary features"),
              ("C_canonical_trace", ORANGE, "canonical test, full voltage trace"),
              ("D_multi_protocol", GREEN, "other protocols, features or trace"))
    for j, (lv, colour, label) in enumerate(series):
        vals = [sum(flag(r, lv) for r in by[mm]) for mm in models]
        ax.bar(x + (j - 1) * w, vals, w, color=colour, edgecolor="black", linewidth=0.6, label=label)
    for xi, mm in zip(x, models):
        ax.plot([xi - 1.5 * w, xi + 1.5 * w], [len(by[mm])] * 2, color="black", linestyle="--", linewidth=1)
    ax.set_xticks(x, [short(mm) for mm in models], fontsize=8)
    ax.set_ylim(0, max(len(v) for v in by.values()) * 1.35)
    ax.set_ylabel("faults detected", fontsize=9)
    n_neither = sum(not (flag(r, "B_canonical_feature") or flag(r, "C_canonical_trace")) for r in sem)
    ax.set_title(f"Validation levels, never merged (n = {len(sem)} faults with any detected change; dashed = "
                 f"available)\n{n_neither} faults escape the canonical test on features and full trace alike",
                 fontsize=9.3)
    ax.legend(fontsize=7.5, loc="upper left", ncol=3, framealpha=0.95)
    _style(ax)
    fig.tight_layout()
    return _save(fig, out)


def h4_random(m: DetectionMatrix, selected: list[str], seed: int, draws: int, out: Path) -> list[Path]:
    cands = [p for p in m.protocol_ids if p != CANONICAL]
    exact = np.array([m.rate(list(s)) for s in itertools.combinations(sorted(cands), len(selected))])
    budget = float(sum(m.cost[p] for p in selected))
    rt = greedy.random_runtime_matched(m, budget, draws, seed + 1, cands)
    sel, can = m.rate(selected), m.rate([CANONICAL])
    fig = Figure(figsize=(8.2, 3.8))
    axes = fig.subplots(1, 2, sharey=False)
    bins = np.linspace(0.3, 1.0, 29)
    for ax, data, title in ((axes[0], exact, f"all {exact.size} random 3-protocol batteries"),
                            (axes[1], rt, f"{rt.size:,} random batteries within the same cost")):
        ax.hist(data, bins=bins, color=GREY, edgecolor="white")
        ax.axvline(sel, color=GREEN, linewidth=2, label=f"selected battery {sel:.3f}")
        ax.axvline(can, color=BLUE, linewidth=2, linestyle="--", label=f"canonical {can:.3f}")
        p = (exact >= sel).mean() if data is exact else (1 + (data >= sel).sum()) / (1 + data.size)
        ax.set_title(f"{title}\nshare at least as good as selected: {p:.3f}", fontsize=8.5)
        ax.set_xlabel("held-out detection rate", fontsize=8.5)
        ax.legend(fontsize=7, loc="upper left")
        _style(ax)
    axes[0].set_ylabel("number of batteries", fontsize=8.5)
    fig.suptitle("Protocol selection on development models transfers: the chosen battery beats random ones",
                 fontsize=9.5)
    fig.tight_layout()
    return _save(fig, out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--selection", default="results/processed/pilot2/selection_k4.json")
    a = ap.parse_args(argv)
    cfg = config.study()
    proc = config.results_dir() / "processed" / a.campaign
    figs = config.results_dir() / "figures" / a.campaign
    meta = json.loads((proc / "STUDY_METADATA.json").read_text(encoding="utf-8"))
    set_designation(" | ".join(f"{k}: {v}" for k, v in meta.items()
                               if k in ("study_phase", "protocol_version", "designation")))
    pe = json.loads((proc / "heldout_evaluation.json").read_text(encoding="utf-8"))["primary_endpoint"]
    selected = json.loads((REPO_ROOT / a.selection).read_text(encoding="utf-8"))["selected_protocols"]
    m = DetectionMatrix.from_csv(proc / "detection_matrix.csv")
    cls = read_csv(proc / "classification.csv")
    rows = per_model(m, selected)
    assert sum(r["n"] for r in rows) == pe["counts"]["n"], "matrix and primary endpoint disagree"
    written = []
    written += h1_per_model(rows, pe, figs / "h1_per_model_primary")
    written += h2_difference(rows, pe, figs / "h2_primary_difference")
    written += h3_levels(cls, figs / "h3_validation_levels")
    written += h4_random(m, selected, int(cfg["selection"]["seed"]), int(cfg["selection"]["random_draws"]),
                         figs / "h4_random_baselines")
    written += f2_attrition(cls, figs / "h5_attrition")
    for p in written:
        print(f"  {p.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
