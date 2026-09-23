"""Workflow step: GATED held-out evaluation. Equivalent to ``neurosem evaluate-heldout``.

Refuses to run unless configs/FROZEN.lock matches the preregistered files; every access is logged.
"""

import sys

from nexclamp.cli import main

if __name__ == "__main__":
    sys.exit(main(["evaluate-heldout", *sys.argv[1:]]))
