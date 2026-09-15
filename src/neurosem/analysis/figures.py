"""Paper figures (spec "Required figures" 1-8; ARCHITECTURE.md section 3.8).

Each ``figN_*`` function takes tidy pandas DataFrames whose required columns are listed in
its docstring and an output path, and writes ``<out>.png`` (300 dpi) and ``<out>.pdf``
(returned as ``[png, pdf]``; a ``.png``/``.pdf`` suffix on ``out_path`` is ignored). Drawing
uses matplotlib's object-oriented ``Figure`` API only, never pyplot, so no global figure
state is touched and the functions work headless.

Colours come from the Okabe-Ito palette (Okabe M, Ito K, 2008, "Color Universal Design"),
chosen because its hues stay distinguishable under the common colour-vision deficiencies;
line styles, markers and hatches add a second, non-colour cue. PDF output embeds TrueType
fonts and carries no creation date, so a re-run on the same data gives the same file.

Titles and labels describe what is plotted and never state a finding.
"""

from __future__ import annotations

import functools
import textwrap
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import matplotlib as mpl
import numpy as np
import pandas as pd
from cycler import cycler
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator

from neurosem.analysis.metrics import as_binary, as_label

_DESIGNATION = ""


def set_designation(text: str) -> None:
    """Footer printed on every figure saved afterwards (study phase, protocol version); empty = none."""
    global _DESIGNATION
    _DESIGNATION = text or ""

OKABE_ITO = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
}
GREY = "#999999"
PALETTE = [OKABE_ITO[k] for k in ("blue", "orange", "bluish_green", "vermillion", "reddish_purple", "sky_blue",
                                   "yellow", "black")]
_MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
_LINESTYLES = ["-", "--", ":", "-."]
_HATCHES = ["", "//", "..", "xx", "\\\\", "--", "++", "oo"]

FIGURE_TITLES = {
    "fig1": "Reference and variant membrane potential under the canonical and additional protocols",
    "fig2": "Validation cascade of generated mutants",
    "fig3": "Detection by protocol for each mutant, grouped by base model and mutation family",
    "fig4": "Detection rate versus protocol count and simulation cost",
    "fig5": "Detection rate by evaluation set and strategy",
    "fig6": "Detections on valid transformations and tolerance sensitivity",
    "fig7": "Case studies: reference and variant responses",
    "fig8": "AI-assisted transformation tasks: outcomes by validation layer (secondary case study)",
}

STAGE_LABELS = {
    "total": "All mutants",
    "schema_valid": "Structurally valid",
    "executable": "Executable",
    "numerically_stable": "Numerically stable",
    "canonical_survivors": "Pass canonical protocol",
    "perturbation_detected": "Detected by {battery}",
    "missed_by_battery": "Non-equivalent, not detected by {battery}",
    "unresolved_survivors": "No reproducible divergence in exhaustive battery (equivalent within tested domain)",
}

STRATEGY_STYLES: dict[str, dict[str, Any]] = {
    "canonical": {"color": OKABE_ITO["black"], "marker": "s", "linestyle": "-"},
    "selected": {"color": OKABE_ITO["blue"], "marker": "o", "linestyle": "-"},
    "random_count_matched": {"color": OKABE_ITO["sky_blue"], "marker": "^", "linestyle": "--"},
    "random_runtime_matched": {"color": OKABE_ITO["orange"], "marker": "v", "linestyle": ":"},
    "exhaustive": {"color": OKABE_ITO["vermillion"], "marker": "D", "linestyle": "-."},
}

OUTCOME_STYLES: dict[str, dict[str, Any]] = {
    "pass": {"color": OKABE_ITO["bluish_green"], "hatch": ""},
    "fail": {"color": OKABE_ITO["vermillion"], "hatch": "//"},
    "not_reached": {"color": GREY, "hatch": ".."},
}

ROLE_STYLES = {
    "reference": {"color": OKABE_ITO["black"], "linestyle": "-", "linewidth": 1.1, "label": "reference"},
    "variant": {"color": OKABE_ITO["vermillion"], "linestyle": "--", "linewidth": 1.0, "label": "variant"},
}

_RC = {
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.prop_cycle": cycler(color=PALETTE),
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}


# --------------------------------------------------------------------------- helpers


def _styled(fn: Callable[..., list[Path]]) -> Callable[..., list[Path]]:
    """Run a figure function inside the house rc settings without changing global rcParams."""

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> list[Path]:
        with mpl.rc_context(_RC):
            return fn(*args, **kwargs)

    return wrapper


def _require(df: Any, columns: Sequence[str], name: str) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"{name}: expected a pandas DataFrame (got {type(df).__name__})")
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"{name}: missing required column(s) {missing}; have {list(df.columns)}")
    if df.empty:
        raise ValueError(f"{name}: table is empty")
    return df


def _save(fig: Figure, out_path: Path | str) -> list[Path]:
    out = Path(out_path)
    if out.suffix.lower() in (".png", ".pdf"):
        out = out.with_suffix("")
    out.parent.mkdir(parents=True, exist_ok=True)
    png = out.parent / f"{out.name}.png"
    pdf = out.parent / f"{out.name}.pdf"
    if _DESIGNATION:
        fig.text(0.005, 0.002, textwrap.fill(_DESIGNATION, 180), fontsize=5, ha="left", va="bottom", color="#555555")
    fig.savefig(png, dpi=300)
    fig.savefig(pdf, metadata={"CreationDate": None})
    return [png, pdf]


def _suptitle(fig: Figure, key: str) -> None:
    """Figure-level title wrapped to the figure width (about 12 characters per inch at 9 pt)."""
    width_in = float(fig.get_size_inches()[0])
    fig.suptitle(textwrap.fill(FIGURE_TITLES[key], max(30, int(width_in * 12))), fontsize=9)


def _strategy_style(name: str, index: int) -> dict[str, Any]:
    if name in STRATEGY_STYLES:
        return dict(STRATEGY_STYLES[name])
    return {"color": PALETTE[index % len(PALETTE)], "marker": _MARKERS[index % len(_MARKERS)],
            "linestyle": _LINESTYLES[index % len(_LINESTYLES)]}


def _as_str(values: pd.Series) -> pd.Series:
    """Series of display labels; enum members are shown by value (see ``metrics.as_label``)."""
    return values.map(as_label)


def _unique_in_order(values: pd.Series) -> list[str]:
    return list(dict.fromkeys(_as_str(values).tolist()))


def _draw_trace_pair(ax: Any, df: pd.DataFrame, where: str) -> None:
    for role, style in ROLE_STYLES.items():
        sub = df[_as_str(df["role"]) == role]
        if sub.empty:
            raise ValueError(f"{where}: no '{role}' trace")
        sub = sub.sort_values("t_ms")
        ax.plot(sub["t_ms"].to_numpy(float), sub["v_mV"].to_numpy(float), **style)


def _role_handles() -> list[Line2D]:
    return [Line2D([], [], **style) for style in ROLE_STYLES.values()]


def _optional(df: pd.DataFrame, col: str) -> np.ndarray | None:
    return df[col].to_numpy(float) if col in df.columns else None


# --------------------------------------------------------------------------- figure 1


@_styled
def fig1_concept(traces: pd.DataFrame, out_path: Path | str, canonical_protocol: str = "P00_canonical") -> list[Path]:
    """Figure 1: reference versus variant under the canonical protocol and other protocols.

    ``traces`` columns: ``protocol_id``, ``role`` (``reference`` | ``variant``), ``t_ms``,
    ``v_mV``; one row per sample. The canonical protocol is drawn first, followed by every
    other protocol in order of appearance; each panel needs both roles.
    """
    df = _require(traces, ["protocol_id", "role", "t_ms", "v_mV"], "fig1_concept")
    protocols = _unique_in_order(df["protocol_id"])
    if canonical_protocol not in protocols:
        raise ValueError(f"fig1_concept: canonical protocol {canonical_protocol!r} not in traces")
    panels = [canonical_protocol] + [p for p in protocols if p != canonical_protocol]
    if len(panels) < 2:
        raise ValueError("fig1_concept: needs the canonical protocol and at least one other protocol")
    fig = Figure(figsize=(3.6 * len(panels), 3.0), layout="constrained")
    axes = fig.subplots(1, len(panels), sharey=True, squeeze=False)[0]
    for ax, pid in zip(axes, panels):
        _draw_trace_pair(ax, df[_as_str(df["protocol_id"]) == pid], f"fig1_concept[{pid}]")
        ax.set_title(f"{pid} (canonical)" if pid == canonical_protocol else pid)
        ax.set_xlabel("Time (ms)")
    axes[0].set_ylabel("Membrane potential (mV)")
    fig.legend(handles=_role_handles(), loc="outside lower center", ncols=2, frameon=False)
    _suptitle(fig, "fig1")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 2


@_styled
def fig2_validation_cascade(
    cascade: pd.DataFrame, out_path: Path | str, battery: str = "perturbation battery"
) -> list[Path]:
    """Figure 2: validation cascade.

    ``cascade`` columns: ``stage``, ``count``; optional ``fraction_of_total``. Produced by
    :func:`neurosem.analysis.metrics.validation_cascade`. Rows are drawn top to bottom in
    table order; the ``perturbation_detected``, ``missed_by_battery`` and
    ``unresolved_survivors`` stages (which partition the canonical survivors) are drawn with
    distinct colours and hatches. ``battery`` names the illustrated battery in the labels
    (e.g. ``"selected battery"``). Only ``unresolved_survivors`` (class EQUIVALENT) is
    labelled "equivalent within tested domain"; mutants a smaller battery missed are
    non-equivalent and are labelled as such.
    """
    df = _require(cascade, ["stage", "count"], "fig2_validation_cascade").reset_index(drop=True)
    df["stage"] = _as_str(df["stage"])
    counts = df["count"].to_numpy(float)
    if np.any(counts < 0) or not np.all(np.isfinite(counts)):
        raise ValueError("fig2_validation_cascade: counts must be finite and non-negative")
    total = counts[0]
    frac = _optional(df, "fraction_of_total")
    if frac is None:
        frac = counts / total if total > 0 else np.full(counts.size, np.nan)
    special = {
        "perturbation_detected": (OKABE_ITO["bluish_green"], "//"),
        "missed_by_battery": (OKABE_ITO["vermillion"], "xx"),
        "unresolved_survivors": (OKABE_ITO["orange"], ".."),
    }
    labels = [textwrap.fill(STAGE_LABELS.get(s, s).replace("{battery}", battery), 48) for s in df["stage"]]
    fig = Figure(figsize=(7.0, 0.5 * len(df) + 1.2), layout="constrained")
    ax = fig.add_subplot()
    y = np.arange(len(df))
    for i, stage in enumerate(df["stage"]):
        colour, hatch = special.get(stage, (OKABE_ITO["blue"], ""))
        ax.barh(y[i], counts[i], color=colour, hatch=hatch, edgecolor="black", linewidth=0.5)
        pct = "" if not np.isfinite(frac[i]) else f" ({100 * frac[i]:.0f}%)"
        ax.text(counts[i], y[i], f" {int(counts[i])}{pct}", va="center", ha="left")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(total, counts.max(), 1) * 1.25)
    ax.set_xlabel("Mutants")
    _suptitle(fig, "fig2")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 3


@_styled
def fig3_detection_heatmap(
    detections: pd.DataFrame, out_path: Path | str, protocol_order: Sequence[str] | None = None
) -> list[Path]:
    """Figure 3: mutant-by-protocol detection heat map grouped by base model and family.

    ``detections`` columns: ``mutant_id``, ``model_id``, ``family``, ``protocol_id``,
    ``detected`` (bool); one row per evaluated (mutant, protocol). Rows are sorted by
    model, family, mutant; pairs absent from the table are drawn grey ("not evaluated").
    ``protocol_order`` fixes the column order (default: sorted protocol ids) and must cover
    every protocol in the table.
    """
    df = _require(detections, ["mutant_id", "model_id", "family", "protocol_id", "detected"],
                  "fig3_detection_heatmap").copy()
    for c in ("mutant_id", "model_id", "family", "protocol_id"):
        df[c] = _as_str(df[c])
    if df.duplicated(["mutant_id", "protocol_id"]).any():
        raise ValueError("fig3_detection_heatmap: duplicate (mutant_id, protocol_id) rows")
    det = as_binary(df["detected"].to_numpy(), "detected")
    meta = df[["mutant_id", "model_id", "family"]].drop_duplicates()
    if meta["mutant_id"].duplicated().any():
        raise ValueError("fig3_detection_heatmap: a mutant is assigned to more than one model or family")
    meta = meta.sort_values(["model_id", "family", "mutant_id"]).reset_index(drop=True)
    protocols = ([as_label(p) for p in protocol_order] if protocol_order is not None
                 else sorted(df["protocol_id"].unique()))
    extra = sorted(set(df["protocol_id"]) - set(protocols))
    if extra:
        raise ValueError(f"fig3_detection_heatmap: protocols missing from protocol_order: {extra}")
    row = {m: i for i, m in enumerate(meta["mutant_id"])}
    col = {p: j for j, p in enumerate(protocols)}
    mat = np.full((len(meta), len(protocols)), np.nan)
    for m, p, d in zip(df["mutant_id"], df["protocol_id"], det):
        mat[row[m], col[p]] = float(d)

    height = min(24.0, max(3.5, 0.12 * len(meta) + 2.5))
    width = max(5.5, 0.4 * len(protocols) + 4.0)
    fig = Figure(figsize=(width, height), layout="constrained")
    ax = fig.add_subplot()
    cmap = ListedColormap(["#FFFFFF", OKABE_ITO["blue"]]).with_extremes(bad=GREY)
    ax.imshow(np.ma.masked_invalid(mat), cmap=cmap, vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    groups = list(zip(meta["model_id"], meta["family"]))
    ticks, labels = [], []
    start = 0
    for i in range(1, len(groups) + 1):
        if i == len(groups) or groups[i] != groups[start]:
            ticks.append((start + i - 1) / 2)
            labels.append(f"{groups[start][0]} | {groups[start][1]} (n={i - start})")
            if i < len(groups):
                new_model = groups[i][0] != groups[start][0]
                ax.axhline(i - 0.5, color="black" if new_model else GREY, linewidth=1.4 if new_model else 0.6)
            start = i
    ax.set_yticks(ticks, labels)
    ax.set_xticks(np.arange(len(protocols)), protocols, rotation=90)
    ax.set_xlabel("Protocol")
    ax.set_ylabel("Mutants (base model | mutation family)")
    for spine in ax.spines.values():
        spine.set_visible(True)
    fig.legend(
        handles=[Patch(facecolor=OKABE_ITO["blue"], edgecolor="black", label="detected"),
                 Patch(facecolor="#FFFFFF", edgecolor="black", label="not detected"),
                 Patch(facecolor=GREY, edgecolor="black", label="not evaluated")],
        loc="outside lower center", ncols=3, frameon=False,
    )
    _suptitle(fig, "fig3")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 4


@_styled
def fig4_efficiency_curve(
    curves: pd.DataFrame, out_path: Path | str, cost_label: str = "Simulation cost (cell-steps)"
) -> list[Path]:
    """Figure 4: detection rate versus protocol count (panel A) and cost (panel B).

    ``curves`` columns: ``strategy`` (e.g. ``canonical``, ``selected``,
    ``random_count_matched``, ``random_runtime_matched``, ``exhaustive``), ``n_protocols``,
    ``cost``, ``detection_rate``; optional ``lower``/``upper`` drawn as a band (for random
    batteries: the spread of draws from ``metrics.summarize_draws``). Rows with ``nan`` in a
    panel's x column are omitted from that panel only.
    """
    df = _require(curves, ["strategy", "n_protocols", "cost", "detection_rate"], "fig4_efficiency_curve")
    strategies = _unique_in_order(df["strategy"])
    fig = Figure(figsize=(8.0, 3.4), layout="constrained")
    axes = fig.subplots(1, 2, sharey=True)
    handles: dict[str, Line2D] = {}
    for ax, xcol, xlabel, tag in ((axes[0], "n_protocols", "Number of protocols", "A"),
                                  (axes[1], "cost", cost_label, "B")):
        drawn = False
        for i, s in enumerate(strategies):
            style = _strategy_style(s, i)
            sub = df[_as_str(df["strategy"]) == s]
            sub = sub[np.isfinite(sub[xcol].to_numpy(float)) & np.isfinite(sub["detection_rate"].to_numpy(float))]
            if sub.empty:
                continue
            sub = sub.sort_values(xcol)
            x = sub[xcol].to_numpy(float)
            y = sub["detection_rate"].to_numpy(float)
            lo, hi = _optional(sub, "lower"), _optional(sub, "upper")
            (line,) = ax.plot(x, y, label=s, markersize=4, **style)
            handles.setdefault(s, line)
            if lo is not None and hi is not None:
                ok = np.isfinite(lo) & np.isfinite(hi)
                if ok.sum() > 1:
                    ax.fill_between(x[ok], lo[ok], hi[ok], color=style["color"], alpha=0.18, linewidth=0)
                elif ok.sum() == 1:
                    ax.errorbar(x[ok], y[ok], yerr=[y[ok] - lo[ok], hi[ok] - y[ok]], color=style["color"],
                                linestyle="none", capsize=2)
            drawn = True
        if not drawn:
            ax.text(0.5, 0.5, f"no finite {xcol} values", transform=ax.transAxes, ha="center", va="center")
        ax.set_xlabel(xlabel)
        ax.set_title(f"{tag}  by {'protocol count' if xcol == 'n_protocols' else 'cost'}", loc="left")
        ax.set_ylim(-0.02, 1.02)
    axes[0].set_ylabel("Detection rate")
    fig.legend(handles=list(handles.values()), loc="outside lower center", ncols=min(5, max(1, len(handles))),
               frameon=False)
    _suptitle(fig, "fig4")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 5


@_styled
def fig5_heldout_generalization(table: pd.DataFrame, out_path: Path | str) -> list[Path]:
    """Figure 5: detection rate on discovery models, held-out models and the held-out family.

    ``table`` columns: ``evaluation_set`` (e.g. ``discovery models``, ``held-out models``,
    ``held-out family``), ``strategy``, ``detection_rate``; optional ``ci_low``/``ci_high``
    (error bars) and ``n_mutants`` (shown under the set label when identical across
    strategies). One row per (evaluation_set, strategy); order of appearance is kept.
    """
    df = _require(table, ["evaluation_set", "strategy", "detection_rate"], "fig5_heldout_generalization").copy()
    df["evaluation_set"] = _as_str(df["evaluation_set"])
    df["strategy"] = _as_str(df["strategy"])
    if df.duplicated(["evaluation_set", "strategy"]).any():
        raise ValueError("fig5_heldout_generalization: duplicate (evaluation_set, strategy) rows")
    sets = _unique_in_order(df["evaluation_set"])
    strategies = _unique_in_order(df["strategy"])
    width = 0.8 / len(strategies)
    fig = Figure(figsize=(max(5.0, 1.6 * len(sets) + 2.0), 3.4), layout="constrained")
    ax = fig.add_subplot()
    for j, s in enumerate(strategies):
        style = _strategy_style(s, j)
        sub = df[df["strategy"] == s].set_index("evaluation_set").reindex(sets)
        x = np.arange(len(sets)) + (j - (len(strategies) - 1) / 2) * width
        y = sub["detection_rate"].to_numpy(float)
        ok = np.isfinite(y)
        yerr = None
        if "ci_low" in sub.columns and "ci_high" in sub.columns:
            lo, hi = sub["ci_low"].to_numpy(float), sub["ci_high"].to_numpy(float)
            yerr = np.vstack([np.clip(y - lo, 0, None), np.clip(hi - y, 0, None)])[:, ok]
            yerr = np.where(np.isfinite(yerr), yerr, 0.0)
        ax.bar(x[ok], y[ok], width=width * 0.95, color=style["color"], hatch=_HATCHES[j % len(_HATCHES)],
               edgecolor="black", linewidth=0.5, label=s, yerr=yerr, capsize=2,
               error_kw={"elinewidth": 0.8, "ecolor": "black"})
    labels = []
    for es in sets:
        label = es
        if "n_mutants" in df.columns:
            ns = df.loc[df["evaluation_set"] == es, "n_mutants"].dropna().unique()
            if len(ns) == 1:
                label = f"{es}\n(n={int(ns[0])})"
        labels.append(label)
    ax.set_xticks(np.arange(len(sets)), labels)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Detection rate")
    ax.legend(frameon=False, ncols=min(4, len(strategies)), loc="upper center", bbox_to_anchor=(0.5, -0.18))
    _suptitle(fig, "fig5")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 6


@_styled
def fig6_false_positives(fp_by_category: pd.DataFrame, sensitivity: pd.DataFrame, out_path: Path | str) -> list[Path]:
    """Figure 6: detections on valid transformations (A) and tolerance sensitivity (B).

    ``fp_by_category`` columns: ``category``, ``n``, ``n_detected``, ``rate``; optional
    ``ci_low``/``ci_high`` (e.g. from ``metrics.by_family`` with ``family`` renamed).
    ``sensitivity`` columns: ``tolerance_multiplier``, ``series`` (e.g.
    ``false_positive_rate``, ``detection_rate:selected``), ``rate``; optional
    ``ci_low``/``ci_high`` drawn as bands. The dotted vertical line marks multiplier 1
    (the calibrated tolerances).
    """
    fp = _require(fp_by_category, ["category", "n", "n_detected", "rate"], "fig6_false_positives[fp_by_category]")
    sens = _require(sensitivity, ["tolerance_multiplier", "series", "rate"], "fig6_false_positives[sensitivity]")
    fig = Figure(figsize=(8.5, max(3.2, 0.3 * len(fp) + 1.6)), layout="constrained")
    ax_a, ax_b = fig.subplots(1, 2, width_ratios=[1, 1.2])

    y = np.arange(len(fp))
    rate = fp["rate"].to_numpy(float)
    xerr = None
    if "ci_low" in fp.columns and "ci_high" in fp.columns:
        lo, hi = fp["ci_low"].to_numpy(float), fp["ci_high"].to_numpy(float)
        xerr = np.vstack([np.clip(rate - lo, 0, None), np.clip(hi - rate, 0, None)])
        xerr = np.where(np.isfinite(xerr), xerr, 0.0)
    ax_a.errorbar(rate, y, xerr=xerr, fmt="o", color=OKABE_ITO["vermillion"], ecolor="black", elinewidth=0.8,
                  capsize=2, markersize=4)
    ax_a.set_yticks(y, [f"{c} ({int(k)}/{int(n)})" for c, k, n in
                        zip(_as_str(fp["category"]), fp["n_detected"], fp["n"])])
    ax_a.invert_yaxis()
    ax_a.set_xlim(-0.02, 1.02)
    ax_a.set_xlabel("Fraction of valid transformations detected")
    ax_a.set_title("A  valid transformations", loc="left")

    series = _unique_in_order(sens["series"])
    mult_all = sens["tolerance_multiplier"].to_numpy(float)
    for i, s in enumerate(series):
        style = _strategy_style(s, i + 1)
        sub = sens[_as_str(sens["series"]) == s].sort_values("tolerance_multiplier")
        x = sub["tolerance_multiplier"].to_numpy(float)
        r = sub["rate"].to_numpy(float)
        ax_b.plot(x, r, label=s, markersize=4, **style)
        if "ci_low" in sub.columns and "ci_high" in sub.columns:
            lo, hi = sub["ci_low"].to_numpy(float), sub["ci_high"].to_numpy(float)
            ok = np.isfinite(lo) & np.isfinite(hi)
            if ok.sum() > 1:
                ax_b.fill_between(x[ok], lo[ok], hi[ok], color=style["color"], alpha=0.18, linewidth=0)
    ax_b.axvline(1.0, color=GREY, linestyle=":", linewidth=1.0, label="calibrated tolerance (x1)")
    finite = mult_all[np.isfinite(mult_all)]
    if finite.size and np.all(finite > 0) and finite.max() / finite.min() >= 4:
        ax_b.set_xscale("log", base=2)
    ticks = np.unique(finite)
    ax_b.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax_b.set_ylim(-0.02, 1.02)
    ax_b.set_xlabel("Tolerance multiplier")
    ax_b.set_ylabel("Rate")
    ax_b.set_title("B  tolerance sensitivity", loc="left")
    ax_b.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncols=2)
    _suptitle(fig, "fig6")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 7


@_styled
def fig7_case_studies(traces: pd.DataFrame, out_path: Path | str, cases: Sequence[str] | None = None) -> list[Path]:
    """Figure 7: interpretable case studies (the spec asks for two or three).

    ``traces`` columns: ``case_id``, ``protocol_id``, ``role`` (``reference`` | ``variant``),
    ``t_ms``, ``v_mV``; optional ``case_label`` (a descriptive label such as the mutation
    operator and parameters). One row per case (order of ``cases`` or appearance) with one
    panel per protocol of that case.
    """
    df = _require(traces, ["case_id", "protocol_id", "role", "t_ms", "v_mV"], "fig7_case_studies").copy()
    df["case_id"] = _as_str(df["case_id"])
    df["protocol_id"] = _as_str(df["protocol_id"])
    order = [as_label(c) for c in cases] if cases is not None else _unique_in_order(df["case_id"])
    missing = [c for c in order if c not in set(df["case_id"])]
    if missing:
        raise ValueError(f"fig7_case_studies: cases not in traces: {missing}")
    per_case = {c: _unique_in_order(df.loc[df["case_id"] == c, "protocol_id"]) for c in order}
    ncols = max(len(v) for v in per_case.values())
    fig = Figure(figsize=(3.4 * ncols, 2.4 * len(order) + 0.8), layout="constrained")
    axes = fig.subplots(len(order), ncols, squeeze=False)
    for i, c in enumerate(order):
        sub_case = df[df["case_id"] == c]
        label = c
        if "case_label" in sub_case.columns:
            labels = _as_str(sub_case["case_label"].dropna()).unique()
            if len(labels):
                label = f"{c}: {labels[0]}"
        for j in range(ncols):
            ax = axes[i, j]
            if j >= len(per_case[c]):
                ax.set_axis_off()
                continue
            pid = per_case[c][j]
            _draw_trace_pair(ax, sub_case[sub_case["protocol_id"] == pid], f"fig7_case_studies[{c}, {pid}]")
            ax.set_title(pid if j else f"{label}\n{pid}", loc="left")
            ax.set_xlabel("Time (ms)")
            if j == 0:
                ax.set_ylabel("V (mV)")
    fig.legend(handles=_role_handles(), loc="outside lower center", ncols=2, frameon=False)
    _suptitle(fig, "fig7")
    return _save(fig, out_path)


# --------------------------------------------------------------------------- figure 8


@_styled
def fig8_agent_case_study(
    outcomes: pd.DataFrame,
    out_path: Path | str,
    layer_order: Sequence[str] | None = None,
    outcome_order: Sequence[str] | None = None,
) -> list[Path]:
    """Figure 8: AI-assisted transformation task outcomes by validation layer (secondary).

    ``outcomes`` columns: ``task_id``, ``layer`` (e.g. ``basic_checks``, ``jnml_validate``,
    ``canonical``, ``neurosem_battery``), ``outcome`` (``pass`` | ``fail`` |
    ``not_reached`` or other labels); one row per (task, layer). Drawn as stacked task
    counts per layer, first layer at the top.
    """
    df = _require(outcomes, ["task_id", "layer", "outcome"], "fig8_agent_case_study").copy()
    for c in ("task_id", "layer", "outcome"):
        df[c] = _as_str(df[c])
    if df.duplicated(["task_id", "layer"]).any():
        raise ValueError("fig8_agent_case_study: duplicate (task_id, layer) rows")
    layers = [as_label(x) for x in layer_order] if layer_order is not None else _unique_in_order(df["layer"])
    extra = sorted(set(df["layer"]) - set(layers))
    if extra:
        raise ValueError(f"fig8_agent_case_study: layers missing from layer_order: {extra}")
    present = _unique_in_order(df["outcome"])
    if outcome_order is not None:
        kinds = [as_label(k) for k in outcome_order]
        if set(present) - set(kinds):
            raise ValueError(f"fig8_agent_case_study: outcomes missing from outcome_order: {sorted(set(present) - set(kinds))}")
    else:
        kinds = [k for k in OUTCOME_STYLES if k in present] + [k for k in present if k not in OUTCOME_STYLES]
    table = df.groupby(["layer", "outcome"]).size().unstack(fill_value=0).reindex(index=layers, columns=kinds,
                                                                                  fill_value=0)
    fig = Figure(figsize=(6.5, 0.5 * len(layers) + 1.6), layout="constrained")
    ax = fig.add_subplot()
    y = np.arange(len(layers))
    left = np.zeros(len(layers))
    extra_i = 0
    for k in kinds:
        if k in OUTCOME_STYLES:
            style = OUTCOME_STYLES[k]
        else:
            style = {"color": PALETTE[(extra_i + 5) % len(PALETTE)], "hatch": _HATCHES[(extra_i + 3) % len(_HATCHES)]}
            extra_i += 1
        vals = table[k].to_numpy(float)
        ax.barh(y, vals, left=left, color=style["color"], hatch=style["hatch"], edgecolor="black", linewidth=0.5,
                label=k)
        for yi, (l0, v) in enumerate(zip(left, vals)):
            if v > 0:
                ax.text(l0 + v / 2, yi, f"{int(v)}", ha="center", va="center",
                        bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none", "alpha": 0.8})
        left += vals
    ax.set_yticks(y, layers)
    ax.invert_yaxis()
    ax.set_xlabel("Tasks")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(frameon=False, ncols=min(4, len(kinds)), loc="upper center", bbox_to_anchor=(0.5, -0.25))
    _suptitle(fig, "fig8")
    return _save(fig, out_path)
