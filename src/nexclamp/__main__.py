"""``python -m nexclamp`` runs the command-line interface (same entry point as the console script)."""

from __future__ import annotations

from nexclamp.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
