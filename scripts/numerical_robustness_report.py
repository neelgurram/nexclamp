"""Derived, read-only reanalysis of a sealed campaign's numerical mutants (DECISIONS D-030).

Pilot 1 ran before the semantic/numerical split. This script leaves the sealed campaign untouched
and writes to ``results/derived/<campaign>/``:

- ``reclassification.csv``: every mutant with its original class, its stratum, and a label that
  never calls a numerical result semantic drift; time-step mutants carry the unequal-setting note;
- ``numerical_robustness.csv``: per (protocol, feature) deviation of each numerical mutant versus
  the reference's own h / h/2 / h/4 discretisation error (h/4 exists for references only);
- ``primary_semantic_summary.json``: Pilot 1 class counts and the in-sample battery-vs-canonical
  paired counts recomputed over the semantic stratum only.

Example::

    python scripts/numerical_robustness_report.py --campaign pilot
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml  # noqa: E402

from neuraxis import config  # noqa: E402
from neuraxis.experiments import strata  # noqa: E402
from neuraxis.protocols.definitions import CANONICAL_ID  # noqa: E402
from neuraxis.provenance import utc_now  # noqa: E402
from neuraxis.schemas import MutantClass, VariantKind  # noqa: E402
from neuraxis.selection.matrix import DetectionMatrix  # noqa: E402
from neuraxis.validation.fingerprint import load_fingerprint  # noqa: E402

INCREASE_DT_NOTE = ("confound: the canonical harness and the battery started from different base steps "
                    "(harness step x factor versus nominal battery step x factor), so canonical and battery "
                    "detections are not comparable for this mutant")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    results = config.results_dir()
    proc = results / "processed" / a.campaign
    out = results / "derived" / a.campaign
    out.mkdir(parents=True, exist_ok=True)
    tol_file = proc / "config_snapshot" / "tolerances.yaml"
    c = float(yaml.safe_load(tol_file.read_text(encoding="utf-8"))["c_refinement"])
    work_variants = config.work_dir() / "variants" / a.campaign / "mutants"

    cls = list(csv.DictReader(open(proc / "classification.csv", encoding="utf-8")))
    recl, nr_rows = [], []
    for r in cls:
        if r["kind"] != VariantKind.MUTANT.value:
            continue
        s = strata.stratum(r["kind"], r["family"], r["operator"])
        klass = MutantClass(r["class"])
        vfile = work_variants / r["model_id"] / r["variant_id"] / "variant.json"
        exec_overrides = json.loads(vfile.read_text(encoding="utf-8")).get("exec_overrides", {}) if vfile.is_file() else {}
        recl.append({"variant_id": r["variant_id"], "model_id": r["model_id"], "family": r["family"],
                     "operator": r["operator"], "params": r["params"], "exec_overrides": json.dumps(exec_overrides),
                     "original_class": r["class"], "stratum": s, "interpretation": strata.interpretation(s, klass),
                     "in_primary_semantic_denominator": s == strata.SEMANTIC and klass.admissible,
                     "note": INCREASE_DT_NOTE if r["operator"] == "increase_dt" else ""})
        if s != strata.NUMERICAL:
            continue
        ref_dir = proc / "references" / r["model_id"]
        ref_fps = {f: load_fingerprint(ref_dir / f"fingerprint_L{f}.json") for f in (1, 2, 4)
                   if (ref_dir / f"fingerprint_L{f}.json").is_file()}
        vdir = proc / "variants" / r["variant_id"]
        var_fps = {f: load_fingerprint(vdir / f"fingerprint_L{f}.json") for f in (1, 2, 4)
                   if (vdir / f"fingerprint_L{f}.json").is_file()}
        if ref_fps and var_fps:
            v = SimpleNamespace(variant_id=r["variant_id"], model_id=r["model_id"], operator=r["operator"],
                                exec_overrides=exec_overrides)
            nr_rows += strata.numerical_robustness_rows(ref_fps, var_fps, v, c)

    def write(path: Path, rows: list[dict]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["empty"], lineterminator="\n")
            w.writeheader()
            w.writerows(rows)

    write(out / "reclassification.csv", recl)
    write(out / "numerical_robustness.csv", nr_rows)

    m = DetectionMatrix.from_csv(proc / "detection_matrix.csv")
    keep = [i for i, mid in enumerate(m.mutant_ids) if m.family_of[mid] in strata.SEMANTIC_FAMILIES]
    sem = m.take_rows(keep)
    battery = [p for p in sem.protocol_ids if p != CANONICAL_ID]
    can, bat = sem.covered([CANONICAL_ID]), sem.covered(battery)
    summary = {
        "campaign": a.campaign, "created_utc": utc_now(), "status": "exploratory, derived from a sealed campaign",
        "classes_by_stratum": {s: dict(Counter(x["original_class"] for x in recl if x["stratum"] == s))
                               for s in sorted({x["stratum"] for x in recl})},
        "primary_semantic_admissible": int(sem.n_mutants),
        "primary_semantic_silent": sum(1 for x in recl if x["stratum"] == strata.SEMANTIC
                                       and x["original_class"] == MutantClass.SILENT.value),
        "numerical_rows_removed_from_matrix": int(m.n_mutants - sem.n_mutants),
        "paired_in_sample_semantic": {"both": int((can & bat).sum()), "battery_only": int((bat & ~can).sum()),
                                      "canonical_only": int((can & ~bat).sum()), "neither": int((~can & ~bat).sum())},
        "numerical_label_counts": dict(Counter(x["label"] for x in nr_rows)),
    }
    (out / "primary_semantic_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
