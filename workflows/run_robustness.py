"""Workflow step: robustness analyses for a finished campaign (no new simulation).

- tolerance sensitivity (every tolerance multiplied by ``configs/tolerances.yaml``
  ``sensitivity_multipliers``), written by ``neuraxis analyze``;
- numerical robustness: deviation of numerical stress tests against the reference's h, h/2 and h/4
  error (``scripts/numerical_robustness_report.py``).

Robustness analyses of the held-out campaign are reported as prespecified only if the
preregistration lists them.

    python workflows/run_robustness.py --campaign pilot-v2
"""

from __future__ import annotations

import argparse
import runpy
import sys

from neuraxis.cli import main as cli_main
from neuraxis.provenance import REPO_ROOT


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    rc = cli_main(["analyze", "--campaign", a.campaign])
    sys.argv = ["numerical_robustness_report.py", "--campaign", a.campaign]
    try:
        runpy.run_path(str(REPO_ROOT / "scripts" / "numerical_robustness_report.py"), run_name="__main__")
    except SystemExit as exc:
        rc = rc or int(exc.code or 0)
    return rc


if __name__ == "__main__":
    sys.exit(main())
