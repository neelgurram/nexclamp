"""Schema-grounded transforms: unit conversion, numeric literal formatting, explicit defaults.

Every fact about what is *allowed* comes from files installed in the environment, never from
memory:

* attribute types, unit strings and default values come from the NeuroML v2.3.1 XSD shipped
  inside libNeuroML (``neuroml/nml/NeuroML_v2.3.1.xsd``);
* unit scale factors come from ``NeuroML2CoreTypes/NeuroMLCoreDimensions.xml`` inside the
  jNeuroML jar that pyNeuroML ships, i.e. the definitions jLEMS itself uses.

Unit conversion is done with :class:`decimal.Decimal` so the written literal is the *exact*
decimal value of the original quantity in the new unit. Exactness is at the level of the
text only: the simulator parses each literal to a binary double and then scales it by the
unit's power of ten, and the product of two rounded doubles need not be the double nearest
to the exact result. So ``0.07 mS_per_cm2`` and ``0.7 S_per_m2`` can become SI values that
differ in their last bits, and fixed-step integration of a spiking model can amplify such a
difference. That residual is exactly what these controls are meant to measure.
"""

from __future__ import annotations

import dataclasses as dc
import functools
import importlib.util
import re
import zipfile
from decimal import Decimal, Inexact, InvalidOperation, localcontext
from pathlib import Path

from lxml import etree

from nexclamp.models import Workspace
from nexclamp.schemas import Edit, VariantKind
from nexclamp.transforms.formatting import (
    Site,
    TransformError,
    XmlDoc,
    load_docs,
    local_name,
    model_files,
    namespace,
    replace_ranges,
    write_doc,
)

XS = "{http://www.w3.org/2001/XMLSchema}"
XSD_NAME = "NeuroML_v2.3.1.xsd"
CORE_DIMENSIONS = "NeuroML2CoreTypes/NeuroMLCoreDimensions.xml"
_NUMERIC_BASES = ("xs:double", "xs:float", "xs:decimal")


def xsd_path() -> Path:
    """Location of the v2.3.1 schema inside the installed libNeuroML package (not imported)."""
    spec = importlib.util.find_spec("neuroml")
    if spec is None or not spec.submodule_search_locations:
        raise RuntimeError("libNeuroML (package 'neuroml') is not installed")
    path = Path(next(iter(spec.submodule_search_locations))) / "nml" / XSD_NAME
    if not path.is_file():
        raise RuntimeError(f"{XSD_NAME} not found in the installed libNeuroML package ({path})")
    return path


# ------------------------------------------------------------------------ XSD index


@dc.dataclass(frozen=True)
class AttributeDecl:
    name: str
    type: str
    default: str | None
    use: str


@dc.dataclass(frozen=True)
class QuantityType:
    """An ``Nml2Quantity*`` simple type: its XSD pattern and the unit strings the pattern allows."""

    name: str
    pattern: str
    units: tuple[str, ...]

    @functools.cached_property
    def regex(self) -> re.Pattern[str]:
        return re.compile(self.pattern)          # XSD patterns are implicitly anchored: use fullmatch

    def matches(self, text: str) -> bool:
        return self.regex.fullmatch(text) is not None


@dc.dataclass
class ComplexTypeDecl:
    name: str
    base: str | None
    attributes: dict[str, AttributeDecl]
    children: dict[str, str | None]            # element name -> type (None if declared ambiguously)


class XsdIndex:
    """Just enough of the NeuroML XSD to type elements in context and read attribute declarations."""

    def __init__(self, path: Path) -> None:
        self.path = path
        tree = etree.parse(str(path))
        schema = tree.getroot()
        self.target_namespace: str = schema.get("targetNamespace", "")
        self.simple_bases: dict[str, str] = {}
        self.quantity_types: dict[str, QuantityType] = {}
        for st in schema.findall(f"{XS}simpleType"):
            name = st.get("name")
            restr = st.find(f"{XS}restriction")
            if not name or restr is None:
                continue
            self.simple_bases[name] = restr.get("base", "")
            pat = restr.find(f"{XS}pattern")
            if name.startswith("Nml2Quantity") and pat is not None:
                pattern = pat.get("value")
                m = re.search(r"\(([A-Za-z0-9_|]+)\)$", pattern)
                units = tuple(m.group(1).split("|")) if m else ()
                self.quantity_types[name] = QuantityType(name, pattern, units)
        self._groups = {g.get("name"): g for g in schema.findall(f"{XS}group") if g.get("name")}
        self._attr_groups = {g.get("name"): g for g in schema.findall(f"{XS}attributeGroup") if g.get("name")}
        self.complex_types: dict[str, ComplexTypeDecl] = {}
        for ct in schema.findall(f"{XS}complexType"):
            name = ct.get("name")
            if not name:
                continue
            base = None
            for tag in ("extension", "restriction"):
                node = ct.find(f"{XS}complexContent/{XS}{tag}")
                if node is None:
                    node = ct.find(f"{XS}simpleContent/{XS}{tag}")
                if node is not None:
                    base = node.get("base")
                    break
            decl = ComplexTypeDecl(name, base, {}, {})
            self._collect(ct, decl)
            self.complex_types[name] = decl
        self.root_elements = {e.get("name"): e.get("type") for e in schema.findall(f"{XS}element")
                              if e.get("name") and e.get("type")}

    def _collect(self, node: etree._Element, decl: ComplexTypeDecl) -> None:
        for child in node:
            if not isinstance(child.tag, str):
                continue
            if child.tag == f"{XS}element":
                name, typ = child.get("name"), child.get("type")
                if name and typ:
                    if name in decl.children and decl.children[name] != typ:
                        decl.children[name] = None
                    else:
                        decl.children[name] = typ
                continue                          # never descend into local element declarations
            if child.tag == f"{XS}complexType":
                continue
            if child.tag == f"{XS}attribute" and child.get("name"):
                decl.attributes[child.get("name")] = AttributeDecl(
                    child.get("name"), child.get("type", ""), child.get("default"), child.get("use", "optional"))
                continue
            if child.tag == f"{XS}group" and child.get("ref") in self._groups:
                self._collect(self._groups[child.get("ref")], decl)
                continue
            if child.tag == f"{XS}attributeGroup" and child.get("ref") in self._attr_groups:
                self._collect(self._attr_groups[child.get("ref")], decl)
                continue
            self._collect(child, decl)

    # ------------------------------------------------------------------ queries
    def group_elements(self, group: str) -> tuple[str, ...]:
        g = self._groups.get(group)
        if g is None:
            return ()
        decl = ComplexTypeDecl(group, None, {}, {})
        self._collect(g, decl)
        return tuple(decl.children)

    def _chain(self, type_name: str) -> list[ComplexTypeDecl]:
        out, seen = [], set()
        t: str | None = type_name
        while t and t in self.complex_types and t not in seen:
            seen.add(t)
            out.append(self.complex_types[t])
            t = self.complex_types[t].base
        return out

    def attributes(self, type_name: str) -> dict[str, AttributeDecl]:
        merged: dict[str, AttributeDecl] = {}
        for decl in reversed(self._chain(type_name)):
            merged.update(decl.attributes)
        return merged

    def children(self, type_name: str) -> dict[str, str | None]:
        merged: dict[str, str | None] = {}
        for decl in reversed(self._chain(type_name)):
            merged.update(decl.children)
        return merged

    def child_type(self, parent_type: str, child: str) -> str | None:
        for decl in self._chain(parent_type):
            if child in decl.children:
                return decl.children[child]
        return None

    def numeric_base(self, type_name: str) -> str | None:
        t, seen = type_name, set()
        while t and t not in seen:
            if t in _NUMERIC_BASES:
                return t
            seen.add(t)
            t = self.simple_bases.get(t, "")
        return None

    def type_document(self, doc: XmlDoc) -> list[str | None]:
        """XSD complex type of every element of a NeuroML document (None = not described by the XSD)."""
        types: list[str | None] = [None] * len(doc.elements)
        if doc.root_name != "neuroml" or namespace(doc.root) not in (self.target_namespace, None):
            return types
        pos = {id(e): i for i, e in enumerate(doc.elements)}
        for i, el in enumerate(doc.elements):
            if namespace(el) not in (self.target_namespace, None):
                continue
            parent = el.getparent()
            if parent is None:
                types[i] = self.root_elements.get(local_name(el))
                continue
            ptype = types[pos[id(parent)]]
            types[i] = self.child_type(ptype, local_name(el)) if ptype else None
        return types


@functools.cache
def xsd_index() -> XsdIndex:
    return XsdIndex(xsd_path())


# ----------------------------------------------------------------- unit definitions


@dc.dataclass(frozen=True)
class CoreUnit:
    symbol: str
    dimension: str
    power: int
    scale: Decimal
    offset: Decimal

    @property
    def factor(self) -> Decimal:
        """Multiplier to the dimension's SI unit (exact decimal)."""
        return self.scale.scaleb(self.power)


@functools.cache
def core_units() -> dict[str, CoreUnit]:
    """Unit definitions from ``NeuroMLCoreDimensions.xml`` inside the installed jNeuroML jar."""
    from nexclamp.simulators.jneuroml import find_jar

    jar = find_jar()
    if jar is None:
        raise RuntimeError("jNeuroML jar not found; unit factors are read from its NeuroMLCoreDimensions.xml")
    with zipfile.ZipFile(jar) as z:
        root = etree.fromstring(z.read(CORE_DIMENSIONS))
    out = {}
    for u in root.iter():
        if isinstance(u.tag, str) and etree.QName(u).localname == "Unit" and u.get("symbol"):
            out[u.get("symbol")] = CoreUnit(u.get("symbol"), u.get("dimension", ""), int(u.get("power", "0")),
                                            Decimal(u.get("scale", "1")), Decimal(u.get("offset", "0")))
    return out


# ------------------------------------------------------------------ number handling

_NUMBER_UNIT_RE = re.compile(r"(-?[0-9]*(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?)(\s*)([A-Za-z_][A-Za-z0-9_]*)?")
_PLAIN_NUMBER_RE = re.compile(r"-?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?")


@dc.dataclass(frozen=True)
class Literal:
    number: str
    space: str
    unit: str

    @property
    def value(self) -> Decimal:
        return Decimal(self.number)

    def text(self) -> str:
        return f"{self.number}{self.space}{self.unit}"


def parse_literal(text: str) -> Literal | None:
    m = _NUMBER_UNIT_RE.fullmatch(text)
    if not m or not _PLAIN_NUMBER_RE.fullmatch(m.group(1)):
        return None
    return Literal(m.group(1), m.group(2), m.group(3) or "")


def format_decimal(d: Decimal, allow_exponent: bool = True) -> str:
    """Shortest plain/exponent decimal text for ``d`` that NeuroML's XSD number pattern accepts.

    The XSD pattern has no ``+`` in exponents and no bare trailing ``.``, so neither is emitted.
    """
    if not d.is_finite():
        raise ValueError("non-finite value")
    sign = "-" if d.is_signed() else ""
    if d.is_zero():
        return f"{sign}0"
    d = d.normalize()
    _, digits, exp = d.as_tuple()
    ds = "".join(map(str, digits))
    adjusted = d.adjusted()
    if not allow_exponent or -6 <= adjusted <= 12:
        if exp >= 0:
            return sign + ds + "0" * exp
        point = len(ds) + exp
        if point > 0:
            return f"{sign}{ds[:point]}.{ds[point:]}"
        return f"{sign}0.{'0' * -point}{ds}"
    mant = ds[0] + (f".{ds[1:]}" if len(ds) > 1 else "")
    return f"{sign}{mant}e{adjusted}"


def convert_literal(text: str, target_unit: str, qtype: QuantityType) -> str | None:
    """Exact decimal conversion of a quantity literal to ``target_unit``; None if not exactly possible."""
    lit = parse_literal(text)
    units = core_units()
    if lit is None or not lit.unit or target_unit == lit.unit:
        return None
    if lit.unit not in qtype.units or target_unit not in qtype.units:
        return None
    src, dst = units.get(lit.unit), units.get(target_unit)
    if src is None or dst is None or src.dimension != dst.dimension or src.offset != 0 or dst.offset != 0:
        return None
    with localcontext() as ctx:
        ctx.prec = 80
        ctx.traps[Inexact] = True
        try:
            value = lit.value * src.factor / dst.factor
        except (Inexact, InvalidOperation):
            return None
    new = f"{format_decimal(value)}{lit.space}{target_unit}"
    if not qtype.matches(new) or Decimal(parse_literal(new).number) * dst.factor != lit.value * src.factor:
        return None
    return new


def si_value(text: str) -> Decimal:
    """Exact SI value of a NeuroML quantity literal (offset units included)."""
    lit = parse_literal(text)
    if lit is None:
        raise ValueError(f"not a quantity literal: {text!r}")
    if not lit.unit:
        return lit.value
    u = core_units()[lit.unit]
    return lit.value * u.factor + u.offset


# -------------------------------------------------------------------- site iteration


def _typed_attributes(ws: Workspace, files: list[str] | None = None):
    """Yield (doc, element, type_name, attribute decls) for XSD-typed elements of NeuroML model files."""
    xsd = xsd_index()
    docs = load_docs(ws, files if files is not None else model_files(ws))
    for rel in sorted(docs):
        doc = docs[rel]
        if doc.root_name != "neuroml":
            continue
        for el, typ in zip(doc.elements, xsd.type_document(doc)):
            if typ:
                yield doc, el, typ, xsd.attributes(typ)


def _set_one(ws: Workspace, site: Site, attribute: str, expected_old: str | None, new: str,
             note: str) -> tuple[list[Edit], dict, dict]:
    doc = XmlDoc.load(ws.root, site.file)
    el = doc.find(site.locator)
    old = el.get(attribute)
    if old != expected_old:
        raise TransformError(f"{site.file}{site.locator}@{attribute}: expected {expected_old!r}, found {old!r}")
    write_doc(ws.root, doc, replace_ranges(doc.text, [doc.set_attr_change(el, attribute, new)]))
    return [Edit(site.file, site.locator, attribute, old, new, "set", note)], {}, {}


class UnitConversion:
    """Rewrite one quantity in another unit allowed by the XSD pattern of its type, exactly."""

    name = "unit_conversion"
    family = "unit_conversion"
    kind = VariantKind.VALID_TRANSFORM

    def sites(self, ws: Workspace) -> list[Site]:
        xsd = xsd_index()
        out = []
        for doc, el, _typ, attrs in _typed_attributes(ws):
            for attr, value in el.attrib.items():
                decl = attrs.get(attr)
                qtype = xsd.quantity_types.get(decl.type) if decl else None
                if qtype is None or len(qtype.units) < 2 or not qtype.matches(value):
                    continue
                for unit in qtype.units:
                    new = convert_literal(value, unit, qtype)
                    if new is not None:
                        out.append(Site(self.name, doc.rel, doc.locator(el),
                                        {"attribute": attr, "old": value, "new": new, "to_unit": unit,
                                         "xsd_type": qtype.name}))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        p = site.params
        qtype = xsd_index().quantity_types[p["xsd_type"]]
        new = convert_literal(p["old"], p["to_unit"], qtype)
        if new != p["new"]:
            raise TransformError(f"conversion of {p['old']!r} to {p['to_unit']} is not reproducible")
        return _set_one(ws, site, p["attribute"], p["old"], new,
                        f"exact decimal unit conversion ({p['xsd_type']})")

    def describe(self, site: Site) -> str:
        p = site.params
        return f"{site.file}{site.locator}@{p['attribute']}: {p['old']} -> {p['new']} (same SI value)"


class NumericLiteralFormat:
    """Rewrite one numeric literal in a numerically identical spelling.

    Styles: ``scientific`` (``0.1`` -> ``1e-1``), ``plain`` (no exponent), ``padded`` (one
    extra trailing zero) and ``unit_spacing`` (toggle the optional space before the unit).
    Applies to ``Nml2Quantity*`` attributes and to attributes whose XSD type derives from
    ``xs:double``/``xs:float``/``xs:decimal``; integer-typed attributes are excluded because
    ``3.0`` is not a valid integer literal.
    """

    name = "numeric_literal_format"
    family = "literal_format"
    kind = VariantKind.VALID_TRANSFORM
    styles = ("scientific", "plain", "padded", "unit_spacing")

    @staticmethod
    def restyle(text: str, style: str) -> str | None:
        lit = parse_literal(text)
        if lit is None:
            return None
        value = lit.value
        num = lit.number
        if style == "scientific":
            if value.is_zero() or value.adjusted() == 0:
                return None                       # avoid 'e0' spellings
            d = value.normalize()
            ds = "".join(map(str, d.as_tuple().digits))
            mant = ds[0] + (f".{ds[1:]}" if len(ds) > 1 else "")
            num = f"{'-' if d.is_signed() else ''}{mant}e{d.adjusted()}"
        elif style == "plain":
            if not value.is_zero() and abs(value.adjusted()) > 20:
                return None
            num = format_decimal(value, allow_exponent=False)
        elif style == "padded":
            mant, sep, exp = re.split(r"([eE])", num, maxsplit=1) if re.search("[eE]", num) else (num, "", "")
            mant = mant + "0" if "." in mant else mant + ".0"
            num = f"{mant}{sep}{exp}"
        elif style == "unit_spacing":
            if not lit.unit:
                return None
            return f"{lit.number}{'' if lit.space else ' '}{lit.unit}"
        else:
            raise ValueError(f"unknown numeric_literal_format style {style!r}")
        new = f"{num}{lit.space}{lit.unit}"
        if new == text or Decimal(parse_literal(new).number) != value:
            return None
        return new

    def _valid_for(self, decl, value: str, new: str) -> bool:
        xsd = xsd_index()
        qtype = xsd.quantity_types.get(decl.type)
        if qtype is not None:
            return qtype.matches(value) and qtype.matches(new)
        return bool(xsd.numeric_base(decl.type)) and bool(_PLAIN_NUMBER_RE.fullmatch(value)) \
            and bool(_PLAIN_NUMBER_RE.fullmatch(new))

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for doc, el, _typ, attrs in _typed_attributes(ws):
            for attr, value in el.attrib.items():
                decl = attrs.get(attr)
                if decl is None:
                    continue
                for style in self.styles:
                    new = self.restyle(value, style)
                    if new is not None and self._valid_for(decl, value, new):
                        out.append(Site(self.name, doc.rel, doc.locator(el),
                                        {"attribute": attr, "old": value, "new": new, "style": style,
                                         "xsd_type": decl.type}))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        p = site.params
        if self.restyle(p["old"], p["style"]) != p["new"]:
            raise TransformError("literal restyling is not reproducible")
        return _set_one(ws, site, p["attribute"], p["old"], p["new"],
                        f"numerically identical literal ({p['style']})")

    def describe(self, site: Site) -> str:
        p = site.params
        return f"{site.file}{site.locator}@{p['attribute']}: {p['old']!r} -> {p['new']!r} ({p['style']})"


class ExplicitDefault:
    """Write out an attribute that is omitted, using the default declared for it in the XSD.

    A schema default is the value the NeuroML standard assigns when the attribute is absent,
    so stating it explicitly must not change behaviour. The value is read from the
    ``default=`` of the attribute declaration (for example ``segmentGroup`` on channel
    densities), never supplied from memory.
    """

    name = "explicit_default"
    family = "explicit_default"
    kind = VariantKind.VALID_TRANSFORM

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for doc, el, typ, attrs in _typed_attributes(ws):
            for attr, decl in sorted(attrs.items()):
                if decl.default is not None and el.get(attr) is None:
                    out.append(Site(self.name, doc.rel, doc.locator(el),
                                    {"attribute": attr, "value": decl.default, "xsd_type": typ}))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        p = site.params
        decl = xsd_index().attributes(p["xsd_type"]).get(p["attribute"])
        if decl is None or decl.default != p["value"]:
            raise TransformError(f"XSD default for {p['xsd_type']}@{p['attribute']} is not {p['value']!r}")
        edits, e, m = _set_one(ws, site, p["attribute"], None, p["value"], f"explicit XSD default of {p['xsd_type']}")
        return [dc.replace(edits[0], action="insert")], e, m

    def describe(self, site: Site) -> str:
        p = site.params
        return f"{site.file}{site.locator}: add {p['attribute']}={p['value']!r} (XSD default)"
