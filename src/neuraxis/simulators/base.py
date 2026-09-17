"""Simulator interface.

A simulator validates NeuroML files and runs LEMS simulation files. It must never
confuse "the tool is broken" with "the model is broken": tool problems are reported
as :attr:`RunStatus.TOOL_FAILURE` / ``ValidationResult.valid is None``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from neuraxis.schemas import SimResult, ValidationResult

# Recorded values beyond this magnitude (after conversion to "mV") are treated as numerical blow-up.
# Deliberately far outside physiology (10 V): a harness that records a non-voltage state (a gate in
# [0, 1] or a concentration, e.g. the record_wrong_variable mutant) must be judged behaviourally, not
# labelled unstable. Real divergence in jLEMS shows up as non-finite values or an aborted run.
PHYSICAL_V_BOUND_MV = 10_000.0


@dataclass(frozen=True)
class OutputSpec:
    """Which file/columns to read after a run, and what to call each trace."""

    file: str                               # relative to the LEMS file's directory
    columns: dict[str, int]                 # trace name -> 1-based column (0 is time)


class Simulator(Protocol):
    name: str

    def available(self) -> bool: ...

    def version_info(self) -> dict[str, str]: ...

    def validate(self, files: list[Path]) -> ValidationResult: ...

    def run_lems(self, lems_file: Path, outputs: list[OutputSpec], timeout_s: float = 3600.0) -> SimResult: ...
