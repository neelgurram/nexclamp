"""Biophysical mutations: single-parameter faults in the cell's membrane and channel kinetics.

Default grids: multiplicative factors are log-symmetric pairs (0.9/1.1, 0.8/1.25, 0.5/2)
so that "too small" and "too large" faults of the same magnitude are both represented,
from a plausible slip (10 %) to a gross error (factor 2). Voltage shifts cover +-2 mV (the
scale of a liquid-junction or rounding discrepancy) up to +-10 mV (reversal) or +-20 mV
(initial voltage, which can trigger an initial spike). Small faults are expected to be
detected less often; including them is what makes a detection rate informative.
"""

from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal

from lxml import etree

from neuraxis.models import Workspace
from neuraxis.mutations.base import (
    Inapplicable,
    MutationError,
    OperatorBase,
    Site,
    apply_attribute_changes,
    attribute_site,
    cell_rel,
    element_children,
    expect_set_edits,
    find_cell,
    insert_before,
    is_scaled,
    is_shifted,
    iter_elements,
    localname,
    locator,
    parent_locator,
    parse_snippet,
    qualified,
    quantity_si,
    read_xml,
    record_param,
    register,
    require,
    resolve,
    same_quantity,
    scale_quantity,
    shift_quantity,
    snippet,
    step_name,
    transitive_includes,
    write_xml,
)
from neuraxis.schemas import Edit, MutationFamily, VariantRecord

FACTORS = (0.5, 0.8, 0.9, 1.1, 1.25, 2.0)
CHANNEL_TAGS = ("ionChannel", "ionChannelHH", "ionChannelPassive", "ionChannelVShift", "ionChannelKS")
GATE_TAGS = ("gate", "gateHHrates", "gateHHtauInf", "gateHHratesTau", "gateHHratesInf", "gateHHratesTauInf",
             "gateHHInstantaneous", "gateFractional", "gateKS")
RATE_GATES = ("gateHHrates", "gateHHratesInf")                              # tau = 1/((alpha+beta) rateScale)
TIMECOURSE_GATES = ("gateHHtauInf", "gateHHratesTau", "gateHHratesTauInf")  # tau = timeCourse/t / rateScale
CORE_RATES = ("HHExpRate", "HHSigmoidRate", "HHExpLinearRate")             # r is linear in the `rate` parameter
INSTANTANEOUS = ("gateHHInstantaneous", "gateHHratesInstantaneous")


def cell_element(ws: Workspace):
    doc = read_xml(ws.cell_path)
    cell = find_cell(doc.root, ws.model.cell_id)
    return doc, (cell if cell is not None else doc.root)


def channel_densities(scope) -> list:
    return [e for e in iter_elements(scope) if localname(e).startswith("channelDensity")]


def is_channel_density(name: str) -> bool:
    return name.startswith("channelDensity")


def membrane_elements(scope, name: str) -> list:
    return [e for e in iter_elements(scope) if localname(e) == name]


class _ScaleAttr(OperatorBase):
    family = MutationFamily.BIOPHYSICAL
    attribute: str = ""

    def __init__(self, factors: Sequence[float] = FACTORS) -> None:
        self.factors = tuple(factors)

    def targets(self, scope) -> list:
        raise NotImplementedError

    def target_name_ok(self, name: str) -> bool:
        raise NotImplementedError

    def sites(self, ws: Workspace) -> list[Site]:
        _, scope = cell_element(ws)
        out = []
        for el in self.targets(scope):
            old = el.get(self.attribute)
            if old is None:
                continue
            try:
                if quantity_si(old) == 0:      # scaling zero changes nothing: not a fault site
                    continue
            except (MutationError, TypeError, ValueError):
                pass
            for f in self.factors:
                out.append(attribute_site(self.name, cell_rel(ws), el, [(el, self.attribute, old, scale_quantity(old, f))],
                                          factor=f, element=localname(el), element_id=el.get("id")))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=(self.attribute,), element=self.target_name_ok, files=(cell_rel(ref),))
        f = record_param(record, "factor")
        require(is_scaled(e.old, e.new, f), record, f"{self.attribute} {e.old!r} -> {e.new!r} is not a x{f} scaling")


class ScaleConductance(_ScaleAttr):
    name = "scale_conductance"
    attribute = "condDensity"

    def targets(self, scope) -> list:
        return channel_densities(scope)

    def target_name_ok(self, name: str) -> bool:
        return is_channel_density(name)


class ScaleCapacitance(_ScaleAttr):
    name = "scale_capacitance"
    attribute = "value"

    def targets(self, scope) -> list:
        return membrane_elements(scope, "specificCapacitance")

    def target_name_ok(self, name: str) -> bool:
        return name == "specificCapacitance"


class _ShiftAttr(OperatorBase):
    family = MutationFamily.BIOPHYSICAL
    attribute = "value"

    def __init__(self, shifts_mV: Sequence[float]) -> None:
        self.shifts_mV = tuple(shifts_mV)

    def targets(self, scope) -> list:
        raise NotImplementedError

    def target_name_ok(self, name: str) -> bool:
        raise NotImplementedError

    def sites(self, ws: Workspace) -> list[Site]:
        _, scope = cell_element(ws)
        out = []
        for el in self.targets(scope):
            old = el.get(self.attribute)
            if old is None:
                continue
            for s in self.shifts_mV:
                out.append(attribute_site(self.name, cell_rel(ws), el,
                                          [(el, self.attribute, old, shift_quantity(old, s, "mV"))],
                                          shift_mV=s, element=localname(el), element_id=el.get("id")))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=(self.attribute,), element=self.target_name_ok, files=(cell_rel(ref),))
        s = record_param(record, "shift_mV")
        require(is_shifted(e.old, e.new, s, "mV"), record, f"{self.attribute} {e.old!r} -> {e.new!r} is not a {s} mV shift")


class ShiftReversal(_ShiftAttr):
    name = "shift_reversal"
    attribute = "erev"

    def __init__(self, shifts_mV: Sequence[float] = (-10.0, -5.0, -2.0, 2.0, 5.0, 10.0)) -> None:
        super().__init__(shifts_mV)

    def targets(self, scope) -> list:
        return channel_densities(scope)

    def target_name_ok(self, name: str) -> bool:
        return is_channel_density(name)

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        _, scope = cell_element(ws)
        return [Inapplicable(self.name, cell_rel(ws), locator(e), "no erev attribute (computed, e.g. Nernst/GHK)")
                for e in channel_densities(scope) if e.get("erev") is None]


class ShiftInitialVoltage(_ShiftAttr):
    name = "shift_initial_voltage"

    def __init__(self, shifts_mV: Sequence[float] = (-20.0, -5.0, -2.0, 2.0, 5.0, 20.0)) -> None:
        super().__init__(shifts_mV)

    def targets(self, scope) -> list:
        return membrane_elements(scope, "initMembPotential")

    def target_name_ok(self, name: str) -> bool:
        return name == "initMembPotential"


class WrongSegmentGroup(OperatorBase):
    """Move one channel density to another existing segment group (absent attribute = "all").

    In single-compartment cells every group holds the same segment, so these mutants are
    expected to be behaviourally equivalent; they remain useful negative controls.
    """

    name = "wrong_segment_group"
    family = MutationFamily.BIOPHYSICAL

    def sites(self, ws: Workspace) -> list[Site]:
        _, scope = cell_element(ws)
        groups = [g.get("id") for g in iter_elements(scope) if localname(g) == "segmentGroup" and g.get("id")]
        out = []
        for el in channel_densities(scope):
            if "NonUniform" in localname(el) or el.get("segment") is not None:
                continue
            old = el.get("segmentGroup")
            current = old if old is not None else "all"
            for g in groups:
                if g != current:
                    out.append(attribute_site(self.name, cell_rel(ws), el, [(el, "segmentGroup", old, g)],
                                              element=localname(el), element_id=el.get("id"), new_group=g))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=("segmentGroup",), element=is_channel_density, files=(cell_rel(ref),))
        _, scope = cell_element(ref)
        groups = {g.get("id") for g in iter_elements(scope) if localname(g) == "segmentGroup" and g.get("id")}
        require(e.new in groups, record, f"new segment group {e.new!r} is not an existing group")
        require(e.new != (e.old if e.old is not None else "all"), record, "segment group is unchanged")
        require(e.new == record_param(record, "new_group"), record, "edit does not match params.new_group")


def used_channels(ws: Workspace) -> list[tuple[str, object]]:
    """(file, ionChannel element) for channels referenced by the cell's channel densities."""
    _, scope = cell_element(ws)
    used = {e.get("ionChannel") for e in channel_densities(scope)}
    out, seen = [], set()
    for rel in transitive_includes(ws, cell_rel(ws)):
        for el in iter_elements(read_xml(ws.path(rel)).root):
            cid = el.get("id")
            if localname(el) in CHANNEL_TAGS and cid in used and cid not in seen:
                seen.add(cid)
                out.append((rel, el))
    return out


class ScaleGateTimeConstant(OperatorBase):
    """Scale all rates of one gate by k (tau -> tau/k, steady state unchanged).

    Mechanisms, in order of preference:

    * core rate gates (``gateHHrates``, ``gateHHratesInf``) whose forward and reverse rates
      are core ``HHExpRate``/``HHSigmoidRate``/``HHExpLinearRate``: multiply both ``rate``
      parameters by k (each r is linear in ``rate``, so alpha/(alpha+beta) is unchanged);
    * core time-course gates (``gateHHtauInf``, ``gateHHratesTau``, ``gateHHratesTauInf``)
      with a ``fixedTimeCourse``: multiply ``tau`` by 1/k;
    * only if ``allow_q10_fallback``: core gates whose rate/timeCourse is a custom LEMS
      ComponentType (no parameter to scale) get a ``q10Fixed`` of k, or an existing
      ``q10Fixed`` scaled by k. In NeuroML2CoreTypes ``rateScale`` is the product of all
      ``q10Settings[*]/q10`` and divides tau in every core HH gate. This is off by default
      because the architecture contract restricts the operator to rate/timeCourse
      parameters (see docs/build_notes/mutations.md).

    Custom gate types (e.g. LTS ``IT_s_gate``), instantaneous, fractional and kinetic-scheme
    gates are reported by :meth:`inapplicable`.
    """

    name = "scale_gate_time_constant"
    family = MutationFamily.BIOPHYSICAL
    container_children = frozenset({"forwardRate", "reverseRate"})

    def __init__(self, factors: Sequence[float] = (0.5, 0.8, 1.25, 2.0), allow_q10_fallback: bool = False) -> None:
        self.factors = tuple(factors)
        self.allow_q10_fallback = allow_q10_fallback

    # classification --------------------------------------------------------------
    def _classify(self, gate) -> tuple[str, str]:
        """Return (mechanism, reason); mechanism '' means inapplicable."""
        gtype = gate.get("type") or localname(gate)
        kids = {localname(c): c for c in element_children(gate)}
        if gtype in INSTANTANEOUS:
            return "", f"instantaneous gate type {gtype} (tau = 0)"
        if gtype not in RATE_GATES + TIMECOURSE_GATES:
            return "", f"gate type {gtype} is not a core HH rate/time-course gate (custom LEMS or unsupported)"
        if gtype in RATE_GATES:
            fr, rr = kids.get("forwardRate"), kids.get("reverseRate")
            if (fr is not None and rr is not None and fr.get("type") in CORE_RATES and rr.get("type") in CORE_RATES
                    and fr.get("rate") is not None and rr.get("rate") is not None):
                return "rate_parameters", ""
            detail = f"rates {fr.get('type') if fr is not None else None}/{rr.get('type') if rr is not None else None}"
        else:
            tc = kids.get("timeCourse")
            if tc is not None and tc.get("type") == "fixedTimeCourse" and tc.get("tau") is not None:
                if quantity_si(tc.get("tau")) == 0:
                    return "", "fixedTimeCourse tau is 0"
                return "time_course_tau", ""
            detail = f"timeCourse {tc.get('type') if tc is not None else None}"
        if not self.allow_q10_fallback:
            return "", f"{detail} is a custom ComponentType without a scalable parameter (q10 fallback disabled)"
        q10 = [c for c in element_children(gate) if localname(c) == "q10Settings"]
        if not q10:
            return "q10_insert", ""
        if len(q10) == 1 and q10[0].get("type") == "q10Fixed" and q10[0].get("fixedQ10") is not None:
            return "q10_scale", ""
        return "", f"{detail} is custom and existing q10Settings type {q10[0].get('type')} cannot be scaled linearly"

    def _gates(self, ws: Workspace):
        for rel, ch in used_channels(ws):
            for gate in element_children(ch):
                if localname(gate) in GATE_TAGS:
                    yield rel, ch, gate

    # protocol ----------------------------------------------------------------------
    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel, ch, gate in self._gates(ws):
            mech, _ = self._classify(gate)
            if not mech:
                continue
            kids = {localname(c): c for c in element_children(gate)}
            for k in self.factors:
                meta = {"factor": k, "mechanism": mech, "channel": ch.get("id"), "gate": gate.get("id")}
                if mech == "rate_parameters":
                    changes = [(kids[n], "rate", kids[n].get("rate"), scale_quantity(kids[n].get("rate"), k))
                               for n in ("forwardRate", "reverseRate")]
                    out.append(attribute_site(self.name, rel, gate, changes, **meta))
                elif mech == "time_course_tau":
                    tc = kids["timeCourse"]
                    inv = Decimal(1) / Decimal(repr(float(k)))
                    out.append(attribute_site(self.name, rel, gate,
                                              [(tc, "tau", tc.get("tau"), scale_quantity(tc.get("tau"), inv))], **meta))
                elif mech == "q10_scale":
                    q = next(c for c in element_children(gate) if localname(c) == "q10Settings")
                    out.append(attribute_site(self.name, rel, gate,
                                              [(q, "fixedQ10", q.get("fixedQ10"), scale_quantity(q.get("fixedQ10"), k))],
                                              **meta))
                else:
                    out.append(Site(self.name, rel, locator(gate), meta))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        self._check_site(site)
        if site.params["mechanism"] != "q10_insert":
            return apply_attribute_changes(ws, site), {}, {}
        doc = read_xml(ws.path(site.file))
        gate = resolve(doc.root, site.locator)
        if any(localname(c) == "q10Settings" for c in element_children(gate)):
            raise MutationError(f"stale site: {site.locator} already has q10Settings")
        new = etree.Element(qualified(gate, "q10Settings"))
        new.set("type", "q10Fixed")
        new.set("fixedQ10", scale_quantity("1", site.params["factor"]))
        kids = element_children(gate)
        after_notes = [c for c in kids if localname(c) != "notes"]    # XSD order: notes?, q10Settings?, rates...
        if after_notes:
            insert_before(after_notes[0], new)
        else:
            gate.append(new)
        loc = locator(new)
        write_xml(doc)
        return [Edit(site.file, loc, None, None, snippet(new), "insert", self.name)], {}, {}

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        out = []
        for rel, _, gate in self._gates(ws):
            mech, reason = self._classify(gate)
            if not mech:
                out.append(Inapplicable(self.name, rel, locator(gate), reason))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        """Only the gate's time scale may change, by the same factor k everywhere.

        The q10 mechanisms are accepted structurally even when this instance has the fallback
        disabled: they are this operator's fault (tau / k via rateScale), and whether a study
        uses them is a registration decision, not a property of a single record.
        """
        mech = record_param(record, "mechanism")
        k = record_param(record, "factor")
        files = transitive_includes(ref, cell_rel(ref))
        edits = record.edits

        def in_gate(e: Edit) -> bool:
            return step_name(parent_locator(e.locator)) in GATE_TAGS

        if mech == "rate_parameters":
            edits = expect_set_edits(record, attributes=("rate",), element=("forwardRate", "reverseRate"),
                                     files=files, count=2)
            require({step_name(e.locator) for e in edits} == {"forwardRate", "reverseRate"}, record,
                    "must scale the forward AND reverse rate of one gate")
            require(len({parent_locator(e.locator) for e in edits}) == 1 and in_gate(edits[0]), record,
                    "rates do not belong to one gate")
            for e in edits:
                require(is_scaled(e.old, e.new, k), record, f"rate {e.old!r} -> {e.new!r} is not a x{k} scaling")
        elif mech == "time_course_tau":
            [e] = expect_set_edits(record, attributes=("tau",), element=("timeCourse",), files=files)
            require(in_gate(e), record, "timeCourse is not a gate child")
            inv = Decimal(1) / Decimal(repr(float(k)))
            require(is_scaled(e.old, e.new, inv), record, f"tau {e.old!r} -> {e.new!r} is not tau / {k}")
        elif mech == "q10_scale":
            [e] = expect_set_edits(record, attributes=("fixedQ10",), element=("q10Settings",), files=files)
            require(in_gate(e), record, "q10Settings is not a gate child")
            require(is_scaled(e.old, e.new, k), record, f"fixedQ10 {e.old!r} -> {e.new!r} is not a x{k} scaling")
        elif mech == "q10_insert":
            require(len(edits) == 1 and edits[0].action == "insert" and edits[0].file in files, record,
                    "q10_insert must record exactly one insert")
            e = edits[0]
            el = parse_snippet(e.new)
            require(el is not None and localname(el) == "q10Settings" and step_name(e.locator) == "q10Settings"
                    and in_gate(e), record, "inserted element is not a gate's q10Settings")
            require(dict(el.attrib).keys() == {"type", "fixedQ10"} and el.get("type") == "q10Fixed"
                    and not element_children(el) and same_quantity(el.get("fixedQ10"), scale_quantity("1", k)),
                    record, f"inserted q10Settings is not q10Fixed with fixedQ10 = {k}")
        else:
            raise MutationError(f"{record.operator}: unknown mechanism {mech!r}")


# The q10Fixed mechanism is enabled (DECISIONS D-021): every core HH gate divides tau by the product of its
# q10 factors and leaves the steady state unchanged, so inserting/scaling q10Fixed scales exactly the time
# constant. Without it the operator has no sites in any Pospischil model (custom rate ComponentTypes).
for _op in (ScaleConductance(), ShiftReversal(), ScaleCapacitance(), ScaleGateTimeConstant(allow_q10_fallback=True),
            ShiftInitialVoltage(), WrongSegmentGroup()):
    register(_op)
