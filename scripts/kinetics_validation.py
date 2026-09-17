"""Run the kinetics-operator validation on development fixtures (writes under results/audits/kinetics_validation/).

    python scripts/kinetics_validation.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis.orchestration.kinetics_validation import default_fixtures, validate_fixtures  # noqa: E402
from neuraxis.provenance import REPO_ROOT  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="neuraxis_kinfix_") as tmp:
        report = validate_fixtures(REPO_ROOT / "results" / "audits" / "kinetics_validation", default_fixtures(Path(tmp)))
    for r in report["rows"]:
        print(r["fixture"], r["operator"], r.get("site"), r.get("status", ""), r.get("atomicity", ""),
              r.get("simulation_status", ""), r.get("spikes_before_after", ""), r.get("passed", ""))
    print("ALL SITES PASSED" if report["all_sites_passed"] else "SOME SITES FAILED")
    return 0 if report["all_sites_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
