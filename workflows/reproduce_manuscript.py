"""Workflow step: rebuild every table and figure of a campaign from raw and processed results.

Equivalent to ``nexclamp reproduce-paper``. Example: python workflows/reproduce_manuscript.py --help
"""

import sys

from nexclamp.cli import main

if __name__ == "__main__":
    sys.exit(main(["reproduce-paper", *sys.argv[1:]]))
