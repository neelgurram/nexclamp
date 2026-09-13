"""Tolerance rule, detection and six-way classification on synthetic fingerprints."""

from __future__ import annotations

import math
from collections import namedtuple

import pytest

from neurosem.protocols.definitions import CANONICAL_ID
from neurosem.schemas import MutantClass, RunStatus
from neurosem.validation.convergence import (EXCLUDED_DEFINEDNESS, EXCLUDED_REGIME, MISSING, ToleranceTable, calibrate,
                                             convergence_report)
from neurosem.validation.fingerprint import Detection, Fingerprint, ToolFailure, classify, compare, detecting_protocols

FV = namedtuple("FV", "name value state unit source")

TOL_CFG = {
    "c_refinement": 3.0,
    "features": {
        "latency": {"abs_floor": 0.5, "rel": 0.02},
        "count": {"abs_floor": 0.5, "rel": 0.0},
        "regime": {},
        "rheobase": {"abs_floor": 0.0, "rel": 0.02, "resolution_multiple": 2.0},
    },
}
FEAT_CFG = {"features": {"count": {"kind": "count"}, "regime": {"kind": "categorical"}}}


def d(v):
    return FV("x", v, "defined", "", "t")


U = FV("x", None, "undefined", "", "t")
NA = FV("x", None, "not_applicable", "", "t")


def fp(tables, factor=1, status=RunStatus.OK, variant="ref", rheobase=None):
    return Fingerprint("m", variant, factor, 0.005 / factor, status, rheobase, tables,
                       {pid: f"{variant}-{pid}-{factor}" for pid in tables})


def test_tau_is_max_of_three_terms_and_names_the_limiting_term():
    h = fp({"P1": {"latency": d(100.0)}})
    h2 = fp({"P1": {"latency": d(100.1)}}, 2)
    (e,) = calibrate({1: h, 2: h2}, "m", TOL_CFG, FEAT_CFG)
    assert e.rel_term == pytest.approx(2.0)
    assert e.refine_term == pytest.approx(0.3)
    assert e.tau == pytest.approx(2.0) and e.limiting == "relative"

    h2b = fp({"P1": {"latency": d(101.0)}}, 2)
    (e2,) = calibrate({1: h, 2: h2b}, "m", TOL_CFG, FEAT_CFG)
    assert e2.tau == pytest.approx(3.0) and e2.limiting == "refinement"

    hs = fp({"P1": {"latency": d(1.0)}})
    (e3,) = calibrate({1: hs, 2: fp({"P1": {"latency": d(1.0)}}, 2)}, "m", TOL_CFG, FEAT_CFG)
    assert e3.tau == pytest.approx(0.5) and e3.limiting == "abs_floor"


def test_state_changes_under_refinement_are_excluded_not_dropped():
    h = fp({"P1": {"latency": d(10.0), "regime": d("tonic"), "count": U}})
    h2 = fp({"P1": {"latency": NA, "regime": d("adapting"), "count": U}}, 2)
    entries = {e.feature: e for e in calibrate({1: h, 2: h2}, "m", TOL_CFG, FEAT_CFG)}
    assert entries["latency"].limiting == EXCLUDED_DEFINEDNESS and entries["latency"].tau is None
    assert entries["regime"].limiting == EXCLUDED_REGIME and entries["regime"].excluded
    assert entries["count"].limiting == "both_undefined" and entries["count"].tau == math.inf


def test_missing_protocol_at_h2_is_recorded():
    (e,) = calibrate({1: fp({"P1": {"latency": d(1.0)}}), 2: fp({}, 2)}, "m", TOL_CFG, FEAT_CFG)
    assert e.limiting == MISSING and e.excluded


def test_rheobase_floor_uses_search_resolution():
    rh = {"upper_nA": 0.5, "lower_nA": 0.45}
    h = fp({"P03_rheobase": {"rheobase": d(0.5)}}, rheobase=rh)
    h2 = fp({"P03_rheobase": {"rheobase": d(0.5)}}, 2, rheobase=rh)
    (e,) = calibrate({1: h, 2: h2}, "m", TOL_CFG, FEAT_CFG)
    assert e.abs_floor == pytest.approx(0.1) and e.tau == pytest.approx(0.1)


def test_calibration_requires_h_and_h2():
    with pytest.raises(ValueError):
        calibrate({1: fp({})}, "m", TOL_CFG, FEAT_CFG)


def test_tolerance_csv_round_trip(tmp_path):
    h = fp({"P1": {"latency": d(10.0), "regime": d("tonic"), "count": U}})
    h2 = fp({"P1": {"latency": d(10.2), "regime": d("tonic"), "count": U}}, 2)
    t = ToleranceTable(calibrate({1: h, 2: h2}, "m", TOL_CFG, FEAT_CFG))
    t.to_csv(tmp_path / "tol.csv")
    back = ToleranceTable.from_csv(tmp_path / "tol.csv")
    for e in t.entries:
        b = back.get(e.model_id, e.protocol_id, e.feature)
        assert b.limiting == e.limiting and b.kind == e.kind and b.f_h == e.f_h
        assert (b.tau == e.tau) or (math.isinf(b.tau) and math.isinf(e.tau))
    with pytest.raises(ValueError):
        ToleranceTable(t.entries + t.entries[:1])


def _table(ref_latency=10.0, h2_latency=10.1):
    h = fp({"P1": {"latency": d(ref_latency), "regime": d("tonic"), "count": d(5.0)},
            CANONICAL_ID: {"count": d(5.0)}})
    h2 = fp({"P1": {"latency": d(h2_latency), "regime": d("tonic"), "count": d(5.0)},
             CANONICAL_ID: {"count": d(5.0)}}, 2)
    return h, ToleranceTable(calibrate({1: h, 2: h2}, "m", TOL_CFG, FEAT_CFG))


def test_compare_exceeds_definedness_categorical_and_multiplier():
    ref, tol = _table()  # latency tau = max(0.5, 0.2, 0.3) = 0.5
    same = fp({"P1": {"latency": d(10.4), "regime": d("tonic"), "count": d(5.0)}, CANONICAL_ID: {"count": d(5.0)}}, variant="v")
    assert compare(ref, same, tol) == []
    moved = fp({"P1": {"latency": d(10.6), "regime": d("bursting"), "count": NA}, CANONICAL_ID: {"count": d(5.0)}}, variant="v")
    dets = {(x.feature, x.reason) for x in compare(ref, moved, tol)}
    assert dets == {("latency", "exceeds"), ("regime", "categorical"), ("count", "definedness")}
    assert all(x.ref_run_id and x.var_run_id for x in compare(ref, moved, tol))
    assert {x.feature for x in compare(ref, moved, tol, multiplier=2.0)} == {"regime", "count"}


def test_excluded_features_never_detect():
    h = fp({"P1": {"latency": d(10.0)}})
    h2 = fp({"P1": {"latency": NA}}, 2)
    tol = ToleranceTable(calibrate({1: h, 2: h2}, "m", TOL_CFG, FEAT_CFG))
    assert compare(h, fp({"P1": {"latency": d(99.0)}}, variant="v"), tol) == []


def _det(pid, feat, level=1):
    return Detection("v", "m", level, pid, feat, "exceeds", 1.0, 2.0, 1.0, 0.5, "r", "s")


def test_classification_cascade():
    ok1, ok2 = fp({}, 1, variant="v"), fp({}, 2, variant="v")
    assert classify(False, None, None, [], None) is MutantClass.STRUCTURALLY_INVALID
    assert classify(True, fp({}, status=RunStatus.BUILD_ERROR), None, [], None) is MutantClass.NON_EXECUTABLE
    assert classify(True, fp({}, status=RunStatus.UNSTABLE), None, [], None) is MutantClass.NUMERICALLY_UNSTABLE
    assert classify(True, ok1, None, [], None) is MutantClass.EQUIVALENT
    # detected at h only -> not reproducible -> equivalent within tested domain
    assert classify(True, ok1, ok2, [_det("P1", "latency")], []) is MutantClass.EQUIVALENT
    # reproducible battery detection, canonical silent -> SILENT
    k = classify(True, ok1, ok2, [_det("P1", "latency")], [_det("P1", "latency", 2)])
    assert k is MutantClass.SILENT and k.admissible
    # canonical also detects reproducibly -> NON_EQUIVALENT
    assert classify(True, ok1, ok2, [_det("P1", "latency"), _det(CANONICAL_ID, "count")],
                    [_det("P1", "latency", 2), _det(CANONICAL_ID, "count", 2)]) is MutantClass.NON_EQUIVALENT
    # canonical detection at h that vanishes at h/2 is solver noise, as for every protocol -> SILENT
    assert classify(True, ok1, ok2, [_det("P1", "latency"), _det(CANONICAL_ID, "count")],
                    [_det("P1", "latency", 2)]) is MutantClass.SILENT
    # only canonical reproducible -> NON_EQUIVALENT, not silent
    assert classify(True, ok1, ok2, [_det(CANONICAL_ID, "count")], [_det(CANONICAL_ID, "count", 2)]) is MutantClass.NON_EQUIVALENT
    # different feature at each level is not reproducible
    assert classify(True, ok1, ok2, [_det("P1", "latency")], [_det("P1", "count", 2)]) is MutantClass.EQUIVALENT
    with pytest.raises(ToolFailure):
        classify(None, ok1, None, [], None)
    assert detecting_protocols([_det("P1", "a"), _det("P2", "b")], [_det("P1", "a", 2)]) == {"P1"}


def test_convergence_report_observed_order():
    h = fp({"P1": {"latency": d(10.0)}})
    h2 = fp({"P1": {"latency": d(9.0)}}, 2)
    h4 = fp({"P1": {"latency": d(8.5)}}, 4)
    (row,) = convergence_report({1: h, 2: h2, 4: h4})
    assert row["d12"] == pytest.approx(1.0) and row["d24"] == pytest.approx(0.5)
    assert row["observed_order"] == pytest.approx(1.0)
