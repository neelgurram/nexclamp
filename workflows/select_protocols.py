"""Workflow step: greedy protocol selection on the discovery split. Equivalent to ``neurosem select-protocols``."""

import sys

from nexclamp.cli import main

if __name__ == "__main__":
    sys.exit(main(["select-protocols", *sys.argv[1:]]))
