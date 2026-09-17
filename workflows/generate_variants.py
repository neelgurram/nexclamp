"""Workflow step: generate mutants and valid transformations (alias of generate_mutants.py).

Equivalent to ``neuraxis generate-mutants``. Example: python workflows/generate_variants.py --help
"""

import sys

from neuraxis.cli import main

if __name__ == "__main__":
    sys.exit(main(["generate-mutants", *sys.argv[1:]]))
