"""Mutation engine core: XML I/O, locators, quantity arithmetic, semantic diff, enforcement, generation."""

from __future__ import annotations

import csv
import dataclasses as dc
import json
import shutil
import zlib

import numpy as np
import pytest

from neuraxis.models import copy_workspace, materialize
from neuraxis.mutations import (
    REGISTRY,
    MutationError,
    enforce_single_operator,
    generate_mutants,
    load_variant,
    write_manifest,
    xml_changes,
)
from neuraxis.mutations.base import (
    choose_sites,
    format_decimal,
    harness_simulation,
    iter_elements,
    locator,
    read_xml,
    resolve,
    scale_quantity,
    shift_quantity,
    write_xml,
)
from neuraxis.provenance import sha256_file
from neuraxis.schemas import Edit, VariantKind, dumps

RS = "pospischil2008_rs"
IT_FILE = "NeuroML2/channels/IT/IT.channel.nml"
RS_CELL = "NeuroML2/cells/RS/RS.cell.nml"


# --------------------------------------------------------------------------- XML I/O
def test_roundtrip_preserves_iso_8859_1_declaration_and_semantics(lts_ws, tmp_path):
    src = lts_ws.path(IT_FILE)
    orig = src.read_bytes()
    doc = read_xml(src)
    assert doc.encoding.upper() == "ISO-8859-1"
    out = tmp_path / "IT.copy.nml"
    doc.path = out
    write_xml(doc)
    new = out.read_bytes()
    assert new.splitlines()[0] == orig.splitlines()[0] == b'<?xml version="1.0" encoding="ISO-8859-1"?>'
    assert xml_changes(src, out) == []


def test_non_ascii_text_is_written_in_declared_latin1(tmp_path):
    p = tmp_path / "latin.nml"
    p.write_bytes('<?xml version="1.0" encoding="ISO-8859-1"?>\n<neuroml id="x"><notes>café</notes>'
                  '<a id="k" v="1"/></neuroml>\n'.encode("latin-1"))
    before = tmp_path / "before.nml"
    shutil.copy(p, before)
    doc = read_xml(p)
    resolve(doc.root, "/neuroml[@id='x']/a[@id='k']").set("v", "2")
    write_xml(doc)
    raw = p.read_bytes()
    assert b"caf\xe9" in raw and raw.startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?>')
    assert [c["kind"] for c in xml_changes(before, p)] == ["attribute"]


def test_undeclared_utf8_harness_keeps_no_declaration(hh_ws):
    p = hh_ws.harness_path
    doc = read_xml(p)
    write_xml(doc)
    assert p.read_bytes().startswith(b"<Lems>")


# --------------------------------------------------------------------------- locators
@pytest.mark.parametrize("rel_attr", ["cell_path", "harness_path"])
@pytest.mark.parametrize("fixture", ["rs_ws", "hh_ws", "lts_ws"])
def test_every_element_locator_resolves_to_itself(request, fixture, rel_attr):
    ws = request.getfixturevalue(fixture)
    doc = read_xml(getattr(ws, rel_attr))
    locs = []
    for el in iter_elements(doc.root):
        loc = locator(el)
        assert resolve(doc.root, loc) is el
        locs.append(loc)
    assert len(set(locs)) == len(locs)


def test_resolve_rejects_missing_steps(rs_ws):
    root = read_xml(rs_ws.cell_path).root
    with pytest.raises(MutationError):
        resolve(root, "/neuroml[@id='RS']/cell[@id='nope']")
    with pytest.raises(MutationError):
        resolve(root, "/neuroml[@id='RS']/include[99]")


def test_harness_simulation_handles_both_syntaxes(rs_ws, hh_ws):
    assert harness_simulation(read_xml(rs_ws.harness_path).root).get("type") == "Simulation"   # namespaced Component
    sim = harness_simulation(read_xml(hh_ws.harness_path).root)                                # bare <Simulation>
    assert sim.tag == "Simulation" and sim.get("id") == "sim1"


# --------------------------------------------------------------------------- quantities
@pytest.mark.parametrize("text,factor,expected", [
    ("7.5E-10A", 0.9, "6.75E-10A"),
    ("50.0 mS_per_cm2", 0.5, "25.0 mS_per_cm2"),
    ("0.07 mS_per_cm2", 0.9, "0.063 mS_per_cm2"),
    ("1e-5 S_per_cm2", 2.0, "2e-5 S_per_cm2"),
    ("0.001ms", 20, "0.02ms"),
    ("1000.0ms", 1.1, "1100.0ms"),
    ("7.5E-10A", -1.0, "-7.5E-10A"),
])
def test_scale_quantity_is_decimal_exact_and_keeps_style(text, factor, expected):
    assert scale_quantity(text, factor) == expected


@pytest.mark.parametrize("text,delta,unit,expected", [
    ("-70.0 mV", 5, "mV", "-65.0 mV"),
    ("0.3s", 10, "ms", "0.31s"),
    ("400ms", -50, "ms", "350ms"),
    ("-54.3mV", -2, "mV", "-56.3mV"),
])
def test_shift_quantity_in_original_unit(text, delta, unit, expected):
    assert shift_quantity(text, delta, unit) == expected


def test_shift_quantity_rejects_dimension_mismatch():
    with pytest.raises(MutationError):
        shift_quantity("1.0 uF_per_cm2", 5, "mV")


def test_format_decimal_never_emits_plus_exponent():
    from decimal import Decimal
    assert format_decimal(Decimal("2.5E+3"), "1e3") == "2.5e3"


# --------------------------------------------------------------------------- semantic diff
def _pair(tmp_path, a: str, b: str):
    pa, pb = tmp_path / "a.xml", tmp_path / "b.xml"
    pa.write_text(a, encoding="utf-8")
    pb.write_text(b, encoding="utf-8")
    return pa, pb


def test_xml_changes_ignores_whitespace_comments_and_attribute_order(tmp_path):
    a = '<neuroml id="n"><cell id="c" x="1" y="2"><notes>some  text</notes></cell></neuroml>'
    b = '<neuroml  id="n">\n  <!-- hi -->\n  <cell y="2"\n x="1" id="c">\n <notes>some text</notes>\n </cell>\n</neuroml>\n'
    assert xml_changes(*_pair(tmp_path, a, b)) == []


def test_xml_changes_reports_each_kind(tmp_path):
    a = '<r id="r"><i href="a"/><i href="b"/><c id="c" v="1"><notes>x</notes></c></r>'
    b = '<r id="r"><i href="a"/><c id="c" v="2"><notes>y</notes></c><c id="d" v="1"/></r>'
    ch = xml_changes(*_pair(tmp_path, a, b))
    kinds = sorted((c["kind"], c["locator"]) for c in ch)
    assert kinds == [("attribute", "/r[@id='r']/c[@id='c']"), ("insert", "/r[@id='r']/c[@id='d']"),
                     ("remove", "/r[@id='r']/i[2]"), ("text", "/r[@id='r']/c[@id='c']/notes[1]")]


def test_xml_changes_reports_encoding_change(tmp_path):
    pa, pb = tmp_path / "a.xml", tmp_path / "b.xml"
    pa.write_bytes(b'<?xml version="1.0" encoding="ISO-8859-1"?>\n<r/>')
    pb.write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n<r/>')
    assert [c["kind"] for c in xml_changes(pa, pb)] == ["encoding"]


# --------------------------------------------------------------------------- generation
def test_generation_is_deterministic_and_uses_documented_rng(models, rs_ws, tmp_path):
    ops = ["scale_conductance", "shift_reversal", "stim_amplitude"]
    a = generate_mutants(models[RS], ops, 3, 11, tmp_path / "a")
    b = generate_mutants(models[RS], ops, 3, 11, tmp_path / "b")
    assert [r.variant_id for r in a] == [r.variant_id for r in b]
    assert [r.edits for r in a] == [r.edits for r in b]
    for name in ops:
        sites = REGISTRY[name].sites(rs_ws)
        idx = np.random.default_rng([11, zlib.crc32(name.encode())]).choice(len(sites), size=3, replace=False)
        expected = [sites[i] for i in sorted(idx)]
        assert choose_sites(sites, 3, 11, name) == expected
        got = [r for r in a if r.operator == name]
        assert [r.description for r in got] == [REGISTRY[name].describe(s) for s in expected]
    c = generate_mutants(models[RS], ["scale_conductance"], 3, 12, tmp_path / "c")
    assert len(c) == 3        # a different seed is still valid (it may or may not pick different sites)


def test_generation_writes_loadable_variants_and_manifest(models, tmp_path):
    recs = generate_mutants(models[RS], ["scale_capacitance", "increase_dt", "recording_resolution"], 1, 5,
                            tmp_path / "v")
    assert {r.family for r in recs} == {"biophysical", "numerical"}
    for r in recs:
        ws, loaded = load_variant(tmp_path / "v" / RS / r.variant_id, models)
        assert loaded == r and loaded.kind == VariantKind.MUTANT
        assert ws.tree_sha256() == r.tree_sha256
        assert r.params["generator_seed"] == 5
    man = tmp_path / "mutation_manifest.csv"
    write_manifest(recs, man)
    with open(man, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == ["variant_id", "model_id", "family", "operator", "params_json", "edits_json",
                                    "exec_overrides_json", "description", "generator_seed"]
    assert all(r["generator_seed"] == "5" and "generator_seed" not in json.loads(r["params_json"]) for r in rows)
    dt_row = next(r for r in rows if r["operator"] == "increase_dt")
    assert json.loads(dt_row["exec_overrides_json"]) == {"dt_factor": json.loads(dt_row["params_json"])["factor"]}


def test_generate_rejects_unknown_operator(models, tmp_path):
    with pytest.raises(ValueError):
        generate_mutants(models[RS], ["no_such_operator"], 1, 0, tmp_path)


# --------------------------------------------------------------------------- enforcement (tamper tests)
@pytest.fixture
def rs_mutant(models, rs_ws, tmp_path):
    [rec] = generate_mutants(models[RS], ["scale_conductance"], 1, 3, tmp_path / "v")
    ws, rec = load_variant(tmp_path / "v" / RS / rec.variant_id, models)
    return rs_ws, ws, rec


def _set_attr(path, loc, attr, value):
    doc = read_xml(path)
    resolve(doc.root, loc).set(attr, value)
    write_xml(doc)


def test_enforcement_accepts_generated_mutant(rs_mutant):
    ref, var, rec = rs_mutant
    enforce_single_operator(ref, var, rec)


@pytest.mark.parametrize("clear_hash", [False, True])
def test_enforcement_catches_unrecorded_attribute_change_in_edited_file(rs_mutant, clear_hash):
    ref, var, rec = rs_mutant
    loc = "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]"
    _set_attr(var.path(RS_CELL), loc, "value", "-71.0 mV")
    if clear_hash:
        rec = dc.replace(rec, tree_sha256="")   # the semantic diff alone must catch it
    with pytest.raises(MutationError, match="unrecorded change|tree hash"):
        enforce_single_operator(ref, var, rec)


def test_enforcement_catches_change_in_another_file(rs_mutant):
    ref, var, rec = rs_mutant
    p = var.path("NeuroML2/channels/Kd/Kd.channel.nml")
    p.write_bytes(p.read_bytes() + b"   ")     # formatting-only, still an unrecorded change of that file
    with pytest.raises(MutationError, match="unrecorded change to file"):
        enforce_single_operator(ref, var, dc.replace(rec, tree_sha256=""))


def test_enforcement_catches_recorded_edit_that_is_absent(rs_mutant):
    ref, var, rec = rs_mutant
    shutil.copy(ref.path(RS_CELL), var.path(RS_CELL))
    with pytest.raises(MutationError, match="not present"):
        enforce_single_operator(ref, var, dc.replace(rec, tree_sha256=""))


def test_enforcement_catches_misrecorded_value(rs_mutant):
    ref, var, rec = rs_mutant
    e = rec.edits[0]
    wrong = dc.replace(e, new=e.new + " ")
    with pytest.raises(MutationError):
        enforce_single_operator(ref, var, dc.replace(rec, edits=[wrong], tree_sha256=""))


def test_enforcement_rejects_edits_in_two_elements(models, rs_ws, tmp_path):
    var = copy_workspace(rs_ws, tmp_path / "two")
    mp = "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]"
    edits = []
    for cid, new in (("Kd_all", "2.5 mS_per_cm2"), ("IM_all", "0.035 mS_per_cm2")):
        loc = f"{mp}/channelDensity[@id='{cid}']"
        old = resolve(read_xml(var.cell_path).root, loc).get("condDensity")
        _set_attr(var.cell_path, loc, "condDensity", new)
        edits.append(Edit(RS_CELL, loc, "condDensity", old, new))
    rec = dc.replace(_record(var, "scale_conductance", "biophysical"), edits=edits)
    with pytest.raises(MutationError, match="one target element"):
        enforce_single_operator(rs_ws, var, rec)


def _record(ws, operator, family, **kw):
    from neuraxis.schemas import VariantRecord
    return VariantRecord(variant_id="t", model_id=ws.model.model_id, kind=VariantKind.MUTANT, family=family,
                         operator=operator, **kw)


def test_enforcement_rejects_added_or_removed_files(rs_mutant):
    ref, var, rec = rs_mutant
    extra = var.path("NeuroML2/cells/RS/RS.dat")
    extra.write_text("0 0\n")
    with pytest.raises(MutationError, match="additions"):
        enforce_single_operator(ref, var, rec)
    enforce_single_operator(ref, var, rec, ignore_patterns=["*.dat"])   # explicit exemption for sim outputs
    extra.unlink()
    var.path("NeuroML2/channels/Leak/Leak.channel.nml").unlink()
    with pytest.raises(MutationError, match="removals"):
        enforce_single_operator(ref, var, rec)


def test_enforcement_hash_catches_comment_only_tampering(rs_mutant):
    ref, var, rec = rs_mutant
    p = var.path(RS_CELL)
    p.write_bytes(p.read_bytes().replace(b"<cell id=", b"<!-- tamper --><cell id=", 1))
    with pytest.raises(MutationError, match="tree hash"):
        enforce_single_operator(ref, var, rec)


def test_enforcement_record_level_checks(rs_mutant, rs_ws, tmp_path):
    ref, var, rec = rs_mutant
    with pytest.raises(MutationError, match="unknown exec_overrides"):
        enforce_single_operator(ref, var, dc.replace(rec, exec_overrides={"solver": "x"}))
    with pytest.raises(MutationError, match="family"):
        enforce_single_operator(ref, var, dc.replace(rec, family="numerical"))
    with pytest.raises(MutationError, match="model mismatch"):
        enforce_single_operator(ref, var, dc.replace(rec, model_id="other"))
    clean = copy_workspace(rs_ws, tmp_path / "clean")
    with pytest.raises(MutationError, match="no change"):
        enforce_single_operator(rs_ws, clean, _record(clean, "scale_conductance", "biophysical"))


def test_enforcement_checks_increase_dt_consistency(models, rs_ws, tmp_path):
    [rec] = generate_mutants(models[RS], ["increase_dt"], 1, 1, tmp_path / "v")
    ws, rec = load_variant(tmp_path / "v" / RS / rec.variant_id, models)
    enforce_single_operator(rs_ws, ws, rec)
    bad = dc.replace(rec, exec_overrides={"dt_factor": rec.exec_overrides["dt_factor"] * 2})
    with pytest.raises(MutationError, match="dt_factor"):
        enforce_single_operator(rs_ws, ws, bad)


@pytest.mark.parametrize("extra", [
    {"exec_overrides": {"dt_factor": 20}},
    {"exec_overrides": {"sample_every_ms": 2.0}},
    {"model_overrides": {"harness_v_column": "2"}},
], ids=["dt_factor", "sample_every_ms", "model_override"])
def test_enforcement_rejects_second_fault_carried_by_overrides(rs_mutant, extra):
    """A file mutant plus any override is two faults; enforcement must refuse it."""
    ref, var, rec = rs_mutant
    with pytest.raises(MutationError, match="exec_overrides|model_overrides"):
        enforce_single_operator(ref, var, dc.replace(rec, **extra))


@pytest.mark.parametrize("operator,family,kw", [
    ("scale_conductance", "biophysical", {"model_overrides": {"cell_id": "NOPE"}}),
    ("scale_conductance", "biophysical", {"exec_overrides": {"dt_factor": 50}}),
    ("increase_dt", "numerical", {"exec_overrides": {"dt_factor": 50}, "params": {"factor": 50}}),
], ids=["model_override_only", "exec_only_mislabelled", "increase_dt_without_harness_edit"])
def test_enforcement_rejects_override_only_mutants(rs_ws, tmp_path, operator, family, kw):
    clean = copy_workspace(rs_ws, tmp_path / "clean")
    with pytest.raises(MutationError):
        enforce_single_operator(rs_ws, clean, _record(clean, operator, family, **kw))


@pytest.mark.parametrize("operator,extra", [("solver_config", {"dt_factor": 20}),
                                            ("increase_dt", {"sample_every_ms": 2.0})])
def test_enforcement_rejects_extra_exec_override_on_numerical_mutant(models, rs_ws, tmp_path, operator, extra):
    [rec] = generate_mutants(models[RS], [operator], 1, 4, tmp_path / "v")
    ws, rec = load_variant(tmp_path / "v" / RS / rec.variant_id, models)
    enforce_single_operator(rs_ws, ws, rec)
    with pytest.raises(MutationError, match="exec_overrides"):
        enforce_single_operator(rs_ws, ws, dc.replace(rec, exec_overrides={**rec.exec_overrides, **extra}))


def test_enforcement_rejects_params_changes_that_disagree_with_edits(rs_mutant):
    ref, var, rec = rs_mutant
    changes = [dict(c, new="999.0 mS_per_cm2") for c in rec.params["changes"]]
    with pytest.raises(MutationError, match="params.changes"):
        enforce_single_operator(ref, var, dc.replace(rec, params={**rec.params, "changes": changes}))


def test_load_variant_refuses_mutant_with_model_overrides(rs_mutant, models):
    _, var, rec = rs_mutant
    (var.root / "variant.json").write_text(dumps(dc.replace(rec, model_overrides={"cell_id": "NOPE"})),
                                           encoding="utf-8")
    with pytest.raises(MutationError, match="model_overrides"):
        load_variant(var.root, models)


def test_ignore_patterns_exempt_only_files_absent_from_reference(rs_ws, tmp_path):
    """Snapshot files matching a pattern are still hash-compared, and the recorded hashes
    (computed over the reference file set) still match when ignored outputs are added."""
    ref = copy_workspace(rs_ws, tmp_path / "ref")
    keep = "NeuroML2/keep.dat"
    ref.path(keep).write_text("1 2\n")
    op = REGISTRY["scale_conductance"]
    site = op.sites(ref)[0]
    var = copy_workspace(ref, tmp_path / "var")
    edits, _, _ = op.apply(var, site)
    rec = _record(var, op.name, op.family.value, params=dict(site.params), edits=edits,
                  tree_sha256=var.tree_sha256(), parent_tree_sha256=ref.tree_sha256())
    enforce_single_operator(ref, var, rec, ignore_patterns=["*.dat"])
    var.path("NeuroML2/cells/RS/out.dat").write_text("0 0\n")              # simulator output written later
    enforce_single_operator(ref, var, rec, ignore_patterns=["*.dat"])
    var.path(keep).write_text("9 9\n")                                     # but a snapshot .dat may not change
    with pytest.raises(MutationError, match="unrecorded change to file"):
        enforce_single_operator(ref, var, dc.replace(rec, tree_sha256=""), ignore_patterns=["*.dat"])
    with pytest.raises(MutationError, match="tree hash|unrecorded change"):
        enforce_single_operator(ref, var, rec, ignore_patterns=["*.dat"])


def test_generate_mutants_deduplicates_repeated_operators(models, tmp_path):
    recs = generate_mutants(models[RS], ["scale_capacitance", "scale_capacitance"], 2, 1, tmp_path / "v")
    ids = [r.variant_id for r in recs]
    assert len(ids) == 2 and len(set(ids)) == 2


def test_enforcement_accepts_exec_only_record_with_unchanged_tree(models, rs_ws, tmp_path):
    [rec] = generate_mutants(models[RS], ["recording_resolution"], 1, 2, tmp_path / "v")
    ws, rec = load_variant(tmp_path / "v" / RS / rec.variant_id, models)
    assert rec.edits == [] and ws.tree_sha256() == rs_ws.tree_sha256()
    enforce_single_operator(rs_ws, ws, rec)
    assert sha256_file(ws.cell_path) == sha256_file(rs_ws.cell_path)
    materialize(models[RS], tmp_path / "unused")    # snapshot is still intact
