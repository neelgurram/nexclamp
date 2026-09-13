"""Numerical mutations: faults in how the model is integrated, discretised or sampled.

Harness edits and ``exec_overrides`` go together: the harness edit mutates the canonical
run, the override applies the same fault to every NeuroSem-generated probe run, so the
fault is visible to both the canonical test and the battery.

Default grids: dt x2 is a plausible "speed-up" edit, x20 approaches forward-Euler
instability for fast Na kinetics; output sampling from 0.05 ms (harmless for most
features) to 2 ms (longer than an action potential's half-width, so shape features must
break).

``solver_config`` inserts ``<Meta for="jlems" method=...>``. The Milestone 0 source reading
of jLEMS ``Sim.java`` (docs/m0_evidence/tools/neuroml-lems.verify.json) found that jnml calls
``Sim.run()``, which already takes the consolidated (flattened) path, so ``method="rk4"`` is
a documented no-op; ``method="eulertree"`` does change the code path (it skips
consolidation and integrates the raw state tree, still with forward Euler), so evaluation
order may differ. Both were observed to give traces bit-identical to the reference on RS
(400 ms at dt 0.025 ms; tests/integration/test_mutants_validate.py). These mutants are
therefore *expected* to be equivalent under jnml, but for ``eulertree`` that is an
empirical observation on one model and simulator version, not established by construction.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from lxml import etree

from neurosem.models import Workspace
from neurosem.mutations.base import (
    Inapplicable,
    MutationError,
    OperatorBase,
    Site,
    apply_attribute_changes,
    attribute_site,
    cell_rel,
    element_children,
    expect_set_edits,
    harness_rel,
    harness_simulation,
    insert_before,
    is_scaled,
    iter_elements,
    localname,
    locator,
    parent_locator,
    parse_snippet,
    qualified,
    read_xml,
    record_param,
    register,
    require,
    resolve,
    scale_quantity,
    snippet,
    step_name,
    transitive_includes,
    write_xml,
)
from neurosem.mutations.biophysics import cell_element
from neurosem.schemas import Edit, MutationFamily, VariantRecord


def _harness_sim_locator(ref: Workspace) -> str:
    return locator(harness_simulation(read_xml(ref.harness_path).root))


class IncreaseDt(OperatorBase):
    name = "increase_dt"
    family = MutationFamily.NUMERICAL
    exec_override_keys = frozenset({"dt_factor"})

    # No x2: a x2 mutant simulated at the h/2 refinement level reruns the reference at h exactly, so its
    # difference can never exceed tau at h/2 and it could never be admissible (science-docs build note 1).
    def __init__(self, factors: Sequence[int] = (4, 10, 20)) -> None:
        self.factors = tuple(factors)

    def sites(self, ws: Workspace) -> list[Site]:
        rel = harness_rel(ws)
        sim = harness_simulation(read_xml(ws.path(rel)).root)
        old = sim.get("step")
        if old is None:
            return []
        return [attribute_site(self.name, rel, sim, [(sim, "step", old, scale_quantity(old, f))], factor=f)
                for f in self.factors]

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        self._check_site(site)
        return apply_attribute_changes(ws, site), {"dt_factor": site.params["factor"]}, {}

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        f = record_param(record, "factor")
        require(record.exec_overrides == {"dt_factor": f}, record,
                f"exec_overrides {record.exec_overrides} must be exactly {{'dt_factor': {f}}} (params.factor)")
        require(isinstance(f, (int, float)) and not isinstance(f, bool) and f > 1, record,
                f"dt_factor {f!r} does not increase dt")
        [e] = expect_set_edits(record, attributes=("step",), element=("Simulation", "Component"),
                               files=(harness_rel(ref),))
        require(e.locator == _harness_sim_locator(ref), record, "edit is not on the harness Simulation")
        require(is_scaled(e.old, e.new, f), record, f"harness step {e.old!r} -> {e.new!r} is not x dt_factor {f}")


class SolverConfig(OperatorBase):
    name = "solver_config"
    family = MutationFamily.NUMERICAL
    exec_override_keys = frozenset({"integrator_method"})

    def __init__(self, methods: Sequence[str] = ("rk4", "eulertree")) -> None:
        self.methods = tuple(methods)

    @staticmethod
    def _jlems_meta(sim):
        return next((c for c in element_children(sim) if localname(c) == "Meta" and c.get("for") == "jlems"), None)

    def sites(self, ws: Workspace) -> list[Site]:
        rel = harness_rel(ws)
        sim = harness_simulation(read_xml(ws.path(rel)).root)
        meta = self._jlems_meta(sim)
        out = []
        for m in self.methods:
            if meta is None:
                out.append(Site(self.name, rel, locator(sim), {"method": m, "mechanism": "insert_meta"}))
            elif meta.get("method") != m:
                out.append(attribute_site(self.name, rel, meta, [(meta, "method", meta.get("method"), m)],
                                          method=m, mechanism="set_meta_method"))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        self._check_site(site)
        overrides = {"integrator_method": site.params["method"]}
        if site.params["mechanism"] == "set_meta_method":
            return apply_attribute_changes(ws, site), overrides, {}
        doc = read_xml(ws.path(site.file))
        sim = resolve(doc.root, site.locator)
        if self._jlems_meta(sim) is not None:
            raise MutationError(f"stale site: {site.locator} already has a jlems Meta")
        new = etree.Element(qualified(sim, "Meta"))
        new.set("for", "jlems")
        new.set("method", site.params["method"])
        kids = element_children(sim)
        if kids:
            insert_before(kids[0], new)
        else:
            sim.append(new)
        loc = locator(new)
        write_xml(doc)
        return [Edit(site.file, loc, None, None, snippet(new), "insert", self.name)], overrides, {}

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        method = record_param(record, "method")
        require(isinstance(method, str) and method != "", record, "params.method must be a non-empty string")
        require(record.exec_overrides == {"integrator_method": method}, record,
                f"exec_overrides {record.exec_overrides} must be exactly {{'integrator_method': {method!r}}}")
        rel, sim_loc = harness_rel(ref), _harness_sim_locator(ref)
        mech = record_param(record, "mechanism")
        if mech == "insert_meta":
            require(len(record.edits) == 1, record, f"expected one insert, got {len(record.edits)} edits")
            e = record.edits[0]
            el = parse_snippet(e.new)
            require(e.action == "insert" and e.file == rel and step_name(e.locator) == "Meta"
                    and parent_locator(e.locator) == sim_loc, record, "must insert one Meta into the harness Simulation")
            require(el is not None and localname(el) == "Meta" and dict(el.attrib) == {"for": "jlems", "method": method}
                    and not element_children(el), record, f"inserted element is not <Meta for='jlems' method={method!r}/>")
        elif mech == "set_meta_method":
            [e] = expect_set_edits(record, attributes=("method",), element=("Meta",), files=(rel,))
            require(parent_locator(e.locator) == sim_loc, record, "Meta is not a child of the harness Simulation")
            require(resolve(read_xml(ref.harness_path).root, e.locator).get("for") == "jlems", record,
                    "edited Meta is not for jlems")
            require(e.new == method and e.old != method, record, "edit does not set params.method")
        else:
            raise MutationError(f"{record.operator}: unknown mechanism {mech!r}")


class ReduceSpatialDiscretization(OperatorBase):
    """Coarsen ``numberInternalDivisions`` segment-group properties of multicompartment cells.

    The property sets the number of compartments per section in simulators that honour it
    (NEURON export). jLEMS integrates one compartment per segment and is expected to ignore
    it, so under jNeuroML these mutants should be equivalent. Single-compartment cells
    yield no sites.
    """

    name = "reduce_spatial_discretization"
    family = MutationFamily.NUMERICAL

    def __init__(self, factors: Sequence[int] = (2, 4)) -> None:
        self.factors = tuple(factors)

    def _segments(self, ws: Workspace, scope) -> int:
        n = sum(1 for e in iter_elements(scope) if localname(e) == "segment")
        morph_ref = scope.get("morphology") if localname(scope) != "neuroml" else None
        if n == 0 and morph_ref:
            for rel in transitive_includes(ws, cell_rel(ws)):
                for m in iter_elements(read_xml(ws.path(rel)).root):
                    if localname(m) == "morphology" and m.get("id") == morph_ref:
                        return sum(1 for e in iter_elements(m) if localname(e) == "segment")
        return n

    def _properties(self, scope) -> list:
        return [p for p in iter_elements(scope) if localname(p) == "property"
                and p.get("tag") == "numberInternalDivisions" and p.getparent() is not None
                and localname(p.getparent()) == "segmentGroup"]

    def sites(self, ws: Workspace) -> list[Site]:
        _, scope = cell_element(ws)
        if self._segments(ws, scope) <= 1:
            return []
        out = []
        for p in self._properties(scope):
            try:
                old = int(p.get("value"))
            except (TypeError, ValueError):
                continue
            for f in self.factors:
                new = max(1, old // int(f))
                if new < old:
                    out.append(attribute_site(self.name, cell_rel(ws), p, [(p, "value", p.get("value"), str(new))],
                                              factor=f, segment_group=p.getparent().get("id")))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=("value",), element=("property",), files=(cell_rel(ref),))
        require(step_name(parent_locator(e.locator)) == "segmentGroup", record, "property is not on a segment group")
        require(resolve(read_xml(ref.cell_path).root, e.locator).get("tag") == "numberInternalDivisions", record,
                "property is not numberInternalDivisions")
        f = record_param(record, "factor")
        try:
            old, new = int(e.old), int(e.new)  # type: ignore[arg-type]
            expected = max(1, old // int(f))
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise MutationError(f"{record.operator}: non-integer divisions or factor: {exc}") from exc
        require(new == expected and new < old, record, f"divisions {old} -> {new} is not {old} // {f}")

    def inapplicable(self, ws: Workspace) -> list[Inapplicable]:
        _, scope = cell_element(ws)
        if self._segments(ws, scope) <= 1:
            return [Inapplicable(self.name, cell_rel(ws), locator(scope), "single-compartment cell")]
        if not self._properties(scope):
            return [Inapplicable(self.name, cell_rel(ws), locator(scope),
                                 "multicompartment cell without numberInternalDivisions properties")]
        return []


class RecordingResolution(OperatorBase):
    """Post-hoc output sampling (``exec_overrides.sample_every_ms``); no file is edited."""

    name = "recording_resolution"
    family = MutationFamily.NUMERICAL
    exec_override_keys = frozenset({"sample_every_ms"})
    LOCATOR = "exec_overrides.sample_every_ms"

    def __init__(self, sample_every_ms: Sequence[float] = (0.05, 0.25, 1.0, 2.0)) -> None:
        self.sample_every_ms = tuple(sample_every_ms)

    def sites(self, ws: Workspace) -> list[Site]:
        return [Site(self.name, "", self.LOCATOR, {"sample_every_ms": float(x)}) for x in self.sample_every_ms]

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        self._check_site(site)
        return [], {"sample_every_ms": site.params["sample_every_ms"]}, {}

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        require(not record.edits and set(record.exec_overrides) == {"sample_every_ms"}, record,
                "must set only exec_overrides.sample_every_ms")
        x = record.exec_overrides["sample_every_ms"]
        require(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x > 0, record,
                f"sample_every_ms {x!r} must be a positive finite number")
        require(x == record_param(record, "sample_every_ms"), record, "exec_overrides do not match params.sample_every_ms")


for _op in (IncreaseDt(), SolverConfig(), ReduceSpatialDiscretization(), RecordingResolution()):
    register(_op)
