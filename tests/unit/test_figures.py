"""Render every required figure from synthetic tidy tables and check the outputs."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from neurosem.analysis import figures as F
from neurosem.analysis import metrics as M
from neurosem.schemas import MutantClass as MC

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _check_outputs(paths, expected_stem):
    assert [p.suffix for p in paths] == [".png", ".pdf"]
    png, pdf = paths
    assert png.with_suffix("") == expected_stem and pdf.with_suffix("") == expected_stem
    assert png.stat().st_size > 1000 and pdf.stat().st_size > 1000
    assert png.read_bytes()[:8] == PNG_MAGIC
    assert pdf.read_bytes()[:5] == b"%PDF-"


def _trace_rows(protocol_id, role, shift_ms=0.0, amp=1.0, **extra):
    t = np.arange(0.0, 300.0, 0.5)
    spikes = np.arange(50.0, 250.0, 25.0) + shift_ms
    v = -65.0 + amp * sum(95.0 * np.exp(-((t - s) / 1.5) ** 2) for s in spikes)
    return pd.DataFrame({"protocol_id": protocol_id, "role": role, "t_ms": t, "v_mV": v, **extra})


# --------------------------------------------------------------------------- synthetic tables


def _concept_traces():
    return pd.concat([
        _trace_rows("P00_canonical", "reference"),
        _trace_rows("P00_canonical", "variant", shift_ms=0.3),
        _trace_rows("P08_rebound", "reference"),
        _trace_rows("P08_rebound", "variant", shift_ms=9.0, amp=0.6),
    ], ignore_index=True)


def _detections():
    rng = np.random.default_rng(0)
    rows = []
    for model in ("pospischil2008_rs", "pospischil2008_lts", "nml2_hh_example"):
        for family in ("biophysical", "reference"):
            for i in range(4):
                for p in (f"P{j:02d}" for j in range(6)):
                    rows.append({"mutant_id": f"{model}-{family}-{i}", "model_id": model, "family": family,
                                 "protocol_id": p, "detected": bool(rng.random() < 0.35)})
    return pd.DataFrame(rows).iloc[1:]           # one (mutant, protocol) pair not evaluated


def _curves():
    det = np.random.default_rng(1).random((40, 6)) < 0.3
    pids = [f"P{j:02d}" for j in range(6)]
    cost = {p: float(1e6 * (j + 1)) for j, p in enumerate(pids)}
    sel = M.coverage_curve(det, pids, ["P03", "P01", "P05", "P00"], cost)
    rows = [{"strategy": "selected", "n_protocols": r.n_protocols, "cost": r.cumulative_cost,
             "detection_rate": r.detection_rate} for r in sel.itertuples()]
    rng = np.random.default_rng(2)
    for k in range(1, 5):
        rows.append(M.summarize_draws(rng.uniform(0.1, 0.6, 500), "random_count_matched", n_protocols=k))
        rows.append(M.summarize_draws(rng.uniform(0.1, 0.6, 500), "random_runtime_matched",
                                      n_protocols=float("nan"), cost=k * 3e6))
    rows.append({"strategy": "canonical", "n_protocols": 1, "cost": 1e6, "detection_rate": 0.2})
    rows.append({"strategy": "exhaustive", "n_protocols": 6, "cost": 2.1e7,
                 "detection_rate": M.detection_rate(det.any(axis=1))})
    return pd.DataFrame(rows)


def _heldout_table():
    rows = []
    for es, n in (("discovery models", 90), ("held-out models", 40), ("held-out family", 25)):
        for strategy, k in (("canonical", n // 4), ("selected", n // 2), ("random_count_matched", n // 3),
                            ("exhaustive", (3 * n) // 4)):
            lo, hi = M.proportion_ci(k, n)
            rows.append({"evaluation_set": es, "strategy": strategy, "detection_rate": k / n,
                         "ci_low": lo, "ci_high": hi, "n_mutants": n})
    return pd.DataFrame(rows)


def _fp_tables():
    cats = ["unit_conversion"] * 10 + ["rename_identifier"] * 8 + ["xml_formatting"] * 6
    det = np.zeros(len(cats), dtype=bool)
    det[3] = True
    fp = M.by_family({"neurosem": det}, cats, include_all=True).rename(columns={"family": "category"})
    sens = []
    for m in (0.5, 1.0, 2.0, 4.0):
        for series, base in (("false_positive_rate", 0.2 / m), ("detection_rate:selected", 0.9 / m ** 0.3)):
            r = min(1.0, base)
            sens.append({"tolerance_multiplier": m, "series": series, "rate": r,
                         "ci_low": max(0.0, r - 0.1), "ci_high": min(1.0, r + 0.1)})
    return fp, pd.DataFrame(sens)


def _case_traces():
    parts = []
    for case, label, protocols in (("case1", "scale_conductance IM x0.5", ("P00_canonical", "P05_long_step")),
                                   ("case2", "shift_reversal Kd +5 mV", ("P00_canonical", "P07_hyperpolarizing_step",
                                                                       "P08_rebound"))):
        for j, p in enumerate(protocols):
            parts.append(_trace_rows(p, "reference", case_id=case, case_label=label))
            parts.append(_trace_rows(p, "variant", shift_ms=4.0 * j, case_id=case, case_label=label))
    return pd.concat(parts, ignore_index=True)


def _agent_outcomes():
    rng = np.random.default_rng(4)
    layers = ["basic_checks", "jnml_validate", "canonical", "neurosem_battery"]
    rows = []
    for t in range(20):
        failed = False
        for layer in layers:
            if failed:
                outcome = "not_reached"
            else:
                outcome = "fail" if rng.random() < 0.2 else "pass"
                failed = outcome == "fail"
            rows.append({"task_id": f"T{t:02d}", "layer": layer, "outcome": outcome})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- rendering


def test_fig1_concept(tmp_path):
    paths = F.fig1_concept(_concept_traces(), tmp_path / "fig1_concept.png")
    _check_outputs(paths, tmp_path / "fig1_concept")


def test_fig2_validation_cascade(tmp_path):
    classes = ([MC.STRUCTURALLY_INVALID] * 5 + [MC.NON_EXECUTABLE] * 3 + [MC.NUMERICALLY_UNSTABLE]
               + [MC.EQUIVALENT] * 6 + [MC.NON_EQUIVALENT] * 12 + [MC.SILENT] * 9)
    paths = F.fig2_validation_cascade(M.validation_cascade(classes), tmp_path / "sub" / "fig2")
    _check_outputs(paths, tmp_path / "sub" / "fig2")


def _capture_figure(monkeypatch):
    """Keep the Figure passed to ``_save`` so a test can inspect what was drawn."""
    captured = {}
    save = F._save

    def spy(fig, out_path):
        captured["fig"] = fig
        return save(fig, out_path)

    monkeypatch.setattr(F, "_save", spy)
    return captured


def test_fig2_battery_cascade_does_not_call_missed_mutants_equivalent(tmp_path, monkeypatch):
    classes = [MC.EQUIVALENT] * 2 + [MC.NON_EQUIVALENT] * 3 + [MC.SILENT] * 6
    det = np.zeros(len(classes), dtype=bool)
    det[5:7] = True                                   # the selected battery detects 2 of the 6 SILENT mutants
    captured = _capture_figure(monkeypatch)
    paths = F.fig2_validation_cascade(M.validation_cascade(classes, det), tmp_path / "fig2_sel",
                                      battery="selected battery")
    _check_outputs(paths, tmp_path / "fig2_sel")
    ax = captured["fig"].axes[0]
    labels = [t.get_text().replace("\n", " ") for t in ax.get_yticklabels()]
    widths = [p.get_width() for p in ax.patches]
    drawn = dict(zip(labels, widths))
    equivalent_labels = [lab for lab in labels if "equivalent within tested domain" in lab]
    assert len(equivalent_labels) == 1 and drawn[equivalent_labels[0]] == 2      # EQUIVALENT only
    assert drawn["Non-equivalent, not detected by selected battery"] == 4
    assert drawn["Detected by selected battery"] == 2


def test_fig3_detection_heatmap(tmp_path):
    paths = F.fig3_detection_heatmap(_detections(), tmp_path / "fig3")
    _check_outputs(paths, tmp_path / "fig3")


def test_fig3_accepts_enum_families_and_object_detected_column(tmp_path, monkeypatch):
    from neurosem.schemas import MutationFamily as MF

    det = _detections()
    det["family"] = det["family"].map(MF)
    det["detected"] = det["detected"].astype(int).astype(object)      # e.g. after a CSV round-trip
    captured = _capture_figure(monkeypatch)
    _check_outputs(F.fig3_detection_heatmap(det, tmp_path / "fig3_enum"), tmp_path / "fig3_enum")
    labels = [t.get_text() for t in captured["fig"].axes[0].get_yticklabels()]
    assert labels and not any("MutationFamily" in lab for lab in labels)
    assert any("| biophysical (n=" in lab for lab in labels)


def test_fig4_efficiency_curve(tmp_path):
    paths = F.fig4_efficiency_curve(_curves(), tmp_path / "fig4.pdf")
    _check_outputs(paths, tmp_path / "fig4")


def test_fig5_heldout_generalization(tmp_path):
    paths = F.fig5_heldout_generalization(_heldout_table(), tmp_path / "fig5")
    _check_outputs(paths, tmp_path / "fig5")


def test_fig6_false_positives(tmp_path):
    fp, sens = _fp_tables()
    paths = F.fig6_false_positives(fp, sens, tmp_path / "fig6")
    _check_outputs(paths, tmp_path / "fig6")


def test_fig7_case_studies(tmp_path):
    paths = F.fig7_case_studies(_case_traces(), tmp_path / "fig7")
    _check_outputs(paths, tmp_path / "fig7")


def test_fig8_agent_case_study(tmp_path):
    paths = F.fig8_agent_case_study(_agent_outcomes(), tmp_path / "fig8")
    _check_outputs(paths, tmp_path / "fig8")


def test_pdf_output_is_reproducible(tmp_path):
    first = F.fig2_validation_cascade(M.validation_cascade([MC.SILENT, MC.EQUIVALENT]), tmp_path / "a")
    second = F.fig2_validation_cascade(M.validation_cascade([MC.SILENT, MC.EQUIVALENT]), tmp_path / "b")
    assert first[1].read_bytes() == second[1].read_bytes()


# --------------------------------------------------------------------------- input checks


@pytest.mark.parametrize(
    "call",
    [
        lambda p: F.fig1_concept(_concept_traces().drop(columns="role"), p),
        lambda p: F.fig2_validation_cascade(pd.DataFrame({"stage": ["total"]}), p),
        lambda p: F.fig3_detection_heatmap(_detections().drop(columns="family"), p),
        lambda p: F.fig4_efficiency_curve(_curves().drop(columns="cost"), p),
        lambda p: F.fig5_heldout_generalization(_heldout_table().drop(columns="strategy"), p),
        lambda p: F.fig6_false_positives(_fp_tables()[0], _fp_tables()[1].drop(columns="series"), p),
        lambda p: F.fig7_case_studies(_case_traces().drop(columns="case_id"), p),
        lambda p: F.fig8_agent_case_study(_agent_outcomes().drop(columns="outcome"), p),
    ],
)
def test_missing_columns_raise(tmp_path, call):
    with pytest.raises(ValueError, match="missing required column"):
        call(tmp_path / "x")
    assert not list(tmp_path.iterdir())


def test_semantic_input_errors(tmp_path):
    only_canonical = _concept_traces().query("protocol_id == 'P00_canonical'")
    with pytest.raises(ValueError, match="at least one other protocol"):
        F.fig1_concept(only_canonical, tmp_path / "x")
    no_variant = _concept_traces().query("not (protocol_id == 'P08_rebound' and role == 'variant')")
    with pytest.raises(ValueError, match="variant"):
        F.fig1_concept(no_variant, tmp_path / "x")
    det = _detections()
    with pytest.raises(ValueError, match="duplicate"):
        F.fig3_detection_heatmap(pd.concat([det, det.iloc[:1]]), tmp_path / "x")
    with pytest.raises(ValueError, match="protocol_order"):
        F.fig3_detection_heatmap(det, tmp_path / "x", protocol_order=["P00"])
    with pytest.raises(TypeError):
        F.fig2_validation_cascade({"stage": ["total"], "count": [1]}, tmp_path / "x")


def test_palette_is_okabe_ito_and_titles_make_no_claims():
    assert set(F.OKABE_ITO.values()) == {"#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2",
                                         "#D55E00", "#CC79A7"}
    assert set(F.PALETTE) <= set(F.OKABE_ITO.values())
    claim_words = ("outperform", "better", "worse", "superior", "significant", "improve", "beats", "fails to",
                   "more than", "higher", "lower", "generalizes", "robust", "%")
    for title in F.FIGURE_TITLES.values():
        assert not any(w in title.lower() for w in claim_words), title
    assert sorted(F.FIGURE_TITLES) == [f"fig{i}" for i in range(1, 9)]
