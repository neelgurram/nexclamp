"""Compressed pre-run archival package (protocol, configs, manifests, environment, Git metadata).

Contains no model files, credentials, secrets or API keys. It is write-once. Its SHA-256,
size and member list go to ``manifests/pilot_pre_run_package.json`` (tracked in Git).

    python scripts/pre_run_package.py --protocol docs/PILOT_PROTOCOL_V1.md --config-dir configs/pilot_protocol_v1 \
        --out archive/pilot-v2/pre_run/neuraxis_pilot_protocol_v1_pre_run.tar.gz
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp.provenance import REPO_ROOT, python_environment, sha256_file, utc_now  # noqa: E402

SECRET = re.compile(r"(gho_|ghp_|github_pat_|sk-ant-|AKIA[0-9A-Z]{16}|PRIVATE KEY|password\s*[:=])", re.IGNORECASE)


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--protocol", required=True, type=Path)
    ap.add_argument("--config-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--record", default=Path("manifests/pilot_pre_run_package.json"), type=Path)
    a = ap.parse_args(argv)
    from nexclamp.simulators.jneuroml import JNeuroML

    out = REPO_ROOT / a.out
    if out.exists():
        print(f"{out} exists; packages are write-once", file=sys.stderr)
        return 2
    files = [a.protocol, *sorted(p.relative_to(REPO_ROOT) for p in (REPO_ROOT / a.config_dir).glob("*") if p.is_file()),
             *sorted(p.relative_to(REPO_ROOT) for p in (REPO_ROOT / "manifests").glob("pilot_pre_run_*") if p.is_file()
                     and p.name != a.record.name),
             Path("docs/pilot/pilot_v2_design.md"), Path("data/model_manifest.csv"), Path("requirements.lock"),
             Path("environment.yml"), Path("pyproject.toml"), Path(".tools/jdk_provenance.json")]
    files = [f for f in files if (REPO_ROOT / f).is_file()]
    for f in files:
        if SECRET.search((REPO_ROOT / f).read_text(encoding="utf-8", errors="replace")):
            print(f"possible secret in {f}; refusing to package", file=sys.stderr)
            return 2
    generated = {
        "environment_info.json": {"created_utc": utc_now(), "python_environment": python_environment(),
                                  "simulator": JNeuroML().version_info()},
        "git_metadata.json": {"head": _git("rev-parse", "HEAD").strip(), "branch": _git("rev-parse", "--abbrev-ref", "HEAD").strip(),
                              "remotes": _git("remote", "-v").splitlines(), "status_porcelain": _git("status", "--porcelain").splitlines(),
                              "log": _git("log", "-15", "--format=%H %cI %s").splitlines(), "tags": _git("tag", "-n1").splitlines()},
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    partial = out.with_name(out.name + ".partial")
    with tarfile.open(partial, "w:gz") as tf:
        for f in files:
            tf.add(REPO_ROOT / f, arcname=f"package/{Path(f).as_posix()}")
        for name, obj in generated.items():
            data = (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()
            info = tarfile.TarInfo(f"package/{name}")
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    partial.replace(out)
    record = {"created_utc": utc_now(), "path": a.out.as_posix(), "sha256": sha256_file(out), "size_bytes": out.stat().st_size,
              "format": "tar + gzip (Python tarfile, PAX)", "members": [Path(f).as_posix() for f in files] + list(generated),
              "git_head": generated["git_metadata.json"]["head"], "excludes": "model files, credentials, secrets, API keys",
              "storage": "local, Git-ignored (archive/); this record is in Git"}
    (REPO_ROOT / a.record).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: record[k] for k in ("path", "sha256", "size_bytes")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
