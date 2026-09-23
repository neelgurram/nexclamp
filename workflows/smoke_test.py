"""Workflow step: infrastructure smoke test (load, validate, simulate, save traces, extract features, plot, reproduce, provenance, tests).

Equivalent to ``nexclamp smoke-test``. Example: python workflows/smoke_test.py --help
"""

import sys

from nexclamp.cli import main

if __name__ == "__main__":
    sys.exit(main(["smoke-test", *sys.argv[1:]]))
