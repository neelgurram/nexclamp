"""Tests for nexclamp.protocols.generate: probe network / LEMS XML, probe bundles and harness parsing.

Generated networks are checked two ways without Java: structurally with lxml, and
against NeuroML_v2.3.1.xsd shipped inside the installed libNeuroML (the schema version
the generated files declare). jnml -validate of a generated file runs in
tests/integration/test_probe_battery.py.
"""

from __future__ import annotations

import dataclasses as dc
from pathlib import Path

import pytest
from lxml import etree

from nexclamp.models import load_models, snapshot_dir
from nexclamp.protocols.definitions import DEFAULT_TEMPLATES, batched
from nexclamp.protocols.generate import (
    DEFAULT_SEED,
    PROBE_NET_ID,
    PROBE_SIM_ID,
    ProbeBundle,
    canonical_output,
    group_by_length,
    harness_step_and_length,
    lems_xml,
    network_xml,
    population_id,
    write_probe,
)
from nexclamp.schemas import AnalysisWindow, ConcreteProtocol, ExecConfig, StimulusComponent
from nexclamp.simulators.base import OutputSpec
from nexclamp.units import parse

NML = "{http://www.neuroml.org/schema/neuroml2}"
MODELS = load_models()
RS = MODELS["pospischil2008_rs"]
HH = MODELS["nml2_hh_example"]
BATTERY = [t.instantiate(0.1, 300) for t in batched(DEFAULT_TEMPLATES)]


@pytest.fixture(scope="module")
def schema() -> etree.XMLSchema:
    import neuroml

    return etree.XMLSchema(etree.parse(str(Path(neuroml.__file__).parent / "nml" / "NeuroML_v2.3.1.xsd")))


def _proto(pid: str, *comps: StimulusComponent, total: float = 100.0) -> ConcreteProtocol:
    return ConcreteProtocol(pid, "step", tuple(comps), total, AnalysisWindow(10.0, 60.0), ())


def _pulse(delay=10.0, dur=50.0, amp=0.2) -> StimulusComponent:
    return StimulusComponent("pulse", delay, dur, amp)


def _parse(text: str) -> etree._Element:
    return etree.fromstring(text.encode("utf-8"))


def _q(value: str, unit: str) -> float:
    q = parse(value)
    assert q.unit == unit, value
    return q.value


# ------------------------------------------------------------------------------------ population ids
def test_population_id():
    assert population_id("P01_baseline") == "ns_P01_baseline"
    assert population_id("R00") == "ns_R00"


@pytest.mark.parametrize("bad", ["P-01", "P 01", "P01.x", "Pé", ""])
def test_population_id_rejects_non_nml_ids(bad):
    if bad == "":
        assert population_id(bad) == "ns_"      # the prefix alone is still a valid NmlId
        return
    with pytest.raises(ValueError, match="not a valid NeuroML id"):
        population_id(bad)


# ------------------------------------------------------------------------------------- network xml
def test_network_structure_for_full_battery():
    root = _parse(network_xml(RS, "RS.cell.nml", BATTERY))
    assert root.tag == f"{NML}neuroml" and root.get("id") == "ns_probe"
    assert [i.get("href") for i in root.findall(f"{NML}include")] == ["RS.cell.nml"]
    net = root.find(f"{NML}network")
    assert net.get("id") == PROBE_NET_ID
    assert net.get("type") == "networkWithTemperature" and net.get("temperature") == "36.0 degC"
    pops = net.findall(f"{NML}population")
    assert [p.get("id") for p in pops] == [population_id(p.protocol_id) for p in BATTERY]
    for p in pops:
        assert p.get("component") == "RS" and p.get("size") == "1" and p.get("type") == "populationList"
        (inst,) = p.findall(f"{NML}instance")
        assert inst.get("id") == "0" and inst.find(f"{NML}location") is not None


def test_network_inputs_match_components_exactly():
    root = _parse(network_xml(RS, "RS.cell.nml", BATTERY))
    gens = {g.get("id"): g for tag in ("pulseGenerator", "rampGenerator") for g in root.findall(f"{NML}{tag}")}
    assert len(gens) == sum(len(p.components) for p in BATTERY)
    lists = root.find(f"{NML}network").findall(f"{NML}inputList")
    assert len(lists) == len(gens)
    for p in BATTERY:
        pop = population_id(p.protocol_id)
        for i, c in enumerate(p.components):
            cid = f"{pop}_c{i}"
            g = gens[cid]
            assert g.tag == f"{NML}{'pulseGenerator' if c.kind == 'pulse' else 'rampGenerator'}"
            assert _q(g.get("delay"), "ms") == c.delay_ms and _q(g.get("duration"), "ms") == c.duration_ms
            if c.kind == "pulse":
                assert _q(g.get("amplitude"), "nA") == c.amplitude_nA           # exact: format_number round-trips
            else:
                assert _q(g.get("startAmplitude"), "nA") == c.start_nA
                assert _q(g.get("finishAmplitude"), "nA") == c.finish_nA
                assert _q(g.get("baselineAmplitude"), "nA") == c.baseline_nA
            (il,) = [x for x in lists if x.get("component") == cid]
            assert il.get("id") == f"{cid}_in" and il.get("population") == pop
            (inp,) = il.findall(f"{NML}input")
            assert inp.get("target") == f"../{pop}/0/RS" and inp.get("destination") == "synapses"


def test_paired_pulse_gets_two_generators_on_one_population():
    p10 = next(p for p in BATTERY if p.protocol_id == "P10_paired_pulses")
    root = _parse(network_xml(RS, "RS.cell.nml", [p10]))
    lists = root.find(f"{NML}network").findall(f"{NML}inputList")
    assert [x.get("population") for x in lists] == ["ns_P10_paired_pulses"] * 2
    assert [_q(g.get("delay"), "ms") for g in root.findall(f"{NML}pulseGenerator")] == [300.0, 323.0]


def test_network_without_temperature_is_plain_network():
    root = _parse(network_xml(HH, "NML2_SingleCompHHCell.nml", BATTERY[:2]))
    net = root.find(f"{NML}network")
    assert net.get("type") is None and net.get("temperature") is None
    assert root.find(f"{NML}network/{NML}population").get("component") == "hhcell"


def test_include_href_is_attribute_escaped():
    root = _parse(network_xml(RS, 'odd "name" & <x>.nml', BATTERY[:1]))
    assert root.find(f"{NML}include").get("href") == 'odd "name" & <x>.nml'


def test_generated_values_never_use_plus_exponent():
    comps = (_pulse(10.0, 50.0, 1e16), _pulse(60.0, 1.0, 1e-7))
    text = network_xml(RS, "RS.cell.nml", [_proto("PX", *comps)])
    assert "e+" not in text and 'amplitude="1e16nA"' in text and 'amplitude="1e-7nA"' in text


def test_unsupported_component_kind_raises():
    with pytest.raises(ValueError, match="unsupported stimulus component kind 'sine'"):
        network_xml(RS, "RS.cell.nml", [_proto("PX", StimulusComponent("sine", 1.0, 2.0))])


def test_pulse_only_network_is_schema_valid(schema):
    pulses = [p for p in BATTERY if all(c.kind == "pulse" for c in p.components)]
    for model, include in ((RS, "RS.cell.nml"), (HH, "NML2_SingleCompHHCell.nml")):
        doc = _parse(network_xml(model, include, pulses))
        assert schema.validate(doc), [str(e) for e in schema.error_log]


def test_single_ramp_network_is_schema_valid(schema):
    ramp = [p for p in BATTERY if p.kind == "ramp"]
    doc = _parse(network_xml(RS, "RS.cell.nml", ramp))
    assert schema.validate(doc), [str(e) for e in schema.error_log]


def test_extreme_formatted_values_are_schema_valid(schema):
    comps = (_pulse(1e-5, 1e16, 1e-7), _pulse(0.00125, 0.1, -2.5e-10), _pulse(3.0, 5e-324, 0.15000000000000002))
    doc = _parse(network_xml(RS, "RS.cell.nml", [_proto("PX", *comps)]))
    assert schema.validate(doc), [str(e) for e in schema.error_log]


def test_full_battery_network_is_schema_valid(schema):
    """NeuroMLDocument is an xs:sequence: every pulseGenerator must precede every rampGenerator."""
    doc = _parse(network_xml(RS, "RS.cell.nml", BATTERY))
    assert schema.validate(doc), [str(e) for e in schema.error_log][:2]


def test_ramp_before_pulse_order_is_schema_valid(schema):
    ramp = next(p for p in BATTERY if p.kind == "ramp")
    step = next(p for p in BATTERY if p.protocol_id == "P04_step_2x")
    doc = _parse(network_xml(RS, "RS.cell.nml", [ramp, step]))
    assert schema.validate(doc), [str(e) for e in schema.error_log][:2]


# ---------------------------------------------------------------------------------------- lems xml
def test_lems_structure():
    text = lems_xml(RS, "ns_probe.net.nml", BATTERY, ExecConfig(0.005), "ns_probe_v.dat", 2500.0)
    root = _parse(text)
    assert root.tag == "Lems"
    assert root.find("Target").get("component") == PROBE_SIM_ID
    assert [i.get("file") for i in root.findall("Include")] == ["Cells.xml", "Networks.xml", "Simulation.xml",
                                                                "ns_probe.net.nml"]
    sim = root.find("Simulation")
    assert sim.get("id") == PROBE_SIM_ID and sim.get("target") == PROBE_NET_ID
    assert sim.get("length") == "2500.0ms" and sim.get("step") == "0.005ms" and sim.get("seed") == str(DEFAULT_SEED)
    assert sim.find("Meta") is None
    (of,) = sim.findall("OutputFile")
    assert of.get("fileName") == "ns_probe_v.dat"
    cols = of.findall("OutputColumn")
    assert [c.get("id") for c in cols] == [f"{population_id(p.protocol_id)}_v" for p in BATTERY]
    assert [c.get("quantity") for c in cols] == [f"{population_id(p.protocol_id)}/0/RS/v" for p in BATTERY]


def test_lems_meta_only_when_integrator_requested():
    text = lems_xml(RS, "n.nml", BATTERY[:1], ExecConfig(0.025, integrator_method="rk4"), "o.dat", 100.0, seed=7)
    sim = _parse(text).find("Simulation")
    (meta,) = sim.findall("Meta")
    assert meta.get("for") == "jlems" and meta.get("method") == "rk4"
    assert sim.get("seed") == "7"
    assert list(sim).index(meta) == 0                                  # Meta precedes the OutputFile


@pytest.mark.parametrize("dt, expected", [(0.005, "0.005ms"), (0.0025, "0.0025ms"), (0.00125, "0.00125ms"),
                                          (0.025, "0.025ms"), (1e-5, "1e-5ms")])
def test_lems_step_formatting_for_refinement_levels(dt, expected):
    sim = _parse(lems_xml(RS, "n.nml", BATTERY[:1], ExecConfig(dt), "o.dat", 1000)).find("Simulation")
    assert sim.get("step") == expected and sim.get("length") == "1000.0ms"      # ints are written as floats
    assert _q(sim.get("step"), "ms") == dt


# ------------------------------------------------------------------------------------- write_probe
def test_write_probe_bundle(rs_ws):
    protos = [p for p in BATTERY if p.total_ms == 1000.0] + [next(p for p in BATTERY if p.total_ms == 2500.0)]
    b = write_probe(rs_ws, protos, ExecConfig(0.025), tag="battery 1/x")
    assert isinstance(b, ProbeBundle)
    cell_dir = rs_ws.cell_path.parent
    assert b.net_file == cell_dir / "ns_battery_1_x.net.nml" and b.net_file.is_file()
    assert b.lems_file == cell_dir / "LEMS_ns_battery_1_x.xml" and b.lems_file.is_file()
    assert b.output == OutputSpec("ns_battery_1_x_v.dat", {p.protocol_id: i + 1 for i, p in enumerate(protos)})
    assert b.length_ms == 2500.0 and b.protocol_ids == tuple(p.protocol_id for p in protos)
    assert b.cell_steps == 100_000 * len(protos)
    lems = _parse(b.lems_file.read_text(encoding="utf-8"))
    assert lems.findall("Include")[-1].get("file") == "ns_battery_1_x.net.nml"
    assert lems.find("Simulation").get("length") == "2500.0ms"
    assert lems.find("Simulation/OutputFile").get("fileName") == b.output.file
    net = _parse(b.net_file.read_text(encoding="utf-8"))
    assert net.find(f"{NML}include").get("href") == "RS.cell.nml"


def test_write_probe_rewrites_same_tag(rs_ws):
    b1 = write_probe(rs_ws, BATTERY[:1], ExecConfig(0.025), tag="t")
    b2 = write_probe(rs_ws, BATTERY[1:3], ExecConfig(0.025), tag="t")
    assert b1.lems_file == b2.lems_file
    assert "ns_P02_weak_step" in b2.net_file.read_text() and "ns_P01_baseline" not in b2.net_file.read_text()


def test_write_probe_cell_steps_rounding(rs_ws):
    b = write_probe(rs_ws, [_proto("PX", _pulse(), total=100.0)], ExecConfig(0.0125))
    assert b.cell_steps == 8000


def test_write_probe_rejects_empty_and_duplicates(rs_ws):
    with pytest.raises(ValueError, match="no protocols"):
        write_probe(rs_ws, [], ExecConfig(0.025))
    with pytest.raises(ValueError, match="duplicate protocol ids"):
        write_probe(rs_ws, [BATTERY[0], BATTERY[0]], ExecConfig(0.025))


def test_write_probe_changes_workspace_tree_hash(rs_ws):
    """Probe files live inside the workspace, so hash a variant's tree before generating probes."""
    before = rs_ws.tree_sha256()
    write_probe(rs_ws, BATTERY[:1], ExecConfig(0.025))
    assert rs_ws.tree_sha256() != before


# ---------------------------------------------------------------------------------------- grouping
def test_group_by_length_sorted_and_stable():
    groups = group_by_length(BATTERY)
    assert [g[0].total_ms for g in groups] == [500.0, 1000.0, 1100.0, 1500.0, 2500.0]
    assert [[p.protocol_id for p in g] for g in groups] == [
        ["P09_short_pulse", "P10_paired_pulses"],
        ["P01_baseline", "P02_weak_step", "P04_step_2x", "P07_hyperpolarizing_step"],
        ["P08_rebound"], ["P06_ramp"], ["P05_long_step"]]
    assert sorted(p.protocol_id for g in groups for p in g) == sorted(p.protocol_id for p in BATTERY)
    assert group_by_length([]) == []


# ---------------------------------------------------------------------------------- harness parsing
def test_canonical_output():
    assert canonical_output(RS) == OutputSpec("RS.dat", {"P00_canonical": 1})
    assert canonical_output(HH) == OutputSpec("results/ex5_v.dat", {"P00_canonical": 1})


EXPECTED_HARNESS = {
    "pospischil2008_rs": ("0.001ms", "1000.0ms"), "pospischil2008_lts": ("0.001ms", "1000.0ms"),
    "nml2_hh_example": ("0.01ms", "300ms"), "wangbuzsaki1996_wb": ("0.001ms", "100ms"),
}


@pytest.mark.parametrize("model_id", sorted(MODELS))
def test_harness_step_and_length_on_shipped_harnesses(model_id):
    m = MODELS[model_id]
    text = (snapshot_dir(m) / m.harness_lems).read_text(encoding="utf-8")
    step, length = harness_step_and_length(text)
    assert parse(step).dimension == "time" and parse(length).dimension == "time"
    assert 0 < parse(step).si < parse(length).si
    if model_id in EXPECTED_HARNESS:
        assert (step, length) == EXPECTED_HARNESS[model_id]


def test_harness_parsing_attribute_order_and_newlines():
    text = '<Lems>\n  <Simulation id="s"\n     length="250ms"\n     target="n" step="0.02ms">\n</Simulation></Lems>'
    assert harness_step_and_length(text) == ("0.02ms", "250ms")


def test_harness_parsing_ignores_attributes_of_other_elements():
    text = ('<Lems><Display id="d" timeScale="1ms" step="9ms" length="9ms"/>'
            '<Component type="Simulation" id="s" length="5ms" step="0.5ms"/></Lems>')
    assert harness_step_and_length(text) == ("0.5ms", "5ms")


def test_harness_parsing_requires_both():
    with pytest.raises(ValueError, match="could not find Simulation step/length"):
        harness_step_and_length('<Lems><Simulation id="s" length="5ms"/></Lems>')


def test_probe_bundle_is_frozen():
    b = ProbeBundle(Path("a"), Path("b"), OutputSpec("o", {}), 1.0, (), 0)
    with pytest.raises(dc.FrozenInstanceError):
        b.length_ms = 2.0
