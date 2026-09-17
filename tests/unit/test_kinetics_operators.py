"""Ion-channel kinetics family (D-037): one documented gating change, valid units, provenance enforced.

The operators are exercised for correctness on development fixtures only; no detection data are made.
"""

from __future__ import annotations

import pytest

from neuraxis.models import copy_workspace
from neuraxis.mutations import REGISTRY
from neuraxis.mutations.base import (
    MutationError,
    element_children,
    enforce_single_operator,
    localname,
    read_xml,
    resolve,
)
from neuraxis.experiments import strata
from neuraxis.schemas import Edit, MutationFamily, VariantKind, VariantRecord

KINETICS = ("shift_gate_midpoint", "scale_gate_slope", "shift_forward_rate_midpoint", "shift_channel_vshift")


def mutate(ref, tmp_path, site, tag="k"):
    op = REGISTRY[site.operator]
    var = copy_workspace(ref, tmp_path / f"{tag}_{site.operator}")
    edits, exec_o, model_o = op.apply(var, site)
    rec = VariantRecord("t", ref.model.model_id, VariantKind.MUTANT, op.family.value, op.name, dict(site.params),
                        edits, exec_o, model_o, tree_sha256=var.tree_sha256(), parent_tree_sha256=ref.tree_sha256())
    enforce_single_operator(ref, var, rec)
    return var, rec


def pick(sites, **match):
    return next(s for s in sites if all(s.params.get(k) == v for k, v in match.items()))


def test_family_is_semantic_and_excluded_from_selection():
    for name in KINETICS:
        op = REGISTRY[name]
        assert op.family is MutationFamily.KINETICS and not op.exec_override_keys
        assert strata.stratum(VariantKind.MUTANT, op.family.value, name) == strata.SEMANTIC
    assert MutationFamily.KINETICS.value in strata.SELECTION_EXCLUDED_FAMILIES


def test_shift_gate_midpoint_moves_both_rates_of_one_gate(hh_ws, tmp_path):
    sites = REGISTRY["shift_gate_midpoint"].sites(hh_ws)
    assert len(sites) == 3 * 4 and {s.params["mechanism"] for s in sites} == {"rates"}
    site = pick(sites, gate="m", delta_mV=5.0)
    var, rec = mutate(hh_ws, tmp_path, site)
    gate = resolve(read_xml(var.cell_path).root, site.locator)
    mids = {localname(c): c.get("midpoint") for c in element_children(gate)}
    assert mids == {"forwardRate": "-35mV", "reverseRate": "-60mV"}
    assert len(rec.edits) == 2 and {e.attribute for e in rec.edits} == {"midpoint"}
    strata.check_identical_numerics(rec)              # no stimulus, solver or step change


def test_scale_gate_slope_keeps_sign_and_unit(hh_ws, tmp_path):
    site = pick(REGISTRY["scale_gate_slope"].sites(hh_ws), gate="h", factor=1.25)
    var, rec = mutate(hh_ws, tmp_path, site)
    gate = resolve(read_xml(var.cell_path).root, site.locator)
    scales = {localname(c): c.get("scale") for c in element_children(gate)}
    assert scales["forwardRate"] == "-25mV"
    assert all(e.new.endswith("mV") for e in rec.edits)


def test_forward_only_shift_changes_one_rate(hh_ws, tmp_path):
    site = pick(REGISTRY["shift_forward_rate_midpoint"].sites(hh_ws), gate="n", delta_mV=-5.0)
    _, rec = mutate(hh_ws, tmp_path, site)
    assert [(e.old, e.new) for e in rec.edits] == [("-55mV", "-60mV")]


def test_channel_vshift_shift_on_pospischil(rs_ws, tmp_path):
    sites = REGISTRY["shift_channel_vshift"].sites(rs_ws)
    assert {s.params["element_id"] for s in sites} == {"Na_all"}
    _, rec = mutate(rs_ws, tmp_path, pick(sites, delta_mV=5.0))
    assert (rec.edits[0].old, rec.edits[0].new) == ("0mV", "5mV")


def test_custom_rate_gates_are_reported_inapplicable(rs_ws):
    op = REGISTRY["shift_gate_midpoint"]
    assert op.sites(rs_ws) == []
    reasons = [i.reason for i in op.inapplicable(rs_ws)]
    assert reasons and all("not core rate types" in r or "no core rate" in r for r in reasons)


def test_check_record_rejects_a_forged_change(hh_ws, tmp_path):
    site = pick(REGISTRY["shift_gate_midpoint"].sites(hh_ws), gate="m", delta_mV=5.0)
    _, rec = mutate(hh_ws, tmp_path, site)
    forged = [Edit(e.file, e.locator, e.attribute, e.old, "-30mV" if e.old == "-40mV" else e.new) for e in rec.edits]
    bad = VariantRecord("t", rec.model_id, rec.kind, rec.family, rec.operator, rec.params, forged)
    with pytest.raises(MutationError):
        REGISTRY["shift_gate_midpoint"].check_record(bad, hh_ws)
    one = VariantRecord("t", rec.model_id, rec.kind, rec.family, rec.operator, rec.params, rec.edits[:1])
    with pytest.raises(MutationError):
        REGISTRY["shift_gate_midpoint"].check_record(one, hh_ws)
