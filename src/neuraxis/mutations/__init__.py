"""Mutation engine (ARCHITECTURE.md section 3.4).

Importing the package registers every operator in :data:`REGISTRY`.
"""

from neuraxis.mutations import biophysics, kinetics, numerical, references, stimulus  # noqa: F401  (registration)
from neuraxis.mutations.base import (
    GENERATOR_SEED_KEY,
    REGISTRY,
    Inapplicable,
    MutationError,
    MutationOperator,
    Site,
    enforce_single_operator,
    generate_mutants,
    inapplicable_sites,
    load_variant,
    write_manifest,
    xml_changes,
)

FAMILY_OPERATORS: dict[str, tuple[str, ...]] = {}
for _name, _op in REGISTRY.items():
    FAMILY_OPERATORS.setdefault(_op.family.value, ())
    FAMILY_OPERATORS[_op.family.value] += (_name,)

__all__ = [
    "FAMILY_OPERATORS",
    "GENERATOR_SEED_KEY",
    "REGISTRY",
    "Inapplicable",
    "MutationError",
    "MutationOperator",
    "Site",
    "enforce_single_operator",
    "generate_mutants",
    "inapplicable_sites",
    "load_variant",
    "write_manifest",
    "xml_changes",
]
