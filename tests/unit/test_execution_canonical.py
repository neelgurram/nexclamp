"""Execution helpers, canonical protocol parsing and harness refinement on real fixtures."""

from __future__ import annotations

import pytest

from neurosem.schemas import ExecConfig, RunStatus, VariantKind, VariantRecord
from neurosem.validation.canonical import canonical_protocol, refine_harness_step
from neurosem.validation.execution import (TaskError, apply_overrides, effective_workspace, inputs_manifest,
                                           reachable_files, run_parallel, worst_status)
from neurosem.validation.structural import harness_nml_files


def test_reachable_files_follow_includes_and_skip_core_types(rs_ws):
    files = {p.relative_to(rs_ws.root.resolve()).as_posix() for p in reachable_files(rs_ws.harness_path)}
    assert "NeuroML2/cells/RS/LEMS_RS.xml" in files
    assert "NeuroML2/cells/RS/RS.net.nml" in files and "NeuroML2/cells/RS/RS.cell.nml" in files
    assert {"NeuroML2/channels/Na/Na.channel.nml", "NeuroML2/channels/IM/IM.channel.nml"} <= files
    assert not any(f.endswith(("Cells.xml", "Simulation.xml")) for f in files)
    cell_only = {p.name for p in reachable_files(rs_ws.cell_path)}
    assert "RS.net.nml" not in cell_only and "Kd.channel.nml" in cell_only


def test_inputs_manifest_changes_when_any_reachable_file_changes(rs_ws):
    before = inputs_manifest(rs_ws.cell_path, rs_ws.root)
    assert all(not k.startswith("/") for k in before)
    ch = rs_ws.root / "NeuroML2/channels/Leak/Leak.channel.nml"
    ch.write_text(ch.read_text(encoding="utf-8") + "\n<!-- edit -->\n", encoding="utf-8")
    after = inputs_manifest(rs_ws.cell_path, rs_ws.root)
    assert before != after and set(before) == set(after)


def test_apply_overrides_and_effective_workspace(rs_ws):
    e = apply_overrides(ExecConfig(0.005), {"dt_factor": 4, "integrator_method": "rk4", "sample_every_ms": 0.5})
    assert e.dt_ms == pytest.approx(0.02) and e.integrator_method == "rk4" and e.sample_every_ms == 0.5
    v = VariantRecord("v", rs_ws.model.model_id, VariantKind.VALID_TRANSFORM, model_overrides={"cell_id": "RS2"})
    assert effective_workspace(rs_ws, v).model.cell_id == "RS2"
    with pytest.raises(ValueError):
        effective_workspace(rs_ws, VariantRecord("v", "m", VariantKind.MUTANT, model_overrides={"nope": "x"}))


def test_run_parallel_preserves_order_and_captures_errors():
    def boom():
        raise RuntimeError("x")

    out = run_parallel([lambda: 1, boom, lambda: 3], workers=3)
    assert out[0] == 1 and out[2] == 3 and isinstance(out[1], TaskError) and "RuntimeError" in out[1].error


def test_worst_status_ordering():
    assert worst_status([RunStatus.OK, RunStatus.UNSTABLE, RunStatus.BUILD_ERROR]) is RunStatus.BUILD_ERROR
    assert worst_status([RunStatus.OK, RunStatus.TOOL_FAILURE]) is RunStatus.TOOL_FAILURE
    assert worst_status([]) is RunStatus.OK


def test_canonical_protocol_windows_from_shipped_harnesses(rs_ws, lts_ws, hh_ws):
    rs = canonical_protocol(rs_ws)
    assert (rs.window.start_ms, rs.window.end_ms, rs.total_ms) == pytest.approx((300.0, 700.0, 1000.0))
    assert rs.components[0].amplitude_nA == pytest.approx(0.75)
    lts = canonical_protocol(lts_ws)
    assert (lts.window.start_ms, lts.window.end_ms) == pytest.approx((400.0, 800.0))
    hh = canonical_protocol(hh_ws)
    assert (hh.window.start_ms, hh.window.end_ms, hh.total_ms) == pytest.approx((100.0, 200.0, 300.0))


def test_refine_harness_step_divides_step(rs_ws):
    new = refine_harness_step(rs_ws.harness_path, 2.0)
    assert new == "0.0005ms"
    assert 'step="0.0005ms"' in rs_ws.harness_path.read_text(encoding="utf-8")


def test_harness_nml_files(rs_ws, hh_ws):
    assert {p.name for p in harness_nml_files(rs_ws)} >= {"RS.net.nml", "RS.cell.nml", "Na.channel.nml"}
    assert [p.name for p in harness_nml_files(hh_ws)] == ["NML2_SingleCompHHCell.nml"]


@pytest.mark.jnml
def test_structural_check_reference_and_broken_reference(rs_ws, lts_ws, sim):
    from neurosem.validation.structural import check

    r = check(rs_ws, sim)
    assert r.valid is True and r.libneuroml_strict is True and not r.baseline_errors
    # Upstream LTS channel files with custom LEMS ComponentTypes fail standalone schema validation, but the
    # cell and network files (what OMV validates) pass: the reference is valid with recorded baseline errors.
    lt = check(lts_ws, sim)
    assert lt.valid is True
    assert {"NeuroML2/channels/IT/IT.channel.nml", "NeuroML2/channels/Ca/Ca.nml"} <= set(lt.baseline_invalid_files)

    # A new error inside an INCLUDED channel file must make a variant invalid, even though validating the cell
    # file alone would not notice (verified: jnml -validate does not schema-check included files).
    leak = rs_ws.root / "NeuroML2/channels/Leak/Leak.channel.nml"
    leak.write_text(leak.read_text(encoding="utf-8").replace('pS"', 'pX"', 1), encoding="utf-8")
    bad_include = check(rs_ws, sim, reference=r)
    assert bad_include.valid is False and bad_include.new_errors

    cell = rs_ws.cell_path
    cell.write_text(cell.read_text(encoding="utf-8").replace('ionChannel="Kd"', 'ionChannel="Kdx"'), encoding="utf-8")
    bad = check(rs_ws, sim, reference=r)
    assert bad.valid is False and any("Kdx" in m for m in bad.new_errors)

    # The LTS reference's own baseline errors do not make an unchanged LTS copy invalid.
    assert check(lts_ws, sim, reference=lt).valid is True
