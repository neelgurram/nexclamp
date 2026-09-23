"""Valid transformations and no-change controls (ARCHITECTURE.md section 3.5).

Valid transformations are representational edits that must not change tested behaviour.
Running them through the full pipeline estimates the false-positive rate of the detector;
a detection on one of them is a false alarm (or a genuine numerical sensitivity of the
simulator, which is itself worth reporting). Passing these controls never proves
equivalence -- it only shows that no difference was found by the finite battery.

Registry (names are binding):

=========================  ==================  =============================================
operator                   family              change
=========================  ==================  =============================================
``unit_conversion``        unit_conversion     exact decimal value in another XSD-allowed unit
``xml_formatting``         formatting          whitespace / attribute order (NO_CHANGE)
``add_comments``           formatting          XML comments (NO_CHANGE)
``numeric_literal_format`` literal_format      same number, different spelling
``rename_identifier``      renaming            id + every reference, incl. harness paths
``factor_file``            factoring           component moved to a new included file
``reorder_independent``    reordering          permute order-free sibling elements
``explicit_default``       explicit_default    omitted attribute written with its XSD default
=========================  ==================  =============================================
"""

from __future__ import annotations

import csv
import dataclasses as dc
import json
import random
import tempfile
from collections.abc import Sequence
from pathlib import Path

from nexclamp.models import Workspace, materialize
from nexclamp.provenance import utc_now
from nexclamp.schemas import ModelRecord, VariantKind, VariantRecord, dumps, to_jsonable
from nexclamp.transforms.factoring import FactorFile, ReorderIndependent
from nexclamp.transforms.formatting import AddComments, Site, TransformError, TransformOperator, XmlFormatting
from nexclamp.transforms.identifiers import RenameIdentifier
from nexclamp.transforms.units import ExplicitDefault, NumericLiteralFormat, UnitConversion

__all__ = [
    "MANIFEST_COLUMNS",
    "REGISTRY",
    "Site",
    "TransformError",
    "TransformOperator",
    "apply_model_overrides",
    "choose_sites",
    "generate_transforms",
    "write_manifest",
]

REGISTRY: dict[str, TransformOperator] = {op.name: op for op in (
    UnitConversion(), XmlFormatting(), AddComments(), NumericLiteralFormat(), RenameIdentifier(), FactorFile(),
    ReorderIndependent(), ExplicitDefault())}

MANIFEST_COLUMNS = ["variant_id", "model_id", "family", "operator", "params_json", "edits_json",
                    "exec_overrides_json", "description", "generator_seed", "no_change", "model_overrides_json"]


def choose_sites(sites: Sequence[Site], n: int, rng: random.Random) -> list[tuple[int, Site]]:
    """Up to ``n`` sites sampled without replacement, returned in their original (deterministic) order."""
    if n <= 0:
        return []
    idx = list(range(len(sites))) if n >= len(sites) else sorted(rng.sample(range(len(sites)), n))
    return [(i, sites[i]) for i in idx]


def apply_model_overrides(ws: Workspace, overrides: dict[str, str]) -> Workspace:
    """Workspace view whose ModelRecord reflects a variant's ``model_overrides`` (e.g. a renamed cell)."""
    fields = {f.name for f in dc.fields(ModelRecord)}
    unknown = set(overrides) - fields
    if unknown:
        raise ValueError(f"model_overrides keys are not ModelRecord fields: {sorted(unknown)}")
    return Workspace(ws.root, dc.replace(ws.model, **overrides)) if overrides else ws


def generate_transforms(model: ModelRecord, operators: Sequence[str], n_per_operator: int, seed: int,
                        root: Path) -> list[VariantRecord]:
    """Materialize, apply and record valid transformations of ``model``.

    Sites are enumerated on a pristine copy; for each operator up to ``n_per_operator`` of them
    are sampled with a generator seeded by ``(seed, model_id, operator)``, so adding an operator
    never changes the sites chosen for another. Each variant is written to
    ``root/<model_id>/<variant_id>/`` with its ``variant.json``.
    """
    unknown = [o for o in operators if o not in REGISTRY]
    if unknown:
        raise ValueError(f"unknown transform operators {unknown}; known: {sorted(REGISTRY)}")
    root = Path(root)
    (root / model.model_id).mkdir(parents=True, exist_ok=True)
    records: list[VariantRecord] = []
    with tempfile.TemporaryDirectory(prefix="ns_sites_", dir=root / model.model_id) as tmp:
        pristine = materialize(model, Path(tmp) / "pristine")
        parent_sha = pristine.tree_sha256()
        for op_name in operators:
            op = REGISTRY[op_name]
            sites = op.sites(pristine)
            rng = random.Random(f"{seed}:{model.model_id}:{op_name}")
            for k, (site_index, site) in enumerate(choose_sites(sites, n_per_operator, rng)):
                variant_id = f"{model.model_id}__{op_name}__{k:03d}"
                ws = materialize(model, root / model.model_id / variant_id, overwrite=True)
                edits, exec_overrides, model_overrides = op.apply(ws, site)
                record = VariantRecord(
                    variant_id=variant_id, model_id=model.model_id, kind=op.kind, family=op.family,
                    operator=op_name,
                    params={"file": site.file, "locator": site.locator, **site.params, "site_index": site_index,
                            "n_sites": len(sites), "generator_seed": seed},
                    edits=edits, exec_overrides=exec_overrides, model_overrides=model_overrides,
                    description=op.describe(site), parent_tree_sha256=parent_sha, tree_sha256=ws.tree_sha256(),
                    created_utc=utc_now())
                (ws.root / "variant.json").write_text(dumps(record), encoding="utf-8")
                records.append(record)
    return records


def write_manifest(records: Sequence[VariantRecord], path: Path) -> None:
    """Write ``data/valid_transforms.csv`` rows (mutation-manifest columns + no_change + model_overrides)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    def js(obj) -> str:
        return json.dumps(to_jsonable(obj), sort_keys=True, separators=(",", ":"))

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in records:
            w.writerow({"variant_id": r.variant_id, "model_id": r.model_id, "family": r.family,
                        "operator": r.operator, "params_json": js(r.params), "edits_json": js(r.edits),
                        "exec_overrides_json": js(r.exec_overrides), "description": r.description,
                        "generator_seed": r.params.get("generator_seed", ""),
                        "no_change": str(r.kind == VariantKind.NO_CHANGE).lower(),
                        "model_overrides_json": js(r.model_overrides)})
