"""File factoring (``factor_file``) and reordering of independent elements (``reorder_independent``).

``factor_file`` moves one top-level component of a NeuroML file F into a new file N in the
same directory and adds ``<include href="N"/>`` to F. Because the include is added to F
itself, every consumer of F still reaches the component: the probe network (which includes
only the cell file) and the shipped harness (which may include channel files directly)
both resolve it transitively. N also receives copies of F's own ``<include>`` elements so
that N validates on its own (``jnml -validate`` checks references through includes). A
component is only moved if it does not reference a sibling top-level definition of F
(otherwise N would need to include F back, creating an include cycle), and only if every
NeuroML element inside it is described by the XSD, so that N can pass schema validation by
itself. The second rule excludes custom LEMS content the schema does not describe, e.g. the
Pospischil calcium-pool ``ComponentType`` with a ``<Child>`` element, which fails
``jnml -validate`` as soon as it is placed in a file of its own.

``reorder_independent`` permutes a run of consecutive same-name sibling elements whose order
carries no meaning in NeuroML: channel densities in a membrane (currents are summed), gates
of a channel (conductance is a product), includes, populations and inputs of a network, and
top-level components. Only same-name runs are permuted so that the XSD ``xs:sequence`` order
of different element names is preserved. Such permutations are semantically neutral but can
change floating-point summation or multiplication order. Elements whose order does carry
meaning are never touched: segments (parent before child), ``OutputColumn`` (column index)
and anything separated by comments or other content. Segment groups are also excluded:
jNeuroML 0.14.0 emits validation warning 100005 when a group is included by another group
before it is defined ("for optimal portability"), so their order is not free in practice and
the result would not validate cleanly (observed on the Pospischil RS cell).
"""

from __future__ import annotations

import re
from itertools import pairwise
from pathlib import Path, PurePosixPath

from lxml import etree

from nexclamp.models import Workspace
from nexclamp.schemas import Edit, VariantKind
from nexclamp.transforms.formatting import (
    Site,
    TransformError,
    XmlDoc,
    escape_attr,
    load_docs,
    local_name,
    model_files,
    namespace,
    replace_ranges,
    write_doc,
    xml_files,
)
from nexclamp.transforms.identifiers import nml_tags
from nexclamp.transforms.units import xsd_index

_IDENT_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_XML_DECL = re.compile(r"\s*(<\?xml[^>]*\?>)")
_NON_COMPONENT = {"include", "notes", "annotation", "property"}


def _ident(el: etree._Element) -> str | None:
    return el.get("id") or (el.get("name") if local_name(el) == "ComponentType" else None)


def _references_siblings(el: etree._Element, siblings: list[etree._Element]) -> bool:
    """Conservative test: does ``el`` mention the id/name of another top-level component?"""
    names = {_ident(s) for s in siblings if s is not el} - {None}
    tokens: set[str] = set()
    for e in el.iter():
        if isinstance(e.tag, str):
            tokens.add(local_name(e))
            for v in e.attrib.values():
                tokens.update(_IDENT_TOKEN.findall(v))
    return bool(tokens & names)


class FactorFile:
    """Move one top-level component into a new included file."""

    name = "factor_file"
    family = "factoring"
    kind = VariantKind.VALID_TRANSFORM

    def sites(self, ws: Workspace) -> list[Site]:
        docs = load_docs(ws)
        taken = set(xml_files(ws))
        xsd = xsd_index()
        out = []
        for rel in model_files(ws, docs):
            doc = docs[rel]
            if doc.root_name != "neuroml":
                continue
            typed = {id(e): t for e, t in zip(doc.elements, xsd.type_document(doc))}
            nml_ns = namespace(doc.root)
            kids = doc.children(doc.root)
            for el in kids:
                ident = _ident(el)
                if local_name(el) in _NON_COMPONENT or not ident or _references_siblings(el, kids):
                    continue
                if not all(typed[id(e)] for e in el.iter() if isinstance(e.tag, str) and namespace(e) == nml_ns):
                    continue
                new_rel = _new_file(rel, ident, taken)
                taken.add(new_rel)
                out.append(Site(self.name, rel, doc.locator(el),
                                {"element": local_name(el), "ident": ident, "new_file": new_rel}))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        p = site.params
        doc = XmlDoc.load(ws.root, site.file)
        if doc.root_name != "neuroml":
            raise TransformError(f"{site.file} is not a NeuroML document")
        el = doc.find(site.locator)
        if local_name(el) != p["element"] or _ident(el) != p["ident"]:
            raise TransformError(f"{site.file}{site.locator} is not <{p['element']}> {p['ident']!r}")
        new_rel = p["new_file"]
        if PurePosixPath(new_rel).parent != PurePosixPath(site.file).parent:
            raise TransformError("factored file must live next to its parent file")
        if (Path(ws.root) / new_rel).exists():
            raise TransformError(f"{new_rel} already exists")
        kids = doc.children(doc.root)
        nl = doc.newline
        sp = doc.span(el)
        element_text = doc.text[sp.start:sp.end]
        indent = doc.indentation_before(sp.start)

        # remove the element (whole lines when it stands alone on them)
        rm_start, rm_end = sp.start, sp.end
        line_end = doc.text.find("\n", sp.end)
        if indent is not None and line_end >= 0 and doc.text[sp.end:line_end].strip() == "":
            rm_start, rm_end = doc.line_start(sp.start), line_end + 1
        indent = indent if indent else "    "

        # add the include after existing includes (XSD sequence: notes, property, annotation, include, ...)
        href = PurePosixPath(new_rel).name
        includes = [k for k in kids if local_name(k) == "include"]
        meta = [k for k in kids if local_name(k) in ("notes", "property", "annotation")]
        anchor_end = doc.span(includes[-1]).end if includes else (doc.span(meta[-1]).end if meta
                                                                  else doc.spans[0].tag_end)
        include_text = f'<include href="{escape_attr(href, chr(34))}"/>'
        new_parent = replace_ranges(doc.text, [(rm_start, rm_end, ""),
                                               (anchor_end, anchor_end, f"{nl}{indent}{include_text}")])

        # new file: same XML declaration and root element, parent's includes, the moved element
        decl = _XML_DECL.match(doc.text)
        root_sp = doc.spans[0]
        parts = [decl.group(1) + nl if decl else "", doc.text[root_sp.start:root_sp.tag_end], nl]
        for inc in includes:
            parts.append(f"{nl}{indent}{doc.text[doc.span(inc).start:doc.span(inc).end]}")
        parts += [f"{nl}{nl}{indent}{element_text}{nl}{nl}</{root_sp.qname}>{nl}"]
        skeleton = XmlDoc.from_text("".join(parts), new_rel, doc.encoding, doc.bom)
        doc_id = re.sub(r"[^A-Za-z0-9_]", "_", p["ident"]) + "_factored"
        new_text = replace_ranges(skeleton.text, [skeleton.set_attr_change(skeleton.root, "id", doc_id)])
        new_doc = XmlDoc.from_text(new_text, new_rel, doc.encoding, doc.bom)
        if len(new_doc.children(new_doc.root)) != len(includes) + 1:
            raise TransformError("factored file does not contain exactly the moved element and includes")

        (Path(ws.root) / new_rel).write_bytes(doc.encode(new_text))
        write_doc(ws.root, doc, new_parent)
        root = doc.root_name
        edits = [
            Edit(site.file, site.locator, None, element_text, None, "remove", f"moved to {new_rel}"),
            Edit(site.file, f"/{root}/include[@href='{href}']", "href", None, href, "insert",
                 "include of the factored file"),
            Edit(new_rel, f"/{root}", None, None, new_text, "insert",
                 f"new file holding <{p['element']}> {p['ident']!r} plus copies of {site.file}'s includes"),
        ]
        return edits, {}, {}

    def describe(self, site: Site) -> str:
        p = site.params
        return f"move <{p['element']}> {p['ident']!r} from {site.file} to included file {p['new_file']}"


def _new_file(rel: str, ident: str, taken: set[str]) -> str:
    parent = PurePosixPath(rel).parent
    stem = re.sub(r"[^A-Za-z0-9_]", "_", ident)
    candidate, k = (parent / f"{stem}.factored.nml").as_posix(), 2
    while candidate in taken:
        candidate, k = (parent / f"{stem}.factored{k}.nml").as_posix(), k + 1
    return candidate


# ------------------------------------------------------------------------ reordering

_NETWORK_CHILDREN = {"population", "inputList", "explicitInput", "projection", "electricalProjection",
                     "continuousProjection"}


def _runs(doc: XmlDoc, parent: etree._Element) -> list[list[etree._Element]]:
    kids = doc.children(parent)
    runs: list[list[etree._Element]] = []
    for kid in kids:
        if runs and local_name(runs[-1][-1]) == local_name(kid) and \
                doc.text[doc.span(runs[-1][-1]).end:doc.span(kid).start].strip() == "":
            runs[-1].append(kid)
        else:
            runs.append([kid])
    return [r for r in runs if len(r) >= 2]


def _reorderable(ws: Workspace, doc: XmlDoc, parent: etree._Element, child: str,
                 run: list[etree._Element]) -> bool:
    tags = nml_tags()
    pname = local_name(parent)
    if doc.root_name == "neuroml":
        if pname == "neuroml":
            return child == "include" or child == "ComponentType" or child in (
                tags.channels | tags.cells | tags.inputs | tags.concentration_models)
        if pname.startswith("membraneProperties"):
            return child in tags.densities
        if pname in tags.channels:
            return child in tags.gates
        if pname == "network":
            return child in _NETWORK_CHILDREN
        return False
    if doc.root_name == "Lems" and pname == "Lems" and child == "Include":
        base = (Path(ws.root) / doc.rel).parent
        return all(e.get("file") and (base / e.get("file")).is_file() for e in run)
    return False


def _label(el: etree._Element, position: int) -> str:
    for key in ("id", "name", "href", "file"):
        if el.get(key):
            return el.get(key)
    return f"#{position}"


class ReorderIndependent:
    """Permute a run of same-name sibling elements whose order has no meaning."""

    name = "reorder_independent"
    family = "reordering"
    kind = VariantKind.VALID_TRANSFORM

    def sites(self, ws: Workspace) -> list[Site]:
        docs = load_docs(ws)
        out = []
        for rel in model_files(ws, docs):
            doc = docs[rel]
            for parent in doc.elements:
                for run in _runs(doc, parent):
                    child = local_name(run[0])
                    if not _reorderable(ws, doc, parent, child, run):
                        continue
                    same = [c for c in doc.children(parent) if local_name(c) == child]
                    first = same.index(run[0]) + 1
                    perms = ("reverse", "rotate") if len(run) >= 3 else ("reverse",)
                    for perm in perms:
                        out.append(Site(self.name, rel, doc.locator(parent),
                                        {"tag": child, "first": first, "count": len(run), "permutation": perm}))
        return out

    @staticmethod
    def permutation(count: int, name: str) -> list[int]:
        order = list(range(count))
        if name == "reverse":
            return order[::-1]
        if name == "rotate":
            return order[1:] + order[:1]
        raise ValueError(f"unknown permutation {name!r}")

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        p = site.params
        doc = XmlDoc.load(ws.root, site.file)
        parent = doc.find(site.locator)
        same = [c for c in doc.children(parent) if local_name(c) == p["tag"]]
        run = same[p["first"] - 1:p["first"] - 1 + p["count"]]
        if len(run) != p["count"] or not any(r == run for r in _runs(doc, parent)) \
                or not _reorderable(ws, doc, parent, p["tag"], run):
            raise TransformError(f"{site.file}{site.locator}: run of <{p['tag']}> no longer matches the site")
        spans = [doc.span(e) for e in run]
        pieces = [doc.text[s.start:s.end] for s in spans]
        gaps = [doc.text[a.end:b.start] for a, b in pairwise(spans)] + [""]
        perm = self.permutation(len(run), p["permutation"])
        new_run = "".join(pieces[i] + gap for i, gap in zip(perm, gaps))
        write_doc(ws.root, doc, replace_ranges(doc.text, [(spans[0].start, spans[-1].end, new_run)]))
        labels = [_label(e, i + p["first"]) for i, e in enumerate(run)]
        edit = Edit(site.file, site.locator, None, ",".join(labels), ",".join(labels[i] for i in perm), "text",
                    f"reorder {len(run)} consecutive <{p['tag']}> siblings ({p['permutation']})")
        return [edit], {}, {}

    def describe(self, site: Site) -> str:
        p = site.params
        return f"{p['permutation']} {p['count']} <{p['tag']}> children of {site.file}{site.locator}"
