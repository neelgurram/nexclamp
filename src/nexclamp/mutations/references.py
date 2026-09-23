"""Reference mutations: the model points at the wrong thing, or loses/duplicates a reference.

``wrong_channel`` and ``wrong_compatible_component`` partition the alternatives by ion
species (different species vs same species) so the two operators never generate the same
mutant under two labels, which would double-count it in per-family statistics.
"""

from __future__ import annotations

from nexclamp.models import Workspace
from nexclamp.mutations.base import (
    MutationError,
    OperatorBase,
    Site,
    attribute_site,
    cell_rel,
    deepcopy_element,
    element_children,
    expect_set_edits,
    insert_after,
    iter_elements,
    localname,
    locator,
    locator_steps,
    parent_locator,
    parse_snippet,
    read_xml,
    record_param,
    register,
    remove_element,
    require,
    resolve,
    signature,
    snippet,
    step_name,
    transitive_includes,
    write_xml,
)
from nexclamp.mutations.biophysics import CHANNEL_TAGS, cell_element, channel_densities, is_channel_density
from nexclamp.schemas import Edit, MutationFamily, VariantRecord


def channel_catalog(ws: Workspace) -> dict[str, tuple[str, str]]:
    """channel id -> (file, species) for every ion channel reachable from the cell file (first definition wins)."""
    out: dict[str, tuple[str, str]] = {}
    for rel in transitive_includes(ws, cell_rel(ws)):
        for el in iter_elements(read_xml(ws.path(rel)).root):
            if localname(el) in CHANNEL_TAGS and el.get("id") and el.get("id") not in out:
                out[el.get("id")] = (rel, el.get("species") or "non_specific")
    return out


class _SwapChannel(OperatorBase):
    family = MutationFamily.REFERENCE
    same_species: bool

    def sites(self, ws: Workspace) -> list[Site]:
        catalog = channel_catalog(ws)
        _, scope = cell_element(ws)
        out = []
        for el in channel_densities(scope):
            current = el.get("ionChannel")
            if current not in catalog:
                continue
            species = catalog[current][1]
            for cid, (_, sp) in catalog.items():
                if cid != current and (sp == species) == self.same_species:
                    out.append(attribute_site(self.name, cell_rel(ws), el, [(el, "ionChannel", current, cid)],
                                              element_id=el.get("id"), old_species=species, new_species=sp))
        return out

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        [e] = expect_set_edits(record, attributes=("ionChannel",), element=is_channel_density, files=(cell_rel(ref),))
        catalog = channel_catalog(ref)
        require(e.old in catalog and e.new in catalog and e.old != e.new, record,
                f"{e.old!r} -> {e.new!r} is not a swap between two channels defined in the includes")
        same = catalog[e.old][1] == catalog[e.new][1]
        require(same == self.same_species, record,
                f"species {catalog[e.old][1]} -> {catalog[e.new][1]} violates this operator's species relation")


class WrongChannel(_SwapChannel):
    name = "wrong_channel"
    same_species = False


class WrongCompatibleComponent(_SwapChannel):
    name = "wrong_compatible_component"
    same_species = True


class OmitInclude(OperatorBase):
    name = "omit_include"
    family = MutationFamily.REFERENCE

    def sites(self, ws: Workspace) -> list[Site]:
        doc = read_xml(ws.cell_path)
        return [Site(self.name, cell_rel(ws), locator(el), {"href": el.get("href"), "removed": snippet(el)})
                for el in element_children(doc.root) if localname(el) == "include" and el.get("href")]

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        self._check_site(site)
        doc = read_xml(ws.path(site.file))
        el = resolve(doc.root, site.locator)
        if el.get("href") != site.params["href"]:
            raise MutationError(f"stale site: {site.locator} href is {el.get('href')!r}")
        old = snippet(el)
        remove_element(el)
        write_xml(doc)
        return [Edit(site.file, site.locator, None, old, None, "remove", self.name)], {}, {}

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        require(len(record.edits) == 1, record, f"expected one removal, got {len(record.edits)} edits")
        e = record.edits[0]
        require(e.action == "remove" and e.attribute is None and e.file == cell_rel(ref), record,
                "must remove one element of the cell file")
        el = parse_snippet(e.old)
        require(el is not None and localname(el) == "include" and step_name(e.locator) == "include"
                and len(locator_steps(e.locator)) == 2, record, "removed element is not a top-level <include>")
        require(el.get("href") == record_param(record, "href"), record, "removed include does not match params.href")


class DuplicateConductance(OperatorBase):
    """Insert a copy of one channel density (new id) directly after the original.

    Placing the copy next to the original keeps the XSD ``membraneProperties`` sequence order.
    """

    name = "duplicate_conductance"
    family = MutationFamily.REFERENCE

    def sites(self, ws: Workspace) -> list[Site]:
        doc, scope = cell_element(ws)
        ids = {e.get("id") for e in iter_elements(doc.root) if e.get("id")}
        out = []
        for el in channel_densities(scope):
            base = f"{el.get('id')}_dup"
            new_id, i = base, 2
            while new_id in ids:
                new_id, i = f"{base}{i}", i + 1
            out.append(Site(self.name, cell_rel(ws), locator(el), {"source_id": el.get("id"), "new_id": new_id}))
        return out

    def apply(self, ws: Workspace, site: Site) -> tuple[list[Edit], dict, dict]:
        self._check_site(site)
        doc = read_xml(ws.path(site.file))
        el = resolve(doc.root, site.locator)
        if el.get("id") != site.params["source_id"]:
            raise MutationError(f"stale site: {site.locator}")
        if any(e.get("id") == site.params["new_id"] for e in iter_elements(doc.root)):
            raise MutationError(f"id {site.params['new_id']!r} already exists")
        dup = deepcopy_element(el)
        dup.set("id", site.params["new_id"])
        insert_after(el, dup)
        write_xml(doc)
        return [Edit(site.file, locator(dup), None, None, snippet(dup), "insert", self.name)], {}, {}

    def check_record(self, record: VariantRecord, ref: Workspace) -> None:
        """One inserted channel density that is an exact copy of an existing one except for its id."""
        require(len(record.edits) == 1, record, f"expected one insert, got {len(record.edits)} edits")
        e = record.edits[0]
        require(e.action == "insert" and e.file == cell_rel(ref) and is_channel_density(step_name(e.locator)),
                record, "must insert one channel density into the cell file")
        dup = parse_snippet(e.new)
        source_id, new_id = record_param(record, "source_id"), record_param(record, "new_id")
        require(dup is not None and is_channel_density(localname(dup)) and dup.get("id") == new_id, record,
                "inserted element is not a channel density with params.new_id")
        doc, scope = cell_element(ref)
        require(all(x.get("id") != new_id for x in iter_elements(doc.root)), record, f"id {new_id!r} already exists")
        sources = [c for c in channel_densities(scope) if c.get("id") == source_id]
        require(len(sources) == 1, record, f"source channel density {source_id!r} not found")
        require(parent_locator(e.locator) == parent_locator(locator(sources[0])), record,
                "copy is not placed beside its source")
        restored = deepcopy_element(dup)
        restored.set("id", source_id)
        require(signature(restored) == signature(sources[0]), record, "inserted copy differs from its source")


for _op in (WrongChannel(), OmitInclude(), DuplicateConductance(), WrongCompatibleComponent()):
    register(_op)
