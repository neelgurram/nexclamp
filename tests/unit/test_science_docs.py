"""Consistency tests for the science documentation (docs/*.md written by the science-docs module).

These do not judge prose. They check that the documents cover every item the
specification and ARCHITECTURE.md require, and that numbers copied from code (protocol
timings and costs) still match the code.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

from neurosem import config
from neurosem.protocols.definitions import CANONICAL_FEATURES, batched, templates_from_config
from neurosem.protocols.generate import group_by_length
from neurosem.protocols.rheobase import search

REPO = Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
DOC_NAMES = ("glossary.md", "model_selection.md", "protocol_catalog.md", "mutation_catalog.md",
             "statistical_plan.md", "ai_disclosure.md", "preregistration_draft.md", "neel_learning_guide.md")


def read(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", DOC_NAMES)
def test_doc_exists_and_has_title(name):
    text = read(name)
    assert text.startswith("# "), name
    assert len(text) > 2000, name


def test_glossary_covers_operational_definitions_and_required_terms():
    text = read("glossary.md").lower()
    required = ["reference model", "transformation", "valid transformation", "mutant",
                "admissible non-equivalent mutant", "canonical protocol", "perturbation fingerprint",
                "silent semantic drift", "empirical semantic certificate", "rheobase", "sag", "ahp",
                "forward euler", "tolerance", "detection matrix", "cluster bootstrap", "exact mcnemar"]
    for term in required:
        assert f"**{term}" in text, term


def _study():
    return config.study()


def test_protocol_catalog_mentions_every_template_and_feature():
    text = read("protocol_catalog.md")
    templates = templates_from_config(_study().get("protocols"))
    for t in templates:
        assert t.protocol_id in text, t.protocol_id
        for f in t.features:
            assert f in text, (t.protocol_id, f)
    for f in CANONICAL_FEATURES:
        assert f in text, f
    for t in templates:
        if not t.implemented:
            assert "deferred" in text.lower() and t.protocol_id in text


_ROW = re.compile(r"^\| (P\d{2}_[A-Za-z0-9_]+) \| [^|]+ \| (\d+)-(\d+) \| (\d+) \| ([\d,]+) \|\s*$")


def test_protocol_catalog_timing_table_matches_code():
    cfg = _study()
    settle = float(cfg["numerics"]["settle_ms"])
    dt = float(cfg["numerics"]["dt_nominal_ms"])
    rows = {}
    for line in read("protocol_catalog.md").splitlines():
        m = _ROW.match(line)
        if m:
            rows[m.group(1)] = tuple(int(m.group(i).replace(",", "")) for i in range(2, 6))
    expected_ids = [t.protocol_id for t in batched(templates_from_config(cfg.get("protocols")))]
    assert sorted(rows) == sorted(expected_ids)
    for t in batched(templates_from_config(cfg.get("protocols"))):
        p = t.instantiate(1.0, settle)
        start, end, total, steps = rows[t.protocol_id]
        assert (start, end) == (round(p.window.start_ms), round(p.window.end_ms)), t.protocol_id
        assert total == round(p.total_ms), t.protocol_id
        assert steps == round(p.total_ms / dt), t.protocol_id


def _section(text: str, start: str, stop: str) -> str:
    return text[text.index(start):text.index(stop)]


_COST_ROW = re.compile(r"^\| (P\d{2}(?:, P\d{2})*) \| ([\d,]+)(?: each)? \| (\d+) ms \|\s*$")


def _int(s: str) -> int:
    return int(s.replace(",", ""))


def test_protocol_catalog_cost_table_matches_code():
    cfg = _study()
    settle = float(cfg["numerics"]["settle_ms"])
    dt = float(cfg["numerics"]["dt_nominal_ms"])
    templates = templates_from_config(cfg.get("protocols"))
    by_short = {t.protocol_id[:3]: t for t in templates}
    section = _section(read("protocol_catalog.md"), "## 6. Cost measure", "## 7.")

    seen = set()
    for line in section.splitlines():
        m = _COST_ROW.match(line)
        if not m:
            continue
        for short in m.group(1).split(", "):
            p = by_short[short].instantiate(1.0, settle)
            assert _int(m.group(2)) == round(p.total_ms / dt), short
            assert int(m.group(3)) == round(p.total_ms), short
            seen.add(short)
    battery = batched(templates)
    assert seen == {t.protocol_id[:3] for t in battery}

    protos = [t.instantiate(1.0, settle) for t in battery]
    m = re.search(r"^\| \*\*Batched battery P01-P10 without P03\*\* \| \*\*([\d,]+)\*\* \| (\d+) simulations "
                  r"\(lengths ([\d, ]+) ms\) \|", section, re.MULTILINE)
    assert m, "battery row not found"
    assert _int(m.group(1)) == sum(round(p.total_ms / dt) for p in protos)
    assert int(m.group(2)) == len(group_by_length(protos))
    assert [int(x) for x in m.group(3).split(", ")] == sorted({round(p.total_ms) for p in protos})


def _fake_counter(threshold_nA: float | None):
    """Spike counter for rheobase.search: spikes at amplitudes >= threshold (None: never)."""
    return lambda amps: [int(threshold_nA is not None and a >= threshold_nA) for a in amps]


def test_protocol_catalog_rheobase_cost_matches_search():
    cfg = _study()
    rh = cfg["rheobase"]
    settle = float(cfg["numerics"]["settle_ms"])
    dt = float(cfg["numerics"]["dt_nominal_ms"])
    kw = dict(hi_nA=rh["initial_hi_nA"], grid=rh["grid"], rounds=rh["rounds"], expand=rh["expand"],
              max_hi_nA=rh["max_hi_nA"])
    per_sim = int(rh["grid"]) * round((settle + float(rh["step_duration_ms"])) / dt)
    worst = search(_fake_counter(0.97 * rh["max_hi_nA"]), **kw)     # brackets in the last grid, refines fully
    assert worst.status == "ok"
    spontaneous = search(_fake_counter(0.0), **kw)
    not_found = search(_fake_counter(None), **kw)
    assert spontaneous.status == "spontaneous" and not_found.status == "not_found"

    section = _section(read("protocol_catalog.md"), "## 6. Cost measure", "## 7.")
    m = re.search(r"^\| P03 rheobase search \| ([\d,]+) per simulation; 1-(\d+) simulations \| up to ([\d,]+) "
                  r"\(1 if spontaneous, 2-(\d+) if ok, (\d+) if not found\) \|", section, re.MULTILINE)
    assert m, "P03 cost row not found"
    assert _int(m.group(1)) == per_sim
    assert int(m.group(2)) == worst.n_simulations == int(m.group(4))
    assert _int(m.group(3)) == per_sim * worst.n_simulations
    assert spontaneous.n_simulations == 1
    assert int(m.group(5)) == not_found.n_simulations
    text = _norm(read("protocol_catalog.md"))
    assert f"exactly {not_found.n_simulations} if nothing spikes up to {rh['max_hi_nA']:g} nA" in text
    assert f"up to {worst.n_simulations} simulations, or {per_sim * worst.n_simulations:,} cell-steps" in text


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _g(x) -> str:
    return f"{float(x):g}"


def test_quoted_config_values_match_configs():
    cfg = _study()
    tol = config.load_yaml("tolerances.yaml")
    sel, pilot, num, rh = cfg["selection"], cfg["pilot"], cfg["numerics"], cfg["rheobase"]
    rheo_tol = tol["features"]["rheobase"]
    mults = ", ".join(_g(m) for m in tol["sensitivity_multipliers"])
    factors = ", ".join(str(f) for f in num["refinement_factors"])
    expected = {
        "statistical_plan.md": [
            f"k = {sel['budget_k']} in `configs/study.yaml`",
            f"`selection.seed` = {sel['seed']}",
            f"`random_draws` = {sel['random_draws']}",
            f"`sensitivity_multipliers` = [{mults}]",
            f"seed {cfg['analysis']['seed']} from `configs/study.yaml`",
        ],
        "preregistration_draft.md": [
            f"`selection.budget_k: {sel['budget_k']}`",
            f"{sel['random_draws']} draws, seed {sel['seed']}",
            f"Current provisional: {_g(num['timeout_s'])} s.",
            f"Current provisional: c = {_g(tol['c_refinement'])};",
            f"Current provisional: {mults}.",
            f"Current provisional: {_g(num['dt_nominal_ms'])} ms, refinement factors [{factors}]",
            f"Current provisional: settle {_g(num['settle_ms'])} ms",
            f"seed {cfg['analysis']['seed']}, ci 0.95",
        ],
        "mutation_catalog.md": [
            f"`mutants_per_operator: {pilot['mutants_per_operator']}`",
            f"`transforms_per_operator: {pilot['transforms_per_operator']}`",
        ],
        "protocol_catalog.md": [
            f"`grid` = {rh['grid']} cells",
            f"s = {_g(num['settle_ms'])} ms settling, then a {_g(rh['step_duration_ms'])} ms step",
            f"upward crossings of {_g(rh['spike_threshold_mV'])} mV",
            f"The grid spans [0, {_g(rh['initial_hi_nA'])}] nA",
            f"(expand x {_g(rh['expand'])}, cap {_g(rh['max_hi_nA'])} nA)",
            f"`rounds` - 1 = {rh['rounds'] - 1}",
            f"`abs_floor` {_g(rheo_tol['abs_floor'])} and `rel` {_g(rheo_tol['rel'])}",
            f"at least {_g(rheo_tol['resolution_multiple'])} x the search resolution",
        ],
    }
    for name, phrases in expected.items():
        text = _norm(read(name))
        for phrase in phrases:
            assert phrase in text, (name, phrase)


def test_quoted_heldout_bootstrap_resamples_match_code():
    """B, n_perm and the seed come from configs/study.yaml `analysis`; the docs must quote those values."""
    src = (REPO / "src" / "neurosem" / "experiments" / "heldout.py").read_text(encoding="utf-8")
    assert 'acfg.get("n_boot"' in src and 'acfg.get("n_perm"' in src and "paired_comparison(" in src,         "heldout.py bootstrap call changed; update statistical_plan.md and preregistration_draft.md"
    acfg = _study()["analysis"]
    for name in ("statistical_plan.md", "preregistration_draft.md"):
        text = _norm(read(name))
        assert f"B = {acfg['n_boot']}" in text and "configs/study.yaml" in text, name


def test_detection_rule_matches_heldout_code():
    """The documented primary-endpoint rule is the one heldout.py applies (reproducible detection)."""
    src = (REPO / "src" / "neurosem" / "experiments" / "heldout.py").read_text(encoding="utf-8")
    assert "set(o.detecting_protocols)" in src and "CANONICAL_ID in o.detecting_protocols" in src
    for name in ("statistical_plan.md", "preregistration_draft.md"):
        text = _norm(read(name))
        assert "detected at h and at h/2" in text or "detected at h and h/2" in text or "at h and at h/2" in text, name
        assert "Option A (recommended)" not in text, name


def test_protocol_catalog_fingerprint_size_matches_code():
    templates = [t for t in templates_from_config(_study().get("protocols")) if t.implemented]
    n = sum(len(t.features) for t in templates) + len(CANONICAL_FEATURES)
    assert f"{n} entries per model" in read("protocol_catalog.md")


def _architecture_section(start: str, stop: str) -> str:
    text = (DOCS / "ARCHITECTURE.md").read_text(encoding="utf-8")
    return text[text.index(start):text.index(stop)]


def test_mutation_catalog_covers_every_operator_and_transform():
    ops_section = _architecture_section("### 3.4", "### 3.5")
    operators = re.findall(r"^\| (?:stimulus|biophysical|reference|numerical) \| `(\w+)`", ops_section, re.MULTILINE)
    assert len(operators) == 19
    transforms = ["unit_conversion", "xml_formatting", "add_comments", "numeric_literal_format",
                  "rename_identifier", "factor_file", "reorder_independent", "explicit_default"]
    tr_section = _architecture_section("### 3.5", "### 3.6")
    for name in transforms:
        assert f"`{name}`" in tr_section, name
    catalog = read("mutation_catalog.md")
    for name in operators + transforms:
        assert f"`{name}`" in catalog, name


def test_statistical_plan_covers_endpoints_and_methods():
    text = read("statistical_plan.md").lower()
    for phrase in ["primary hypothesis", "primary endpoint", "cost-matched random", "silent-survival rate",
                   "false-positive rate", "by mutation family", "exhaustive-battery coverage",
                   "runtime and simulations per detected mutant", "agent-task success", "cluster bootstrap",
                   "exact mcnemar", "random baselines", "tolerance sensitivity", "undefined", "crashes",
                   "equivalent mutants", "denominator", "limitations", "few held-out models"]:
        assert phrase in text, phrase


def test_preregistration_draft_covers_every_required_item_with_blanks():
    text = read("preregistration_draft.md")
    lower = text.lower()
    for item in ["primary hypothesis", "primary endpoint", "inclusion and exclusion rules",
                 "model and mutation splits", "canonical protocol", "candidate protocols", "tolerance policy",
                 "primary statistical comparison", "handling of undefined features",
                 "treatment of crashes and equivalent mutants"]:
        assert re.search(rf"^## \d+\. {re.escape(item)}", lower, re.MULTILINE), item
    assert text.count("[NEEL DECISION REQUIRED") >= 20
    assert "DRAFT" in text


def test_preregistration_draft_does_not_assign_heldout_models():
    text = read("preregistration_draft.md")
    with open(REPO / "data" / "model_manifest.csv", newline="", encoding="utf-8") as f:
        model_ids = [r["model_id"] for r in csv.DictReader(f)]
    for mid in model_ids:
        assert mid not in text, f"preregistration draft must not name models ({mid})"


def test_learning_guide_has_fourteen_items_each_with_two_question_self_check():
    text = read("neel_learning_guide.md")
    sections = re.split(r"^## (?=\d+\. )", text, flags=re.MULTILINE)[1:]
    assert [int(s.split(".", 1)[0]) for s in sections] == list(range(1, 15))
    for s in sections:
        assert "**Analogy.**" in s or "*Analogy:*" in s
        assert "**Self-check.**" in s
        check = s.split("**Self-check.**", 1)[1].split("<details>", 1)[0]
        questions = re.findall(r"^\d\. ", check, re.MULTILINE)
        assert len(questions) == 2, s[:40]


def test_model_selection_lists_every_manifest_model():
    text = read("model_selection.md")
    with open(REPO / "data" / "model_manifest.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            assert r["model_id"] in text, r["model_id"]


def test_ai_disclosure_points_to_log():
    text = read("ai_disclosure.md")
    assert "AI_USE_LOG.md" in text
    assert (REPO / "AI_USE_LOG.md").is_file()
