"""Kinetics operators simulate correctly on development fixtures (D-037 gate before any study use)."""

from __future__ import annotations

import pytest

from neuraxis.orchestration.kinetics_validation import KINETICS_OPERATORS, default_fixtures, validate_fixtures


@pytest.mark.jnml
def test_kinetics_operators_pass_validation_on_fixtures(tmp_path):
    report = validate_fixtures(tmp_path / "out", default_fixtures(tmp_path / "fx"), max_sites=2)
    rows = [r for r in report["rows"] if r.get("site") is not None]
    assert {r["operator"] for r in rows} == set(KINETICS_OPERATORS)
    assert report["all_sites_passed"], [r for r in rows if not r["passed"]]
    for r in rows:
        assert r["harness_unchanged"] and not r["exec_overrides"] and r["single_change_enforced"] is True
        assert r["atomicity"].startswith("atomic") == (r["operator"] in ("shift_forward_rate_midpoint",
                                                                         "shift_channel_vshift"))
        assert r["affected_equations"] and (tmp_path / "out" / r["plot"]).is_file()
