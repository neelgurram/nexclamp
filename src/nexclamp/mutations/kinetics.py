"""Ion-channel kinetics mutations (family 2 of the prospective taxonomy; DECISIONS D-037).

Each operator makes one documented change to the gating of one channel, keeps units and
dimensions, and never touches the stimulus, the solver or the time step. The family's detection
matrix is never used to select the protocol battery: it is labelled "excluded from protocol
selection" (not "completely unseen by the researchers": its operators are exercised for
correctness on development fixtures in the test suite).

Operators
- ``shift_gate_midpoint``: shift one gate's voltage dependence rigidly by d mV. Both core rate
  midpoints (alpha and beta) of a rate gate move, together with a core steady-state midpoint if the
  gate has one; a time-course gate moves its steady-state midpoint.
- ``scale_gate_slope``: multiply the voltage-dependence scale (slope) of the same elements by k.
- ``shift_forward_rate_midpoint``: shift only the opening (forward) rate midpoint of a pure rate gate,
  which changes the shape of both the steady-state and time-constant curves.
- ``shift_channel_vshift``: shift the ``vShift`` of one ``channelDensityVShift`` (NeuroML core
  semantics: the whole channel's voltage dependence moves by vShift).

Gates whose rates or steady states are custom LEMS ComponentTypes have no such parameter; they are
reported by :meth:`inapplicable` (for example every gate of the Pospischil 2008 channels).
"""

from __future__ import annotations

from collections.abc import Sequence

from nexclamp.models import Workspace
from nexclamp.mutations.base import (
    Inapplicable,
    OperatorBase,
    Site,
    attribute_site,
    cell_rel,
    element_children,
    expect_set_edits,
    is_scaled,
    is_shifted,
    localname,
    locator,
    parent_locator,
    read_xml,
    record_param,
    register,
    require,
    resolve,
    scale_quantity,
    shift_quantity,
    step_name,
    transitive_includes,
)
from nexclamp.mutations.biophysics import CORE_RATES, GATE_TAGS, cell_element, channel_densities, used_channels
from nexclamp.schemas import MutationFamily, VariantRecord

MIDPOINT_DELTAS_MV = (-10.0, -5.0, 5.0, 10.0)
SLOPE_FACTORS = (0.8, 1.25)
FORWARD_DELTAS_MV = (-5.0, 5.0)
VSHIFT_DELTAS_MV = (-5.0, 5.0)
CORE_VARIABLES = ("HHSigmoidVariable", "HHExpVariable", "HHExpLinearVariable")
VOLTAGE_CHILDREN = ("forwardRate", "reverseRate", "steadyState")


def voltage_targets(gate, attr: str, forward_only: bool = False) -> tuple[str, list, str]:
    """(mechanism, elements, reason) for the elements whose ``attr`` sets ``gate``'s voltage dependence."""
    kids = {localname(c): c for c in element_children(gate)}
    fr, rr, ss = kids.get("forwardRate"), kids.get("reverseRate"), kids.get("steadyState")
    core_ss = ss is not None and ss.get("type") in CORE_VARIABLES and ss.get(attr) is not None
    if fr is not None and rr is not None:
        core_rates = all(r.get("type") in CORE_RATES and r.get(attr) is not None for r in (fr, rr))
        if not core_rates:
            return "", [], f"rates {fr.get('type')}/{rr.get('type')} are not core rate types with {attr!r}"
        if forward_only:
            if ss is not None:
                return "", [], "gate has a steady-state element; a forward-only shift would be overridden"
            return "forward_rate", [fr], ""
        if ss is not None and not core_ss:
            return "", [], f"steadyState {ss.get('type')} is not a core variable with {attr!r}"
        return ("rates_and_steady_state", [fr, rr, ss], "") if ss is not None else ("rates", [fr, rr], "")
    if forward_only:
        return "", [], "not a rate gate (no forward and reverse rate)"
    if core_ss:
        return "steady_state", [ss], ""
    return "", [], f"gate type {gate.get('type') or localname(gate)} has no core rate or steady state with {attr!r}"


class _GateVoltageOperator(OperatorBase):
    family = MutationFamily.KINETICS
    container_children = frozenset(VOLTAGE_CHILDREN)
    attr = "midpoint"
    forward_only = False

    def _gates(self, ws: Workspace):
        for rel, ch in used_channels(ws):
            for gate in element_children(ch):
                if localname(gate) in GATE_TAGS:
                    yield rel, ch, gate

    def _change(self, old: str, value: float) -> str:
        raise NotImplementedError

    def _ok(self, old: str | None, new: str | None, value: float) -> bool:
        raise NotImplementedError

    values: Sequence[float] = ()
    value_key = "delta_mV"

    def sites(self, ws: Workspace) -> list[Site]:
        out = []
        for rel, ch, gate in self._gates(ws):
            mech, targets, _ = voltage_targets(gate, self.attr, self.forward_only)
            if not mech:
                continue
            for v in self.values:
                changes = [(el, self.attr, el.get(self.attr), self._change(el.get(self.attr), v)) for el in targets]
                out.append(attribute_site(self.name, rel, gate, changes, mechanism=mech, channel=ch.get("id"),
                                          gate=gate.get("id"), **{self.value_key: v}))
        return out

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        out = []
        for rel, _, gate in self._gates(ws):
            mech, _, reason = voltage_targets(gate, self.attr, self.forward_only)
            if not mech:
                out.append(Inapplicable(self.name, rel, locator(gate), reason))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        v = record_param(record, self.value_key)
        files = transitive_includes(ref, cell_rel(ref))
        edits = expect_set_edits(record, attributes=(self.attr,), element=VOLTAGE_CHILDREN, files=files, count=range(1, 4))
        parents = {(e.file, parent_locator(e.locator)) for e in edits}
        require(len(parents) == 1, record, "edits do not belong to one gate")
        (file, gate_loc), = parents
        require(step_name(gate_loc) in GATE_TAGS, record, "edited elements are not children of a gate")
        gate = resolve(read_xml(ref.path(file)).root, gate_loc)
        mech, targets, reason = voltage_targets(gate, self.attr, self.forward_only)
        require(bool(mech), record, f"gate is not a valid target: {reason}")
        require(mech == record_param(record, "mechanism"), record, f"mechanism {mech!r} does not match the record")
        require(sorted(step_name(e.locator) for e in edits) == sorted(localname(t) for t in targets), record,
                f"must change exactly {[localname(t) for t in targets]}")
        for e in edits:
            require(self._ok(e.old, e.new, v), record, f"{self.attr} {e.old!r} -> {e.new!r} is not the {self.name} change {v}")


class ShiftGateMidpoint(_GateVoltageOperator):
    name = "shift_gate_midpoint"
    attr = "midpoint"

    def __init__(self, deltas_mV: Sequence[float] = MIDPOINT_DELTAS_MV) -> None:
        self.values = tuple(deltas_mV)

    def _change(self, old: str, value: float) -> str:
        return shift_quantity(old, value, "mV")

    def _ok(self, old, new, value) -> bool:
        return is_shifted(old, new, value, "mV")


class ScaleGateSlope(_GateVoltageOperator):
    name = "scale_gate_slope"
    attr = "scale"
    value_key = "factor"

    def __init__(self, factors: Sequence[float] = SLOPE_FACTORS) -> None:
        self.values = tuple(factors)

    def _change(self, old: str, value: float) -> str:
        return scale_quantity(old, value)

    def _ok(self, old, new, value) -> bool:
        return is_scaled(old, new, value)


class ShiftForwardRateMidpoint(ShiftGateMidpoint):
    name = "shift_forward_rate_midpoint"
    forward_only = True
    container_children = frozenset({"forwardRate"})

    def __init__(self, deltas_mV: Sequence[float] = FORWARD_DELTAS_MV) -> None:
        super().__init__(deltas_mV)


class ShiftChannelVShift(OperatorBase):
    """Shift ``vShift`` of one ``channelDensityVShift`` by d mV (the channel's whole voltage dependence)."""

    name = "shift_channel_vshift"
    family = MutationFamily.KINETICS

    def __init__(self, deltas_mV: Sequence[float] = VSHIFT_DELTAS_MV) -> None:
        self.deltas = tuple(deltas_mV)

    def sites(self, ws: Workspace) -> list[Site]:
        _, scope = cell_element(ws)
        out = []
        for el in channel_densities(scope):
            if localname(el) != "channelDensityVShift" or el.get("vShift") is None:
                continue
            for d in self.deltas:
                out.append(attribute_site(self.name, cell_rel(ws), el,
                                          [(el, "vShift", el.get("vShift"), shift_quantity(el.get("vShift"), d, "mV"))],
                                          element_id=el.get("id"), channel=el.get("ionChannel"), delta_mV=d))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=("vShift",), element=("channelDensityVShift",), files=(cell_rel(ref),))
        d = record_param(record, "delta_mV")
        require(is_shifted(e.old, e.new, d, "mV"), record, f"vShift {e.old!r} -> {e.new!r} is not a shift by {d} mV")


for _op in (ShiftGateMidpoint(), ScaleGateSlope(), ShiftForwardRateMidpoint(), ShiftChannelVShift()):
    register(_op)
