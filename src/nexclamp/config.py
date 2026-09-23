"""Configuration loading. Every config file is hashed so runs can record exactly what they used."""

from __future__ import annotations

import dataclasses as dc
import os
from pathlib import Path
from typing import Any

import yaml

from nexclamp.provenance import REPO_ROOT, env_var, sha256_file, sha256_json
from nexclamp.schemas import ExecConfig

CONFIG_DIR = REPO_ROOT / "configs"
# A development campaign (for example a bounded pilot iteration) may load a complete set of
# config files from another directory. The held-out evaluation refuses any override, because
# configs/FROZEN.lock covers configs/ only.
CONFIG_DIR_ENV = "NEXCLAMP_CONFIG_DIR"
# The project was renamed twice (neurosem -> neuraxis -> nexclamp); both old names keep working so
# recorded commands and historical scripts still run.
LEGACY_CONFIG_DIR_ENVS = ("NEURAXIS_CONFIG_DIR", "NEUROSEM_CONFIG_DIR")


def config_dir() -> Path:
    value = os.environ.get(CONFIG_DIR_ENV) or next(
        (os.environ[k] for k in LEGACY_CONFIG_DIR_ENVS if os.environ.get(k)), None)
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


STUDY_CONFIG_ENV = "NEXCLAMP_STUDY_CONFIG"     # a single frozen study file, e.g. configs/pilot2_frozen.yaml


def study_config_path() -> Path:
    """The study configuration in use: ``NEXCLAMP_STUDY_CONFIG`` if set, else ``<config dir>/study.yaml``."""
    override = env_var("STUDY_CONFIG")
    if not override:
        return config_dir() / "study.yaml"
    p = Path(override)
    return p if p.is_absolute() else REPO_ROOT / p


def uses_default_study_config() -> bool:
    return study_config_path().resolve() == (CONFIG_DIR / "study.yaml").resolve()


def study() -> LoadedConfig:
    return load_yaml(study_config_path())


def features() -> LoadedConfig:
    return load_yaml(config_dir() / "features.yaml")


def tolerances() -> LoadedConfig:
    return load_yaml(config_dir() / "tolerances.yaml")


def agent_policy() -> LoadedConfig:
    return load_yaml(config_dir() / "agent_policy.yaml")


STUDY_METADATA_KEYS = ("study_id", "project_name", "study_phase", "protocol_version", "designation")


def study_metadata(cfg: LoadedConfig | None = None) -> dict[str, str]:
    """Labels stamped on every run record, table, report and figure (``study_metadata`` in study.yaml)."""
    cfg = cfg or study()
    m = cfg.get("study_metadata") or {}
    return {k: str(m[k]) for k in STUDY_METADATA_KEYS if m.get(k) not in (None, "")}


def designation_text(cfg: LoadedConfig | None = None) -> str:
    return " | ".join(f"{k}: {v}" for k, v in study_metadata(cfg).items())


def config_set_sha256() -> str:
    """One hash for the study, feature and tolerance config files currently in use."""
    return sha256_json({c.path.name: c.sha256 for c in (study(), features(), tolerances())})


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
