"""Tolerance-sensitivity summary from re-classified variants."""

from __future__ import annotations

import pandas as pd
import pytest

from neuraxis.experiments.analyze import tolerance_sensitivity


def test_rates_exclude_not_evaluable_and_count_them():
    rows = []
    for mult, classes in {1.0: ["6_silent_under_canonical", "4_equivalent_within_tested_domain", "5_non_equivalent"],
                          0.5: ["6_silent_under_canonical", "not_evaluable", "5_non_equivalent"]}.items():
        for i, c in enumerate(classes):
            rows.append({"variant_id": f"m{i}", "kind": "mutant", "tolerance_multiplier": mult, "class": c})
        rows.append({"variant_id": "t0", "kind": "valid_transform", "tolerance_multiplier": mult,
                     "class": "5_non_equivalent" if mult == 0.5 else "4_equivalent_within_tested_domain"})
    sens, notes = tolerance_sensitivity(pd.DataFrame(rows))
    get = lambda m, s: sens[(sens.tolerance_multiplier == m) & (sens.series == s)].rate.item()
    assert get(1.0, "admissible_fraction_of_mutants") == pytest.approx(2 / 3)
    assert get(1.0, "silent_fraction_of_mutants") == pytest.approx(1 / 3)
    assert get(0.5, "admissible_fraction_of_mutants") == pytest.approx(1.0)   # not_evaluable excluded from denominator
    assert get(0.5, "false_positive_rate") == pytest.approx(1.0) and get(1.0, "false_positive_rate") == 0.0
    assert notes["0.5"]["not_evaluable"] == 1 and notes["1.0"]["not_evaluable"] == 0
