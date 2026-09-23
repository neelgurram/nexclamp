"""Resolve the pre-exposed Pilot 2 variants to their frozen variant ids (amendment A-01).

Operator validation simulated four of the five Pilot 2 models before the campaign, and nine of those
sites are the *same edit* as a frozen mutant: same model, operator, channel, gate and magnitude. For
those nine the canonical-harness outcome is already known, so amendment A-01 requires every primary
result to be reported over all mutants **and** over the subset with no prior exposure.

This script writes that subset as a fixed list, once, so the analysis reads a manifest instead of
recomputing a judgement each time:

    python scripts/pilot2_exposed_variants.py

Output: ``manifests/PILOT2_EXPOSED_VARIANTS.csv``. It matches on the recorded edit, never on an
outcome, and it never drops a variant from the campaign - the frozen matrix is unchanged.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp.provenance import REPO_ROOT, sha256_file, utc_now  # noqa: E402

COLUMNS = ["variant_id", "model_id", "operator", "severity", "channel", "gate", "magnitude",
           "validation_site", "canonical_spikes_before_after", "max_abs_dv_mV", "evidence"]


def site_key(params: dict) -> tuple:
    """What the edit is, independent of the variant id: channel, gate, mechanism, magnitude."""
    return (params.get("channel", ""), params.get("gate", ""), params.get("mechanism", ""),
            params.get("delta_mV", params.get("shift_mV", params.get("factor", ""))))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--validation", default="results/audits/kinetics_pilot2/kinetics_validation.json")
    ap.add_argument("--variants", default="manifests/PILOT2_VARIANTS.csv")
    ap.add_argument("--out", default="manifests/PILOT2_EXPOSED_VARIANTS.csv")
    a = ap.parse_args(argv)

    val_path, var_path = REPO_ROOT / a.validation, REPO_ROOT / a.variants
    for p in (val_path, var_path):
        if not p.is_file():
            print(f"missing input: {p}")
            return 1
    validation = json.loads(val_path.read_text(encoding="utf-8"))
    with open(var_path, newline="", encoding="utf-8") as f:
        frozen = list(csv.DictReader(f))
    index: dict[tuple, list[dict]] = {}
    for v in frozen:
        try:
            params = json.loads(v["params"])
        except (ValueError, TypeError):
            continue
        index.setdefault((v["model_id"], v["operator"], *site_key(params)), []).append(v)

    rows, unmatched = [], 0
    for r in validation["rows"]:
        if r.get("site") is None:
            continue
        params = r.get("params") or {}
        key = (r["fixture"], r["operator"], *site_key(params))
        hits = index.get(key, [])
        if not hits:
            continue
        if len(hits) > 1:
            unmatched += 1          # ambiguous: recorded, never guessed
            continue
        v = hits[0]
        rows.append({"variant_id": v["variant_id"], "model_id": v["model_id"], "operator": v["operator"],
                     "severity": v.get("severity", ""), "channel": params.get("channel", ""),
                     "gate": params.get("gate", ""),
                     "magnitude": params.get("delta_mV", params.get("factor", "")),
                     "validation_site": r["site"],
                     "canonical_spikes_before_after": ";".join(str(x) for x in (r.get("spikes_before_after") or [])),
                     "max_abs_dv_mV": r.get("max_abs_dv_mV", ""),
                     "evidence": a.validation})
    rows.sort(key=lambda x: (x["model_id"], x["operator"]))

    out = REPO_ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {a.out}: {len(rows)} exposed variant(s) over "
          f"{len({r['model_id'] for r in rows})} model(s); sha256 {sha256_file(out)[:16]}...")
    if unmatched:
        print(f"  {unmatched} validation site(s) matched more than one frozen variant and were left out; "
              "they are listed in the overlap audit and must be resolved by hand before reporting")
    for r in rows:
        print(f"  {r['variant_id']:34s} {r['model_id']:22s} {r['operator']:28s} "
              f"canonical spikes {r['canonical_spikes_before_after']}")
    print(f"\nRecorded {utc_now()}. The frozen matrix is unchanged; these variants are reported separately, "
          "never removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
