"""Workflow step: run a fixed development (pilot) matrix as an exploratory campaign; use NEURAXIS_CONFIG_DIR for a protocol's config directory.

Equivalent to ``neuraxis pilot``. Example: python workflows/run_development.py --help
"""

import sys

from neuraxis.cli import main

if __name__ == "__main__":
    sys.exit(main(["pilot", *sys.argv[1:]]))
