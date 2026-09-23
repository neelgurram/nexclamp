"""DetectionMatrix: validation, detection rate, exact CSV round trip, and protocol costs."""

from __future__ import annotations

import numpy as np
import pytest

from nexclamp.config import study
from nexclamp.protocols.definitions import batched, templates_from_config
from nexclamp.protocols.generate import group_by_length, write_probe
from nexclamp.schemas import ExecConfig
from nexclamp.selection.matrix import COST_ROW_ID, DetectionMatrix, cell_step_costs


def small() -> DetectionMatrix:
    det = np.array([[1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                    [0, 0, 0]], dtype=bool)
    ids = [f"m{i}" for i in range(5)]
    return DetectionMatrix(ids, ["P01", "P02", "P03"], det,
                           {m: ("modelA" if i < 3 else "modelB") for i, m in enumerate(ids)},
                           {m: "biophysical" for m in ids},
                           {"P01": 100.0, "P02": 250.0, "P03": 1 / 3})


def test_rate_is_fraction_detected_by_any_protocol():
    m = small()
    assert m.rate(["P01"]) == pytest.approx(2 / 5)
    assert m.rate(["P01", "P02"]) == pytest.approx(3 / 5)
    assert m.rate(["P01", "P02", "P03"]) == pytest.approx(4 / 5)
    assert m.rate([]) == 0.0
    mask = np.array([False, False, True, True, True])
    assert m.rate(["P02"], rows=mask) == pytest.approx(1 / 3)
    # repeated indices weight a mutant twice (bootstrap resamples)
    assert m.rate(["P01"], rows=np.array([0, 0, 4])) == pytest.approx(2 / 3)
    assert m.total_cost(["P01", "P03"]) == pytest.approx(100 + 1 / 3)


def test_rate_errors():
    m = small()
    with pytest.raises(KeyError):
        m.rate(["P99"])
    with pytest.raises(ValueError):
        m.rate(["P01"], rows=np.zeros(5, dtype=bool))
    with pytest.raises(IndexError):
        m.rate(["P01"], rows=np.array([5]))
    with pytest.raises(ValueError):
        m.rate(["P01"], rows=np.ones(4, dtype=bool))


@pytest.mark.parametrize("change", ["shape", "dup_mutant", "dup_protocol", "missing_cost", "negative_cost",
                                    "nan_cost", "non_binary", "missing_model", "reserved_id"])
def test_construction_validation(change):
    ids, pids = ["a", "b"], ["P1", "P2"]
    det = np.zeros((2, 2), dtype=int)
    model_of, family_of, cost = {"a": "x", "b": "x"}, {"a": "f", "b": "f"}, {"P1": 1.0, "P2": 2.0}
    if change == "shape":
        det = np.zeros((2, 3), dtype=int)
    elif change == "dup_mutant":
        ids = ["a", "a"]
    elif change == "dup_protocol":
        pids = ["P1", "P1"]
    elif change == "missing_cost":
        cost = {"P1": 1.0}
    elif change == "negative_cost":
        cost["P2"] = -1.0
    elif change == "nan_cost":
        cost["P2"] = float("nan")
    elif change == "non_binary":
        det[0, 0] = 2
    elif change == "missing_model":
        model_of = {"a": "x"}
    elif change == "reserved_id":
        ids = ["a", COST_ROW_ID]
        model_of[COST_ROW_ID] = "x"
        family_of[COST_ROW_ID] = "f"
    with pytest.raises(ValueError):
        DetectionMatrix(ids, pids, det, model_of, family_of, cost)


def test_integer_matrix_is_coerced_to_bool_copy():
    det = np.array([[0, 1], [1, 0]])
    m = DetectionMatrix(["a", "b"], ["P1", "P2"], det, {"a": "x", "b": "y"}, {"a": "f", "b": "f"},
                        {"P1": 1, "P2": 2})
    assert m.detected.dtype == np.bool_
    det[0, 0] = 1
    assert not m.detected[0, 0]
    assert isinstance(m.cost["P1"], float)


def test_csv_round_trip_is_exact_and_byte_stable(tmp_path):
    rng = np.random.default_rng(7)
    ids = ["mut,with,comma", 'quote"id', "plain"] + [f"m{i}" for i in range(20)]
    pids = ["P00_canonical", "P01_baseline", "P05_long_step", "P10_paired_pulses"]
    det = rng.random((len(ids), len(pids))) < 0.4
    cost = {"P00_canonical": 1 / 3, "P01_baseline": 200000.0, "P05_long_step": 12345678.901234567,
            "P10_paired_pulses": 1e300}
    m = DetectionMatrix(ids, pids, det, {i: f"model{j % 3}" for j, i in enumerate(ids)},
                        {i: ("numerical" if j % 2 else "reference") for j, i in enumerate(ids)}, cost)
    p1, p2 = tmp_path / "a" / "matrix.csv", tmp_path / "b.csv"
    m.to_csv(p1)
    back = DetectionMatrix.from_csv(p1)
    assert back == m
    assert back.cost == cost                     # exact float equality, not approx
    back.to_csv(p2)
    assert p1.read_bytes() == p2.read_bytes()
    lines = p1.read_bytes().split(b"\n")
    assert lines[0] == b"mutant_id,model_id,family," + ",".join(pids).encode()
    assert lines[1].startswith(COST_ROW_ID.encode() + b",,,")
    assert b"\r" not in p1.read_bytes()


def test_csv_round_trip_with_zero_rows(tmp_path):
    m = DetectionMatrix([], ["P1"], np.zeros((0, 1), dtype=bool), {}, {}, {"P1": 5.0})
    m.to_csv(tmp_path / "empty.csv")
    assert DetectionMatrix.from_csv(tmp_path / "empty.csv") == m


@pytest.mark.parametrize("text", [
    "mutant_id,model_id,family,P1\na,x,f,1\n",                       # no cost row
    "mutant_id,model_id,family,P1\n__cost__,,,1.0\na,x,f,2\n",       # non-binary value
    "mutant_id,model_id,family,P1\n__cost__,,,1.0\na,x,f,1,0\n",     # ragged row
    "mutant_id,model_id,family,P1\n__cost__,,,1.0\na,x,f,1\na,x,f,0\n",  # duplicate mutant
    "id,model,family,P1\n__cost__,,,1.0\n",                          # wrong header
])
def test_from_csv_rejects_malformed(tmp_path, text):
    p = tmp_path / "bad.csv"
    p.write_bytes(text.encode())
    with pytest.raises(ValueError):
        DetectionMatrix.from_csv(p)


def test_from_detected_sets_and_take_rows():
    m = small()
    built = DetectionMatrix.from_detected_sets(
        m.mutant_ids, m.protocol_ids,
        {"m0": {"P01"}, "m1": ["P01", "P02"], "m2": ("P02",), "m3": {"P03"}, "m4": set()},
        m.model_of, m.family_of, m.cost)
    assert built == m
    with pytest.raises(KeyError):
        DetectionMatrix.from_detected_sets(["m0"], ["P01"], {}, {"m0": "x"}, {"m0": "f"}, {"P01": 1.0})
    with pytest.raises(KeyError):
        DetectionMatrix.from_detected_sets(["m0"], ["P01"], {"m0": ["P02"]}, {"m0": "x"}, {"m0": "f"}, {"P01": 1.0})
    sub = m.take_rows(np.array([3, 1]))
    assert sub.mutant_ids == ["m3", "m1"]
    assert sub.model_of == {"m3": "modelB", "m1": "modelA"}
    assert sub.detected.tolist() == [[False, False, True], [True, True, False]]
    with pytest.raises(ValueError):
        m.take_rows(np.array([1, 1]))


def test_cell_step_costs_match_probe_bundles(rs_ws):
    """Costs from real protocol definitions equal the cell-steps write_probe reports per batch."""
    templates = batched(templates_from_config(study()["protocols"]))
    protocols = [t.instantiate(0.1, 300.0) for t in templates]
    dt = 0.025
    costs = cell_step_costs(protocols, dt, measured={"P03_rheobase": 987654.0})
    assert costs["P03_rheobase"] == 987654.0
    assert costs["P05_long_step"] == pytest.approx((300 + 2000 + 200) / dt)
    for i, group in enumerate(group_by_length(protocols)):
        bundle = write_probe(rs_ws, group, ExecConfig(dt_ms=dt), tag=f"cost{i}")
        assert bundle.cell_steps == sum(costs[p.protocol_id] for p in group)
    with pytest.raises(ValueError):
        cell_step_costs(protocols, 0.0)
