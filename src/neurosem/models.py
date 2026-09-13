"""Reference-model manifest and model workspaces.

A *workspace* is a private, writable copy of a model snapshot (``models/raw/<snapshot>``).
References, mutants and valid transformations are all workspaces; nothing ever edits
``models/raw`` in place.
"""

from __future__ import annotations

import csv
import dataclasses as dc
import shutil
from pathlib import Path

from neurosem.provenance import REPO_ROOT, tree_sha256
from neurosem.schemas import ModelRecord

MODEL_MANIFEST = REPO_ROOT / "data" / "model_manifest.csv"
RAW_MODELS = REPO_ROOT / "models" / "raw"
MANIFEST_COLUMNS = [f.name for f in dc.fields(ModelRecord)]


def load_models(path: Path = MODEL_MANIFEST, include_only: bool = False) -> dict[str, ModelRecord]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames or []
    missing = set(MANIFEST_COLUMNS) - set(header)
    if missing:
        raise ValueError(f"model manifest missing columns: {sorted(missing)}")
    ids = [r["model_id"] for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise ValueError(f"duplicate model_id in manifest: {dup}")
    models = {r["model_id"]: ModelRecord(**{k: r[k] for k in MANIFEST_COLUMNS}) for r in rows}
    if include_only:
        models = {k: m for k, m in models.items() if m.inclusion == "include"}
    return models


def write_models(models: list[ModelRecord], path: Path = MODEL_MANIFEST) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS, lineterminator="\n")
        w.writeheader()
        for m in models:
            w.writerow(dc.asdict(m))


def snapshot_dir(model: ModelRecord) -> Path:
    return RAW_MODELS / model.snapshot


@dc.dataclass(frozen=True)
class Workspace:
    root: Path
    model: ModelRecord

    @property
    def cell_path(self) -> Path:
        return self.root / self.model.cell_file

    @property
    def harness_path(self) -> Path:
        return self.root / self.model.harness_lems

    def path(self, rel: str) -> Path:
        return self.root / rel

    def tree_sha256(self) -> str:
        return tree_sha256(self.root)


def materialize(model: ModelRecord, dest: Path, overwrite: bool = False) -> Workspace:
    """Copy the pristine snapshot of ``model`` to ``dest``."""
    src = snapshot_dir(model)
    if not src.is_dir():
        raise FileNotFoundError(f"snapshot not found: {src} (run scripts/fetch_models.py)")
    if dest.exists():
        if not overwrite:
            raise FileExistsError(dest)
        _rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("PROVENANCE.json"))
    for p in dest.rglob("*"):          # snapshots may be read-only; workspaces are writable
        if p.is_file():
            p.chmod(0o644)
    return Workspace(dest, model)


def copy_workspace(ws: Workspace, dest: Path, overwrite: bool = False) -> Workspace:
    if dest.exists():
        if not overwrite:
            raise FileExistsError(dest)
        _rmtree(dest)
    shutil.copytree(ws.root, dest)
    return Workspace(dest, ws.model)


def _rmtree(path: Path) -> None:
    def onerror(func, p, _exc):  # read-only files on Windows
        Path(p).chmod(0o644)
        func(p)

    shutil.rmtree(path, onexc=onerror)
