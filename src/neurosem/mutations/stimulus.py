"""Stimulus mutations: faults in the shipped harness, i.e. the canonical protocol.

They edit only the harness: the input generators in the NeuroML files included by the
harness LEMS file (``RS.net.nml`` for Pospischil cells; the cell file itself for the
NeuroML2 HH example, which defines its ``pulseGenerator`` there) and the harness
``Simulation``/``OutputFile``. Probe batteries never read these elements, so stimulus
mutants can only be seen by the canonical test, which is the point of the family.

Default grids mix small and large perturbations on purpose: a small change (x0.9/x1.1,
+-2 ms) probes whether tolerances are tight enough to notice a plausible transcription
slip, a large one (x0.5/x2, +-50 ms, sign inversion) is an unmistakable fault whose
detection checks basic sensitivity. Both ends are needed to calibrate a detection rate.
"""

from __future__ import annotations

from collections.abc import Sequence

from neurosem.models import Workspace
from neurosem.mutations.base import (
    Inapplicable,
    OperatorBase,
    Site,
    attribute_site,
    expect_set_edits,
    harness_includes,
    harness_rel,
    harness_simulation,
    is_scaled,
    is_shifted,
    iter_elements,
    localname,
    locator,
    quantity_si,
    read_xml,
    record_param,
    register,
    require,
    scale_quantity,
    shift_quantity,
    step_name,
)
from neurosem.schemas import MutationFamily, VariantRecord

AMPLITUDE_ATTRS: dict[str, tuple[str, ...]] = {
    "pulseGenerator": ("amplitude",), "pulseGeneratorDL": ("amplitude",),
    "sineGenerator": ("amplitude",), "sineGeneratorDL": ("amplitude",),
    "rampGenerator": ("startAmplitude", "finishAmplitude", "baselineAmplitude"),
    "rampGeneratorDL": ("startAmplitude", "finishAmplitude", "baselineAmplitude"),
}


def harness_generators(ws: Workspace) -> list[tuple[str, object]]:
    """(file, element) for every current-clamp generator in files included by the harness, in document order."""
    out = []
    for rel in harness_includes(ws):
        doc = read_xml(ws.path(rel))
        if localname(doc.root) != "neuroml":
            continue
        out += [(rel, el) for el in iter_elements(doc.root) if localname(el) in AMPLITUDE_ATTRS]
    return out


class _GeneratorOperator(OperatorBase):
    family = MutationFamily.STIMULUS

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        if harness_generators(ws):
            return []
        return [Inapplicable(self.name, harness_rel(ws), "", "no input generator in files included by the harness")]

    def _generator_edit(self, record: VariantRecord, ref: Workspace, attribute: str):
        files = sorted({rel for rel, _ in harness_generators(ref)})
        [e] = expect_set_edits(record, attributes=(attribute,), element=AMPLITUDE_ATTRS.keys(), files=files)
        return e


class StimAmplitude(_GeneratorOperator):
    name = "stim_amplitude"

    def __init__(self, factors: Sequence[float] = (-1.0, 0.5, 0.9, 1.1, 2.0)) -> None:
        self.factors = tuple(factors)

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel, el in harness_generators(ws):
            attrs = [a for a in AMPLITUDE_ATTRS[localname(el)] if el.get(a) is not None]
            for f in self.factors:
                changes = [(el, a, el.get(a), scale_quantity(el.get(a), f)) for a in attrs]
                changes = [c for c in changes if quantity_si(c[2]) != quantity_si(c[3])]
                if changes:
                    out.append(attribute_site(self.name, rel, el, changes, factor=f, element=localname(el),
                                              element_id=el.get("id")))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        """Amplitude attributes of ONE generator, all scaled by the same factor (a ramp's
        start/finish/baseline together form one amplitude fault)."""
        files = sorted({rel for rel, _ in harness_generators(ref)})
        all_attrs = sorted({a for attrs in AMPLITUDE_ATTRS.values() for a in attrs})
        edits = expect_set_edits(record, attributes=all_attrs, element=AMPLITUDE_ATTRS.keys(), files=files,
                                 count=range(1, 4))
        f = record_param(record, "factor")
        require(len({(e.file, e.locator) for e in edits}) == 1, record, "edits address more than one generator")
        require(len({e.attribute for e in edits}) == len(edits), record, "an attribute is edited twice")
        for e in edits:
            require(e.attribute in AMPLITUDE_ATTRS[step_name(e.locator)], record,
                    f"{e.attribute!r} is not an amplitude of {step_name(e.locator)}")
            require(is_scaled(e.old, e.new, f), record, f"{e.attribute} {e.old!r} -> {e.new!r} is not a x{f} scaling")


class StimOnset(_GeneratorOperator):
    name = "stim_onset"

    def __init__(self, shifts_ms: Sequence[float] = (-50.0, -10.0, -2.0, 2.0, 10.0, 50.0)) -> None:
        self.shifts_ms = tuple(shifts_ms)

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel, el in harness_generators(ws):
            old = el.get("delay")
            if old is None:
                continue
            for s in self.shifts_ms:
                new = shift_quantity(old, s, "ms")
                if quantity_si(new) < 0:        # a negative delay is not a meaningful onset
                    continue
                out.append(attribute_site(self.name, rel, el, [(el, "delay", old, new)], shift_ms=s,
                                          element=localname(el), element_id=el.get("id")))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        e = self._generator_edit(record, ref, "delay")
        s = record_param(record, "shift_ms")
        require(is_shifted(e.old, e.new, s, "ms"), record, f"delay {e.old!r} -> {e.new!r} is not a {s} ms shift")
        require(quantity_si(e.new) >= 0, record, "negative delay")


class StimDuration(_GeneratorOperator):
    name = "stim_duration"

    def __init__(self, factors: Sequence[float] = (0.5, 0.9, 1.1, 2.0)) -> None:
        self.factors = tuple(factors)

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel, el in harness_generators(ws):
            old = el.get("duration")
            if old is None or quantity_si(old) == 0:
                continue
            for f in self.factors:
                out.append(attribute_site(self.name, rel, el, [(el, "duration", old, scale_quantity(old, f))],
                                          factor=f, element=localname(el), element_id=el.get("id")))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        e = self._generator_edit(record, ref, "duration")
        f = record_param(record, "factor")
        require(is_scaled(e.old, e.new, f), record, f"duration {e.old!r} -> {e.new!r} is not a x{f} scaling")


class SimLength(OperatorBase):
    name = "sim_length"
    family = MutationFamily.STIMULUS

    def __init__(self, factors: Sequence[float] = (0.5, 0.9, 1.1, 2.0)) -> None:
        self.factors = tuple(factors)

    def sites(self, ws: Workspace) -> list[Site]:
        rel = harness_rel(ws)
        sim = harness_simulation(read_xml(ws.path(rel)).root)
        old = sim.get("length")
        if old is None:
            return []
        return [attribute_site(self.name, rel, sim, [(sim, "length", old, scale_quantity(old, f))], factor=f)
                for f in self.factors]

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=("length",), element=("Simulation", "Component"),
                               files=(harness_rel(ref),))
        require(e.locator == locator(harness_simulation(read_xml(ref.harness_path).root)), record,
                "edit is not on the harness Simulation")
        f = record_param(record, "factor")
        require(is_scaled(e.old, e.new, f), record, f"length {e.old!r} -> {e.new!r} is not a x{f} scaling")


class RecordWrongVariable(OperatorBase):
    """Point the canonical voltage column at another state path already recorded or displayed by the harness.

    Only paths that the shipped harness itself references (Display lines, other output
    columns) are used, so the substitute is a real, resolvable quantity of the model.
    """

    name = "record_wrong_variable"
    family = MutationFamily.STIMULUS

    def _v_column(self, ws: Workspace):
        sim = harness_simulation(read_xml(ws.path(harness_rel(ws))).root)
        files = [e for e in sim.iter() if isinstance(e.tag, str) and localname(e) == "OutputFile"
                 and e.get("fileName") == ws.model.harness_output_file]
        if not files:
            return sim, None
        cols = [c for c in files[0] if isinstance(c.tag, str) and localname(c) == "OutputColumn"]
        k = int(ws.model.harness_v_column) - 1
        return sim, (cols[k] if 0 <= k < len(cols) else None)

    def sites(self, ws: Workspace) -> list[Site]:
        sim, col = self._v_column(ws)
        if col is None:
            return []
        v_q = col.get("quantity")
        alternatives: list[str] = []
        for e in sim.iter():
            if isinstance(e.tag, str) and localname(e) in ("Line", "OutputColumn"):
                q = e.get("quantity")
                if q and q != v_q and q not in alternatives:
                    alternatives.append(q)
        return [attribute_site(self.name, harness_rel(ws), col, [(col, "quantity", v_q, q)], new_quantity=q)
                for q in alternatives]

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        _, col = self._v_column(ws)
        if col is None:
            return [Inapplicable(self.name, harness_rel(ws), "", "harness v column not found")]
        return []

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=("quantity",), element=("OutputColumn",), files=(harness_rel(ref),))
        _, col = self._v_column(ref)
        require(col is not None and e.locator == locator(col), record, "edit is not on the harness v column")
        substitutes = {s.params["new_quantity"] for s in self.sites(ref)}
        require(e.new in substitutes, record, f"{e.new!r} is not a state path referenced by the shipped harness")
        require(e.new == record_param(record, "new_quantity"), record, "edit does not match params.new_quantity")


for _op in (StimAmplitude(), StimOnset(), StimDuration(), SimLength(), RecordWrongVariable()):
    register(_op)
