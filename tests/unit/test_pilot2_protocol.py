"""The written Pilot 2 protocol, its frozen configuration and the fixed matrix must agree.

`docs/PILOT2_PROTOCOL.md` is the prespecification. Nothing in Pilot 2 may be executed under settings
that differ from it, and the counts it reports must be the counts in `manifests/PILOT2_*.csv`.
"""

from __future__ import annotations

import csv
import re
from collections import Counter

import pytest
import yaml

from nexclamp import config
from nexclamp.experiments import strata
from nexclamp.experiments.pilot_v2_outputs import BRANCH_RULES
from nexclamp.provenance import REPO_ROOT

PROTOCOL = REPO_ROOT / "docs" / "PILOT2_PROTOCOL.md"
CONFIG = REPO_ROOT / "configs" / "pilot2_frozen.yaml"
MANIFESTS = REPO_ROOT / "manifests"


@pytest.fixture(scope="module")
def written():
    text = PROTOCOL.read_text(encoding="utf-8")
    m = re.search(r"<!-- executable-settings -->\s*```yaml\n(.*?)```", text, re.DOTALL)
    assert m, "protocol lacks the executable-settings block"
    return yaml.safe_load(m.group(1))


@pytest.fixture(scope="module")
def study():
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def rows(name: str) -> list[dict]:
    path = MANIFESTS / name
    if not path.is_file():
        pytest.skip(f"{name} not prepared yet (scripts/pilot2_prepare.py)")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_metadata_is_exploratory_development_data(written, study):
    assert written["study_metadata"] == study["study_metadata"]
    meta = study["study_metadata"]
    assert meta["study_id"] == "neuron_model_behavioral_validation"
    assert meta["study_phase"] == "development_pilot"
    assert meta["protocol_version"] == "PILOT2_PROTOCOL"
    assert "not independent confirmation" in meta["designation"]
    assert "never pooled" in meta["designation"]


def test_models_are_five_new_models_and_never_the_pilot1_models(written, study):
    for key in ("models", "new_models", "repeated_models"):
        assert written[key] == study["pilot"][key], key
    models = study["pilot"]["models"]
    assert 4 <= len(models) <= 6                       # Neel's Pilot 2 scope
    assert set(models) == set(study["pilot"]["new_models"])
    assert not study["pilot"]["repeated_models"]
    assert not set(models) & {"pospischil2008_rs", "pospischil2008_lts"}   # Pilot 1 models
    assert "wangbuzsaki1996_wb" not in models                              # D-051


def test_mutation_settings_and_seed_agree(written, study):
    for key in ("mutation_families", "exclude_operators", "mutants_per_operator", "transforms_per_operator",
                "severity_levels", "sites_per_severity", "sites_without_severity"):
        assert written[key] == study["pilot"][key], key
    assert written["seed"] == study["selection"]["seed"] == study["analysis"]["seed"]
    assert study["pilot"]["severity_levels"] == ["mild", "strong"]         # two prespecified severities


def test_numerics_rheobase_canonical_levels_and_protocols_agree(written, study):
    for k, v in written["numerics"].items():
        assert study["numerics"][k] == v, k
    assert written["rheobase"] == study["rheobase"]
    assert written["canonical"] == study["canonical"]
    assert written["validation_levels"] == study["validation_levels"] == {"enabled": True}
    assert written["protocols"] == study["protocols"]
    assert 6 <= len(study["protocols"]) <= 10                              # prespecified protocol count


def test_primary_panel_is_eight_features_and_secondary_completes_eighteen(written):
    prim = set(written["canonical"]["features"])
    sec = set(written["canonical"]["secondary_features"])
    for p in written["protocols"]:
        prim |= set(p.get("features", []))
        sec |= set(p.get("secondary_features", []))
    prim |= {"rheobase"}                                                   # P03 default feature
    assert len(prim) == 8 and not prim & sec and len(prim | sec) == 18


def test_branch_rules_in_the_protocol_are_the_rules_in_code(written):
    assert written["branch_rules"] == BRANCH_RULES


def test_written_dependency_versions_match_the_lock_file(written):
    lock = {}
    for line in (REPO_ROOT / "requirements.lock").read_text(encoding="utf-8").splitlines():
        if "==" in line and not line.startswith("#"):
            name, ver = line.split("==", 1)
            lock[name.strip().lower()] = ver.split()[0].strip()
    for name, ver in written["dependencies"].items():
        assert lock.get(name.lower()) == str(ver), name


def test_the_config_loads_through_the_study_override(monkeypatch, written):
    monkeypatch.setenv(config.STUDY_CONFIG_ENV, "configs/pilot2_frozen.yaml")
    assert config.study_metadata() == {k: str(v) for k, v in written["study_metadata"].items()}
    assert not config.uses_default_study_config()


def test_the_prepared_matrix_matches_the_frozen_models_and_families(study):
    models = rows("PILOT2_MODELS.csv")
    assert [m["model_id"] for m in models] == study["pilot"]["models"]
    assert all(m["curation_decision"].startswith("include") for m in models), \
        [m["curation_decision"] for m in models]
    assert len({m["source_family"] for m in models}) == len(models)        # one model per source paper
    assert all(m["license"] for m in models)                              # licence recorded for every model

    variants = rows("PILOT2_VARIANTS.csv")
    semantic = [v for v in variants if v["stratum"] == strata.SEMANTIC]
    per_model = Counter(v["model_id"] for v in semantic)
    assert set(per_model) == set(study["pilot"]["models"])
    for mid, n in per_model.items():
        assert 15 <= n <= 25, (mid, n)                                     # 15-25 mutants per model
    controls = Counter(v["model_id"] for v in variants if v["stratum"] == strata.CONTROL)
    for mid in study["pilot"]["models"]:
        assert controls[mid] >= 5, (mid, controls[mid])                    # at least five valid transformations
    families = {v["analysis_family"] for v in semantic}
    assert 4 <= len(families) <= 6, sorted(families)                       # 4-6 mutation families
    assert "numerical_robustness" not in families                          # numerics never in the primary stratum
    assert {v["severity"] for v in semantic} >= {"mild", "strong"}


def test_no_excluded_operator_appears_in_the_prepared_matrix(study):
    used = {v["operator"] for v in rows("PILOT2_VARIANTS.csv")}
    assert not used & set(study["pilot"]["exclude_operators"])


def test_every_matrix_row_names_a_planned_variant_and_refinement_level(study):
    variants = {v["variant_id"] for v in rows("PILOT2_VARIANTS.csv")}
    matrix = rows("PILOT2_EXPERIMENT_MATRIX.csv")
    assert variants and {r["variant_id"] for r in matrix} == variants
    assert {r["refinement_level"] for r in matrix} == {"h", "h/2", "h/4"}
    planned = {r["protocol_id"] for r in matrix}
    assert planned == {"P00_canonical", *[p["protocol_id"] for p in study["protocols"]]}


def test_pre_run_manifest_hashes_the_protocol_config_and_matrix():
    path = MANIFESTS / "PILOT2_PRE_RUN.sha256"
    if not path.is_file():
        pytest.skip("pre-run manifest not prepared yet")
    text = path.read_text(encoding="utf-8")
    for needed in ("docs/PILOT2_PROTOCOL.md", "configs/pilot2_frozen.yaml", "manifests/PILOT2_MODELS.csv",
                   "manifests/PILOT2_VARIANTS.csv", "manifests/PILOT2_EXPERIMENT_MATRIX.csv",
                   "configs/features.yaml", "configs/tolerances.yaml", "requirements.lock"):
        assert needed in text, needed
