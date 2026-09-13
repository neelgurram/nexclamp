"""Build docs/novelty_matrix.csv from the verified prior-art evidence (Milestone 0).

Rows come only from deep-read evidence files (docs/m0_evidence/prior_art/deepread_*.json), in which each
candidate's existence and metadata were checked against a primary source. Candidates that were found by
search but never deep-read are NOT matrix rows; they are listed in
docs/m0_evidence/prior_art/screened_not_deep_read.json and counted in the summary, so nothing is dropped
silently.

Columns follow the specification ("Required novelty sweep"): citation, year, model type, mutations,
multiple stimuli, electrophysiology features, protocol optimization, held-out evaluation, AI
transformations, software availability, distinction from NeuroSem, plus provenance columns.

Usage: python scripts/build_novelty_matrix.py
"""

from __future__ import annotations

import csv
import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs" / "m0_evidence" / "prior_art"
OUT = REPO / "docs" / "novelty_matrix.csv"
SUMMARY = EVIDENCE / "novelty_matrix_summary.json"

COLUMNS = [
    ("citation", "citation"), ("year", "year"), ("model_type", "model_type"),
    ("controlled_mutations", "mutations"), ("multiple_stimuli", "multiple_stimuli"),
    ("electrophysiology_features", "electrophysiology_features"), ("protocol_optimization", "protocol_optimization"),
    ("heldout_evaluation", "heldout_evaluation"), ("ai_transformations", "ai_transformations"),
    ("software", "software_availability"), ("distinction_from_neurosem", "distinction_from_neurosem"),
    ("closeness", "closeness_1to5"), ("kind", "kind"), ("doi", "doi"), ("url", "url"),
    ("verification_method", "verification_method"), ("found_via", "found_via"),
]


def _doi(r: dict) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (r.get("doi") or "").strip().lower())


def _title_key(r: dict) -> str:
    cit = r.get("citation") or ""
    title = cit.split(").", 1)[-1] if ")." in cit else cit
    return re.sub(r"[^a-z0-9]", "", title.lower())[:70]


def main() -> int:
    files = sorted(glob.glob(str(EVIDENCE / "deepread_*.json")))
    rows, rejected, dup = [], [], 0
    seen_doi, seen_title = set(), set()
    for f in files:
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        rejected += data.get("rejected", [])
        for r in data.get("rows", []):
            d, t = _doi(r), _title_key(r)
            if (d and d in seen_doi) or (t and t in seen_title):
                dup += 1
                continue
            if d:
                seen_doi.add(d)
            if t:
                seen_title.add(t)
            r = dict(r, source_file=Path(f).name)
            rows.append(r)
    rows.sort(key=lambda r: (-int(r.get("closeness") or 0), str(r.get("year") or ""), r.get("citation") or ""))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow([name for _, name in COLUMNS] + ["evidence_file"])
        for r in rows:
            w.writerow([r.get(k, "") for k, _ in COLUMNS] + [r["source_file"]])

    screened_path = EVIDENCE / "screened_not_deep_read.json"
    unread_src = REPO / "work" / "tmp" / "prior_art" / "unread_c2_not_deep_read.json"
    if unread_src.is_file() and not screened_path.is_file():
        screened_path.write_text(unread_src.read_text(encoding="utf-8"), encoding="utf-8")
    screened = json.loads(screened_path.read_text(encoding="utf-8")) if screened_path.is_file() else []

    summary = {
        "deep_read_files": len(files), "matrix_rows": len(rows), "duplicates_removed": dup,
        "rejected_at_verification": len(rejected), "closeness_distribution": dict(sorted(Counter(
            int(r.get("closeness") or 0) for r in rows).items())),
        "screened_not_deep_read": len(screened),
        "note": "Matrix rows are verified works only. Screened-but-unread candidates are listed separately; "
                "absence from the matrix is not evidence that a work is irrelevant or that no such work exists.",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
