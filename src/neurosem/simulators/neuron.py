"""NEURON adapter (optional cross-simulator extension; not used by the pilot).

The specification makes 4-6 cross-simulator models "optional but valuable". NEURON is
not installed in the frozen pilot environment. When enabled, this adapter will export
LEMS files with ``jnml <LEMS> -neuron`` (verified to exist in jNeuroML 0.14.0 via
``pynml -h``), compile the generated mechanisms, run them, and read the same OutputFile
columns so traces feed the identical feature and tolerance pipeline. NEURON integrates
differently from jLEMS's forward Euler, so tolerances must be calibrated per simulator.
"""

from __future__ import annotations

from pathlib import Path

from neurosem.schemas import RunStatus, SimResult, ValidationResult
from neurosem.simulators.base import OutputSpec


class NeuronSimulator:
    name = "NEURON"

    def available(self) -> bool:
        try:
            import neuron  # noqa: F401
        except ImportError:
            return False
        return True

    def version_info(self) -> dict[str, str]:
        if not self.available():
            return {"simulator": "NEURON", "status": "not installed"}
        import neuron

        return {"simulator": "NEURON", "neuron_version": neuron.__version__}

    def validate(self, files: list[Path]) -> ValidationResult:
        return ValidationResult(None, -1, ["NEURON does not validate NeuroML; use jNeuroML"], "", self.name)

    def run_lems(self, lems_file: Path, outputs: list[OutputSpec], timeout_s: float = 3600.0) -> SimResult:
        return SimResult(RunStatus.TOOL_FAILURE, -1, 0.0, {}, [],
                         "NEURON cross-simulator runs are an optional extension and are not implemented in the pilot")
