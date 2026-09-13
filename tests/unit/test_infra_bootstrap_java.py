"""Tests for scripts/bootstrap_java.py (Temurin downloader used by `make java` and the Dockerfile).

Offline tests start a real loopback HTTP server that serves an Adoptium-shaped API answer,
a real archive and its ``.sha256.txt``, so download, hashing, safe extraction and provenance
run end to end without mocks. The API field names in the payloads below were copied from
live responses on 2026-09-13; release numbers used for synthetic archives (21.0.99+9) are
deliberately fake. Live Adoptium checks run only with ``NEUROSEM_NETWORK_TESTS=1``.
"""

from __future__ import annotations

import functools
import hashlib
import http.server
import importlib.util
import io
import json
import os
import sys
import tarfile
import threading
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "bootstrap_java.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("neurosem_bootstrap_java", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve annotations through sys.modules
    spec.loader.exec_module(module)
    return module


bj = _load_script()

VERSION = {"build": 1, "major": 21, "minor": 0, "openjdk_version": "21.0.12.1+1-LTS", "optional": "LTS",
           "patch": 1, "security": 12, "semver": "21.0.12+101.0.LTS"}
REAL_JRE_NAME = "OpenJDK21U-jre_x64_linux_hotspot_21.0.12.1_1.tar.gz"
REAL_JRE_LINK = ("https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/"
                 + REAL_JRE_NAME)
REAL_JRE_SHA = "2413149700df0f7d440500a84a8f764c535f21e5a5e87d38328b64eec2c5b500"


def _binary(*, os_name="linux", arch="x64", image_type="jre", name=REAL_JRE_NAME, link=REAL_JRE_LINK,
            sha=REAL_JRE_SHA, size=52059408):
    return {"architecture": arch, "heap_size": "normal", "image_type": image_type, "jvm_impl": "hotspot",
            "os": os_name, "project": "jdk",
            "package": {"checksum": sha, "checksum_link": link + ".sha256.txt", "link": link, "name": name,
                        "size": size}}


def _latest_payload(binary, release="jdk-21.0.12.1+1", version=VERSION):
    return [{"binary": binary, "release_link": "", "release_name": release, "vendor": "eclipse", "version": version}]


def _release_payload(binaries, release="jdk-21.0.12.1+1", version=VERSION):
    return {"binaries": binaries, "release_name": release, "release_type": "ga", "vendor": "eclipse",
            "version_data": version}


# ------------------------------------------------------------------------------ pure functions
@pytest.mark.parametrize(("system", "machine", "expected"), [
    ("Windows", "AMD64", ("windows", "x64")),
    ("Linux", "x86_64", ("linux", "x64")),
    ("Linux", "aarch64", ("linux", "aarch64")),
    ("Darwin", "arm64", ("mac", "aarch64")),
    ("Darwin", "x86_64", ("mac", "x64")),
])
def test_platform_mapping(system, machine, expected):
    assert bj.adoptium_platform(system, machine) == expected


@pytest.mark.parametrize(("system", "machine"), [("SunOS", "x86_64"), ("Linux", "ppc64le"), ("Windows", "x86")])
def test_platform_mapping_rejects_unsupported(system, machine):
    with pytest.raises(bj.BootstrapError):
        bj.adoptium_platform(system, machine)


def test_api_urls_match_the_live_verified_queries():
    assert bj.api_url("linux", "x64", "jre") == (
        "https://api.adoptium.net/v3/assets/latest/21/hotspot?os=linux&architecture=x64&image_type=jre&vendor=eclipse")
    assert bj.api_url("windows", "x64", "jdk", release="jdk-21.0.12.1+1") == (
        "https://api.adoptium.net/v3/assets/release_name/eclipse/jdk-21.0.12.1%2B1"
        "?os=windows&architecture=x64&image_type=jdk&jvm_impl=hotspot&heap_size=normal")


def test_parse_assets_accepts_both_response_shapes():
    kw = {"os_name": "linux", "arch": "x64", "image_type": "jre", "url": "u"}
    a = bj.parse_assets(_latest_payload(_binary()), **kw)
    b = bj.parse_assets(_release_payload([_binary(arch="aarch64", name="x.tar.gz", link="https://h/x.tar.gz"),
                                          _binary()]), **kw)
    assert a == b
    assert a.release_name == "jdk-21.0.12.1+1"
    assert a.openjdk_version == "21.0.12.1+1-LTS"
    assert a.sha256 == REAL_JRE_SHA
    assert a.size == 52059408
    assert a.checksum_link == REAL_JRE_LINK + ".sha256.txt"
    assert bj.expected_install_name(a) == "jdk-21.0.12.1+1-jre"


@pytest.mark.parametrize("payload", [
    _latest_payload(_binary(arch="aarch64")),                                  # no match for x64
    _release_payload([_binary(), _binary()]),                                  # ambiguous
    _latest_payload(_binary(sha="not-a-digest")),
    _latest_payload(_binary(link="http://example.org/" + REAL_JRE_NAME)),     # plain HTTP
    _latest_payload(_binary(link="https://example.org/other.tar.gz")),        # link/name mismatch
    _latest_payload(_binary(name="evil/../x.tar.gz")),
    _latest_payload(_binary(size=0)),
    _latest_payload(_binary(), version=dict(VERSION, major=17)),
    {"unexpected": "shape"},
])
def test_parse_assets_rejects_bad_answers(payload):
    with pytest.raises(bj.BootstrapError):
        bj.parse_assets(payload, os_name="linux", arch="x64", image_type="jre", url="u")


def test_parse_checksum_file():
    line = f"{REAL_JRE_SHA}  {REAL_JRE_NAME}\n"
    assert bj.parse_checksum_file(line, REAL_JRE_NAME) == REAL_JRE_SHA
    assert bj.parse_checksum_file(f"{REAL_JRE_SHA.upper()} *{REAL_JRE_NAME}", REAL_JRE_NAME) == REAL_JRE_SHA
    assert bj.parse_checksum_file(REAL_JRE_SHA, REAL_JRE_NAME) == REAL_JRE_SHA
    with pytest.raises(bj.BootstrapError):
        bj.parse_checksum_file(f"{REAL_JRE_SHA}  other.tar.gz", REAL_JRE_NAME)


@pytest.mark.parametrize(("url", "ok"), [
    ("https://api.adoptium.net/v3", True),
    ("http://127.0.0.1:8000/x", True),
    ("http://localhost/x", True),
    ("http://api.adoptium.net/v3", False),
    ("file:///etc/passwd", False),
    ("ftp://example.org/x", False),
])
def test_require_safe_url(url, ok):
    if ok:
        bj.require_safe_url(url)
    else:
        with pytest.raises(bj.BootstrapError):
            bj.require_safe_url(url)


# ------------------------------------------------------------------------------ archives
RELEASE_FILE = 'IMPLEMENTOR="Eclipse Adoptium"\nJAVA_RUNTIME_VERSION="21.0.99+9-LTS"\nJAVA_VERSION="21.0.99"\n'


def _tar_gz(members: dict[str, bytes], symlinks: dict[str, str] | None = None) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o755
            t.addfile(info, io.BytesIO(data))
        for name, target in (symlinks or {}).items():
            info = tarfile.TarInfo(name)
            info.type = tarfile.SYMTYPE
            info.linkname = target
            t.addfile(info)
    return buf.getvalue()


def _zip(members: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in members.items():
            z.writestr(name, data)
    return buf.getvalue()


def test_safe_extract_tar_gz_linux_layout(tmp_path):
    archive = tmp_path / "jre.tar.gz"
    archive.write_bytes(_tar_gz({"jdk-21.0.99+9-jre/bin/java": b"#!/bin/sh\n",
                                 "jdk-21.0.99+9-jre/release": RELEASE_FILE.encode()}))
    dest = tmp_path / "dest"
    install = bj.safe_extract(archive, dest)
    assert install == dest / "jdk-21.0.99+9-jre"
    assert bj.java_executable(install, "linux") == install / "bin" / "java"
    assert bj.read_release_file(bj.java_home(install))["JAVA_RUNTIME_VERSION"] == "21.0.99+9-LTS"
    assert sorted(p.name for p in dest.iterdir()) == ["jdk-21.0.99+9-jre"]  # temp dir cleaned up


def test_safe_extract_zip_windows_layout(tmp_path):
    archive = tmp_path / "jdk.zip"
    archive.write_bytes(_zip({"jdk-21.0.99+9/bin/java.exe": b"MZ", "jdk-21.0.99+9/release": RELEASE_FILE.encode()}))
    install = bj.safe_extract(archive, tmp_path / "dest")
    assert bj.java_executable(install, "windows").name == "java.exe"
    with pytest.raises(bj.BootstrapError):
        bj.java_executable(install, "linux")


def test_mac_layout_uses_contents_home(tmp_path):
    archive = tmp_path / "mac.tar.gz"
    archive.write_bytes(_tar_gz({"jdk-21.0.99+9/Contents/Home/bin/java": b"",
                                 "jdk-21.0.99+9/Contents/Home/release": RELEASE_FILE.encode()},
                                symlinks={"jdk-21.0.99+9/Contents/MacOS/libjli.dylib": "../Home/lib/libjli.dylib"}))
    install = bj.safe_extract(archive, tmp_path / "dest")
    assert bj.java_home(install) == install / "Contents" / "Home"
    assert bj.java_executable(install, "mac") == install / "Contents" / "Home" / "bin" / "java"


@pytest.mark.parametrize("builder", [
    lambda: ("evil.tar.gz", _tar_gz({"jdk-x/bin/java": b"", "../escaped.txt": b"x"})),
    lambda: ("evil.tar.gz", _tar_gz({"jdk-x/bin/java": b""}, symlinks={"jdk-x/lib/link": "/etc/passwd"})),
    lambda: ("evil.zip", _zip({"jdk-x/bin/java.exe": b"", "../escaped.txt": b"x"})),
    lambda: ("evil.zip", _zip({"/abs/escaped.txt": b"x"})),
    lambda: ("two.tar.gz", _tar_gz({"a/bin/java": b"", "b/bin/java": b""})),
    lambda: ("thing.7z", b"not an archive"),
])
def test_safe_extract_rejects_unsafe_or_malformed_archives(tmp_path, builder):
    name, data = builder()
    archive = tmp_path / name
    archive.write_bytes(data)
    dest = tmp_path / "dest"
    with pytest.raises(bj.BootstrapError):
        bj.safe_extract(archive, dest)
    assert not (tmp_path / "escaped.txt").exists()
    assert list(dest.iterdir()) == []  # nothing half-installed, temp dir removed


def test_safe_extract_verifies_before_install_and_discards_on_failure(tmp_path):
    archive = tmp_path / "jre.tar.gz"
    archive.write_bytes(_tar_gz({"jdk-21.0.99+9-jre/bin/java": b"#!/bin/sh\n"}))
    dest = tmp_path / "dest"
    seen: list[Path] = []

    def reject(top: Path) -> None:
        seen.append(top)
        raise bj.BootstrapError("runtime failed its check")

    with pytest.raises(bj.BootstrapError, match="failed its check"):
        bj.safe_extract(archive, dest, verify=reject)
    assert seen and seen[0].name == "jdk-21.0.99+9-jre"
    assert seen[0].parent != dest  # checked while still in the private temporary directory
    assert list(dest.iterdir()) == []

    install = bj.safe_extract(archive, dest, verify=seen.append)
    assert install == dest / "jdk-21.0.99+9-jre" and len(seen) == 2


def test_safe_extract_refuses_to_overwrite_existing_install(tmp_path):
    archive = tmp_path / "jre.tar.gz"
    archive.write_bytes(_tar_gz({"jdk-21.0.99+9-jre/bin/java": b""}))
    dest = tmp_path / "dest"
    bj.safe_extract(archive, dest)
    with pytest.raises(bj.BootstrapError):
        bj.safe_extract(archive, dest)


# ------------------------------------------------------------------------------ loopback server e2e
class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # stdlib signature; silence request logging
        pass


@pytest.fixture
def fake_adoptium(tmp_path):
    """Serve ``tmp_path/www`` over HTTP on 127.0.0.1 and yield a helper to publish a release."""
    www = tmp_path / "www"
    www.mkdir()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_QuietHandler, directory=str(www)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    def publish(archive_bytes: bytes, *, api_sha: str | None = None, checksum_file_sha: str | None = None,
                served_bytes: bytes | None = None) -> dict:
        release = "jdk-21.0.99+9"
        name = "OpenJDK21U-jre_x64_linux_hotspot_21.0.99_9.tar.gz"
        real_sha = hashlib.sha256(archive_bytes).hexdigest()
        api_sha = api_sha or real_sha
        (www / "dl").mkdir(exist_ok=True)
        (www / "dl" / name).write_bytes(served_bytes if served_bytes is not None else archive_bytes)
        (www / "dl" / (name + ".sha256.txt")).write_text(f"{checksum_file_sha or api_sha}  {name}\n")
        version = dict(VERSION, openjdk_version="21.0.99+9-LTS", security=99, build=9)
        binary = _binary(name=name, link=f"{base}/dl/{name}", sha=api_sha, size=len(archive_bytes))
        rel_dir = www / "v3" / "assets" / "release_name" / "eclipse"
        rel_dir.mkdir(parents=True, exist_ok=True)
        (rel_dir / release).write_text(json.dumps(_release_payload([binary], release=release, version=version)))
        latest_dir = www / "v3" / "assets" / "latest" / "21"
        latest_dir.mkdir(parents=True, exist_ok=True)
        (latest_dir / "hotspot").write_text(json.dumps(_latest_payload(binary, release=release, version=version)))
        return {"release": release, "name": name, "sha": api_sha, "api_base": f"{base}/v3"}

    yield publish
    server.shutdown()
    server.server_close()


def _jre_archive() -> bytes:
    return _tar_gz({"jdk-21.0.99+9-jre/bin/java": b"#!/bin/sh\necho fake\n",
                    "jdk-21.0.99+9-jre/release": RELEASE_FILE.encode()})


def _argv(pub: dict, dest: Path, *extra: str) -> list[str]:
    return ["--api-base", pub["api_base"], "--os", "linux", "--arch", "x64", "--image-type", "jre",
            "--dest", str(dest), "--skip-java-check", *extra]


def test_end_to_end_download_verify_extract_and_provenance(tmp_path, fake_adoptium, capsys):
    pub = fake_adoptium(_jre_archive())
    dest = tmp_path / "java"
    rc = bj.main(_argv(pub, dest, "--release", pub["release"], "--expect-sha256", pub["sha"]))
    out = capsys.readouterr().out
    assert rc == 0, out
    install = dest / "jdk-21.0.99+9-jre"
    assert (install / "bin" / "java").is_file()
    assert not (dest / pub["name"]).exists(), "archive should be removed unless --keep-archive"
    assert not list(dest.glob("*.part"))
    prov_path = dest / "jdk-21.0.99+9-jre.provenance.json"
    prov = json.loads(prov_path.read_text(encoding="utf-8"))
    assert prov["schema"] == "neurosem.bootstrap_java/1"
    assert prov["action"] == "downloaded"
    assert prov["verification"] == {"api_sha256": pub["sha"], "checksum_file_sha256": pub["sha"],
                                    "pinned_sha256": pub["sha"], "archive_sha256": pub["sha"],
                                    "archive_verified": True}
    assert prov["asset"]["release_name"] == pub["release"]
    assert prov["release_file"]["JAVA_RUNTIME_VERSION"] == "21.0.99+9-LTS"
    assert prov["script_sha256"] == hashlib.sha256(SCRIPT.read_bytes()).hexdigest()

    # Second run sees the matching install and leaves the provenance untouched.
    before = prov_path.read_bytes()
    assert bj.main(_argv(pub, dest, "--release", pub["release"])) == 0
    assert prov_path.read_bytes() == before
    assert "matches the API release" in capsys.readouterr().out


def test_keep_archive_and_reuse(tmp_path, fake_adoptium):
    pub = fake_adoptium(_jre_archive())
    dest = tmp_path / "java"
    assert bj.main(_argv(pub, dest, "--keep-archive")) == 0  # latest endpoint (list shape)
    assert (dest / pub["name"]).is_file()
    assert hashlib.sha256((dest / pub["name"]).read_bytes()).hexdigest() == pub["sha"]


def test_dry_run_writes_nothing(tmp_path, fake_adoptium, capsys):
    pub = fake_adoptium(_jre_archive())
    dest = tmp_path / "java"
    assert bj.main(_argv(pub, dest, "--dry-run")) == 0
    assert not dest.exists()
    assert "would download" in capsys.readouterr().out


def test_tampered_download_is_rejected_and_cleaned_up(tmp_path, fake_adoptium, capsys):
    good = _jre_archive()
    evil = _tar_gz({"jdk-21.0.99+9-jre/bin/java": b"#!/bin/sh\necho tampered\n"})
    pub = fake_adoptium(good, served_bytes=evil + b"\0" * (len(good) - len(evil)) if len(evil) < len(good) else evil)
    dest = tmp_path / "java"
    assert bj.main(_argv(pub, dest)) == 1
    assert "mismatch" in capsys.readouterr().err
    assert not (dest / "jdk-21.0.99+9-jre").exists()
    assert list(dest.iterdir()) == []


def test_runtime_failing_java_version_is_not_left_installed(tmp_path, fake_adoptium, capsys):
    # A verified archive whose java cannot run here (wrong --arch, broken JRE). On Linux the stub
    # exits 3; on Windows it is not an executable image, so starting it raises OSError. Either
    # way no jdk-* directory may remain where find_java() globs, and no provenance is written.
    broken = _tar_gz({"jdk-21.0.99+9-jre/bin/java": b"#!/bin/sh\nexit 3\n",
                      "jdk-21.0.99+9-jre/release": RELEASE_FILE.encode()})
    pub = fake_adoptium(broken)
    dest = tmp_path / "java"
    argv = [a for a in _argv(pub, dest) if a != "--skip-java-check"]
    assert bj.main(argv) == 1
    assert "-version" in capsys.readouterr().err
    assert not list(dest.glob("jdk-*")), "unchecked runtime left in dest"
    assert sorted(p.name for p in dest.iterdir()) == [pub["name"]]  # only the verified archive, for a retry


def test_checksum_file_disagreeing_with_api_stops_before_download(tmp_path, fake_adoptium, capsys):
    pub = fake_adoptium(_jre_archive(), checksum_file_sha="0" * 64)
    dest = tmp_path / "java"
    assert bj.main(_argv(pub, dest)) == 1
    assert "checksum file" in capsys.readouterr().err
    assert not dest.exists()


def test_pin_mismatch_stops_before_download(tmp_path, fake_adoptium, capsys):
    pub = fake_adoptium(_jre_archive())
    dest = tmp_path / "java"
    assert bj.main(_argv(pub, dest, "--expect-sha256", "f" * 64)) == 1
    assert "--expect-sha256" in capsys.readouterr().err
    assert not dest.exists()


def test_existing_install_with_other_version_is_an_error(tmp_path, fake_adoptium, capsys):
    pub = fake_adoptium(_jre_archive())
    dest = tmp_path / "java"
    (dest / "jdk-21.0.99+9-jre" / "bin").mkdir(parents=True)
    (dest / "jdk-21.0.99+9-jre" / "bin" / "java").write_bytes(b"")
    (dest / "jdk-21.0.99+9-jre" / "release").write_text('JAVA_RUNTIME_VERSION="21.0.1+12-LTS"\n')
    assert bj.main(_argv(pub, dest)) == 1
    assert "JAVA_RUNTIME_VERSION" in capsys.readouterr().err


# ------------------------------------------------------------------------------ real JDK / live API
_LOCAL_JAVA = sorted((REPO_ROOT / ".tools").glob("jdk-*/bin/java.exe" if os.name == "nt" else "jdk-*/bin/java"))


@pytest.mark.skipif(not _LOCAL_JAVA, reason="no Temurin install under .tools/")
def test_java_version_on_the_repository_jdk():
    java = _LOCAL_JAVA[-1]
    banner = bj.java_version(java)
    assert '"21.' in banner.splitlines()[0]
    release = bj.read_release_file(bj.java_home(java.parent.parent))
    assert release["IMPLEMENTOR"] == "Eclipse Adoptium"


@pytest.mark.skipif(os.environ.get("NEUROSEM_NETWORK_TESTS") != "1", reason="set NEUROSEM_NETWORK_TESTS=1 for live API")
def test_live_adoptium_dry_run_for_the_docker_pin(tmp_path, capsys):
    rc = bj.main(["--dry-run", "--os", "linux", "--arch", "x64", "--image-type", "jre",
                  "--release", "jdk-21.0.12.1+1", "--expect-sha256", REAL_JRE_SHA, "--dest", str(tmp_path / "j")])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "matches the publisher's .sha256.txt file" in out
    assert not (tmp_path / "j").exists()
