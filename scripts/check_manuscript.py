"""Check the manuscript against the recorded results and the journal's formal requirements.

Three kinds of check, all mechanical:

1. **Numbers.** Every headline figure in the text is compared with ``verified_numbers.json``, which is
   extracted from the sealed campaign outputs. A claim that does not appear verbatim is reported, so a
   number can never drift from the data it came from.
2. **Citations.** Every author-year citation in the text must have an entry in the reference list, and
   every reference must be cited at least once.
3. **Journal rules** (Neuroinformatics, Springer Nature): abstract 150-250 words, 4-6 keywords, at most
   three heading levels, required sections present, Information Sharing Statement immediately before
   the declarations, and no "available on request" wording (the journal forbids it).

    python scripts/check_manuscript.py --manuscript docs/manuscript/MANUSCRIPT_V2.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def strip_accents(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def surname(s: str) -> str:
    """Last name as APA writes it, keeping compound names such as Van Geit or Le Traon together."""
    return strip_accents(s).strip().rstrip(",.").replace("  ", " ")


def expected_claims(f: dict) -> list[tuple[str, str]]:
    """(what it is, the exact string that must appear in the manuscript)."""
    pe, lv, ca = f["counts"], f["levels"], f["cascade"]
    return [
        ("admissible faults", f"{pe['n']}"),
        ("canonical detected", f"{pe['both'] + pe['only_b']} of {pe['n']}"),
        ("battery detected", f"{pe['both'] + pe['only_a']} of {pe['n']}"),
        ("canonical rate", f"{f['can']:.3f}"),
        ("battery rate", f"{f['bat']:.3f}"),
        ("difference", f"{f['diff']:.3f}"),
        ("interval low", f"{f['ci'][0]:.3f}"),
        ("interval high", f"{f['ci'][1]:.3f}"),
        ("McNemar p", f"{f['mcnemar']:.3f}"),
        ("permutation p", f"{f['perm']:.3f}"),
        ("smallest attainable p", f"{f['perm_min']:.3f}"),
        ("paired counts both", f"both {pe['both']}"),
        ("paired counts battery only", f"battery only {pe['only_a']}"),
        ("paired counts canonical only", f"canonical only {pe['only_b']}"),
        ("faults generated", f"{ca['total_mutants']}"),
        ("schema valid", f"{ca['schema_valid']}"),
        ("executable", f"{ca['executable']}"),
        ("numerically stable", f"{ca['numerically_stable']}"),
        ("equivalent", f"{ca['equivalent_within_tested_domain']}"),
        ("any-change denominator", f"{lv['n']}"),
        ("canonical features", f"detected {lv['B_features']}"),
        ("canonical trace", f"trace {lv['C_full_trace']}"),
        ("either level", f"either {lv['B_or_C']}"),
        ("neither level", f"neither {lv['neither']}"),
        ("controls", f"0 of {f['evidence']['n_controls']}"),
        ("silent survival", f"{f['S2']['rate']:.3f}"),
        ("count-matched share", f"{f['S1']['count_matched']['p_rand']:.3f}"),
        ("runtime-matched share", f"{f['S1']['runtime_matched']['p_rand']:.3f}"),
        ("random count-matched mean", f"{f['S1']['count_matched']['mean']:.3f}"),
        ("random runtime-matched mean", f"{f['S1']['runtime_matched']['mean']:.3f}"),
        ("source-family interval low", f"{f['sens_family']['cluster_ci'][0]:.3f}"),
        ("source-family interval high", f"{f['sens_family']['cluster_ci'][1]:.3f}"),
    ]


def check_numbers(text: str, f: dict) -> list[str]:
    return [f"missing or wrong: {what} (expected {want!r})" for what, want in expected_claims(f) if want not in text]


def check_citations(text: str, refs: str) -> list[str]:
    problems = []
    body = text.split("## References")[0]
    cited = set()
    for m in re.finditer(r"\(([^()]*?\d{4}[a-z]?)\)", body):          # (Author, 2011; Other et al., 2016)
        for part in m.group(1).split(";"):
            mm = re.match(r"\s*((?:[A-Z][\w'’-]+)(?:\s+(?:van|von|de|der|den|Le|La|Van|Von|De)?\s*[A-Z][\w'’-]+)*?)"
                          r"(?:\s*(?:et al\.|&\s*[A-Z][\w'’-]+(?:\s+[A-Z][\w'’-]+)*))?,\s*(\d{4})", part.strip())
            if mm:
                cited.add((surname(mm.group(1)), mm.group(2)))
    for m in re.finditer(r"((?:[A-Z][\w'’-]+)(?:\s+[A-Z][\w'’-]+)*?)(?:\s+et al\.|\s+&\s+[A-Z][\w'’-]+)?"
                         r"\s*\((\d{4})\)", body):                                                    # narrative
        cited.add((surname(m.group(1)), m.group(2)))
    entries = {}
    for line in refs.splitlines():
        m = re.match(r"([^,]+),.*?\((\d{4})\)", strip_accents(line))
        if m:
            entries[(surname(m.group(1)), m.group(2))] = line
    for c in sorted(cited):
        if c not in entries:
            problems.append(f"cited but not in the reference list: {c[0]} ({c[1]})")
    for e in sorted(entries):
        if e not in cited:
            problems.append(f"in the reference list but never cited: {e[0]} ({e[1]})")
    return problems


def check_journal_rules(text: str) -> list[str]:
    problems = []
    abs_m = re.search(r"## Abstract\s+(.*?)\n\*\*Keywords", text, re.S)
    if not abs_m:
        problems.append("no Abstract section ending in a Keywords line")
    else:
        n = len(abs_m.group(1).split())
        if not 150 <= n <= 250:
            problems.append(f"abstract is {n} words; the journal requires 150-250")
    kw = re.search(r"\*\*Keywords\.?\*\*\s*(.+)", text)
    if kw:
        k = [x for x in re.split(r"[·;]", kw.group(1)) if x.strip()]
        if not 4 <= len(k) <= 6:
            problems.append(f"{len(k)} keywords; the journal requires 4-6")
    else:
        problems.append("no keywords line")
    if re.search(r"^#{4,} ", text, re.MULTILINE):
        problems.append("more than three heading levels")
    for needed in ("## Information Sharing Statement", "## Statements and Declarations", "**Funding.**",
                   "**Competing interests.**", "**Ethics approval.**", "**Author contributions.**",
                   "**Data availability.**", "**Code availability.**", "## References", "## Figure captions"):
        if needed not in text:
            problems.append(f"missing required element: {needed}")
    iss, decl = text.find("## Information Sharing Statement"), text.find("## Statements and Declarations")
    if iss >= 0 and decl >= 0 and iss > decl:
        problems.append("Information Sharing Statement must come before the declarations")
    for banned in ("available on request", "available upon request"):
        if banned in text.lower():
            problems.append(f"the journal does not accept {banned!r} for data or resources")
    for m in re.finditer(r"\*\*Fig\. \d\*\*.*?(?=\n\n|\Z)", text, re.S):
        if m.group(0).rstrip().endswith("."):
            problems.append(f"figure caption ends with punctuation: {m.group(0)[:40]}...")
    body = text.split("## Figure captions")[0]
    for n in range(1, 6):
        if f"Fig. {n}" not in body:
            problems.append(f"Fig. {n} is never cited in the text")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manuscript", default="docs/manuscript/MANUSCRIPT_V2.md")
    ap.add_argument("--numbers", default="docs/manuscript/verified_numbers.json")
    ap.add_argument("--references", default="docs/manuscript/references_apa7.md")
    a = ap.parse_args(argv)
    text = (REPO / a.manuscript).read_text(encoding="utf-8")
    text = text.split("## Open items before submission")[0]   # notes to the authors, not the paper
    f = json.loads((REPO / a.numbers).read_text(encoding="utf-8"))
    refs = (REPO / a.references).read_text(encoding="utf-8")

    groups = {"numbers against the sealed results": check_numbers(text, f),
              "citations versus reference list": check_citations(text, refs),
              "journal requirements": check_journal_rules(text)}
    total = 0
    for name, problems in groups.items():
        print(f"\n{name}: {'OK' if not problems else str(len(problems)) + ' problem(s)'}")
        for p in problems:
            print(f"  - {p}")
        total += len(problems)
    print(f"\n{total} problem(s) in total")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
