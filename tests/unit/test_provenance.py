"""Tests for nexclamp.provenance: hashes, tree manifests, environment digests and immutable writes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

import pytest

from nexclamp import provenance as prov
from nexclamp.provenance import (
    ImmutableWriteError,
    environment_digest,
    git_state,
    python_environment,
    relpath,
    sha256_bytes,
    sha256_file,
    sha256_json,
    tree_manifest,
    tree_sha256,
    utc_now,
    write_immutable,
    write_immutable_text,
)

ABC_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"   # FIPS 180-2 test vector


def _make_tree(root: Path, files: dict[str, bytes]) -> None:
    for rel, data in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def _writable(path: Path) -> bool:
    return bool(path.stat().st_mode & stat.S_IWRITE)


# ---------------------------------------------------------------------------------------- hashing
def test_sha256_bytes_known_vector():
    assert sha256_bytes(b"abc") == ABC_SHA256


def test_sha256_file_matches_bytes_across_chunk_boundaries(tmp_path):
    data = bytes(range(256)) * 3 + b"tail"
    p = tmp_path / "blob.bin"
    p.write_bytes(data)
    assert sha256_file(p) == sha256_bytes(data)
    assert sha256_file(p, chunk=7) == sha256_bytes(data)
    assert sha256_file(str(p)) == sha256_bytes(data)


def test_sha256_json_is_canonical():
    a = {"b": [1, 2, {"y": 1.5, "x": None}], "a": "µV"}
    b = {"a": "µV", "b": [1, 2, {"x": None, "y": 1.5}]}
    assert sha256_json(a) == sha256_json(b)
    canonical = json.dumps(a, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert sha256_json(a) == hashlib.sha256(canonical).hexdigest()
    assert sha256_json({"a": 1}) != sha256_json({"a": 1.5})
    assert sha256_json([1, 2]) != sha256_json([2, 1])          # list order is significant


# ---------------------------------------------------------------------------------- tree hashes
FILES = {
    "NeuroML2/cells/RS/RS.cell.nml": b"<cell/>",
    "NeuroML2/channels/Na/Na.channel.nml": b"<ionChannel/>",
    "LICENSE": b"MIT",
}


def test_tree_manifest_relative_posix_paths(tmp_path):
    _make_tree(tmp_path, FILES)
    m = tree_manifest(tmp_path)
    assert m == {k: sha256_bytes(v) for k, v in FILES.items()}
    assert all("\\" not in k for k in m)


def test_tree_sha256_independent_of_creation_order(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    _make_tree(a, FILES)
    _make_tree(b, dict(reversed(list(FILES.items()))))
    assert tree_sha256(a) == tree_sha256(b)
    assert tree_sha256(a) == tree_sha256(a)


def test_tree_sha256_ignores_metadata(tmp_path):
    _make_tree(tmp_path, FILES)
    before = tree_sha256(tmp_path)
    p = tmp_path / "LICENSE"
    os.utime(p, (1_000_000, 1_000_000))
    p.chmod(stat.S_IREAD)
    (tmp_path / "empty_dir" / "nested").mkdir(parents=True)        # empty directories are not content
    assert tree_sha256(tmp_path) == before
    p.chmod(stat.S_IREAD | stat.S_IWRITE)


@pytest.mark.parametrize("change", ["content", "rename", "add", "delete"])
def test_tree_sha256_detects_changes(tmp_path, change):
    _make_tree(tmp_path, FILES)
    before = tree_sha256(tmp_path)
    target = tmp_path / "NeuroML2/cells/RS/RS.cell.nml"
    if change == "content":
        target.write_bytes(b"<cell />")
    elif change == "rename":
        target.rename(target.with_name("RS2.cell.nml"))
    elif change == "add":
        (tmp_path / "extra.txt").write_bytes(b"")                  # even an empty file counts
    else:
        target.unlink()
    assert tree_sha256(tmp_path) != before


def test_default_exclusions_apply_by_name_at_any_depth(tmp_path):
    _make_tree(tmp_path, FILES)
    before = tree_sha256(tmp_path)
    _make_tree(tmp_path, {"variant.json": b"{}", "PROVENANCE.json": b"{}",
                          "NeuroML2/variant.json": b"{1}", "NeuroML2/cells/PROVENANCE.json": b"{2}"})
    assert tree_sha256(tmp_path) == before
    assert set(tree_manifest(tmp_path)) == set(FILES)


def test_exclusion_is_exact_name_not_substring(tmp_path):
    _make_tree(tmp_path, FILES)
    before = tree_sha256(tmp_path)
    (tmp_path / "my_variant.json").write_bytes(b"{}")
    (tmp_path / "variant.json.bak").write_bytes(b"{}")
    assert tree_sha256(tmp_path) != before
    assert {"my_variant.json", "variant.json.bak"} <= set(tree_manifest(tmp_path))


def test_custom_exclusion_replaces_defaults(tmp_path):
    _make_tree(tmp_path, {**FILES, "variant.json": b"{}", "LEMS_ns_probe.xml": b"<Lems/>"})
    m = tree_manifest(tmp_path, exclude=("LEMS_ns_probe.xml",))
    assert "variant.json" in m and "LEMS_ns_probe.xml" not in m


# ---------------------------------------------------------------------------------- immutable write
def test_write_immutable_creates_read_only_file(tmp_path):
    p = tmp_path / "results" / "raw" / "c1" / "r-abc" / "run.json"
    digest = write_immutable(p, b'{"a": 1}\n')
    assert digest == sha256_bytes(b'{"a": 1}\n')
    assert p.read_bytes() == b'{"a": 1}\n'
    assert not _writable(p)
    assert not os.access(p, os.W_OK)
    with pytest.raises(PermissionError):
        p.write_bytes(b"tamper")
    assert list(p.parent.iterdir()) == [p]                          # no temporary file left behind


def test_identical_rewrite_is_noop(tmp_path):
    p = tmp_path / "features.json"
    d1 = write_immutable(p, b"same")
    st1 = p.stat()
    d2 = write_immutable(p, b"same")
    st2 = p.stat()
    assert d1 == d2 == sha256_bytes(b"same")
    assert st2.st_mtime_ns == st1.st_mtime_ns
    assert not _writable(p)


def test_different_content_raises_and_preserves_original(tmp_path):
    p = tmp_path / "run.json"
    write_immutable(p, b"first")
    with pytest.raises(ImmutableWriteError, match="refusing to overwrite"):
        write_immutable(p, b"second")
    assert p.read_bytes() == b"first"
    assert not (tmp_path / "run.json.tmp").exists()


def test_existing_mutable_file_with_different_content_is_protected(tmp_path):
    # A file that already exists (e.g. written by hand) is never silently replaced.
    p = tmp_path / "run.json"
    p.write_bytes(b"hand written")
    with pytest.raises(ImmutableWriteError):
        write_immutable(p, b"generated")
    assert p.read_bytes() == b"hand written"


def test_write_immutable_text_is_utf8(tmp_path):
    p = tmp_path / "note.txt"
    digest = write_immutable_text(p, "µV drift ✓")
    assert p.read_bytes() == "µV drift ✓".encode("utf-8")
    assert digest == sha256_bytes("µV drift ✓".encode("utf-8"))
    assert write_immutable_text(p, "µV drift ✓") == digest


def test_write_immutable_file_without_suffix(tmp_path):
    p = tmp_path / "LOCK"
    write_immutable(p, b"x")
    assert p.read_bytes() == b"x" and not (tmp_path / "LOCK.tmp").exists()


# ------------------------------------------------------------------------------------ environment
def test_python_environment_records_pinned_packages():
    env = python_environment()
    assert re.fullmatch(r"3\.12\.\d+", env["python"])
    pk = set(env["packages"])
    assert "efel==5.7.34" in pk and "pyneuroml==1.3.22" in pk and "libneuroml==0.6.7" in pk
    assert env["packages"] == sorted(env["packages"])


def test_environment_digest_extra_changes_digest_without_leaking_into_cache():
    d0, e0 = environment_digest()
    d1, e1 = environment_digest({"jar_sha256": "0" * 64})
    d2, _ = environment_digest({"jar_sha256": "0" * 64})
    assert d0 != d1 and d1 == d2
    assert e1["jar_sha256"] == "0" * 64
    assert "jar_sha256" not in python_environment()
    assert d0 == sha256_json(e0)


def test_git_state_outside_repository(tmp_path):
    assert git_state(tmp_path) == ("unknown", True)


def test_git_state_in_repository():
    commit, dirty = git_state()
    assert isinstance(dirty, bool)
    assert commit == "unknown" or re.fullmatch(r"[0-9a-f]{40}", commit)


def test_relpath_inside_and_outside_repo(tmp_path):
    assert relpath(prov.REPO_ROOT / "configs" / "study.yaml") == "configs/study.yaml"
    outside = relpath(tmp_path / "x.txt")
    assert outside == (tmp_path / "x.txt").resolve().as_posix()
    assert relpath(tmp_path / "a" / "b.txt", root=tmp_path) == "a/b.txt"


def test_utc_now_is_iso_utc():
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00", utc_now())


def test_repo_root_points_at_repository():
    assert (prov.REPO_ROOT / "pyproject.toml").is_file()
    assert (prov.REPO_ROOT / "src" / "nexclamp" / "provenance.py").is_file()
