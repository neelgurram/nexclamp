# Name-conflict audit: "Neuraxis"

Searches run on 2026-09-16 (local date; the machine clock showed 2026-09-17 01:14 to 01:18 UTC). The raw evidence, one object per source or query, is in `docs/m0_evidence/names/neuraxis_audit_2026-09-16.json`. The earlier audit of the old name "NeuroSem" is in `docs/NAME_CONFLICT_AUDIT.md`. This document does not change it.

**This is not legal trademark clearance.** It records what public sources returned on one day. A zero count means only that the source returned nothing for that query at that time.

## In plain English

- The spec keeps "Neuraxis" provisional until the name has been searched in the listed places. This document records those searches.
- The software package names are free. There is no `neuraxis` project on PyPI, conda-forge, npm, crates.io or CRAN, and no GitHub account called `neuraxis`.
- Most scholarly hits use "neuraxis" as an ordinary anatomy word (the brain and spinal cord axis). Those are not name conflicts. They do mean a search for "Neuraxis" will turn up thousands of anatomy papers (PubMed: 2,092 title/abstract hits).
- **The serious problem is a company.** NeurAxis, Inc. is a US medical-device company listed on the NYSE American stock exchange (ticker NRXS). It sells a nerve-stimulation device (IB-Stim) and owns neuraxis.com. That puts it in neuromodulation, next to this project's own field.
- **That company holds two live US trademark registrations for NEURAXIS** (Reg. Nos. 7715671 and 7715689, registered 2025-03-04, class 10, nerve stimulator apparatus). Those cover devices, not software. But the name is identical and the fields are neighbours.
- Other uses are small: about 20 GitHub repositories (a Markdown notes tool, several AI-agency sites, a new Python repository created on 2026-09-15), a German IT company, and a medical-device firm that renamed itself.
- Some sources could not be checked: Google Scholar blocked the request, the EUIPO, TMview and WIPO pages need JavaScript, the UK IPO query did not work, and GitHub code search needs a login.
- **Recommendation: rename.** The earlier first choice, **PerturbPrint**, still had zero hits today on PyPI, conda-forge, GitHub and USPTO. **DriftClamp** is the backup. The decision is Neel's.

Analogy: calling a home-made hiking app "Garmin Trails". The app store may let you, but readers and search engines will send people to the big company, and that company has a registered name to protect.

---

## 1. Method

- Variants searched: `Neuraxis`, `neuraxis`, `NeurAxis`, and `neur-axis` on PyPI and GitHub. PyPI and GitHub searches ignore case, so `NeurAxis` and `neuraxis` give the same result there.
- APIs were called with `curl` from Git Bash, without logging in. Web searches used the WebSearch tool. One SEC filing was read with WebFetch (a model summary, not a full read).
- Controls: PyPI `efel` returned 200, conda-forge `numpy` returned 200, USPTO `google` returned 194 records, and UK IPO `google` returned 0 records (so the UK IPO query did not work; see 2.6).
- Nothing was registered, reserved or submitted. No accounts or logins were used.
- Conflict levels are the auditor's judgement: none, low, medium or high.

## 2. Results by source

### 2.1 Package registries

| Source | Query / URL | Answered | Hits | Conflict |
|---|---|---|---|---|
| PyPI JSON API | `https://pypi.org/pypi/neuraxis/json`, `.../neur-axis/json`, `https://pypi.org/simple/neuraxis/` | Yes | 0 (all HTTP 404; control 200) | None |
| PyPI web search | `https://pypi.org/search/?q=neuraxis` | **No.** A JavaScript bot-check page came back instead of results. | n/a | Not assessed |
| conda-forge | `https://api.anaconda.org/package/conda-forge/neuraxis` | Yes | 0 (HTTP 404; control 200) | None |
| npm (extra) | `https://registry.npmjs.org/neuraxis` | Yes | 0 (404) | None |
| crates.io (extra) | `https://crates.io/api/v1/crates?q=neuraxis` | Yes | 0 | None |
| CRAN (extra) | `https://crandb.r-pkg.org/neuraxis` | Yes | 0 (404) | None |
| Read the Docs (extra) | `https://readthedocs.org/api/v3/projects/neuraxis/` | Yes | 0 (404) | None |

### 2.2 Code hosting

| Source | Query / URL | Answered | Hits | Relevant hits | Conflict |
|---|---|---|---|---|---|
| GitHub account | `https://api.github.com/users/neuraxis` | Yes | 0 (404) | The exact login is unclaimed | None |
| GitHub user search | `https://api.github.com/search/users?q=neuraxis` | Yes | 8 | **Neuraxis-Labs** org (created 2026-08-27) hosts a robustness-testing tool for time-series foundation models (pushed 2026-09-16). `neuraxisltd` is an empty org from 2019. The others are personal accounts with 0 or 1 public repositories. | Low |
| GitHub repository search | `https://api.github.com/search/repositories?q=neuraxis&per_page=100` | Yes (complete) | 20 | `timabell/markdown-neuraxis` (Markdown notes tool, Rust, 46 stars, active). `bstBizEra/neuraxis` (Python, created 2026-09-15, conformance-suite PRs). `MAHAD6798/NEURAXIS.AI` ("NeurAxis.AI" disease-diagnostics demo app, one day of activity). `parasdahal/neuraxis` (ML service, archived 2017). Several 2026 AI-agency and landing-page repos. **No neuroscience modelling tool.** 15 of the 20 were created in 2025 or 2026. | Low-medium |
| GitHub phrase `"neur-axis"` | `https://api.github.com/search/repositories?q=%22neur-axis%22` | Yes | 12 | Only near-spellings (NeuroAxis, NeuralAxis, NeuraAxis). One of them is `WangQian-NUSLiuLab/NeuroAxis`, with no description. | Low |
| GitHub code search | `https://api.github.com/search/code?q=neuraxis` | **No** (HTTP 401, needs a login) | n/a | n/a | Not assessed |
| GitLab | `https://gitlab.com/api/v4/projects?search=neuraxis`, `.../groups?search=neuraxis` | Yes | 0 | Public projects and groups only | None |

### 2.3 Literature and data repositories

"Neuraxis" is standard anatomy vocabulary, so literature hits are expected. None of the screened hits was a tool, dataset or product named Neuraxis.

| Source | Query / URL | Answered | Hits | Relevant hits | Conflict |
|---|---|---|---|---|---|
| Google Scholar | `https://scholar.google.com/scholar?q=%22neuraxis%22+software` | **No.** The page said the system could not perform the operation. | n/a | Not searched directly. Two substitute web searches (a `site:scholar.google.com` query and a neuroscience-tool query) found no research software named Neuraxis. | Not assessed (substitute: none) |
| PubMed | `esearch.fcgi?db=pubmed&term=neuraxis[tiab]` | Yes | 2,092 | Not screened one by one. PubMed maps the plain word to the MeSH term "central nervous system" (1,794,764 records). | None as a name conflict; high search noise |
| IEEE Xplore | WebSearch `neuraxis site:ieeexplore.ieee.org` | Yes (web search) | 9 | All anatomical or unrelated, e.g. an intrathecal tracer study "along neuraxis" (document 8770104) | None |
| arXiv | `export.arxiv.org/api/query?search_query=all:neuraxis` (also `ti:`); `arxiv.org/search/?query=neuraxis` | Yes | 0 | none | None |
| bioRxiv | WebSearch `neuraxis site:biorxiv.org` (the bioRxiv API has no keyword search) | Yes (web search) | 9 | All anatomical preprints | None |
| Europe PMC preprints (extra, bioRxiv supplement) | `query=neuraxis AND SRC:PPR` | Yes | 49 | The first 30 titles were all anatomical (bioRxiv, Research Square) | None |
| Zenodo | `https://zenodo.org/api/records?q=neuraxis&size=25` (also `title:neuraxis`) | Yes. The first try with size=50 got HTTP 400 because of the page-size limit, and the retry worked. | 15 (title-only: 3) | Anatomical case reports and papers. No software or dataset named Neuraxis. | None |
| Crossref (extra) | `query.bibliographic=neuraxis` | Yes | 294 (fuzzy) | Top 30 anatomical, including dictionary entries titled "Neuraxis" | None; high noise |
| DataCite (extra) | `query=neuraxis` | Yes | 123 | Anatomical theses and articles. One software hit, VirtualFlyBrain `geppetto-vfb` v2.2.10.4, matched the word somewhere in its metadata. It is not named Neuraxis. | None |
| OpenAlex (extra) | `works?search=neuraxis` | Yes | 9,866 | Count only, not screened | None; high noise |

### 2.4 General web (Google-style search)

The WebSearch tool was used. It is not Google itself.

| Query | Answered | Relevant hits | Conflict |
|---|---|---|---|
| `"Neuraxis" company`; `"NeurAxis" neuromodulation IB-Stim` | Yes | **NeurAxis, Inc. (NYSE American: NRXS), neuraxis.com.** A medical-technology company in Carmel, Indiana, selling IB-Stim, an FDA-cleared nerve-field stimulation device for abdominal pain. It was renamed from Innovative Health Solutions in March 2022 and listed in August 2023. It is very active: a press release dated 2026-09-16 announces wider insurance coverage. | **High** |
| `"Neuraxis Ltd" OR "Neuraxis GmbH" OR "Neuraxis Labs" OR "Neuraxis Technologies"` | Yes | **neuraxis IT Solutions GmbH** (Germany, incorporated 2016, reported active; Tracxn summary, not checked in the German company register). The neuraxismed.com page says "Neuraxis is now hypoflo", a medical-device firm that renamed itself. | Low |
| `"neuraxis" software OR python OR github OR platform`; `"Neuraxis" AI OR neurotech OR startup -NRXS` | Yes | The GitHub projects in 2.2. Near-names: Neuraxle/Neuraxio (AutoML library), NeuraX (CLI assistant). Neurotech newsletters mention NeurAxis, Inc. | Low-medium |
| `"Neuraxis" toolbox OR framework OR "open-source" neuron model` | Yes | No neuron-modelling tool named Neuraxis | None |

### 2.5 Domains (extra)

| Domain | Method | Result |
|---|---|---|
| neuraxis.com | RDAP (Verisign) | Registered 1998-07-22, expires 2027-07-21, locked. Serves NeurAxis, Inc. |
| neuraxis.org | RDAP (PIR) | Registered 2002-02-21, expires 2028-02-21. Holder not identified. |
| neuraxis.io | RDAP (rdap.org) | 404. This proves nothing for .io (see the earlier audit). |
| neuraxis.ai | RDAP (rdap.org) | Redirect with an empty body. Not determined. |

### 2.6 Trademarks

| Office | Query / URL | Answered | Result | Conflict |
|---|---|---|---|---|
| **USPTO** | POST to `https://tmsearch.uspto.gov/prod-stage-v1-0-0/tmsearch`, the undocumented backend of the tmsearch web app (same method as the NeuroSem audit). Wordmark `neuraxis`, then wildcard `neuraxis* OR neur-axis* OR neuroaxis*`. | Yes (control `google` = 194) | 4 exact-wordmark records, 8 with the wildcard. **LIVE: NEURAXIS, Reg. No. 7715671** (serial 97327951) and **LIVE: NEURAXIS, Reg. No. 7715689** (serial 97356330). Both are owned by Neuraxis, Inc., registered 2025-03-04, class 10, nerve stimulator apparatus. The company's 10-K lists a word mark and a stylized mark. DEAD: NEURAXIS 87791864 (Neuraxis, LLC, Michigan, abandoned 2019). DEAD: NEURAXIS 74429400 (epidural needles, abandoned 1994). Similar live applications: NEUROAXISS (99715168, class 10, filed 2026-03-20) and NEUROAXIS (99562753, class 5, filed 2025-12-23). The company's FY2023 10-K also mentions a July 2022 trademark agreement related to its name; the terms are not given. | **High** |
| EUIPO eSearch | `https://euipo.europa.eu/eSearch/#basic/.../neuraxis` | **No** (JavaScript app, no results in the HTML) | Not verified | Not assessed |
| TMview (EU and national offices) | `https://www.tmdn.org/tmview/#/tmview/results?...basicSearch=neuraxis` | **No** (JavaScript app) | Not verified | Not assessed |
| WIPO Global Brand Database | `https://branddb.wipo.int/en/similarname/results?...neuraxis` | **No** (JavaScript app) | Not verified. It is unknown whether the US marks were extended abroad under the Madrid system. | Not assessed |
| UK IPO | `https://trademarks.ipo.gov.uk/ipo-tmtext/page/Results?searchType=text&wordMarkText=neuraxis` | **No.** The page said 0 marks, but the control `google` also said 0, so the query parameters were ignored. | Not verified | Not assessed |
| Web search for EU, WIPO or UK marks | `"NEURAXIS" EUIPO OR WIPO OR "UK IPO" trade mark` | Yes | Only generic office pages. No mark was found, and none was ruled out. | Not assessed |

## 3. What could not be checked

1. Google Scholar (blocked). Web-search substitutes only.
2. EUIPO, TMview and WIPO Global Brand Database (JavaScript apps). UK IPO (query not honoured). **Non-US trademark status is therefore unknown.**
3. GitHub code search (requires a login).
4. The PyPI web search page (bot check). The PyPI JSON API did answer.
5. The IEEE Xplore and bioRxiv native search APIs. Site-restricted web searches were used instead.
6. PubMed and OpenAlex hits were counted but not screened one by one.
7. Company registries (Companies House, US state registries, the German Handelsregister) were not searched. The GmbH comes from a Tracxn summary.
8. The SEC 10-K details come from a WebFetch summary. The trademark agreement's counterparty and terms are not public in that summary.
9. Owners of neuraxis.org and neuraxis.ai are unknown.

## 4. Overall assessment

| Area | Conflict |
|---|---|
| Package and account names (PyPI, conda-forge, npm, crates, CRAN, RTD, GitHub login, GitLab) | None |
| Literature (PubMed, IEEE, arXiv, bioRxiv, Zenodo, Crossref) | None as a name, but heavy search noise from the anatomy term |
| Open-source projects (GitHub) | Low-medium: about 20 small repos, none in neuroscience modelling |
| Companies and web presence | **High**: NeurAxis, Inc., a listed neuromodulation company that owns neuraxis.com |
| US trademarks | **High**: two live NEURAXIS registrations in class 10 (nerve stimulators) owned by that company |
| EU, UK and international trademarks | Unknown |

**Why the overall risk is high even though the goods differ.** The live marks cover nerve-stimulation devices (class 10), and this project is free research software (class 9/42 if it were ever registered). Different classes lower the legal risk, but they do not remove it when the name is identical and the fields are neighbours. A neuromodulation company and a neuron-model validation tool both sit in "neurotech", and the company is listed, active and has shown it protects its name (the 2022 trademark agreement and two registrations). Apart from the law:

- a web search for "Neuraxis" returns the company first, and a literature search returns anatomy papers, so the project would be hard to find;
- reviewers or readers could assume an affiliation with a medical-device company, which is unwelcome in a validation paper;
- the name does not describe the method, much like "NeuroSem" did not.

## 5. Recommendation

**Rename. Do not keep "Neuraxis", even with conditions.** The decision is Neel's.

| Option | Assessment |
|---|---|
| Keep Neuraxis | Not recommended. It is identical to a live US registered mark held by a listed neurotech company, and discoverability is poor. |
| Keep with conditions (e.g. "Neuraxis-Fingerprint", lower-case `neuraxis` only, a disclaimer) | Not recommended. The dominant word is still the registered mark, and search results would still be dominated by the company and the anatomy term. |
| **Rename to PerturbPrint (preferred)** | Matches the project's defined term "perturbation fingerprint". The NeuroSem audit found zero hits in every source that answered. Re-checked today: PyPI 404, conda-forge 404, GitHub user 404, repositories 0, USPTO wordmark 0. The known weak spot remains that "Perturb-" suggests Perturb-seq screens. |
| Rename to DriftClamp (backup) | Re-checked today: PyPI 404, conda-forge 404, GitHub user 404, repositories 0, USPTO 0. The earlier audit found 102 GitHub code identifiers using it, and "clamp" suggests lab hardware. |

Today's re-check of the two alternatives covered only registries, GitHub and USPTO. Before adopting either one, run this same full source list for it: literature, Zenodo, web, EUIPO/TMview, WIPO and UK IPO, ideally in a browser, because those trademark sites need JavaScript. Repeat the registry and trademark checks just before any public release. If the project is ever commercialised or a trademark is wanted, get professional legal advice. This audit is not a substitute for it.

## 6. Files

- `docs/m0_evidence/names/neuraxis_audit_2026-09-16.json`: raw evidence (35 source/query objects)
- `docs/NAME_CONFLICT_AUDIT.md`: earlier audit of "NeuroSem" and the alternatives (unchanged)
- `docs/m0_evidence/names/name_search.json`, `name_verify.json`: evidence for the earlier audit
