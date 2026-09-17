"""Workflow step: tolerance calibration from reference refinement. Equivalent to ``neurosem calibrate-tolerances``."""

import sys

from neuraxis.cli import main

if __name__ == "__main__":
    sys.exit(main(["calibrate-tolerances", *sys.argv[1:]]))
