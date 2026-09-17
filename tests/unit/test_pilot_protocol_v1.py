"""The written pilot protocol and its executable configuration must agree (PILOT_PROTOCOL_V1)."""

from __future__ import annotations

import re

import pytest
import yaml

from neuraxis import config
from neuraxis.provenance import REPO_ROOT

PROTOCOL = REPO_ROOT / "docs" / "PILOT_PROTOCOL_V1.md"
CONFIG_DIR = REPO_ROOT / "configs" / "pilot_protocol_v1"


@pytest.fixture(scope="module")
def written():
    text = PROTOCOL.read_text(encoding="utf-8")
    m = re.search(r"<!-- executable-settings -->\s*```yaml\n(.*?)```", text, re.DOTALL)
    assert m, "protocol lacks the executable-settings block"
    return yaml.safe_load(m.group(1))


@pytest.fixture(scope="module")
def study():
    return yaml.safe_load((CONFIG_DIR / "study.yaml").read_text(encoding="utf-8"))


def test_metadata_models_and_mutation_settings_agree(written, study):
    assert written["study_metadata"] == study["study_metadata"]
    assert written["study_metadata"]["project_name"] == "Neuraxis"
    assert written["study_metadata"]["study_phase"] == "development_pilot"
    for key in ("models", "repeated_models", "new_models", "mutation_families", "exclude_operators",
                "mutants_per_operator", "transforms_per_operator"):
        assert written[key] == study["pilot"][key], key
    assert set(written["repeated_models"]) | set(written["new_models"]) == set(written["models"])
    assert written["seed"] == study["selection"]["seed"]


def test_numerics_rheobase_canonical_and_protocols_agree(written, study):
    for k, v in written["numerics"].items():
        assert study["numerics"][k] == v, k
    assert written["rheobase"] == study["rheobase"]
    assert written["canonical"]["features"] == study["canonical"]["features"]
    assert written["canonical"]["secondary_features"] == study["canonical"]["secondary_features"]
    assert written["protocols"] == study["protocols"]


def test_config_directory_is_complete_and_shares_feature_and_tolerance_files(written):
    for name in ("study.yaml", "features.yaml", "tolerances.yaml", "agent_policy.yaml"):
        assert (CONFIG_DIR / name).is_file(), name
    for name in ("features.yaml", "tolerances.yaml"):
        assert (CONFIG_DIR / name).read_bytes() == (REPO_ROOT / "configs" / name).read_bytes(), name


def test_written_dependency_versions_match_the_lock_file(written):
    lock = {}
    for line in (REPO_ROOT / "requirements.lock").read_text(encoding="utf-8").splitlines():
        if "==" in line and not line.startswith("#"):
            name, ver = line.split("==", 1)
            lock[name.strip().lower()] = ver.split()[0].strip()
    for name, ver in written["dependencies"].items():
        assert lock.get(name.lower()) == str(ver), name


def test_primary_panel_is_eight_features_and_secondary_panel_completes_eighteen(written):
    prim = set(written["canonical"]["features"])
    sec = set(written["canonical"]["secondary_features"])
    for p in written["protocols"]:
        prim |= set(p.get("features", []))
        sec |= set(p.get("secondary_features", []))
    prim |= {"rheobase"}                     # P03 default feature
    assert len(prim) == 8 and not prim & sec and len(prim | sec) == 18


def test_protocol_config_loads_through_the_override(monkeypatch, written):
    monkeypatch.setenv(config.CONFIG_DIR_ENV, str(CONFIG_DIR))
    assert config.study_metadata() == {k: str(v) for k, v in written["study_metadata"].items()}
