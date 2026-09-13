"""A run that starts and then diverges under a too-large step is UNSTABLE, not a build error.

Reproduces the case seen in the pilot integration check: a x20 time-step mutant ran the RS
battery at dt = 0.1 ms; the 2 x rheobase step made forward-Euler HH rate expressions overflow
shortly after stimulus onset and jLEMS aborted with a time-step hint.
"""

from __future__ import annotations

import pytest

from neurosem.protocols.definitions import DEFAULT_TEMPLATES
from neurosem.protocols.generate import canonical_output, write_probe
from neurosem.schemas import ExecConfig, RunStatus

pytestmark = pytest.mark.jnml


def test_huge_step_during_spiking_is_numerically_unstable(rs_ws, sim):
    step2x = next(t for t in DEFAULT_TEMPLATES if t.protocol_id == "P04_step_2x").instantiate(0.5607, 300.0)
    bundle = write_probe(rs_ws, [step2x], ExecConfig(0.1), tag="unstable")
    res = sim.run_lems(bundle.lems_file, [bundle.output], timeout_s=300)
    assert res.status is RunStatus.UNSTABLE, (res.status, res.message)


def test_quiet_huge_step_can_still_run(rs_ws, sim):
    baseline = next(t for t in DEFAULT_TEMPLATES if t.protocol_id == "P01_baseline").instantiate(0.5607, 300.0)
    bundle = write_probe(rs_ws, [baseline], ExecConfig(0.1), tag="quiet")
    res = sim.run_lems(bundle.lems_file, [bundle.output], timeout_s=300)
    assert res.status is RunStatus.OK


def test_missing_component_is_build_error(rs_ws, sim):
    h = rs_ws.harness_path
    h.write_text(h.read_text(encoding="utf-8").replace('<Include file="RS.net.nml"/>', '<Include file="NOPE.net.nml"/>'),
                 encoding="utf-8")
    res = sim.run_lems(h, [canonical_output(rs_ws.model)], timeout_s=300)
    assert res.status is RunStatus.BUILD_ERROR
