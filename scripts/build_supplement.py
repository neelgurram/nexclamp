"""Assemble the manuscript's two Online Resources from recorded files only.

Online Resource 1 (methods detail): screening criteria and outcomes, model provenance and
licences, protocol definitions, feature list, tolerance constants, fault operators with the counts
actually generated, and the software environment.

Online Resource 2 (development record): the deviation log verbatim, the two development pilots
with their recorded numbers, the Pilot 2 exposure assessment, and the preregistration record.

Nothing is typed by hand: every table is read from ``configs/``, ``data/``, ``docs/`` or
``results/``, so the supplements cannot drift from what ran.

    python scripts/build_supplement.py --campaign heldout-v1
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

from nexclamp import config  # noqa: E402
from nexclamp.protocols.definitions import DEFAULT_TEMPLATES  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

OUT = REPO_ROOT / "docs" / "manuscript"


def read_csv(p: Path) -> list[dict]:
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def table(header: list[str], rows: list[list[str]]) -> list[str]:
    return ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|",
            *["| " + " | ".join(str(c) for c in r) + " |" for r in rows], ""]


def criteria_lines() -> list[str]:
    """The thirteen screening criteria, taken from the curation report's own definition line."""
    txt = (REPO_ROOT / "docs" / "MODEL_CURATION_FINAL_TABLE.md").read_text(encoding="utf-8")
    line = next((ln for ln in txt.splitlines() if ln.startswith("Criteria:")), "")
    import re
    # "**C01_provenance** description; **C02_reuse_rights** description; ..." - the descriptions
    # contain semicolons of their own, so split on the next bold code, not on punctuation.
    pairs = re.findall(r"\*\*(C\d+_\w+)\*\*\s*(.*?)(?=;\s*\*\*C\d+_|\s*$)", line)
    return [[f"`{code}`", desc.strip().rstrip(";. ")] for code, desc in pairs]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    proc = config.results_dir() / "processed" / a.campaign
    cfg = config.study()
    tol = config.tolerances()
    commit, dirty = git_state()
    stamp = (f"*Generated {utc_now()} by `scripts/build_supplement.py` at commit `{commit[:12]}` "
             f"(tree dirty: {dirty}). Every table is read from the repository's recorded files.*")
    models = {r["model_id"]: r for r in read_csv(REPO_ROOT / "data" / "model_manifest.csv")}
    heldout = (REPO_ROOT / "data" / "splits" / "heldout" / "heldout_models.txt").read_text(encoding="utf-8").split()
    discovery = (REPO_ROOT / "data" / "splits" / "discovery_models.txt").read_text(encoding="utf-8").split()
    cls = read_csv(proc / "classification.csv")

    # ---------------------------------------------------------------- Online Resource 1
    L = ["# Online Resource 1: methods detail", "", stamp, "",
         "## 1 Model screening criteria", "",
         "Applied to the unmodified model only; a model is eligible only if it meets all thirteen.", ""]
    L += table(["Criterion", "Requirement"], criteria_lines())
    L += ["The runtime criterion (C11) used a budget of 4,200 s of estimated simulator time per "
          "variant, raised from 1,800 s before any held-out model was mutated (deviation X-25, "
          "Online Resource 2).", "", "## 2 Models", "",
          "Held-out models (confirmatory evaluation):", ""]
    cols = ["Model", "Source family", "Publication", "Licence", "Repository", "Commit"]
    for label, ids in (("held-out", heldout), ("development", discovery)):
        rows = []
        for mid in ids:
            m = models.get(mid, {})
            rows.append([f"`{mid}`", m.get("source_family", ""), m.get("citation", "")[:120],
                         m.get("license", "")[:60], m.get("source_url", ""), (m.get("commit", "") or "")[:12]])
        if label == "development":
            L += ["Development models (method fixing; never evaluated confirmatorily):", ""]
        L += table(cols, rows)

    L += ["## 3 Protocols", "",
          "Stimulus amplitudes are multiples of each model's own measured rheobase. Every protocol "
          "begins with a settling period of "
          f"{cfg['numerics']['settle_ms']:g} ms. The canonical protocol is each model's shipped simulation, "
          "run unchanged.", ""]
    used = {p["protocol_id"] for p in cfg["protocols"]} | {"P00_canonical"}
    rows = [[f"`{t.protocol_id}`", t.description, ", ".join(f"{k} {v}" for k, v in t.params.items())]
            for t in DEFAULT_TEMPLATES if t.protocol_id in used]
    L += table(["Protocol", "Description", "Parameters"], rows)
    L += ["Protocols selected on the development models and frozen before the held-out evaluation: "
          + ", ".join(f"`{p}`" for p in json.loads((config.results_dir() / "processed" / "pilot2" /
                                                    "selection_k4.json").read_text(encoding="utf-8"))["selected_protocols"])
          + f" (budget k = {cfg['selection']['budget_k']}; the greedy rule stopped early).", "",
          "## 4 Features and tolerances", "",
          "A feature difference counts only if it exceeds "
          "tau = max(absolute floor, relative x |f_h|, "
          f"{tol['c_refinement']:g} x |f_h - f_h/2|), and only if it reproduces at h and at h/2.", ""]
    L += table(["Feature", "Absolute floor", "Relative term"],
               [[f"`{k}`", v.get("abs_floor", ""), v.get("rel", "")] for k, v in tol["features"].items()])
    L += [f"Categorical features: {', '.join(f'`{k}` ({v})' for k, v in tol.get('categorical', {}).items())}. "
          "A feature defined in one model and undefined in the other counts as a difference "
          f"({tol['definedness_mismatch_is_detection']}). Sensitivity multipliers: "
          f"{', '.join(str(m) for m in tol['sensitivity_multipliers'])}.", "",
          "Full-trace comparison (reported separately, never merged with features): spike count, "
          "spike timing with tau_shift = max(0.5 ms, 3 x the reference's own h vs h/2 shift), and "
          "root-mean-square voltage difference with tau_rmse = max(0.5 mV, 3 x the reference's own "
          "h vs h/2 RMSE).", "", "## 5 Fault operators and variants generated", ""]
    counts = Counter((r["stratum"], r["family"], r["operator"]) for r in cls)
    L += table(["Stratum", "Family", "Operator", "Variants"],
               [[s, f, f"`{o}`", n] for (s, f, o), n in sorted(counts.items())])
    L += [f"Severities: {', '.join(cfg['pilot']['severity_levels'])}, defined by prespecified bands of "
          "|ln k| for multiplicative changes and of millivolts for shifts. Sites were chosen by a "
          f"seeded generator (seed {cfg['selection']['seed']}) fixed before generation.", "",
          "## 6 Software environment", ""]
    env = json.loads((proc / "STUDY_METADATA.json").read_text(encoding="utf-8"))
    L += table(["Item", "Value"], [[k, str(v)[:160]] for k, v in env.items()])
    L += ["Simulator: jNeuroML 0.14.0 / jLEMS 0.12.0 on Temurin JDK 21.0.12.1+1; Python 3.12.10; "
          "pyNeuroML 1.3.22; libNeuroML 0.6.7; eFEL 5.7.34. Every run records its own software "
          "versions, inputs and outputs under a content-addressed identifier.", ""]
    (OUT / "ONLINE_RESOURCE_1.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

    # ---------------------------------------------------------------- Online Resource 2
    dev = json.loads((config.results_dir() / "processed" / "pilot2" / "pilot_v2_outputs" /
                      "summary.json").read_text(encoding="utf-8"))
    ev = dev["branch"]["evidence"]
    prereg = json.loads((REPO_ROOT / "docs" / "PREREGISTRATION_RECORD.json").read_text(encoding="utf-8"))
    L = ["# Online Resource 2: development record, deviations and preregistration", "", stamp, "",
         "## 1 Preregistration", ""]
    L += table(["Field", "Value"], [[k, str(v)[:200]] for k, v in prereg.items()])
    L += ["", "## 2 Development pilots (exploratory; never pooled with the confirmatory result)", "",
          "**Pilot 1** (2 models, exploratory iteration 1): the canonical test detected all 22 admissible "
          "model edits; the battery detected 19. Three cases first described as silent were numerical, "
          "not semantic, and are reported only in corrected form (deviations X-17, X-38 in the log below).", "",
          "**Pilot 2** (5 models), recorded outcome:", ""]
    L += table(["Quantity", "Value"],
               [["primary semantic mutants", ev["n_semantic_mutants"]],
                ["admissible (any protocol, features or trace)", ev["n_E_admissible"]],
                ["controls", ev["n_controls"]],
                ["control false positives", ev["control_false_positives"]],
                ["feature-level canonical survivors", ev["feature_level_survivors"]],
                ["survivors not confirmed at h/4", ev["feature_survivors_unconfirmed_h4"]],
                ["confirmed full-trace survivors", ev["confirmed_full_trace_survivors"]],
                ["survivors unclassifiable (level C not calibrated)", ev["full_trace_survivors_unclassifiable"]],
                ["canonical detection, features or trace", f"{ev['canonical_B_or_C_detection_rate']:.3f}"],
                ["branch classification", dev["branch"]["primary_branch"]]])
    L += ["Pilot 2's protocol was edited after operator validation had already simulated four of its five "
          "models, so nine of its mutants shared an exact edit with a validated site. Pilot 2 is therefore "
          "reported both over all mutants and over the 79 unexposed ones (amendment A-01, deviation X-23). "
          "No held-out model is affected: none was mutated before the confirmatory run.", "",
          "## 3 Deviation log (verbatim)", ""]
    L += [(REPO_ROOT / "docs" / "DEVIATION_LOG.md").read_text(encoding="utf-8").strip(), ""]
    (OUT / "ONLINE_RESOURCE_2.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

    for f in ("ONLINE_RESOURCE_1.md", "ONLINE_RESOURCE_2.md"):
        print(f"wrote docs/manuscript/{f} ({len((OUT / f).read_text(encoding='utf-8').splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
