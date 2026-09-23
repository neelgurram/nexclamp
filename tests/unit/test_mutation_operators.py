"""Every operator of ARCHITECTURE.md section 3.4 on real model files (RS, LTS, NeuroML2 HH example)."""

from __future__ import annotations

import dataclasses as dc

import pytest

from nexclamp.models import copy_workspace
from nexclamp.mutations import FAMILY_OPERATORS, REGISTRY, MutationError, enforce_single_operator
from nexclamp.mutations.base import (
    Site,
    element_children,
    localname,
    read_xml,
    remove_element,
    resolve,
    scale_quantity,
    shift_quantity,
    snippet,
    write_xml,
)
from nexclamp.mutations.biophysics import ScaleGateTimeConstant
from nexclamp.schemas import Edit, MutationFamily, VariantKind, VariantRecord

BINDING = {
    "stimulus": {"stim_amplitude", "stim_onset", "stim_duration", "sim_length", "record_wrong_variable"},
    "biophysical": {"scale_conductance", "shift_reversal", "scale_capacitance", "scale_gate_time_constant",
                    "shift_initial_voltage", "wrong_segment_group"},
    "reference": {"wrong_channel", "omit_include", "duplicate_conductance", "wrong_compatible_component"},
    "numerical": {"increase_dt", "solver_config", "reduce_spatial_discretization", "recording_resolution"},
    "kinetics": {"shift_gate_midpoint", "scale_gate_slope", "shift_forward_rate_midpoint", "shift_channel_vshift"},
}
RS_MP = "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]"
LEMS_NS = "{http://www.neuroml.org/lems/0.7.2}"


def mutate(ref, tmp_path, site: Site, op=None, tag="var"):
    """Apply one site to a copy of ``ref`` and enforce the single-operator contract."""
    op = op or REGISTRY[site.operator]
    var = copy_workspace(ref, tmp_path / f"{tag}_{site.operator}")
    edits, exec_o, model_o = op.apply(var, site)
    rec = VariantRecord("t", ref.model.model_id, VariantKind.MUTANT, op.family.value, op.name, dict(site.params),
                        edits, exec_o, model_o, tree_sha256=var.tree_sha256(), parent_tree_sha256=ref.tree_sha256())
    enforce_single_operator(ref, var, rec)
    return var, rec


def pick(sites, **match):
    return next(s for s in sites if all(s.params.get(k) == v for k, v in match.items()))


def attr(ws, rel, loc, name):
    return resolve(read_xml(ws.path(rel)).root, loc).get(name)


# --------------------------------------------------------------------------- registry
def test_registry_matches_binding_operator_table():
    assert {f: set(ops) for f, ops in FAMILY_OPERATORS.items()} == BINDING
    for name, op in REGISTRY.items():
        assert op.name == name and isinstance(op.family, MutationFamily)


@pytest.mark.parametrize("fixture", ["rs_ws", "lts_ws", "hh_ws"])
def test_sites_are_deterministic_and_read_only(request, fixture, tmp_path):
    ws = request.getfixturevalue(fixture)
    before = ws.tree_sha256()
    other = copy_workspace(ws, tmp_path / "other")
    for op in REGISTRY.values():
        assert op.sites(ws) == op.sites(ws) == op.sites(other)
        op.inapplicable(ws)
    assert ws.tree_sha256() == before


@pytest.mark.parametrize("fixture", ["rs_ws", "lts_ws", "hh_ws"])
def test_every_site_passes_enforcement(request, fixture, tmp_path):
    ws = request.getfixturevalue(fixture)
    for op in REGISTRY.values():
        for i, site in enumerate(op.sites(ws)):
            mutate(ws, tmp_path, site, tag=f"all{i}")


# --------------------------------------------------------------------------- stimulus
def test_stim_amplitude_edits_harness_network_file(rs_ws, tmp_path):
    site = pick(REGISTRY["stim_amplitude"].sites(rs_ws), factor=0.9)
    assert site.file == "NeuroML2/cells/RS/RS.net.nml"
    var, rec = mutate(rs_ws, tmp_path, site)
    assert attr(var, site.file, site.locator, "amplitude") == "6.75E-10A"
    assert {e.file for e in rec.edits} == {"NeuroML2/cells/RS/RS.net.nml"}


def test_stimulus_of_hh_example_lives_in_cell_file(hh_ws, tmp_path):
    sites = REGISTRY["stim_amplitude"].sites(hh_ws)
    assert {s.file for s in sites} == {"examples/NML2_SingleCompHHCell.nml"}
    var, _ = mutate(hh_ws, tmp_path, pick(sites, factor=0.5))
    assert attr(var, "examples/NML2_SingleCompHHCell.nml", sites[0].locator, "amplitude") == "0.04nA"


def test_stim_onset_and_duration(lts_ws, tmp_path):
    onset = REGISTRY["stim_onset"].sites(lts_ws)
    var, _ = mutate(lts_ws, tmp_path, pick(onset, shift_ms=10.0))
    assert attr(var, onset[0].file, onset[0].locator, "delay") == "410ms"
    dur = REGISTRY["stim_duration"].sites(lts_ws)
    var, _ = mutate(lts_ws, tmp_path, pick(dur, factor=2.0), tag="d")
    assert attr(var, dur[0].file, dur[0].locator, "duration") == "800ms"


def test_stim_onset_skips_negative_delays(models, tmp_path):
    from nexclamp.models import materialize
    wb = materialize(models["wangbuzsaki1996_wb"], tmp_path / "wb")     # delay="0ms"
    assert sorted(s.params["shift_ms"] for s in REGISTRY["stim_onset"].sites(wb)) == [2.0, 10.0, 50.0]


def test_sim_length_on_component_and_simulation_syntax(rs_ws, hh_ws, tmp_path):
    s = pick(REGISTRY["sim_length"].sites(rs_ws), factor=0.5)
    var, _ = mutate(rs_ws, tmp_path, s)
    assert attr(var, s.file, s.locator, "length") == "500.0ms"
    s = pick(REGISTRY["sim_length"].sites(hh_ws), factor=2.0)
    var, _ = mutate(hh_ws, tmp_path, s, tag="hh")
    assert attr(var, s.file, s.locator, "length") == "600ms"


def test_record_wrong_variable_uses_existing_state_paths(rs_ws, lts_ws, tmp_path):
    sites = REGISTRY["record_wrong_variable"].sites(rs_ws)
    quantities = [s.params["new_quantity"] for s in sites]
    assert quantities == [f"CG_RS/0/RS/biophys/membraneProperties/{p}/q"
                          for p in ("Na_all/Na/m", "Na_all/Na/h", "Kd_all/Kd/n", "IM_all/IM/p")]
    _, rec = mutate(rs_ws, tmp_path, sites[0])
    assert rec.edits[0].old == "CG_RS/0/RS/v" and rec.edits[0].attribute == "quantity"
    lts_q = [s.params["new_quantity"] for s in REGISTRY["record_wrong_variable"].sites(lts_ws)]
    assert "CG_LTS/0/LTS/caConc" in lts_q and "CG_LTS/0/LTS/v" not in lts_q


# --------------------------------------------------------------------------- biophysical
def test_scale_conductance_covers_all_channel_density_kinds(rs_ws, lts_ws, tmp_path):
    rs = REGISTRY["scale_conductance"].sites(rs_ws)
    assert len(rs) == 4 * 6 and {s.params["element"] for s in rs} == {"channelDensity", "channelDensityVShift"}
    assert "channelDensityNernst" in {s.params["element"] for s in REGISTRY["scale_conductance"].sites(lts_ws)}
    var, _ = mutate(rs_ws, tmp_path, pick(rs, element_id="Na_all", factor=0.5))
    assert attr(var, "NeuroML2/cells/RS/RS.cell.nml", f"{RS_MP}/channelDensityVShift[@id='Na_all']",
                "condDensity") == "25.0 mS_per_cm2"


def test_shift_reversal_skips_nernst(lts_ws, tmp_path):
    op = REGISTRY["shift_reversal"]
    assert "IT_all" not in {s.params["element_id"] for s in op.sites(lts_ws)}
    assert any("IT_all" in i.locator for i in op.inapplicable(lts_ws))
    var, _ = mutate(lts_ws, tmp_path, pick(op.sites(lts_ws), element_id="Kd_all", shift_mV=-10.0))
    assert var.path("NeuroML2/cells/LTS/LTS.cell.nml").read_text().count('erev="-110.0 mV"') == 1


def test_scale_capacitance_and_initial_voltage(rs_ws, tmp_path):
    var, _ = mutate(rs_ws, tmp_path, pick(REGISTRY["scale_capacitance"].sites(rs_ws), factor=2.0))
    assert attr(var, "NeuroML2/cells/RS/RS.cell.nml", f"{RS_MP}/specificCapacitance[1]", "value") == "2.0 uF_per_cm2"
    var, _ = mutate(rs_ws, tmp_path, pick(REGISTRY["shift_initial_voltage"].sites(rs_ws), shift_mV=5.0), tag="v")
    assert attr(var, "NeuroML2/cells/RS/RS.cell.nml", f"{RS_MP}/initMembPotential[1]", "value") == "-65.0 mV"


def test_wrong_segment_group_inserts_attribute_with_existing_group(rs_ws, tmp_path):
    sites = REGISTRY["wrong_segment_group"].sites(rs_ws)
    assert len(sites) == 8 and {s.params["new_group"] for s in sites} == {"Soma", "soma_group"}
    _, rec = mutate(rs_ws, tmp_path, sites[0])
    assert rec.edits[0].old is None and rec.edits[0].new == "Soma"


def test_scale_gate_time_constant_scales_both_core_rates(hh_ws, tmp_path):
    sites = REGISTRY["scale_gate_time_constant"].sites(hh_ws)
    assert len(sites) == 3 * 4 and {s.params["mechanism"] for s in sites} == {"rate_parameters"}
    site = pick(sites, gate="m", factor=2.0)
    var, rec = mutate(hh_ws, tmp_path, site)
    gate = resolve(read_xml(var.cell_path).root, site.locator)
    rates = {localname(c): c.get("rate") for c in element_children(gate)}
    assert rates == {"forwardRate": "2per_ms", "reverseRate": "8per_ms"}
    assert len(rec.edits) == 2


def test_scale_gate_time_constant_fixed_time_course(hh_ws, tmp_path):
    p = hh_ws.cell_path
    text = p.read_text(encoding="utf-8")
    start = text.index('<gateHHrates id="n"')
    end = text.index("</gateHHrates>", start) + len("</gateHHrates>")
    p.write_text(text[:start] + '<gateHHtauInf id="n" instances="4"><timeCourse type="fixedTimeCourse" tau="5ms"/>'
                 '<steadyState type="HHSigmoidVariable" rate="1" midpoint="-55mV" scale="10mV"/></gateHHtauInf>'
                 + text[end:], encoding="utf-8")
    site = pick(REGISTRY["scale_gate_time_constant"].sites(hh_ws), gate="n", factor=2.0)
    assert site.params["mechanism"] == "time_course_tau"
    _, rec = mutate(hh_ws, tmp_path, site)
    assert (rec.edits[0].old, rec.edits[0].new) == ("5ms", "2.5ms")


def test_scale_gate_time_constant_reports_custom_gates_as_inapplicable(lts_ws, rs_ws):
    op = ScaleGateTimeConstant()                       # contract default: q10 fallback disabled
    assert op.sites(lts_ws) == [] and op.sites(rs_ws) == []
    # The registered operator enables the exact q10Fixed mechanism (DECISIONS D-021), so the pilot has sites.
    assert REGISTRY["scale_gate_time_constant"].allow_q10_fallback and REGISTRY["scale_gate_time_constant"].sites(rs_ws)
    reasons = {i.locator.split("/")[-2] + "/" + i.locator.split("/")[-1]: i.reason for i in op.inapplicable(lts_ws)}
    assert "IT_s_gate" in reasons["ionChannel[@id='IT']/gate[@id='s']"]
    assert "custom LEMS" in reasons["ionChannel[@id='IT']/gate[@id='s']"]
    assert "q10 fallback disabled" in reasons["ionChannel[@id='Na']/gate[@id='m']"]


def test_scale_gate_q10_fallback_inserts_in_schema_order(lts_ws, tmp_path):
    op = ScaleGateTimeConstant(allow_q10_fallback=True)
    sites = op.sites(lts_ws)
    assert {(s.params["channel"], s.params["gate"]) for s in sites} == {("Na", "m"), ("Na", "h"), ("Kd", "n"),
                                                                      ("IM", "p")}
    reasons = [i.reason for i in op.inapplicable(lts_ws)]
    assert any("IT_s_gate" in r for r in reasons) and any("q10ExpTemp" in r for r in reasons)
    site = pick(sites, channel="Na", gate="m", factor=2.0)
    var, rec = mutate(lts_ws, tmp_path, site, op=op)
    gate = resolve(read_xml(var.path(site.file)).root, site.locator)
    kids = element_children(gate)
    assert [localname(c) for c in kids] == ["q10Settings", "forwardRate", "reverseRate"]
    assert (kids[0].get("type"), kids[0].get("fixedQ10")) == ("q10Fixed", "2")
    assert var.path(site.file).read_bytes().startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?>')
    assert rec.edits[0].action == "insert"


# --------------------------------------------------------------------------- reference
def test_channel_swaps_are_partitioned_by_species(rs_ws, tmp_path):
    wrong = REGISTRY["wrong_channel"].sites(rs_ws)
    compat = REGISTRY["wrong_compatible_component"].sites(rs_ws)
    key = lambda s: (s.locator, s.params["changes"][0]["new"])
    assert not {key(s) for s in wrong} & {key(s) for s in compat}
    assert sorted((s.params["element_id"], s.params["changes"][0]["new"]) for s in compat) == [("IM_all", "Kd"),
                                                                                             ("Kd_all", "IM")]
    assert all(s.params["old_species"] != s.params["new_species"] for s in wrong)
    mutate(rs_ws, tmp_path, compat[0])


def test_omit_include(rs_ws, hh_ws, tmp_path):
    sites = REGISTRY["omit_include"].sites(rs_ws)
    assert [s.params["href"] for s in sites] == ["../../channels/Kd/Kd.channel.nml", "../../channels/IM/IM.channel.nml",
                                                "../../channels/Leak/Leak.channel.nml", "../../channels/Na/Na.channel.nml"]
    var, rec = mutate(rs_ws, tmp_path, sites[1])
    assert b"IM.channel.nml" not in var.cell_path.read_bytes() and rec.edits[0].action == "remove"
    assert REGISTRY["omit_include"].sites(hh_ws) == []


def test_duplicate_conductance_inserts_after_original(rs_ws, tmp_path):
    site = pick(REGISTRY["duplicate_conductance"].sites(rs_ws), source_id="Kd_all")
    var, rec = mutate(rs_ws, tmp_path, site)
    mp = resolve(read_xml(var.cell_path).root, RS_MP)
    ids = [c.get("id") for c in element_children(mp) if localname(c).startswith("channelDensity")]
    assert ids == ["LeakConductance_all", "Kd_all", "Kd_all_dup", "IM_all", "Na_all"]
    assert rec.edits[0].locator.endswith("channelDensity[@id='Kd_all_dup']")
    with pytest.raises(MutationError):
        REGISTRY["duplicate_conductance"].apply(var, site)     # id already taken -> stale site


# --------------------------------------------------------------------------- numerical
def test_increase_dt_edits_step_and_sets_override(rs_ws, tmp_path):
    site = pick(REGISTRY["increase_dt"].sites(rs_ws), factor=10)
    var, rec = mutate(rs_ws, tmp_path, site)
    assert attr(var, site.file, site.locator, "step") == "0.01ms"
    assert rec.exec_overrides == {"dt_factor": 10}


@pytest.mark.parametrize("fixture,tag", [("rs_ws", LEMS_NS + "Meta"), ("hh_ws", "Meta")])
def test_solver_config_adds_meta_in_harness_namespace(request, fixture, tag, tmp_path):
    ws = request.getfixturevalue(fixture)
    site = pick(REGISTRY["solver_config"].sites(ws), method="rk4")
    var, rec = mutate(ws, tmp_path, site)
    sim = resolve(read_xml(var.harness_path).root, site.locator)
    meta = element_children(sim)[0]
    assert meta.tag == tag and (meta.get("for"), meta.get("method")) == ("jlems", "rk4")
    assert rec.exec_overrides == {"integrator_method": "rk4"}
    follow_up = REGISTRY["solver_config"].sites(var)          # existing Meta: set method instead of inserting
    assert [(s.params["method"], s.params["mechanism"]) for s in follow_up] == [("eulertree", "set_meta_method")]


def test_recording_resolution_changes_only_exec_overrides(rs_ws, tmp_path):
    site = pick(REGISTRY["recording_resolution"].sites(rs_ws), sample_every_ms=1.0)
    var, rec = mutate(rs_ws, tmp_path, site)
    assert rec.edits == [] and rec.exec_overrides == {"sample_every_ms": 1.0}
    assert var.tree_sha256() == rs_ws.tree_sha256()


def test_exec_override_keys_are_declared_only_by_exec_operators():
    declared = {n: set(op.exec_override_keys) for n, op in REGISTRY.items() if op.exec_override_keys}
    assert declared == {"increase_dt": {"dt_factor"}, "solver_config": {"integrator_method"},
                        "recording_resolution": {"sample_every_ms"}}


# --------------------------------------------------------------------------- operator-specific record checks
def handmade(ref, tmp_path, operator, sets, params, exec_overrides=None, tag="hand"):
    """Apply attribute sets ``(file, locator, attribute, new | old -> new)`` to a copy of ``ref``
    and record them, faithfully, as ONE mutant of ``operator`` with correct tree hashes, so
    only the operator's own record check can reject it."""
    var = copy_workspace(ref, tmp_path / tag)
    edits = []
    for rel, loc, name, new in sets:
        doc = read_xml(var.path(rel))
        el = resolve(doc.root, loc)
        old = el.get(name)
        new = new(old) if callable(new) else new
        el.set(name, new)
        write_xml(doc)
        edits.append(Edit(rel, loc, name, old, new))
    rec = VariantRecord("t", ref.model.model_id, VariantKind.MUTANT, REGISTRY[operator].family.value, operator,
                        dict(params), edits, dict(exec_overrides or {}), {},
                        tree_sha256=var.tree_sha256(), parent_tree_sha256=ref.tree_sha256())
    return var, rec


def _kd(ws):
    return ws.model.cell_file, f"{RS_MP}/channelDensity[@id='Kd_all']"


def _site0(ws, operator):
    s = REGISTRY[operator].sites(ws)[0]
    return s.file, s.locator


def _x(f):
    return lambda old: scale_quantity(old, f)


def _gate_rates(ws):
    s = pick(REGISTRY["scale_gate_time_constant"].sites(ws), gate="m", factor=2.0)
    return [(s.file, c["locator"]) for c in s.params["changes"]]


TAMPERS = {
    # biophysical
    "conductance_and_erev_in_one_element": ("rs_ws", lambda ws: ("scale_conductance", [
        (*_kd(ws), "condDensity", _x(2.0)), (*_kd(ws), "erev", lambda o: shift_quantity(o, 50, "mV"))],
        {"factor": 2.0}, None)),
    "channel_swap_labelled_scale_conductance": ("rs_ws", lambda ws: ("scale_conductance", [
        (*_kd(ws), "ionChannel", "IM")], {"factor": 2.0}, None)),
    "conductance_factor_disagrees_with_params": ("rs_ws", lambda ws: ("scale_conductance", [
        (*_kd(ws), "condDensity", _x(2.0))], {"factor": 0.5}, None)),
    "capacitance_label_on_conductance": ("rs_ws", lambda ws: ("scale_capacitance", [
        (*_kd(ws), "condDensity", _x(2.0))], {"factor": 2.0}, None)),
    "reversal_shift_disagrees_with_params": ("rs_ws", lambda ws: ("shift_reversal", [
        (*_kd(ws), "erev", lambda o: shift_quantity(o, 5, "mV"))], {"shift_mV": 10.0}, None)),
    "initial_voltage_label_on_erev": ("rs_ws", lambda ws: ("shift_initial_voltage", [
        (*_kd(ws), "erev", lambda o: shift_quantity(o, 5, "mV"))], {"shift_mV": 5.0}, None)),
    "segment_group_that_does_not_exist": ("rs_ws", lambda ws: ("wrong_segment_group", [
        (*_kd(ws), "segmentGroup", "nope")], {"new_group": "nope"}, None)),
    "gate_midpoints_shifted": ("hh_ws", lambda ws: ("scale_gate_time_constant", [
        (f, loc, "midpoint", lambda o: shift_quantity(o, 5, "mV")) for f, loc in _gate_rates(ws)],
        {"factor": 2.0, "mechanism": "rate_parameters"}, None)),
    "gate_rates_scaled_by_different_factors": ("hh_ws", lambda ws: ("scale_gate_time_constant", [
        (*_gate_rates(ws)[0], "rate", _x(2.0)), (*_gate_rates(ws)[1], "rate", _x(0.5))],
        {"factor": 2.0, "mechanism": "rate_parameters"}, None)),
    "gate_forward_rate_only": ("hh_ws", lambda ws: ("scale_gate_time_constant", [
        (*_gate_rates(ws)[0], "rate", _x(2.0))], {"factor": 2.0, "mechanism": "rate_parameters"}, None)),
    # reference
    "wrong_channel_with_same_species": ("rs_ws", lambda ws: ("wrong_channel", [
        (*_kd(ws), "ionChannel", "IM")], {}, None)),
    "compatible_component_with_other_species": ("rs_ws", lambda ws: ("wrong_compatible_component", [
        (*_kd(ws), "ionChannel", "Na")], {}, None)),
    # stimulus
    "amplitude_label_on_delay": ("rs_ws", lambda ws: ("stim_amplitude", [
        (*_site0(ws, "stim_amplitude"), "delay", _x(2.0))], {"factor": 2.0}, None)),
    "onset_label_on_amplitude": ("rs_ws", lambda ws: ("stim_onset", [
        (*_site0(ws, "stim_amplitude"), "amplitude", _x(2.0))], {"shift_ms": 2.0}, None)),
    "sim_length_label_on_step": ("rs_ws", lambda ws: ("sim_length", [
        (*_site0(ws, "sim_length"), "step", _x(2.0))], {"factor": 2.0}, None)),
    "record_nonexistent_state_path": ("rs_ws", lambda ws: ("record_wrong_variable", [
        (*_site0(ws, "record_wrong_variable"), "quantity", "CG_RS/0/RS/nope")],
        {"new_quantity": "CG_RS/0/RS/nope"}, None)),
    # numerical
    "increase_dt_that_decreases_dt": ("rs_ws", lambda ws: ("increase_dt", [
        (*_site0(ws, "increase_dt"), "step", _x(0.5))], {"factor": 0.5}, {"dt_factor": 0.5})),
    "increase_dt_on_sim_length": ("rs_ws", lambda ws: ("increase_dt", [
        (*_site0(ws, "sim_length"), "length", _x(2))], {"factor": 2}, {"dt_factor": 2})),
}


@pytest.mark.parametrize("case", sorted(TAMPERS))
def test_record_check_rejects_mislabelled_or_compound_fault(request, case, tmp_path):
    fixture, build = TAMPERS[case]
    ws = request.getfixturevalue(fixture)
    operator, sets, params, exec_o = build(ws)
    var, rec = handmade(ws, tmp_path, operator, sets, params, exec_o)
    with pytest.raises(MutationError, match=operator):
        enforce_single_operator(ws, var, rec)


def test_handmade_faithful_mutant_is_accepted(rs_ws, tmp_path):
    """Positive control for the tamper helper: a correct record of a legitimate fault passes."""
    var, rec = handmade(rs_ws, tmp_path, "scale_conductance", [(*_kd(rs_ws), "condDensity", _x(2.0))],
                        {"factor": 2.0})
    enforce_single_operator(rs_ws, var, rec)


def test_record_check_rejects_removal_of_non_include_labelled_omit_include(rs_ws, tmp_path):
    var = copy_workspace(rs_ws, tmp_path / "var")
    rel, loc = _kd(rs_ws)
    doc = read_xml(var.path(rel))
    el = resolve(doc.root, loc)
    old = snippet(el)
    remove_element(el)
    write_xml(doc)
    rec = VariantRecord("t", rs_ws.model.model_id, VariantKind.MUTANT, "reference", "omit_include",
                        {"href": "../../channels/Kd/Kd.channel.nml"}, [Edit(rel, loc, None, old, None, "remove")],
                        tree_sha256=var.tree_sha256(), parent_tree_sha256=rs_ws.tree_sha256())
    with pytest.raises(MutationError, match="omit_include"):
        enforce_single_operator(rs_ws, var, rec)


def test_record_check_rejects_duplicate_that_is_not_an_exact_copy(rs_ws, tmp_path):
    site = pick(REGISTRY["duplicate_conductance"].sites(rs_ws), source_id="Kd_all")
    var, rec = mutate(rs_ws, tmp_path, site)
    doc = read_xml(var.cell_path)
    dup = resolve(doc.root, rec.edits[0].locator)
    dup.set("condDensity", scale_quantity(dup.get("condDensity"), 2.0))
    write_xml(doc)
    bad = dc.replace(rec, edits=[dc.replace(rec.edits[0], new=snippet(dup))], tree_sha256=var.tree_sha256())
    with pytest.raises(MutationError, match="differs from its source"):
        enforce_single_operator(rs_ws, var, bad)


def test_record_check_rejects_numerical_param_mismatches(rs_ws, tmp_path):
    var, rec = mutate(rs_ws, tmp_path, pick(REGISTRY["solver_config"].sites(rs_ws), method="rk4"))
    with pytest.raises(MutationError, match="solver_config"):
        enforce_single_operator(rs_ws, var, dc.replace(rec, params={**rec.params, "method": "eulertree"}))
    var, rec = mutate(rs_ws, tmp_path, pick(REGISTRY["recording_resolution"].sites(rs_ws), sample_every_ms=1.0),
                      tag="rr")
    with pytest.raises(MutationError, match="recording_resolution"):
        enforce_single_operator(rs_ws, var, dc.replace(rec, exec_overrides={"sample_every_ms": 2.0}))


def test_reduce_spatial_discretization_single_vs_multi_compartment(rs_ws, hh_ws, tmp_path):
    op = REGISTRY["reduce_spatial_discretization"]
    assert op.sites(rs_ws) == [] and [i.reason for i in op.inapplicable(rs_ws)] == ["single-compartment cell"]
    p = hh_ws.cell_path
    text = p.read_text(encoding="utf-8")
    text = text.replace('<segmentGroup id="soma_group">',
                        '<segment id="1" name="dend"><parent segment="0"/><distal x="0" y="100" z="0" diameter="2"/>'
                        '</segment>\n<segmentGroup id="dend_group"><property tag="numberInternalDivisions" value="8"/>'
                        '<member segment="1"/></segmentGroup>\n<segmentGroup id="soma_group">')
    p.write_text(text, encoding="utf-8")
    sites = op.sites(hh_ws)
    assert [(s.params["factor"], s.params["changes"][0]["new"]) for s in sites] == [(2, "4"), (4, "2")]
    mutate(hh_ws, tmp_path, sites[1])
