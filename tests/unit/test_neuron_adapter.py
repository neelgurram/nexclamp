"""NEURON adapter: export works everywhere, execution is honest about a missing runtime (N-08).

The export half of the cross-simulator evidence needs only Java and the jNeuroML jar, so it is
tested here for real. The execution half needs a NEURON runtime; where none exists the adapter must
say so precisely rather than pretend the model failed.
"""

from __future__ import annotations

import pytest

from neuraxis.schemas import RunStatus
from neuraxis.simulators.neuron import NeuronSimulator, export_to_neuron


@pytest.fixture(scope="module")
def nrn():
    return NeuronSimulator()


def test_a_missing_runtime_is_never_reported_as_a_model_failure(nrn, tmp_path):
    """No runtime must give TOOL_FAILURE with an actionable message, never RUNTIME_ERROR."""
    if nrn.available():
        pytest.skip("NEURON is installed here; this test covers the absent-runtime path")
    info = nrn.version_info()
    assert info["simulator"] == "NEURON" and info["status"] == "not installed"
    assert "NEURON (not installed)" == nrn.version_string()
    missing = tmp_path / "nothing.xml"
    missing.write_text("<Lems/>", encoding="utf-8")
    out = nrn.run_lems(missing, [])
    assert out.status is RunStatus.TOOL_FAILURE
    assert "export" in out.message.lower() or "not installed" in out.message.lower()


def test_validation_stays_with_jneuroml(nrn):
    """NEURON has no NeuroML validator, so validity is never re-decided here (D-006)."""
    result = nrn.validate([])
    assert result.valid is None and "does not validate" in result.messages[0]


@pytest.mark.jnml
def test_export_generates_mechanisms_and_a_runner(hh_ws):
    """``jnml -neuron`` must produce .mod mechanisms, a .hoc cell and a Python runner."""
    exported = export_to_neuron(hh_ws.harness_path)
    assert exported.ok, exported.output[-500:]
    assert exported.runner is not None and exported.runner.name.endswith("_nrn.py")
    assert exported.mod_files, "no .mod mechanisms were generated"
    assert any(f.suffix == ".hoc" for f in exported.hoc_files)
    assert all(f.is_file() for f in exported.files)
    # The export must not disturb the model files the study hashes.
    assert hh_ws.cell_path.is_file() and hh_ws.harness_path.is_file()


@pytest.mark.jnml
def test_export_reports_a_bad_lems_file_without_raising(tmp_path):
    bad = tmp_path / "LEMS_broken.xml"
    bad.write_text("<Lems><Simulation id='x' unresolved='yes'/></Lems>", encoding="utf-8")
    exported = export_to_neuron(bad)
    assert exported.ok is False and exported.runner is None
    assert exported.output           # the tool's own message is kept for the record


@pytest.mark.jnml
def test_run_lems_without_a_runtime_still_proves_the_export(hh_ws, nrn):
    """The adapter exports first, so 'cannot execute' is distinguishable from 'cannot export'."""
    if nrn.available():
        pytest.skip("NEURON is installed here; this test covers the absent-runtime path")
    out = nrn.run_lems(hh_ws.harness_path, [])
    assert out.status is RunStatus.TOOL_FAILURE
    assert "exported successfully" in out.message
    assert any(hh_ws.root.rglob("*.mod")), "the export should have run before execution was attempted"
