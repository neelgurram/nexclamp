# Name-conflict audit: "NeuroSem"

Milestone 0 deliverable: the name-conflict search (spec, "Milestone 0: Audit"). Written 2026-09-13 on branch `m0-audit`; counts were measured at about 17:07 UTC against the working tree at commit `d323afa` (which differs from `3cdb957` only in `AI_USE_LOG.md` and `src/neuraxis/provenance.py`). The project name is Neel's decision, logged as DECISIONS.md **N-10**.

## In plain English

- Before a project goes public, you check that nobody else already uses its name.
- Nobody owns "neurosem" as a Python package, conda package or GitHub account. Those slots are free.
- But other people already use the name. There is a 2025 simulation paper called "NeuroSEM" with public code. There is an active neuroscience project on GitHub spelled exactly "NeuroSem". A marketing company uses the name NeuroSEM on neurosem.com (the domain was registered in 2013; how long the company has traded is unverified).
- Think of opening a bookshop called "Riverside Books" when another Riverside Books already exists in the next town. Hanging the sign is allowed, but readers will mix the two up and find the wrong one when they search.
- The audit suggests a new name: **PerturbPrint**. It comes from the project's own term "perturbation fingerprint", and none of the sources that answered had it (some, such as Zenodo and European trademarks, could not be checked). **DriftClamp** is the backup choice.
- Renaming is cheaper now than later. The code already uses `neurosem` about 780 times outside the historical evidence files, and the Milestone 6 pilot, which started at 17:11 UTC on 2026-09-13, is writing raw outputs that carry the name.
- This is a search, not legal clearance. The choice is Neel's.

---

## 1. Scope, sources and rules of evidence

- **What this is.** A record of which public sources were searched for "NeuroSem" and six alternatives, what they returned, and what could not be searched. A 404 or a zero count only means that source returned nothing for that query at that time. It does not prove a name is legally or commercially free.
- **Evidence files** (all dated 2026-09-13):
  - `docs/m0_evidence/names/name_search.json`: the first search (NeuroSem, six alternatives, about 20 names screened).
  - `docs/m0_evidence/names/name_verify.json`: an independent re-check of NeuroSem and the top three alternatives. **Where the two files disagree, the re-check wins.** Corrections are marked "(corrected by re-check)" below.
  - Section 5 lists the checks I re-ran myself today, with the exact commands.
- **Nothing was registered or reserved.** No package, account, domain or trademark was claimed.
- **Requirement being met.** The final spec lists "Name-conflict search" under Milestone 0 (`docs/handoff/NEUROSEM_FINAL_SPEC.extracted.md`, lines 762-766). The earlier handoff's initial prompt says to "Search for project/package/name conflicts; do not assume NeuroSem is available" (`docs/handoff/NEUROSEM_CLAUDE_HANDOFF.extracted.md`, line 280).

## 2. What was checked, where, and what came back ("NeuroSem")

Variants searched: `NeuroSem`, `neurosem`, `Neuro-Sem`, `NeuroSEM`, `neuro_sem`, `neuro-sem` (name_search.json, `variants_checked`). All rows are from 2026-09-13.

### 2.1 Package registries and hosting

| Source | Query URL(s) | Result | Evidence |
|---|---|---|---|
| PyPI JSON API | `https://pypi.org/pypi/neurosem/json` (also `neuro-sem`, `neuro_sem`, `NeuroSEM`, `Neuro-Sem`), `https://pypi.org/simple/neurosem/` | HTTP 404 for all. Also 404 for `neurosem3d`, `neurosem-3d`, `neurosemantics`, `neurosemantic`. Re-check used a positive control (`efel` returned 200) and scanned the full PyPI simple index (890,745 projects): no `neuro.?sem` project. | search + verify |
| conda-forge (anaconda.org API) | `https://api.anaconda.org/package/conda-forge/neurosem` (and `neuro-sem`, `neuro_sem`) | HTTP 404. The HTML page `https://anaconda.org/conda-forge/<name>` returns 200 even for missing names, so it is not a valid test. Re-check: control `numpy` returned 200; `channeldata.json` (34,335 packages) has no `neuro.?sem` match. | search + verify |
| conda-forge feedstocks | `https://api.github.com/repos/conda-forge/neurosem-feedstock` (and variants) | HTTP 404 | search + verify |
| npm | `https://registry.npmjs.org/neurosem` (and variants) | HTTP 404 | search + verify |
| CRAN (crandb) | `https://crandb.r-pkg.org/neurosem` | HTTP 404 | verify |
| Read the Docs | `https://readthedocs.org/api/v3/projects/neurosem/`, `https://neurosem.readthedocs.io/` (and `neuro-sem`) | HTTP 404 | search + verify |
| Hugging Face model search | (URL not recorded in the evidence) | Nothing returned | verify |

### 2.2 GitHub

| Check | URL | Result | Evidence |
|---|---|---|---|
| User / organisation | `https://api.github.com/users/neurosem` (and `neuro-sem`, `neuro_sem`) | 404. User search (`search/users?q=neurosem`) returns one organisation, `neurosemantica` (prefix overlap only). | search + verify; re-run today (Section 5) |
| Repository search | `https://api.github.com/search/repositories?q=neurosem&per_page=50` | 19 repositories. See conflicts in Section 3. | search; re-run today: 19 |
| Phrase `"neuro-sem"` | `https://api.github.com/search/repositories?q=%22neuro-sem%22&per_page=30` | 46 fuzzy hits, mostly "neuro seminar" and "neurosemantics" | search |
| Code search | `https://api.github.com/search/code?q=neurosem` | 1,140 code hits (CMAME citations in publication lists, joke prompt files, identifiers) | verify; re-run today: 1,140 |

### 2.3 Scholarly indexes

| Source | Query URL(s) | Result | Evidence |
|---|---|---|---|
| Crossref | `https://api.crossref.org/works?query.bibliographic=neurosem&rows=20` | The top two hits are the NeuroSEM PINN / spectral-element framework: CMAME article `10.1016/j.cma.2024.117498` and SSRN preprint `10.2139/ssrn.4912094`. "Neuro-SEM Unveiled" DOIs resolved separately. | search + verify |
| DataCite (includes arXiv DOIs) | `https://api.datacite.org/dois?query=neurosem&page%5Bsize%5D=10` | 1 DOI: `10.48550/arxiv.2407.21217` (NeuroSEM, 2024). The `neuro-sem` query is tokenised into 180 unrelated matches, so it tells us nothing. | search + verify |
| OpenAlex | `https://api.openalex.org/works?search=neurosem&per-page=25` and title/abstract phrase filters | 18 works, 3 of them exact-name records of the NeuroSEM framework. Phrase "neuro-sem": 2. Phrase "neuro-semantic": 63. No sources, institutions or authors named neurosem. **The re-check could not repeat any OpenAlex query (HTTP 429), so these counts come from the first search only.** | search; verify unverifiable |
| arXiv | API `https://export.arxiv.org/api/query?search_query=all:neurosem` (HTTP 429); web search `https://arxiv.org/search/?query=neurosem&searchtype=all` | 1 result: arXiv 2407.21217 (v1 2024-07-30, v2 2024-10-15, primary cs.LG) | search + verify |
| Europe PMC | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=neurosem&format=json&pageSize=25` | hitCount 0 | search |
| PubMed (E-utilities) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=neurosem&retmode=json` (also `neurosem[tiab]`, `"neuro-sem"`) | 0. Unquoted `neuro sem` is auto-expanded into structural equation modelling and scanning electron microscopy journal terms (1,410 records), which itself shows how ambiguous "SEM" is. | search + verify |
| Semantic Scholar | `https://api.semanticscholar.org/graph/v1/paper/search?query=neurosem&limit=25&fields=title,year,externalIds,venue,url` | **Not retrieved** (HTTP 429 on every attempt, both passes) | search + verify |
| Zenodo | `https://zenodo.org/api/records?q=neurosem&size=25` | **Not retrieved** (HTTP 504 on every attempt, both passes). DataCite is only a partial substitute. | search + verify |
| DBLP | `https://dblp.org/search/publ/api?q=neurosem&format=json&h=20` | **Not retrieved** (anti-bot page) | search + verify |

### 2.4 Domains

| Domain | Method | Result | Evidence |
|---|---|---|---|
| neurosem.com | HTTP fetch; RDAP `https://rdap.org/domain/neurosem.com` | Live site. RDAP: registered 2013-03-01, expires 2027-03-01, status "client transfer prohibited", last changed 2026-02-14. | search + verify; RDAP re-run today (Section 5) |
| neurosem.org | HTTP fetch; RDAP | No HTTP response; RDAP 404. Suggests no registration record, but not confirmed with a registrar. | search |
| neurosem.io | HTTP fetch; RDAP | No HTTP response. RDAP 404 means nothing here: rdap.org also returned 404 for the registered domain github.io. | search |
| neurosem.ai, neurosem.net | HTTP fetch only | No HTTP response | search |

### 2.5 Trademarks

| Office | Method | Result | Evidence |
|---|---|---|---|
| USPTO (US federal) | POST to the backend used by the tmsearch web app, `https://tmsearch.uspto.gov/prod-stage-v1-0-0/tmsearch`. This endpoint is not a documented public API. | Wordmark field: 0 records for `neurosem` (and `neurosem*` in the first search). Controls: `google` 194, `neuron` 125, reproduced in the re-check. An unfielded query gave 1,764 fuzzy or phonetic matches (e.g. NORSMAN); none on the first page was spelled NEUROSEM. The re-check did not repeat the wildcard query. | search + verify |
| EUIPO | `https://euipo.europa.eu/eSearch/#basic/1+1+1+1/100+100+100+100/neurosem` | **Not verifiable.** The site is a JavaScript app and the fetched HTML had no results. | search |
| WIPO Global Brand Database, other national offices | none | **Not checked** | search + verify |

### 2.6 General web search

The first search ran four WebSearch queries: `"NeuroSem"`; `"NeuroSEM" OR "Neuro-SEM" OR "neuro_sem"`; `"neurosem" software OR company OR lab OR course`; `NeuroSEM trademark USPTO OR EUIPO`. These found the uses listed in Section 3 and no trademark record. The re-check could not repeat WebSearch because the session search budget was exhausted.

## 3. Conflicts found for "NeuroSem"

Severity labels are the auditors' judgement as recorded in the evidence files. They are not a formal scale.

| # | Conflict | What it is | Key facts (source) | Severity |
|---|---|---|---|---|
| C1 | **NeuroSEM framework paper** (CMAME 2025, arXiv, SSRN) | "NeuroSEM: A hybrid framework for simulating multiphysics problems by coupling PINNs and spectral elements". Here SEM means spectral element method. | Crossref: journal article, CMAME vol 433, article 117498, issued 2025-01; authors Shukla, Zou, Chan, Pandey, Wang, Karniadakis. arXiv 2407.21217 (2024). SSRN `10.2139/ssrn.4912094` (2024). It takes the top two Crossref hits for "neurosem". (`https://api.crossref.org/works/10.1016/j.cma.2024.117498`, `https://arxiv.org/abs/2407.21217`, `https://api.crossref.org/works/10.2139/ssrn.4912094`) | **High** |
| C2 | **vafaei-ar/NeuroSem** (GitHub) | Identical spelling. A neuroscience-plus-language-model project: can human neural representational geometry (EEG/fMRI) supervise language models? | GitHub API: created 2026-08-19, pushed 2026-09-13T03:20:37Z, Python, GPL-3.0, 0 stars. The README says the project is in a submission freeze with an author-review package. **Target journal unverified.** (`https://api.github.com/repos/vafaei-ar/NeuroSem`) Re-confirmed today. | **High** |
| C3 | **"SEM" is overloaded in neuroscience** | A neuroscience reader will likely read SEM as scanning electron microscopy, standard error of the mean or structural equation modelling, not "semantic". | First search, OpenAlex title/abstract counts: "scanning electron microscopy" AND neuron 1,232; "standard error of the mean" AND neuron 167; "structural equation model" AND neuron 78. **The re-check could not repeat these counts (HTTP 429), so the numbers are unverified.** The PubMed expansion of `neuro sem` was confirmed (1,410 records). | **High** |
| C4 | **ZongrenZou/NeuroSEM** (GitHub) | Public code for C1 | Created 2024-12-19, Python, no licence, 6 stars, description "Codes of PINNs for the NeuroSEM paper". (`https://api.github.com/repos/ZongrenZou/NeuroSEM`) | Medium |
| C5 | **NeuroSEM company, neurosem.com** | Applies neuromarketing to search-engine marketing (SEM = search engine marketing) | Domain registered 2013-03-01 (RDAP). **(Corrected by re-check)** The homepage lists regional contacts as US East Coast, US West Coast and Europe. It names no cities, so the first search's "New York / San Francisco" is not confirmed. Continuous trading since 2013 is unverified; the RDAP date only dates the domain. The page description is a WebFetch summary, not a full-page read. | Medium |
| C6 | **Samsomyajit/NAVIER-CFD** (GitHub) (new in re-check) | Third-party CFD code that already uses `neurosem` as a runtime model key for C1 | Created 2026-07-11. Registers `neurosem` in `src/navier_cfd/runtime_registry.py`. (`https://api.github.com/repos/Samsomyajit/NAVIER-CFD`) | Medium |
| C7 | **"Neuro-SEM Unveiled: Mapping Brain, Behavior, and Decision-Making"** | 2025 paper using "Neuro-SEM" | Crossref: `10.2139/ssrn.5194408` (SSRN, 2025) and `10.63456/ghs-2-1-12` (Global Health Synapse vol 2, 2025-06-02). **That "SEM" there means structural equation modelling is unverified**: Crossref gave no abstract. | Medium |
| C8 | **Neuro-Semantics coaching movement** | L. Michael Hall and the International Society of Neuro-Semantics; derived from neuro-linguistic programming | Crown House author page (WebFetch summary): `https://www.crownhouse.co.uk/l-michael-hall` | Medium |
| C9 | **Academic "neuro-semantic" usage** | In neuroscience the term already means the neural basis of word meaning | Example: `10.1002/hbm.23814` ("Decoding the neural representation of story meanings across languages", Human Brain Mapping, 2017). GitHub `samiraabnar/NeuroSemantics` and `NeuroSemanticsDemo`. The OpenAlex count of 63 works was not re-checked. | Medium |
| C10 | drresearch2288/Neurosem-3D | Text-to-3D semantic field (graphics / machine learning) | Created 2026-08-02, package path `src/neurosem3d/` | Low |
| C11 | AlexMrzv/NeuroSEM, Bashkirov-NS/NeuroSEM | Small inactive 2023 repositories with no description | GitHub API | Low |
| C12 | magabimkt/NeuroSemNeura | Portuguese neuroanatomy study project "Neuro sem Neura" (sem = "without") | GitHub API | Low |
| C13 | nsucher/semiology_quant (new in re-check) | MATLAB functions `neurosem_plot` and `neurosem_data` for seizure-semiology neural data | `https://api.github.com/repos/nsucher/semiology_quant` | Low |
| C14 | GitHub organisation neurosemantica | Data pipelines, knowledge graphs, agentic systems; created 2026-01-12 | `https://api.github.com/users/neurosemantica` | Low |
| C15 | 1,140 GitHub code hits for "neurosem" (new in re-check) | Noise: citations of C1, a joke prompt term, identifiers | `https://api.github.com/search/code?q=neurosem`. Re-run today: 1,140. | Low |

**No conflict found (severity "none"):** PyPI, conda-forge, npm, CRAN, Read the Docs, GitHub user/organisation names, and the USPTO wordmark field.

**Verdict in both evidence files: do not keep "NeuroSem".** The package slots are free. The trouble is confusion in papers and searches: C1 to C3 are high severity, and the name does not describe the method (behavioural regression testing of neuron models).

## 4. What could not be checked

From `unverifiable` in both files, with re-check status:

1. **Semantic Scholar.** HTTP 429 for NeuroSem in both passes. Of the alternatives, `perturbprint` and `driftclamp` each returned total 0 once in the re-check.
2. **Zenodo API.** HTTP 504 on every attempt in both passes. Zenodo records not visible through DataCite may be missed.
3. **arXiv API.** HTTP 429 or timeouts. The arXiv web search page (all fields) was used instead.
4. **DBLP.** Anti-bot page, not searched.
5. **Google Scholar, IEEE Xplore, ACM Digital Library.** Not queried directly. Covered only indirectly through Crossref, OpenAlex and the first search's WebSearch.
6. **OpenAlex in the re-check.** HTTP 429 all day. Every OpenAlex count in this document comes from the first search only.
7. **WebSearch in the re-check.** Budget exhausted. First-search web-only claims (the Perturb-seq association, drift-racing products, the METACLAMP/MTCLAMP marks) were not re-checked.
8. **Trademarks.** EUIPO (JavaScript app, no results), WIPO Global Brand Database and other national offices were not checked. USPTO results come from an undocumented endpoint and cover US federal marks only, not state or common-law marks.
9. **Domains.** rdap.org cannot answer for .io. The .com/.org 404s were not confirmed with a registrar. .ai and .net were only probed over HTTP.
10. **Other code hosts.** Only public GitHub repositories were searched. GitLab, Bitbucket, Codeberg, SourceForge and private repositories were not.
11. **Company registries** (e.g. Companies House, US state registries). Not searched.
12. **Page summaries.** The neurosem.com and Crown House descriptions are WebFetch summaries, not full-page reads.
13. **Future publication.** Whether the vafaei-ar/NeuroSem manuscript will be published under that name, and where, is unknown.
14. **Lower-ranked alternatives.** NeuroCanary, MutaClamp and StimBattery were checked only once, in the first search.

## 5. Checks re-run today

Run on 2026-09-13 between 17:05 and 17:08 UTC, from Git Bash. Scratch outputs are in `work/tmp/m0docs/name_conflict_audit/`.

**PyPI JSON API** (17:05:05 UTC):

```bash
for n in neurosem neuro-sem perturbprint perturb-print driftclamp drift-clamp efel; do
  printf "%s " "$n"; curl -s -o /dev/null -w "%{http_code}\n" "https://pypi.org/pypi/$n/json"; done
```

| Name | HTTP |
|---|---|
| neurosem | 404 |
| neuro-sem | 404 |
| perturbprint | 404 |
| perturb-print | 404 |
| driftclamp | 404 |
| drift-clamp | 404 |
| efel (positive control) | 200 |

**GitHub repository search, unauthenticated REST** (17:05:08 UTC):

```bash
for q in neurosem perturbprint driftclamp; do
  curl -s -H "Accept: application/vnd.github+json" \
    "https://api.github.com/search/repositories?q=$q&per_page=100" > gh_repo_$q.json; done
# then total_count and incomplete_results read with Python json
```

| Query | total_count | incomplete_results |
|---|---|---|
| neurosem | **19** | false |
| perturbprint | **0** | false |
| driftclamp | **0** | false |

The 19 `neurosem` repositories match the first search's count and include every GitHub conflict in Section 3 (vafaei-ar/NeuroSem still shows pushed 2026-09-13T03:20:37Z, GPL-3.0).

**Extra cheap checks** (17:06-17:07 UTC):

```bash
for n in neurosem perturbprint driftclamp numpy; do
  curl -s -o /dev/null -w "%{http_code}\n" "https://api.anaconda.org/package/conda-forge/$n"; done
for n in neurosem perturbprint driftclamp; do
  curl -s -o /dev/null -w "%{http_code}\n" "https://api.github.com/users/$n"; done
curl -s -L https://rdap.org/domain/neurosem.com
gh api -X GET search/code -f q=<name> --jq '.total_count'     # authenticated, read-only
```

| Check | neurosem | perturbprint | driftclamp |
|---|---|---|---|
| conda-forge API (control numpy = 200) | 404 | 404 | 404 |
| GitHub `users/<name>` | 404 | 404 | 404 |
| GitHub code search total_count | 1,140 | **0** | 102 |
| RDAP neurosem.com | registered 2013-03-01, expires 2027-03-01, last changed 2026-02-14 | not run | not run |

All of today's results match the evidence files. None of these checks establishes that a name is legally available.

## 6. Alternatives

About 20 names were screened first on PyPI, the anaconda.org API and GitHub repository search. Names dropped at screening:

- `neurodrift`: 16 GitHub repositories.
- `silentdrift`: an existing GitHub organisation.
- `driftprobe`: the PyPI name is taken (HTTP 200).
- `spikeguard`: 14 repositories.
- `neuromutant`, `neuroregress`: one similar repository each.
- `nmlregress`, `lemsdrift`, `nmldrift`: not carried forward, because an NML or LEMS prefix could suggest an official NeuroML project.
- `clampdrift`, `spikeprint`, `ephysdrift`, `clampsentinel`, `protoscreen`: no screening hit, not carried forward (no reason recorded).

Six names got full checks. Scores are copied from `name_search.json`. That file does not define the scale; its ranking and recommendation treat higher as better. The re-check ranked only the top three and gave no new scores.

| Name | Registries (PyPI, conda-forge, npm, RTD; plain and hyphenated) | GitHub | Scholarly / web | Trademark and domains | Main risk | Score | Re-check |
|---|---|---|---|---|---|---|---|
| **PerturbPrint** | All 404. CRAN 404. No `perturb.?print` in the full PyPI index. | Repositories 0, users 404, user search 0, **code search 0** | Crossref 0, DataCite 0, Europe PMC 0, PubMed 0, arXiv "no results", Semantic Scholar 0 (one successful call). OpenAlex phrase "perturbation fingerprint": 2 unrelated works (first search only). | USPTO 0. RDAP .com and .org 404. | "Perturb-" suggests CRISPR Perturb-seq screens (first-search web result, not re-checked). At least 15 perturb-prefixed PyPI projects are listed in the re-check (e.g. `perturbguard`, `perturb-tools`, `PerturbNet`), none identical. | 4 | **Rank 1, confirmed.** The only name of the three with zero hits in every source that answered. |
| **DriftClamp** | All 404. CRAN 404. | Repositories 0. Hyphenated `drift-clamp` returns 3 unrelated repositories. Users 404. **Code search 102 (corrected by re-check).** | Crossref 0, DataCite 0, Europe PMC 0, PubMed 0, arXiv "no results", Semantic Scholar 0. OpenAlex: 1 fuzzy and 2 phrase hits, all unrelated (first search only). | USPTO 0. RDAP .com 404 (.org only in the first search). | In patch-clamp work, "drift" means recording drift and "clamp" suggests wet-lab or dynamic-clamp tools. The 102 code hits are existing identifiers (a C helper `DriftClamp` in Hexlord/project-drift, a `driftClamp` key in TheFaucett/stock-game), not a named project. | 4 | **Rank 2, corrected.** "Slightly weaker than first reported" because of the code-identifier collisions. |
| **EphysPrint** | All 404. CRAN 404. | Repositories, users and code search 0 | Crossref 0, DataCite 0, Europe PMC 0, PubMed 0, arXiv "no results". "Electrophysiological fingerprint" is established wording for recorded cells (e.g. `10.1098/rsif.2016.0999`, `10.1038/srep30259`). | USPTO 0. RDAP .com 404. | Reads as a tool for recorded data, not models. 47 PyPI project names contain "ephys". | 3 | Rank 3, confirmed |
| NeuroCanary | All 404 | Repositories 0, users 404 | OpenAlex, Crossref, DataCite and arXiv web search 0; Semantic Scholar (429) and Zenodo (504) not retrieved | USPTO 0 (also `neurocanary*`). RDAP .com and .org 404. | "Canary" means canary release in software. The "Neuro" prefix is crowded. | 3 | Not re-checked |
| MutaClamp | All 404 | Repositories 0, users 404 | OpenAlex, Crossref, DataCite and arXiv web search 0; Semantic Scholar and Zenodo not retrieved. Web results were DNA-repair sliding-clamp literature. | USPTO 0 for the exact name. An unfielded query surfaced the similar marks METACLAMP and MTCLAMP (not re-checked). | Suggests DNA mismatch-repair proteins; awkward to say | 2 | Not re-checked |
| StimBattery | All 404 | Repositories 0, users 404 | Crossref, DataCite and arXiv web search 0; Semantic Scholar and Zenodo not retrieved. OpenAlex phrase "stimulation battery": 53 works, mostly deep-brain-stimulator batteries. | USPTO 0. RDAP 404. | Reads as neurostimulator hardware; generic | 2 | Not re-checked |

**Why PerturbPrint fits.** The handoff defines the central term: "Perturbation fingerprint: Electrophysiological feature vector across several stimulation protocols" (`NEUROSEM_CLAUDE_HANDOFF.extracted.md`, line 49). The final spec describes the framework as using "perturbation fingerprints" (`NEUROSEM_FINAL_SPEC.extracted.md`, line 154). The repository glossary defines the term too (`docs/glossary.md`, line 40), and the `pyproject.toml` description already says "mutation-calibrated perturbation fingerprints". The name does not say "regression testing" by itself. A subtitle can carry that, such as the current CITATION.cff title after the colon.

## 7. Cost of renaming now versus later

### 7.1 What the name is attached to today (measured 2026-09-13)

The first search advised renaming "before Milestone 1 creates the package (src/neuraxis/, CLI 'neurosem', CITATION.cff)". That window has passed. `src/neuraxis/__init__.py` was first committed in `de693e1` (2026-09-13) and `CITATION.cff` in `3cdb957` (2026-09-13). The command `git log --diff-filter=A --format="%h %ad %s" --date=short -- <path>` shows this.

Counts are case-insensitive matches of `neurosem` in the working-tree contents of git-tracked files. `.venv`, `.git`, `work/` and the untracked `results/` are excluded unless stated. Base command:

```bash
git ls-files -- <path> | xargs -r grep -Ioi neurosem | wc -l     # occurrences
git ls-files -- <path> | xargs -r grep -Ili neurosem | wc -l     # files
```

| Area | Occurrences | Files | What changes in a rename |
|---|---|---|---|
| All tracked files (486 tracked) | **2,208** | **245** | Total |
| `docs/m0_evidence/` | 1,376 | 86 | **Keep unchanged.** These are dated audit records. |
| `docs/handoff/` (handoff and spec, text and PDF) | 54 | 2 (text extracts) | **Keep unchanged.** These are authoritative inputs. |
| **Everything else (rename candidates)** | **778** | **157** | See rows below |
| `src/` (package directory `src/neuraxis/`) | 264 | 45 | Directory name, imports, docstrings |
| `tests/` | 208 | 35 | Imports, patch targets |
| Python import lines, all tracked `.py` | 359 lines | 86 files | `from neurosem ...` / `import neurosem`. 69 of the lines are indented (lazy imports inside functions). |
| `agent_study/` | 37 | 28 | Task and prompt files |
| `scripts/`, `workflows/` | 19 / 10 | 5 / 5 | Imports; workflow docstrings name the `neurosem <command>` equivalents |
| `configs/` | 13 | 4 | `study_id: neurosem`; `schema: neurosem-agent-policy/1`; feature source key `neurosem:` in `features.yaml` |
| `docs/` outside evidence and handoff | 151 | 21 | Prose, commands |
| `Dockerfile` | 20 | 1 | Image tags (`neurosem:dev`), user/group `neurosem`, `WORKDIR /opt/neurosem`, `NEUROSEM_*` environment variables |
| `Makefile` | 16 | 1 | CLI calls |
| `DECISIONS.md` / `AI_USE_LOG.md` / `CHANGELOG.md` | 13 / 3 / 2 | 3 | Logs. Past entries should probably keep the old name, with a new entry recording the rename. |
| `.github/workflows/ci.yml` | 6 | 1 | Image tag `neurosem:ci`, import check |
| `data/` | 4 | 2 | README references to `neurosem.selection...` |
| `pyproject.toml` | 3 | 1 | Distribution `name = "neurosem"`, script `neurosem = "neurosem.cli:main"` |
| `CITATION.cff` | 2 | 1 | `title` and `abstract` |
| `README.md`, `environment.yml` (conda env `name: neurosem`), `requirements.lock`, `LICENSE` | 2 / 2 / 2 / 1 | 4 | Headings, env name, comments |

Other places the name is attached:

- **CLI.** `pyproject.toml` `[project.scripts] neurosem = "neurosem.cli:main"` and `argparse.ArgumentParser(prog="neurosem", ...)` at `src/neuraxis/cli.py:148`. The spec's suggested commands also use the `neurosem` prefix (`NEUROSEM_FINAL_SPEC.extracted.md`, line 759), and its repository tree is rooted at `neurosem/` (line 529).
- **Environment variables.** Six distinct names (`NEUROSEM_CONTAINER_IMAGE`, `NEUROSEM_FEATURES`, `NEUROSEM_GIT_COMMIT`, `NEUROSEM_JAVA`, `NEUROSEM_JNML_JAR`, `NEUROSEM_NETWORK_TESTS`), used in 12 tracked files.
- **Schema and label identifiers** in tracked src, configs, tests, agent_study, workflows and scripts. Examples: `neurosem-public-checks/` (10), `neurosem-agent-task/` (10), `neurosem-public-reference/` (9), `neurosem-agent-policy/` (2), `neurosem-trial-log/`, `neurosem-trial-export/`, `neurosem-hidden-checks/`, `neurosem-agent-frozen/`, and the feature labels `neurosem:firing_regime` and `neurosem:rheobase`.
- **Installed package.** `.venv/Scripts/python -m pip show neurosem` reports `Name: neurosem`, `Version: 0.1.0.dev0`. A rename needs a reinstall.
- **Pilot raw outputs already carry the name.** The Milestone 6 pilot (campaign `pilot`) has been writing `results/raw/pilot/` since 2026-09-13 17:11 UTC (the reference warm-up wrote earlier development records). At about 17:07 UTC the untracked `results/` directory held 497 occurrences (`grep -rIoi neurosem results | wc -l`), 333 of them just the local folder path `C:\Users\gurra\NeuroSem`; at about 17:15 UTC there were 843 and 606. The count keeps growing while the pilot runs. Besides folder paths, occurrences include the provenance string `"neurosem==0.1.0.dev0"` and feature source labels such as `"neurosem:firing_regime"`.
- **No hosted repository yet.** `git remote -v` prints nothing, so there is no GitHub repository to rename.
- **Nothing public yet.** No PyPI release, DOI or public repository exists. `CITATION.cff` says "The software is unreleased (0.1.0.dev0): there is no DOI, public repository URL or release date yet".

### 7.2 Now versus later

**Renaming now (after the pilot has started, but before preregistration, the frozen study and any release):**

- It is a text refactor of about 778 occurrences in 157 tracked files. The main parts are one directory move, 359 import lines and one CLI entry point.
- It also changes six environment-variable names, 11 distinct `neurosem-` identifier prefixes plus the `neurosem:` feature labels, the Docker image, user and workdir, and the conda environment name. Only 1 of the 778 occurrences is a local folder path (`gurra/NeuroSem`); the rest are uses of the name.
- Pilot and development outputs under `results/` would carry the old labels. They are untracked development and pilot artefacts (not frozen-study results). They could in principle be regenerated by re-running the pilot after a rename (not attempted; unverified), or kept with a documented old-to-new name mapping.
- The effort has not been measured. **No trial rename was run, so "mechanical refactor" (DECISIONS N-10) is plausible but unverified.** A dry run would prove it: rename in a scratch copy, reinstall, run the test suite.

**Renaming later costs more at each step, for these reasons:**

1. **After the frozen study runs.** The spec says "Raw results must be immutable. Derived results should be reproducible from raw outputs with one workflow command" (`NEUROSEM_FINAL_SPEC.extracted.md`, line 758). Raw records would then permanently carry `neurosem==...` provenance and `neurosem:` feature labels. A later rename would need a compatibility alias or a documented mapping so that reproduction still works.
2. **After preregistration.** The registered documents would carry the old name, and the published study would have to explain the change.
3. **After a public release** (PyPI package, public repository, DOI in CITATION.cff). Users and citations would point at the old name. How each service handles a rename after release was not checked (unverified).
4. **After a manuscript is submitted.** The name would appear in the paper, figures and supplementary code.

**Low-cost option either way.** Decide the name before preregistration and the frozen study, whose raw results are immutable by design. The pilot's outputs are development-stage and can be mapped or regenerated. The historical evidence files and handoff PDFs keep the old name as dated records.

## 8. Recommendation (Neel's decision, DECISIONS N-10)

Both evidence files recommend renaming, and the choice is Neel's:

- **Preferred: PerturbPrint.** Package and CLI name `perturbprint`. It matches the project's defined term "perturbation fingerprint". It had zero hits in every source that answered, including GitHub code search (re-confirmed today: PyPI 404, conda-forge 404, repositories 0, code 0). Known weak spot: the "Perturb-" prefix is associated with Perturb-seq genetic screens.
- **Runner-up: DriftClamp.** Registries and literature were clean, and today repository search was 0. But 102 GitHub code identifiers already use it, and "drift" and "clamp" can suggest recording drift or clamp hardware to electrophysiologists.
- **Keeping NeuroSem** is possible, because the package slots are free. It means accepting the high-severity confusion with the NeuroSEM framework paper (C1), the identically spelled neuroscience repository (C2) and the "SEM" ambiguity (C3).

N-10 records the rename recommendation (PerturbPrint preferred, DriftClamp runner-up) with the timing "before any public release", and notes that code keeps `neurosem` until Neel decides. This audit recommends an earlier point: before preregistration and the frozen study, because their raw results are immutable. N-10's phrase "zero hits in every source checked" should read "every source that answered". Options for Neel:

| Option | What happens |
|---|---|
| A. Rename to PerturbPrint now (recommended) | Rename (a scripted refactor, to be proven by a dry run plus the test suite) before preregistration and the frozen study; map or regenerate pilot outputs. Re-check registries and trademarks just before any public release. |
| B. Rename to DriftClamp now | Same as A, with the risks noted above |
| C. Choose the name later, before public release | Every result, label and document produced in the meantime carries `neurosem` (Section 7.2) |
| D. Keep NeuroSem | Accept conflicts C1 to C3. Consider a distinguishing subtitle everywhere the name appears. |

**Before any public release, whatever name is chosen:**

- Re-run PyPI, conda-forge, GitHub (repositories, users, code) and USPTO for the chosen name.
- Try the sources that failed in this audit: Semantic Scholar, Zenodo, OpenAlex, EUIPO, WIPO Global Brand Database.
- None of this is legal clearance. If commercial use or trademark protection ever matters, that needs separate advice.

## 9. Source files

- `docs/m0_evidence/names/name_search.json` (first search, 2026-09-13)
- `docs/m0_evidence/names/name_verify.json` (independent re-check, 2026-09-13; takes precedence)
- `DECISIONS.md` (N-10)
- `docs/handoff/NEUROSEM_FINAL_SPEC.extracted.md` (lines 154, 529, 758, 759, 762-766)
- `docs/handoff/NEUROSEM_CLAUDE_HANDOFF.extracted.md` (lines 49, 210, 280)
- `docs/glossary.md` (line 40)
- `pyproject.toml`, `CITATION.cff`, `src/neuraxis/cli.py`, `Dockerfile`, `Makefile`, `environment.yml`, `configs/*.yaml`, `.github/workflows/ci.yml`
- Scratch outputs from today's checks: `work/tmp/m0docs/name_conflict_audit/` (`gh_repo_neurosem.json`, `gh_repo_perturbprint.json`, `gh_repo_driftclamp.json`, `vafaei.json`, `rdap_neurosem_com.json`)
