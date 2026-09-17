# Project name decision packet

Searches ran on 2026-09-16, local date. The machine clock showed 2026-09-17, 02:01 to 02:25 UTC. The raw evidence is in `docs/m0_evidence/names/name_candidates_2026-09-16.json`: 8 names and 179 source/query records, each marked answered or not. This packet builds on `docs/NAME_AUDIT.md` (Neuraxis) and `docs/NAME_CONFLICT_AUDIT.md` (NeuroSem). It does not change either one.

> **This is not legal trademark clearance.** It only records what public sources returned on one day. A zero means the source found nothing for that query at that moment. Non-US trademark offices were not searched.

## In plain English

- **Why a new name is needed.** "Neuraxis" is identical to two live US trademark registrations held by NeurAxis, Inc., a listed neuromodulation company (see `NAME_AUDIT.md`). "NeuroSem" had already been set aside earlier.
- **What was compared.** Eight names: the two earlier finalists, PerturbPrint and DriftClamp, plus six new ones (SpikeParity, IsoSpike, EphysPrint, TwinTrace, ClampPrint, VoltPrint).
- **Package names are free for all eight.** Every name is unclaimed on PyPI, conda-forge and npm, including the hyphenated forms.
- **The names differ in other ways:**
  - existing products or projects using the name;
  - other meanings in the science literature;
  - similar trademarks.
- **Recommendation: PerturbPrint.** It is still clean in every source that answered, and it is the project's own term ("perturbation fingerprint"). **SpikeParity** is the new runner-up. **DriftClamp** comes third.
- **Drop IsoSpike and TwinTrace.** "Isospike" is already a named technique in nonlinear dynamics, the same maths that neuron models use. "TwinTrace" is already used by a Windows app, a German battery project and a taken GitHub login.
- **Neel decides.** Nothing has been registered or reserved.

Analogy: choosing a team name for a science fair. First you check that no other team already wears it (package registries and GitHub). Then you check it doesn't mean something else to the judges (literature). Last, you check no company owns it (trademarks). PerturbPrint passes all three checks we could run. The one check we could not run is the international trademark offices.

## 1. Internal identifier rule

The study identifier **`neuron_model_behavioral_validation` stays fixed whatever the brand is.** It keeps the same spelling in:

- preregistration records;
- frozen-study directories;
- evidence file names;
- the internal metadata.

Renaming, re-branding or dropping a brand never changes it. The brand is only a public label: the package name, repository name, DOI title and paper title. It can be decided or changed separately.

## 2. Method

- **Registries and code hosting.** Unauthenticated `curl` from Git Bash to:
  - the PyPI JSON API, including hyphen and underscore variants (PyPI ignores case);
  - conda-forge on anaconda.org;
  - the npm registry;
  - the GitHub users and repository-search APIs;
  - the GitLab projects API.
- **Literature.** The Zenodo, arXiv and PubMed APIs. Extra sources: Europe PMC and Crossref. Google Scholar was fetched with curl; seven of the eight queries answered.
- **bioRxiv and IEEE.** No keyword API was used. Instead, WebSearch was run restricted to those two domains. These were combined OR queries, so the evidence is weak.
- **General web.** The WebSearch tool, which is not Google.
- **USPTO.** A POST to the tmsearch web app's undocumented backend (`https://tmsearch.uspto.gov/prod-stage-v1-0-0/tmsearch`), the same method as the earlier audits. Three searches per name:
  - the exact wordmark;
  - the name followed by a wildcard (`name*`);
  - the two-word form, as a phrase.

  Near-mark prefix searches were also run. The tmsearch web page itself is a JavaScript app and was not used.
- **Domains.** RDAP for .com (Verisign) and .org (PIR). This only hints at whether a domain is registered.
- **Controls.** All answered as expected:
  - PyPI `efel`: 200;
  - conda-forge `numpy`: 200;
  - npm `react`: 200;
  - Zenodo `neuroml`: 19;
  - GitLab `neuroml`: 6;
  - Europe PMC `neuroml`: 256;
  - USPTO `google`: 194;
  - USPTO `neuraxis*`: 4, matching the Neuraxis audit;
  - RDAP `google.com`: 200.
- **Not run: GitHub code search.** It needs a login.

## 3. Comparison table

Key to the table:

- **free** means HTTP 404 on PyPI and conda-forge.
- **GitHub** gives two values: whether the exact login is taken, then the number of repository-search hits.
- **Risk** is the auditor's judgement, not a legal opinion.

| Name | Meaning | PyPI | conda-forge | GitHub (login / repos) | Other software or products | Literature overload | US trademark (USPTO) | Domain hints (.com / .org) | Risk |
|---|---|---|---|---|---|---|---|---|---|
| **PerturbPrint** | perturbation + fingerprint (the project's own term) | free (+ `perturb-print`, `perturb_print`) | free | free / 0 | None found (npm and GitLab 0) | None (Zenodo, arXiv, PubMed, Scholar and Europe PMC all 0). The "Perturb-" stem suggests Perturb-seq tools (PerturbNet, PerturBase). | 0 exact, 0 wildcard. Near: live PERTURBO (Caltech, class 9, physics software). | no record / no record | **Low** |
| **SpikeParity** | the transformed model's spikes stay at parity with the original | free (+ `spike-parity`) | free | free / 0 | None found | None as a name (all 0). "Spike parity" appears as a plain phrase in neuromorphic comparison plots. | 0 exact, 0 wildcard, 0 phrase. The word PARITY is crowded (128 marks, several live in class 9); no SPIKE + PARITY mark. | no record / no record | **Low** |
| **DriftClamp** | hold behavioural drift fixed | free (+ `drift-clamp`) | free | free / 0 | No product. The earlier audit found 102 GitHub code identifiers (code search not re-run today). | None (all 0). "Drift" and "clamp" carry electrophysiology lab meanings. | 0 exact, 0 wildcard, 0 phrase. Near: live DRIFTCLIP (class 6, metal connectors). | no record / no record | **Low-medium** |
| **EphysPrint** | electrophysiology + fingerprint | free (+ `ephys-print`) | free | free / 0 | None found | None (all 0) | 0 exact, 0 wildcard. Near: **live OPEN EPHYS** (Open Ephys, Inc., classes 9 and 42, electrophysiology), same field. | no record / no record | **Medium** |
| **ClampPrint** | clamp protocols + fingerprint | free (+ `clamp-print`) | free | free / 0 | Web results dominated by 3D-printable "clamp print-in-place" models | None (all 0) | 0 exact, 0 wildcard, 0 phrase (dead CLAMPPOD only) | no record / no record | **Medium** (poor discoverability; reads as 3D printing) |
| **VoltPrint** | voltage + fingerprint | free (+ `volt-print`) | free | free / 2 (power-meter tool, 2022; empty repo, 2026) | VoltPrints Etsy shop and "Volt Print" social accounts (3D printing) | None (all 0) | 0 exact, 0 wildcard, 0 phrase | **voltprint.com registered 2026-03-28** / no record | **Medium-high** |
| **TwinTrace** | twin models, matching traces | free (+ `twin-trace`) | free | **login taken** / 6 | **TwinTrace duplicate-file app (Microsoft Store)**; **TwinTRACE battery digital-twin project (CustomCells, Fraunhofer IPA)** | None (all 0) | 0 exact. Phrase "TWIN TRACE": 1 **dead** mark (Ela Medical, pacemaker sensors, cancelled 2009). | **twintrace.com registered 2025-10-02** / no record | **High** |
| **IsoSpike** | iso (same) + spike | free (+ `iso-spike`) | free | free / 1 (isotope-geochemistry tool) | Python repo for isotope "double-spike" data reduction | **High.** "Isospike diagrams" are an established nonlinear-dynamics method: PubMed 9 (Chaos, Phys Rev E, PCCP), arXiv 1, Crossref 2. Scholar did not answer. | 0 exact, 0 wildcard, 0 phrase | no record / **isospike.org registered** | **High** |

Sources checked and answering for every name:

- package registries: PyPI, conda-forge, npm;
- code hosting: the GitHub user and repository APIs, GitLab;
- literature: Zenodo, arXiv, PubMed;
- web and trademarks: WebSearch, USPTO backend, RDAP.

Google Scholar answered for 7 of 8 names; it did not answer for IsoSpike.

## 4. Notes on each name

**PerturbPrint.** This is the earlier first choice, and it is still clean.
- It had zero hits in every source that answered today and in both earlier audits (the earlier GitHub code search also found 0).
- It fits the project's defined term "perturbation fingerprint" (`docs/glossary.md`).
- Weak spots:
  - "Perturb-" reminds single-cell biologists of Perturb-seq tools, although none is called PerturbPrint.
  - Caltech's live PERTURBO mark (class 9, physics software) shares only the stem. Low concern.
  - The name does not say "neuron" or "validation", so a subtitle should carry that. Example: *PerturbPrint: behavioural validation of transformed neuron models*.

**SpikeParity.** This is the strongest new name.
- It had zero hits for the joined word in every source that answered, and no USPTO SPIKE + PARITY mark.
- It says exactly what the tool checks: whether behaviour matches after a transformation.
- Weak spots:
  - "Parity" is a crowded trademark word, but not in combination with "spike".
  - "Spike parity" is used as a plain phrase in neuromorphic papers. That supports the meaning but may add a little search noise.
  - The name stresses spikes, while the fingerprints also cover subthreshold and passive features.

**DriftClamp.** This is the earlier runner-up.
- The registries, literature and USPTO are all clean.
- Weak spots:
  - About 102 existing GitHub code identifiers use the word (earlier audit; code search needs a login, so it was not re-run).
  - To electrophysiologists, "drift" and "clamp" suggest recording drift and clamp rigs. That could mislead readers about what the software does.

**EphysPrint.** The name is clean as a string, but the "ephys" element is shared with Open Ephys, Inc.
- That company holds a live US registration in software and electrophysiology classes. That is the same field.
- Readers may also expect a data-acquisition or recording tool, not a model-validation tool.

**ClampPrint.** The name is clean in registries and trademarks. But web search is swamped by 3D-printing clamp models, and the meaning is vague.

**VoltPrint.** There are small commercial uses: an Etsy shop and 3D-printing social accounts. The .com domain was registered in March 2026. It is weak on discoverability and would be awkward if any of those users grow.

**TwinTrace.** Reject.
- A Windows app is live under this name.
- An industrial EU battery digital-twin project uses "TwinTRACE".
- The GitHub login is taken, and the .com domain is registered.
- There is also a dead US mark for pacemaker sensors.

**IsoSpike.** Reject.
- "Isospike diagram" is a named method in nonlinear dynamics. It counts spikes per period across parameter planes, which is exactly the kind of analysis done on conductance-based neuron models.
- A neuron-modelling tool with this name would be confused with that technique.

## 5. Ranked recommendation (Neel's decision)

1. **PerturbPrint (recommended).**
   - It is the cleanest in every source that answered, across three separate search rounds.
   - It matches the project's defined vocabulary, so the paper's terms and the tool's name reinforce each other.
   - Its only known issue is the Perturb-seq association, which is manageable with a descriptive subtitle.
2. **SpikeParity (runner-up).**
   - It is equally clean in today's sources and very descriptive of "behaviour preserved".
   - It ranks below PerturbPrint because it was searched only once, it contains a crowded trademark word ("parity"), and it undersells the non-spiking features.
3. **DriftClamp.** The name is clean, but the code-identifier collisions and the lab-hardware connotations make it weaker than the top two.
4. **EphysPrint.** Not recommended, because it overlaps the "ephys" element of a live registered mark in the same field.
5. **ClampPrint.** Not recommended, because of poor discoverability.
6. **VoltPrint.** Not recommended, because of existing small businesses and a registered .com domain.
7. **TwinTrace.** Reject.
8. **IsoSpike.** Reject.

Before adopting the chosen name:

- Complete the manual checks in section 6.
- Repeat the registry and USPTO checks just before any public release.
- If the name is ever commercialised or a trademark is wanted, get professional legal advice.

## 6. What remains unchecked

1. **EUIPO, TMview, WIPO Global Brand Database and UK IPO.** These were not searched for any candidate. In today's Neuraxis audit, EUIPO, TMview and WIPO were JavaScript apps that returned no results in the HTML, and UK IPO ignored the query parameters. They must be checked by hand in a browser for the chosen name, including similar marks in classes 9 and 42. **Non-US trademark status is unknown for every name.**
2. **GitHub code search.** It needs a login. DriftClamp's figure of 102 comes from the earlier audit, and the other names were not code-searched today.
3. **Google Scholar for IsoSpike.** The page returned a "Sorry" notice. The other seven names answered with no matching articles.
4. **bioRxiv and IEEE Xplore.** Only combined site-restricted web searches were run, not native keyword searches, so this is weak evidence.
5. **Crossref and Europe PMC.** These were not run for every name; the JSON records which names were covered. IsoSpike's two Crossref titles were not read.
6. **Domains.** Only .com and .org were checked, through RDAP. A 404 is a hint, not a guarantee. Registrars, .io and .dev were not checked.
7. **Company registries** (Companies House, US state registries, EU registers) were not searched.
8. **Social handles, and app stores other than the one Microsoft Store hit that web search found,** were not searched.
9. **US state trademarks and unregistered (common-law) use** beyond what web search surfaced were not checked.

## 7. Release rule

Until Neel explicitly approves a final brand, **no final brand name may be used in any of these:**

- a package publication (PyPI, conda-forge, npm or any other registry);
- a public repository name or public GitHub/GitLab organisation;
- a Zenodo or other DOI record;
- a preregistration (OSF or other);
- a manuscript or preprint title.

Until then, use the fixed identifier `neuron_model_behavioral_validation` or a neutral working label. Nothing in this packet registers, reserves or claims any name. Nothing was registered, reserved or submitted during the searches, and no accounts or logins were used.

## 8. Files

- `docs/m0_evidence/names/name_candidates_2026-09-16.json`: raw evidence for this packet (8 names, 179 records, with controls)
- `docs/NAME_AUDIT.md`, `docs/m0_evidence/names/neuraxis_audit_2026-09-16.json`: the Neuraxis audit
- `docs/NAME_CONFLICT_AUDIT.md`, `docs/m0_evidence/names/name_search.json`, `name_verify.json`: the NeuroSem audit and earlier PerturbPrint/DriftClamp evidence
