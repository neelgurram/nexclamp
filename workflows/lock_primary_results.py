"""Workflow step: lock the primary confirmatory results immediately after the held-out run.

Writes ``results/locks/<campaign>_PRIMARY_RESULTS.lock`` (write-once) with the SHA-256 of
``heldout_evaluation.json`` and every file in ``results/processed/<campaign>/``, plus the Git
commit. Any later analysis is exploratory unless it was preregistered; a changed primary file is
detectable with ``--verify``.

    python workflows/lock_primary_results.py --campaign heldout-v1
    python workflows/lock_primary_results.py --campaign heldout-v1 --verify
"""

from __future__ import annotations

import argparse
import sys

from nexclamp import config
from nexclamp.experiments import registry
from nexclamp.provenance import REPO_ROOT, git_state, utc_now


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args(argv)
    results = config.results_dir()
    processed = results / "processed" / a.campaign
    lock = REPO_ROOT / "results" / "locks" / f"{a.campaign}_PRIMARY_RESULTS.lock"
    roots = {"processed": processed}
    if a.verify:
        problems = registry.verify_manifest(lock, roots)
        print("intact" if not problems else f"CHANGED: {problems[:20]}")
        return 0 if not problems else 1
    if registry.role_of(a.campaign, results) != registry.CONFIRMATORY_HELDOUT:
        print(f"refused: {a.campaign} is not a confirmatory held-out campaign", file=sys.stderr)
        return 2
    if not (processed / "heldout_evaluation.json").is_file():
        print("refused: heldout_evaluation.json not found", file=sys.stderr)
        return 2
    if lock.exists():
        print(f"refused: {lock} exists (locks are write-once)", file=sys.stderr)
        return 2
    entries = registry.build_manifest(roots)
    lock.parent.mkdir(parents=True, exist_ok=True)
    registry.write_manifest(lock, entries)
    commit, dirty = git_state()
    (lock.with_suffix(".json")).write_text(
        f'{{"campaign": "{a.campaign}", "locked_utc": "{utc_now()}", "git_commit": "{commit}", '
        f'"git_dirty": {str(dirty).lower()}, "n_files": {len(entries)}}}\n', encoding="utf-8")
    print(f"locked {len(entries)} files -> {lock}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
