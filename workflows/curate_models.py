"""Workflow step: apply the model inclusion and exclusion criteria to candidate models (reference simulations only).

Equivalent to ``neuraxis curate-models``. Example: python workflows/curate_models.py --help
"""

import sys

from neuraxis.cli import main

if __name__ == "__main__":
    sys.exit(main(["curate-models", *sys.argv[1:]]))
