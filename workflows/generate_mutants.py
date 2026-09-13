"""Workflow step: generate mutants and valid transformations. Equivalent to ``neurosem generate-mutants``."""

import sys

from neurosem.cli import main

if __name__ == "__main__":
    sys.exit(main(["generate-mutants", *sys.argv[1:]]))
