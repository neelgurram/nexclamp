"""Write the frozen agent-evaluation config from a finished campaign (agent protocol, step 1.5).

The agent study's behavioural layers -- ``canonical_passes`` and ``hidden_battery_passes`` -- need
three things the harness cannot invent: the frozen tolerance table, the selected protocol battery,
and each base model's reference rheobase. All three are produced by a finished main campaign. This
script reads them from that campaign and writes ``frozen_agent_eval.yaml`` with every hash the
evaluator checks.

Ordering matters and is enforced by the protocol, not by convenience: the tolerance table and the
protocol battery must have been chosen **without looking at any agent output**. This script only
copies values that already exist; it never chooses one.

    python scripts/agent_freeze_config.py --campaign pilot2 \\
        --out results/agent_study/study01/frozen_agent_eval.yaml

The output goes **outside version control** (``results/agent_study/`` is Git-ignored for the private
parts) and is refused later if any hashed input changes.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

from neuraxis import config  # noqa: E402
from neuraxis.experiments import agent as ag  # noqa: E402
from neuraxis.provenance import REPO_ROOT, git_state, sha256_file, utc_now  # noqa: E402

SCHEMA = "neurosem-agent-frozen/1"


def reference_rheobase(campaign: str) -> dict[str, float]:
    """Each base model's reference rheobase, read from the campaign's reference records."""
    out: dict[str, float] = {}
    refs = config.results_dir() / "processed" / campaign / "references"
    for d in sorted(p for p in refs.iterdir() if p.is_dir()) if refs.is_dir() else []:
        search = d / "rheobase_search.json"
        if not search.is_file():
            continue
        j = json.loads(search.read_text(encoding="utf-8"))
        value = j.get("rheobase_nA", (j.get("result") or {}).get("rheobase_nA"))
        if value is not None:
            out[d.name] = float(value)
    return out


def selected_protocols(campaign: str) -> list[str]:
    """The protocol battery the campaign actually ran, in its recorded order."""
    costs = config.results_dir() / "processed" / campaign / "protocol_costs.csv"
    if costs.is_file():
        with open(costs, newline="", encoding="utf-8") as f:
            ids = [r["protocol_id"] for r in csv.DictReader(f)]
        if ids:
            return ids
    cfg = config.study()
    return [p["protocol_id"] for p in cfg["protocols"]]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True, help="finished campaign supplying tolerances and rheobase")
    ap.add_argument("--out", required=True, help="path for frozen_agent_eval.yaml (outside version control)")
    ap.add_argument("--study", default="", help="study name recorded in the config (default: the campaign)")
    ap.add_argument("--timeout-s", type=float, default=3600.0)
    ap.add_argument("--tolerance-multiplier", type=float, default=1.0, help="1.0 for the primary analysis")
    ap.add_argument("--hidden-root", default="", help="agent_study/hidden (Git-ignored; absent in a worktree)")
    a = ap.parse_args(argv)

    hidden_root = Path(a.hidden_root).resolve() if a.hidden_root else ag.HIDDEN_DIR
    processed = config.results_dir() / "processed" / a.campaign
    tolerance_table = processed / "tolerances.csv"
    problems = []
    if not tolerance_table.is_file():
        problems.append(f"no tolerance table at {tolerance_table}")
    # An empty hidden-spec mapping would be written silently and refused later; catch it here.
    if not sorted(Path(hidden_root).glob("*/hidden_checks.yaml")) if Path(hidden_root).is_dir() else True:
        problems.append(f"no hidden evaluator specs under {hidden_root}; pass --hidden-root")
    rheobase = reference_rheobase(a.campaign)
    if not rheobase:
        problems.append(f"no reference rheobase records under {processed / 'references'}")
    protocols = selected_protocols(a.campaign)
    if not protocols:
        problems.append("no protocol battery recorded")
    commit, dirty = git_state()
    if dirty:
        problems.append("the working tree is dirty; freeze from a clean, tagged checkout (protocol step 1.4)")
    if problems:
        for p in problems:
            print(f"BLOCKED: {p}")
        print("\nNothing was written. The frozen config may only be built from a finished campaign on a clean tree.")
        return 1

    study_cfg, features_cfg, tol_cfg = config.study(), config.features(), config.tolerances()
    # Only the schema's own keys are accepted, plus "notes": anything else is refused by
    # load_frozen_config, so provenance that is not part of the contract goes inside notes.
    doc = {
        "schema": SCHEMA,
        "campaign": a.study or a.campaign,
        "results_root": str(config.results_dir()),
        "dt_ms": float(study_cfg["numerics"]["dt_nominal_ms"]),
        "timeout_s": float(a.timeout_s),
        "tolerance_table": str(tolerance_table),
        "tolerance_table_sha256": sha256_file(tolerance_table),
        "tolerance_multiplier": float(a.tolerance_multiplier),
        "selected_protocols": protocols,
        "reference_rheobase_nA": rheobase,
        "configs": {name: {"path": str(c.path), "sha256": c.sha256}
                    for name, c in (("study", study_cfg), ("features", features_cfg), ("tolerances", tol_cfg))},
        "evaluator_git_commit": commit,
        "notes": {
            "created_utc": utc_now(),
            "source_campaign": a.campaign,
            "provenance": ("Tolerances and the protocol battery come from the main study and were chosen without "
                           "any agent output. This file lives outside version control and is refused if any "
                           "hashed input changes."),
        },
        **ag.freeze_hashes(hidden_root=hidden_root),
    }
    out = Path(a.out)
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    print(f"wrote {out}")
    print(f"  campaign            {doc['campaign']} (from {a.campaign})")
    print(f"  evaluator commit    {commit}")
    print(f"  protocols           {len(protocols)}: {', '.join(protocols)}")
    print(f"  reference rheobase  {len(rheobase)} model(s): " +
          ", ".join(f"{k}={v:.6g} nA" for k, v in sorted(rheobase.items())))
    print(f"  tolerance table     {tolerance_table.name} ({doc['tolerance_table_sha256'][:12]}...)")
    print(f"  tasks hashed        {len(doc['task_sha256'])}; hidden specs hashed {len(doc['hidden_spec_sha256'])}")
    print(f"\n  config sha256       {sha256_file(out)}")
    print("\nRecord that hash and the commit before the first trial (protocol step 1.6).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
