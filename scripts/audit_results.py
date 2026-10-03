"""Combine the two returned human-audit packets into one record, and compare them.

Reads the auditors' own files in ``results/tables/<campaign>/audit/returned/``: the Word packet is
parsed from its tables, the PDF by the position of each X inside its answer box. Neither file is
modified. The verdicts are written out as a CSV and a readable summary, together with:

- agreement between the two auditors on each question;
- agreement with the automated re-check (``AUTOMATED_CHECK.csv``), which the auditors did not use;
- every fault where either auditor answered anything other than Yes, with their notes quoted.

Resolutions are not invented here. Where a flag needs a decision from the auditor, the record says
so and leaves it open.

    python scripts/audit_results.py --campaign heldout-v1
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp import config  # noqa: E402
from nexclamp.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
QUESTIONS = {"Q1": "edit matches its label", "Q2": "assigned class plausible", "Q3": "detection plausible"}


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"Human audit packet . page \d+", "", s)).strip()


def from_docx(path: Path) -> tuple[dict, dict]:
    """Verdicts and header box from a returned Word packet."""
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    text = lambda c: " ".join("".join(t.text or "" for t in p.iter(W + "t")).strip()  # noqa: E731
                              for p in c.iter(W + "p")).strip()
    out, header = {}, {}
    for tb in root.iter(W + "tbl"):
        rows = [[text(c) for c in r.iter(W + "tc")] for r in tb.iter(W + "tr")]
        if not rows:
            continue
        flat = " ".join(rows[0])
        if "Auditor name" in flat or any("Auditor name" in " ".join(r) for r in rows):
            header = {r[0]: r[1] for r in rows if len(r) > 1}
            continue
        m = re.search(r"answers for fault (\d+)", flat)
        if not m:
            continue
        n, rec = int(m.group(1)), {}
        for r in rows[1:]:
            q = re.match(r"(Q[123])", r[0])
            if q and len(r) >= 4:
                choice = [c for c, v in zip(("Yes", "No", "Unsure", "N/A"), r[1:5]) if v.strip().upper() == "X"]
                rec[q.group(1)] = choice[0] if choice else ""
            elif r[0].startswith("Confidence"):
                rec["confidence"] = next((c for c in ("High", "Medium", "Low")
                                          if any(c in v and "X" in v.upper() for v in r[1:])), "")
            elif r[0].startswith("Notes"):
                rec["note"] = clean(r[0].split(":", 1)[1]) if ":" in r[0] else ""
        out[n] = rec
    return out, header


def from_pdf(path: Path) -> tuple[dict, dict]:
    """Verdicts and header box from a returned PDF packet, read by X position in each answer box."""
    import fitz
    doc = fitz.open(path)
    out: dict[int, dict] = {}
    cur, cols = None, {}
    for page in doc:
        words = page.get_text("words")
        hdr = [w for w in words if w[4] == "answers"]
        if hdr:
            hy = hdr[0][1]
            nums = [w for w in words if abs(w[1] - hy) < 4 and w[4].isdigit()]
            if nums:
                cur = int(nums[0][4])
                out.setdefault(cur, {})
            c = {w[4]: (w[0] + w[2]) / 2 for w in words if abs(w[1] - hy) < 6
                 and w[4] in ("Yes", "No", "Unsure", "N/A")}
            if len(c) >= 3:
                cols = c
        if cur is None or not cols:
            continue
        for label, key in (("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Confidence:", "confidence")):
            lab = [w for w in words if w[4] == label]
            if not lab:
                continue
            ry = lab[0][1]
            marks = [w for w in words if abs(w[1] - ry) < 6 and w[4].upper() == "X" and w[0] > 150]
            if not marks:
                continue
            opts = ({w[4]: (w[0] + w[2]) / 2 for w in words if abs(w[1] - ry) < 6
                     and w[4] in ("High", "Medium", "Low")} if key == "confidence" else cols)
            if opts:
                out[cur][key] = min(opts, key=lambda o: min(abs(opts[o] - (m[0] + m[2]) / 2) for m in marks))
        m = re.search(r"Notes \(required for any No or Unsure\):\s*(.*?)(?:\n\s*\n|\Z)", page.get_text(), re.S)
        if m and len(clean(m.group(1))) > 3:
            out[cur]["note"] = clean(out[cur].get("note", "") + " " + clean(m.group(1)))[:600]
    first = doc[0].get_text()
    hm = re.search(r"Auditor name\s*\n(.*?)\n", first)
    am = re.search(r"check \(Yes / No\)\s*\n(\w+)", first)
    return out, {"Auditor name": hm.group(1).strip() if hm else "", "worked alone / unseen check": am.group(1) if am else ""}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    audit = config.results_dir() / "tables" / a.campaign / "audit"
    returned = audit / "returned"
    kit = json.loads((audit / "kit" / "build" / "kit.json").read_text(encoding="utf-8"))
    ids = {f["n"]: f for f in kit["faults"]}
    auto = {r["variant_id"]: r for r in csv.DictReader(open(audit / "AUTOMATED_CHECK.csv", encoding="utf-8"))}

    auditors = {}
    # A corrected return supersedes the first one; the original stays in the folder as evidence.
    for p in sorted(returned.glob("Audit_Packet_*")):
        if "_firstreturn" in p.stem:
            continue
        name = p.stem.replace("Audit_Packet_", "").replace(".docx", "")
        auditors[name] = from_docx(p) if p.suffix == ".docx" else from_pdf(p)

    names = sorted(auditors)
    rows = []
    for n in sorted(ids):
        f = ids[n]
        row = {"fault": n, "variant_id": f["variant_id"], "model_id": f["model_id"],
               "operator": f["operator"], "assigned_class": f["assigned_class"]}
        for who in names:
            v = auditors[who][0].get(n, {})
            for q in QUESTIONS:
                row[f"{who}_{q}"] = v.get(q, "")
            row[f"{who}_confidence"] = v.get("confidence", "")
            row[f"{who}_note"] = v.get("note", "")
        for q in QUESTIONS:
            row[f"agree_{q}"] = "yes" if len({row[f"{w}_{q}"] for w in names}) == 1 else "no"
        ac = auto.get(f["variant_id"], {})
        row["automated_flag"] = ac.get("flag", "") or "clear"
        rows.append(row)

    cols = list(rows[0])
    with open(audit / "HUMAN_AUDIT_RESULTS.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    commit, dirty = git_state()
    L = ["# Human audit: returned verdicts", "",
         f"*{len(rows)} faults, {len(names)} auditors. Compiled {utc_now()} at commit `{commit[:12]}` "
         f"(tree dirty: {dirty}) by `scripts/audit_results.py` from the auditors' own returned files in "
         "`returned/`, which are preserved unmodified.*", "", "## Auditors", ""]
    for who in names:
        hdr = auditors[who][1]
        L.append(f"- **{who}**: " + "; ".join(f"{k}: {v}" for k, v in hdr.items() if v))
    conditions = audit / "AUDIT_CONDITIONS.md"
    if conditions.is_file():                       # hand-written record of how the audit was run
        L += ["", conditions.read_text(encoding="utf-8").strip()]
    L += ["", "## Verdict counts", "",
          "| Question | " + " | ".join(names) + " | both answered the same |", "|---|" + "---|" * (len(names) + 1)]
    for q, meaning in QUESTIONS.items():
        cells = []
        for who in names:
            c: dict[str, int] = {}
            for r in rows:
                c[r[f"{who}_{q}"] or "(blank)"] = c.get(r[f"{who}_{q}"] or "(blank)", 0) + 1
            cells.append(", ".join(f"{k} {v}" for k, v in sorted(c.items())))
        same = sum(r[f"agree_{q}"] == "yes" for r in rows)
        L.append(f"| **{q}** ({meaning}) | " + " | ".join(cells) + f" | {same}/{len(rows)} |")
    L += ["", "## Faults where either auditor did not answer Yes", ""]
    for r in rows:
        flagged = [q for q in QUESTIONS if any(r[f"{w}_{q}"] not in ("Yes", "") for w in names)]
        if not flagged:
            continue
        L += [f"### Fault {r['fault']}: `{r['variant_id']}`", "",
              f"- {r['model_id']}, operator `{r['operator']}`, assigned class `{r['assigned_class']}`",
              "- " + "; ".join(f"{w}: " + ", ".join(f"{q}={r[f'{w}_{q}'] or '-'}" for q in QUESTIONS)
                               for w in names),
              f"- automated re-check: {r['automated_flag']}"]
        for w in names:
            if r[f"{w}_note"]:
                L.append(f"- *{w}*: \"{r[f'{w}_note']}\"")
        L.append("")
    (audit / "HUMAN_AUDIT_RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

    print(f"{len(rows)} faults; auditors: {', '.join(names)}")
    for q in QUESTIONS:
        print(f"  {q}: identical verdicts on {sum(r[f'agree_{q}'] == 'yes' for r in rows)}/{len(rows)} faults")
    print(f"wrote {(audit / 'HUMAN_AUDIT_RESULTS.md').relative_to(REPO_ROOT).as_posix()} and .csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
