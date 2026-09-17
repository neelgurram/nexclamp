"""Prespecified mutation severity levels (PILOT2_PROTOCOL).

A site's severity comes only from its recorded magnitude, never from any result:
- multiplicative faults (``factor``): **mild** if |ln k| <= ln 1.25 (0.8 to 1.25),
  **strong** if |ln k| >= ln 2 (0.5 or 2), otherwise **intermediate**;
- voltage shifts (``shift_mV`` or ``delta_mV``): **mild** if |d| <= 5 mV, **strong** if |d| >= 10 mV,
  otherwise intermediate;
- operators without a magnitude (for example reference swaps): **not_applicable**.

Site selection then draws a fixed number of sites per requested level, with a seed per operator and
level, so the choice for one operator never depends on another.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

MILD, INTERMEDIATE, STRONG, NOT_APPLICABLE = "mild", "intermediate", "strong", "not_applicable"
_EPS = 1e-9


def severity(params: Mapping[str, Any]) -> str:
    if "factor" in params:
        k = float(params["factor"])
        m = abs(math.log(k))
        return MILD if m <= math.log(1.25) + _EPS else STRONG if m >= math.log(2.0) - _EPS else INTERMEDIATE
    for key in ("shift_mV", "delta_mV"):
        if key in params:
            d = abs(float(params[key]))
            return MILD if d <= 5.0 + _EPS else STRONG if d >= 10.0 - _EPS else INTERMEDIATE
    return NOT_APPLICABLE


def select_sites(sites: Sequence[Any], operator: str, seed: int, levels: Sequence[str],
                 per_level: int = 1, without_magnitude: int = 1) -> list[Any]:
    """``per_level`` sites for each level in ``levels``; ``without_magnitude`` sites if the operator has none."""
    from neuraxis.mutations.base import choose_sites

    graded = [s for s in sites if severity(s.params) != NOT_APPLICABLE]
    if not graded:
        return choose_sites(list(sites), without_magnitude, seed, operator)
    out = []
    for level in levels:
        pool = [s for s in graded if severity(s.params) == level]
        out += choose_sites(pool, per_level, seed, f"{operator}:{level}")
    return out
