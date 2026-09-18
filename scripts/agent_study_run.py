"""Operator tool for the agent study: prepare trials, then score them (docs/agent_study_protocol.md).

The harness never starts an agent, and neither does this script. It does the two jobs a human
operator needs: export clean trial directories, and score them afterwards with the hidden
evaluator. Between those two steps a person (or an isolated agent session) edits the model inside
the trial directory.

    python scripts/agent_study_run.py prepare --tasks t01_unit_repair t05_unit_conversion \\
        --trials-root ../agent_trials --replicates 1
    python scripts/agent_study_run.py score --trials-root ../agent_trials --frozen development

**What the agent may see**: only the trial directory (``TASK.md``, ``model/``, ``public_tests/``,
``scratch/``). Never this repository, never ``agent_study/hidden/``, never the private record that
holds the answer key. This script prints trial paths and never prints a hidden assertion or a seed
edit, so its own output is safe to paste into an agent session.

**Isolation is environmental, not a permission setting** (protocol section 2). A confirmatory run
needs a separate OS account, container or VM that cannot read this repository. When that is not the
case, pass ``--isolation partial`` and the run is recorded as a **feasibility pilot**, never as the
confirmatory agent study.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses as dc
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis.experiments import agent as ag  # noqa: E402
from neuraxis.provenance import REPO_ROOT, git_state, sha256_file, utc_now  # noqa: E402

LAYERS = ("edit_scope", "hidden_assertions_pass", "schema_valid", "executes", "canonical_passes",
          "hidden_battery_passes")
TRIAL_COLUMNS = ["trial_id", "task_id", "task_type", "category", "basic_pass", "neurosem_pass",
                 "basic_pass_battery_fail", "first_failed_layer", "unauthorized_edits_detected", "model_changed",
                 *[f"layer_{x}" for x in LAYERS],
                 "provisional", "isolation", "export_content_sha256", "scored_utc"]


def layer_status(score, layer: str) -> str:
    """The recorded status of one layer ('pass', 'fail', 'error', 'not_evaluated', or '' if absent)."""
    out = score.layers.get(layer)
    if out is None:
        return ""
    status = getattr(out, "status", None)
    return getattr(status, "value", str(status)) if status is not None else ""


def prepare(a: argparse.Namespace) -> int:
    root = Path(a.trials_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    tasks = a.tasks or sorted(ag.load_all_tasks())
    manifest, commit, dirty = [], *git_state()
    for task_id in tasks:
        for rep in range(1, int(a.replicates) + 1):
            trial_id = f"{task_id}__r{rep:02d}"
            dest = root / trial_id
            export = ag.prepare_trial(task_id, dest, overwrite=a.overwrite, allow_dirty=a.allow_dirty)
            manifest.append({"trial_id": trial_id, "task_id": task_id, "replicate": rep,
                             "trial_dir": str(export.trial_dir), "private_dir": str(export.private_dir),
                             "content_sha256": export.content_sha256,
                             "development_only": export.development_only,
                             "task_md": str(export.trial_dir / "TASK.md")})
            print(f"prepared {trial_id}: {export.trial_dir}"
                  f"{'  [development_only]' if export.development_only else ''}")
    record = {"created_utc": utc_now(), "commit": commit, "tree_dirty": dirty, "trials_root": str(root),
              "isolation": a.isolation, "trials": manifest,
              "note": "The agent sees only its own trial directory. Private records hold the answer key and are "
                      "never placed under the trials root."}
    (root / "TRIALS.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\n{len(manifest)} trial(s) prepared under {root}")
    print("Each agent session may read and write ONLY its own trial directory. Do not give it this repository.")
    return 0


def score(a: argparse.Namespace) -> int:
    root = Path(a.trials_root).resolve()
    record = json.loads((root / "TRIALS.json").read_text(encoding="utf-8"))
    if a.frozen == "development":
        cfg = ag.FrozenConfig.development(results_root=REPO_ROOT / "results")
        frozen_sha = ""
    else:
        cfg = ag.load_frozen_config(Path(a.frozen))
        frozen_sha = sha256_file(Path(a.frozen))
    # The hidden specs are Git-ignored, so a worktree does not carry them. They live in the main checkout.
    hidden_root = Path(a.hidden_root).resolve() if a.hidden_root else ag.HIDDEN_DIR
    if not hidden_root.is_dir():
        print(f"no hidden specs at {hidden_root}; pass --hidden-root <main checkout>/agent_study/hidden")
        return 1
    rows, scores = [], []
    for t in record["trials"]:
        trial_dir = Path(t["trial_dir"])
        if not trial_dir.is_dir():
            print(f"skipped {t['trial_id']}: trial directory missing")
            continue
        s = ag.score_trial(t["task_id"], trial_dir, cfg, trial_id=t["trial_id"], hidden_root=hidden_root)
        scores.append(s)
        rows.append({"trial_id": s.trial_id, "task_id": s.task_id, "task_type": s.task_type,
                     "category": s.category, "basic_pass": s.basic_pass, "neurosem_pass": s.neurosem_pass,
                     "basic_pass_battery_fail": s.basic_pass_battery_fail,
                     "first_failed_layer": s.first_failed_layer,
                     "unauthorized_edits_detected": s.unauthorized_edits_detected,
                     "model_changed": s.model_changed,
                     **{f"layer_{x}": layer_status(s, x) for x in LAYERS},
                     "provisional": s.provisional,
                     "isolation": record.get("isolation", "unknown"),
                     "export_content_sha256": s.export_content_sha256, "scored_utc": s.scored_utc})
        print(f"{s.trial_id}: {s.category} (basic_pass={s.basic_pass}, neurosem_pass={s.neurosem_pass}, "
              f"first_failed_layer={s.first_failed_layer})")

    out = Path(a.out).resolve() if a.out else REPO_ROOT / "results" / "agent_study" / f"run_{utc_now()[:10]}"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "trials.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TRIAL_COLUMNS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    n = len(rows)
    commit, dirty = git_state()
    summary = {
        "created_utc": utc_now(), "commit": commit, "tree_dirty": dirty, "trials_scored": n,
        "isolation": record.get("isolation", "unknown"),
        "frozen_config": a.frozen, "frozen_config_sha256": frozen_sha,
        "provisional": any(r["provisional"] for r in rows),
        "counts": {
            "basic_pass": sum(1 for r in rows if r["basic_pass"]),
            "neurosem_pass": sum(1 for r in rows if r["neurosem_pass"]),
            "basic_pass_battery_fail": sum(1 for r in rows if r["basic_pass_battery_fail"]),
            "unauthorized_edits": sum(1 for r in rows if r["unauthorized_edits_detected"]),
            "model_unchanged": sum(1 for r in rows if r["model_changed"] is False),
        },
        "by_layer": {k: sum(1 for r in rows if r["first_failed_layer"] == k)
                     for k in sorted({r["first_failed_layer"] for r in rows if r["first_failed_layer"]})},
        "layer_status_counts": {x: {v: sum(1 for r in rows if r[f"layer_{x}"] == v)
                                    for v in sorted({r[f"layer_{x}"] for r in rows})} for x in LAYERS},
        "scores": [dc.asdict(s) | {"layers": {k: dc.asdict(v) for k, v in s.layers.items()}} for s in scores],
        "interpretation": (
            "basic_pass_battery_fail counts edits that pass the checks a practitioner would normally run "
            "(schema validity, execution, the canonical harness) but fail the perturbation battery. That is the "
            "only quantity this study claims about agents."),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n",
                                      encoding="utf-8", newline="\n")
    status = ("FEASIBILITY PILOT (isolation partial; not the confirmatory agent study)"
              if record.get("isolation") != "full" or summary["provisional"] else "confirmatory")
    lines = ["# Agent study run", "",
             f"*{utc_now()}; commit `{commit}`; {n} trial(s); status: **{status}**.*", "",
             f"- passed basic validation (schema, execution, canonical): **{summary['counts']['basic_pass']} of {n}**",
             f"- passed every layer: **{summary['counts']['neurosem_pass']} of {n}**",
             f"- **passed basic validation but failed the battery: {summary['counts']['basic_pass_battery_fail']} of {n}**",
             f"- unauthorized edits detected: {summary['counts']['unauthorized_edits']}",
             f"- left the model unchanged: {summary['counts']['model_unchanged']}", "",
             "| trial | task type | edit scope | hidden assertions | schema | executes | canonical | battery | category |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['trial_id']}` | {r['task_type']} | {r['layer_edit_scope']} | "
                     f"{r['layer_hidden_assertions_pass']} | {r['layer_schema_valid']} | {r['layer_executes']} | "
                     f"{r['layer_canonical_passes']} | {r['layer_hidden_battery_passes']} | {r['category']} |")
    lines += ["", summary["interpretation"], ""]
    if status.startswith("FEASIBILITY"):
        lines += ["**This run is not the confirmatory agent study.** Isolation was not environmental (the agent "
                  "ran under an account that can read the repository), and/or the evaluation config was not "
                  "frozen. It is reported as harness and feasibility evidence only.", ""]
    (out / "agent_study_run.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines[:9]))
    print(f"\nwrote {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare", help="export clean trial directories")
    p.add_argument("--tasks", nargs="*", help="task ids (default: all nine)")
    p.add_argument("--trials-root", required=True, help="directory OUTSIDE this repository")
    p.add_argument("--replicates", type=int, default=1)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--allow-dirty", action="store_true", help="export from an uncommitted tree (development only)")
    p.add_argument("--isolation", choices=["full", "partial"], default="partial",
                   help="'full' only when the agent account cannot read this repository")
    p.set_defaults(fn=prepare)

    s = sub.add_parser("score", help="score finished trials with the hidden evaluator")
    s.add_argument("--trials-root", required=True)
    s.add_argument("--frozen", default="development", help="path to frozen_agent_eval.yaml, or 'development'")
    s.add_argument("--out", default="")
    s.add_argument("--hidden-root", default="", help="agent_study/hidden (Git-ignored; not present in a worktree)")
    s.set_defaults(fn=score)

    a = ap.parse_args(argv)
    return int(a.fn(a))


if __name__ == "__main__":
    raise SystemExit(main())
