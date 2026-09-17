"""Workflow step: freeze the confirmatory study (write ``configs/FROZEN.lock`` and tag the commit).

Run once, after the pilot phase ends and before any held-out run. Refuses unless:
- ``data/splits/SPLITS.sha256`` exists (splits frozen with ``scripts/freeze_splits.py``) and the
  held-out model and family files are assigned;
- the frozen protocol selection JSON (computed on discovery data only) exists;
- the preregistration draft exists;
- ``configs/study.yaml`` says ``status: frozen``;
- provenance paths are clean;
- no lock exists yet (a lock is never overwritten).

The lock covers every ``configs/*.yaml``, the split hash file, the model manifest, the selection
JSON and the preregistration draft, in the ``sha256  path`` format read by ``HeldoutGate``.

    python workflows/freeze_study.py --selection results/processed/<discovery>/selection.json --tag study-freeze-v1
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

from neuraxis.provenance import REPO_ROOT, git_state, sha256_file, utc_now

LOCK = REPO_ROOT / "configs" / "FROZEN.lock"


def lock_entries(selection: Path, prereg: Path) -> list[str]:
    files = sorted(p for p in (REPO_ROOT / "configs").glob("*.yaml"))
    files += [REPO_ROOT / "data" / "splits" / "SPLITS.sha256", REPO_ROOT / "data" / "model_manifest.csv", selection, prereg]
    return [f"{sha256_file(p)}  {p.resolve().relative_to(REPO_ROOT).as_posix()}" for p in files]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selection", required=True, type=Path)
    ap.add_argument("--prereg", default=Path("docs/CONFIRMATORY_PREREGISTRATION_DRAFT.md"), type=Path)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args(argv)
    selection = a.selection if a.selection.is_absolute() else REPO_ROOT / a.selection
    prereg = a.prereg if a.prereg.is_absolute() else REPO_ROOT / a.prereg
    problems = []
    if LOCK.exists():
        problems.append(f"{LOCK} already exists; locks are never overwritten")
    splits = REPO_ROOT / "data" / "splits"
    for f in ("SPLITS.sha256", "heldout/heldout_models.txt", "heldout/heldout_families.txt"):
        if not (splits / f).is_file():
            problems.append(f"missing data/splits/{f}")
    for p in (selection, prereg):
        if not p.is_file():
            problems.append(f"missing {p}")
    study = yaml.safe_load((REPO_ROOT / "configs" / "study.yaml").read_text(encoding="utf-8"))
    if study.get("status") != "frozen":
        problems.append("configs/study.yaml status is not 'frozen'")
    commit, dirty = git_state()
    if dirty:
        problems.append("provenance paths have uncommitted changes")
    if problems:
        print("refused:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 2
    header = f"# Neuraxis frozen study lock, written {utc_now()} at commit {commit}\n"
    LOCK.write_text(header + "\n".join(lock_entries(selection, prereg)) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {LOCK}. Commit it, then run: git tag -a {a.tag} -m 'Frozen confirmatory study'")
    subprocess.run(["git", "status", "--short", "configs/FROZEN.lock"], cwd=REPO_ROOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
