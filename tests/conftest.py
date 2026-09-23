"""Shared pytest fixtures. Tests marked ``jnml`` are skipped when Java/jNeuroML is unavailable."""

from __future__ import annotations

from pathlib import Path

import pytest

from nexclamp.models import load_models, materialize
from nexclamp.simulators.jneuroml import JNeuroML

REPO_ROOT = Path(__file__).resolve().parents[1]


def pytest_collection_modifyitems(config, items):
    if JNeuroML().available():
        return
    skip = pytest.mark.skip(reason="Java or jNeuroML jar not available")
    for item in items:
        if "jnml" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def sim() -> JNeuroML:
    s = JNeuroML()
    if not s.available():
        pytest.skip("Java or jNeuroML jar not available")
    return s


@pytest.fixture(scope="session")
def models():
    return load_models()


@pytest.fixture
def rs_ws(tmp_path, models):
    return materialize(models["pospischil2008_rs"], tmp_path / "rs")


@pytest.fixture
def lts_ws(tmp_path, models):
    return materialize(models["pospischil2008_lts"], tmp_path / "lts")


@pytest.fixture
def hh_ws(tmp_path, models):
    return materialize(models["nml2_hh_example"], tmp_path / "hh")
