"""Run the kinetics-operator validation (writes under results/audits/kinetics_validation/).

Without arguments it validates the development fixtures (the synthetic HH-type fixture and
Pospischil RS). ``--models`` adds named models from the manifest, which is how the per-model
applicability report for a pilot is produced:

    python scripts/kinetics_validation.py --models acnet2_pyr_soma migliore2014_mt_soma \\
        nml2_hh_example osb_hh2_477127614 pospischil2008_fs --max-sites 6 \\
        --out results/audits/kinetics_pilot2

A model to which a gate-level operator does not apply (custom LEMS rate types have no core midpoint
or slope parameter) is reported as ``no_site`` with the recorded reason. That is a property of the
model's encoding, not a model failure.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp.models import load_models, materialize  # noqa: E402
from nexclamp.orchestration.kinetics_validation import default_fixtures, validate_fixtures  # noqa: E402
from nexclamp.provenance import REPO_ROOT  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--models", nargs="*", default=[], help="model ids to validate in addition to the fixtures")
    ap.add_argument("--only-models", action="store_true", help="validate only --models, not the default fixtures")
    ap.add_argument("--max-sites", type=int, default=16, help="sites per operator and model")
    ap.add_argument("--out", default="results/audits/kinetics_validation")
    a = ap.parse_args(argv)
    out = Path(a.out)
    if not out.is_absolute():
        out = REPO_ROOT / out
    with tempfile.TemporaryDirectory(prefix="neuraxis_kinfix_") as tmp:
        fixtures = [] if a.only_models else default_fixtures(Path(tmp))
        if a.models:
            known = load_models()
            fixtures += [(mid, materialize(known[mid], Path(tmp) / mid)) for mid in a.models]
        report = validate_fixtures(out, fixtures, max_sites=int(a.max_sites))
    for r in report["rows"]:
        print(r["fixture"], r["operator"], r.get("site"), r.get("status", ""), r.get("atomicity", ""),
              r.get("simulation_status", ""), r.get("spikes_before_after", ""), r.get("passed", ""))
    print("ALL SITES PASSED" if report["all_sites_passed"] else "SOME SITES FAILED")
    return 0 if report["all_sites_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
