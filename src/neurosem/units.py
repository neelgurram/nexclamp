"""NeuroML physical quantities: parsing, SI conversion and schema-safe formatting.

NeuroML v2 writes quantities as ``<number><optional space><unit>`` (e.g. ``"0.3s"``,
``"7.5E-10A"``, ``"0.1 mS_per_cm2"``). The XSD patterns allow an optional minus sign
and an exponent without a ``+`` sign, so :func:`format_number` never emits ``e+``.
"""

from __future__ import annotations

import dataclasses as dc
import math
import re

_QUANTITY_RE = re.compile(r"^\s*(-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*([A-Za-z_][A-Za-z_0-9]*)?\s*$")

# unit -> (dimension, factor to SI, offset to SI)
UNITS: dict[str, tuple[str, float, float]] = {
    # time
    "s": ("time", 1.0, 0.0), "ms": ("time", 1e-3, 0.0),
    # voltage
    "V": ("voltage", 1.0, 0.0), "mV": ("voltage", 1e-3, 0.0),
    # current
    "A": ("current", 1.0, 0.0), "uA": ("current", 1e-6, 0.0), "nA": ("current", 1e-9, 0.0), "pA": ("current", 1e-12, 0.0),
    # conductance
    "S": ("conductance", 1.0, 0.0), "mS": ("conductance", 1e-3, 0.0), "uS": ("conductance", 1e-6, 0.0),
    "nS": ("conductance", 1e-9, 0.0), "pS": ("conductance", 1e-12, 0.0),
    # conductance density
    "S_per_m2": ("conductanceDensity", 1.0, 0.0), "mS_per_cm2": ("conductanceDensity", 10.0, 0.0),
    "S_per_cm2": ("conductanceDensity", 1e4, 0.0),
    # capacitance and specific capacitance
    "F": ("capacitance", 1.0, 0.0), "uF": ("capacitance", 1e-6, 0.0), "nF": ("capacitance", 1e-9, 0.0),
    "pF": ("capacitance", 1e-12, 0.0),
    "F_per_m2": ("specificCapacitance", 1.0, 0.0), "uF_per_cm2": ("specificCapacitance", 1e-2, 0.0),
    # concentration
    "mol_per_m3": ("concentration", 1.0, 0.0), "mol_per_cm3": ("concentration", 1e6, 0.0), "mM": ("concentration", 1.0, 0.0),
    # temperature
    "K": ("temperature", 1.0, 0.0), "degC": ("temperature", 1.0, 273.15),
    # length
    "m": ("length", 1.0, 0.0), "cm": ("length", 1e-2, 0.0), "um": ("length", 1e-6, 0.0),
    # resistivity
    "ohm_m": ("resistivity", 1.0, 0.0), "kohm_cm": ("resistivity", 10.0, 0.0), "ohm_cm": ("resistivity", 1e-2, 0.0),
    # rates
    "per_s": ("per_time", 1.0, 0.0), "per_ms": ("per_time", 1e3, 0.0), "Hz": ("per_time", 1.0, 0.0),
}


@dc.dataclass(frozen=True)
class Quantity:
    value: float
    unit: str          # "" for dimensionless
    dimension: str
    si: float

    def to(self, unit: str) -> "Quantity":
        return convert(self, unit)


def parse(text: str) -> Quantity:
    m = _QUANTITY_RE.match(text)
    if not m:
        raise ValueError(f"not a NeuroML quantity: {text!r}")
    value = float(m.group(1))
    unit = m.group(2) or ""
    if unit == "":
        return Quantity(value, "", "none", value)
    if unit not in UNITS:
        raise ValueError(f"unknown unit {unit!r} in {text!r}")
    dim, factor, offset = UNITS[unit]
    return Quantity(value, unit, dim, value * factor + offset)


def convert(q: Quantity, unit: str) -> Quantity:
    if unit not in UNITS:
        raise ValueError(f"unknown unit {unit!r}")
    dim, factor, offset = UNITS[unit]
    if dim != q.dimension:
        raise ValueError(f"cannot convert {q.dimension} to {dim}")
    return Quantity((q.si - offset) / factor, unit, dim, q.si)


def units_for(dimension: str) -> list[str]:
    return [u for u, (d, _, _) in UNITS.items() if d == dimension]


def format_number(x: float) -> str:
    """Shortest round-tripping decimal representation that matches the NeuroML XSD."""
    if not math.isfinite(x):
        raise ValueError("non-finite quantity")
    s = repr(float(x))
    if "e" in s or "E" in s:
        mant, exp = s.lower().split("e")
        s = f"{mant}e{int(exp)}"          # drops '+' and leading zeros
    return s


def format_quantity(value: float, unit: str, space: bool = False) -> str:
    return f"{format_number(value)}{' ' if space and unit else ''}{unit}"


def same_si(a: str, b: str, rel: float = 1e-12) -> bool:
    """True if two quantity strings denote the same physical value."""
    qa, qb = parse(a), parse(b)
    if qa.dimension != qb.dimension:
        return False
    return math.isclose(qa.si, qb.si, rel_tol=rel, abs_tol=0.0)
