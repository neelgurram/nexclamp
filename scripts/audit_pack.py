"""Build a human audit pack: everything a person needs to check mutants, in one readable document.

The specification requires a person to audit at least 20 mutants before any claim rests on them
(Milestone 4 exit criterion). The campaign already writes ``mutant_audit_sheet.csv``, but a bare CSV
of XML locators is not something a human can actually audit: the evidence is scattered across
per-variant directories.

This produces two files in one place:

- ``AUDIT_PACK.md`` - one section per sampled mutant, with the exact edit (old value -> new value,
  file and element), the recorded classification, which protocols detected it, and the diagnostic
  the campaign wrote. Readable top to bottom, no repository navigation needed.
- ``AUDIT_SHEET.csv`` - the same mutants as rows with empty verdict columns to fill in.

The pack states what the assistant already believes and asks the auditor to disagree where the
evidence does not support it. It never fills a verdict column.

    python scripts/audit_pack.py --campaign pilot2 --n 20
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp import config  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

VERDICT_COLUMNS = ["human_auditor", "edit_matches_label_yes_no", "class_plausible_yes_no",
                   "detection_plausible_yes_no", "notes"]


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def describe_edits(raw: str) -> list[str]:
    """Turn the recorded edit JSON into lines a person can check against the model file."""
    try:
        edits = json.loads(raw or "[]")
    except (ValueError, TypeError):
        return [f"unparsed edit record: {raw[:200]}"]
    out = []
    for e in edits:
        loc = e.get("locator") or e.get("file") or "?"
        attr = e.get("attribute", "?")
        old, new = e.get("old", "?"), e.get("new", "?")
        out.append(f"`{e.get('file', '?')}` · `{loc}` · **{attr}**: `{old}` → `{new}`")
    return out or ["no edit recorded"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--n", type=int, default=20, help="mutants to sample (the exit criterion is 20)")
    ap.add_argument("--seed", type=int, default=0, help="0 uses the study seed, for a reproducible sample")
    ap.add_argument("--out", default="")
    ap.add_argument("--variants", default="", help="comma-separated ids to audit instead of a random sample")
    ap.add_argument("--title", default="", help="heading suffix, e.g. 'targeted: canonical survivors'")
    a = ap.parse_args(argv)

    processed = config.results_dir() / "processed" / a.campaign
    sheet = read_csv(processed / "mutant_audit_sheet.csv")
    cls = {r["variant_id"]: r for r in read_csv(processed / "classification.csv")}
    if not sheet:
        print(f"no mutant_audit_sheet.csv under {processed}")
        return 1
    seed = a.seed or int(config.study()["selection"]["seed"])
    rng = random.Random(seed)
    pool = sorted(sheet, key=lambda r: r["variant_id"])
    if a.variants:
        wanted = [v.strip() for v in a.variants.split(",") if v.strip()]
        by_id = {r["variant_id"]: r for r in pool}
        missing = [v for v in wanted if v not in by_id]
        if missing:
            print(f"not in the audit sheet: {missing}")
            return 1
        sample = [by_id[v] for v in wanted]
    else:
        sample = pool if len(pool) <= a.n else rng.sample(pool, a.n)
    sample.sort(key=lambda r: (r.get("operator", ""), r["variant_id"]))

    out = Path(a.out) if a.out else processed / "audit"
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    commit, dirty = git_state()

    how = (f"chosen by name ({a.title or 'targeted'}), not sampled" if a.variants
           else f"sampled with seed {seed} so the selection is reproducible")
    L = [f"# Audit pack: campaign `{a.campaign}`" + (f" ({a.title})" if a.title else ""), "",
         f"*{len(sample)} of {len(pool)} mutants, {how}. "
         f"Generated {utc_now()} at commit `{commit}` (tree dirty: {dirty}).*", "",
         "## How to audit", "",
         "For each mutant below, three questions. They take a minute each once you have the model file open.", "",
         "1. **Does the edit match its label?** The operator name claims a specific kind of change "
         "(a conductance scaled, a reversal potential shifted, a channel reference broken). Read the "
         "old → new values and say whether that is what happened.",
         "2. **Is the assigned class plausible?** `5_non_equivalent` means the behaviour changed "
         "reproducibly; `4_equivalent_within_tested_domain` means it did not; `2_non_executable` means "
         "the model would not run. Does that match the diagnostic?",
         "3. **Is the detection plausible?** If protocols are listed as detecting it, does the "
         "diagnostic show a difference big enough to believe?", "",
         "Record your answers in `AUDIT_SHEET.csv`. **Disagreement is the useful output** - if an edit "
         "looks mislabelled or a class looks wrong, say so; that is what the audit is for.", "",
         "---", ""]

    for i, r in enumerate(sample, 1):
        vid = r["variant_id"]
        c = cls.get(vid, {})
        L += [f"## {i}. `{vid}`", "",
              f"- **operator**: `{r.get('operator', '')}`  ·  **family**: {r.get('family', '')}",
              f"- **assigned class**: `{c.get('class', r.get('assigned_class', ''))}`",
              f"- **detected by**: {c.get('detecting_protocols') or r.get('detecting_protocols') or 'nothing'}",
              f"- **structurally valid**: {c.get('structural_valid', '?')}  ·  "
              f"**execution overrides**: {r.get('exec_overrides') or 'none'}", "",
              "**The edit**", ""]
        L += [f"- {line}" for line in describe_edits(r.get("edits", ""))]
        diag = processed / "variants" / vid / "diagnostic.md"
        if diag.is_file():
            text = diag.read_text(encoding="utf-8").strip()
            body = "\n".join(text.splitlines()[:26])
            L += ["", "**Diagnostic recorded by the campaign**", "", "```", body, "```"]
        else:
            L += ["", "*No diagnostic file for this variant.*"]
        L += ["", "**Your verdict** — edit matches label? · class plausible? · detection plausible? · notes", "",
              "---", ""]

    (out / "AUDIT_PACK.md").write_text("\n".join(L), encoding="utf-8", newline="\n")

    rows = []
    for r in sample:
        c = cls.get(r["variant_id"], {})
        rows.append({"variant_id": r["variant_id"], "operator": r.get("operator", ""),
                     "family": r.get("family", ""), "assigned_class": c.get("class", ""),
                     "detecting_protocols": c.get("detecting_protocols", ""),
                     **{k: "" for k in VERDICT_COLUMNS}})
    cols = ["variant_id", "operator", "family", "assigned_class", "detecting_protocols", *VERDICT_COLUMNS]
    with open(out / "AUDIT_SHEET.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {(out / 'AUDIT_PACK.md').relative_to(REPO_ROOT).as_posix()} "
          f"and AUDIT_SHEET.csv ({len(rows)} mutants, seed {seed})")
    print("The pack is self-contained: edits, classes, detections and diagnostics are inline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
