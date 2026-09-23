"""Byte-preserving XML editing shared by all valid transformations, plus the two no-change controls.

Why a custom scanner: a valid transformation must change *only* what it claims to change.
Re-serialising a file with lxml would silently rewrite quote styles, ``<a />`` spacing and
the XML declaration, so every variant would also carry unrecorded formatting edits. Instead,
every file is parsed twice: lxml gives the element tree (semantics, namespaces), and a small
quote-aware scanner gives the exact character span of each element in document order. The
two views are checked against each other, and all edits are applied as character-range
replacements on the original text.

This module also defines :class:`Site` / :class:`TransformOperator` (same shape as the
mutation operator protocol in ARCHITECTURE.md section 3.4) and the model file set used to
choose where transformations act.

Controls defined here (``VariantKind.NO_CHANGE``):

* ``xml_formatting`` -- re-indents insignificant whitespace or reverses attribute order
  (attribute order carries no meaning in XML).
* ``add_comments`` -- inserts XML comments.
"""

from __future__ import annotations

import dataclasses as dc
import os
import re
from collections import deque
from collections.abc import Iterable
from itertools import pairwise
from pathlib import Path
from typing import Any, Protocol

from lxml import etree

from nexclamp.models import Workspace
from nexclamp.schemas import Edit, VariantKind

# --------------------------------------------------------------------------- protocol


@dc.dataclass(frozen=True)
class Site:
    """One concrete place a transform can act (mirrors ``mutations.base.Site``)."""

    operator: str
    file: str                      # relative POSIX path inside the workspace
    locator: str                   # XPath-like locator, see :meth:`XmlDoc.locator`
    params: dict[str, Any]


class TransformOperator(Protocol):
    name: str
    family: str                    # transform category (stored in VariantRecord.family)
    kind: VariantKind              # VALID_TRANSFORM or NO_CHANGE

    def sites(self, ws: Workspace) -> list[Site]: ...

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]: ...

    def describe(self, site: Site) -> str: ...


class TransformError(RuntimeError):
    """A transform could not be applied exactly as its site describes."""


# --------------------------------------------------------------------------- scanning

_ENCODING_RE = re.compile(rb'^\s*<\?xml[^>]*?encoding\s*=\s*["\']([A-Za-z0-9._-]+)["\']')
_NAME_RE = re.compile(r"[^\s/>]+")
_ATTR_RE = re.compile(r"""(\s+)([^\s=/>"']+)(\s*=\s*)("[^"]*"|'[^']*')""")
_LOCATOR_STEP_RE = re.compile(r"/([^/\[\]]+)(?:\[(?:@([\w:.-]+)='([^']*)'|(\d+))\])?")
LOCATOR_KEYS = ("id", "name", "href", "file")


@dc.dataclass(frozen=True)
class ElementSpan:
    start: int                     # offset of '<'
    tag_end: int                   # offset just past the start tag's '>'
    end: int                       # offset just past the end tag ('== tag_end' if self-closing)
    qname: str
    self_closing: bool
    depth: int                     # number of open ancestors


@dc.dataclass(frozen=True)
class Token:
    kind: str                      # start | empty | end | text | comment | pi | cdata | doctype
    start: int
    end: int
    depth: int                     # open elements before this token
    parent: int | None             # element index enclosing this token (None outside the root)
    element: int | None = None     # element index for start/empty/end tokens


def scan(text: str) -> tuple[list[ElementSpan], list[Token]]:
    """Quote-aware scan of an XML document into element spans (document order) and tokens."""
    spans: list[list[Any]] = []
    tokens: list[Token] = []
    stack: list[int] = []
    i, n = 0, len(text)
    while i < n:
        j = text.find("<", i)
        if j < 0:
            tokens.append(Token("text", i, n, len(stack), stack[-1] if stack else None))
            break
        if j > i:
            tokens.append(Token("text", i, j, len(stack), stack[-1] if stack else None))
        parent = stack[-1] if stack else None
        if text.startswith("<!--", j):
            k = text.find("-->", j + 4)
            if k < 0:
                raise ValueError("unterminated comment")
            end, kind = k + 3, "comment"
            tokens.append(Token(kind, j, end, len(stack), parent))
        elif text.startswith("<![CDATA[", j):
            k = text.find("]]>", j)
            if k < 0:
                raise ValueError("unterminated CDATA section")
            end = k + 3
            tokens.append(Token("cdata", j, end, len(stack), parent))
        elif text.startswith("<?", j):
            k = text.find("?>", j)
            if k < 0:
                raise ValueError("unterminated processing instruction")
            end = k + 2
            tokens.append(Token("pi", j, end, len(stack), parent))
        elif text.startswith("<!", j):
            k = text.find(">", j)
            if k < 0 or "[" in text[j:k]:
                raise ValueError("DOCTYPE with internal subset is not supported")
            end = k + 1
            tokens.append(Token("doctype", j, end, len(stack), parent))
        elif text.startswith("</", j):
            k = text.find(">", j)
            if k < 0 or not stack:
                raise ValueError(f"unbalanced end tag at offset {j}")
            name = text[j + 2:k].strip()
            idx = stack.pop()
            if spans[idx][3] != name:
                raise ValueError(f"end tag </{name}> does not close <{spans[idx][3]}>")
            end = k + 1
            spans[idx][2] = end
            tokens.append(Token("end", j, end, len(stack) + 1, stack[-1] if stack else None, idx))
        else:
            k, quote = j + 1, ""
            while k < n:
                c = text[k]
                if quote:
                    if c == quote:
                        quote = ""
                elif c in "\"'":
                    quote = c
                elif c == ">":
                    break
                k += 1
            if k >= n:
                raise ValueError(f"unterminated start tag at offset {j}")
            m = _NAME_RE.match(text, j + 1)
            if m is None:
                raise ValueError(f"malformed start tag at offset {j}")
            self_closing = text[j:k].rstrip().endswith("/")
            end = k + 1
            idx = len(spans)
            spans.append([j, end, end if self_closing else None, m.group(0), self_closing, len(stack)])
            tokens.append(Token("empty" if self_closing else "start", j, end, len(stack), parent, idx))
            if not self_closing:
                stack.append(idx)
        i = end
    if stack:
        raise ValueError("document ends with unclosed elements")
    return [ElementSpan(*s) for s in spans], tokens


def local_name(el: etree._Element) -> str:
    return etree.QName(el).localname


def namespace(el: etree._Element) -> str | None:
    return etree.QName(el).namespace


def _decode(data: bytes) -> tuple[str, str, bool]:
    bom = data.startswith(b"\xef\xbb\xbf")
    if bom:
        data = data[3:]
    m = _ENCODING_RE.match(data[:300])
    encoding = m.group(1).decode("ascii") if m else "utf-8"
    return data.decode(encoding), encoding, bom


_PARSER = etree.XMLParser(remove_blank_text=False, remove_comments=False, remove_pis=False,
                          resolve_entities=False, no_network=True, load_dtd=False, huge_tree=True)


@dc.dataclass
class XmlDoc:
    """One XML file: original text, lxml tree and exact element spans (same document order)."""

    rel: str
    text: str
    encoding: str
    bom: bool
    root: etree._Element
    elements: list[etree._Element]
    spans: list[ElementSpan]
    tokens: list[Token]
    path: Path | None = None

    @classmethod
    def load(cls, ws_root: Path, rel: str) -> XmlDoc:
        path = Path(ws_root) / rel
        text, encoding, bom = _decode(path.read_bytes())
        return cls.from_text(text, rel, encoding, bom, path)

    @classmethod
    def from_text(cls, text: str, rel: str = "", encoding: str = "utf-8", bom: bool = False,
                  path: Path | None = None) -> XmlDoc:
        root = etree.fromstring(text.encode(encoding), _PARSER)
        elements = [e for e in root.iter() if isinstance(e.tag, str)]
        spans, tokens = scan(text)
        if len(spans) != len(elements):
            raise ValueError(f"{rel}: scanner found {len(spans)} elements, lxml {len(elements)}")
        for sp, el in zip(spans, elements):
            if sp.qname.rsplit(":", 1)[-1] != local_name(el):
                raise ValueError(f"{rel}: scanner/lxml mismatch at <{sp.qname}> vs <{local_name(el)}>")
        return cls(rel, text, encoding, bom, root, elements, spans, tokens, path)

    # ------------------------------------------------------------------ facts
    @property
    def newline(self) -> str:
        return "\r\n" if "\r\n" in self.text else "\n"

    @property
    def root_name(self) -> str:
        return local_name(self.root)

    def index(self, el: etree._Element) -> int:
        for i, e in enumerate(self.elements):
            if e is el:
                return i
        raise KeyError("element not in document")

    def span(self, el: etree._Element) -> ElementSpan:
        return self.spans[self.index(el)]

    def children(self, el: etree._Element) -> list[etree._Element]:
        return [c for c in el if isinstance(c.tag, str)]

    # --------------------------------------------------------------- locators
    def locator(self, el: etree._Element) -> str:
        """XPath-like locator using local names, e.g. ``/neuroml/cell[@id='RS']/morphology[1]``."""
        steps = []
        e: etree._Element | None = el
        while e is not None:
            parent = e.getparent()
            name = local_name(e)
            if parent is None:
                steps.append(name)
            else:
                sibs = [c for c in parent if isinstance(c.tag, str) and local_name(c) == name]
                step = ""
                for key in LOCATOR_KEYS:
                    v = e.get(key)
                    if v is not None and "'" not in v and sum(1 for s in sibs if s.get(key) == v) == 1:
                        step = f"{name}[@{key}='{v}']"
                        break
                steps.append(step or f"{name}[{sibs.index(e) + 1}]")
            e = parent
        return "/" + "/".join(reversed(steps))

    def find(self, locator: str) -> etree._Element:
        pos, cur = 0, None
        for m in _LOCATOR_STEP_RE.finditer(locator):
            if m.start() != pos:
                break
            pos = m.end()
            name, key, val, num = m.groups()
            if cur is None:
                if local_name(self.root) != name:
                    raise TransformError(f"{self.rel}: locator root {name!r} does not match {self.root_name!r}")
                cur = self.root
                continue
            sibs = [c for c in cur if isinstance(c.tag, str) and local_name(c) == name]
            if key:
                hits = [c for c in sibs if c.get(key) == val]
                if len(hits) != 1:
                    raise TransformError(f"{self.rel}: locator step {m.group(0)!r} matched {len(hits)} elements")
                cur = hits[0]
            else:
                k = int(num) if num else 1
                if not 1 <= k <= len(sibs):
                    raise TransformError(f"{self.rel}: locator step {m.group(0)!r} out of range")
                cur = sibs[k - 1]
        if cur is None or pos != len(locator):
            raise TransformError(f"{self.rel}: malformed locator {locator!r}")
        return cur

    # ------------------------------------------------------------ attributes
    def text_attr_name(self, el: etree._Element, key: str) -> str:
        if not key.startswith("{"):
            return key
        ns, local = key[1:].split("}", 1)
        prefixes = [p for p, uri in el.nsmap.items() if uri == ns and p]
        if not prefixes:
            raise TransformError(f"no prefix bound for namespace {ns}")
        return f"{prefixes[0]}:{local}"

    def attr_value_range(self, el: etree._Element, key: str) -> tuple[int, int, str] | None:
        """(start, end, quote) of the attribute *value* characters inside the start tag, or None."""
        sp = self.span(el)
        name = self.text_attr_name(el, key)
        tag = self.text[sp.start:sp.tag_end]
        for m in _ATTR_RE.finditer(tag):
            if m.group(2) == name:
                q = m.group(4)[0]
                vstart = sp.start + m.start(4) + 1
                return vstart, vstart + len(m.group(4)) - 2, q
        return None

    def set_attr_change(self, el: etree._Element, key: str, value: str) -> tuple[int, int, str]:
        """Character-range replacement that sets (or appends) one attribute."""
        found = self.attr_value_range(el, key)
        if found:
            start, end, q = found
            return start, end, escape_attr(value, q)
        sp = self.span(el)
        body_end = sp.tag_end - (2 if sp.self_closing else 1)
        p = body_end
        while self.text[p - 1].isspace():
            p -= 1
        return p, p, f' {self.text_attr_name(el, key)}="{escape_attr(value, chr(34))}"'

    # ------------------------------------------------------------------- misc
    def line_start(self, offset: int) -> int:
        return self.text.rfind("\n", 0, offset) + 1

    def indentation_before(self, offset: int) -> str | None:
        """Whitespace between the start of the line and ``offset``, or None if other text precedes."""
        ls = self.line_start(offset)
        prefix = self.text[ls:offset]
        return prefix if prefix.strip() == "" else None

    def encode(self, text: str) -> bytes:
        return (b"\xef\xbb\xbf" if self.bom else b"") + text.encode(self.encoding)


def escape_attr(value: str, quote: str) -> str:
    out = value.replace("&", "&amp;").replace("<", "&lt;")
    return out.replace('"', "&quot;") if quote == '"' else out.replace("'", "&apos;")


def replace_ranges(text: str, changes: Iterable[tuple[int, int, str]]) -> str:
    ordered = sorted(changes, key=lambda c: (c[0], c[1]))
    for (_s1, e1, _), (s2, _e2, _) in pairwise(ordered):
        if s2 < e1:
            raise TransformError("overlapping text edits")
    out = text
    for s, e, new in reversed(ordered):
        out = out[:s] + new + out[e:]
    return out


def write_doc(ws_root: Path, doc: XmlDoc, text: str) -> XmlDoc:
    """Write ``text`` to the document's file (same encoding) after checking it still parses."""
    new = XmlDoc.from_text(text, doc.rel, doc.encoding, doc.bom, Path(ws_root) / doc.rel)
    (Path(ws_root) / doc.rel).write_bytes(doc.encode(text))
    return new


# ----------------------------------------------------------------- model file set


def xml_files(ws: Workspace) -> list[str]:
    root = Path(ws.root)
    out = [p.relative_to(root).as_posix() for p in root.rglob("*")
           if p.is_file() and p.suffix.lower() in (".nml", ".xml")]
    return sorted(out)


def include_targets(ws: Workspace, doc: XmlDoc) -> list[str]:
    """Workspace files included by ``doc`` (NeuroML ``<include href>``, LEMS ``<Include file>``).

    Includes that do not resolve inside the workspace (e.g. jLEMS core ``Cells.xml``) are skipped.
    """
    refs: list[str] = []
    if doc.root_name == "neuroml":
        refs += [c.get("href") for c in doc.children(doc.root) if local_name(c) == "include" and c.get("href")]
    refs += [e.get("file") for e in doc.elements if local_name(e) == "Include" and e.get("file")]
    root = Path(ws.root).resolve()
    base = (root / doc.rel).parent
    out = []
    for r in refs:
        target = Path(os.path.normpath(base / r))
        try:
            rel = target.resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        if (root / rel).is_file() and rel not in out:
            out.append(rel)
    return out


def load_docs(ws: Workspace, files: Iterable[str] | None = None) -> dict[str, XmlDoc]:
    return {rel: XmlDoc.load(ws.root, rel) for rel in (xml_files(ws) if files is None else files)}


def include_graph(ws: Workspace, docs: dict[str, XmlDoc] | None = None) -> dict[str, list[str]]:
    docs = docs if docs is not None else load_docs(ws)
    return {rel: include_targets(ws, d) for rel, d in docs.items()}


def closure(graph: dict[str, list[str]], starts: Iterable[str]) -> list[str]:
    """Files reachable from ``starts`` (inclusive), in breadth-first order."""
    seen: list[str] = []
    queue = deque(s for s in starts)
    while queue:
        f = queue.popleft()
        if f in seen:
            continue
        seen.append(f)
        queue.extend(graph.get(f, []))
    return seen


def ancestors(graph: dict[str, list[str]], target: str) -> list[str]:
    """Files that include ``target`` directly or transitively (exclusive)."""
    reverse: dict[str, list[str]] = {}
    for f, tgts in graph.items():
        for t in tgts:
            reverse.setdefault(t, []).append(f)
    return [f for f in closure(reverse, [target]) if f != target]


def model_files(ws: Workspace, docs: dict[str, XmlDoc] | None = None) -> list[str]:
    """The files a simulation of this model reads: closure of the cell file and the shipped harness."""
    graph = include_graph(ws, docs)
    return sorted(closure(graph, [ws.model.cell_file, ws.model.harness_lems]))


# ------------------------------------------------------------------- no-change controls

_NOCHANGE_COMMENT = "NeuroSem no-change control comment"


class XmlFormatting:
    """Change insignificant whitespace or attribute order in one file (a no-change control).

    Only whitespace-only text runs that contain a line break and sit between child elements
    are re-indented; text inside elements without child elements (e.g. ``<notes>``) and in
    mixed-content elements is left untouched because it is character data, not layout.
    """

    name = "xml_formatting"
    family = "formatting"
    kind = VariantKind.NO_CHANGE
    styles = ("reindent", "attribute_order")

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel in model_files(ws):
            doc = XmlDoc.load(ws.root, rel)
            for style in self.styles:
                if self.render(doc, style) != doc.text:
                    out.append(Site(self.name, rel, "/" + doc.root_name, {"style": style}))
        return out

    def render(self, doc: XmlDoc, style: str) -> str:
        if style == "reindent":
            return _reindent(doc)
        if style == "attribute_order":
            return _reverse_attributes(doc)
        raise ValueError(f"unknown xml_formatting style {style!r}")

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        doc = XmlDoc.load(ws.root, site.file)
        new = self.render(doc, site.params["style"])
        if new == doc.text:
            raise TransformError(f"{site.file}: style {site.params['style']} changes nothing")
        write_doc(ws.root, doc, new)
        return [Edit(site.file, site.locator, None, None, None, "text",
                     f"xml_formatting style={site.params['style']} (whitespace/attribute order only)")], {}, {}

    def describe(self, site: Site) -> str:
        return f"XML formatting ({site.params['style']}) of {site.file}; no semantic change"


def _reindent(doc: XmlDoc) -> str:
    unit = "  " if f"{doc.newline}    <" in doc.text else "    "
    has_child = [False] * len(doc.spans)
    mixed = [False] * len(doc.spans)
    for tok in doc.tokens:
        if tok.parent is None:
            continue
        if tok.kind in ("start", "empty", "comment", "pi", "cdata"):
            has_child[tok.parent] = True
        if tok.kind == "text" and doc.text[tok.start:tok.end].strip():
            mixed[tok.parent] = True
        if tok.kind == "cdata":
            mixed[tok.parent] = True
    changes = []
    for i, tok in enumerate(doc.tokens):
        if tok.kind != "text" or tok.parent is None:
            continue
        chunk = doc.text[tok.start:tok.end]
        if chunk.strip() or "\n" not in chunk or mixed[tok.parent] or not has_child[tok.parent]:
            continue
        nxt = doc.tokens[i + 1] if i + 1 < len(doc.tokens) else None
        level = tok.depth - 1 if nxt is not None and nxt.kind == "end" else tok.depth
        changes.append((tok.start, tok.end, doc.newline + unit * level))
    return replace_ranges(doc.text, changes)


def _reverse_attributes(doc: XmlDoc) -> str:
    changes = []
    for sp in doc.spans:
        tag = doc.text[sp.start:sp.tag_end]
        m = _NAME_RE.match(tag, 1)
        close = 2 if sp.self_closing else 1
        body = tag[m.end():len(tag) - close]
        attrs = list(_ATTR_RE.finditer(body))
        if len(attrs) < 2 or attrs[0].start() != 0:
            continue
        if any(a.start() != b.end() for b, a in pairwise(attrs)):
            continue
        trailing = body[attrs[-1].end():]
        if trailing.strip():
            continue
        seps = [a.group(1) for a in attrs]
        items = [a.group(2) + a.group(3) + a.group(4) for a in attrs][::-1]
        new_body = "".join(s + it for s, it in zip(seps, items)) + trailing
        changes.append((sp.start + m.end(), sp.tag_end - close, new_body))
    return replace_ranges(doc.text, changes)


class AddComments:
    """Insert XML comments inside the root element of one file (a no-change control)."""

    name = "add_comments"
    family = "formatting"
    kind = VariantKind.NO_CHANGE
    positions = ("root_start", "before_each_child", "before_root_end")

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel in model_files(ws):
            doc = XmlDoc.load(ws.root, rel)
            for pos in self.positions:
                if pos == "before_each_child" and not doc.children(doc.root):
                    continue
                out.append(Site(self.name, rel, "/" + doc.root_name, {"position": pos}))
        return out

    def render(self, doc: XmlDoc, position: str) -> tuple[str, int]:
        nl = doc.newline
        root = doc.spans[0]
        kids = doc.children(doc.root)
        first_indent = doc.indentation_before(doc.span(kids[0]).start) if kids else None
        indent = first_indent if first_indent else "    "
        changes = []
        if position == "root_start":
            changes.append((root.tag_end, root.tag_end, f"{nl}{indent}<!-- {_NOCHANGE_COMMENT} (root start) -->"))
        elif position == "before_each_child":
            for kid in kids:
                sp = doc.span(kid)
                comment = f"<!-- {_NOCHANGE_COMMENT} (before {local_name(kid)}) -->"
                ind = doc.indentation_before(sp.start)
                if ind is not None:
                    ls = doc.line_start(sp.start)
                    changes.append((ls, ls, f"{ind}{comment}{nl}"))
                else:
                    changes.append((sp.start, sp.start, comment))
        elif position == "before_root_end":
            end_start = doc.text.rfind("</", 0, root.end)
            changes.append((end_start, end_start, f"{indent}<!-- {_NOCHANGE_COMMENT} (root end) -->{nl}"))
        else:
            raise ValueError(f"unknown add_comments position {position!r}")
        return replace_ranges(doc.text, changes), len(changes)

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        doc = XmlDoc.load(ws.root, site.file)
        new, count = self.render(doc, site.params["position"])
        write_doc(ws.root, doc, new)
        return [Edit(site.file, site.locator, None, None, f"{count} comment(s)", "insert",
                     f"add_comments position={site.params['position']}")], {}, {}

    def describe(self, site: Site) -> str:
        return f"XML comments inserted ({site.params['position']}) in {site.file}; no semantic change"
