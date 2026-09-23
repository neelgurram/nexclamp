"""Workflow step: the frozen held-out evaluation. GATED.

Refuses to run unless every one of these holds:
- the exact authorisation sentence from Neel is supplied (DECISIONS D-036);
- the AsPredicted verification URL and the downloaded, time-stamped preregistration PDF are given
  (the PDF's SHA-256 is written to the access record);
- ``configs/FROZEN.lock`` exists and verifies (checked again inside ``evaluate-heldout``);
- the working tree is clean for provenance paths.

Example (only after preregistration)::

    python workflows/run_heldout.py --campaign heldout-v1 --selection results/processed/<discovery>/selection.json \
        --reason "frozen confirmatory evaluation" --aspredicted-url https://aspredicted.org/... \
        --aspredicted-pdf docs/preregistration/aspredicted.pdf --authorization "<exact sentence>"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nexclamp.cli import main as cli_main
from nexclamp.provenance import REPO_ROOT, git_state, sha256_file, utc_now

AUTHORIZATION = ("THE ASPREDICTED PREREGISTRATION HAS BEEN SUBMITTED AND VERIFIED. "
                 "BEGIN THE FROZEN HELD-OUT EVALUATION.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--selection", required=True)
    ap.add_argument("--reason", required=True)
    ap.add_argument("--aspredicted-url", required=True)
    ap.add_argument("--aspredicted-pdf", required=True, type=Path)
    ap.add_argument("--authorization", required=True)
    ap.add_argument("--workers", type=int)
    a = ap.parse_args(argv)
    if a.authorization.strip() != AUTHORIZATION:
        print("refused: the authorisation sentence does not match exactly (DECISIONS D-036)", file=sys.stderr)
        return 2
    if not a.aspredicted_url.startswith("https://aspredicted.org/"):
        print("refused: an AsPredicted verification URL (https://aspredicted.org/...) is required", file=sys.stderr)
        return 2
    pdf = a.aspredicted_pdf if a.aspredicted_pdf.is_absolute() else REPO_ROOT / a.aspredicted_pdf
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        print(f"refused: preregistration PDF not found: {pdf}", file=sys.stderr)
        return 2
    commit, dirty = git_state()
    if dirty:
        print("refused: provenance paths have uncommitted changes", file=sys.stderr)
        return 2
    record = {"campaign": a.campaign, "utc": utc_now(), "git_commit": commit, "aspredicted_url": a.aspredicted_url,
              "aspredicted_pdf": str(pdf), "aspredicted_pdf_sha256": sha256_file(pdf), "authorization": AUTHORIZATION}
    log = REPO_ROOT / "results" / "heldout_authorizations.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    args = ["evaluate-heldout", "--campaign", a.campaign, "--selection", a.selection, "--reason", a.reason]
    if a.workers:
        args += ["--workers", str(a.workers)]
    return cli_main(args)


if __name__ == "__main__":
    sys.exit(main())
