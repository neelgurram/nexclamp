"""Preserve and seal a finished campaign (DECISIONS D-027).

Steps:
1. copy the named run logs into ``results/processed/<campaign>/logs/`` (tracked in Git);
2. snapshot the config files, after checking they still match the hashes the campaign recorded;
3. write ``ARCHIVE_MANIFEST.sha256`` covering every file under ``results/raw/<campaign>``,
   ``work/variants/<campaign>`` and ``work/runs/<campaign>``, including the Git-ignored traces;
4. write a write-once tar of those files under ``archive/<campaign>/`` (Git-ignored; Neel chooses
   durable storage) and record its hash in ``ARCHIVE.json``;
5. register the campaign's role and seal it, so the pipeline never writes into it again.

Example::

    python scripts/archive_campaign.py --campaign pilot --role exploratory_pilot \
        --code-commit d323afa --code-tag pilot-v1-code --note "..." --log work/logs/pilot_run.log
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neurosem import config  # noqa: E402
from neurosem.experiments import registry as reg  # noqa: E402
from neurosem.provenance import REPO_ROOT, sha256_file, utc_now  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--role", required=True, choices=reg.ROLES)
    ap.add_argument("--code-commit", required=True, help="commit the campaign's simulations ran on")
    ap.add_argument("--code-tag", default="", help="Git tag pinning that commit, if any")
    ap.add_argument("--note", required=True)
    ap.add_argument("--log", action="append", default=[], help="log file to preserve (repeatable)")
    ap.add_argument("--extra", action="append", default=[], metavar="LABEL=DIR",
                    help="additional development output to preserve, e.g. work_smoke=work/smoke (repeatable)")
    ap.add_argument("--archive-dir", default="archive")
    a = ap.parse_args(argv)
    extra = {}
    for item in a.extra:
        label, _, path = item.partition("=")
        if not label or not path or label in ("raw", "work_variants", "work_runs"):
            print(f"bad --extra {item!r}; expected LABEL=DIR with a new label", file=sys.stderr)
            return 2
        extra[label] = REPO_ROOT / path

    cfg = config.study()
    results, work = config.results_dir(cfg), config.work_dir(cfg)
    processed, raw = results / "processed" / a.campaign, results / "raw" / a.campaign
    snap_file = processed / "campaign_configs.json"
    if not snap_file.is_file():
        print(f"no campaign snapshot at {snap_file}", file=sys.stderr)
        return 2
    if reg.is_sealed(a.campaign, results):
        print(f"campaign {a.campaign!r} is already sealed", file=sys.stderr)
        return 2
    snap = json.loads(snap_file.read_text(encoding="utf-8"))

    logdir = processed / "logs"
    logdir.mkdir(exist_ok=True)
    for lp in a.log:
        src = Path(lp)
        dst = logdir / src.name
        if dst.exists() and sha256_file(dst) != sha256_file(src):
            print(f"{dst} exists with different content", file=sys.stderr)
            return 2
        shutil.copyfile(src, dst)

    loaded = []
    for name, digest in sorted(snap["configs"].items()):
        lc = config.load_yaml(config.config_dir() / name)
        if lc.sha256 != digest:
            print(f"{lc.path} no longer matches the campaign snapshot; recover it with "
                  f"`git show {a.code_commit}:configs/{name}` before archiving", file=sys.stderr)
            return 2
        loaded.append(lc)
    reg.snapshot_configs(processed, loaded)

    roots = {"raw": raw, "work_variants": work / "variants" / a.campaign, "work_runs": work / "runs" / a.campaign,
             **extra}
    entries = reg.build_manifest(roots)
    manifest = processed / reg.ARCHIVE_MANIFEST
    reg.write_manifest(manifest, entries)
    tar_path = REPO_ROOT / a.archive_dir / a.campaign / f"{a.campaign}_raw_and_workspaces.tar"
    info = reg.write_archive(tar_path, roots, manifest)
    archive = {
        "campaign": a.campaign, "created_utc": utc_now(), "n_files": len(entries),
        "manifest": reg.ARCHIVE_MANIFEST, "manifest_sha256": sha256_file(manifest),
        "tar": {**info, "path": tar_path.relative_to(REPO_ROOT).as_posix()},
        "storage": "local, Git-ignored; not uploaded anywhere. Neel chooses durable storage (DECISIONS N-16).",
    }
    (processed / "ARCHIVE.json").write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n", encoding="utf-8",
                                            newline="\n")

    reg.register(a.campaign, a.role, results, a.note)
    seal = reg.seal(a.campaign, results, role=a.role, code_commit=a.code_commit, note=a.note,
                    extra={"code_tag": a.code_tag, "archive_manifest_sha256": archive["manifest_sha256"],
                           "archive_tar_sha256": info["sha256"], "n_files": len(entries)})
    print(f"sealed {a.campaign}: {len(entries)} files, tar {info['size_bytes'] / 1e9:.2f} GB, {seal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
