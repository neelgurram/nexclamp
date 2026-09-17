"""Verify a campaign archive: whole-file SHA-256, test extraction, and per-file checksums.

Checks, in order:
1. the tar's SHA-256 equals the value recorded in ``ARCHIVE.json``;
2. the tar extracts into an empty temporary directory (Python ``tarfile``, ``data`` filter:
   no absolute paths, links outside the tree or device files);
3. every extracted file matches ``ARCHIVE_MANIFEST.sha256``, and nothing is missing or extra;
4. the manifest inside the tar is byte-identical to the committed manifest.

Writes a JSON verification record. Used both for verification and as the restore procedure
(``docs`` in ``results/processed/<campaign>/ARCHIVE_README.md``).

Example::

    python scripts/verify_archive.py --campaign pilot --tar archive/pilot/pilot_raw_and_workspaces.tar \
        --extract-to <empty temp dir> --record results/processed/pilot/ARCHIVE_VERIFICATION_local.json
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis import config  # noqa: E402
from neuraxis.experiments import registry as reg  # noqa: E402
from neuraxis.provenance import sha256_file, utc_now  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--tar", required=True, type=Path)
    ap.add_argument("--extract-to", required=True, type=Path, help="empty or absent directory")
    ap.add_argument("--record", required=True, type=Path, help="JSON verification record to write")
    ap.add_argument("--location", default="", help="free-text description of where this copy is stored")
    ap.add_argument("--keep", action="store_true", help="keep the extracted files (restore mode)")
    a = ap.parse_args(argv)

    processed = config.results_dir() / "processed" / a.campaign
    archive = json.loads((processed / "ARCHIVE.json").read_text(encoding="utf-8"))
    manifest = processed / reg.ARCHIVE_MANIFEST
    record: dict = {"campaign": a.campaign, "verified_utc": utc_now(), "tar_path": str(a.tar),
                    "location": a.location, "python": platform.python_version(),
                    "tarfile_module": "Python standard library tarfile", "platform": platform.platform()}

    record["tar_size_bytes"] = a.tar.stat().st_size
    record["tar_sha256"] = sha256_file(a.tar)
    record["tar_sha256_matches_record"] = record["tar_sha256"] == archive["tar"]["sha256"]
    record["tar_size_matches_record"] = record["tar_size_bytes"] == archive["tar"]["size_bytes"]

    if a.extract_to.exists() and any(a.extract_to.iterdir()):
        print(f"{a.extract_to} is not empty", file=sys.stderr)
        return 2
    a.extract_to.mkdir(parents=True, exist_ok=True)
    with tarfile.open(a.tar, "r:") as tf:
        members = tf.getmembers()
        record["tar_member_files"] = sum(1 for m in members if m.isfile())
        record["tar_format_detected"] = {tarfile.USTAR_FORMAT: "ustar", tarfile.GNU_FORMAT: "gnu",
                                         tarfile.PAX_FORMAT: "pax"}.get(tf.format, str(tf.format))
        tf.extractall(a.extract_to, filter="data")

    labels = sorted({line.split("  ", 1)[1].split("/", 1)[0]
                     for line in manifest.read_text(encoding="utf-8").splitlines()})
    roots = {label: a.extract_to / label for label in labels}
    expected = {line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines()}
    extracted = {f"{label}/{p.relative_to(root).as_posix()}" for label, root in roots.items()
                 for p in root.rglob("*") if p.is_file()}
    problems = reg.verify_manifest(manifest, roots)
    record["manifest_entries"] = len(expected)
    record["extracted_files_excluding_manifest"] = len(extracted)
    record["files_missing_or_mismatched"] = problems
    record["unexpected_extra_files"] = sorted(extracted - expected)
    inner = a.extract_to / reg.ARCHIVE_MANIFEST
    record["inner_manifest_identical"] = inner.is_file() and sha256_file(inner) == sha256_file(manifest)
    record["verified"] = bool(record["tar_sha256_matches_record"] and record["tar_size_matches_record"]
                              and not problems and not record["unexpected_extra_files"]
                              and record["inner_manifest_identical"] and len(extracted) == len(expected))
    if not a.keep:
        shutil.rmtree(a.extract_to)
        record["extraction_removed_after_check"] = True

    a.record.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: record[k] for k in ("verified", "tar_sha256", "manifest_entries",
                                             "extracted_files_excluding_manifest")}, indent=2))
    return 0 if record["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
