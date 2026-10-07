"""Check that every path written in the documentation exists.

Two kinds of reference are checked in each tracked Markdown file, and they are not the same kind
of statement. A Markdown link is a claim that the reader can follow it, so a broken one fails this
check. A path in backticks is a mention, and a mention is often deliberately of something this
repository does not contain: a file name quoted from the execution plan that was never created, or
a path inside somebody else's project cited by the name-conflict audit. Stale mentions are listed
as warnings for a human to judge.

- Markdown links, ``[text](path)``, excluding external URLs and pure anchors;
- paths written in backticks whose first segment is a real top-level directory of the repository,
  which is how these documents cite a file. A bare filename in backticks (``run.json``) or a
  shorthand inside a package (``validation/execution.py``) is prose, not a path, and is left alone.

A path is resolved relative to the file that writes it and then, if that fails, relative to the
repository root, because both styles are used. Directories count as resolved, and a trailing
anchor or a ``*`` glob is stripped first.

Hash-locked files are checked but reported separately: their contents cannot be edited to follow a
later reorganisation, so a stale path inside one is a known consequence of freezing, not a defect.

    python scripts/check_doc_links.py

Exit status is 1 if an editable document points at something that does not exist.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", ".tools", "work", "node_modules", "__pycache__", "results", "models"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TICKED = re.compile(r"`([^`\n]+)`")
# A backticked string counts as a path only when it starts at a real top-level directory, so that
# prose shorthand is not mistaken for a link.
TOP_LEVEL = {p.name for p in REPO_ROOT.iterdir() if p.is_dir() and p.name not in SKIP_DIRS}
PATH_LIKE = re.compile(r"^(?:" + "|".join(sorted(TOP_LEVEL)) + r")/[\w./\-]+$")


def locked_files() -> set[str]:
    lock = REPO_ROOT / "configs/FROZEN.lock"
    if not lock.is_file():
        return set()
    return {line.split(None, 1)[1].strip() for line in lock.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")}


def candidates(text: str) -> set[str]:
    out = {m.group(1) for m in LINK.finditer(text)}
    out |= {m.group(1) for m in TICKED.finditer(text) if PATH_LIKE.match(m.group(1))}
    return out


def resolves(ref: str, doc: Path) -> bool:
    ref = ref.split("#", 1)[0].split("?", 1)[0].strip()
    if not ref or ref.startswith(("http://", "https://", "mailto:", "doi:")):
        return True
    if "*" in ref:                                   # a glob: the directory above it must exist
        ref = ref.rsplit("/", 1)[0] if "/" in ref else "."
    for base in (doc.parent, REPO_ROOT):
        if (base / ref).exists():
            return True
    return False


def main() -> int:
    locked = locked_files()
    broken: list[tuple[str, str]] = []
    mentions: list[tuple[str, str]] = []
    frozen_stale: list[tuple[str, str]] = []
    n_docs = n_refs = 0
    for doc in sorted(REPO_ROOT.rglob("*.md")):
        if set(doc.relative_to(REPO_ROOT).parts) & SKIP_DIRS:
            continue
        rel = doc.relative_to(REPO_ROOT).as_posix()
        n_docs += 1
        text = doc.read_text(encoding="utf-8", errors="replace")
        linked = {m.group(1) for m in LINK.finditer(text)}
        for ref in sorted(candidates(text)):
            n_refs += 1
            if resolves(ref, doc):
                continue
            if rel in locked:
                frozen_stale.append((rel, ref))
            elif ref in linked:
                broken.append((rel, ref))
            else:
                mentions.append((rel, ref))

    print(f"{n_docs} documents, {n_refs} written paths")
    if frozen_stale:
        print(f"\n{len(frozen_stale)} stale path(s) inside hash-locked documents (expected; these files "
              "cannot be edited):")
        for rel, ref in frozen_stale:
            print(f"  {rel}: {ref}")
    if mentions:
        print(f"\n{len(mentions)} path(s) mentioned in backticks that do not exist. Some are meant to be "
              "absent (names quoted from the execution plan, paths in other projects); check new ones:")
        for rel, ref in mentions:
            print(f"  {rel}: {ref}")
    if broken:
        print(f"\n{len(broken)} broken link(s):")
        for rel, ref in broken:
            print(f"  {rel}: {ref}")
        return 1
    print("\nevery link in an editable document resolves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
