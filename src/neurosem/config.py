"""Configuration loading. Every config file is hashed so runs can record exactly what they used."""

from __future__ import annotations

import dataclasses as dc
import os
from pathlib import Path
from typing import Any

import yaml

from neurosem.provenance import REPO_ROOT, sha256_file
from neurosem.schemas import ExecConfig

CONFIG_DIR = REPO_ROOT / "configs"
# A development campaign (for example a bounded pilot iteration) may load a complete set of
# config files from another directory. The held-out evaluation refuses any override, because
# configs/FROZEN.lock covers configs/ only.
CONFIG_DIR_ENV = "NEUROSEM_CONFIG_DIR"


def config_dir() -> Path:
    value = os.environ.get(CONFIG_DIR_ENV)
    if not value:
        return CONFIG_DIR
    p = Path(value)
    return p if p.is_absolute() else REPO_ROOT / p


def uses_default_config_dir() -> bool:
    return config_dir().resolve() == CONFIG_DIR.resolve()


@dc.dataclass(frozen=True)
class LoadedConfig:
    path: Path
    sha256: str
    data: dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)


def load_yaml(path: Path | str) -> LoadedConfig:
    p = Path(path)
    if not p.is_absolute():
        p = config_dir() / p
    with open(p, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return LoadedConfig(p, sha256_file(p), data)


def study() -> LoadedConfig:
    return load_yaml(config_dir() / "study.yaml")


def features() -> LoadedConfig:
    return load_yaml(config_dir() / "features.yaml")


def tolerances() -> LoadedConfig:
    return load_yaml(config_dir() / "tolerances.yaml")


def agent_policy() -> LoadedConfig:
    return load_yaml(config_dir() / "agent_policy.yaml")


def nominal_exec(cfg: LoadedConfig | None = None) -> ExecConfig:
    cfg = cfg or study()
    return ExecConfig(dt_ms=float(cfg["numerics"]["dt_nominal_ms"]))


def refinement_levels(cfg: LoadedConfig | None = None) -> list[float]:
    cfg = cfg or study()
    h = float(cfg["numerics"]["dt_nominal_ms"])
    return [h / f for f in cfg["numerics"]["refinement_factors"]]


def work_dir(cfg: LoadedConfig | None = None) -> Path:
    cfg = cfg or study()
    return REPO_ROOT / cfg["paths"]["work"]


def results_dir(cfg: LoadedConfig | None = None) -> Path:
    cfg = cfg or study()
    return REPO_ROOT / cfg["paths"]["results"]
