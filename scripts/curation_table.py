"""Final curation table: every candidate attempted, with the evidence behind its decision.

Reads a finished curation campaign (``results/processed/<campaign>/curation/*.json``) and writes

- ``manifests/CURATION_FINAL_TABLE.csv``: one row per candidate with all recorded columns;
- ``docs/MODEL_CURATION_FINAL_TABLE.md``: the same table in a readable form, plus the counts.

It simulates nothing and changes no decision; it only reorganises recorded evidence.

    python scripts/curation_table.py --curation curation-v3
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis import config  # noqa: E402
from neuraxis.orchestration.curation import CRITERIA  # noqa: E402
from neuraxis.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

COLUMNS = ["model_id", "name", "source_family", "decision", "exact_reason", "publication", "license", "license_url",
           "snapshot", "commit", "validation", "validation_errors", "execution", "recording_location",
           "current_response", "response_type", "rheobase_nA", "rebound_spikes_P08", "sag_ratio_P07",
           "estimated_variant_runtime_s", "runtime_within_budget", "convergence", "refinement_excluded",
           "deterministic", "mutation_applicability", "semantic_operators_with_site", "ion_channels",
           "protocols_compatible", "pilot2_selected"]
DECISIONS = {"include_eligible": "eligible", "exclude": "excluded", "review": "needs human judgement"}


def flag(v: object) -> str:
    return "" if v is None else ("pass" if v else "fail")


def rows_for(campaign: str, selected: set[str]) -> list[dict]:
    d = config.results_dir() / "processed" / campaign / "curation"
    out = []
    for f in sorted(d.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        m, c, e = j["model"], j["criteria"], j["evidence"]
        reasons = j.get("reasons") or []
        out.append({
            "model_id": m["model_id"], "name": m["name"], "source_family": m["source_family"],
            "decision": DECISIONS.get(j["decision"], j["decision"]),
            "exact_reason": "; ".join(f"{k}: {CRITERIA[k]}" for k in reasons) if reasons else "all criteria met",
            "publication": m["citation"], "license": m["license"], "license_url": m["license_url"],
            "snapshot": m["snapshot"], "commit": m["commit"],
            "validation": flag(c.get("C04_validation")), "validation_errors": "; ".join(e.get("validation_errors") or []),
            "execution": flag(c.get("C05_executes")), "recording_location": flag(c.get("C07_recording_location")),
            "current_response": flag(c.get("C08_responds_to_current")),
            "response_type": e.get("firing_regime_P05", ""), "rheobase_nA": e.get("rheobase_nA", ""),
            "rebound_spikes_P08": e.get("rebound_spikes_P08", ""), "sag_ratio_P07": e.get("sag_ratio_P07", ""),
            "estimated_variant_runtime_s": e.get("estimated_variant_runtime_s", ""),
            "runtime_within_budget": flag(c.get("C11_runtime")),
            "convergence": flag(c.get("C10_refinement_stable")), "refinement_excluded": e.get("refinement_excluded", ""),
            "deterministic": flag(c.get("C09_deterministic")),
            "mutation_applicability": flag(c.get("C12_operators")),
            "semantic_operators_with_site": ";".join(e.get("semantic_operators_with_site") or []),
            "ion_channels": ";".join(e.get("ion_channels") or []),
            "protocols_compatible": flag(c.get("C13_protocols_compatible")),
            "pilot2_selected": "yes" if m["model_id"] in selected else "no",
        })
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--curation", required=True)
    ap.add_argument("--pilot-config", default="configs/pilot2_frozen.yaml")
    a = ap.parse_args(argv)
    import yaml

    pilot = yaml.safe_load((REPO_ROOT / a.pilot_config).read_text(encoding="utf-8"))["pilot"]
    selected = set(pilot["models"])
    rows = rows_for(a.curation, selected)
    if not rows:
        print(f"no curation evidence for campaign {a.curation}")
        return 1

    csv_path = REPO_ROOT / "manifests" / "CURATION_FINAL_TABLE.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    counts = {k: sum(1 for r in rows if r["decision"] == k) for k in ("eligible", "excluded", "needs human judgement")}
    commit, dirty = git_state()
    lines = [
        "# Final model curation table", "",
        (f"*Campaign `{a.curation}`; written {utc_now()}; commit `{commit}` (tree dirty: {dirty}). "
         "Machine-readable form: `manifests/CURATION_FINAL_TABLE.csv`. Generated from recorded evidence only; "
         "no decision is re-made here.*"), "",
        f"- **candidates attempted: {len(rows)}**",
        (f"- eligible: **{counts['eligible']}**; excluded: **{counts['excluded']}**; "
         f"needing human judgement: **{counts['needs human judgement']}**"),
        f"- selected for Pilot 2: **{len(selected)}** ({', '.join(sorted(selected))})", "",
        "Criteria: " + "; ".join(f"**{k}** {v}" for k, v in CRITERIA.items()), "",
        ("| model | source | decision | exact reason | publication | licence | validation | execution | "
         "current response | response type | rheobase (nA) | runtime/variant (s) | convergence | "
         "mutation operators with a site | Pilot 2 |"),
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["decision"] != "eligible", r["model_id"])):
        pub = r["publication"].split(". doi")[0][:90]
        ops = r["semantic_operators_with_site"].count(";") + 1 if r["semantic_operators_with_site"] else 0
        conv = f"{r['convergence']} ({r['refinement_excluded']} excluded)" if r["refinement_excluded"] else r["convergence"]
        lines.append(f"| `{r['model_id']}` | {r['source_family']} | {r['decision']} | {r['exact_reason']} | {pub} | "
                     f"{r['license']} | {r['validation']} | {r['execution']} | {r['current_response']} | "
                     f"{r['response_type']} | {r['rheobase_nA']} | {r['estimated_variant_runtime_s']} "
                     f"({r['runtime_within_budget']}) | {conv} | {ops} | {r['pilot2_selected']} |")
    lines += ["", ("Validation errors, recording location, determinism, protocol compatibility, ion channels and "
                   "the full operator lists are columns of the CSV."), ""]
    md = REPO_ROOT / "docs" / "MODEL_CURATION_FINAL_TABLE.md"
    md.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"{len(rows)} candidates: {counts}; wrote {csv_path.relative_to(REPO_ROOT)} and {md.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
