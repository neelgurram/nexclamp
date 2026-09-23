"""Campaign roles, sealing and the firewall between exploratory and confirmatory data.

Neel's direction for the pilot (DECISIONS D-026, D-027):

- Every pilot campaign is exploratory/developmental. It may be used to debug the pipeline,
  refine operators, calibrate tolerances, and select features and protocols.
- Pilot data are preserved, never discarded. A finished campaign is *sealed*: its
  configuration snapshot, logs and a SHA-256 manifest of every raw file (including the
  Git-ignored traces) are recorded, and the pipeline refuses to write into it again.
  A revision is a new campaign name, so the development history stays reportable.
- The confirmatory held-out campaign starts fresh on one clean commit (D-025) and is never
  pooled with exploratory or discovery campaigns for the primary estimate.

``results/campaign_registry.json`` records the role of every campaign.
"""

from __future__ import annotations

import json
import shutil
import tarfile
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from nexclamp.provenance import sha256_file, utc_now, write_immutable_text

EXPLORATORY_PILOT = "exploratory_pilot"
DISCOVERY = "discovery"
CONFIRMATORY_HELDOUT = "confirmatory_heldout"
MODEL_CURATION = "model_curation"      # reference-only checks of candidate models
ROLES = (EXPLORATORY_PILOT, DISCOVERY, CONFIRMATORY_HELDOUT, MODEL_CURATION)
NON_CONFIRMATORY = frozenset({EXPLORATORY_PILOT, DISCOVERY, MODEL_CURATION})

REGISTRY_FILE = "campaign_registry.json"
SEAL_FILE = "SEALED.json"
CONFIG_SNAPSHOT_DIR = "config_snapshot"
ARCHIVE_MANIFEST = "ARCHIVE_MANIFEST.sha256"


class CampaignError(RuntimeError):
    """A campaign would be overwritten, reused under another role, or pooled."""


# --------------------------------------------------------------------------- registry
def _registry_path(results_root: Path) -> Path:
    return Path(results_root) / REGISTRY_FILE


def load_registry(results_root: Path) -> dict[str, dict[str, Any]]:
    p = _registry_path(results_root)
    if not p.is_file():
        return {}
    return dict(json.loads(p.read_text(encoding="utf-8")).get("campaigns", {}))


def _write_registry(results_root: Path, campaigns: Mapping[str, Any]) -> None:
    p = _registry_path(results_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"campaigns": dict(campaigns)}, indent=2, sort_keys=True) + "\n", encoding="utf-8",
                 newline="\n")


def role_of(name: str, results_root: Path) -> str | None:
    return load_registry(results_root).get(name, {}).get("role")


def register(name: str, role: str, results_root: Path, note: str = "") -> dict[str, Any]:
    """Record ``name`` under ``role``. A campaign never changes role."""
    if role not in ROLES:
        raise ValueError(f"unknown campaign role {role!r}; expected one of {ROLES}")
    campaigns = load_registry(results_root)
    current = campaigns.get(name)
    if current is not None:
        if current["role"] != role:
            raise CampaignError(f"campaign {name!r} is registered as {current['role']!r} and cannot be reused as "
                                f"{role!r}; start a new campaign name")
        return current
    entry: dict[str, Any] = {"role": role, "registered_utc": utc_now()}
    if note:
        entry["note"] = note
    campaigns[name] = entry
    _write_registry(results_root, campaigns)
    return entry


# --------------------------------------------------------------------------- guards
def seal_path(name: str, results_root: Path) -> Path:
    return Path(results_root) / "processed" / name / SEAL_FILE


def is_sealed(name: str, results_root: Path) -> bool:
    return seal_path(name, results_root).is_file()


def assert_writable(name: str, role: str, results_root: Path) -> None:
    """Refuse to run pipeline stages into a sealed campaign or under a different role."""
    if is_sealed(name, results_root):
        raise CampaignError(f"campaign {name!r} is sealed ({seal_path(name, results_root)}); its data are preserved "
                            "read-only. Run a revision as a new campaign name.")
    current = role_of(name, results_root)
    if current is not None and current != role:
        raise CampaignError(f"campaign {name!r} is registered as {current!r}, not {role!r}")


def assert_confirmatory_fresh(name: str, results_root: Path) -> None:
    """A confirmatory campaign is new: not an exploratory name, and no prior raw or processed data (D-025)."""
    current = role_of(name, results_root)
    if current in NON_CONFIRMATORY:
        raise CampaignError(f"campaign {name!r} is registered as {current!r}; exploratory and discovery data never "
                            "enter the confirmatory estimate")
    if current is None:
        for sub in ("raw", "processed"):
            d = Path(results_root) / sub / name
            if d.is_dir() and any(d.iterdir()):
                raise CampaignError(f"{d} already contains data; a confirmatory campaign must start fresh (D-025)")


def assert_not_pooled(campaigns: Iterable[str], results_root: Path) -> None:
    """A confirmatory estimate comes from exactly one confirmatory campaign and nothing else."""
    names = sorted(set(campaigns))
    roles = {n: role_of(n, results_root) for n in names}
    if CONFIRMATORY_HELDOUT in roles.values() and len(names) > 1:
        raise CampaignError(f"refusing to pool a confirmatory campaign with other campaigns: {roles}")


def check_config_snapshot(processed: Path, snap: Mapping[str, Any]) -> None:
    """One campaign, one configuration and simulator. A changed config needs a new campaign name."""
    p = Path(processed) / "campaign_configs.json"
    if not p.is_file():
        return
    old = json.loads(p.read_text(encoding="utf-8"))
    for key in ("configs", "simulator"):
        if old.get(key) != snap.get(key):
            raise CampaignError(f"campaign {old.get('campaign')!r} was created with different {key} "
                                f"({p}); start a new campaign name so every campaign has one configuration")


def snapshot_configs(processed: Path, loaded: Iterable[Any]) -> None:
    """Copy each loaded config file into ``<processed>/config_snapshot/`` (write-once, hash-checked)."""
    d = Path(processed) / CONFIG_SNAPSHOT_DIR
    d.mkdir(parents=True, exist_ok=True)
    for lc in loaded:
        target = d / lc.path.name
        if target.is_file():
            if sha256_file(target) != lc.sha256:
                raise CampaignError(f"{target} differs from the config now in use ({lc.path})")
            continue
        shutil.copyfile(lc.path, target)
        if sha256_file(target) != lc.sha256:
            raise CampaignError(f"copy of {lc.path} does not match its recorded hash")


def check_single_clean_commit(raw_dir: Path) -> str:
    """Every run record in ``raw_dir`` comes from one commit with a clean tree. Returns the commit."""
    commits: set[str | None] = set()
    dirty: list[str] = []
    for f in sorted(Path(raw_dir).glob("*/run.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        commits.add(rec.get("git_commit"))
        if rec.get("git_dirty") is not False:
            dirty.append(f.parent.name)
    if not commits:
        raise CampaignError(f"no run records under {raw_dir}")
    if len(commits) != 1 or None in commits:
        raise CampaignError(f"runs under {raw_dir} come from {len(commits)} commits: {sorted(map(str, commits))}")
    if dirty:
        raise CampaignError(f"{len(dirty)} runs under {raw_dir} were recorded with a dirty tree, e.g. {dirty[:3]}")
    return str(commits.pop())


# --------------------------------------------------------------------------- preservation
def build_manifest(roots: Mapping[str, Path]) -> list[tuple[str, str]]:
    """``(sha256, "<label>/<relative path>")`` for every file under each root, sorted by path."""
    out: list[tuple[str, str]] = []
    for label, root in roots.items():
        root = Path(root)
        if not root.is_dir():
            continue
        for f in root.rglob("*"):
            if f.is_file():
                out.append((sha256_file(f), f"{label}/{f.relative_to(root).as_posix()}"))
    return sorted(out, key=lambda t: t[1])


def write_manifest(path: Path, entries: Iterable[tuple[str, str]]) -> None:
    Path(path).write_text("".join(f"{h}  {n}\n" for h, n in entries), encoding="utf-8", newline="\n")


def verify_manifest(path: Path, roots: Mapping[str, Path]) -> list[str]:
    """Paths whose current content is missing or differs from the manifest (empty list = intact)."""
    problems = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        h, name = line.split("  ", 1)
        label, rel = name.split("/", 1)
        f = Path(roots[label]) / rel
        if not f.is_file() or sha256_file(f) != h:
            problems.append(name)
    return problems


def write_archive(tar_path: Path, roots: Mapping[str, Path], manifest_path: Path) -> dict[str, Any]:
    """Write-once uncompressed tar of the manifest and every root; returns its name, hash and size."""
    tar_path = Path(tar_path)
    if tar_path.exists():
        raise CampaignError(f"{tar_path} already exists; archives are write-once")
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    partial = tar_path.with_name(tar_path.name + ".partial")
    with tarfile.open(partial, "w") as tf:
        tf.add(manifest_path, arcname=Path(manifest_path).name)
        for label, root in sorted(roots.items()):
            root = Path(root)
            if root.is_dir():
                for f in sorted(p for p in root.rglob("*") if p.is_file()):
                    tf.add(f, arcname=f"{label}/{f.relative_to(root).as_posix()}")
    partial.replace(tar_path)
    return {"file": tar_path.name, "sha256": sha256_file(tar_path), "size_bytes": tar_path.stat().st_size}


def seal(name: str, results_root: Path, *, role: str, code_commit: str, note: str,
         extra: Mapping[str, Any] | None = None) -> Path:
    """Mark a registered campaign read-only. Sealing is permanent."""
    current = role_of(name, results_root)
    if current != role:
        raise CampaignError(f"campaign {name!r} is registered as {current!r}, not {role!r}")
    p = seal_path(name, results_root)
    if p.exists():
        raise CampaignError(f"campaign {name!r} is already sealed")
    record = {"campaign": name, "role": role, "sealed_utc": utc_now(), "code_commit": code_commit, "note": note,
              **dict(extra or {})}
    write_immutable_text(p, json.dumps(record, indent=2, sort_keys=True) + "\n")
    return p
