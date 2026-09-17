"""Prepare the fixed Pilot 2 matrix: model, variant, experiment and pre-run manifests.

Generates variants **without simulating anything** (a dry run in a temporary directory) so the exact
matrix is known and hashed before execution, then writes:

- ``manifests/PILOT2_MODELS.csv``: the included models with provenance, licence, curation criteria and
  response type;
- ``manifests/PILOT2_VARIANTS.csv``: every planned variant with operator, analysis family, severity
  and the recorded edit;
- ``manifests/PILOT2_EXPERIMENT_MATRIX.csv``: one row per planned simulation unit
  (variant x protocol x refinement level), with the validation levels it feeds;
- ``manifests/PILOT2_PRE_RUN.sha256``: hashes of the protocol, configuration, model manifest, model
  snapshots, environment lock files and analysis code.

    NEURAXIS_STUDY_CONFIG=configs/pilot2_frozen.yaml python scripts/pilot2_prepare.py --curation curation-v3
"""

from __future__ import annotations

import argparse
import csv
import dataclasses as dc
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neuraxis import config  # noqa: E402
from neuraxis.experiments import strata  # noqa: E402
from neuraxis.mutations import severity as sev  # noqa: E402
from neuraxis.orchestration.curation import read_candidates  # noqa: E402
from neuraxis.protocols.definitions import CANONICAL_ID, batched, templates_from_config  # noqa: E402
from neuraxis.provenance import REPO_ROOT, sha256_file, utc_now  # noqa: E402

SOURCES = ("data/model_manifest.csv", "data/model_candidates.csv", "data/model_candidates_sweep2.csv")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = list(dict.fromkeys(k for r in rows for k in r)) if rows else ["empty"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def curation_evidence(campaign: str) -> dict[str, dict]:
    out = {}
    d = config.results_dir() / "processed" / campaign / "curation"
    for f in sorted(d.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        out[j["model"]["model_id"]] = j
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--curation", required=True, help="curation campaign whose evidence justifies inclusion")
    ap.add_argument("--protocol", default="docs/PILOT2_PROTOCOL.md")
    a = ap.parse_args(argv)
    cfg = config.study()
    pilot = cfg["pilot"]
    models = {m.model_id: m for m in read_candidates([REPO_ROOT / s for s in SOURCES])}
    evidence = curation_evidence(a.curation)
    seed = int(cfg["selection"]["seed"])

    rows = []
    for mid in pilot["models"]:
        m, ev = models[mid], evidence.get(mid, {})
        e = ev.get("evidence", {})
        rows.append({"model_id": mid, "name": m.name, "source_family": m.source_family, "citation": m.citation,
                     "snapshot": m.snapshot, "commit": m.commit, "license": m.license, "license_url": m.license_url,
                     "curation_campaign": a.curation, "curation_decision": ev.get("decision", "not curated"),
                     "curation_open_criteria": ";".join(ev.get("reasons", [])),
                     **{k: ("" if v is None else ("pass" if v else "fail")) for k, v in ev.get("criteria", {}).items()},
                     "response_type_P05": e.get("firing_regime_P05", ""), "rebound_spikes_P08": e.get("rebound_spikes_P08", ""),
                     "sag_ratio_P07": e.get("sag_ratio_P07", ""), "rheobase_nA": e.get("rheobase_nA", ""),
                     "ion_channels": ";".join(e.get("ion_channels", [])),
                     "estimated_variant_runtime_s": e.get("estimated_variant_runtime_s", ""),
                     "semantic_operators_with_site": ";".join(e.get("semantic_operators_with_site", []))})
    write_csv(REPO_ROOT / "manifests" / "PILOT2_MODELS.csv", rows)

    from neuraxis import mutations, transforms

    ops = strata.select_mutation_operators(pilot["mutation_families"], pilot.get("exclude_operators") or [])
    levels = list(pilot.get("severity_levels") or [])
    per = dict(pilot.get("sites_per_severity") or {})
    variants, matrix = [], []
    templates = batched(templates_from_config(cfg["protocols"]))
    factors = [int(f) for f in cfg["numerics"]["refinement_factors"]]
    with tempfile.TemporaryDirectory(prefix="neuraxis_pilot2_") as tmp:
        for mid in pilot["models"]:
            model = models[mid]

            def selector(op, sites, seed=seed):
                return sev.select_sites(sites, op.name, seed, levels, int(per.get(op.name, per.get("default", 1))),
                                        int(pilot.get("sites_without_severity", 1)))

            recs = mutations.generate_mutants(model, ops, int(pilot["mutants_per_operator"]), seed,
                                              Path(tmp) / "m" / mid, selector=selector)
            recs += transforms.generate_transforms(model, list(transforms.REGISTRY),
                                                   int(pilot["transforms_per_operator"]), seed, Path(tmp) / "t" / mid)
            for r in recs:
                variants.append({"model_id": mid, "variant_id": r.variant_id, "kind": r.kind.value, "family": r.family,
                                 "analysis_family": strata.analysis_family(r.operator, r.family),
                                 "stratum": strata.variant_stratum(r), "operator": r.operator,
                                 "severity": sev.severity(r.params), "params": json.dumps(r.params, sort_keys=True),
                                 "edits": json.dumps([dc.asdict(e) for e in r.edits]),
                                 "exec_overrides": json.dumps(r.exec_overrides),
                                 "tree_sha256": r.tree_sha256, "parent_tree_sha256": r.parent_tree_sha256})
                for pid in [CANONICAL_ID, *[t.protocol_id for t in templates]]:
                    for f in (1, 2, 4):
                        matrix.append({"model_id": mid, "variant_id": r.variant_id, "protocol_id": pid,
                                       "refinement_level": f"h/{f}" if f > 1 else "h",
                                       "planned": "always" if f == 1 else
                                                  ("if detected at h" if f == 2 else "if an apparent canonical survivor"),
                                       "validation_levels": "B,C" if pid == CANONICAL_ID else "D,E"})
    write_csv(REPO_ROOT / "manifests" / "PILOT2_VARIANTS.csv", variants)
    write_csv(REPO_ROOT / "manifests" / "PILOT2_EXPERIMENT_MATRIX.csv", matrix)

    manifest = ["# Pilot 2 pre-run SHA-256 manifest (neuron_model_behavioral_validation)",
                f"# created {utc_now()}; protocol {a.protocol}; study config {config.study_config_path().relative_to(REPO_ROOT).as_posix()}",
                "# format: sha256  path  [category]"]
    files = [(a.protocol, "protocol"), (config.study_config_path().relative_to(REPO_ROOT).as_posix(), "config")]
    files += [(f"configs/{n}", "config") for n in ("features.yaml", "tolerances.yaml")]
    files += [("data/model_manifest.csv", "model_manifest"), ("requirements.lock", "environment"),
              ("pyproject.toml", "environment"), ("environment.yml", "environment"),
              (".tools/jdk_provenance.json", "environment")]
    files += [(f"manifests/{n}", "matrix") for n in ("PILOT2_MODELS.csv", "PILOT2_VARIANTS.csv",
                                                     "PILOT2_EXPERIMENT_MATRIX.csv")]
    snaps = sorted({models[m].snapshot for m in pilot["models"]})
    for snap in snaps:
        for root in ("models/raw", "models/candidates"):
            d = REPO_ROOT / root / snap
            if d.is_dir():
                files += [(p.relative_to(REPO_ROOT).as_posix(), "model_snapshot") for p in sorted(d.rglob("*"))
                          if p.is_file()]
                break
    tracked = subprocess.run(["git", "ls-files", "src", "scripts", "tests", "workflows"], cwd=REPO_ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
    files += [(f, "analysis_code") for f in sorted(tracked) if (REPO_ROOT / f).is_file() and "__pycache__" not in f]
    body = [f"{sha256_file(REPO_ROOT / rel)}  {rel}  [{cat}]" for rel, cat in files if (REPO_ROOT / rel).is_file()]
    (REPO_ROOT / "manifests" / "PILOT2_PRE_RUN.sha256").write_text("\n".join(manifest + body) + "\n",
                                                                   encoding="utf-8", newline="\n")
    print(f"models {len(rows)}; variants {len(variants)} "
          f"(mutants {sum(1 for v in variants if v['kind'] == 'mutant')}, "
          f"controls {sum(1 for v in variants if v['kind'] != 'mutant')}); matrix rows {len(matrix)}; "
          f"manifest entries {len(body)}")
    for mid in pilot["models"]:
        mv = [v for v in variants if v["model_id"] == mid]
        print(f"  {mid}: {sum(1 for v in mv if v['kind'] == 'mutant')} mutants, "
              f"{sum(1 for v in mv if v['kind'] != 'mutant')} controls, "
              f"families {sorted({v['analysis_family'] for v in mv if v['kind'] == 'mutant'})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
