"""Model-curation pipeline for additional NeuroSem reference-model candidates.

Stages (run in this order; each writes evidence under ``docs/m0_evidence/model_curation/``):

``evidence``
    Repository metadata, the LICENSE text *at the pinned commit* (GitHub contents API with
    ``ref=<sha>``), commit metadata, CI runs at that commit, the recursive git tree, and
    Crossref records for the original publications. Repositories screened out for having no
    license are recorded too, with the API response that shows it.
``fetch``
    Downloads the pinned entry files plus their NeuroML/LEMS include closure into
    ``models/candidates/<repo>@<sha8>/``. It refuses any source whose license was not verified
    in a previously written evidence file, which enforces "license before download". Every
    downloaded byte string is checked against the git blob SHA-1 recorded in the pinned tree, so
    the files provably belong to that commit.
``verify``
    See ``verify_candidates.py``.

Usage::

    python docs/m0_evidence/model_curation/curate_candidates.py evidence
    python docs/m0_evidence/model_curation/curate_candidates.py fetch
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
EVIDENCE_FILE = HERE / "license_evidence.json"
TREES_DIR = HERE / "trees"
CANDIDATES_ROOT = REPO_ROOT / "models" / "candidates"

MIT_GRANT = "Permission is hereby granted, free of charge, to any person obtaining a copy"
MIT_HEADER = "The MIT License"
MIT_CONDITION = "The above copyright notice and this permission notice shall be included"
MIT_LAST_SENTENCE = "OTHER DEALINGS IN THE SOFTWARE."
# OSB LICENSE preambles exclude directories that hold third-party original code, e.g.
# "apart from that in directories NEURON and NEURON_2007." The sentence may end the text.
EXCEPTION_RE = re.compile(r"apart from that\s+in\s+director(?:y|ies)\s+(.+?)\.(?=\s|$)", re.IGNORECASE | re.DOTALL)
DIRECTORY_NAME_RE = re.compile(r"^[A-Za-z0-9_.\-/]+$")
# The only preamble text (after removing the parsed exception sentence and "=" rules) that is accepted
# without manual review: the OSB template seen in the screened repositories. Anything else fails closed.
OSB_PREAMBLE_RE = re.compile(
    r"^(?:The following license applies to all software in this repository"
    r"(?: Code located there is provided on condition of citing the ModelDB entry and original publication"
    r" as outlined in CITATION\.md\.?)?)?$")
# Wording that can carve files out of a licence grant; any occurrence outside the parsed exception
# sentence sends the licence to manual review.
RESTRICTION_WORDS_RE = re.compile(r"\b(?:apart from|except|excluding|exclude[sd]?|other than|exception|non-?commercial"
                                  r"|does not apply|not covered)\b", re.IGNORECASE)
# LEMS/NeuroML core-type libraries that jNeuroML ships internally; never fetched.
BUILTIN_BASENAMES = {"Cells.xml", "Networks.xml", "Simulation.xml", "Inputs.xml", "Channels.xml", "Synapses.xml",
                     "PyNN.xml", "NeuroMLCoreDimensions.xml", "NeuroMLCoreCompTypes.xml"}

# SHAs are the default-branch HEADs returned by ``gh api repos/<repo>/commits/<branch>`` on
# 2026-09-13; DOIs are the Crossref ``query.bibliographic`` hits saved in crossref_search.json.
SOURCES: list[dict] = [
    {
        "repo": "OpenSourceBrain/PyloricNetwork",
        "sha": "e97696fca408ef375db6cbb2054bf8c1e5e5de0e",
        "dois": ["10.1152/jn.00641.2003", "10.1038/nn1352"],
        "entries": ["LICENSE", "CITATION.md", "README.md", "NeuroML2/README.md",
                    "NeuroML2/AB_PD_1.cell.nml", "NeuroML2/LP_1.cell.nml", "NeuroML2/PY_1.cell.nml",
                    "NeuroML2/LEMS_Fig2a.xml", "NeuroML2/LEMS_Fig2b.xml", "NeuroML2/LEMS_Fig2c.xml",
                    "NeuroML2/LEMS_Fig2d.xml", "NeuroML2/.test.fig2a.jnml.omt", "NeuroML2/.test.fig2b.jnml.omt",
                    "NeuroML2/.test.fig2c.jnml.omt", "NeuroML2/.test.fig2d.jnml.omt", "NeuroML2/.test.validate.omt"],
    },
    {
        "repo": "OpenSourceBrain/GranCellLayer",
        "sha": "cee8604721c8654c24d3c69cedc07edb9679d935",
        "dois": ["10.1152/jn.1998.80.5.2521"],
        "entries": ["LICENSE", "CITATION.md", "README.md", "NeuroML2/Granule_98.cell.nml", "NeuroML2/Golgi_98.cell.nml",
                    "NeuroML2/.test.1d.jnmlnrn.omt", "NeuroML2/.test.validate.omt",
                    # NeuroMLlite descriptions of the shipped network: record the network temperature.
                    "NeuroML2/MaexDeSchutter1998.json", "NeuroML2/SimMaexDeSchutter1998.json"],
    },
    {
        "repo": "OpenSourceBrain/SolinasEtAl-GolgiCell",
        "sha": "ab4506963638dda6df5cc01721022ee7c6ea51e2",
        "dois": ["10.3389/neuro.03.002.2007"],
        "entries": ["LICENSE", "CITATION.md", "README.md", "NeuroML2/TestSoma.cell.nml", "NeuroML2/TestSoma.net.nml",
                    "NeuroML2/LEMS_Soma_Test.xml", "NeuroML2/.test.soma.jnml.omt", "NeuroML2/.test.soma2.jnml.omt",
                    "NeuroML2/.test.validate.omt",
                    # TestSoma has all active channels except CaHVA commented out; the HELPER variant is the
                    # one OMV compares with the NEURON pacemaking reference (NEURON/ carries a citation condition).
                    "NeuroML2/TestSoma_HELPER.cell.nml", "NeuroML2/TestSoma_HELPER.net.nml",
                    "NeuroML2/LEMS_Soma_Test_HELPER.xml", "NEURON/test/.test.soma.mep"],
    },
    {
        "repo": "OpenSourceBrain/SmithEtAl2013-L23DendriticSpikes",
        "sha": "179c596e44303ad08065d1eb7eafc23506478f99",
        "dois": ["10.1038/nature12600"],
        "entries": ["LICENSE", "CITATION.md", "README.md", "NeuroML2/singleCompAllChans.cell.nml",
                    "NeuroML2/singleCompAllChans.net.nml", "NeuroML2/LEMS_singleCompAllChans.xml",
                    "NeuroML2/.test.soma.jnml.omt", "NeuroML2/.test.validate.omt", "NEURON/test/.test.mep"],
    },
    {
        "repo": "OpenSourceBrain/MiglioreEtAl14_OlfactoryBulb3D",
        "sha": "eaad1c8f4afc9a19ff7b2492c150e8b42cc18edf",
        "dois": ["10.3389/fncom.2014.00050"],
        "entries": ["LICENSE", "CITATION.md", "README.md", "NeuroML2/Channels/test/MT_soma.cell.nml",
                    "NeuroML2/Channels/test/GC_soma.cell.nml", "NeuroML2/Channels/test/LEMS_OlfactoryTest_12.xml",
                    "NeuroML2/Channels/test/LEMS_OlfactoryTest_35.xml", "NeuroML2/Channels/test/OlfactoryTest_12.net.nml",
                    "NeuroML2/Channels/test/OlfactoryTest_35.net.nml", "NeuroML2/Channels/test/.test.12.jnml.omt",
                    "NeuroML2/Channels/test/.test.12.mep", "NeuroML2/Channels/test/.test.35.jnml.omt",
                    "NeuroML2/Channels/test/.test.35.mep", "NeuroML2/Channels/test/.test.validate.omt"],
    },
    {
        "repo": "OpenSourceBrain/PinskyRinzelModel",
        "sha": "a9aa9c90d2669c259e153d01b12e470114b767de",
        "dois": ["10.1007/bf00962717"],
        "entries": ["LICENSE", "CITATION.md", "README.md", "NeuroML2/twoCompartment/twoCompartmentCell.cell.nml",
                    "NeuroML2/twoCompartment/LEMS_Figure2.xml", "NeuroML2/twoCompartment/LEMS_Figure3.xml",
                    "NeuroML2/twoCompartment/.test.fig2.jnml.omt", "NeuroML2/twoCompartment/.test.fig2.mep",
                    "NeuroML2/twoCompartment/.test.fig3.jnml.omt"],
    },
]

# Screened repositories that contain single-compartment or simple NeuroML2 cells but show no
# license (GitHub license API 404 and no LICENSE* file at the pinned tree's top level). Excluded
# by rule; the evidence stage re-checks and records the responses.
SCREENED_NO_LICENSE = [
    ("OpenSourceBrain/GranuleCell", "87eb83ead7b682e260f35f2b4a1a43b45c6c5a0b"),
    ("OpenSourceBrain/Cerebellum3DDemo", "3b7be8aa0de7ccaaad4ca5bbcac2ea12efb0b45d"),
    ("OpenSourceBrain/CerebellarNucleusNeuron", "68457e1841367ded16f24369bb2acdaf324088ae"),
    ("OpenSourceBrain/HNN", "2e5abfb8290f7dcca8d897e6727a0ffaf9b861c1"),
    ("OpenSourceBrain/OSBv2_Showcase", "f71c6f6b28df5b4f73ab37f9ff80180c71abe6d7"),
    ("OpenSourceBrain/ACnet2", "20979ff64bb29ccab8fd48f35e274d57ee69ec7d"),
    ("OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell", "8275beaa52267801720d1664856d13e5d56bd11c"),
    ("OpenSourceBrain/PINGnets", "28d9a6bd4085c2e0e979224a2751e03447f42ac7"),
    ("OpenSourceBrain/Ferrante2009-DentateGyrusGranuleCell", "ed991d45490b824a8059f3f77b4c734bf6c18175"),
    ("OpenSourceBrain/IonChannelGenealogyShowcase", "8f2242bb8738bd33f2afcbf82a68afd029f10403"),
    ("OpenSourceBrain/NetPyNEShowcase", "78b052df82044a9ac9ab15bd758446401814f4d0"),
    ("OpenSourceBrain/GranularLayerSolinasNieusDAngelo2010", "b1206c3ca1eaeb3ddea3cf41d9425280494227c2"),
    ("OpenSourceBrain/MOOSEShowcase", "988b3a6378fc24597bf386b5f4e79d44a93ed615"),
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def snapshot_name(repo: str, sha: str) -> str:
    return f"{repo.split('/')[1]}@{sha[:8]}"


def gh_api(path: str) -> tuple[int, dict | list | None, str]:
    """Call ``gh api``; returns (exit code, parsed JSON or None, raw stderr)."""
    proc = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    try:
        body = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        body = None
    return proc.returncode, body, proc.stderr.strip()


def http_get(url: str, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "neurosem-model-curation/0.1"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 502, 503, 504) and attempt < retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise RuntimeError("unreachable")


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def license_exceptions(text: str) -> list[str]:
    m = EXCEPTION_RE.search(text)
    if not m:
        return []
    return [d.strip() for d in re.split(r",|\band\b", m.group(1)) if d.strip()]


def license_verdict(text: str, commit_ok: bool = True) -> dict:
    """Decide whether a LICENSE text is a plain MIT grant with machine-readable directory exceptions.

    The gate fails closed: a missing MIT header, grant or condition, any preamble that is not the known
    OSB template, restriction wording outside the parsed exception sentence, an unparseable directory
    list, or text after the MIT disclaimer all set ``license_verified`` to False with a review reason.
    A licence that only a human can read correctly must never be labelled MIT file by file.
    """
    reasons: list[str] = []
    is_mit = MIT_GRANT in text
    if not is_mit:
        reasons.append("MIT permission grant not found")
    if MIT_CONDITION not in text:
        reasons.append("MIT copyright-notice condition not found")
    head = text.find(MIT_HEADER)
    if head < 0:
        reasons.append(f"'{MIT_HEADER}' header not found")
    preamble = text[:head] if head >= 0 else text
    exceptions = license_exceptions(preamble)
    if any(not DIRECTORY_NAME_RE.match(d) for d in exceptions):
        reasons.append(f"unparseable directory exception list: {exceptions}")
    residual = " ".join(re.sub(r"^=+$", " ", EXCEPTION_RE.sub(" ", preamble), flags=re.MULTILINE).split())
    if not OSB_PREAMBLE_RE.match(residual):
        reasons.append(f"preamble is not the known OSB template: {residual[:200]!r}")
    if RESTRICTION_WORDS_RE.search(EXCEPTION_RE.sub(" ", text)):
        reasons.append("restriction wording outside the parsed exception sentence")
    tail = text.rsplit(MIT_LAST_SENTENCE, 1)
    if len(tail) != 2 or tail[1].strip():
        reasons.append("MIT disclaimer missing or followed by further text")
    return {"mit_grant_present": is_mit, "excluded_directories": exceptions,
            "spdx_for_candidate_files": "MIT" if is_mit and not reasons else None,
            "license_verified": bool(commit_ok and is_mit and not reasons), "review_reasons": reasons}


def xml_includes(data: bytes, rel: str) -> list[str]:
    """Relative include targets of a NeuroML/LEMS file, read with an XML parser.

    Parsing (rather than a regex over raw text) skips includes inside XML comments and accepts either
    quote style, so the fetched closure is exactly what jNeuroML/jLEMS would resolve. NeuroML uses
    ``<include href>`` and LEMS ``<Include file>``; both attributes are collected on both spellings.
    A file that does not parse raises, so an incomplete closure can never pass silently.
    """
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_comments=True, huge_tree=True)
    try:
        root = etree.fromstring(data, parser=parser)
    except etree.XMLSyntaxError as exc:
        raise SystemExit(f"{rel}: cannot parse XML to resolve includes: {exc}") from exc
    out: list[str] = []
    for el in root.iter():
        if not isinstance(el.tag, str) or etree.QName(el).localname not in ("include", "Include"):
            continue
        for attr in ("href", "file"):
            ref = el.get(attr)
            if ref and not ref.startswith(("http://", "https://")):
                out.append(ref)
    return out


def _slim(d: dict | None, keys: tuple[str, ...]) -> dict | None:
    return None if d is None else {k: d.get(k) for k in keys}


def crossref(doi: str) -> dict:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    msg = json.loads(http_get(url))["message"]
    return {"query_url": url, "retrieved_utc": utc_now(),
            "record": {k: msg.get(k) for k in ("DOI", "title", "author", "container-title", "issued", "volume",
                                                "issue", "page", "URL", "type")}}


def format_citation(rec: dict) -> str:
    authors = ", ".join(f"{a.get('family', '')} {''.join(p[0] for p in a.get('given', '').replace('-', ' ').split())}"
                        for a in rec.get("author", []))
    year = rec["issued"]["date-parts"][0][0]
    vol = rec.get("volume") or ""
    issue = f"({rec['issue']})" if rec.get("issue") else ""
    page = f":{rec['page']}" if rec.get("page") else ""
    return f"{authors} ({year}). {rec['title'][0]}. {rec['container-title'][0]} {vol}{issue}{page}. doi:{rec['DOI']}"


# --------------------------------------------------------------------------- evidence
def evidence_for_source(src: dict) -> dict:
    repo, sha = src["repo"], src["sha"]
    snap = snapshot_name(repo, sha)
    rc_repo, repo_meta, _ = gh_api(f"repos/{repo}")
    rc_commit, commit, _ = gh_api(f"repos/{repo}/commits/{sha}")
    rc_lic, lic_api, lic_err = gh_api(f"repos/{repo}/license")
    rc_con, lic_contents, con_err = gh_api(f"repos/{repo}/contents/LICENSE?ref={sha}")
    rc_cit, cit_contents, _ = gh_api(f"repos/{repo}/contents/CITATION.md?ref={sha}")
    rc_runs, runs, _ = gh_api(f"repos/{repo}/actions/runs?head_sha={sha}&per_page=10")
    rc_tree, tree, _ = gh_api(f"repos/{repo}/git/trees/{sha}?recursive=1")

    license_text = ""
    if rc_con == 0 and isinstance(lic_contents, dict) and lic_contents.get("encoding") == "base64":
        license_text = base64.b64decode(lic_contents["content"]).decode("utf-8", errors="replace")
    citation_text = ""
    if rc_cit == 0 and isinstance(cit_contents, dict) and cit_contents.get("encoding") == "base64":
        citation_text = base64.b64decode(cit_contents["content"]).decode("utf-8", errors="replace")

    commit_ok = rc_commit == 0 and isinstance(commit, dict) and commit.get("sha") == sha
    verdict = license_verdict(license_text, commit_ok)

    TREES_DIR.mkdir(parents=True, exist_ok=True)
    if rc_tree == 0 and isinstance(tree, dict):
        blobs = {e["path"]: {"blob_sha1": e["sha"], "size": e.get("size")} for e in tree["tree"]
                 if e["type"] == "blob" and "/Exported/" not in e["path"]}
        (TREES_DIR / f"{snap}.tree.json").write_text(json.dumps(
            {"repo": repo, "sha": sha, "api": f"repos/{repo}/git/trees/{sha}?recursive=1", "truncated": tree.get("truncated"),
             "note": "blobs under */Exported/* omitted for size", "blobs": blobs}, indent=1) + "\n", encoding="utf-8")

    papers = []
    for doi in src["dois"]:
        rec = crossref(doi)
        rec["citation"] = format_citation(rec["record"])
        papers.append(rec)
        time.sleep(2)

    return {
        "repo": repo, "sha": sha, "snapshot": snap, "retrieved_utc": utc_now(),
        "repo_api": _slim(repo_meta, ("full_name", "html_url", "description", "default_branch", "fork", "archived",
                                      "created_at", "pushed_at", "license")) if rc_repo == 0 else {"error": "failed"},
        "commit_api": {"exit": rc_commit, "sha": commit.get("sha") if isinstance(commit, dict) else None,
                       "html_url": commit.get("html_url") if isinstance(commit, dict) else None,
                       "date": commit["commit"]["committer"]["date"] if commit_ok else None,
                       "message_first_line": commit["commit"]["message"].splitlines()[0] if commit_ok else None},
        "license_api": {"endpoint": f"repos/{repo}/license (default branch)", "exit": rc_lic,
                        "response": _slim(lic_api, ("name", "path", "sha", "html_url", "license")) if rc_lic == 0 else lic_err},
        "license_at_commit_api": {"endpoint": f"repos/{repo}/contents/LICENSE?ref={sha}", "exit": rc_con,
                                  "response": _slim(lic_contents, ("name", "path", "sha", "size", "html_url", "download_url"))
                                  if rc_con == 0 else con_err,
                                  "text": license_text,
                                  "text_sha256": hashlib.sha256(license_text.encode("utf-8")).hexdigest() if license_text else None},
        "license_url": f"https://github.com/{repo}/blob/{sha}/LICENSE",
        "license_verdict": verdict,
        "citation_md_at_commit": citation_text,
        "ci_runs_at_commit": [{k: r.get(k) for k in ("name", "html_url", "status", "conclusion", "created_at", "event")}
                              for r in (runs or {}).get("workflow_runs", [])] if rc_runs == 0 else [],
        "papers_crossref": papers,
    }


def evidence_for_screened(repo: str, sha: str) -> dict:
    rc_lic, _, lic_err = gh_api(f"repos/{repo}/license")
    rc_tree, tree, _ = gh_api(f"repos/{repo}/git/trees/{sha}")
    top = [e["path"] for e in tree["tree"]] if rc_tree == 0 and isinstance(tree, dict) else None
    has_license_file = bool(top) and any(p.upper().startswith(("LICENSE", "LICENCE", "COPYING")) for p in top)
    return {"repo": repo, "sha": sha, "retrieved_utc": utc_now(), "license_api_exit": rc_lic,
            "license_api_error": lic_err[-300:] if rc_lic else None, "top_level_paths_at_sha": top,
            "license_file_at_top_level": has_license_file,
            "verdict": "excluded: no license" if (rc_lic != 0 and not has_license_file) else "needs manual review"}


def cmd_evidence(_args) -> int:
    out = {"generated_utc": utc_now(), "method": __doc__.strip().splitlines()[0],
           "tools": {"gh": subprocess.run(["gh", "--version"], capture_output=True, text=True).stdout.splitlines()[0]},
           "sources": [], "screened_no_license": []}
    for src in SOURCES:
        print(f"evidence: {src['repo']}@{src['sha'][:8]}", flush=True)
        out["sources"].append(evidence_for_source(src))
    for repo, sha in SCREENED_NO_LICENSE:
        print(f"screen: {repo}@{sha[:8]}", flush=True)
        out["screened_no_license"].append(evidence_for_screened(repo, sha))
    EVIDENCE_FILE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for s in out["sources"]:
        print(f"  {s['snapshot']}: license_verified={s['license_verdict']['license_verified']} "
              f"exceptions={s['license_verdict']['excluded_directories']}")
    for s in out["screened_no_license"]:
        print(f"  {s['repo']}: {s['verdict']}")
    return 0


# --------------------------------------------------------------------------- fetch
def fetch_source(src: dict, ev: dict, dest_root: Path) -> dict:
    repo, sha = src["repo"], src["sha"]
    if not ev["license_verdict"]["license_verified"]:
        raise SystemExit(f"{repo}: license not verified in {EVIDENCE_FILE.name}; refusing to download")
    # Re-apply the current (fail-closed) gate to the stored LICENSE text, so an evidence file written by
    # an older, laxer rule cannot authorise a download.
    recheck = license_verdict(ev["license_at_commit_api"]["text"], ev["commit_api"]["sha"] == sha)
    if not recheck["license_verified"] or recheck["excluded_directories"] != ev["license_verdict"]["excluded_directories"]:
        raise SystemExit(f"{repo}: stored license fails the current gate ({recheck['review_reasons']}); "
                         "re-run the evidence stage and review manually")
    tree = json.loads((TREES_DIR / f"{ev['snapshot']}.tree.json").read_text(encoding="utf-8"))["blobs"]
    base = f"https://raw.githubusercontent.com/{repo}/{sha}/"
    out_dir = dest_root / ev["snapshot"]
    queue = list(src["entries"])
    seen: dict[str, dict] = {}
    builtin: set[str] = set()
    while queue:
        rel = posixpath.normpath(queue.pop(0))
        if rel in seen:
            continue
        if rel not in tree:
            if posixpath.basename(rel) in BUILTIN_BASENAMES:
                builtin.add(rel)
                continue
            raise SystemExit(f"{repo}: {rel} is not in the pinned tree")
        url = base + urllib.parse.quote(rel)
        data = http_get(url)
        blob = git_blob_sha1(data)
        if blob != tree[rel]["blob_sha1"]:
            raise SystemExit(f"{repo}: git blob mismatch for {rel}: {blob} != {tree[rel]['blob_sha1']}")
        scope = "MIT"
        for d in ev["license_verdict"]["excluded_directories"]:
            if rel == d or rel.startswith(d.rstrip("/") + "/"):
                scope = f"citation condition ({d}/ excluded from MIT)"
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        seen[rel] = {"url": url, "sha256": hashlib.sha256(data).hexdigest(), "git_blob_sha1": blob, "bytes": len(data),
                     "license_scope": scope, "role": "entry" if rel in src["entries"] else "include"}
        if rel.endswith((".nml", ".xml")):
            for inc in xml_includes(data, rel):
                queue.append(posixpath.join(posixpath.dirname(rel), inc))
    papers = ev["papers_crossref"]
    prov = {
        "snapshot": ev["snapshot"],
        "repository": f"https://github.com/{repo}",
        "commit": sha,
        "commit_date": ev["commit_api"]["date"],
        "license": "MIT" + (f" (directories {', '.join(ev['license_verdict']['excluded_directories'])} carry a citation "
                            f"condition instead)" if ev["license_verdict"]["excluded_directories"] else ""),
        "license_url": ev["license_url"],
        "license_evidence": f"docs/m0_evidence/model_curation/{EVIDENCE_FILE.name} (retrieved {ev['retrieved_utc']})",
        "citation": " | ".join(p["citation"] for p in papers),
        "downloaded_utc": utc_now(),
        "builtin_includes_not_fetched": sorted(builtin),
        "files": dict(sorted(seen.items())),
    }
    if prov["downloaded_utc"] < ev["retrieved_utc"]:
        raise SystemExit("clock error: download timestamp precedes license evidence")
    (out_dir / "PROVENANCE.json").write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")
    return prov


def cmd_fetch(args) -> int:
    evidence = json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))
    by_repo = {e["repo"]: e for e in evidence["sources"]}
    only = set(args.only or [])
    for src in SOURCES:
        if only and src["repo"].split("/")[1] not in only:
            continue
        ev = by_repo.get(src["repo"])
        if ev is None or ev["sha"] != src["sha"]:
            raise SystemExit(f"{src['repo']}: no license evidence for sha {src['sha']}; run the evidence stage first")
        prov = fetch_source(src, ev, CANDIDATES_ROOT)
        print(f"{prov['snapshot']}: {len(prov['files'])} files; builtin includes skipped: {prov['builtin_includes_not_fetched']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("evidence")
    f = sub.add_parser("fetch")
    f.add_argument("--only", nargs="*", help="repository names (without owner) to fetch")
    args = ap.parse_args(argv)
    return {"evidence": cmd_evidence, "fetch": cmd_fetch}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
