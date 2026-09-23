"""Analysis strata and feature panels (DECISIONS D-029, D-030).

Neel's N-15 decision:
- Primary semantic-mutation comparisons use identical solver and time-step settings for the
  reference and the variant.
- Time-step, solver, spatial-discretization and recording-resolution changes are
  *numerical robustness and convergence stress tests*. They are analysed separately and never
  enter the primary semantic-drift denominator.
- A numerical result is never called hidden semantic drift.

Neel's N-14 feature decision:
- Each protocol has a *primary* prespecified feature panel that alone decides the primary
  classification.
- *Secondary* exploratory features are extracted from the same traces and reported, but they
  never change a primary result.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from nexclamp.schemas import Edit, MutantClass, MutationFamily, VariantKind, VariantRecord

SEMANTIC = "primary_semantic"
NUMERICAL = "numerical_robustness"
HARNESS = "harness_stimulus"
CONTROL = "control"
REFERENCE = "reference"

SEMANTIC_FAMILIES = frozenset({MutationFamily.BIOPHYSICAL.value, MutationFamily.REFERENCE.value,
                               MutationFamily.KINETICS.value})
# D-037: never used to select the protocol battery ("excluded from protocol selection").
SELECTION_EXCLUDED_FAMILIES = frozenset({MutationFamily.KINETICS.value})
NUMERICAL_FAMILIES = frozenset({MutationFamily.NUMERICAL.value})
HARNESS_FAMILIES = frozenset({MutationFamily.STIMULUS.value})
# Checked by operator name as well as family, so a mislabelled numerical operator cannot enter the primary corpus.
NUMERICAL_OPERATORS = frozenset({"increase_dt", "solver_config", "reduce_spatial_discretization",
                                 "recording_resolution"})
# Attributes that set solver, step or discretisation. A primary-stratum variant may rewrite them only to an
# equal quantity (for example a unit conversion by a valid transformation).
NUMERIC_ATTRIBUTES = frozenset({"step", "method", "numberInternalDivisions"})


# Prespecified, scientifically interpretable analysis families (PILOT2_PROTOCOL).
ANALYSIS_FAMILY = {
    "scale_conductance": "maximal_conductance",
    "shift_reversal": "reversal_potential",
    "scale_capacitance": "passive_membrane",
    "shift_initial_voltage": "initial_state",
    "wrong_segment_group": "channel_distribution",
    "scale_gate_time_constant": "gating_time_constant",
    "shift_gate_midpoint": "gating_voltage_dependence",
    "scale_gate_slope": "gating_voltage_dependence",
    "shift_forward_rate_midpoint": "gating_voltage_dependence",
    "shift_channel_vshift": "gating_voltage_dependence",
    "wrong_channel": "mechanism_composition",
    "wrong_compatible_component": "mechanism_composition",
    "omit_include": "mechanism_composition",
    "duplicate_conductance": "mechanism_composition",
}


def analysis_family(operator: str, family: str = "") -> str:
    if operator in ANALYSIS_FAMILY:
        return ANALYSIS_FAMILY[operator]
    if operator in NUMERICAL_OPERATORS or family in NUMERICAL_FAMILIES:
        return "numerical_robustness"
    if family in HARNESS_FAMILIES:
        return "harness_stimulus"
    return "control" if not family or family not in SEMANTIC_FAMILIES else family


class StratumError(ValueError):
    """A variant would enter the wrong analysis stratum or run with different numerics."""


def stratum(kind: VariantKind | str, family: str, operator: str = "") -> str:
    kind = kind if isinstance(kind, VariantKind) else VariantKind(kind)
    if kind is VariantKind.REFERENCE:
        return REFERENCE
    if kind in (VariantKind.VALID_TRANSFORM, VariantKind.NO_CHANGE):
        return CONTROL
    if operator in NUMERICAL_OPERATORS or family in NUMERICAL_FAMILIES:
        return NUMERICAL
    if family in HARNESS_FAMILIES:
        return HARNESS
    if family in SEMANTIC_FAMILIES:
        return SEMANTIC
    raise StratumError(f"unknown mutation family {family!r} (operator {operator!r})")


def variant_stratum(v: VariantRecord) -> str:
    return stratum(v.kind, v.family, v.operator)


def _same_quantity(old: str | None, new: str | None) -> bool:
    if old == new:
        return True
    if old is None or new is None:
        return False
    from nexclamp.mutations.base import quantity_si

    try:
        a, b = quantity_si(old), quantity_si(new)
    except (TypeError, ValueError, KeyError):
        return False
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)


def check_identical_numerics(v: VariantRecord) -> None:
    """Primary semantic mutants and controls run with exactly the reference's solver and time step."""
    s = variant_stratum(v)
    if s not in (SEMANTIC, CONTROL):
        return
    if v.exec_overrides:
        raise StratumError(f"{v.variant_id}: {s} variant carries execution overrides {v.exec_overrides}; primary "
                           "comparisons require identical solver and time-step settings")
    for e in v.edits:
        e = e if isinstance(e, Edit) else Edit(**e)
        if e.attribute in NUMERIC_ATTRIBUTES and not _same_quantity(e.old, e.new):
            raise StratumError(f"{v.variant_id}: {s} variant changes numerical attribute {e.attribute!r} "
                               f"({e.old!r} -> {e.new!r}) in {e.file}")


def primary_admissible(outcomes: Iterable[Any]) -> list[Any]:
    """The primary semantic-drift denominator: admissible mutants of the semantic stratum only."""
    out = [o for o in outcomes if o.variant.kind is VariantKind.MUTANT and variant_stratum(o.variant) == SEMANTIC
           and o.klass.admissible]
    assert_primary_denominator(o.variant for o in out)
    return out


def assert_primary_denominator(variants: Iterable[VariantRecord]) -> None:
    bad = [(v.variant_id, variant_stratum(v)) for v in variants
           if v.kind is not VariantKind.MUTANT or variant_stratum(v) != SEMANTIC]
    if bad:
        raise StratumError(f"non-semantic variants in the primary denominator: {bad[:5]}")


def select_mutation_operators(families: Sequence[str], exclude: Iterable[str] = ()) -> list[str]:
    """Registered operators of ``families`` minus ``exclude`` (unknown names are an error)."""
    from nexclamp import mutations

    excluded = set(exclude)
    unknown = excluded - set(mutations.REGISTRY)
    if unknown:
        raise StratumError(f"exclude_operators names unknown operators: {sorted(unknown)}")
    return [name for name, op in mutations.REGISTRY.items()
            if getattr(op.family, "value", op.family) in families and name not in excluded]


# --------------------------------------------------------------------------- feature panels
def split_primary(dets: Sequence[Any], primary_panel: Mapping[str, frozenset[str]]) -> tuple[list[Any], list[Any]]:
    """Split detections into the primary panel and secondary exploratory features.

    A protocol missing from ``primary_panel`` keeps all its features primary (the behaviour
    when no secondary features are configured).
    """
    primary, secondary = [], []
    for d in dets:
        panel = primary_panel.get(d.protocol_id)
        (primary if panel is None or d.feature in panel else secondary).append(d)
    return primary, secondary


def interpretation(stratum_: str, klass: MutantClass) -> str:
    """Plain label for reports. Numerical results are never labelled as semantic drift."""
    if stratum_ == NUMERICAL:
        return {MutantClass.SILENT: "numerical_sensitivity_missed_by_canonical (not semantic drift)",
                MutantClass.NON_EQUIVALENT: "numerical_sensitivity_detected_by_canonical",
                MutantClass.EQUIVALENT: "no_reproducible_numerical_sensitivity"}.get(klass, klass.value)
    if stratum_ == CONTROL:
        return "false_positive" if klass.admissible else ("no_detection" if klass is MutantClass.EQUIVALENT
                                                          else klass.value)
    return klass.value


# --------------------------------------------------------------------------- convergence workflow
def _num(fv: Any) -> float | None:
    if fv is None or getattr(fv, "state", None) != "defined":
        return None
    try:
        x = float(fv.value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def numerical_robustness_rows(ref_fps: Mapping[int, Any], var_fps: Mapping[int, Any], variant: VariantRecord,
                              c: float = 3.0) -> list[dict[str, Any]]:
    """Per (protocol, feature): the variant's deviation against the reference's own discretisation error.

    ``ref_fps`` and ``var_fps`` map refinement factor (1 = h, 2 = h/2, 4 = h/4) to fingerprints.
    The reference error at h is |f(h) - f(h/2)|; the observed order is log2 of the ratio of
    successive reference errors. A deviation within ``c`` times the reference error at h is
    labelled as within discretisation error. None of these labels is a semantic classification.
    """
    rows: list[dict[str, Any]] = []
    r1 = ref_fps.get(1)
    if r1 is None:
        raise ValueError("reference fingerprint at h is required")
    for pid, table in sorted(r1.tables.items()):
        for feat, rv1 in sorted(table.items()):
            def at(fps: Mapping[int, Any], f: int):
                fp = fps.get(f)
                return None if fp is None else fp.tables.get(pid, {}).get(feat)

            ref = {f: _num(at(ref_fps, f)) for f in (1, 2, 4)}
            var = {f: _num(at(var_fps, f)) for f in (1, 2, 4)}
            err_h = abs(ref[1] - ref[2]) if ref[1] is not None and ref[2] is not None else None
            err_h2 = abs(ref[2] - ref[4]) if ref[2] is not None and ref[4] is not None else None
            order = math.log2(err_h / err_h2) if err_h and err_h2 else None
            dev = {f: abs(var[f] - ref[f]) if var[f] is not None and ref[f] is not None else None for f in (1, 2, 4)}
            v1 = at(var_fps, 1)
            if v1 is None:
                label = "not_run"
            elif getattr(rv1, "state", None) != getattr(v1, "state", None):
                label = "definedness_change"
            elif ref[1] is None:
                label = "categorical_change" if rv1.value != v1.value else "no_change"
            elif dev[1] is None:
                label = "not_evaluable"
            elif err_h is None:
                label = "reference_error_unknown"
            elif dev[1] <= c * err_h:
                label = "within_reference_discretization_error"
            else:
                label = "exceeds_reference_discretization_error"
            rows.append({"variant_id": variant.variant_id, "model_id": variant.model_id, "operator": variant.operator,
                         "exec_overrides": json.dumps(dict(variant.exec_overrides), sort_keys=True),
                         "protocol_id": pid, "feature": feat,
                         "ref_h": ref[1], "ref_h2": ref[2], "ref_h4": ref[4], "ref_error_h": err_h,
                         "ref_error_h2": err_h2, "ref_observed_order": order, "var_h": var[1], "var_h2": var[2],
                         "var_h4": var[4], "deviation_h": dev[1], "deviation_h2": dev[2], "deviation_h4": dev[4],
                         "deviation_over_ref_error_h": (dev[1] / err_h if dev[1] is not None and err_h else None),
                         "label": label})
    return rows
