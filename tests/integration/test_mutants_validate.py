"""Mutants of the pilot models under jNeuroML: structural validation and harness execution.

Validity is *reported*, not asserted: a structurally invalid mutant is a legitimate
class-1 outcome, not a test failure. What is asserted is that the tool could judge every
mutant (``valid is not None``), that the unmutated references are valid, and that
single-operator enforcement passes for every generated mutant re-loaded from disk.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np
import pytest

from nexclamp.models import copy_workspace, materialize
from nexclamp.mutations import REGISTRY, enforce_single_operator, generate_mutants, load_variant
from nexclamp.mutations.base import cell_rel, harness_simulation, read_xml, transitive_includes, write_xml
from nexclamp.provenance import sha256_file, sha256_json
from nexclamp.simulators.base import OutputSpec

PILOT = ["pospischil2008_rs", "pospischil2008_lts"]


def _validation_key(ws) -> str:
    """Validation of the cell file depends only on the cell file and what it includes."""
    return sha256_json({rel: sha256_file(ws.path(rel)) for rel in transitive_includes(ws, cell_rel(ws))})


@pytest.mark.jnml
@pytest.mark.parametrize("model_id", PILOT)
def test_mutants_validate_and_pass_enforcement(model_id, models, sim, tmp_path, capsys):
    ref = materialize(models[model_id], tmp_path / "ref")
    ref_result = sim.validate([ref.cell_path])
    assert ref_result.valid is True, ref_result.raw_output

    records = generate_mutants(models[model_id], sorted(REGISTRY), 2, 20260913, tmp_path / "variants")
    base = {"stimulus", "biophysical", "reference", "numerical"}
    assert base <= {r.family for r in records} <= base | {"kinetics"}   # kinetics only where a core gate or vShift exists

    cache = {_validation_key(ref): ref_result}
    report: dict[str, list[tuple[str, bool, list[str]]]] = defaultdict(list)
    for rec in records:
        ws, loaded = load_variant(tmp_path / "variants" / model_id / rec.variant_id, models)
        enforce_single_operator(ref, ws, loaded)
        key = _validation_key(ws)
        if key not in cache:
            cache[key] = sim.validate([ws.cell_path])
        result = cache[key]
        assert result.valid is not None, f"validator could not judge {rec.variant_id}: {result.messages}"
        report[rec.operator].append((rec.variant_id, bool(result.valid), result.messages[:2]))

    invalid_ops = sorted(op for op, rows in report.items() if any(not ok for _, ok, _ in rows))
    with capsys.disabled():
        print(f"\n[{model_id}] {len(records)} mutants, {len(cache)} distinct cell-file validations")
        for op in sorted(report):
            rows = report[op]
            print(f"  {op:30s} valid {sum(ok for _, ok, _ in rows)}/{len(rows)}"
                  + "".join(f"\n      {vid}: {msgs}" for vid, ok, msgs in rows if not ok))
        print(f"  operators yielding structurally invalid cell files: {invalid_ops}")


def _short_harness(ws, length: str = "400ms", step: str = "0.025ms") -> None:
    doc = read_xml(ws.harness_path)
    sim_el = harness_simulation(doc.root)
    sim_el.set("length", length)
    sim_el.set("step", step)
    write_xml(doc)


@pytest.mark.jnml
@pytest.mark.parametrize("method", ["rk4", "eulertree"])
def test_solver_config_harness_still_runs(method, models, sim, tmp_path, capsys):
    """The mutated harness (``<Meta for="jlems" method=...>``) must still run under jnml.

    Setup: RS harness shortened identically for reference and mutant to 400 ms at
    dt 0.025 ms (stimulus onset at 300 ms, so spikes occur in the window).
    Observed on 2026-09-13 (jNeuroML 0.14.0 / jLEMS 0.12.0, Temurin 21): both ``rk4`` and
    ``eulertree`` runs finished with status OK, 3 spikes, and a voltage trace
    bit-identical to the reference (max |dv| = 0.0 mV); the same held for LTS (no spikes
    in that window) in an exploratory run. How this relates to the Milestone 0 source
    reading of jLEMS ``Sim.java`` (docs/m0_evidence/tools/neuroml-lems.verify.json):
    jnml's ``Sim.run()`` already takes the consolidated (flattened) path, so ``rk4`` is a
    documented no-op; ``eulertree`` DOES change the code path (it skips consolidation and
    integrates the raw state tree, still with forward Euler). The identical ``eulertree``
    trace is therefore an empirical observation for this model, window and simulator
    version, consistent with both paths being forward Euler, not an equivalence that
    holds by construction. Identity is reported here, not asserted, because it is a
    property of the simulator version rather than of NeuroSem.
    """
    model = models["pospischil2008_rs"]
    ref = materialize(model, tmp_path / "ref")
    site = next(s for s in REGISTRY["solver_config"].sites(ref) if s.params["method"] == method)
    var = copy_workspace(ref, tmp_path / "var")
    _, exec_overrides, _ = REGISTRY["solver_config"].apply(var, site)
    assert exec_overrides == {"integrator_method": method}
    _short_harness(ref)
    _short_harness(var)
    out = [OutputSpec(model.harness_output_file, {"v": int(model.harness_v_column)})]
    r_ref, r_var = sim.run_lems(ref.harness_path, out), sim.run_lems(var.harness_path, out)
    assert r_ref.status.value == "ok", r_ref.message
    assert r_var.status.value == "ok", r_var.message
    a, b = r_ref.traces["v"], r_var.traces["v"]
    assert a.v_mV.shape == b.v_mV.shape
    with capsys.disabled():
        print(f"\n[solver_config={method}] max|dv| vs reference = {float(np.max(np.abs(a.v_mV - b.v_mV)))} mV")
