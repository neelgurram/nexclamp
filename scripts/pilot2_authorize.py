"""Check every automatic-authorisation condition for Pilot 2 and record the answer.

Neel's conditions (2026-09-17). Pilot 2 may start **only** if all of them hold:

1. at least four eligible models that were not used in Pilot 1;
2. the complete post-change test suite passes;
3. a clean end-to-end smoke test;
4. adequate provenance and licensing for every included model;
5. the mutation operators pass their validation tests;
6. the pre-run files are committed;
7. the held-out models are isolated;
8. the Pilot 1 raw data is unchanged;
9. any frozen variant whose outcome was generated outside the campaign is declared by a numbered
   protocol amendment (added 2026-09-18 after the leakage audit, D-055).

Anything that fails stops the run and is reported. This script never simulates and never launches
anything; it writes ``results/audits/pilot2_authorization/<stamp>.json`` and prints the verdict.

    python scripts/pilot2_authorize.py --curation curation-v3
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

from nexclamp import config  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, sha256_file, utc_now  # noqa: E402

PILOT1_MODELS = ("pospischil2008_rs", "pospischil2008_lts")
PRE_RUN_FILES = ("docs/PILOT2_PROTOCOL.md", "configs/pilot2_frozen.yaml", "manifests/PILOT2_MODELS.csv",
                 "manifests/PILOT2_VARIANTS.csv", "manifests/PILOT2_EXPERIMENT_MATRIX.csv",
                 "manifests/PILOT2_PRE_RUN.sha256")


INPUT_PATHS = ("src", "scripts", "tests", "configs", "docs", "manifests", "data", "workflows",
               "pyproject.toml", "requirements.lock", "environment.yml", "Makefile", "Dockerfile")


def inputs_dirty() -> list[str]:
    """Uncommitted changes to the files that define a run (audit and result outputs are excluded).

    Running the readiness sequence and a campaign necessarily writes new files under ``results/``;
    those are outputs, not inputs. What must be committed is everything that decides what runs.
    """
    out = subprocess.run(["git", "status", "--porcelain", "--", *INPUT_PATHS], cwd=REPO_ROOT,
                         capture_output=True, text=True, check=False).stdout
    return [ln[3:] for ln in out.splitlines() if ln.strip()]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False).stdout.strip()


def curation_evidence(campaign: str) -> dict[str, dict]:
    d = config.results_dir() / "processed" / campaign / "curation"
    return {j["model"]["model_id"]: j for j in
            (json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json")))}


def latest(dir_path: Path, pattern: str) -> Path | None:
    files = sorted(dir_path.glob(pattern)) if dir_path.is_dir() else []
    return files[-1] if files else None


def check_models(ev: dict[str, dict], selected: list[str]) -> tuple[list[dict], list[str]]:
    eligible = [m for m, j in ev.items() if j["decision"] == "include_eligible"]
    new_eligible = sorted(set(eligible) - set(PILOT1_MODELS))
    checks = [{"id": "C1_eligible_new_models", "requirement": "at least four eligible models not used in Pilot 1",
               "passed": len(new_eligible) >= 4, "evidence": {"eligible": sorted(eligible), "new": new_eligible}}]
    bad = [m for m in selected if m not in new_eligible]
    checks.append({"id": "C1b_selected_models_are_eligible_and_new", "requirement": "every selected model is eligible "
                   "and was not used in Pilot 1", "passed": not bad,
                   "evidence": {"selected": selected, "not_eligible_or_repeated": bad}})
    lic = {}
    for m in selected:
        j = ev.get(m, {})
        rec, crit = j.get("model", {}), j.get("criteria", {})
        lic[m] = {"license": rec.get("license", ""), "license_url": rec.get("license_url", ""),
                  "citation_recorded": bool(rec.get("citation")), "commit": rec.get("commit", ""),
                  "C01_provenance": crit.get("C01_provenance"), "C02_reuse_rights": crit.get("C02_reuse_rights")}
    ok = all(v["C01_provenance"] and v["C02_reuse_rights"] and v["license"] and "unclear" not in v["license"].lower()
             for v in lic.values())
    checks.append({"id": "C4_provenance_and_licensing", "requirement": "provenance and licensing recorded and clear "
                   "for every included model", "passed": bool(ok), "evidence": lic})
    return checks, new_eligible


def check_suite() -> dict:
    rec = latest(config.results_dir() / "audits" / "readiness", "*/readiness.json")
    if rec is None:
        return {"id": "C2_test_suite", "requirement": "the complete post-change test suite passes", "passed": False,
                "evidence": {"error": "no readiness record under results/audits/readiness/"}}
    j = json.loads(rec.read_text(encoding="utf-8"))
    commit, dirty = git_state()
    pending = inputs_dirty()
    passed = (j.get("failed", 1) == 0 and j.get("errors", 1) == 0 and j.get("commit") == commit
              and not j.get("inputs_dirty", ["unknown"]) and not pending and j.get("all_steps_passed", False))
    return {"id": "C2_test_suite", "requirement": "the complete post-change test suite passes at this commit",
            "passed": bool(passed), "evidence": {"record": rec.relative_to(REPO_ROOT).as_posix(),
                                                 "reported": {k: j.get(k) for k in
                                                              ("passed", "failed", "errors", "skipped", "warnings",
                                                               "commit", "dirty", "duration_s")},
                                                 "head_commit": commit, "tree_dirty": dirty,
                                                 "uncommitted_inputs": pending}}


def check_smoke() -> dict:
    rec = latest(config.results_dir() / "audits" / "smoke_test", "*/smoke_report.json")
    if rec is None:
        return {"id": "C3_smoke_test", "requirement": "a clean end-to-end smoke test", "passed": False,
                "evidence": {"error": "no smoke report"}}
    j = json.loads(rec.read_text(encoding="utf-8"))
    commit, _ = git_state()
    return {"id": "C3_smoke_test", "requirement": "a clean end-to-end smoke test at this commit",
            "passed": bool(j.get("passed")) and j.get("git", {}).get("commit") == commit,
            "evidence": {"record": rec.relative_to(REPO_ROOT).as_posix(), "passed": j.get("passed"),
                         "git": j.get("git"), "head_commit": commit, "steps": j.get("steps")}}


def check_operators() -> dict:
    roots = sorted((config.results_dir() / "audits").glob("kinetics*"))
    reports = {}
    for r in roots:
        f = r / "kinetics_validation.json"
        if f.is_file():
            j = json.loads(f.read_text(encoding="utf-8"))
            reports[r.name] = {"all_sites_passed": j.get("all_sites_passed"),
                               "sites": sum(1 for row in j["rows"] if row.get("site") is not None),
                               "models": sorted({row["fixture"] for row in j["rows"]})}
    return {"id": "C5_operators_validated", "requirement": "the mutation operators pass their validation tests",
            "passed": bool(reports) and all(v["all_sites_passed"] for v in reports.values()),
            "evidence": reports}


def check_prior_exposure() -> dict:
    """No frozen variant's outcome may have been generated outside the campaign without a declaration.

    The gate that authorised the first launch had no such condition, which is how operator-validation
    runs on the Pilot 2 models went unnoticed (D-055). Exposure does not block on its own: it must be
    declared by a numbered protocol amendment that names the affected variants.
    """
    overlap = config.results_dir() / "audits" / "PILOT2_KINETICS_OVERLAP_AUDIT.csv"
    exposed = []
    if overlap.is_file():
        with open(overlap, newline="", encoding="utf-8") as f:
            exposed = [r for r in csv.DictReader(f) if r.get("in_frozen_variant_manifest") == "yes"]
    protocol = (REPO_ROOT / "docs" / "PILOT2_PROTOCOL.md").read_text(encoding="utf-8")
    declared = "Amendment A-01" in protocol and "exposed variants" in protocol.lower()
    return {"id": "C9_prior_outcome_exposure_declared",
            "requirement": "any frozen variant whose outcome was generated outside the campaign is declared in a "
                           "numbered protocol amendment",
            "passed": (not exposed) or declared,
            "evidence": {"exact_overlaps": len(exposed), "declared_by_amendment": declared,
                         "audit": overlap.relative_to(REPO_ROOT).as_posix() if overlap.is_file() else None,
                         "models": sorted({r["model_id"] for r in exposed}),
                         "note": "Declared exposure does not make the campaign confirmatory; it requires the "
                                 "with-and-without reporting rule of amendment A-01."}}


def check_pre_run() -> dict:
    tracked = set(git("ls-files", *PRE_RUN_FILES).splitlines())
    untracked = [f for f in PRE_RUN_FILES if f not in tracked]
    modified = [line[3:] for line in git("status", "--porcelain", "--", *PRE_RUN_FILES).splitlines()]
    manifest = REPO_ROOT / "manifests" / "PILOT2_PRE_RUN.sha256"
    stale = []
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or not line.strip():
                continue
            digest, rel = line.split()[0], line.split()[1]
            p = REPO_ROOT / rel
            if not p.is_file() or sha256_file(p) != digest:
                stale.append(rel)
    return {"id": "C6_pre_run_files_committed", "requirement": "the pre-run files are committed and their hashes match",
            "passed": not untracked and not modified and manifest.is_file() and not stale,
            "evidence": {"untracked": untracked, "modified": modified, "stale_hashes": stale[:20],
                         "n_stale": len(stale)}}


def check_heldout(selected: list[str], ev: dict[str, dict]) -> dict:
    heldout, path = [], REPO_ROOT / "manifests" / "heldout_split.csv"
    if path.is_file():
        with open(path, newline="", encoding="utf-8") as f:
            heldout = [r for r in csv.DictReader(f) if r.get("item_type") == "model"]
    ids = {r["item_id"] for r in heldout}
    families = {ev.get(m, {}).get("model", {}).get("source_family", "") for m in selected}
    clash_ids = sorted(ids & set(selected))
    clash_fam = sorted({r["item_id"] for r in heldout
                        if ev.get(r["item_id"], {}).get("model", {}).get("source_family", "") in families})
    started = (config.results_dir() / "raw" / "pilot2").exists()
    # A campaign that already holds data may only proceed as a declared resumption: the partial run must be
    # recorded with its status and the protocol must carry the amendment that sanctions resuming on the frozen
    # matrix (A-01 section 14.3 rule 6). An undeclared partial run still blocks, as it did before D-055.
    status_file = config.results_dir() / "CAMPAIGN_STATUS_PILOT2.json"
    declared_partial = False
    if status_file.is_file():
        st = json.loads(status_file.read_text(encoding="utf-8"))
        protocol = (REPO_ROOT / "docs" / "PILOT2_PROTOCOL.md").read_text(encoding="utf-8")
        declared_partial = bool(st.get("status")) and "Resumption rule" in protocol
    return {"id": "C7_heldout_isolated", "requirement": "no selected model or source repository is in the held-out "
            "pool, and any existing partial run is a declared resumption",
            "passed": not clash_ids and not clash_fam and (not started or declared_partial),
            "evidence": {"heldout_models": sorted(ids), "clashing_models": clash_ids,
                         "clashing_sources": clash_fam, "pilot2_raw_already_exists": started,
                         "partial_run_declared": declared_partial,
                         "status_file": status_file.relative_to(REPO_ROOT).as_posix() if status_file.is_file()
                         else None}}


def check_pilot1(campaign: str = "pilot") -> dict:
    manifest = config.results_dir() / "processed" / campaign / "ARCHIVE_MANIFEST.sha256"
    raw_root = config.results_dir() / "raw" / campaign
    if not manifest.is_file():
        return {"id": "C8_pilot1_raw_unchanged", "requirement": "the Pilot 1 raw data is unchanged", "passed": False,
                "evidence": {"error": "no archive manifest"}}
    checked = missing = changed = 0
    bad: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split()[0], line.split()[1]
        if not rel.startswith("raw/"):
            continue                        # work_* roots are regenerable scratch, not raw results
        p = raw_root / rel[len("raw/"):]
        checked += 1
        if not p.is_file():
            missing += 1
            bad.append(f"missing {rel}")
        elif sha256_file(p) != digest:
            changed += 1
            bad.append(f"changed {rel}")
    return {"id": "C8_pilot1_raw_unchanged", "requirement": "every archived Pilot 1 raw file still has its recorded "
            "hash", "passed": checked > 0 and not missing and not changed,
            "evidence": {"files_checked": checked, "missing": missing, "changed": changed, "examples": bad[:10]}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--curation", required=True)
    ap.add_argument("--pilot-config", default="configs/pilot2_frozen.yaml")
    a = ap.parse_args(argv)
    cfg = yaml.safe_load((REPO_ROOT / a.pilot_config).read_text(encoding="utf-8"))
    selected = list(cfg["pilot"]["models"])
    ev = curation_evidence(a.curation)

    checks, new_eligible = check_models(ev, selected)
    checks += [check_suite(), check_smoke(), check_operators(), check_pre_run(),
               check_heldout(selected, ev), check_pilot1(), check_prior_exposure()]
    commit, dirty = git_state()
    authorized = all(c["passed"] for c in checks)
    record = {"created_utc": utc_now(), "commit": commit, "tree_dirty": dirty, "curation_campaign": a.curation,
              "pilot_config": a.pilot_config, "selected_models": selected, "eligible_new_models": new_eligible,
              "checks": checks, "authorized": authorized,
              "note": "Automatic authorisation under Neel's 2026-09-17 conditions. Any failed condition stops the "
                      "run and is reported; nothing is launched by this script."}
    out = config.results_dir() / "audits" / "pilot2_authorization"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{utc_now().replace(':', '').replace('-', '')}.json"
    path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8", newline="\n")
    for c in checks:
        print(f"[{'PASS' if c['passed'] else 'FAIL'}] {c['id']}: {c['requirement']}")
        if not c["passed"]:
            print(f"        evidence: {json.dumps(c['evidence'], default=str)[:400]}")
    print(f"\n{'AUTHORIZED' if authorized else 'NOT AUTHORIZED'} - record: {path.relative_to(REPO_ROOT).as_posix()}")
    return 0 if authorized else 1


if __name__ == "__main__":
    raise SystemExit(main())
