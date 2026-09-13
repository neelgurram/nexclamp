"""Workflow step: reference fingerprints at h, h/2, h/4 with determinism check.

Equivalent to ``neurosem run-reference``. Example: python workflows/run_reference.py --campaign pilot
"""

import sys

from neurosem.cli import main

if __name__ == "__main__":
    sys.exit(main(["run-reference", *sys.argv[1:]]))
