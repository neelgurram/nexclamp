"""Integration tests for neuraxis.simulators.jneuroml against the real jNeuroML jar.

Every failure mode is produced with a real file where that is possible (schema error,
bad reference, missing include, a genuine numerical blow-up). The out-of-bound output
case uses a synthetic .dat read through the real load_dat, because a jLEMS run that
blows up throws before writing output (see docs/build_notes/core.md#jnml-blowup-status).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import numpy as np
import pytest

from neuraxis.models import copy_workspace
from neuraxis.protocols.generate import write_probe
from neuraxis.schemas import AnalysisWindow, ConcreteProtocol, ExecConfig, RunStatus, StimulusComponent, Trace
from neuraxis.simulators import jneuroml as jmod
from neuraxis.simulators.base import PHYSICAL_V_BOUND_MV, OutputSpec
from neuraxis.simulators.jneuroml import JNeuroML, ToolUnavailable, find_jar, find_java, load_dat

RS_OUT = OutputSpec("RS.dat", {"v": 1})


def _shorten_harness(ws, length="200ms", step="0.025ms", name="LEMS_RS_short.xml") -> Path:
    """Tmp copy of the shipped RS harness with a shorter length (and coarser step, to keep the test fast)."""
    text = ws.harness_path.read_text(encoding="utf-8")
    assert 'length="1000.0ms"' in text and 'step="0.001ms"' in text
    out = ws.harness_path.with_name(name)
    out.write_text(text.replace('length="1000.0ms"', f'length="{length}"').replace('step="0.001ms"', f'step="{step}"'),
                   encoding="utf-8")
    return out


def _write_dat(path: Path, t_s: np.ndarray, cols_v: list[np.ndarray]) -> None:
    rows = ["\t".join([repr(float(t))] + [repr(float(c[i])) for c in cols_v]) + "\t" for i, t in enumerate(t_s)]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------ discovery
def test_find_jar_env_override_to_missing_file(monkeypatch, tmp_path):
    monkeypatch.setenv("NEUROSEM_JNML_JAR", str(tmp_path / "missing.jar"))
    assert find_jar() is None


def test_find_jar_env_override_to_existing_file(monkeypatch, tmp_path):
    fake = tmp_path / "jnml.jar"
    fake.write_bytes(b"PK")
    monkeypatch.setenv("NEUROSEM_JNML_JAR", str(fake))
    assert find_jar() == fake


def test_find_java_skips_missing_env_candidate(monkeypatch, tmp_path):
    monkeypatch.setenv("NEUROSEM_JAVA", str(tmp_path / "no_java.exe"))
    j = find_java()
    assert j is None or (j.is_file() and j != tmp_path / "no_java.exe")


def test_find_java_env_candidate_wins(monkeypatch, tmp_path):
    fake = tmp_path / "java.exe"
    fake.write_bytes(b"")
    monkeypatch.setenv("NEUROSEM_JAVA", str(fake))
    assert find_java() == fake


# ---------------------------------------------------------------------------------- tool missing
def test_java_none_is_tool_failure_never_model_failure(rs_ws):
    s = JNeuroML()
    s.java = None                      # the constructor would otherwise auto-discover Java
    assert not s.available()
    v = s.validate([rs_ws.cell_path])
    assert v.valid is None and v.returncode == -1 and "tool unavailable" in v.messages[0]
    r = s.run_lems(rs_ws.harness_path, [RS_OUT])
    assert r.status is RunStatus.TOOL_FAILURE and r.traces == {} and r.returncode == -1
    with pytest.raises(ToolUnavailable, match="Java runtime not found"):
        s.version_info()


def test_jar_none_is_tool_failure(rs_ws):
    s = JNeuroML()
    s.jar = None
    assert s.run_lems(rs_ws.harness_path, [RS_OUT]).status is RunStatus.TOOL_FAILURE
    assert s.validate([rs_ws.cell_path]).valid is None
    with pytest.raises(ToolUnavailable, match="jar not found"):
        s._require()


def test_nonexistent_java_executable_is_tool_failure(rs_ws, tmp_path):
    jar = find_jar()
    if jar is None:
        pytest.skip("jNeuroML jar not installed")
    s = JNeuroML(java=tmp_path / "bin" / "java.exe", jar=jar)
    assert s.available()               # paths are set, but the executable does not exist
    v = s.validate([rs_ws.cell_path])
    assert v.valid is None and "tool failure" in v.messages[0]
    r = s.run_lems(rs_ws.harness_path, [RS_OUT])
    assert r.status is RunStatus.TOOL_FAILURE


# ------------------------------------------------------------------------------------ versions
@pytest.mark.jnml
def test_version_info_matches_audited_versions(sim):
    v = sim.version_info()
    assert v["jneuroml_version"] == "0.14.0" and v["jlems_version"] == "0.12.0"
    assert re.fullmatch(r"[0-9a-f]{64}", v["jar_sha256"])
    assert "21." in v["java_version"]
    assert sim.version_string() == "jNeuroML 0.14.0 / jLEMS 0.12.0"


# ---------------------------------------------------------------------------------- validation
@pytest.mark.jnml
def test_validate_valid_cell(sim, rs_ws):
    r = sim.validate([rs_ws.cell_path])
    assert r.valid is True and r.returncode == 0 and r.messages == []
    assert "All valid" in r.raw_output and r.validator == "jNeuroML -validate"


@pytest.mark.jnml
def test_validate_schema_violation(sim, rs_ws):
    bad = rs_ws.cell_path.with_name("bad_schema.cell.nml")
    bad.write_text(rs_ws.cell_path.read_text().replace('condDensity="5.0 mS_per_cm2"', 'condDensity="5.0 furlongs"'))
    r = sim.validate([bad])
    assert r.valid is False and r.returncode == 1
    assert any("cvc-pattern-valid" in m and "furlongs" in m for m in r.messages)


@pytest.mark.jnml
def test_validate_bad_channel_reference(sim, rs_ws):
    bad = rs_ws.cell_path.with_name("bad_ref.cell.nml")
    bad.write_text(rs_ws.cell_path.read_text().replace('ionChannel="Kd"', 'ionChannel="NoSuchChannel"'))
    r = sim.validate([bad])
    assert r.valid is False and r.returncode == 1
    assert any(m.startswith("Test:") and "failed" in m and "NoSuchChannel" in m for m in r.messages)
    assert "Valid against schema" in r.raw_output            # schema-valid, semantically broken


@pytest.mark.jnml
def test_validate_broken_include_reference(sim, rs_ws):
    bad = rs_ws.cell_path.with_name("bad_include.cell.nml")
    bad.write_text(rs_ws.cell_path.read_text().replace("channels/Kd/Kd.channel.nml", "channels/Kd/NoSuch.channel.nml"))
    r = sim.validate([bad])
    assert r.valid is False and any("Ion channel: Kd" in m for m in r.messages)


@pytest.mark.jnml
def test_validate_malformed_xml(sim, rs_ws):
    bad = rs_ws.cell_path.with_name("truncated.cell.nml")
    text = rs_ws.cell_path.read_text()
    bad.write_text(text[: len(text) // 2])
    r = sim.validate([bad])
    assert r.valid is False and r.returncode == 1


@pytest.mark.jnml
def test_validate_mixed_files_is_invalid(sim, rs_ws):
    bad = rs_ws.cell_path.with_name("bad_ref2.cell.nml")
    bad.write_text(rs_ws.cell_path.read_text().replace('ionChannel="Kd"', 'ionChannel="NoSuchChannel"'))
    r = sim.validate([rs_ws.cell_path, bad])
    assert r.valid is False and "Validated 2 files: 1 passed, 1 failed" in r.raw_output


@pytest.mark.jnml
def test_validate_missing_file_is_not_reported_valid(sim, rs_ws):
    # A missing path is a caller error: the adapter raises instead of recording a tool failure
    # or a model verdict (docs/build_notes/core.md, "Other measured behaviour").
    with pytest.raises(FileNotFoundError):
        sim.validate([rs_ws.cell_path.with_name("does_not_exist.nml")])


# ---------------------------------------------------------------------------------------- runs
@pytest.fixture(scope="module")
def short_run(tmp_path_factory, sim, models):
    from neuraxis.models import materialize

    ws = materialize(models["pospischil2008_rs"], tmp_path_factory.mktemp("rs_short") / "rs")
    lems = _shorten_harness(ws)
    stale = ws.harness_path.parent / "RS.dat"
    stale.write_text("0.0\t99.0\t\n", encoding="utf-8")         # stale output must never be read back
    return ws, lems, sim.run_lems(lems, [RS_OUT], timeout_s=600)


@pytest.mark.jnml
def test_shortened_shipped_harness_runs(short_run):
    _, lems, r = short_run
    assert r.status is RunStatus.OK and r.returncode == 0 and r.message == ""
    assert r.command[-2:] == [lems.name, "-nogui"] and r.runtime_s > 0
    assert "Finished 8000 steps" in r.output_tail or "Written to the file" in r.output_tail


@pytest.mark.jnml
def test_shortened_harness_trace_units_and_grid(short_run):
    _, _, r = short_run
    tr = r.traces["v"]
    assert isinstance(tr, Trace) and set(r.traces) == {"v"}
    assert len(tr.t_ms) == 8001
    assert tr.t_ms[0] == 0.0 and tr.t_ms[-1] == pytest.approx(200.0, abs=1e-9)          # s -> ms
    d = np.diff(tr.t_ms)
    assert np.all(np.abs(d - 0.025) / 0.025 < 1e-6)                                     # uniform grid
    assert tr.v_mV[0] == pytest.approx(-70.0, abs=1e-9)                                 # initMembPotential, V -> mV
    # the shipped 0.75 nA step starts at 300 ms, after this shortened run ends: the cell stays near rest
    assert -75.0 < tr.v_mV.min() and tr.v_mV.max() < -60.0
    assert np.all(np.isfinite(tr.v_mV))


@pytest.mark.jnml
def test_stale_output_is_replaced(short_run):
    ws, _, r = short_run
    assert r.traces["v"].v_mV[0] != 99000.0
    assert (ws.harness_path.parent / "RS.dat").read_text().splitlines()[0].startswith("0.0\t-0.07")


@pytest.mark.jnml
def test_sample_every_ms_strides_real_output(sim, rs_ws):
    lems = _shorten_harness(rs_ws, length="50ms")
    r = sim.run_lems(lems, [RS_OUT], sample_every_ms=0.1)
    tr = r.traces["v"]
    assert r.status is RunStatus.OK and len(tr.t_ms) == 501
    assert np.allclose(np.diff(tr.t_ms), 0.1, rtol=1e-6)


@pytest.mark.jnml
def test_workspace_path_with_spaces(sim, rs_ws, tmp_path):
    ws = copy_workspace(rs_ws, tmp_path / "dir with spaces" / "rs ws")
    lems = _shorten_harness(ws, length="20ms")
    r = sim.run_lems(lems, [RS_OUT])
    assert r.status is RunStatus.OK and len(r.traces["v"].t_ms) == 801


@pytest.mark.jnml
def test_missing_include_is_build_error(sim, rs_ws):
    lems = _shorten_harness(rs_ws)
    lems.write_text(lems.read_text().replace('<Include file="RS.net.nml"/>', '<Include file="NoSuch.net.nml"/>'))
    stale = lems.parent / "RS.dat"
    stale.write_text("0.0\t-0.07\t\n")
    r = sim.run_lems(lems, [RS_OUT])
    assert r.status is RunStatus.BUILD_ERROR and r.returncode != 0
    assert "Can't find file" in r.message and "NoSuch.net.nml" in r.message
    assert r.traces == {}
    assert not stale.exists()                          # deleted before the run, so it cannot masquerade as output


@pytest.mark.jnml
def test_unresolvable_target_is_build_error(sim, rs_ws):
    lems = _shorten_harness(rs_ws)
    lems.write_text(lems.read_text().replace('target="network_PospischilEtAl2008"', 'target="no_such_net"'))
    r = sim.run_lems(lems, [RS_OUT])
    assert r.status is RunStatus.BUILD_ERROR and "No component found: no_such_net" in r.message


@pytest.mark.jnml
def test_missing_output_file_is_runtime_error(sim, rs_ws):
    lems = _shorten_harness(rs_ws, length="10ms")
    r = sim.run_lems(lems, [OutputSpec("not_written.dat", {"v": 1})])
    assert r.status is RunStatus.RUNTIME_ERROR and "output unreadable" in r.message and r.returncode == 0


@pytest.mark.jnml
def test_missing_output_column_is_runtime_error(sim, rs_ws):
    lems = _shorten_harness(rs_ws, length="10ms")
    r = sim.run_lems(lems, [OutputSpec("RS.dat", {"v": 2})])
    assert r.status is RunStatus.RUNTIME_ERROR and "column 2" in r.message


@pytest.mark.jnml
def test_timeout(sim, rs_ws):
    r = sim.run_lems(rs_ws.harness_path, [RS_OUT], timeout_s=0.2)
    assert r.status is RunStatus.TIMEOUT and r.traces == {} and "timeout" in r.message


@pytest.mark.jnml
def test_real_numerical_blowup_is_unstable_not_build_error(sim, rs_ws):
    """100 nA into RS at dt = 0.1 ms: forward integration diverges (jLEMS reports r = Infinity at t = 11.3 ms)."""
    p = [ConcreteProtocol("U1", "step", (StimulusComponent("pulse", 10, 20, 100.0),), 50, AnalysisWindow(10, 30), ())]
    b = write_probe(rs_ws, p, ExecConfig(0.1), tag="blowup")
    r = sim.run_lems(b.lems_file, [b.output])
    assert r.status is RunStatus.UNSTABLE, (r.status, r.message)


@pytest.mark.jnml
def test_moderate_current_at_coarse_dt_is_ok(sim, rs_ws):
    # Control for the blow-up test: 20 nA at dt 0.1 ms stays finite and inside the physical bound.
    p = [ConcreteProtocol("U1", "step", (StimulusComponent("pulse", 10, 20, 20.0),), 50, AnalysisWindow(10, 30), ())]
    b = write_probe(rs_ws, p, ExecConfig(0.1), tag="moderate")
    r = sim.run_lems(b.lems_file, [b.output])
    assert r.status is RunStatus.OK
    assert np.max(np.abs(r.traces["U1"].v_mV)) < PHYSICAL_V_BOUND_MV


# ----------------------------------------------------------------------- load_dat + UNSTABLE rule
def test_load_dat_converts_si_to_ms_mv(tmp_path):
    t = np.arange(0, 11) * 1e-5
    _write_dat(tmp_path / "x.dat", t, [np.full(11, -0.07), np.linspace(-0.07, 0.03, 11)])
    out = load_dat(tmp_path / "x.dat", {"a": 1, "b": 2})
    assert set(out) == {"a", "b"}
    assert np.allclose(out["a"].t_ms, np.arange(0, 11) * 0.01, atol=1e-12)
    assert np.allclose(out["a"].v_mV, -70.0) and np.allclose(out["b"].v_mV, np.linspace(-70, 30, 11))


def test_load_dat_stride_and_errors(tmp_path):
    t = np.arange(0, 101) * 1e-5                    # native 0.01 ms
    _write_dat(tmp_path / "x.dat", t, [np.zeros(101)])
    assert len(load_dat(tmp_path / "x.dat", {"a": 1}, sample_every_ms=0.05)["a"].t_ms) == 21
    assert len(load_dat(tmp_path / "x.dat", {"a": 1}, sample_every_ms=0.001)["a"].t_ms) == 101   # never upsamples
    with pytest.raises(IndexError, match="column 2"):
        load_dat(tmp_path / "x.dat", {"a": 2})
    with pytest.raises(FileNotFoundError):
        load_dat(tmp_path / "missing.dat", {"a": 1})


def test_load_dat_reads_out_of_bound_and_nan_values(tmp_path):
    t = np.arange(0, 5) * 1e-5
    _write_dat(tmp_path / "x.dat", t, [np.array([-0.07, 0.1, 0.3, -0.07, -0.07]),
                                       np.array([-0.07, np.nan, -0.07, -0.07, -0.07])])
    out = load_dat(tmp_path / "x.dat", {"big": 1, "nan": 2})
    assert out["big"].v_mV[2] == pytest.approx(300.0)
    assert np.isnan(out["nan"].v_mV[1])


def _fake_jlems(monkeypatch, columns: list[np.ndarray], dt_s: float = 1e-5):
    """Replace only the subprocess call: write a synthetic OutputFile and report a finished run."""
    def fake_run(cmd, cwd=None, capture_output=True, text=True, timeout=None):
        if "-validate" in cmd:
            raise AssertionError("validation not expected")
        lems = Path(cwd) / cmd[-2]
        name = re.search(r'fileName="([^"]+)"', lems.read_text()).group(1)
        n = len(columns[0])
        _write_dat(Path(cwd) / name, np.arange(n) * dt_s, columns)
        return subprocess.CompletedProcess(cmd, 0, stdout=f"INFO Finished {n - 1} steps\n", stderr="")

    monkeypatch.setattr(jmod.subprocess, "run", fake_run)


def _probe(ws, n: int = 2):
    protos = [ConcreteProtocol(f"S{i}", "step", (StimulusComponent("pulse", 1, 1, 0.1),), 5, AnalysisWindow(1, 2), ())
              for i in range(n)]
    return write_probe(ws, protos, ExecConfig(0.01), tag="synthetic")


@pytest.mark.parametrize("bad_v, status", [
    (10.001, RunStatus.UNSTABLE),         # +10 001 "mV": beyond the blow-up bound
    (-10.001, RunStatus.UNSTABLE),
    (np.nan, RunStatus.UNSTABLE),
    (np.inf, RunStatus.UNSTABLE),
    (10.0, RunStatus.OK),                 # exactly the bound
    (0.3, RunStatus.OK),                  # e.g. a gate variable recorded in a voltage column (x1000): judged behaviourally
    (0.05, RunStatus.OK),
])
def test_unstable_rule_on_synthetic_output(monkeypatch, rs_ws, bad_v, status):
    good = np.full(6, -0.07)
    bad = good.copy()
    bad[3] = bad_v
    _fake_jlems(monkeypatch, [good, bad])
    b = _probe(rs_ws)
    s = JNeuroML(java=Path("java"), jar=Path("jnml.jar"))
    r = s.run_lems(b.lems_file, [b.output])
    assert r.status is status
    assert set(r.traces) == {"S0", "S1"}              # traces are kept even when unstable, for diagnosis
    if status is RunStatus.UNSTABLE:
        assert "S1" in r.message and "out-of-bound" in r.message


def test_unstable_bound_constant():
    assert PHYSICAL_V_BOUND_MV == 10_000.0   # DECISIONS D-021
