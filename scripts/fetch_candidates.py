"""Fetch commit-pinned snapshots of candidate models listed in a candidate CSV (model curation).

For every eligible row: the cell file, the shipped LEMS simulation and their NeuroML/LEMS include
closure are downloaded from ``raw.githubusercontent.com`` at the pinned commit into
``models/candidates/<snapshot>/``. Every file is verified against the git blob SHA-1 in the commit's
tree, so it provably belongs to that commit. The repository's licence file at that commit is stored,
and ``PROVENANCE.json`` records the source, commit, licence and SHA-256 of every file.

Rows are skipped (and reported) when the licence is missing or unclear, when a model is out of the
study's scope, or when an include points outside the repository. Existing files are never overwritten
with different content.

    python scripts/fetch_candidates.py --csv data/model_candidates_sweep2.csv --skip boyle2008_muscle
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import posixpath
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp.provenance import REPO_ROOT, sha256_bytes, utc_now  # noqa: E402

DEST = REPO_ROOT / "models" / "candidates"
BUILTIN = ("NeuroML2CoreTypes/", "Cells.xml", "Networks.xml", "Simulation.xml", "Inputs.xml", "Channels.xml",
           "Synapses.xml", "PyNN.xml", "NeuroMLCoreDimensions.xml", "NeuroMLCoreCompTypes.xml")
LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENSE.lesser", "COPYING", "COPYING.LESSER")


def gh_json(path: str):
    proc = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"gh api {path}: {proc.stderr.strip()[:300]}")
    return json.loads(proc.stdout)


def http_get(url: str, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "nexclamp-model-curation/0.2"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 502, 503, 504) and attempt < retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise RuntimeError("unreachable")


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def includes(data: bytes) -> list[str]:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_comments=True, huge_tree=True)
    root = etree.fromstring(data, parser=parser)
    out = []
    for el in root.iter():
        if isinstance(el.tag, str) and etree.QName(el).localname in ("include", "Include"):
            for attr in ("href", "file"):
                ref = el.get(attr)
                if ref and not ref.startswith(("http://", "https://")):
                    out.append(ref)
    return out


def eligible(row: dict, skip: set[str]) -> str:
    lic = (row.get("license") or "").lower()
    if row["model_id"] in skip:
        return "skipped by request (out of scope)"
    if not lic or lic.startswith("unclear") or "no license" in lic:
        return "licence missing or unclear: not downloaded"
    return ""


def fetch_row(row: dict, trees: dict, dest_root: Path) -> dict:
    repo = row["source_url"].rstrip("/").split("github.com/")[1]
    sha = row["commit"].strip()
    snapshot = row.get("snapshot") or f"{repo.split('/')[1]}@{sha[:8]}"
    if (repo, sha) not in trees:
        tree = gh_json(f"repos/{repo}/git/trees/{sha}?recursive=1")
        if tree.get("truncated"):
            raise RuntimeError(f"{repo}@{sha}: tree listing truncated")
        trees[(repo, sha)] = {e["path"]: e["sha"] for e in tree["tree"] if e["type"] == "blob"}
    blobs = trees[(repo, sha)]
    out_dir = dest_root / snapshot
    todo = [row["cell_file"], row["harness_lems"]] + [n for n in LICENSE_NAMES if n in blobs]
    done: dict[str, str] = {}
    errors = []
    while todo:
        rel = posixpath.normpath(todo.pop(0))
        if rel in done:
            continue
        if rel.startswith("..") or rel not in blobs:
            errors.append(f"{rel}: outside the repository or not in the commit tree")
            continue
        data = http_get(f"https://raw.githubusercontent.com/{repo}/{sha}/{rel}")
        if blob_sha1(data) != blobs[rel]:
            raise RuntimeError(f"{rel}: content does not match the commit's git blob")
        target = out_dir / rel
        if target.is_file() and target.read_bytes() != data:
            raise RuntimeError(f"{target} exists with different content")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        done[rel] = sha256_bytes(data)
        if rel.endswith((".nml", ".xml")):
            base = posixpath.dirname(rel)
            for inc in includes(data):
                if any(inc.endswith(b) or inc.startswith(b) for b in BUILTIN):
                    continue
                todo.append(posixpath.join(base, inc))
    prov_file = out_dir / "PROVENANCE.json"
    prov = json.loads(prov_file.read_text(encoding="utf-8")) if prov_file.is_file() else {
        "snapshot": snapshot, "repository": f"https://github.com/{repo}", "commit": sha, "models": {}, "files": {}}
    prov["files"].update(done)
    prov["models"][row["model_id"]] = {"license": row["license"], "license_url": row["license_url"],
                                       "citation": row["citation"], "doi": row.get("doi", ""),
                                       "fetched_utc": utc_now(), "errors": errors}
    prov["git_blob_sha1_verified"] = True
    prov_file.write_text(json.dumps(prov, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"model_id": row["model_id"], "snapshot": snapshot, "files": len(done), "errors": errors}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--skip", nargs="*", default=[])
    a = ap.parse_args(argv)
    trees: dict = {}
    report = []
    with open(REPO_ROOT / a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        why = eligible(row, set(a.skip))
        if why:
            report.append({"model_id": row["model_id"], "status": why})
            continue
        try:
            r = fetch_row(row, trees, DEST)
            report.append({**r, "status": "fetched" if not r["errors"] else "fetched with missing includes"})
        except Exception as exc:  # recorded per model; one bad source does not stop the others
            report.append({"model_id": row["model_id"], "status": f"failed: {exc}"[:300]})
    out = REPO_ROOT / "docs" / "m0_evidence" / "model_curation" / f"fetch_{Path(a.csv).stem}.json"
    out.write_text(json.dumps({"created_utc": utc_now(), "csv": a.csv.as_posix(), "report": report}, indent=2) + "\n",
                   encoding="utf-8")
    for r in report:
        print(r["model_id"], "|", r["status"], "|", r.get("files", ""), "|", "; ".join(r.get("errors", []))[:200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
