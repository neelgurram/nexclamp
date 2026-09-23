"""Full-trace regression, severity levels and analysis families (PILOT2_PROTOCOL)."""

from __future__ import annotations

from types import SimpleNamespace as NS

import numpy as np
import pytest

from nexclamp.experiments import strata
from nexclamp.mutations import REGISTRY
from nexclamp.mutations import severity as sev
from nexclamp.schemas import Trace
from nexclamp.validation import trace_regression as tr


def spiky(times, dt=0.01, length=300.0, width=1.0):
    t = np.arange(0.0, length, dt)
    v = np.full_like(t, -65.0)
    for s in times:
        v[(t >= s) & (t < s + width)] = 30.0
    return Trace(t, v)


def test_calibration_and_detection_of_the_three_trace_checks():
    ref_h = {"P00_canonical": spiky([100, 150, 200])}
    ref_h2 = {"P00_canonical": spiky([100.1, 150.1, 200.1], dt=0.005)}
    tol = tr.calibrate(ref_h, ref_h2, "m", c=3.0)["P00_canonical"]
    assert tol.status == "ok" and tol.ref_spike_count == 3
    assert tol.tau_shift == pytest.approx(max(tr.SHIFT_FLOOR_MS, 3 * 0.1), abs=0.02)
    same = tr.compare(ref_h, {"P00_canonical": spiky([100, 150, 200])}, {"P00_canonical": tol}, "v", "m", 1)
    assert same == []
    shifted = tr.compare(ref_h, {"P00_canonical": spiky([100, 150, 203])}, {"P00_canonical": tol}, "v", "m", 1)
    assert {d.metric for d in shifted} >= {"spike_timing"}
    extra = tr.compare(ref_h, {"P00_canonical": spiky([100, 150, 200, 250])}, {"P00_canonical": tol}, "v", "m", 1)
    assert "spike_count" in {d.metric for d in extra}
    exact = tr.calibrate({"P07": spiky([])}, {"P07": spiky([], dt=0.005)}, "m", 3.0)["P07"]
    assert exact.tau_rmse == tr.RMSE_FLOOR_MV                 # identical refinement: the floor applies
    offset = spiky([])
    offset.v_mV[:] = offset.v_mV + 1.0
    assert [d.metric for d in tr.compare({"P07": spiky([])}, {"P07": offset}, {"P07": exact}, "v", "m", 1)] == ["trace_rmse"]


def test_protocols_unresolved_under_refinement_are_excluded_not_dropped():
    tol = tr.calibrate({"P05": spiky([100, 150])}, {"P05": spiky([100, 150, 200], dt=0.005)}, "m", 3.0)["P05"]
    assert tol.status == "excluded_spike_count_changes_under_refinement" and tol.tau_rmse is None
    assert tr.compare({"P05": spiky([1])}, {"P05": spiky([2, 3])}, {"P05": tol}, "v", "m", 1) == []


def test_trace_detections_must_reproduce():
    d1 = [NS(protocol_id="P00_canonical", metric="spike_timing"), NS(protocol_id="P04", metric="trace_rmse")]
    d2 = [NS(protocol_id="P00_canonical", metric="spike_timing")]
    assert tr.reproducible(d1, d2) == {("P00_canonical", "spike_timing")}
    assert tr.reproducible(d1, None) == set()


@pytest.mark.parametrize("params, level", [
    ({"factor": 0.8}, sev.MILD), ({"factor": 1.25}, sev.MILD), ({"factor": 0.9}, sev.MILD),
    ({"factor": 2.0}, sev.STRONG), ({"factor": 0.5}, sev.STRONG), ({"factor": 1.5}, sev.INTERMEDIATE),
    ({"shift_mV": -5.0}, sev.MILD), ({"shift_mV": 10.0}, sev.STRONG), ({"delta_mV": 20.0}, sev.STRONG),
    ({"shift_mV": 7.0}, sev.INTERMEDIATE), ({"channel": "x"}, sev.NOT_APPLICABLE)])
def test_severity_comes_only_from_the_recorded_magnitude(params, level):
    assert sev.severity(params) == level


def test_site_selection_draws_per_level_and_is_seeded():
    sites = [NS(params={"factor": f}, operator="scale_conductance", idx=i) for i, f in enumerate((0.5, 0.8, 0.9, 1.1, 1.25, 2.0))]
    a = sev.select_sites(sites, "scale_conductance", 7, ["mild", "strong"], per_level=1)
    b = sev.select_sites(sites, "scale_conductance", 7, ["mild", "strong"], per_level=1)
    assert [s.idx for s in a] == [s.idx for s in b]
    assert sorted(sev.severity(s.params) for s in a) == ["mild", "strong"]
    flat = [NS(params={"channel": c}) for c in "abc"]
    assert len(sev.select_sites(flat, "wrong_channel", 7, ["mild", "strong"], without_magnitude=1)) == 1


def test_every_semantic_operator_has_an_analysis_family():
    for name, op in REGISTRY.items():
        fam = op.family.value
        af = strata.analysis_family(name, fam)
        if fam in strata.SEMANTIC_FAMILIES:
            assert af in set(strata.ANALYSIS_FAMILY.values()), name
    assert strata.analysis_family("increase_dt", "numerical") == "numerical_robustness"
    assert strata.analysis_family("xml_formatting", "") == "control"


def test_candidate_rows_are_normalised_and_zero_conductances_are_not_sites(tmp_path):
    import csv

    from nexclamp.models import MANIFEST_COLUMNS
    from nexclamp.orchestration.curation import decide, read_candidates

    row = {k: "" for k in MANIFEST_COLUMNS}
    row.update(model_id="x", harness_v_column="7 (Pop0[6] at +170 pA)", temperature="6.3 degC (networkWithTemperature in a.nml)")
    path = tmp_path / "c.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        w.writeheader()
        w.writerow(row)
    [m] = read_candidates([path])
    assert (m.harness_v_column, m.temperature) == ("7", "6.3 degC")
    assert decide({"a": True, "b": None}) == ("review", ["b"]) and decide({"a": False, "b": None})[0] == "exclude"


def test_scaling_a_zero_conductance_is_not_a_site(hh_ws):
    p = hh_ws.cell_path
    p.write_text(p.read_text(encoding="utf-8").replace('condDensity="3.0 S_per_m2"', 'condDensity="0.0 S_per_m2"'),
                 encoding="utf-8")
    sites = REGISTRY["scale_conductance"].sites(hh_ws)
    assert sites and all(s.params["element_id"] != "leak" for s in sites)
