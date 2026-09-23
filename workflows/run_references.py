"""Workflow step: reference fingerprints at h, h/2, h/4 with determinism check (plural alias of run_reference.py).

Equivalent to ``nexclamp run-reference``. Example: python workflows/run_references.py --help
"""

import sys

from nexclamp.cli import main

if __name__ == "__main__":
    sys.exit(main(["run-reference", *sys.argv[1:]]))
