"""Mutation engine core: sites, operator protocol, XML editing, semantic diff and enforcement.

A mutant must differ from its reference by exactly one recorded fault. Two independent
checks guarantee that: every operator records an :class:`~neuraxis.schemas.Edit` for each
change it makes, and :func:`enforce_single_operator` recomputes a semantic XML diff of
the whole workspace against a pristine reference and refuses any change that is not
recorded (or any recorded edit that is not present). Formatting introduced by
re-serialising a file is ignored by the diff, but the recorded ``tree_sha256`` pins the
exact bytes, so post-generation tampering is caught as well.
"""

from __future__ import annotations

import abc
import copy
import csv
import dataclasses as dc
import io
import json
import os
import re
import tempfile
import zlib
from collections.abc import Callable, Collection, Iterator, Sequence
from decimal import Decimal
from difflib import SequenceMatcher
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Protocol

import numpy as np
from lxml import etree

from neuraxis.models import Workspace, load_models, materialize
from neuraxis.provenance import sha256_json, tree_manifest, utc_now
from neuraxis.schemas import (
    Edit,
    ModelRecord,
    MutationFamily,
    VariantKind,
    VariantRecord,
    dumps,
    to_jsonable,
    variant_from_dict,
)
from neuraxis.units import UNITS

ALLOWED_EXEC_OVERRIDES = frozenset({"dt_factor", "integrator_method", "sample_every_ms"})
GENERATOR_SEED_KEY = "generator_seed"      # stored in VariantRecord.params (schemas has no seed field)
MANIFEST_COLUMNS = ["variant_id", "model_id", "family", "operator", "params_json", "edits_json",
                    "exec_overrides_json", "description", "generator_seed"]


class MutationError(RuntimeError):
    pass


@dc.dataclass(frozen=True)
class Site:
    """One concrete place (and parameter value) where an operator can act."""

    operator: str
    file: str                      # relative to workspace root ("" for exec-only operators)
    locator: str
    params: dict


@dc.dataclass(frozen=True)
class Inapplicable:
    """A candidate target the operator deliberately skips, with the reason (for audits)."""

    operator: str
    file: str
    locator: str
    reason: str


class MutationOperator(Protocol):
    name: str
    family: MutationFamily

    def sites(self, ws: Workspace) -> list[Site]: ...

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]: ...


class OperatorBase(abc.ABC):
    """Shared behaviour. Subclasses set ``name``/``family`` and implement ``sites`` and ``check_record``."""

    name: str = ""
    family: MutationFamily
    # Child element names that together form ONE target (e.g. forwardRate + reverseRate of
    # one gate). Empty: every edit must address the same element.
    container_children: frozenset[str] = frozenset()
    # The exec_overrides keys every mutant of this operator carries: exactly these, no others.
    # A second key would be a second fault that no file edit records (e.g. a conductance
    # mutant that also coarsens dt), so enforcement rejects any mismatch.
    exec_override_keys: frozenset[str] = frozenset()

    @abc.abstractmethod
    def sites(self, ws: Workspace) -> list[Site]: ...

    @abc.abstractmethod
    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        """Raise :class:`MutationError` unless ``record`` has the shape of this operator's fault.

        Enforcement already proves that the recorded edits are exactly the workspace change
        and lie in one element. This check proves they are the *kind* of change the named
        operator makes (right element, attribute, magnitude, relation), so per-family
        statistics are never computed over mislabelled or compound faults.
        """

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        """Default: apply the attribute ``changes`` precomputed in ``site.params``."""
        self._check_site(site)
        return apply_attribute_changes(ws, site), {}, {}

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        return []

    def describe(self, site: Site) -> str:
        changes = site.params.get("changes", [])
        parts = [f"{c['attribute']}: {c['old']!r} -> {c['new']!r}" for c in changes]
        extra = {k: v for k, v in site.params.items() if k not in ("changes", GENERATOR_SEED_KEY)}
        return f"{self.name} at {site.file or 'exec'}:{site.locator} {json.dumps(extra, sort_keys=True)} " + "; ".join(parts)

    def _check_site(self, site: Site) -> None:
        if site.operator != self.name:
            raise MutationError(f"site for {site.operator!r} passed to {self.name!r}")


REGISTRY: dict[str, MutationOperator] = {}


def register(op: OperatorBase) -> OperatorBase:
    if op.name in REGISTRY:
        raise ValueError(f"duplicate operator {op.name!r}")
    REGISTRY[op.name] = op
    return op


# ----------------------------------------------------------------------------- XML I/O
_DECL_RE = re.compile(rb"^<\?xml[^>]*\?>")
_BOM = b"\xef\xbb\xbf"


@dc.dataclass
class XmlDoc:
    path: Path
    tree: Any
    encoding: str
    declaration: bytes | None
    bom: bytes
    trailing_newline: bool

    @property
    def root(self):
        return self.tree.getroot()


def _parser() -> etree.XMLParser:
    return etree.XMLParser(remove_blank_text=False, remove_comments=False, remove_pis=False,
                           resolve_entities=False, no_network=True)


def read_xml(path: Path) -> XmlDoc:
    path = Path(path)
    raw = path.read_bytes()
    bom = _BOM if raw.startswith(_BOM) else b""
    body = raw[len(bom):]
    m = _DECL_RE.match(body)
    tree = etree.parse(io.BytesIO(raw), _parser(), base_url=str(path))
    return XmlDoc(path, tree, tree.docinfo.encoding or "UTF-8", m.group(0) if m else None, bom,
                  raw.endswith(b"\n"))


def write_xml(doc: XmlDoc) -> None:
    """Write back in the declared encoding, reusing the original declaration bytes verbatim."""
    body = etree.tostring(doc.tree, encoding=doc.encoding, xml_declaration=False)
    head = doc.bom + (doc.declaration + b"\n" if doc.declaration else b"")
    tail = b"\n" if doc.trailing_newline and not body.endswith(b"\n") else b""
    doc.path.write_bytes(head + body + tail)


def is_element(node) -> bool:
    return isinstance(node.tag, str)


def localname(el) -> str:
    return etree.QName(el).localname


def iter_elements(root) -> Iterator:
    return (e for e in root.iter() if is_element(e))


def element_children(el) -> list:
    return [c for c in el if is_element(c)]


def qualified(like, name: str) -> str:
    """Tag ``name`` in the namespace of element ``like`` (LEMS files may or may not be namespaced)."""
    ns = etree.QName(like).namespace
    return f"{{{ns}}}{name}" if ns else name


def snippet(el) -> str:
    return etree.tostring(el, with_tail=False, encoding="unicode")


# ----------------------------------------------------------------------------- locators
_STEP_RE = re.compile(r"^([A-Za-z_][\w.\-]*)(?:\[@id='([^'/]*)'\]|\[(\d+)\])$")


def _same_name_siblings(el) -> list:
    parent = el.getparent()
    if parent is None:
        return [el]
    name = localname(el)
    return [c for c in element_children(parent) if localname(c) == name]


def locator(el) -> str:
    """Deterministic XPath-like path: ``name[@id='x']`` when the id is unique among
    same-name siblings, else ``name[n]`` (1-based among same-name siblings)."""
    steps = []
    node = el
    while node is not None:
        sibs = _same_name_siblings(node)
        nid = node.get("id")
        if nid is not None and "'" not in nid and "/" not in nid and sum(s.get("id") == nid for s in sibs) == 1:
            steps.append(f"{localname(node)}[@id='{nid}']")
        else:
            steps.append(f"{localname(node)}[{sibs.index(node) + 1}]")
        node = node.getparent()
    return "/" + "/".join(reversed(steps))


def resolve(root, loc: str):
    steps = loc.strip("/").split("/")
    current = None
    for i, step in enumerate(steps):
        m = _STEP_RE.match(step)
        if not m:
            raise MutationError(f"bad locator step {step!r} in {loc!r}")
        name, sid, idx = m.groups()
        cands = [root] if i == 0 else [c for c in element_children(current) if localname(c) == name]
        cands = [c for c in cands if localname(c) == name]
        if sid is not None:
            cands = [c for c in cands if c.get("id") == sid]
            if len(cands) != 1:
                raise MutationError(f"locator {loc!r}: step {step!r} matched {len(cands)} elements")
            current = cands[0]
        else:
            k = int(idx) - 1
            if not 0 <= k < len(cands):
                raise MutationError(f"locator {loc!r}: step {step!r} not found")
            current = cands[k]
    return current


def locator_steps(loc: str) -> list[str]:
    return loc.strip("/").split("/")


def step_name(loc: str) -> str:
    """Element name of the last locator step ("" if the locator is malformed)."""
    m = _STEP_RE.match(locator_steps(loc)[-1]) if loc else None
    return m.group(1) if m else ""


def parent_locator(loc: str) -> str:
    return "/" + "/".join(locator_steps(loc)[:-1])


# ----------------------------------------------------------------------------- quantities
_QTEXT_RE = re.compile(r"^(\s*)(-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)(\s*)([A-Za-z_][A-Za-z_0-9]*)?(\s*)$")


def _dec(x: float | str) -> Decimal:
    return Decimal(x) if isinstance(x, (int, str)) else Decimal(repr(float(x)))


def format_decimal(d: Decimal, template: str) -> str:
    """Format ``d`` in the style of the original literal (scientific or plain), XSD-safe
    (no ``+`` in exponents). Decimal arithmetic avoids float noise such as 0.06300000000000001."""
    sci = "e" in template.lower()
    if d == 0:
        return "0.0" if "." in template else "0"
    if sci:
        mant, exp = f"{d.normalize():E}".split("E")
        return f"{mant}{'E' if 'E' in template else 'e'}{int(exp)}"
    s = format(d.normalize(), "f")
    if "." in template and "." not in s:
        s += ".0"
    return s


def split_quantity(text: str) -> tuple[str, str, str, str, str]:
    m = _QTEXT_RE.match(text)
    if not m:
        raise MutationError(f"not a NeuroML quantity: {text!r}")
    lead, num, space, unit, trail = m.groups()
    return lead, num, space, unit or "", trail


def scale_quantity(text: str, factor: float | str | Decimal) -> str:
    lead, num, space, unit, trail = split_quantity(text)
    f = factor if isinstance(factor, Decimal) else _dec(factor)
    return f"{lead}{format_decimal(Decimal(num) * f, num)}{space}{unit}{trail}"


def shift_quantity(text: str, delta: float, delta_unit: str) -> str:
    """Add ``delta`` (given in ``delta_unit``) keeping the literal's own unit."""
    lead, num, space, unit, trail = split_quantity(text)
    if unit not in UNITS or delta_unit not in UNITS:
        raise MutationError(f"cannot shift {text!r} by {delta} {delta_unit}")
    dim, factor, offset = UNITS[unit]
    ddim, dfactor, doffset = UNITS[delta_unit]
    if dim != ddim or offset or doffset:
        raise MutationError(f"cannot shift {text!r} by {delta} {delta_unit}")
    d = _dec(delta) * _dec(dfactor) / _dec(factor)
    return f"{lead}{format_decimal(Decimal(num) + d, num)}{space}{unit}{trail}"


def quantity_si(text: str) -> float:
    _, num, _, unit, _ = split_quantity(text)
    if not unit:
        return float(num)
    if unit not in UNITS:
        raise MutationError(f"unit {unit!r} in {text!r} is not supported by neuraxis.units")
    _, factor, offset = UNITS[unit]
    return float(num) * factor + offset


def same_quantity(a: str | None, b: str | None) -> bool:
    """Same unit and the same exact decimal value, whatever the literal's formatting."""
    try:
        _, na, _, ua, _ = split_quantity(a)  # type: ignore[arg-type]
        _, nb, _, ub, _ = split_quantity(b)  # type: ignore[arg-type]
    except (MutationError, TypeError):
        return False
    return ua == ub and Decimal(na) == Decimal(nb)


def is_scaled(old: str | None, new: str | None, factor: Any) -> bool:
    """``new`` is exactly ``old`` x ``factor`` in ``old``'s unit (Decimal arithmetic, as the operators use)."""
    try:
        return same_quantity(new, scale_quantity(old, factor))  # type: ignore[arg-type]
    except (MutationError, TypeError, ValueError, ArithmeticError):
        return False


def is_shifted(old: str | None, new: str | None, delta: Any, delta_unit: str) -> bool:
    """``new`` is exactly ``old`` + ``delta`` (``delta_unit``) in ``old``'s unit."""
    try:
        return same_quantity(new, shift_quantity(old, delta, delta_unit))  # type: ignore[arg-type]
    except (MutationError, TypeError, ValueError, ArithmeticError):
        return False


# ----------------------------------------------------------------------------- record checks
def require(cond: bool, record: VariantRecord, msg: str) -> None:
    if not cond:
        raise MutationError(f"{record.operator}: {msg}")


def record_param(record: VariantRecord, key: str) -> Any:
    if key not in record.params:
        raise MutationError(f"{record.operator}: params.{key} is missing")
    return record.params[key]


def parse_snippet(text: str | None):
    """Element parsed from a recorded insert/remove snippet, or None if it is not XML."""
    if not text:
        return None
    try:
        return etree.fromstring(text.encode("utf-8"), _parser())
    except etree.XMLSyntaxError:
        return None


def expect_set_edits(record: VariantRecord, *, attributes: Collection[str],
                     element: Collection[str] | Callable[[str], bool], files: Collection[str],
                     count: int | range = 1) -> list[Edit]:
    """The record's edits must be ``count`` attribute sets of ``attributes`` on elements named
    ``element`` (names or a predicate) in ``files``; returns them."""
    edits = list(record.edits)
    n_ok = len(edits) == count if isinstance(count, int) else len(edits) in count
    require(n_ok, record, f"expected {count if isinstance(count, int) else f'{count.start}-{count.stop - 1}'} "
                          f"attribute edit(s), got {len(edits)}")
    ok_name = element if callable(element) else (lambda name: name in element)  # type: ignore[operator]
    for e in edits:
        require(e.action == "set", record, f"edit action {e.action!r} is not an attribute set")
        require(e.attribute in attributes, record, f"attribute {e.attribute!r} is not one of {sorted(attributes)}")
        require(ok_name(step_name(e.locator)), record, f"element {step_name(e.locator)!r} is not a target of this operator")
        require(e.file in files, record, f"file {e.file!r} is not a target file of this operator")
    return edits


# ----------------------------------------------------------------------------- model structure
def rel_path(ws: Workspace, path: Path) -> str | None:
    full = Path(os.path.normpath(path))
    try:
        return full.relative_to(Path(os.path.normpath(ws.root))).as_posix()
    except ValueError:
        return None


def nml_includes(ws: Workspace, rel: str) -> list[str]:
    """Existing files named by top-level NeuroML ``<include href>`` elements of ``rel``."""
    doc = read_xml(ws.path(rel))
    out = []
    for el in element_children(doc.root):
        if localname(el) == "include" and el.get("href"):
            r = rel_path(ws, ws.path(rel).parent / el.get("href"))
            if r is not None and ws.path(r).is_file() and r not in out:
                out.append(r)
    return out


def transitive_includes(ws: Workspace, rel: str) -> list[str]:
    """``rel`` followed by its NeuroML includes, depth-first pre-order, deduplicated."""
    seen: list[str] = []

    def visit(r: str) -> None:
        if r in seen:
            return
        seen.append(r)
        for child in nml_includes(ws, r):
            visit(child)

    visit(rel)
    return seen


def harness_includes(ws: Workspace) -> list[str]:
    """Workspace files included by the harness LEMS file (jLEMS built-ins such as Cells.xml are skipped)."""
    doc = read_xml(ws.harness_path)
    out = []
    for el in iter_elements(doc.root):
        if localname(el) == "Include" and el.get("file"):
            r = rel_path(ws, ws.harness_path.parent / el.get("file"))
            if r is not None and ws.path(r).is_file() and r not in out:
                out.append(r)
    return out


def harness_rel(ws: Workspace) -> str:
    return ws.model.harness_lems


def cell_rel(ws: Workspace) -> str:
    return ws.model.cell_file


def find_cell(root, cell_id: str):
    for el in iter_elements(root):
        if el.get("id") == cell_id and localname(el) in ("cell", "cell2CaPools"):
            return el
    return None


def harness_simulation(root):
    """The Simulation targeted by ``<Target component>``; handles ``<Simulation>`` and
    ``<Component type="Simulation">``."""
    sims = [e for e in iter_elements(root)
            if localname(e) == "Simulation" or (localname(e) == "Component" and e.get("type") == "Simulation")]
    target = next((e.get("component") for e in iter_elements(root) if localname(e) == "Target"), None)
    if target:
        match = [s for s in sims if s.get("id") == target]
        if match:
            return match[0]
    if not sims:
        raise MutationError("no Simulation element in harness")
    return sims[0]


def insert_after(node, new) -> None:
    new.tail = node.tail
    node.addnext(new)


def insert_before(node, new) -> None:
    prev = node.getprevious()
    ws_text = prev.tail if prev is not None else node.getparent().text
    node.addprevious(new)
    new.tail = ws_text if ws_text is not None and not ws_text.strip() else "\n"


def remove_element(el) -> None:
    parent = el.getparent()
    tail = el.tail or ""
    if tail.strip():
        prev = el.getprevious()
        if prev is not None:
            prev.tail = (prev.tail or "") + tail
        else:
            parent.text = (parent.text or "") + tail
    parent.remove(el)


def attribute_site(operator: str, file: str, target, changes: Sequence[tuple[Any, str, str | None, str | None]],
                   **extra: Any) -> Site:
    params = dict(extra)
    params["changes"] = [{"locator": locator(e), "attribute": a, "old": old, "new": new} for e, a, old, new in changes]
    return Site(operator, file, locator(target), params)


def apply_attribute_changes(ws: Workspace, site: Site) -> list[Edit]:
    doc = read_xml(ws.path(site.file))
    edits = []
    for ch in site.params["changes"]:
        el = resolve(doc.root, ch["locator"])
        if el.get(ch["attribute"]) != ch["old"]:
            raise MutationError(f"stale site: {ch['locator']}@{ch['attribute']} is {el.get(ch['attribute'])!r}, "
                                f"expected {ch['old']!r}")
        if ch["new"] is None:
            del el.attrib[ch["attribute"]]
        else:
            el.set(ch["attribute"], ch["new"])
        edits.append(Edit(site.file, ch["locator"], ch["attribute"], ch["old"], ch["new"], "set", site.operator))
    write_xml(doc)
    return edits


# ----------------------------------------------------------------------------- semantic diff
def _norm_text(s: str | None) -> str:
    return " ".join(s.split()) if s else ""


def _content_text(el) -> str:
    return _norm_text(" ".join([el.text or ""] + [c.tail or "" for c in el]))


def signature(el) -> tuple:
    """Whitespace-, comment- and attribute-order-insensitive structure of an element."""
    return (el.tag, tuple(sorted(el.attrib.items())), _content_text(el),
            tuple(signature(c) for c in element_children(el)))


def snippet_signature(text: str | None) -> tuple | None:
    if text is None:
        return None
    try:
        return signature(etree.fromstring(text.encode("utf-8"), _parser()))
    except etree.XMLSyntaxError:
        return ("unparseable", text)


def _key(el) -> tuple:
    if el.get("id") is not None:
        return (el.tag, "id", el.get("id"))
    if el.get("name") is not None:
        return (el.tag, "name", el.get("name"))
    return (el.tag, "attrs", tuple(sorted(el.attrib.items())))


def _change(kind: str, loc: str, attribute: str | None, old: str | None, new: str | None) -> dict:
    return {"kind": kind, "locator": loc, "attribute": attribute, "old": old, "new": new}


def _diff(e1, e2, out: list[dict]) -> None:
    if e1.tag != e2.tag:
        out.append(_change("replace", locator(e1), None, snippet(e1), snippet(e2)))
        return
    for k in sorted(set(e1.attrib) | set(e2.attrib)):
        if e1.get(k) != e2.get(k):
            out.append(_change("attribute", locator(e1), k, e1.get(k), e2.get(k)))
    t1, t2 = _content_text(e1), _content_text(e2)
    if t1 != t2:
        out.append(_change("text", locator(e1), None, t1, t2))
    c1, c2 = element_children(e1), element_children(e2)
    sm = SequenceMatcher(None, [_key(c) for c in c1], [_key(c) for c in c2], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for x, y in zip(c1[i1:i2], c2[j1:j2]):
                _diff(x, y, out)
            continue
        n = min(i2 - i1, j2 - j1) if op == "replace" else 0
        for x, y in zip(c1[i1:i1 + n], c2[j1:j1 + n]):
            if x.tag == y.tag:
                _diff(x, y, out)
            else:
                out.append(_change("remove", locator(x), None, snippet(x), None))
                out.append(_change("insert", locator(y), None, None, snippet(y)))
        for x in c1[i1 + n:i2]:
            out.append(_change("remove", locator(x), None, snippet(x), None))
        for y in c2[j1 + n:j2]:
            out.append(_change("insert", locator(y), None, None, snippet(y)))


def xml_changes(before: Path, after: Path) -> list[dict]:
    """Semantic diff of two XML files (ignores whitespace, comments and attribute order).

    Locators refer to the *before* document, except for inserted elements (after document).
    A change of declared encoding is reported as kind ``encoding``.
    """
    b, a = read_xml(Path(before)), read_xml(Path(after))
    out: list[dict] = []
    if b.encoding.upper() != a.encoding.upper():
        out.append(_change("encoding", "/", None, b.encoding, a.encoding))
    _diff(b.root, a.root, out)
    return out


# ----------------------------------------------------------------------------- enforcement
def _edit_matches(e: Edit, ch: dict) -> bool:
    if e.locator != ch["locator"]:
        return False
    kind = ch["kind"]
    if kind == "attribute":
        return e.action == "set" and e.attribute == ch["attribute"] and e.old == ch["old"] and e.new == ch["new"]
    if kind == "text":
        return e.action == "text" and _norm_text(e.old) == ch["old"] and _norm_text(e.new) == ch["new"]
    if kind == "insert":
        return e.action == "insert" and snippet_signature(e.new) == snippet_signature(ch["new"])
    if kind == "remove":
        return e.action == "remove" and snippet_signature(e.old) == snippet_signature(ch["old"])
    if kind == "replace":
        return (e.action == "replace" and snippet_signature(e.old) == snippet_signature(ch["old"])
                and snippet_signature(e.new) == snippet_signature(ch["new"]))
    return False


def _check_single_target(record: VariantRecord) -> None:
    """All edits address one element, or (for operators declaring ``container_children``)
    distinct declared children of one common parent element, one edit set per child role."""
    locs = sorted({e.locator for e in record.edits})
    if len(locs) == 1:
        return
    steps = [locator_steps(l) for l in locs]
    common: list[str] = []
    for parts in zip(*steps):
        if len(set(parts)) != 1:
            break
        common.append(parts[0])
    op = REGISTRY.get(record.operator)
    roles = [_STEP_RE.match(s[-1]).group(1) if _STEP_RE.match(s[-1]) else "" for s in steps]
    allowed = getattr(op, "container_children", frozenset()) if record.kind == VariantKind.MUTANT else frozenset()
    if (len(common) >= 2 and all(len(s) == len(common) + 1 for s in steps) and all(r in allowed for r in roles)
            and len(set(roles)) == len(roles)):
        return
    raise MutationError(f"edits do not lie inside one target element: {locs}")


def _check_mutant_record(record: VariantRecord) -> OperatorBase:
    """Record-level single-fault rules for mutants (before any file is compared)."""
    op = REGISTRY.get(record.operator)
    if op is None:
        raise MutationError(f"unknown mutation operator {record.operator!r}")
    if record.family != op.family.value:
        raise MutationError(f"family {record.family!r} does not match operator family {op.family.value!r}")
    if record.model_overrides:
        # No mutation operator produces them, and load_variant would apply them silently:
        # a model_override on a mutant is an unrecorded second (or only) fault.
        raise MutationError(f"{record.operator}: mutants must not carry model_overrides "
                            f"({sorted(record.model_overrides)})")
    if set(record.exec_overrides) != set(op.exec_override_keys):  # type: ignore[attr-defined]
        raise MutationError(f"{record.operator}: exec_overrides keys {sorted(record.exec_overrides)} differ from the "
                            f"operator's {sorted(op.exec_override_keys)}")  # type: ignore[attr-defined]
    changes = record.params.get("changes")
    if changes is not None:
        declared = [(c.get("locator"), c.get("attribute"), c.get("old"), c.get("new")) for c in changes]
        recorded = [(e.locator, e.attribute, e.old, e.new) for e in record.edits]
        if declared != recorded or any(e.action != "set" for e in record.edits):
            raise MutationError(f"{record.operator}: params.changes do not match the recorded edits")
    return op  # type: ignore[return-value]


def enforce_single_operator(ref: Workspace, var: Workspace, record: VariantRecord, *,
                            ignore_patterns: Sequence[str] = ()) -> None:
    """Raise :class:`MutationError` unless ``var`` differs from ``ref`` exactly by ``record``.

    Checks: every changed file and every semantic change is covered by ``record.edits``;
    every recorded edit is present; all edits lie inside one target element of one file
    (or the record has exec_overrides only); no files were added or removed; exec
    override keys are known; recorded tree hashes match. For mutants additionally: no
    model_overrides, exactly the operator's declared exec_overrides keys, and the
    operator's own :meth:`OperatorBase.check_record` (the edits are that operator's kind
    of fault). ``ignore_patterns`` (fnmatch on relative paths) exempts only files that are
    *absent from the reference*, e.g. simulator outputs written after generation; every
    reference file is still hash-compared, and the hashes are computed over the reference
    file set. The default is fully strict.
    """
    if record.model_id != ref.model.model_id or record.model_id != var.model.model_id:
        raise MutationError(f"model mismatch: record {record.model_id}, ref {ref.model.model_id}, "
                            f"var {var.model.model_id}")
    unknown = set(record.exec_overrides) - ALLOWED_EXEC_OVERRIDES
    if unknown:
        raise MutationError(f"unknown exec_overrides keys: {sorted(unknown)}")
    model_fields = {f.name for f in dc.fields(ModelRecord)}
    if set(record.model_overrides) - model_fields:
        raise MutationError(f"unknown model_overrides keys: {sorted(set(record.model_overrides) - model_fields)}")
    if not (record.edits or record.exec_overrides or record.model_overrides):
        raise MutationError("record describes no change")
    op = _check_mutant_record(record) if record.kind == VariantKind.MUTANT else None

    m_ref = tree_manifest(ref.root)
    m_var_all = tree_manifest(var.root)
    added = sorted(p for p in set(m_var_all) - set(m_ref) if not any(fnmatch(p, g) for g in ignore_patterns))
    removed = sorted(set(m_ref) - set(m_var_all))
    if added or removed:
        raise MutationError(f"unrecorded file additions {added} / removals {removed}")
    m_var = {p: m_var_all[p] for p in m_ref}
    changed = sorted(p for p in m_ref if m_ref[p] != m_var[p])
    edit_files = sorted({e.file for e in record.edits})
    for f in changed:
        if f not in edit_files:
            raise MutationError(f"unrecorded change to file {f}")
    for f in edit_files:
        if f not in changed:
            raise MutationError(f"recorded edit to {f} is not present in the variant")

    for f in changed:
        try:
            changes = xml_changes(ref.path(f), var.path(f))
        except etree.XMLSyntaxError as exc:
            raise MutationError(f"cannot verify non-XML change to {f}: {exc}") from exc
        unused = [e for e in record.edits if e.file == f]
        for ch in changes:
            for i, e in enumerate(unused):
                if _edit_matches(e, ch):
                    del unused[i]
                    break
            else:
                raise MutationError(f"unrecorded change in {f}: {ch}")
        if unused:
            raise MutationError(f"recorded edit not found in {f}: {unused[0]}")

    if record.edits:
        if len(edit_files) != 1:
            raise MutationError(f"edits span several files: {edit_files}")
        _check_single_target(record)

    if record.tree_sha256 and record.tree_sha256 != sha256_json(m_var):
        raise MutationError("variant tree hash differs from the recorded tree_sha256 (unrecorded change)")
    if record.parent_tree_sha256 and record.parent_tree_sha256 != sha256_json(m_ref):
        raise MutationError("reference tree hash differs from the recorded parent_tree_sha256")
    if op is not None:
        op.check_record(record, ref)


# ----------------------------------------------------------------------------- generation
def site_rng(seed: int, operator: str) -> np.random.Generator:
    return np.random.default_rng([int(seed), zlib.crc32(operator.encode("utf-8"))])


def choose_sites(sites: Sequence[Site], n: int, seed: int, operator: str) -> list[Site]:
    """Sample ``n`` sites without replacement; seeding per operator keeps each operator's
    choice independent of which other operators are requested."""
    k = min(int(n), len(sites))
    if k <= 0:
        return []
    idx = site_rng(seed, operator).choice(len(sites), size=k, replace=False)
    return [sites[i] for i in sorted(int(i) for i in idx)]


def variant_id_for(model_id: str, site: Site) -> str:
    digest = sha256_json({"model_id": model_id, "operator": site.operator, "file": site.file,
                          "locator": site.locator, "params": to_jsonable(site.params)})
    return f"m-{site.operator}-{digest[:10]}"


def get_operator(name: str) -> OperatorBase:
    try:
        return REGISTRY[name]  # type: ignore[return-value]
    except KeyError:
        raise ValueError(f"unknown mutation operator {name!r}; known: {sorted(REGISTRY)}") from None


def inapplicable_sites(ws: Workspace, operators: Sequence[str]) -> list[Inapplicable]:
    out: list[Inapplicable] = []
    for name in operators:
        out.extend(get_operator(name).inapplicable(ws))
    return out


def generate_mutants(model: ModelRecord, operators: Sequence[str], n_per_operator: int, seed: int,
                     root: Path, selector: Callable[[Any, list], list] | None = None) -> list[VariantRecord]:
    """Materialize, mutate, enforce and record ``n_per_operator`` mutants per operator.

    Variants are written to ``root/<model_id>/<variant_id>/`` with ``variant.json``.
    Variant ids hash (model, operator, site), so the same site always gets the same id.
    Repeated operator names are generated once (order preserved): a repeat would rewrite
    the same directories and double-count the same mutants in the manifest.
    """
    if int(seed) < 0:
        raise ValueError("seed must be non-negative")
    ops = [get_operator(n) for n in dict.fromkeys(operators)]
    root = Path(root)
    records: list[VariantRecord] = []
    seen: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="neurosem_mutref_") as tmp:
        ref = materialize(model, Path(tmp) / "ref")
        parent_sha = ref.tree_sha256()
        for op in ops:
            sites = op.sites(ref)
            chosen = selector(op, sites) if selector else choose_sites(sites, n_per_operator, seed, op.name)
            for site in chosen:
                vid = variant_id_for(model.model_id, site)
                if vid in seen:
                    raise MutationError(f"duplicate variant id {vid} (operator {op.name} enumerated a site twice)")
                seen.add(vid)
                ws = materialize(model, root / model.model_id / vid, overwrite=True)
                edits, exec_overrides, model_overrides = op.apply(ws, site)
                rec = VariantRecord(
                    variant_id=vid, model_id=model.model_id, kind=VariantKind.MUTANT, family=op.family.value,
                    operator=op.name, params={**site.params, GENERATOR_SEED_KEY: int(seed)}, edits=list(edits),
                    exec_overrides=dict(exec_overrides), model_overrides=dict(model_overrides),
                    description=op.describe(site), parent_tree_sha256=parent_sha, tree_sha256=ws.tree_sha256(),
                    created_utc=utc_now())
                enforce_single_operator(ref, ws, rec)
                (ws.root / "variant.json").write_text(dumps(rec), encoding="utf-8")
                records.append(rec)
    return records


def load_variant(path: Path, models: dict[str, ModelRecord] | None = None) -> tuple[Workspace, VariantRecord]:
    """Load a variant directory (or its variant.json); ``model_overrides`` are applied to the ModelRecord.

    Mutant records carrying ``model_overrides`` are refused (no operator produces them, so
    applying one would silently add an unrecorded fault), as are unknown override keys.
    """
    p = Path(path)
    vdir = p.parent if p.name == "variant.json" else p
    rec = variant_from_dict(json.loads((vdir / "variant.json").read_text(encoding="utf-8")))
    models = models if models is not None else load_models()
    if rec.model_id not in models:
        raise MutationError(f"model {rec.model_id!r} not in manifest")
    model = models[rec.model_id]
    if rec.kind == VariantKind.MUTANT and rec.model_overrides:
        raise MutationError(f"mutant {rec.variant_id} carries model_overrides {sorted(rec.model_overrides)}")
    fields = {f.name for f in dc.fields(ModelRecord)}
    unknown = set(rec.model_overrides) - fields
    if unknown:
        raise MutationError(f"variant {rec.variant_id}: model_overrides keys are not ModelRecord fields: {sorted(unknown)}")
    if rec.model_overrides:
        model = dc.replace(model, **rec.model_overrides)
    return Workspace(vdir, model), rec


def _compact(obj: Any) -> str:
    return json.dumps(to_jsonable(obj), sort_keys=True, separators=(",", ":"))


def write_manifest(records: Sequence[VariantRecord], path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in records:
            params = {k: v for k, v in r.params.items() if k != GENERATOR_SEED_KEY}
            w.writerow({
                "variant_id": r.variant_id, "model_id": r.model_id, "family": r.family, "operator": r.operator,
                "params_json": _compact(params), "edits_json": _compact(r.edits),
                "exec_overrides_json": _compact(r.exec_overrides), "description": r.description,
                "generator_seed": r.params.get(GENERATOR_SEED_KEY, ""),
            })


def deepcopy_element(el):
    return copy.deepcopy(el)
