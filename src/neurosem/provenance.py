"""Provenance: hashing, environment digests, Git state and immutable result storage."""

from __future__ import annotations

import datetime as dt
import functools
import hashlib
import importlib.metadata
import json
import os
import platform
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path | str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def sha256_json(obj: Any) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def tree_manifest(root: Path, exclude: tuple[str, ...] = ("variant.json", "PROVENANCE.json")) -> dict[str, str]:
    """Relative POSIX path -> SHA-256 for every file under ``root``."""
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name not in exclude:
            out[p.relative_to(root).as_posix()] = sha256_file(p)
    return out


def tree_sha256(root: Path, exclude: tuple[str, ...] = ("variant.json", "PROVENANCE.json")) -> str:
    return sha256_json(tree_manifest(root, exclude))


def git_state(repo: Path = REPO_ROOT) -> tuple[str, bool]:
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=repo,
                                    capture_output=True, text=True, check=True).stdout.strip())
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        # Inside the container there is no .git; the image records the commit it was built from.
        # The tree cannot be checked for local changes, so it is reported as dirty.
        return os.environ.get("NEUROSEM_GIT_COMMIT", "unknown"), True


@functools.lru_cache(maxsize=1)
def python_environment() -> dict[str, Any]:
    dists = sorted(f"{d.metadata['Name'].lower()}=={d.version}" for d in importlib.metadata.distributions()
                   if d.metadata["Name"])
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": dists,
    }


def environment_digest(extra: dict[str, Any] | None = None) -> tuple[str, dict[str, Any]]:
    """Digest of the Python environment plus simulator facts (Java version, jar hash)."""
    env = dict(python_environment())
    if image := os.environ.get("NEUROSEM_CONTAINER_IMAGE"):   # e.g. repo@sha256:..., set with docker run -e
        env["container_image"] = image
    if extra:
        env.update(extra)
    return sha256_json(env), env


class ImmutableWriteError(RuntimeError):
    pass


def write_immutable(path: Path, data: bytes) -> str:
    """Write ``data`` once. Rewriting identical bytes is a no-op; different bytes raise.

    Files are marked read-only after writing. Returns the SHA-256 of the content.
    """
    digest = sha256_bytes(data)
    if path.exists():
        if sha256_file(path) != digest:
            raise ImmutableWriteError(f"refusing to overwrite immutable file {path}")
        return digest
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)
    os.chmod(path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    return digest


def write_immutable_text(path: Path, text: str) -> str:
    return write_immutable(path, text.encode("utf-8"))


def relpath(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()
