"""Turn a finished campaign's output tables into a draft results section (amendment S-01).

It reads only what the campaign already wrote, computes nothing new, and decides nothing. Its job is
to lay the recorded numbers out in the order a reader needs them, with the reporting rules of
amendment S-01 built in so they cannot be forgotten:

- every pooled figure is shown **with its per-model values** (section 11.1);
- the exact **attrition counts** are shown, never a bare percentage (11.4);
- controls and numerical stress tests appear in **their own tables**, never pooled (11.4);
- results are reported over all mutants **and** over those with no prior outcome exposure (11.3);
- the designation and the prohibited-claims list are printed with the numbers (11.5).

Narrative sentences are left as bracketed prompts for the researcher. This script never writes an
interpretation, and never calls an exploratory campaign confirmatory.

    python scripts/build_results_draft.py --campaign pilot2 --out docs/RESULTS_DRAFT_pilot2.md
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from collections.abc import Mapping
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis import config  # noqa: E402
from neuraxis.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

EXPOSED_MANIFEST = "manifests/PILOT2_EXPOSED_VARIANTS.csv"


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def truthy(x: object) -> bool:
    return str(x).strip().lower() in ("true", "1", "yes")


def exposed_variant_ids() -> set[str]:
    """Variants whose outcome was observed before the campaign (amendment A-01), from the manifest."""
    return {r["variant_id"] for r in read_csv(REPO_ROOT / EXPOSED_MANIFEST) if r.get("variant_id")}


def attrition(cls: list[dict]) -> list[tuple[str, int]]:
    """Exact counts at every stage, in the order a reader needs them (S-01 11.4).

    Two admissibility counts are reported, never one. The frozen **class** is decided by the feature
    panel alone, so a fault that changes the voltage trace reproducibly while every summary feature
    stays inside tolerance is classed `4_equivalent_within_tested_domain`. Counting only by class
    hides such a fault; counting only by level flags silently overrides the frozen classification.
    Both numbers are shown, and any disagreement is listed by variant id.
    """
    semantic = [r for r in cls if r.get("stratum") == "primary_semantic" and r.get("kind") == "mutant"]
    executable = [r for r in semantic if r["class"] not in ("1_structurally_invalid", "2_non_executable")]
    stable = [r for r in executable if r["class"] != "3_numerically_unstable"]
    by_class = [r for r in stable if r["class"] in ("5_non_equivalent", "6_silent_under_canonical")]
    by_flags = [r for r in semantic if admissible(r)]
    return [("variants generated (all strata)", len(cls)),
            ("primary semantic mutants", len(semantic)),
            ("structurally valid and executable", len(executable)),
            ("numerically stable", len(stable)),
            ("admissible by frozen class (feature panel)", len(by_class)),
            ("admissible including trace-only detection", len(by_flags)),
            ("equivalent within the tested domain", sum(1 for r in stable if r["class"].startswith("4_")))]


def trace_only_faults(cls: list[dict]) -> list[dict]:
    """Faults the feature panel called equivalent but full-trace comparison detected reproducibly.

    These are the clearest evidence for the study's finding and they are easy to lose: the frozen
    class says "no change", so a class-based count drops them.
    """
    return [r for r in cls if r.get("stratum") == "primary_semantic" and r.get("kind") == "mutant"
            and admissible(r) and r["class"] not in ("5_non_equivalent", "6_silent_under_canonical")]


def canonical_detected(r: Mapping[str, str]) -> bool:
    """The canonical strategy detected this fault: by its features (level B) or its full trace (C).

    This must match the rule the branch classification uses. An earlier version of this function
    counted only feature-level detections, which disagreed with the headline rate by up to five
    percentage points on a model - the kind of mismatch that puts two different numbers for the
    same quantity into one manuscript.
    """
    return truthy(r.get("level_B_canonical_feature")) or truthy(r.get("level_C_canonical_trace"))


def admissible(r: Mapping[str, str]) -> bool:
    return truthy(r.get("level_A_basic_pass")) and truthy(r.get("level_E_full_battery"))


def per_model(cls: list[dict], exposed: set[str]) -> list[dict]:
    rows = []
    for mid in sorted({r["model_id"] for r in cls}):
        sem = [r for r in cls if r["model_id"] == mid and r.get("stratum") == "primary_semantic"
               and r.get("kind") == "mutant"]
        adm = [r for r in sem if admissible(r)]
        canon = [r for r in adm if canonical_detected(r)]
        unexposed = [r for r in adm if r["variant_id"] not in exposed]
        canon_unexp = [r for r in unexposed if canonical_detected(r)]
        rows.append({"model_id": mid, "mutants": len(sem), "admissible": len(adm),
                     "canonical_detected": len(canon),
                     "canonical_rate": f"{len(canon) / len(adm):.3f}" if adm else "",
                     "admissible_unexposed": len(unexposed),
                     "canonical_detected_unexposed": len(canon_unexp),
                     "canonical_rate_unexposed": f"{len(canon_unexp) / len(unexposed):.3f}" if unexposed else ""})
    return rows


def table(rows: list[dict], columns: list[str], header: list[str] | None = None) -> list[str]:
    head = header or columns
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")) for c in columns) + " |")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    processed = config.results_dir() / "processed" / a.campaign
    outputs = processed / "pilot_v2_outputs"
    cls = read_csv(processed / "classification.csv")
    if not cls:
        print(f"no classification.csv under {processed}; run the campaign and its outputs first")
        return 1
    meta = {}
    md_file = processed / "STUDY_METADATA.json"
    if md_file.is_file():
        meta = json.loads(md_file.read_text(encoding="utf-8"))
    exposed = exposed_variant_ids()
    commit, dirty = git_state()

    L = [f"# Results draft: campaign `{a.campaign}`", "",
         f"*Generated {utc_now()} from recorded outputs at commit `{commit}` (tree dirty: {dirty}). "
         "Numbers are copied, never computed here. Bracketed lines are prompts for the researcher.*", ""]
    if meta:
        L += [f"> **{meta.get('study_phase', '')}** - {meta.get('designation', '')}", "",
              f"Protocol version `{meta.get('protocol_version', '')}`, study `{meta.get('study_id', '')}`.", ""]

    L += ["## 1. Attrition", "",
          "Exact counts at every stage; no percentage appears in this section without its counts.", ""]
    L += table([{"stage": k, "n": v} for k, v in attrition(cls)], ["stage", "n"], ["stage", "n"])

    trace_only = trace_only_faults(cls)
    if trace_only:
        L += ["", "### Faults detected only by full-trace comparison", "",
              "The frozen classification uses the feature panel alone. These faults were classed "
              "**equivalent within the tested domain** - every summary feature inside tolerance on every "
              "protocol - yet full-trace comparison detected them reproducibly. They are reported here "
              "explicitly because a class-based count drops them, and they are the clearest evidence that "
              "feature-based regression testing is structurally blind to some real changes.", ""]
        L += table([{"variant_id": r["variant_id"], "model_id": r["model_id"], "operator": r.get("operator", ""),
                     "class": r["class"]} for r in trace_only],
                   ["variant_id", "model_id", "operator", "class"],
                   ["variant", "model", "operator", "frozen class"])

    L += ["", "## 2. Per-model results (the generalization units)", "",
          "Five models is a small number of clusters, so per-model values are reported beside any pooled "
          "figure and never replaced by it (amendment S-01, section 11.1). The right-hand columns repeat the "
          "same quantity over the mutants that carry **no prior outcome exposure** (section 11.3).", ""]
    pm = per_model(cls, exposed)
    L += table(pm, ["model_id", "mutants", "admissible", "canonical_detected", "canonical_rate",
                    "admissible_unexposed", "canonical_detected_unexposed", "canonical_rate_unexposed"],
               ["model", "mutants", "admissible", "canonical detected", "rate",
                "admissible (unexposed)", "canonical detected (unexposed)", "rate (unexposed)"])
    if exposed:
        L += ["", f"Prior-exposure manifest: `{EXPOSED_MANIFEST}` ({len(exposed)} variants)."]
    else:
        L += ["", f"*No exposure manifest found at `{EXPOSED_MANIFEST}`; the unexposed columns repeat the full set.*"]

    for title, name, note in [
        ("3. Validation levels A-E", "01_validation_level_counts.csv",
         "Levels B (canonical features) and C (canonical full trace) are never merged."),
        ("4. Unique protocol contribution", "14_unique_protocol_contribution.csv",
         "Variants that **only** this protocol detected. A protocol that contributes nothing unique is reported "
         "as contributing nothing, and cost-matched comparison is required before any battery is called useful "
         "(S-01, section 11.2)."),
        ("5. Canonical survivors", "02_feature_level_canonical_survivors.csv",
         "Each apparent survivor carries its h/4 confirmation status; unconfirmed survivors are never counted "
         "as hidden drift."),
        ("6. Valid-transformation controls (own table, never pooled)", "07_valid_transformation_false_positives.csv",
         "A control classified non-equivalent is a false positive of the method."),
        ("7. Kinetics: atomic versus compound", "15_kinetics_atomic_vs_compound.csv",
         "Reported separately and never pooled into one kinetics number."),
        ("8. Uncertain cases", "16_uncertain_cases.csv",
         "Listed explicitly rather than forced into a class."),
    ]:
        rows = read_csv(outputs / name)
        L += ["", f"## {title}", "", note, ""]
        if not rows:
            L += [f"*`{name}` not present; run `scripts/pilot_v2_outputs.py` for this campaign.*"]
            continue
        cols = [c for c in rows[0] if c not in ("study_id", "project_name", "study_phase", "protocol_version",
                                                "designation")][:9]
        L += table(rows[:40], cols)
        if len(rows) > 40:
            L += ["", f"*{len(rows)} rows total; first 40 shown. Full table: `{name}`.*"]

    L += ["", "## 9. Numerical robustness stratum (separate analysis)", "",
          "These are convergence stress tests. They never enter the semantic denominator and are never "
          "described as hidden semantic drift.", ""]
    num = [r for r in cls if r.get("stratum") == "numerical_robustness"]
    L += table([{"class": k, "n": v} for k, v in sorted(Counter(r["class"] for r in num).items())],
               ["class", "n"], ["class", "n"]) if num else ["*No numerical stratum rows.*"]

    branch = {}
    summary = outputs / "summary.json"
    if summary.is_file():
        branch = json.loads(summary.read_text(encoding="utf-8")).get("branch", {})
    L += ["", "## 10. Branch classification", ""]
    if branch:
        L += [f"- primary branch: **{branch.get('primary_branch', '')}**",
              f"- precedence: {' > '.join(branch.get('precedence', []))}", "",
              "```json", json.dumps(branch.get("evidence", {}), indent=2), "```", "",
              "Rules were fixed before the data existed and are not re-tuned. Branch A is never forced."]
    else:
        L += ["*No `summary.json`; run the outputs builder.*"]

    L += ["", "## 11. Claims this dataset does not support", "",
          "- no claim of universal behavioural equivalence: an undetected difference is evidence about the "
          "tested protocols and features, not proof that two models behave identically;",
          "- no claim of broad biological validation: these are single-compartment or somatic cells from a "
          "handful of papers;",
          "- every coverage figure is conditional on the empirical reference battery, the frozen tolerance "
          "table and the models tested;",
          "- nothing here is confirmatory.", "",
          "## 12. For the researcher to write", "",
          "- [ ] [One sentence: what the canonical-versus-battery comparison shows, in plain language.]",
          "- [ ] [One sentence: whether any protocol earned its compute, citing section 4.]",
          "- [ ] [One sentence: what the controls and the numerical stratum say about method noise.]",
          "- [ ] [Limitations paragraph: model count, single simulator unless the cross-simulator check ran, "
          "RMSE insensitivity on spiking protocols, and the exposed variants.]", ""]

    out = Path(a.out) if a.out else REPO_ROOT / "docs" / f"RESULTS_DRAFT_{a.campaign}.md"
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(REPO_ROOT).as_posix()} ({len(L)} lines)")
    print(f"  models {len(pm)}; classification rows {len(cls)}; exposure manifest {len(exposed)} variant(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
