"""Manifest fields that reach generated simulation files must be machine-readable (X-19).

Curation sweeps recorded notes inside `temperature` and `harness_v_column`. Written verbatim into a
generated LEMS file, they broke every rheobase search for the affected models. Both readers now
normalise through one function, and the shipped manifest must already be clean.
"""

from __future__ import annotations

import re

from neuraxis.models import load_models, normalise_fields
from neuraxis.orchestration.curation import read_candidates
from neuraxis.provenance import REPO_ROOT

TEMPERATURE = re.compile(r"^$|^[-+]?\d+(\.\d+)? degC$")
PILOT2_MODELS = ("acnet2_pyr_soma", "migliore2014_mt_soma", "nml2_hh_example", "osb_hh2_477127614",
                 "pospischil2008_fs")


def test_notes_are_stripped_from_the_fields_that_reach_generated_files():
    out = normalise_fields({"temperature": "34 degC (networkWithTemperature in network_477127614.net.nml)",
                            "harness_v_column": "7 (Pop0[6] at +170 pA; columns 1-7 are seven copies)"})
    assert out == {"temperature": "34 degC", "harness_v_column": "7"}
    assert normalise_fields({"temperature": "not specified (plain network element)"}) == {"temperature": ""}
    assert normalise_fields({"temperature": "", "harness_v_column": "1"}) == {"temperature": "", "harness_v_column": "1"}


def test_every_manifest_record_is_clean_after_loading():
    for mid, m in load_models().items():
        assert TEMPERATURE.match(m.temperature), (mid, m.temperature)
        assert m.harness_v_column.isdigit(), (mid, m.harness_v_column)


def test_candidate_sources_are_normalised_by_the_same_function():
    sources = [REPO_ROOT / "data" / n for n in ("model_candidates.csv", "model_candidates_sweep2.csv")]
    for m in read_candidates(sources):
        assert TEMPERATURE.match(m.temperature), (m.model_id, m.temperature)
        assert m.harness_v_column == "" or m.harness_v_column.isdigit(), (m.model_id, m.harness_v_column)


def test_the_pilot2_models_are_included_in_the_manifest():
    models = load_models()
    for mid in PILOT2_MODELS:
        assert mid in models, mid
        assert models[mid].inclusion == "include"
        assert "D-053" in models[mid].inclusion_reason
