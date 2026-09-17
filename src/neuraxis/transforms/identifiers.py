"""Consistent identifier renaming (``rename_identifier``).

A rename changes one definition's ``id`` and *every* reference to it in every workspace file
that can see the definition, including LEMS quantity paths in the shipped harness such as
``CG_RS/0/RS/biophys/membraneProperties/Na_all/Na/m/q``.

References are resolved by *kind* and *scope*, never by plain string replacement, because
the same string routinely names different things: in the Pospischil models ``Input_1`` is
both a pulse generator and an input list, ``RS`` is both the document id and the cell id,
and every cell has its own channel density called ``Na_all``. The scope of a definition is
its file plus every file that includes that file (directly or transitively); a rename is
only offered when the definition is unique for its kind within everything that scope can
see. Segment groups whose id is an XSD default value (``all``) are never renamed, since an
omitted ``segmentGroup`` attribute refers to them implicitly.

When the renamed element is the model's cell, ``model_overrides["cell_id"]`` carries the new
id so generated probe networks reference the renamed cell.
"""

from __future__ import annotations

import dataclasses as dc
import functools
import re
from collections import defaultdict

from lxml import etree

from neuraxis.models import Workspace
from neuraxis.schemas import Edit, VariantKind
from neuraxis.transforms.formatting import (
    Site,
    TransformError,
    XmlDoc,
    ancestors,
    closure,
    include_graph,
    load_docs,
    local_name,
    model_files,
    namespace,
    replace_ranges,
    write_doc,
)
from neuraxis.transforms.units import xsd_index

RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
PATH_ATTRIBUTES = {("Line", "quantity"), ("OutputColumn", "quantity"), ("EventSelection", "select"),
                   ("input", "target"), ("inputW", "target"), ("explicitInput", "target")}
CONNECTION_PATH_KEYS = ("preCellId", "postCellId", "preCell", "postCell")
KINDS = ("cell", "morphology", "segmentGroup", "biophysicalProperties", "channelDensity", "ionChannel", "gate",
         "concentrationModel", "input", "population", "network")


@dc.dataclass(frozen=True)
class NmlTags:
    """Element-name sets for each identifier kind, derived from the installed XSD."""

    cells: frozenset[str]
    channels: frozenset[str]
    densities: frozenset[str]
    gates: frozenset[str]
    biophys: frozenset[str]
    inputs: frozenset[str]
    concentration_models: frozenset[str]
    connections: frozenset[str]
    segment_group_defaults: frozenset[str]


@functools.cache
def nml_tags() -> NmlTags:
    xsd = xsd_index()
    doc_children = xsd.children("NeuroMLDocument")
    typed = xsd.complex_types
    channels = {n for n in doc_children if n.startswith("ionChannel")}
    densities = {n for t in typed if t.startswith("MembraneProperties") for n in xsd.children(t)
                 if n.startswith("channel")}
    gates = {n for t in typed if t.startswith("IonChannel") for n in xsd.children(t) if n.startswith("gate")}
    biophys = {n for t in typed if t.startswith("Cell") for n in xsd.children(t)
               if n.startswith("biophysicalProperties")}
    connections = {n for t in typed if "Projection" in t for n in xsd.children(t) if "onnection" in n}
    defaults = {a.default for t in typed for a in xsd.attributes(t).values()
                if a.name == "segmentGroup" and a.default is not None}
    for required in ("morphology", "network"):
        if required not in doc_children:
            raise RuntimeError(f"XSD has no top-level <{required}>; identifier kinds need revisiting")
    return NmlTags(
        cells=frozenset(xsd.group_elements("CellTypes") + xsd.group_elements("PyNNCellTypes")),
        channels=frozenset(channels), densities=frozenset(densities), gates=frozenset(gates),
        biophys=frozenset(biophys),
        inputs=frozenset(xsd.group_elements("InputTypes") + xsd.group_elements("PyNNInputTypes")),
        concentration_models=frozenset(xsd.group_elements("ConcentrationModelTypes")),
        connections=frozenset(connections), segment_group_defaults=frozenset(defaults))


@dc.dataclass
class Definition:
    kind: str
    id: str
    file: str
    locator: str
    element: etree._Element
    cell: str | None                   # enclosing cell id (cell-local kinds)
    channel: str | None                # enclosing ion channel id (gates)
    cell_element: etree._Element | None

    def key(self) -> tuple:
        if self.kind in ("channelDensity", "biophysicalProperties", "segmentGroup") or \
                (self.kind == "morphology" and self.cell):
            return self.kind, self.cell, self.id
        if self.kind == "gate":
            return self.kind, self.channel, self.id
        return self.kind, self.id


@dc.dataclass
class WorkspaceIndex:
    ws: Workspace
    docs: dict[str, XmlDoc]
    graph: dict[str, list[str]]
    defs: list[Definition]
    all_ids: set[str]

    @classmethod
    def build(cls, ws: Workspace) -> WorkspaceIndex:
        docs = load_docs(ws)
        graph = include_graph(ws, docs)
        tags = nml_tags()
        conc_refs = {e.get("concentrationModel") for d in docs.values() if d.root_name == "neuroml"
                     for e in d.elements if local_name(e) == "species" and e.get("concentrationModel")}
        defs: list[Definition] = []
        all_ids: set[str] = set()
        for rel in sorted(docs):
            doc = docs[rel]
            for el in doc.elements:
                for key in ("id", "name"):
                    if el.get(key):
                        all_ids.add(el.get(key))
            if doc.root_name != "neuroml":
                continue
            nml_ns = namespace(doc.root)
            for el in doc.elements:
                if namespace(el) != nml_ns:
                    continue
                kind = _kind_of(el, tags, conc_refs)
                if kind is None:
                    continue
                cell_el = next((a for a in el.iterancestors() if local_name(a) in tags.cells), None)
                chan_el = el.getparent() if kind == "gate" else None
                defs.append(Definition(kind, el.get("id"), rel, doc.locator(el), el,
                                       cell_el.get("id") if cell_el is not None else None,
                                       chan_el.get("id") if chan_el is not None else None, cell_el))
        return cls(ws, docs, graph, defs, all_ids)

    def scope(self, file: str) -> list[str]:
        return [file] + ancestors(self.graph, file)

    def universe(self, scope: list[str]) -> set[str]:
        return set(closure(self.graph, scope))


def _kind_of(el: etree._Element, tags: NmlTags, conc_refs: set[str]) -> str | None:
    parent = el.getparent()
    if parent is None or not el.get("id"):
        return None
    name, pname = local_name(el), local_name(parent)
    if pname == "neuroml":
        if name in tags.cells:
            return "cell"
        if name in tags.channels:
            return "ionChannel"
        if name in tags.inputs:
            return "input"
        if name == "network":
            return "network"
        if name == "morphology":
            return "morphology"
        if name in tags.concentration_models or el.get("id") in conc_refs:
            return "concentrationModel"
        return None
    if name in tags.densities and pname.startswith("membraneProperties"):
        return "channelDensity"
    if name in tags.gates and pname in tags.channels:
        return "gate"
    if name in tags.biophys and pname in tags.cells:
        return "biophysicalProperties"
    if name == "morphology" and pname in tags.cells:
        return "morphology"
    if name == "segmentGroup" and pname == "morphology":
        return "segmentGroup"
    if name == "population" and pname == "network":
        return "population"
    return None


def _new_id(old: str, taken: set[str]) -> str:
    candidate, k = f"{old}_renamed", 2
    while candidate in taken:
        candidate, k = f"{old}_renamed{k}", k + 1
    return candidate


def rewrite_path(path: str, d: Definition, new: str, pops: dict[str, str | None],
                 densities: dict[tuple[str | None, str], str | None]) -> str | None:
    """Rename one kind-matched segment of a LEMS/NeuroML instance path; None if nothing matches.

    Grammar handled: ``[../]pop/index/cell/...`` (population lists) and ``pop[index]/...``.
    Inside the cell, ``.../<biophys>/membraneProperties/<density>/<ionChannel>/<gate>/...``.
    """
    prefix = ""
    rest = path
    while rest.startswith("../"):
        prefix, rest = prefix + "../", rest[3:]
    toks = rest.split("/")
    m = re.fullmatch(r"([^\[\]]+)(\[[^\]]*\])?", toks[0])
    if m is None:
        return None
    pop, bracket = m.group(1), m.group(2) or ""
    list_form = len(toks) >= 3 and toks[1].isdigit()
    path_cell = toks[2] if list_form else pops.get(pop)
    first_inner = 3 if list_form else 1
    out = list(toks)
    if d.kind == "population" and pop == d.id and d.id in pops:
        out[0] = new + bracket
    if d.kind == "cell" and list_form and toks[2] == d.id:
        out[2] = new
    if "membraneProperties" in toks[first_inner:]:
        mi = toks.index("membraneProperties", first_inner)
        if d.kind == "biophysicalProperties" and mi - 1 >= first_inner and toks[mi - 1] == d.id \
                and path_cell == d.cell:
            out[mi - 1] = new
        if d.kind == "channelDensity" and mi + 1 < len(toks) and toks[mi + 1] == d.id and path_cell == d.cell:
            out[mi + 1] = new
        if d.kind == "ionChannel" and mi + 2 < len(toks) and toks[mi + 2] == d.id \
                and densities.get((path_cell, toks[mi + 1])) == d.id:
            out[mi + 2] = new
        if d.kind == "gate" and mi + 3 < len(toks) and toks[mi + 3] == d.id and toks[mi + 2] == d.channel \
                and densities.get((path_cell, toks[mi + 1])) == d.channel:
            out[mi + 3] = new
    if out == toks:
        return None
    return prefix + "/".join(out)


class RenameIdentifier:
    """Rename one identifier and update every reference (attributes and instance paths)."""

    name = "rename_identifier"
    family = "renaming"
    kind = VariantKind.VALID_TRANSFORM

    def sites(self, ws: Workspace) -> list[Site]:
        idx = WorkspaceIndex.build(ws)
        mfiles = set(model_files(ws, idx.docs))
        protected = nml_tags().segment_group_defaults
        out = []
        for d in idx.defs:
            if d.file not in mfiles or (d.kind == "segmentGroup" and d.id in protected):
                continue
            universe = idx.universe(idx.scope(d.file))
            if sum(1 for o in idx.defs if o.file in universe and o.key() == d.key()) != 1:
                continue
            out.append(Site(self.name, d.file, d.locator,
                            {"kind": d.kind, "old": d.id, "new": _new_id(d.id, idx.all_ids)}))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        p = site.params
        idx = WorkspaceIndex.build(ws)
        matches = [d for d in idx.defs if d.file == site.file and d.locator == site.locator
                   and d.kind == p["kind"] and d.id == p["old"]]
        if len(matches) != 1:
            raise TransformError(f"definition {p['kind']} {p['old']!r} not found at {site.file}{site.locator}")
        d, new = matches[0], p["new"]
        if new in idx.all_ids or not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", new):
            raise TransformError(f"new id {new!r} is taken or not a valid NmlId")
        scope = idx.scope(d.file)
        universe = idx.universe(scope)
        pops = {o.id: o.element.get("component") for o in idx.defs if o.kind == "population" and o.file in universe}
        dens = {(o.cell, o.id): o.element.get("ionChannel") for o in idx.defs
                if o.kind == "channelDensity" and o.file in universe}

        changes: dict[str, dict[tuple[int, str], tuple[etree._Element, str, str]]] = defaultdict(dict)
        changes[d.file][(id(d.element), "id")] = (d.element, "id", new)
        for e in d.element.iter():
            if isinstance(e.tag, str) and e.get(RDF_ABOUT) in (d.id, f"#{d.id}"):
                v = e.get(RDF_ABOUT)
                changes[d.file][(id(e), RDF_ABOUT)] = (e, RDF_ABOUT, new if v == d.id else f"#{new}")
        for f in scope:
            doc = idx.docs[f]
            for el in doc.elements:
                for key, value in el.attrib.items():
                    nv = self._rewrite(d, new, el, key, value, pops, dens)
                    if nv is not None and nv != value:
                        changes[f][(id(el), key)] = (el, key, nv)

        edits: list[Edit] = []
        note = f"rename {d.kind} {d.id} -> {new} (locators refer to the pre-edit file)"
        for f in sorted(changes):
            doc = idx.docs[f]
            items = sorted(changes[f].values(), key=lambda t: doc.index(t[0]))
            edits += [Edit(f, doc.locator(el), doc.text_attr_name(el, key), el.get(key), v, "set", note)
                      for el, key, v in items]
            write_doc(ws.root, doc, replace_ranges(doc.text, [doc.set_attr_change(el, key, v)
                                                              for el, key, v in items]))
        overrides = {}
        if d.kind == "cell" and d.id == ws.model.cell_id and d.file == ws.model.cell_file:
            overrides["cell_id"] = new
        return edits, {}, overrides

    @staticmethod
    def _rewrite(d: Definition, new: str, el: etree._Element, key: str, value: str,
                 pops: dict[str, str | None], dens: dict[tuple[str | None, str], str | None]) -> str | None:
        if key.startswith("{"):
            return None
        tags = nml_tags()
        name, old, kind = local_name(el), d.id, d.kind
        if (name, key) in PATH_ATTRIBUTES or (name in tags.connections and key in CONNECTION_PATH_KEYS):
            return rewrite_path(value, d, new, pops, dens)
        if value != old:
            return None
        if kind == "cell" and name == "population" and key == "component":
            return new
        if kind == "ionChannel" and name in tags.densities and key == "ionChannel":
            return new
        if kind == "biophysicalProperties" and name in tags.cells and key == "biophysicalProperties" \
                and el.get("id") == d.cell:
            return new
        if kind == "morphology" and name in tags.cells and key == "morphology" \
                and (d.cell is None or el.get("id") == d.cell):
            return new
        if kind == "population" and ((name == "inputList" and key == "population")
                                     or key in ("presynapticPopulation", "postsynapticPopulation")):
            return new
        if kind == "concentrationModel" and name == "species" and key == "concentrationModel":
            return new
        if kind == "input" and ((name == "inputList" and key == "component")
                                or (name == "explicitInput" and key == "input")):
            return new
        if kind == "network" and key == "target" and (
                name == "Simulation" or (name == "Component" and el.get("type") == "Simulation")):
            return new
        if kind == "segmentGroup" and key == "segmentGroup" and d.cell_element is not None \
                and any(a is d.cell_element for a in el.iterancestors()):
            return new
        return None

    def describe(self, site: Site) -> str:
        p = site.params
        return f"rename {p['kind']} {p['old']!r} -> {p['new']!r} (defined in {site.file}) and all references"
