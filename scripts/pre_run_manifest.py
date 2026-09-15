"""Pre-run SHA-256 manifest for a pilot protocol (Neuraxis development pilot).

Covers the protocol document, every file in the protocol's config directory, the model
manifest, the stored source-model snapshots of the protocol's models, the environment lock
files, and the analysis code (every Git-tracked file under ``src/``, ``scripts/`` and ``tests/``,
plus one aggregate tree hash). The Git commit that contains this manifest is recorded
separately in the push record, because a file cannot contain the hash of its own commit.

    python scripts/pre_run_manifest.py --protocol docs/PILOT_PROTOCOL_V1.md \
        --config-dir configs/pilot_protocol_v1 --out manifests/pilot_pre_run_sha256.txt
    python scripts/pre_run_manifest.py ... --verify      # recompute and compare; exit 1 on any mismatch
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

from neurosem.provenance import REPO_ROOT, sha256_bytes, sha256_file  # noqa: E402

ENVIRONMENT_FILES = ("requirements.lock", "environment.yml", "pyproject.toml", ".tools/jdk_provenance.json", "Dockerfile")


def _rel(p: Path) -> str:
    return p.resolve().relative_to(REPO_ROOT).as_posix()


def entries(protocol: Path, config_dir: Path) -> list[tuple[str, str, str]]:
    """(category, sha256, path) rows."""
    out = [("protocol", sha256_file(protocol), _rel(protocol))]
    out += [("config", sha256_file(p), _rel(p)) for p in sorted(config_dir.glob("*")) if p.is_file()]
    manifest = REPO_ROOT / "data" / "model_manifest.csv"
    out.append(("model_manifest", sha256_file(manifest), _rel(manifest)))
    study = yaml.safe_load((config_dir / "study.yaml").read_text(encoding="utf-8"))
    wanted = set(study["pilot"]["models"])
    snapshots = sorted({r["snapshot"] for r in csv.DictReader(open(manifest, encoding="utf-8")) if r["model_id"] in wanted})
    for snap in snapshots:
        root = REPO_ROOT / "models" / "raw" / snap
        out += [("model_snapshot", sha256_file(p), _rel(p)) for p in sorted(root.rglob("*")) if p.is_file()]
    out += [("environment", sha256_file(REPO_ROOT / f), f) for f in ENVIRONMENT_FILES if (REPO_ROOT / f).is_file()]
    tracked = subprocess.run(["git", "ls-files", "src", "scripts", "tests"], cwd=REPO_ROOT, capture_output=True, text=True,
                             check=True).stdout.split()
    code = [("analysis_code", sha256_file(REPO_ROOT / f), f) for f in sorted(tracked)
            if (REPO_ROOT / f).is_file() and "__pycache__" not in f]
    out += code
    tree = sha256_bytes("".join(f"{h}  {p}\n" for _, h, p in code).encode())
    out.append(("analysis_code_tree", tree, "ANALYSIS_CODE_TREE(src,scripts,tests)"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--protocol", required=True, type=Path)
    ap.add_argument("--config-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args(argv)
    rows = entries(REPO_ROOT / a.protocol, REPO_ROOT / a.config_dir)
    body = "".join(f"{h}  {p}  [{cat}]\n" for cat, h, p in rows)
    out = REPO_ROOT / a.out
    if a.verify:
        recorded = [line for line in out.read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")]
        current = body.splitlines()
        if recorded != current:
            diff = sorted(set(recorded) ^ set(current))
            print(f"MISMATCH ({len(diff)} lines differ):", *diff[:20], sep="\n  ")
            return 1
        print(f"verified {len(current)} entries")
        return 0
    header = ("# Neuraxis development pilot: pre-run SHA-256 manifest\n"
              f"# protocol: {a.protocol.as_posix()}; config dir: {a.config_dir.as_posix()}\n"
              "# format: sha256  path  [category]; the commit containing this file is recorded in "
              "manifests/pilot_pre_run_push_record.json\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + body, encoding="utf-8", newline="\n")
    print(f"wrote {len(rows)} entries to {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
