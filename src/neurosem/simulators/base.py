"""Simulator interface.

A simulator validates NeuroML files and runs LEMS simulation files. It must never
confuse "the tool is broken" with "the model is broken": tool problems are reported
as :attr:`RunStatus.TOOL_FAILURE` / ``ValidationResult.valid is None``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from neurosem.schemas import SimResult, ValidationResult

# Voltages outside this band (mV) are treated as numerical blow-up, not physiology.
PHYSICAL_V_BOUND_MV = 250.0


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
