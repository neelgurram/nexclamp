"""Unit tests for neuraxis.transforms on the real pinned NeuroML snapshots (no Java needed).

Checks that matter scientifically are done with code that does not reuse the module under
test: semantic comparisons parse files with lxml directly, exact SI values are recomputed
with Decimal from the unit definitions, and allowed units are read from the XSD pattern.
"""

from __future__ import annotations

import dataclasses as dc
import json
import re
from collections import Counter
from decimal import Decimal
from pathlib import Path

import pytest
from lxml import etree

from neuraxis.models import materialize
from neuraxis.provenance import tree_manifest
from neuraxis.schemas import VariantKind, variant_from_dict
from neuraxis.transforms import (
    MANIFEST_COLUMNS,
    REGISTRY,
    apply_model_overrides,
    generate_transforms,
    write_manifest,
)
from neuraxis.transforms.formatting import XmlDoc, model_files, scan
from neuraxis.transforms.identifiers import rewrite_path
from neuraxis.transforms.units import (
    convert_literal,
    core_units,
    format_decimal,
    si_value,
    xsd_index,
    xsd_path,
)

NML = "{http://www.neuroml.org/schema/neuroml2}"
EXPECTED_OPERATORS = {"unit_conversion", "xml_formatting", "add_comments", "numeric_literal_format",
                      "rename_identifier", "factor_file", "reorder_independent", "explicit_default"}


# ------------------------------------------------------------------ independent helpers

def canonical(path: Path) -> list[tuple]:
    """Semantic content of an XML file: elements in order with sorted attributes and stripped text.

    Comments, processing instructions, insignificant whitespace and attribute order are ignored.
    """
    root = etree.parse(str(path), etree.XMLParser(remove_comments=True, remove_pis=True)).getroot()
    out = []
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        out.append((el.tag, tuple(sorted(el.attrib.items())), (el.text or "").strip(), (el.tail or "").strip()))
    return out


def attr_changes(before: Path, after: Path) -> list[tuple[int, str, str | None, str | None]]:
    """Attribute differences between two structurally identical XML files."""
    a = [e for e in etree.parse(str(before)).getroot().iter() if isinstance(e.tag, str)]
    b = [e for e in etree.parse(str(after)).getroot().iter() if isinstance(e.tag, str)]
    assert [e.tag for e in a] == [e.tag for e in b], "element structure changed"
    out = []
    for i, (x, y) in enumerate(zip(a, b)):
        for k in sorted(set(x.attrib) | set(y.attrib)):
            if x.get(k) != y.get(k):
                out.append((i, k, x.get(k), y.get(k)))
    return out


def changed_files(ref_root: Path, var_root: Path) -> list[str]:
    ref, var = tree_manifest(ref_root), tree_manifest(var_root)
    return sorted(f for f in set(ref) | set(var) if ref.get(f) != var.get(f))


def includes_closure(root: Path, start: str) -> set[str]:
    """Independent include resolver (NeuroML include/@href and LEMS Include/@file)."""
    seen: set[str] = set()
    todo = [start]
    while todo:
        rel = todo.pop()
        if rel in seen:
            continue
        seen.add(rel)
        tree = etree.parse(str(root / rel)).getroot()
        for el in tree.iter():
            if not isinstance(el.tag, str):
                continue
            local = etree.QName(el).localname
            ref = el.get("href") if local == "include" and el.getparent() is tree else (
                el.get("file") if local == "Include" else None)
            if ref:
                target = (root / rel).parent / ref
                if target.is_file():
                    todo.append(target.resolve().relative_to(root.resolve()).as_posix())
    return seen


def definitions(root: Path, files: set[str], tag_local: str, ident: str) -> int:
    n = 0
    for rel in files:
        for el in etree.parse(str(root / rel)).getroot().iter():
            if isinstance(el.tag, str) and etree.QName(el).localname == tag_local and \
                    (el.get("id") == ident or el.get("name") == ident):
                n += 1
    return n


@pytest.fixture
def workspaces(rs_ws, lts_ws, hh_ws):
    return {"rs": rs_ws, "lts": lts_ws, "hh": hh_ws}


def fresh(ws, tmp_path, name):
    return materialize(ws.model, tmp_path / name)


# ------------------------------------------------------------------------- registry

def test_registry_has_exactly_the_binding_names():
    assert set(REGISTRY) == EXPECTED_OPERATORS
    for name, op in REGISTRY.items():
        assert op.name == name
        expected = VariantKind.NO_CHANGE if name in ("xml_formatting", "add_comments") else VariantKind.VALID_TRANSFORM
        assert op.kind == expected


# ------------------------------------------------------------------------ scanning

def test_scanner_spans_match_lxml_on_every_snapshot_file(repo_root):
    files = sorted(p for p in (repo_root / "models" / "raw").rglob("*") if p.suffix.lower() in (".nml", ".xml"))
    assert files
    for p in files:
        doc = XmlDoc.load(p.parent, p.name)
        assert len(doc.spans) == len(doc.elements)
        for el, sp in zip(doc.elements, doc.spans):
            src = doc.text[sp.start:sp.end]
            reparsed = etree.fromstring(src.encode("utf-8")) if ":" not in sp.qname else None
            if reparsed is not None and not re.search(r"\bxmlns|<\w+:", src):
                assert etree.QName(reparsed).localname == etree.QName(el).localname
        assert doc.find(doc.locator(doc.elements[-1])) is doc.elements[-1]


def test_scanner_handles_quotes_comments_and_cdata():
    text = '<a x="1>2"><!-- <b> --><![CDATA[<c>]]><d y=\'/\'/></a>'
    spans, _ = scan(text)
    assert [s.qname for s in spans] == ["a", "d"]
    assert spans[1].self_closing and spans[0].end == len(text)


# ------------------------------------------------------------------ XSD and units

def test_xsd_comes_from_installed_libneuroml_and_patterns_define_units():
    import neuroml  # noqa: F401  (installed package location is the source of truth)

    path = xsd_path()
    assert path.name == "NeuroML_v2.3.1.xsd" and "neuroml" in path.parts
    raw = path.read_text(encoding="utf-8")
    xsd = xsd_index()
    for name, qtype in xsd.quantity_types.items():
        m = re.search(rf'<xs:simpleType name="{name}">.*?<xs:pattern value="([^"]+)"', raw, re.DOTALL)
        assert m and m.group(1) == qtype.pattern
    assert xsd.quantity_types["Nml2Quantity_conductanceDensity"].units == ("S_per_m2", "mS_per_cm2", "S_per_cm2")
    assert xsd.quantity_types["Nml2Quantity_temperature"].units == ("degC",)


def test_attribute_typing_is_contextual(hh_ws, lts_ws):
    xsd = xsd_index()
    hh = XmlDoc.load(hh_ws.root, hh_ws.model.cell_file)
    types = dict(zip((hh.locator(e) for e in hh.elements), xsd.type_document(hh)))
    rate = next(loc for loc in types if loc.endswith("gateHHrates[@id='m']/forwardRate[1]"))
    assert xsd.attributes(types[rate])["rate"].type == "Nml2Quantity_pertime"
    dens = next(loc for loc in types if loc.endswith("channelDensity[@id='naChans']"))
    assert xsd.attributes(types[dens])["condDensity"].type == "Nml2Quantity_conductanceDensity"
    ca = XmlDoc.load(lts_ws.root, "NeuroML2/channels/Ca/Ca.nml")
    custom = [t for e, t in zip(ca.elements, xsd.type_document(ca))
              if etree.QName(e).localname == "decayingPoolConcentrationModelPosp"]
    assert custom == [None]                      # custom LEMS component: not described by the XSD


def test_unit_factors_come_from_jneuroml_core_dimensions():
    units = core_units()
    assert units["mS_per_cm2"].factor == Decimal(10) and units["mS_per_cm2"].dimension == "conductanceDensity"
    assert units["M"].factor == Decimal(1000) and units["mM"].factor == Decimal(1)
    assert units["degC"].offset != 0


@pytest.mark.parametrize("text,unit,expected", [
    ("0.07 mS_per_cm2", "S_per_m2", "0.7 S_per_m2"),
    ("7.5E-10A", "nA", "0.75nA"),
    ("1e-5 S_per_cm2", "mS_per_cm2", "0.01 mS_per_cm2"),
    ("-70.0 mV", "V", "-0.07 V"),
    ("2.4e-4 mM", "M", "2.4e-7 M"),
])
def test_decimal_unit_conversion_is_exact(text, unit, expected):
    xsd = xsd_index()
    qtype = next(q for q in xsd.quantity_types.values() if unit in q.units and text.split()[-1].lstrip("0123456789.eE-") in q.units)
    assert convert_literal(text, unit, qtype) == expected
    assert si_value(text) == si_value(expected)


def test_conversion_refuses_offset_units_and_foreign_units():
    xsd = xsd_index()
    assert convert_literal("36 degC", "K", xsd.quantity_types["Nml2Quantity_temperature"]) is None
    assert convert_literal("10 pS", "mS_per_cm2", xsd.quantity_types["Nml2Quantity_conductance"]) is None


def test_format_decimal_never_emits_plus_exponent_or_trailing_point():
    for s in ["1E+3", "0.000000001", "123456789012345", "-0.0", "5.000", "1.5E-12"]:
        out = format_decimal(Decimal(s))
        assert "+" not in out and not out.endswith(".") and Decimal(out) == Decimal(s)


# ------------------------------------------------------------------- unit_conversion

@pytest.mark.parametrize("key", ["rs", "lts", "hh"])
def test_unit_conversion_every_attribute_exact_and_schema_valid(workspaces, tmp_path, key):
    ws = workspaces[key]
    op = REGISTRY["unit_conversion"]
    sites = op.sites(ws)
    assert sites
    xsd = xsd_index()
    by_attr = {}
    for s in sites:                                 # one target unit per attribute, applied together
        by_attr.setdefault((s.file, s.locator, s.params["attribute"]), s)
    var = fresh(ws, tmp_path, "var")
    for s in by_attr.values():
        edits, eo, mo = op.apply(var, s)
        assert (eo, mo) == ({}, {}) and len(edits) == 1
    for rel in sorted({s.file for s in by_attr.values()}):
        changes = attr_changes(ws.root / rel, var.root / rel)
        expected = {(s.locator, s.params["attribute"]) for s in by_attr.values() if s.file == rel}
        assert len(changes) == len(expected)
        for _, attr, old, new in changes:
            qtype = xsd.quantity_types[next(s.params["xsd_type"] for s in by_attr.values()
                                            if s.file == rel and s.params["attribute"] == attr and s.params["old"] == old)]
            assert re.fullmatch(qtype.pattern, new), new
            unit = re.search(r"([A-Za-z_][A-Za-z0-9_]*)$", new).group(1)
            assert unit in qtype.units and unit != re.search(r"([A-Za-z_][A-Za-z0-9_]*)$", old).group(1)
            number = lambda t: Decimal(re.match(r"-?[0-9.]+(?:[eE]-?[0-9]+)?", t).group(0))
            u_old = core_units()[re.search(r"([A-Za-z_][A-Za-z0-9_]*)$", old).group(1)]
            assert number(new) * core_units()[unit].factor == number(old) * u_old.factor


def test_unit_conversion_changes_only_one_line(rs_ws, tmp_path):
    op = REGISTRY["unit_conversion"]
    site = op.sites(rs_ws)[0]
    var = fresh(rs_ws, tmp_path, "one")
    op.apply(var, site)
    a = (rs_ws.root / site.file).read_text().splitlines()
    b = (var.root / site.file).read_text().splitlines()
    assert len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1
    assert changed_files(rs_ws.root, var.root) == [site.file]


# ------------------------------------------------------------ numeric_literal_format

@pytest.mark.parametrize("key", ["rs", "hh"])
def test_numeric_literal_format_preserves_decimal_values(workspaces, tmp_path, key):
    ws = workspaces[key]
    op = REGISTRY["numeric_literal_format"]
    sites = op.sites(ws)
    assert {s.params["style"] for s in sites} == {"scientific", "plain", "padded", "unit_spacing"}
    xsd = xsd_index()
    for style in ("scientific", "plain", "padded", "unit_spacing"):
        chosen = {}
        for s in sites:
            if s.params["style"] == style:
                chosen.setdefault((s.file, s.locator, s.params["attribute"]), s)
        var = fresh(ws, tmp_path, style)
        for s in chosen.values():
            op.apply(var, s)
        for s in chosen.values():
            el = XmlDoc.load(var.root, s.file).find(s.locator)
            new = el.get(s.params["attribute"])
            assert new == s.params["new"] and new != s.params["old"]
            lead = r"-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?"
            assert Decimal(re.match(lead, new).group(0)) == Decimal(re.match(lead, s.params["old"]).group(0))
            assert new[len(re.match(lead, new).group(0)):].strip() == s.params["old"][len(re.match(lead, s.params["old"]).group(0)):].strip()
            qtype = xsd.quantity_types.get(s.params["xsd_type"])
            if qtype is not None:
                assert re.fullmatch(qtype.pattern, new)
            assert "+" not in new


# --------------------------------------------------------------------- explicit_default

@pytest.mark.parametrize("key", ["rs", "lts", "hh"])
def test_explicit_default_values_come_from_xsd_default_declarations(workspaces, tmp_path, key, repo_root):
    ws = workspaces[key]
    op = REGISTRY["explicit_default"]
    sites = op.sites(ws)
    assert sites
    raw = xsd_path().read_text(encoding="utf-8")
    for s in sites:
        m = re.search(rf'<xs:attribute name="{s.params["attribute"]}"[^>]*default="([^"]*)"', raw)
        assert m and m.group(1) == s.params["value"]
    s = sites[0]
    var = fresh(ws, tmp_path, "d")
    edits, _, _ = op.apply(var, s)
    assert edits[0].action == "insert" and edits[0].old is None
    changes = attr_changes(ws.root / s.file, var.root / s.file)
    assert [(c[1], c[2], c[3]) for c in changes] == [(s.params["attribute"], None, s.params["value"])]


# --------------------------------------------------------------------- rename_identifier

def _site(op, ws, kind, old):
    return next(s for s in op.sites(ws) if s.params["kind"] == kind and s.params["old"] == old)


def test_rename_cell_updates_network_harness_and_model_overrides(rs_ws, tmp_path):
    op = REGISTRY["rename_identifier"]
    site = _site(op, rs_ws, "cell", "RS")
    var = fresh(rs_ws, tmp_path, "cell")
    edits, eo, mo = op.apply(var, site)
    new = site.params["new"]
    assert mo == {"cell_id": new} and eo == {}
    assert {e.attribute for e in edits} == {"id", "component", "target", "quantity"}
    net = (var.root / "NeuroML2/cells/RS/RS.net.nml").read_text()
    lems = (var.root / "NeuroML2/cells/RS/LEMS_RS.xml").read_text()
    assert f'component="{new}"' in net and f'target="../CG_RS/0/{new}"' in net and 'component="RS"' not in net
    assert "CG_RS/0/RS/" not in lems and f"CG_RS/0/{new}/biophys/membraneProperties/Na_all/Na/m/q" in lems
    cell = etree.parse(str(var.cell_path)).getroot()
    assert cell.get("id") == "RS"                   # document id is not a reference and is kept
    assert cell.find(f"{NML}cell").get("id") == new
    assert set(changed_files(rs_ws.root, var.root)) == {"NeuroML2/cells/RS/RS.cell.nml", "NeuroML2/cells/RS/RS.net.nml",
                                                        "NeuroML2/cells/RS/LEMS_RS.xml"}
    assert apply_model_overrides(var, mo).model.cell_id == new


def test_rename_channel_density_is_scoped_to_its_cell(rs_ws, tmp_path):
    op = REGISTRY["rename_identifier"]
    site = _site(op, rs_ws, "channelDensity", "Na_all")
    var = fresh(rs_ws, tmp_path, "dens")
    op.apply(var, site)
    lems = (var.root / "NeuroML2/cells/RS/LEMS_RS.xml").read_text()
    assert "membraneProperties/Na_all_renamed/Na/m/q" in lems and "membraneProperties/Na_all/" not in lems
    # LTS, FS and IB have their own Na_all: untouched
    assert set(changed_files(rs_ws.root, var.root)) == {"NeuroML2/cells/RS/RS.cell.nml", "NeuroML2/cells/RS/LEMS_RS.xml"}


def test_rename_ion_channel_updates_every_file_that_includes_it(rs_ws, tmp_path):
    op = REGISTRY["rename_identifier"]
    site = _site(op, rs_ws, "ionChannel", "Na")
    var = fresh(rs_ws, tmp_path, "chan")
    op.apply(var, site)
    for cell in ("RS", "LTS", "FS", "IB"):
        root = etree.parse(str(var.root / f"NeuroML2/cells/{cell}/{cell}.cell.nml")).getroot()
        refs = [e.get("ionChannel") for e in root.iter() if isinstance(e.tag, str) and e.get("ionChannel")]
        assert "Na" not in refs and "Na_renamed" in refs
        lems = (var.root / f"NeuroML2/cells/{cell}/LEMS_{cell}.xml").read_text()
        assert "/Na_all/Na/" not in lems
    chan = etree.parse(str(var.root / "NeuroML2/channels/Na/Na.channel.nml")).getroot()
    assert chan.find(f"{NML}ionChannel").get("id") == "Na_renamed"
    # ComponentType names that merely start with "Na" are not references
    assert (var.root / "NeuroML2/channels/Na/Na.channel.nml").read_text().count('name="Na_m_alpha_rate"') == 1


def test_rename_gate_updates_state_paths(rs_ws, tmp_path):
    op = REGISTRY["rename_identifier"]
    site = _site(op, rs_ws, "gate", "m")
    var = fresh(rs_ws, tmp_path, "gate")
    op.apply(var, site)
    lems = (var.root / "NeuroML2/cells/LTS/LEMS_LTS.xml").read_text()
    assert "Na_all/Na/m_renamed/q" in lems and "Na_all/Na/m/q" not in lems and "Na_all/Na/h/q" in lems


def test_rename_population_uses_bracket_paths(hh_ws, tmp_path):
    op = REGISTRY["rename_identifier"]
    site = _site(op, hh_ws, "population", "hhpop")
    var = fresh(hh_ws, tmp_path, "pop")
    op.apply(var, site)
    # parse without comments: the shipped harness also contains commented-out Lines, which are
    # not references (no tool reads them) and are deliberately left as they are
    parser = etree.XMLParser(remove_comments=True)
    lems = etree.parse(str(var.root / hh_ws.model.harness_lems), parser).getroot()
    quantities = [e.get("quantity") for e in lems.iter() if isinstance(e.tag, str) and e.get("quantity")]
    assert "hhpop_renamed[0]/v" in quantities
    assert quantities and all(q.startswith("hhpop_renamed[0]/") for q in quantities)
    cell = (var.root / hh_ws.model.cell_file).read_text()
    assert 'target="hhpop_renamed[0]"' in cell and 'id="hhpop_renamed"' in cell


def test_rename_never_touches_default_segment_group_and_sites_are_unique(workspaces):
    op = REGISTRY["rename_identifier"]
    for ws in workspaces.values():
        sites = op.sites(ws)
        assert not [s for s in sites if s.params["kind"] == "segmentGroup" and s.params["old"] == "all"]
        assert len({(s.file, s.locator) for s in sites}) == len(sites)
        assert all(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", s.params["new"]) for s in sites)


def test_rewrite_path_grammar():
    from neuraxis.transforms.identifiers import Definition

    d = Definition("channelDensity", "Na_all", "f", "/l", None, "RS", None, None)
    pops, dens = {"CG_RS": "RS"}, {("RS", "Na_all"): "Na"}
    assert rewrite_path("CG_RS/0/RS/biophys/membraneProperties/Na_all/Na/m/q", d, "X", pops, dens) == \
        "CG_RS/0/RS/biophys/membraneProperties/X/Na/m/q"
    assert rewrite_path("CG_LTS/0/LTS/biophys/membraneProperties/Na_all/Na/m/q", d, "X", pops, dens) is None
    g = Definition("ionChannel", "IT", "f", "/l", None, None, None, None)
    assert rewrite_path("CG/0/C/b/membraneProperties/IT_all/erev", g, "Y", {}, {("C", "IT_all"): "IT"}) is None


# ------------------------------------------------------------------------- factor_file

@pytest.mark.parametrize("key,ident", [("rs", "RS"), ("rs", "Na_m_alpha_rate"), ("hh", "naChan"),
                                       ("hh", "pulseGen1"), ("lts", "IT_u_tau_tau"), ("lts", "LTS")])
def test_factor_file_keeps_references_resolvable_for_probe_and_harness(workspaces, tmp_path, key, ident):
    ws = workspaces[key]
    op = REGISTRY["factor_file"]
    site = next(s for s in op.sites(ws) if s.params["ident"] == ident)
    var = fresh(ws, tmp_path, "factor")
    edits, _, _ = op.apply(var, site)
    new_file = site.params["new_file"]
    assert (var.root / new_file).is_file() and not (ws.root / new_file).exists()
    tag = site.params["element"]
    # original file no longer defines it; the new file does
    assert definitions(var.root, {site.file}, tag, ident) == 0
    assert definitions(var.root, {new_file}, tag, ident) == 1
    # probe perspective: the probe network includes only the cell file
    probe_files = includes_closure(var.root, ws.model.cell_file)
    harness_files = includes_closure(var.root, ws.model.harness_lems)
    was_reachable_probe = site.file in includes_closure(ws.root, ws.model.cell_file)
    if was_reachable_probe:
        assert definitions(var.root, probe_files, tag, ident) == 1
    assert definitions(var.root, harness_files, tag, ident) == 1
    # overall semantic content of the model is unchanged apart from include/root bookkeeping
    def content(root, files):
        items = Counter()
        for rel in files:
            for item in canonical(root / rel)[1:]:
                if not item[0].endswith("}include"):
                    items[item] += 1
        return items
    assert content(ws.root, includes_closure(ws.root, ws.model.harness_lems)) == \
        content(var.root, harness_files - {new_file}) + Counter(
            {k: v for k, v in content(var.root, {new_file}).items()})
    assert [e.action for e in edits] == ["remove", "insert", "insert"]


def test_factor_file_skips_components_that_depend_on_siblings(hh_ws, lts_ws):
    idents = {s.params["ident"] for s in REGISTRY["factor_file"].sites(hh_ws)}
    assert "hhcell" not in idents and "net1" not in idents          # they reference channels/inputs in the same file
    lts_idents = {s.params["ident"] for s in REGISTRY["factor_file"].sites(lts_ws)}
    assert "Na" not in lts_idents                                  # gates reference ComponentTypes beside it
    # custom ComponentType with <Child>: not described by the XSD, would not validate in a file of its own
    assert "decayingPoolConcentrationModelPosp" not in lts_idents


# --------------------------------------------------------------------- reorder_independent

@pytest.mark.parametrize("key", ["rs", "lts", "hh"])
def test_reorder_preserves_multiset_and_changes_order(workspaces, tmp_path, key):
    ws = workspaces[key]
    op = REGISTRY["reorder_independent"]
    sites = op.sites(ws)
    assert sites
    for k, s in enumerate(sites):
        var = fresh(ws, tmp_path, f"r{k}")
        op.apply(var, s)
        a, b = canonical(ws.root / s.file), canonical(var.root / s.file)
        assert a != b and Counter(a) == Counter(b)
        assert s.params["tag"] not in ("segment", "segmentGroup", "OutputColumn", "member")
        assert changed_files(ws.root, var.root) == [s.file]


# ---------------------------------------------------------------------- no-change controls

@pytest.mark.parametrize("name", ["xml_formatting", "add_comments"])
@pytest.mark.parametrize("key", ["rs", "hh"])
def test_no_change_controls_are_semantically_identical(workspaces, tmp_path, name, key):
    ws = workspaces[key]
    op = REGISTRY[name]
    sites = op.sites(ws)
    assert sites and {s.file for s in sites} == set(model_files(ws))
    for k, s in enumerate(sites):
        var = fresh(ws, tmp_path, f"n{k}")
        op.apply(var, s)
        assert (var.root / s.file).read_bytes() != (ws.root / s.file).read_bytes()
        assert canonical(var.root / s.file) == canonical(ws.root / s.file)
        assert changed_files(ws.root, var.root) == [s.file]


def test_reindent_keeps_notes_text_verbatim(rs_ws, tmp_path):
    op = REGISTRY["xml_formatting"]
    site = next(s for s in op.sites(rs_ws) if s.file.endswith("Na.channel.nml") and s.params["style"] == "reindent")
    var = fresh(rs_ws, tmp_path, "notes")
    op.apply(var, site)
    get = lambda root: [e.text for e in etree.parse(str(root / site.file)).getroot().iter(f"{NML}notes")]
    assert get(var.root) == get(rs_ws.root)


# ------------------------------------------------------------------- generate_transforms

def test_generate_transforms_is_deterministic_and_records_variants(models, tmp_path):
    model = models["nml2_hh_example"]
    ops = sorted(EXPECTED_OPERATORS)
    a = generate_transforms(model, ops, 2, seed=7, root=tmp_path / "a")
    b = generate_transforms(model, ops, 2, seed=7, root=tmp_path / "b")
    strip = lambda r: {k: v for k, v in dc.asdict(r).items() if k != "created_utc"}
    assert [strip(r) for r in a] == [strip(r) for r in b]
    assert {r.operator for r in a} == EXPECTED_OPERATORS
    assert len({r.variant_id for r in a}) == len(a)
    for r in a:
        path = tmp_path / "a" / model.model_id / r.variant_id / "variant.json"
        loaded = variant_from_dict(json.loads(path.read_text()))
        assert loaded.variant_id == r.variant_id and loaded.edits == r.edits
        assert r.tree_sha256 != r.parent_tree_sha256
        assert r.kind == REGISTRY[r.operator].kind and r.family == REGISTRY[r.operator].family
    c = generate_transforms(model, ["rename_identifier"], 2, seed=8, root=tmp_path / "c")
    assert len(c) == 2
    write_manifest(a, tmp_path / "valid_transforms.csv")
    header = (tmp_path / "valid_transforms.csv").read_text().splitlines()[0].split(",")
    assert header == MANIFEST_COLUMNS
    with pytest.raises(ValueError):
        generate_transforms(model, ["no_such_operator"], 1, 0, tmp_path / "d")
