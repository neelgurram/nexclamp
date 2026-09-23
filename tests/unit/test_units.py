"""Tests for nexclamp.units: parsing, SI conversion and XSD-safe formatting of NeuroML quantities.

The expected SI factors below are written out from first principles (e.g. 1 mS/cm2 =
1e-3 S / 1e-4 m2 = 10 S/m2), not copied from the module, so a wrong table entry fails.
The XSD patterns are read from the NeuroML_v2.3.1.xsd shipped inside the installed
libNeuroML package, i.e. the same schema version the generated files declare.
"""

from __future__ import annotations

import math
import random
import re
import struct
from pathlib import Path

import pytest
from lxml import etree

from nexclamp import units
from nexclamp.units import UNITS, Quantity, convert, format_number, format_quantity, parse, same_si, units_for

XS = "{http://www.w3.org/2001/XMLSchema}"

# unit -> (dimension, SI value of "1 <unit>") derived by hand.
EXPECTED_SI: dict[str, tuple[str, float]] = {
    "s": ("time", 1.0), "ms": ("time", 1e-3),
    "V": ("voltage", 1.0), "mV": ("voltage", 1e-3),
    "A": ("current", 1.0), "uA": ("current", 1e-6), "nA": ("current", 1e-9), "pA": ("current", 1e-12),
    "S": ("conductance", 1.0), "mS": ("conductance", 1e-3), "uS": ("conductance", 1e-6),
    "nS": ("conductance", 1e-9), "pS": ("conductance", 1e-12),
    "S_per_m2": ("conductanceDensity", 1.0), "mS_per_cm2": ("conductanceDensity", 10.0),
    "S_per_cm2": ("conductanceDensity", 1e4),
    "F": ("capacitance", 1.0), "uF": ("capacitance", 1e-6), "nF": ("capacitance", 1e-9), "pF": ("capacitance", 1e-12),
    "F_per_m2": ("specificCapacitance", 1.0), "uF_per_cm2": ("specificCapacitance", 1e-2),
    "mol_per_m3": ("concentration", 1.0), "mol_per_cm3": ("concentration", 1e6), "mM": ("concentration", 1.0),
    "M": ("concentration", 1e3),              # 1 mol/L = 1000 mol/m3 (XSD Nml2Quantity_concentration)
    "degC": ("temperature", 274.15),          # 1 degC = 274.15 K (offset unit); K is not a NeuroML unit string
    "m": ("length", 1.0), "cm": ("length", 1e-2), "um": ("length", 1e-6),
    "ohm_m": ("resistivity", 1.0), "kohm_cm": ("resistivity", 10.0), "ohm_cm": ("resistivity", 1e-2),
    "per_s": ("per_time", 1.0), "per_ms": ("per_time", 1e3), "Hz": ("per_time", 1.0),
}

# neurosem dimension name -> XSD simpleType name
XSD_TYPE = {
    "time": "Nml2Quantity_time", "voltage": "Nml2Quantity_voltage", "current": "Nml2Quantity_current",
    "conductance": "Nml2Quantity_conductance", "conductanceDensity": "Nml2Quantity_conductanceDensity",
    "capacitance": "Nml2Quantity_capacitance", "specificCapacitance": "Nml2Quantity_specificCapacitance",
    "concentration": "Nml2Quantity_concentration", "temperature": "Nml2Quantity_temperature",
    "length": "Nml2Quantity_length", "resistivity": "Nml2Quantity_resistivity", "per_time": "Nml2Quantity_pertime",
}


def _xsd_path() -> Path:
    import neuroml

    p = Path(neuroml.__file__).parent / "nml" / "NeuroML_v2.3.1.xsd"
    assert p.is_file(), p
    return p


def _xsd_patterns() -> dict[str, str]:
    tree = etree.parse(str(_xsd_path()))
    out = {}
    for st in tree.iter(f"{XS}simpleType"):
        name = st.get("name", "")
        pat = st.find(f"{XS}restriction/{XS}pattern")
        if name.startswith("Nml2Quantity") and pat is not None:
            out[name] = pat.get("value")
    return out


PATTERNS = _xsd_patterns()


def _xsd_units(type_name: str) -> set[str]:
    m = re.search(r"\(([^()]*)\)$", PATTERNS[type_name])
    assert m, PATTERNS[type_name]
    return set(m.group(1).split("|"))


def _xsd_match(type_name: str, text: str) -> bool:
    # XSD patterns are implicitly anchored at both ends; [\s] and the rest are Python-compatible.
    return re.fullmatch(PATTERNS[type_name], text) is not None


# ---------------------------------------------------------------------------------------------- parse
@pytest.mark.parametrize("text, value, unit, dim", [
    ("0.3s", 0.3, "s", "time"),
    ("7.5E-10A", 7.5e-10, "A", "current"),
    ("0.1 mS_per_cm2", 0.1, "mS_per_cm2", "conductanceDensity"),
    ("-70.0 mV", -70.0, "mV", "voltage"),
    (".5ms", 0.5, "ms", "time"),
    ("5.ms", 5.0, "ms", "time"),
    ("1e-3 s", 1e-3, "s", "time"),
    ("  36.0 degC  ", 36.0, "degC", "temperature"),
    ("1e+5 nA", 1e5, "nA", "current"),          # parse is lenient about '+'; format_number never writes it
    ("3", 3.0, "", "none"),
    ("-2.5", -2.5, "", "none"),
])
def test_parse_accepts_neuroml_quantities(text, value, unit, dim):
    q = parse(text)
    assert q.value == value and q.unit == unit and q.dimension == dim


@pytest.mark.parametrize("text", ["", "mV", "abc", "1..2 mV", "--1 mV", "1 mV extra", "1E5.0 nA", "1 m V", "+1 mV"])
def test_parse_rejects_malformed(text):
    with pytest.raises(ValueError, match="not a NeuroML quantity"):
        parse(text)


def test_parse_rejects_unknown_unit():
    with pytest.raises(ValueError, match="unknown unit 'furlongs'"):
        parse("5 furlongs")


def test_dimensionless_si_is_value():
    q = parse("-4.25")
    assert q.si == -4.25 and q.unit == ""


# ------------------------------------------------------------------------------------------ SI table
def test_expected_table_covers_every_unit():
    # A new unit must come with an independently derived expectation here.
    assert set(EXPECTED_SI) == set(UNITS)


@pytest.mark.parametrize("unit", sorted(EXPECTED_SI))
def test_si_value_of_one_unit(unit):
    dim, si = EXPECTED_SI[unit]
    q = parse(f"1 {unit}")
    assert q.dimension == dim
    assert math.isclose(q.si, si, rel_tol=1e-12, abs_tol=0.0)


def test_real_model_values_to_si():
    assert math.isclose(parse("7.5E-10A").si, 0.75e-9, rel_tol=1e-15)
    assert math.isclose(parse("0.75 nA").si, parse("7.5E-10A").si, rel_tol=1e-12)
    assert math.isclose(parse("50.0 mS_per_cm2").si, 500.0, rel_tol=1e-12)
    assert math.isclose(parse("1.0 uF_per_cm2").si, 0.01, rel_tol=1e-12)
    assert math.isclose(parse("100 ohm_cm").si, 1.0, rel_tol=1e-12)


# ------------------------------------------------------------------------------------ temperature
def test_degc_offset_to_kelvin():
    assert math.isclose(parse("36.0 degC").si, 309.15, rel_tol=1e-12)
    assert math.isclose(parse("0 degC").si, 273.15, rel_tol=1e-15)


def test_kelvin_is_not_a_neuroml_unit_but_degc_has_an_offset():
    with pytest.raises(ValueError):                    # NeuroML v2.3.1 temperatures permit only degC
        parse("309.15 K")
    assert math.isclose(parse("36.0 degC").si, 309.15, rel_tol=1e-12)
    assert math.isclose(parse("0 degC").si, 273.15, rel_tol=1e-12)


def test_degc_round_trip_and_same_si():
    q = parse("37 degC")
    back = q.to("degC")
    assert math.isclose(back.value, 37.0, abs_tol=1e-12)
    assert same_si("36.0 degC", "36 degC")
    assert not same_si("36.0 degC", "37.0 degC")


# --------------------------------------------------------------------------------------- convert
def test_convert_voltage_and_current():
    assert math.isclose(convert(parse("-70 mV"), "V").value, -0.07, rel_tol=1e-12)
    assert math.isclose(parse("7.5E-10A").to("nA").value, 0.75, rel_tol=1e-12)
    c = convert(parse("0.1 mS_per_cm2"), "S_per_m2")
    assert isinstance(c, Quantity) and c.unit == "S_per_m2" and c.dimension == "conductanceDensity"
    assert math.isclose(c.value, 1.0, rel_tol=1e-12) and c.si == parse("0.1 mS_per_cm2").si


def test_convert_rejects_other_dimension_and_unknown_unit():
    with pytest.raises(ValueError, match="cannot convert voltage to time"):
        convert(parse("1 mV"), "ms")
    with pytest.raises(ValueError, match="unknown unit"):
        convert(parse("1 mV"), "kV")


def test_units_for_dimension():
    assert units_for("time") == ["s", "ms"]
    assert set(units_for("current")) == {"A", "uA", "nA", "pA"}
    assert units_for("no_such_dimension") == []


def test_same_si():
    assert same_si("0.3s", "300 ms")
    assert same_si("0 mV", "0.0 V")
    assert not same_si("1 mV", "1 mS")                      # different dimensions
    assert not same_si("1 nA", "1.000001 nA")
    assert same_si("1 nA", "1.000001 nA", rel=1e-5)


# ---------------------------------------------------------------------------- XSD unit agreement
@pytest.mark.parametrize("dim", [
    d
    for d in sorted(XSD_TYPE)
])
def test_every_neurosem_unit_is_permitted_by_xsd(dim):
    """A unit that units.py knows but the XSD forbids would let a unit-conversion transform write an invalid file."""
    assert set(units_for(dim)) <= _xsd_units(XSD_TYPE[dim])


@pytest.mark.parametrize("dim", [
    d
    for d in sorted(XSD_TYPE)
])
def test_every_xsd_unit_is_parseable(dim):
    """A schema-valid model file must never make parse() raise for a supported dimension."""
    missing = _xsd_units(XSD_TYPE[dim]) - set(units_for(dim))
    assert not missing


# ---------------------------------------------------------------------------------- format_number
SPECIAL = [0.0, -0.0, 1.0, 2.0, -70.0, 0.1, 1 / 3, 0.15000000000000002, 1e15, 1e16, 1e22, 1e-4, 1e-5, 1e-7,
           -2.5e-10, 123456789012345678.0, 5e-324, 2.2250738585072014e-308, 1.7976931348623157e308, 0.005, 0.00125]


def _random_doubles(n: int, seed: int = 20260913) -> list[float]:
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        x = struct.unpack("<d", struct.pack("<Q", rng.getrandbits(64)))[0]
        if math.isfinite(x):
            out.append(x)
    return out


@pytest.mark.parametrize("x", SPECIAL)
def test_format_number_special_values(x):
    s = format_number(x)
    assert "e+" not in s and "E+" not in s
    assert float(s) == x and math.copysign(1.0, float(s)) == math.copysign(1.0, x)


def test_format_number_known_strings():
    assert format_number(1e16) == "1e16"
    assert format_number(1e-7) == "1e-7"
    assert format_number(2.0) == "2.0"
    assert format_number(0.00125) == "0.00125"
    assert format_number(-0.0) == "-0.0"
    assert format_number(5e-324) == "5e-324"


def test_format_number_never_emits_plus_and_round_trips_randomised():
    for x in _random_doubles(5000) + SPECIAL:
        s = format_number(x)
        assert "+" not in s, (x, s)
        assert float(s) == x, (x, s)


def test_formatted_strings_match_xsd_patterns():
    """Every formatted value, in every unit of every dimension, matches that dimension's XSD pattern."""
    values = _random_doubles(400) + SPECIAL
    for dim, type_name in XSD_TYPE.items():
        for unit in sorted(_xsd_units(type_name) & set(units_for(dim))):
            for x in values:
                for space in (False, True):
                    text = format_quantity(x, unit, space=space)
                    assert _xsd_match(type_name, text), (type_name, text)
                    back = parse(text)
                    assert back.value == x and back.unit == unit


def test_plus_exponent_would_violate_xsd():
    # Guards the reason format_number exists: Python's repr uses 'e+', which the schema rejects.
    assert repr(1e16) == "1e+16"
    assert not _xsd_match("Nml2Quantity_current", "1e+16nA")
    assert _xsd_match("Nml2Quantity_current", format_quantity(1e16, "nA"))


@pytest.mark.parametrize("x", [math.nan, math.inf, -math.inf])
def test_format_number_rejects_non_finite(x):
    with pytest.raises(ValueError, match="non-finite"):
        format_number(x)


def test_format_quantity_spacing():
    assert format_quantity(0.75, "nA") == "0.75nA"
    assert format_quantity(0.75, "nA", space=True) == "0.75 nA"
    assert format_quantity(3.0, "", space=True) == "3.0"
    assert format_quantity(1e-5, "ms") == "1e-5ms"


def test_module_docstring_states_xsd_rule():
    assert "e+" in (units.__doc__ or "")
