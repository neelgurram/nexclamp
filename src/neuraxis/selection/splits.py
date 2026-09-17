"""Discovery / held-out splits: split files, their hashes, and the single gate to held-out labels.

The study's generalisation claims are only as good as the barrier between the data used
to select protocols (discovery) and the data used to evaluate them (held-out models and
at least one held-out mutation family). The barrier here is structural:

* discovery code reads only ``data/splits/discovery_*.txt`` through :func:`discovery_view`,
  which never opens anything in the held-out directory (tests enforce this by making
  every open of that directory fail);
* split files are frozen by SHA-256 (``data/splits/SPLITS.sha256``, written by
  :func:`freeze_splits`), and a frozen split is never silently overwritten;
* held-out labels are read only by :class:`HeldoutGate`, which refuses unless the study
  configuration is frozen (``configs/FROZEN.lock`` whose hashes match the current files)
  and appends every access to ``results/heldout_access.log``.

Hash files use the ``sha256sum`` text format: ``<64 hex>  <path relative to the repository root>``.
"""

from __future__ import annotations

import csv
import dataclasses as dc
import json
import re
from collections.abc import Iterable, Mapping
from pathlib import Path, PurePosixPath
from typing import Any

import numpy as np

from neuraxis.provenance import git_state, relpath, sha256_bytes, sha256_file, utc_now
from neuraxis.schemas import MutationFamily
from neuraxis.selection.matrix import DetectionMatrix

SPLITS_DIR = "data/splits"
DISCOVERY_MODELS_FILE = "data/splits/discovery_models.txt"
DISCOVERY_FAMILIES_FILE = "data/splits/discovery_families.txt"
DISCOVERY_FILES = (DISCOVERY_MODELS_FILE, DISCOVERY_FAMILIES_FILE)
SPLITS_HASH_FILE = "data/splits/SPLITS.sha256"
FROZEN_LOCK_FILE = "configs/FROZEN.lock"
STUDY_CONFIG_FILE = "configs/study.yaml"
MODEL_MANIFEST_FILE = "data/model_manifest.csv"
FAMILIES = tuple(f.value for f in MutationFamily)

HELDOUT_DIR = "data/splits/heldout"
HELDOUT_MODELS_FILE = f"{HELDOUT_DIR}/heldout_models.txt"
HELDOUT_FAMILIES_FILE = f"{HELDOUT_DIR}/heldout_families.txt"
REQUIRED_SPLIT_FILES = (*DISCOVERY_FILES, HELDOUT_MODELS_FILE, HELDOUT_FAMILIES_FILE)
ACCESS_LOG_FILE = "results/heldout_access.log"

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class LeakageError(RuntimeError):
    """Data that must not reach discovery-side code (or an unverifiable split) was encountered."""


class SplitIntegrityError(LeakageError):
    """Split or configuration files do not match their recorded hashes, or are not frozen."""


class FrozenSplitError(SplitIntegrityError):
    """Refusal to overwrite an existing, different split freeze without a logged reason."""


# ---------------------------------------------------------------------- plain file formats
def read_id_list(path: Path) -> tuple[str, ...]:
    """One identifier per line, in file order. Blank lines and ``#`` comments are ignored.

    A UTF-8 byte-order mark is rejected: it would silently become part of the first id,
    and the resulting mismatch would surface later as a misleading leakage error.
    """
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: UTF-8 byte-order mark not allowed (save as UTF-8 without BOM)")
    ids: list[str] = []
    for n, line in enumerate(text.splitlines(), start=1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if re.search(r"[\s,]", s):
            raise ValueError(f"{path}:{n}: identifier {s!r} contains whitespace or a comma")
        if s in ids:
            raise ValueError(f"{path}:{n}: duplicate identifier {s!r}")
        ids.append(s)
    return tuple(ids)


def parse_hash_manifest(text: str, source: str = "<manifest>") -> dict[str, str]:
    """Parse ``sha256sum``-format lines into ``{relative posix path: sha256}``."""
    out: dict[str, str] = {}
    for n, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            raise SplitIntegrityError(f"{source}:{n}: malformed line {line!r}")
        digest, rel = parts[0].lower(), parts[1].lstrip("*").strip()
        pp = PurePosixPath(rel)
        if not _HEX64.match(digest) or "\\" in rel or pp.is_absolute() or ".." in pp.parts or re.match(r"^[A-Za-z]:", rel):
            raise SplitIntegrityError(f"{source}:{n}: invalid hash or non-relative path in {line!r}")
        if rel in out:
            raise SplitIntegrityError(f"{source}:{n}: duplicate entry for {rel}")
        out[rel] = digest
    return out


def format_hash_manifest(root: Path, relpaths: Iterable[str]) -> str:
    """``sha256sum``-format text for ``relpaths`` (relative to ``root``), sorted by path."""
    return "".join(f"{sha256_file(Path(root) / rel)}  {rel}\n" for rel in sorted(set(relpaths)))


def _verify_entries(root: Path, entries: Mapping[str, str], source: str) -> None:
    problems = []
    for rel, digest in sorted(entries.items()):
        p = Path(root) / rel
        if not p.is_file():
            problems.append(f"missing: {rel}")
        elif sha256_file(p) != digest:
            problems.append(f"changed since freeze: {rel}")
    if problems:
        raise SplitIntegrityError(f"{source} does not match the current files: " + "; ".join(problems))


def _list_split_files(root: Path) -> list[str]:
    base = Path(root) / SPLITS_DIR
    return sorted(p.relative_to(root).as_posix() for p in base.rglob("*.txt") if p.is_file())


def verify_split_hashes(root: Path, scope: str = "all") -> None:
    """Check split files against ``data/splits/SPLITS.sha256``.

    ``scope="all"`` verifies every recorded file and that no unrecorded ``*.txt`` split
    file exists. ``scope="discovery"`` verifies only the discovery files, and opens
    nothing else, so discovery-side code can check integrity without touching held-out data.
    """
    if scope not in ("all", "discovery"):
        raise ValueError("scope must be 'all' or 'discovery'")
    root = Path(root)
    manifest = root / SPLITS_HASH_FILE
    if not manifest.is_file():
        raise SplitIntegrityError(f"{SPLITS_HASH_FILE} not found: splits are not frozen (scripts/freeze_splits.py)")
    entries = parse_hash_manifest(manifest.read_text(encoding="utf-8"), SPLITS_HASH_FILE)
    unlisted_discovery = [f for f in DISCOVERY_FILES if f not in entries]
    if unlisted_discovery:
        raise SplitIntegrityError(f"{SPLITS_HASH_FILE} does not record {unlisted_discovery}")
    if scope == "discovery":
        _verify_entries(root, {f: entries[f] for f in DISCOVERY_FILES}, SPLITS_HASH_FILE)
        return
    _verify_entries(root, entries, SPLITS_HASH_FILE)
    unlisted = [f for f in _list_split_files(root) if f not in entries]
    if unlisted:
        raise SplitIntegrityError(f"split files not recorded in {SPLITS_HASH_FILE}: {unlisted}")


# ---------------------------------------------------------------------- discovery side
@dc.dataclass(frozen=True)
class DiscoveryView:
    """Everything protocol selection may know about the split.

    ``excluded_families`` are the mutation families not listed as discovery families; they
    are derived from the known family names, not from any held-out file. When only the
    contract fields (``models``, ``excluded_families``) are given, ``families`` is derived
    as the known families minus the excluded ones, so such a view is usable.
    """

    models: tuple[str, ...]
    excluded_families: tuple[str, ...]
    families: tuple[str, ...] = ()
    frozen: bool = False
    file_sha256: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        models, excluded, families = tuple(self.models), tuple(self.excluded_families), tuple(self.families)
        unknown = [f for f in (*excluded, *families) if f not in FAMILIES]
        if unknown:
            raise ValueError(f"unknown mutation families {unknown}; known: {list(FAMILIES)}")
        if not families:
            families = tuple(f for f in FAMILIES if f not in excluded)
        overlap = sorted(set(families) & set(excluded))
        if overlap:
            raise ValueError(f"families {overlap} are both discovery and excluded")
        object.__setattr__(self, "models", models)
        object.__setattr__(self, "excluded_families", excluded)
        object.__setattr__(self, "families", families)

    def is_discovery(self, model_id: str, family: str) -> bool:
        return model_id in self.models and family in self.families

    def discovery_mask(self, m: DetectionMatrix) -> np.ndarray:
        return np.array([self.is_discovery(m.model_of[i], m.family_of[i]) for i in m.mutant_ids], dtype=bool)

    def filter_matrix(self, m: DetectionMatrix) -> DetectionMatrix:
        """Return a copy of ``m`` after proving every row is a discovery row.

        A non-discovery row is an error, not something to drop quietly: it means an
        upstream step built a selection artefact from data selection must not see.
        """
        bad = [i for i in m.mutant_ids if not self.is_discovery(m.model_of[i], m.family_of[i])]
        if bad:
            detail = ", ".join(f"{i} (model={m.model_of[i]}, family={m.family_of[i]})" for i in bad[:5])
            raise LeakageError(f"{len(bad)} of {m.n_mutants} matrix rows are not discovery rows: {detail}")
        return m.take_rows(None)


def discovery_view(root: Path, require_frozen: bool = False) -> DiscoveryView:
    """Load the discovery split from ``data/splits/discovery_*.txt`` only.

    If the splits are frozen, the discovery files are verified against their recorded
    hashes (discovery scope). ``require_frozen=True`` refuses provisional splits, which is
    what the frozen study must use.
    """
    root = Path(root)
    frozen = (root / SPLITS_HASH_FILE).is_file()
    if frozen:
        verify_split_hashes(root, scope="discovery")
    elif require_frozen:
        raise SplitIntegrityError(f"{SPLITS_HASH_FILE} not found: discovery split is provisional")
    models = read_id_list(root / DISCOVERY_MODELS_FILE)
    families = read_id_list(root / DISCOVERY_FAMILIES_FILE)
    if not models or not families:
        raise ValueError("discovery split must list at least one model and one mutation family")
    unknown = [f for f in families if f not in FAMILIES]
    if unknown:
        raise ValueError(f"unknown mutation families {unknown}; known: {list(FAMILIES)}")
    excluded = tuple(f for f in FAMILIES if f not in families)
    hashes = tuple((rel, sha256_file(root / rel)) for rel in DISCOVERY_FILES)
    return DiscoveryView(models, excluded, families, frozen, hashes)


# ---------------------------------------------------------------------- held-out side
@dc.dataclass(frozen=True)
class Split:
    discovery_models: tuple[str, ...]
    heldout_models: tuple[str, ...]
    heldout_families: tuple[str, ...]
    discovery_families: tuple[str, ...] = ()


def _read_split(root: Path) -> Split:
    root = Path(root)
    split = Split(read_id_list(root / DISCOVERY_MODELS_FILE), read_id_list(root / HELDOUT_MODELS_FILE),
                  read_id_list(root / HELDOUT_FAMILIES_FILE), read_id_list(root / DISCOVERY_FAMILIES_FILE))
    for name in ("discovery_models", "heldout_models", "heldout_families", "discovery_families"):
        if not getattr(split, name):
            raise ValueError(f"split list {name} is empty")
    unknown = [f for f in (*split.heldout_families, *split.discovery_families) if f not in FAMILIES]
    if unknown:
        raise ValueError(f"unknown mutation families {unknown}; known: {list(FAMILIES)}")
    shared_models = sorted(set(split.discovery_models) & set(split.heldout_models))
    shared_families = sorted(set(split.discovery_families) & set(split.heldout_families))
    if shared_models or shared_families:
        raise LeakageError(f"discovery and held-out splits overlap: models {shared_models}, families {shared_families}")
    return split


def _require_frozen_split_files(entries: Mapping[str, str]) -> None:
    missing = [f for f in REQUIRED_SPLIT_FILES if f not in entries]
    if missing:
        raise SplitIntegrityError(f"{SPLITS_HASH_FILE} does not record required split files {missing}")


def _append_log(root: Path, record: Mapping[str, Any]) -> None:
    log = Path(root) / ACCESS_LOG_FILE
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def read_access_log(root: Path) -> list[dict[str, Any]]:
    """Records of ``results/heldout_access.log`` (JSON lines), oldest first."""
    log = Path(root) / ACCESS_LOG_FILE
    if not log.is_file():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]


class HeldoutGate:
    """The only reader of held-out split files.

    Opening the gate requires (1) a non-empty reason, (2) ``frozen_lock`` to be exactly
    ``<root>/configs/FROZEN.lock`` (the committed study lock is the only freeze marker; a
    lock written anywhere else, even with matching hashes, is refused), recording
    ``data/splits/SPLITS.sha256``, ``configs/study.yaml`` (which must exist) and every other
    ``configs/*.yaml`` with hashes equal to the current files, and (3) split files equal to
    ``SPLITS.sha256``. A successful opening appends a JSON line (timestamp, reason, git
    commit, lock and split hashes) to ``results/heldout_access.log``.

    ``frozen_lock`` stays a parameter for contract compatibility; a relative path is
    resolved against ``root``.
    """

    def __init__(self, root: Path, frozen_lock: Path, reason: str) -> None:
        self.root = Path(root)
        lock = Path(frozen_lock)
        self.frozen_lock = lock if lock.is_absolute() else self.root / lock
        self.reason = (reason or "").strip()
        if not self.reason:
            raise LeakageError("held-out access requires a non-empty reason; every access is logged")
        expected = self.root / FROZEN_LOCK_FILE
        if self.frozen_lock.resolve() != expected.resolve():
            raise SplitIntegrityError(f"held-out access requires the study lock {FROZEN_LOCK_FILE} under the "
                                      f"repository root; refusing lock file {self.frozen_lock}")
        self.frozen_lock = expected
        self._verify()
        commit, dirty = git_state(self.root)
        self.access_record: dict[str, Any] = {
            "event": "heldout_gate_opened",
            "timestamp_utc": utc_now(),
            "reason": self.reason,
            "git_commit": commit,
            "git_dirty": dirty,
            "frozen_lock": relpath(self.frozen_lock, self.root),
            "frozen_lock_sha256": sha256_file(self.frozen_lock),
            "splits_sha256": sha256_file(self.root / SPLITS_HASH_FILE),
        }
        _append_log(self.root, self.access_record)

    def _required_lock_entries(self) -> set[str]:
        configs = self.root / "configs"
        yamls = sorted(p for p in configs.glob("*.y*ml") if p.suffix in (".yaml", ".yml")) if configs.is_dir() else []
        return {SPLITS_HASH_FILE, STUDY_CONFIG_FILE, *(f"configs/{p.name}" for p in yamls)}

    def _verify(self) -> None:
        if not self.frozen_lock.is_file():
            raise SplitIntegrityError(f"{self.frozen_lock} not found: held-out data stay sealed until the study "
                                      "configuration is frozen")
        entries = parse_hash_manifest(self.frozen_lock.read_text(encoding="utf-8"), str(self.frozen_lock))
        missing = sorted(self._required_lock_entries() - set(entries))
        if missing:
            raise SplitIntegrityError(f"{self.frozen_lock} does not record {missing}")
        _verify_entries(self.root, entries, str(self.frozen_lock))
        split_entries = parse_hash_manifest((self.root / SPLITS_HASH_FILE).read_text(encoding="utf-8"),
                                            SPLITS_HASH_FILE)
        _require_frozen_split_files(split_entries)
        verify_split_hashes(self.root, scope="all")

    def split(self) -> Split:
        """Re-verify all hashes, then read the full split."""
        self._verify()
        return _read_split(self.root)


# ---------------------------------------------------------------------- freezing
@dc.dataclass
class FreezeResult:
    status: str                         # frozen | refrozen | unchanged
    manifest: Path
    entries: dict[str, str]
    warnings: list[str]
    log_record: dict[str, Any] | None


def _manifest_checks(root: Path, split: Split) -> list[str]:
    """Model ids must exist in the model manifest; correlated or excluded models give warnings."""
    path = Path(root) / MODEL_MANIFEST_FILE
    if not path.is_file():
        raise FileNotFoundError(f"{MODEL_MANIFEST_FILE} not found; split model ids cannot be checked")
    with open(path, newline="", encoding="utf-8") as f:
        rows = {r["model_id"]: r for r in csv.DictReader(f)}
    all_models = (*split.discovery_models, *split.heldout_models)
    unknown = [m for m in all_models if m not in rows]
    if unknown:
        raise ValueError(f"split models not in {MODEL_MANIFEST_FILE}: {unknown}")
    warnings = [f"model {m} has inclusion={rows[m].get('inclusion')!r}" for m in all_models
                if rows[m].get("inclusion", "include") != "include"]
    disc_sources = {rows[m].get("source_family", "") for m in split.discovery_models} - {""}
    for m in split.heldout_models:
        src = rows[m].get("source_family", "")
        if src in disc_sources:
            warnings.append(f"held-out model {m} shares source_family {src!r} with a discovery model; "
                            "its behaviour is correlated with discovery data")
    return warnings


def freeze_splits(root: Path, force_reason: str | None = None) -> FreezeResult:
    """Validate the split files and record their hashes in ``data/splits/SPLITS.sha256``.

    Validation: all four split files exist and are non-empty, families are known, the
    discovery and held-out lists are disjoint, and every model is in the model manifest.
    An existing freeze with identical content is left untouched. A different existing
    freeze is overwritten only with ``force_reason``; both the first freeze and any forced
    re-freeze are appended to ``results/heldout_access.log``.
    """
    root = Path(root)
    missing = [f for f in REQUIRED_SPLIT_FILES if not (root / f).is_file()]
    if missing:
        raise FileNotFoundError(f"cannot freeze: missing split files {missing} (see {HELDOUT_DIR}/README.md)")
    split = _read_split(root)
    warnings = _manifest_checks(root, split)
    text = format_hash_manifest(root, _list_split_files(root))
    entries = parse_hash_manifest(text, SPLITS_HASH_FILE)
    manifest = root / SPLITS_HASH_FILE
    previous = None
    if manifest.is_file():
        old = manifest.read_bytes()
        if old == text.encode("utf-8"):
            return FreezeResult("unchanged", manifest, entries, warnings, None)
        if not (force_reason or "").strip():
            raise FrozenSplitError(f"{SPLITS_HASH_FILE} already freezes different split files; refusing to "
                                   "overwrite without --force-with-reason")
        previous = sha256_bytes(old)
        accesses = sum(1 for r in read_access_log(root) if r.get("event") == "heldout_gate_opened")
        if accesses:
            warnings.append(f"held-out data were accessed {accesses} time(s) before this re-freeze; "
                            "the re-freeze must be disclosed")
        if (root / FROZEN_LOCK_FILE).is_file():
            warnings.append(f"{FROZEN_LOCK_FILE} records the previous split hashes; HeldoutGate will refuse "
                            "until the lock is regenerated")
        status, event, reason = "refrozen", "splits_refrozen", force_reason.strip()
    else:
        status, event = "frozen", "splits_frozen"
        reason = (force_reason or "").strip() or "initial freeze"
    manifest.write_bytes(text.encode("utf-8"))
    commit, dirty = git_state(root)
    record = {
        "event": event,
        "timestamp_utc": utc_now(),
        "reason": reason,
        "git_commit": commit,
        "git_dirty": dirty,
        "splits_sha256": sha256_file(manifest),
        "previous_splits_sha256": previous,
        "files": entries,
    }
    _append_log(root, record)
    return FreezeResult(status, manifest, entries, warnings, record)
