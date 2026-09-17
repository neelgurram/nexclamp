"""Freeze the discovery / held-out split files by writing ``data/splits/SPLITS.sha256``.

The split is validated first (all four split files present, known families, disjoint
discovery and held-out lists, model ids in ``data/model_manifest.csv``). An existing
freeze that differs from the current files is never overwritten unless
``--force-with-reason`` is given; the freeze and every forced re-freeze are appended to
``results/heldout_access.log``.

Usage:  python scripts/freeze_splits.py [--root DIR] [--force-with-reason "why the split changed"]
Exit codes: 0 frozen or unchanged, 1 invalid split definition, 2 refused (frozen split differs).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from neuraxis.provenance import REPO_ROOT
from neuraxis.selection.splits import ACCESS_LOG_FILE, FrozenSplitError, LeakageError, freeze_splits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=REPO_ROOT, help="repository root (default: this checkout)")
    ap.add_argument("--force-with-reason", dest="force_reason", metavar="REASON", default=None,
                    help="overwrite an existing, different freeze; the reason is logged")
    args = ap.parse_args(argv)
    if args.force_reason is not None and not args.force_reason.strip():
        print("REFUSED: --force-with-reason needs a non-empty reason", file=sys.stderr)
        return 2
    try:
        result = freeze_splits(args.root, force_reason=args.force_reason)
    except FrozenSplitError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError, LeakageError) as exc:
        print(f"INVALID SPLIT: {exc}", file=sys.stderr)
        return 1
    print(f"{result.status}: {result.manifest}")
    for rel, digest in sorted(result.entries.items()):
        print(f"  {digest}  {rel}")
    for w in result.warnings:
        print(f"WARNING: {w}")
    if result.log_record is not None:
        print(f"logged '{result.log_record['event']}' to {Path(args.root) / ACCESS_LOG_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
