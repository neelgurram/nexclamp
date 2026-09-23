"""Download Eclipse Temurin 21 from the Adoptium API into ``.tools/`` with verified provenance.

NeuroSem drives jNeuroML, a Java program bundled with pyNeuroML, so the Java runtime is
part of the study environment. This script installs it without installers or admin
rights, and makes the download auditable:

1. ask the Adoptium API for exactly one asset (the latest Temurin 21, or an exact
   ``--release``) for this operating system and CPU architecture;
2. download the archive while hashing it and require its SHA-256 to equal the API
   checksum, the publisher's ``.sha256.txt`` file, and ``--expect-sha256`` when given
   (a pin written into the Dockerfile, so a changed upstream answer fails the build);
3. extract it safely (no absolute or ``..`` paths; tar uses the stdlib ``data`` filter)
   into a private temporary directory and run ``java -version`` there, so a runtime that
   cannot run on this machine is deleted instead of being left where ``find_java`` looks;
4. move it to ``<dest>/<archive top-level directory>`` and write
   ``<dest>/<directory>.provenance.json``.

API facts verified live on 2026-09-13: ``/v3/assets/latest/21/hotspot`` returns a JSON
list with one ``binary`` per entry; ``/v3/assets/release_name/eclipse/<release>`` returns
one object with a ``binaries`` list; the API answers HTTP 403 to urllib's default
User-Agent, so a descriptive one is sent. Archive layouts for jdk-21.0.12.1+1: JDK
archives unpack to ``jdk-<release>/``, JRE archives to ``jdk-<release>-jre/``, and macOS
archives keep the runtime under ``Contents/Home/``.

Standard library only, because it runs before any project dependency is installed
(including inside the Docker build).

Usage:
    python scripts/bootstrap_java.py --dry-run          # query and report; write nothing
    python scripts/bootstrap_java.py                    # latest Temurin 21 JDK -> .tools/
    python scripts/bootstrap_java.py --release jdk-21.0.12.1+1 --image-type jre \\
        --expect-sha256 <hex> --dest /opt/java
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.adoptium.net/v3"
USER_AGENT = "neurosem-bootstrap-java/1 (python-urllib; reproducible Temurin download)"
PROVENANCE_SCHEMA = "neurosem.bootstrap_java/1"
FEATURE_VERSION = 21
VENDOR = "eclipse"
OS_NAMES = {"windows": "windows", "linux": "linux", "darwin": "mac"}
ARCH_NAMES = {"amd64": "x64", "x86_64": "x64", "x64": "x64", "arm64": "aarch64", "aarch64": "aarch64"}
SUPPORTED_OS = ("windows", "linux", "mac", "alpine-linux")
SUPPORTED_ARCH = ("x64", "aarch64")
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class BootstrapError(RuntimeError):
    """A condition that must stop the bootstrap (bad API answer, checksum mismatch, unsafe archive)."""


@dataclass(frozen=True)
class Asset:
    release_name: str
    openjdk_version: str
    vendor: str
    os: str
    architecture: str
    image_type: str
    jvm_impl: str
    package_name: str
    link: str
    sha256: str
    size: int
    checksum_link: str | None
    updated_at: str | None
    api_url: str


# --------------------------------------------------------------------------- platform / API
def adoptium_platform(system: str | None = None, machine: str | None = None) -> tuple[str, str]:
    """Map ``platform.system()``/``platform.machine()`` to Adoptium ``os``/``architecture`` names."""
    sys_name = (system if system is not None else platform.system()).lower()
    mach = (machine if machine is not None else platform.machine()).lower()
    if sys_name not in OS_NAMES:
        raise BootstrapError(f"unsupported operating system {sys_name!r}; pass --os explicitly")
    if mach not in ARCH_NAMES:
        raise BootstrapError(f"unsupported CPU architecture {mach!r}; pass --arch explicitly")
    return OS_NAMES[sys_name], ARCH_NAMES[mach]


def api_url(os_name: str, arch: str, image_type: str, release: str | None = None,
            api_base: str = API_BASE) -> str:
    """Adoptium v3 asset query. Only query parameters verified live for each endpoint are sent."""
    base = api_base.rstrip("/")
    if release is None:
        query = {"os": os_name, "architecture": arch, "image_type": image_type, "vendor": VENDOR}
        path = f"/assets/latest/{FEATURE_VERSION}/hotspot"
    else:
        query = {"os": os_name, "architecture": arch, "image_type": image_type, "jvm_impl": "hotspot",
                 "heap_size": "normal"}
        path = f"/assets/release_name/{VENDOR}/{urllib.parse.quote(release, safe='')}"
    return f"{base}{path}?{urllib.parse.urlencode(query)}"


def require_safe_url(url: str) -> None:
    """Downloads must use HTTPS; plain HTTP is accepted only for loopback test servers."""
    parts = urllib.parse.urlparse(url)
    if parts.scheme == "https" and parts.hostname:
        return
    if parts.scheme == "http" and parts.hostname in LOOPBACK_HOSTS:
        return
    raise BootstrapError(f"refusing non-HTTPS URL {url!r}")


def parse_assets(payload: Any, *, os_name: str, arch: str, image_type: str, url: str) -> Asset:
    """Select exactly one matching binary from either API response shape and validate it."""
    if isinstance(payload, list):  # /assets/latest/...: one entry per binary
        entries = [(e, e.get("binary") or {}) for e in payload if isinstance(e, dict)]
        version_key = "version"
    elif isinstance(payload, dict) and isinstance(payload.get("binaries"), list):  # /assets/release_name/...
        entries = [(payload, b) for b in payload["binaries"] if isinstance(b, dict)]
        version_key = "version_data"
    else:
        raise BootstrapError(f"unexpected Adoptium API response shape from {url}")
    matches = [(e, b) for e, b in entries
               if b.get("os") == os_name and b.get("architecture") == arch and b.get("image_type") == image_type
               and b.get("jvm_impl") == "hotspot" and b.get("heap_size", "normal") == "normal"
               and b.get("project", "jdk") == "jdk"]
    if len(matches) != 1:
        raise BootstrapError(f"expected exactly one Temurin {image_type} for {os_name}/{arch}, "
                             f"API returned {len(matches)} matching binaries ({url})")
    entry, binary = matches[0]
    pkg = binary.get("package") or {}
    sha = str(pkg.get("checksum", "")).lower()
    name = str(pkg.get("name", ""))
    link = str(pkg.get("link", ""))
    size = pkg.get("size")
    version = entry.get(version_key) or {}
    if not _HEX64.match(sha):
        raise BootstrapError(f"API checksum for {name or '?'} is not a SHA-256 hex digest: {sha!r}")
    if not name.endswith((".zip", ".tar.gz")) or "/" in name or "\\" in name:
        raise BootstrapError(f"unexpected package name {name!r}")
    require_safe_url(link)
    if urllib.parse.unquote(PurePosixPath(urllib.parse.urlparse(link).path).name) != name:
        raise BootstrapError(f"package link {link!r} does not end in package name {name!r}")
    if not isinstance(size, int) or size <= 0:
        raise BootstrapError(f"invalid package size {size!r}")
    if version.get("major") != FEATURE_VERSION:
        raise BootstrapError(f"API returned Java major version {version.get('major')!r}, expected {FEATURE_VERSION}")
    if entry.get("vendor") != VENDOR:
        raise BootstrapError(f"API returned vendor {entry.get('vendor')!r}, expected {VENDOR!r}")
    checksum_link = pkg.get("checksum_link")
    if checksum_link:
        require_safe_url(checksum_link)
    return Asset(
        release_name=str(entry.get("release_name", "")),
        openjdk_version=str(version.get("openjdk_version", "")),
        vendor=VENDOR, os=os_name, architecture=arch, image_type=image_type, jvm_impl="hotspot",
        package_name=name, link=link, sha256=sha, size=size, checksum_link=checksum_link or None,
        updated_at=binary.get("updated_at"), api_url=url,
    )


# --------------------------------------------------------------------------- network
def _open(url: str, accept: str, timeout: float):
    require_safe_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    resp = urllib.request.urlopen(req, timeout=timeout)  # scheme checked above
    require_safe_url(resp.geturl())  # redirects must stay on HTTPS too
    return resp


def fetch_json(url: str, timeout: float = 60.0) -> Any:
    try:
        with _open(url, "application/json", timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        raise BootstrapError(f"HTTP {exc.code} from {url}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise BootstrapError(f"could not read JSON from {url}: {exc}") from exc


def fetch_text(url: str, timeout: float = 60.0) -> str:
    try:
        with _open(url, "text/plain", timeout) as resp:
            return resp.read(1 << 16).decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise BootstrapError(f"HTTP {exc.code} from {url}") from exc
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError) as exc:
        raise BootstrapError(f"could not read {url}: {exc}") from exc


def parse_checksum_file(text: str, package_name: str) -> str:
    """Digest from a ``sha256sum``-style ``<hex>  <name>`` line (a bare digest is also accepted)."""
    for line in text.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        digest = parts[0].lower()
        name = parts[1].lstrip("*") if len(parts) > 1 else package_name
        if _HEX64.match(digest) and name == package_name:
            return digest
    raise BootstrapError(f"no SHA-256 line for {package_name} in checksum file")


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def download(url: str, target: Path, expected_sha256: str, expected_size: int | None = None,
             timeout: float = 120.0, chunk: int = 1 << 20) -> str:
    """Stream ``url`` into ``target`` and return its SHA-256.

    Bytes go to ``<target>.part`` and are hashed while streaming; the file is renamed into
    place only if size and digest both match, so a truncated or tampered download never
    looks like a valid archive.
    """
    part = target.with_name(target.name + ".part")
    h = hashlib.sha256()
    n = 0
    try:
        with _open(url, "application/octet-stream", timeout) as resp, open(part, "wb") as f:
            while block := resp.read(chunk):
                h.update(block)
                f.write(block)
                n += len(block)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        part.unlink(missing_ok=True)
        raise BootstrapError(f"download failed for {url}: {exc}") from exc
    digest = h.hexdigest()
    if expected_size is not None and n != expected_size:
        part.unlink(missing_ok=True)
        raise BootstrapError(f"size mismatch for {target.name}: got {n} bytes, expected {expected_size}")
    if digest != expected_sha256.lower():
        part.unlink(missing_ok=True)
        raise BootstrapError(f"SHA-256 mismatch for {target.name}: got {digest}, expected {expected_sha256}")
    os.replace(part, target)
    return digest


# --------------------------------------------------------------------------- archives / Java
def _member_path_ok(name: str) -> bool:
    p = PurePosixPath(name.replace("\\", "/"))
    return bool(name) and not p.is_absolute() and ".." not in p.parts and not re.match(r"^[A-Za-z]:", name)


def expected_install_name(asset: Asset) -> str:
    """Conventional top-level directory of Temurin archives (verified for jdk-21.0.12.1+1)."""
    return asset.release_name + ("-jre" if asset.image_type == "jre" else "")


def safe_extract(archive: Path, dest: Path, verify: Callable[[Path], None] | None = None) -> Path:
    """Extract ``archive`` (``.zip`` or ``.tar.gz``) and move its single top-level directory into ``dest``.

    Extraction happens in a private temporary directory under ``dest``. ``verify`` (in ``run``:
    locate ``java`` and execute ``java -version``) is called on the extracted directory while it
    is still in that temporary directory, and the move into ``dest`` happens only if it returns.
    A rejected archive or a runtime that fails its check is therefore deleted with the temporary
    directory and never appears where ``find_java`` (``.tools/jdk-*/bin/java``) would pick it up.
    """
    dest.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".extract-", dir=dest))
    try:
        if archive.name.endswith(".zip"):
            with zipfile.ZipFile(archive) as z:
                bad = [n for n in z.namelist() if not _member_path_ok(n)]
                if bad:
                    raise BootstrapError(f"unsafe paths in {archive.name}: {bad[:3]}")
                z.extractall(tmp)
        elif archive.name.endswith(".tar.gz"):
            with tarfile.open(archive, "r:gz") as t:
                try:
                    t.extractall(tmp, filter="data")
                except tarfile.FilterError as exc:
                    raise BootstrapError(f"unsafe member in {archive.name}: {exc}") from exc
        else:
            raise BootstrapError(f"unsupported archive type: {archive.name}")
        tops = list(tmp.iterdir())
        if len(tops) != 1 or not tops[0].is_dir():
            raise BootstrapError(f"{archive.name} must contain exactly one top-level directory, "
                                 f"found {sorted(p.name for p in tops)}")
        final = dest / tops[0].name
        if final.exists():
            raise BootstrapError(f"{final} already exists; remove it or choose another --dest")
        if verify is not None:
            verify(tops[0])
        os.replace(tops[0], final)
        return final
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def java_home(install_dir: Path) -> Path:
    """macOS archives nest the runtime in ``Contents/Home``; other platforms use the top directory."""
    mac_home = install_dir / "Contents" / "Home"
    return mac_home if (mac_home / "bin").is_dir() else install_dir


def java_executable(install_dir: Path, os_name: str) -> Path:
    exe = java_home(install_dir) / "bin" / ("java.exe" if os_name == "windows" else "java")
    if not exe.is_file():
        raise BootstrapError(f"no Java executable at {exe}")
    return exe


def read_release_file(home: Path) -> dict[str, str]:
    """Parse the JDK ``release`` file (``KEY="value"`` lines); empty dict if absent."""
    path = home / "release"
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            out[key.strip()] = value.strip().strip('"')
    return out


def java_version(java: Path, timeout: float = 120.0) -> str:
    """Run ``java -version``; the JVM prints the version banner on stderr."""
    try:
        proc = subprocess.run([str(java), "-version"], capture_output=True, text=True, timeout=timeout,
                              check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BootstrapError(f"could not run {java} -version: {exc}") from exc
    out = (proc.stderr or proc.stdout).strip()
    if proc.returncode != 0:
        raise BootstrapError(f"{java} -version exited {proc.returncode}: {out}")
    return out


# --------------------------------------------------------------------------- provenance
def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def provenance_path(install_dir: Path) -> Path:
    return install_dir.with_name(install_dir.name + ".provenance.json")


def provenance_record(asset: Asset, install_dir: Path, java: Path, action: str, *,
                      downloaded_sha256: str | None, checksum_file_sha256: str | None,
                      pinned_sha256: str | None, java_version_output: str | None) -> dict[str, Any]:
    return {
        "schema": PROVENANCE_SCHEMA,
        "created_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "action": action,
        "script": _display_path(Path(__file__)),
        "script_sha256": sha256_file(Path(__file__)),
        "host": {"system": platform.system(), "release": platform.release(), "machine": platform.machine(),
                 "python": platform.python_version()},
        "asset": asdict(asset),
        "verification": {
            "api_sha256": asset.sha256,
            "checksum_file_sha256": checksum_file_sha256,
            "pinned_sha256": pinned_sha256,
            "archive_sha256": downloaded_sha256,
            "archive_verified": downloaded_sha256 is not None,
        },
        "install_dir": _display_path(install_dir),
        "java_executable": _display_path(java),
        "release_file": read_release_file(java_home(install_dir)),
        "java_version_output": java_version_output,
    }


def write_provenance(path: Path, record: dict[str, Any]) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(record, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# --------------------------------------------------------------------------- CLI
def _sha256_arg(value: str) -> str:
    v = value.strip().lower()
    if not _HEX64.match(v):
        raise argparse.ArgumentTypeError("expected a 64-character hex SHA-256 digest")
    return v


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dest", type=Path, default=REPO_ROOT / ".tools", help="install directory (default: .tools/)")
    p.add_argument("--image-type", choices=("jdk", "jre"), default="jdk")
    p.add_argument("--release", help="exact Adoptium release name, e.g. jdk-21.0.12.1+1 (default: latest 21)")
    p.add_argument("--os", choices=SUPPORTED_OS, help="override detected OS (e.g. alpine-linux for musl)")
    p.add_argument("--arch", choices=SUPPORTED_ARCH, help="override detected CPU architecture")
    p.add_argument("--expect-sha256", type=_sha256_arg, help="pinned archive digest; must equal the API checksum")
    p.add_argument("--dry-run", action="store_true", help="query and verify metadata only; download and write nothing")
    p.add_argument("--keep-archive", action="store_true", help="keep the verified archive next to the install")
    p.add_argument("--skip-java-check", action="store_true",
                   help="do not execute the extracted java (e.g. when installing for another architecture)")
    p.add_argument("--api-base", default=API_BASE, help="Adoptium API base URL (for mirrors and tests)")
    p.add_argument("--timeout", type=float, default=120.0, help="network timeout in seconds")
    return p.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    if args.os and args.arch:
        os_name, arch = args.os, args.arch
    else:
        detected_os, detected_arch = adoptium_platform()
        os_name, arch = args.os or detected_os, args.arch or detected_arch

    url = api_url(os_name, arch, args.image_type, args.release, args.api_base)
    print(f"query     {url}")
    asset = parse_assets(fetch_json(url, args.timeout), os_name=os_name, arch=arch,
                         image_type=args.image_type, url=url)
    if args.release and asset.release_name != args.release:
        raise BootstrapError(f"API returned release {asset.release_name!r}, requested {args.release!r}")
    print(f"release   {asset.release_name} ({asset.openjdk_version}), {asset.os}/{asset.architecture} {asset.image_type}")
    print(f"package   {asset.package_name} ({asset.size / 1e6:.1f} MB)")
    print(f"sha256    {asset.sha256} (API)")
    if args.expect_sha256 and asset.sha256 != args.expect_sha256:
        raise BootstrapError(f"API checksum {asset.sha256} differs from pinned --expect-sha256 {args.expect_sha256}")

    checksum_file_sha = None
    if asset.checksum_link:
        checksum_file_sha = parse_checksum_file(fetch_text(asset.checksum_link, args.timeout), asset.package_name)
        if checksum_file_sha != asset.sha256:
            raise BootstrapError(f"checksum file {asset.checksum_link} says {checksum_file_sha}, API says {asset.sha256}")
        print("sha256    matches the publisher's .sha256.txt file")

    dest: Path = args.dest.resolve()
    install_dir = dest / expected_install_name(asset)

    if install_dir.is_dir():
        java = java_executable(install_dir, asset.os)
        runtime = read_release_file(java_home(install_dir)).get("JAVA_RUNTIME_VERSION")
        if runtime != asset.openjdk_version:
            raise BootstrapError(f"{install_dir} exists but its release file says JAVA_RUNTIME_VERSION={runtime!r}, "
                                 f"not {asset.openjdk_version!r}; remove it or choose another --dest")
        print(f"installed {install_dir} (JAVA_RUNTIME_VERSION={runtime} matches the API release)")
        version_out = None if args.skip_java_check else java_version(java, args.timeout)
        if version_out:
            print(f"java      {java}: {version_out.splitlines()[0]}")
        prov = provenance_path(install_dir)
        if args.dry_run:
            print(f"dry run   nothing downloaded or written (provenance {'present' if prov.exists() else 'absent'}: {prov})")
            return 0
        if prov.exists():
            print(f"provenance already recorded at {prov}; left unchanged")
        else:
            write_provenance(prov, provenance_record(
                asset, install_dir, java, "existing_install", downloaded_sha256=None,
                checksum_file_sha256=checksum_file_sha, pinned_sha256=args.expect_sha256,
                java_version_output=version_out))
            print(f"wrote     {prov} (archive not re-verified: install predates this script run)")
        return 0

    archive = dest / asset.package_name
    if args.dry_run:
        print(f"dry run   would download {asset.link}")
        print(f"          -> {archive}, verify SHA-256, extract to {install_dir}, write {provenance_path(install_dir)}")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    if archive.is_file() and sha256_file(archive) == asset.sha256:
        action, digest = "reused_archive", asset.sha256
        print(f"archive   reusing verified {archive}")
    else:
        print(f"download  {asset.link}")
        digest = download(asset.link, archive, asset.sha256, asset.size, timeout=args.timeout)
        action = "downloaded"
        print(f"verified  {archive.name} SHA-256 {digest}")
    checked: dict[str, str | None] = {}

    def verify_runtime(top: Path) -> None:
        # Runs before the move into dest: a JRE for the wrong --arch or a broken archive must fail
        # here and be discarded, not stay installed without provenance. The verified archive is
        # kept on failure, so a retry does not download it again.
        exe = java_executable(top, asset.os)
        checked["version"] = None if args.skip_java_check else java_version(exe, args.timeout)

    extracted = safe_extract(archive, dest, verify=verify_runtime)
    if extracted.name != install_dir.name:
        print(f"warning   archive top-level directory {extracted.name!r} differs from the expected {install_dir.name!r}")
    java = java_executable(extracted, asset.os)
    version_out = checked["version"]
    if version_out:
        print(f"java      {java}: {version_out.splitlines()[0]}")
    if not args.keep_archive:
        archive.unlink()
    prov = provenance_path(extracted)
    write_provenance(prov, provenance_record(
        asset, extracted, java, action, downloaded_sha256=digest, checksum_file_sha256=checksum_file_sha,
        pinned_sha256=args.expect_sha256, java_version_output=version_out))
    print(f"wrote     {prov}")
    if java_home(extracted) != extracted or dest != (REPO_ROOT / ".tools").resolve():
        # nexclamp.simulators.jneuroml.find_java only globs .tools/jdk-*/bin/java.
        print(f"hint      set NEUROSEM_JAVA={java}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args)
    except BootstrapError as exc:
        print(f"bootstrap_java: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
