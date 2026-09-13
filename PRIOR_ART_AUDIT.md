# Prior-art audit

*Milestone 0 deliverable (spec "Required novelty sweep"). Written 2026-09-13 on branch `m0-audit`.
Evidence: `docs/m0_evidence/prior_art/`. Matrix: `docs/novelty_matrix.csv`, built reproducibly by
`scripts/build_novelty_matrix.py`. No study results exist; nothing here is a finding about NeuroSem's
performance.*

## In plain English

- Before claiming something is new, you check whether someone already did it.
- We searched eleven kinds of sources with over 1,500 queries. We then opened and checked 335 of the works we found.
- Every separate ingredient of NeuroSem already exists somewhere:
  - testing models against saved results;
  - multi-stimulus fingerprints of neurons;
  - picking stimuli that tell models apart;
  - mutation testing;
  - picking a small test suite.
- What we did **not** find is the full combination for neuron models. That combination is: deliberately break models in controlled ways, set tolerances from the solver's own error, choose a small stimulus battery, and show that it still works on models and fault types it never saw.
- Think of a smoke detector. Detectors, test buttons and building codes all exist. The new part would be proving which small set of detectors catches fires in *new* buildings.
- A hostile reviewer could still say "this is standard technique applied to a new field". The answer has to come from data, not wording. So any novelty claim waits for held-out results.
- Not finding something is not proof it does not exist. Some databases blocked automated searching, and some candidates were only screened.

---

## 1. What was searched

### 1.1 Sources and queries

Eleven finder runs recorded 1,552 queries: eight search lenses plus three gap-filling runs requested by a completeness critic. Counts are the queries whose recorded source matches each service. Some queries hit several services.

| Source required by the spec | Queries recorded | Notes |
|---|---|---|
| Google Scholar | 59 | Mostly through web search with site filters; direct access is limited |
| PubMed | 103 | NCBI E-utilities and the PubMed tools |
| IEEE Xplore | 28 | Web search with site filter; also DBLP (34) and Crossref |
| ACM Digital Library | 25 | Web search with site filter; also DBLP |
| Web of Science / Scopus | **0** | **Not searched: no access** (the spec says "if accessible") |
| Semantic Scholar | 64 | Frequently rate-limited (HTTP 429) |
| arXiv | 120 | API often rate-limited; web search fallback |
| bioRxiv | 72 | Web search with site filter and Europe PMC (279 queries), which indexes preprints |
| GitHub | 163 | REST API and code search |
| PyPI | 61 | Web search with site filter and the PyPI JSON API |
| Zenodo | 120 | The API returned HTTP 504 for much of the session |
| Also used | OpenAlex 187, web search 181, DBLP 34, Crossref | Extra indexes beyond the spec's list |

**Search terms.** Every search term the spec lists was run, including combinations:
- "conductance neuron model metamorphic testing" (28 queries);
- "NeuroML mutation testing" (41);
- "neuron model semantic regression" (29);
- "behavior(al) preservation neuronal model conversion" (23);
- "perturbation fingerprint neuron model" (33);
- "automatic stimulation protocol selection model validation" (24);
- "mutation testing computational neuroscience" (29);
- "AI coding agent neuron simulation" (21).

The final specification added two terms, and they were run far less often:
- "scientific software testing NeuroML" (4);
- "LLM computational neuroscience code" (5).

### 1.2 Access problems (recorded in the finder files)

- **OpenAlex:** HTTP 429 ("insufficient budget") after the anonymous daily quota ran out.
- **Semantic Scholar Graph API:** HTTP 429 on many requests, with no API key.
- **arXiv API:** HTTP 429, 503 and timeouts for much of the session.
- **DBLP:** an anti-bot page instead of results.
- **Zenodo REST API:** HTTP 504 on many requests.
- **Web search tool:** a per-session budget of 200 calls was exhausted in several finder runs, so some site-filtered fallbacks did not run.
- **Europe PMC references endpoint:** HTTP 503 (maintenance). Crossref references were used instead.

These gaps reduce recall. They are listed again under open items (section 7).

## 2. How candidates were verified

1. **Screening.** Finders returned candidate works with a URL or DOI taken from a retrieved result. Each got an estimated closeness from 1 (irrelevant) to 5 (could anticipate NeuroSem's core claim).
2. **Deep read.** Every candidate estimated at closeness 2 or higher in the first round was checked against a primary source: Crossref, the DOI landing page, the publisher, the arXiv, PubMed, OpenAlex or Semantic Scholar APIs, or GitHub, PyPI or Zenodo for software. Its abstract, and where possible its methods or README, was read. The matrix columns were then filled with *yes / no / partial / unclear* plus a short justification, and closeness was re-rated.
3. **Interruption and rescoping.** A session limit interrupted the second-round deep reads. They were re-run for all 73 second-round candidates estimated at closeness 3. The 144 second-round candidates estimated at closeness 2 were **screened but not deep-read**. They are listed in `docs/m0_evidence/prior_art/screened_not_deep_read.json`, are not matrix rows, and are counted here.
4. **Result** (`docs/m0_evidence/prior_art/novelty_matrix_summary.json`):
   - 54 deep-read evidence files;
   - **335 unique verified works**, after removing 39 duplicates;
   - 1 candidate rejected at verification;
   - closeness: 100 at 1, 204 at 2, **31 at 3**, **none at 4 or 5**.

The matrix columns follow the spec: citation, year, model type, mutations, multiple stimuli, electrophysiology features, protocol optimisation, held-out evaluation, AI transformations, software availability, and distinction from NeuroSem. Closeness, kind, DOI, URL, verification method, finder route and evidence file are added for traceability.

## 3. What NeuroSem reuses and must not claim

The specification's novelty boundary is confirmed by verified works (examples; the full list is in the matrix):

| Established capability | Verified examples |
|---|---|
| Standard neuron-model representation, validation and simulation | NeuroML/LEMS, pyNeuroML and jNeuroML (see `DEPENDENCY_AUDIT.md`); OSB Model Validation (OMV; Marin and Gleeson) |
| Regression tests against saved traces or spike times | OMV (tolerance-based comparison of NeuroML model outputs in continuous integration) |
| Testing neuron models against experimental features across many protocols | NeuronUnit (Gerkin et al.), HippoUnit (Sáray et al. 2021), Appukuttan and Davison 2022 |
| Multi-protocol, rheobase-scaled electrophysiological characterisation of NeuroML models | NeuroML-DB (Birgiolas et al. 2023) |
| Parameter perturbation effects on features; validation on unseen stimuli | Reva et al. 2023 (BluePyEModel universal workflow) |
| Running one protocol battery across versions of a model | Cardiac functional curation and Web Lab (Cooper et al. 2011, 2016; Daly et al. 2018) |
| Choosing effective or informative stimuli | Druckmann et al. 2011; Lei et al. 2022; Patten-Elliott et al. 2024/2025 |
| Mutation testing of continuous or simulation models, and test selection under budget | Zhan and Clark 2005; Brillout et al. 2010; Matinnejad et al. 2016/2019; Arrieta et al. 2019; Ling and Menzies 2023; Bartocci et al. 2025 |
| Mutation sensitivity and tolerance in scientific software | Hook and Kelly 2009; Gray and Kelly 2010; Kelly, Gray and Shao 2011 |
| Metamorphic testing of scientific and simulation software, including LLM-translated code | Srinivasan and Kanewala 2022; Clark et al. 2023; Li et al. 2026; Ludwig et al. 2026 (Kaizen); Song et al. 2026 |
| Rigorous evaluation of AI-generated code | Liu et al. 2023 |

NeuroSem uses these as dependencies, baselines or background. It must not present any of them as its contribution.

## 4. Closest prior work: novelty stress test

A hostile-reviewer agent examined the eight closest lines of work. For each, it tried to argue that the work already anticipates NeuroSem, then searched for follow-up work by the same groups (`docs/m0_evidence/prior_art/stress_test_r2.json`). Every verdict was **"partially anticipates"**. None does the whole integrated method.

| Line of work | Already done there | Not done there |
|---|---|---|
| OMV | Tolerance-based regression of NeuroML model outputs in CI, across simulators | Tolerances set by hand; no controlled mutants; no protocol selection; no held-out evaluation |
| NeuronUnit / HippoUnit | Many protocols and features, reusable across models | Reference is experimental data, not the model's own previous version; no mutants; no selection |
| NeuroML-DB | Multi-protocol, rheobase-scaled fingerprints of NeuroML cells; notes that fixed stimuli characterise some models poorly | Fingerprints serve clustering; missing values imputed; better protocol choice left as future work |
| Reva et al. 2023 | One-parameter perturbations and their effect on features; validation on unseen stimuli and morphologies | Sensitivity analysis, not edit detection; no battery selection; no held-out mutation family |
| Cardiac functional curation / Web Lab | The closest idea: rerun one protocol battery on each model version; a real model-file error was found this way | No systematic mutants; no calibrated tolerances or pass/fail rule; cardiac models only |
| Druckmann et al. 2011 | Compares stimulus sets on withheld stimuli; aims for a minimal effective set | Goal is constraining parameters to data, not catching edits; no faults |
| Ion-channel optimal experimental design (Lei; Patten-Elliott) | Optimises protocols to discriminate model variants; robustness to an out-of-design model | Variants are competing hypotheses, not unintended edits; continuous design, not a library; no false-alarm control or unseen variant family |
| Mutation-guided testing of Simulink/CPS models | Seeded faults in continuous models; small suites; budgeted and cost-aware selection; random baselines | Selection by surrogate goals (coverage, diversity), not mutant detection; no calibrated tolerances; no held-out models or families |

**Most defensible distinction** (the same in all eight): measuring how well stimulation protocols detect behaviour-changing edits in conductance-based neuron models. Specifically:
- using controlled single-fault mutants and admissible, behaviour-preserving transformations;
- using tolerances calibrated by numerical refinement;
- testing whether a battery chosen on some models and mutation families transfers to held-out ones, against canonical and cost-matched random batteries.

## 5. Obviousness risk and what the data must show

| Lens | Risk | Why |
|---|---|---|
| Software testing / mutation analysis | **High** | Mutant-based test adequacy, greedy minimisation over a detection matrix and cost-aware selection are standard. Without a strong transfer result, NeuroSem reads as a routine application. |
| Computational neuroscience / model validation | **Medium** | OMV, NeuroML-DB fingerprints and protocol design already point in this direction. |

To overcome the objection, the frozen study would need to show most of the following. These are the specification's own success criteria, sharpened by the review.
1. Silent, behaviour-changing transformations occur at meaningful rates, not only in contrived cases. The canonical test, and one or two obvious extra protocols, do not already catch nearly all of them.
2. The selected battery beats count-matched and runtime-matched random batteries on **held-out models and a held-out mutation family**, with a frozen split.
3. The selected battery also beats simple alternatives from the literature at matched cost:
   - protocols people already use: the shipped canonical test, NeuroML-DB-style rheobase-multiple steps, standard NeuronUnit/HippoUnit sets;
   - coverage- or diversity-based selectors.
4. Refinement-calibrated tolerances keep false alarms on valid transformations low, compared with fixed hand-set tolerances.
5. Which protocol detects which mutation family can be explained by the neurons' dynamics.
6. Results hold across more than one source family of models (the pilot pair is correlated; see `RISK_REGISTER.md`).

## 6. Candidate novelty statement (conditional; not a claim yet)

*Candidate wording, to be used only if the held-out results support it.* To our knowledge, this is the first study to evaluate mutation-guided selection of stimulation protocols for regression testing of conductance-based neuron models. Detection tolerances are calibrated against numerical refinement, and transfer is tested on held-out models and a held-out mutation family. The selection and mutation techniques are standard; the contribution is their calibrated adaptation to this setting and the transfer evidence.

**Claims to avoid:**
- a new selection algorithm;
- the first mutation testing of simulation models;
- the first multi-protocol neuron fingerprinting;
- the first automated NeuroML regression testing;
- the first demonstration that one reference trace can hide errors;
- the first protocol optimisation for discriminating electrophysiology models;
- any biological-validity claim;
- any finding stated before data exist.

## 7. Open items and limits

- **Not searched:** Web of Science and Scopus (no access).
- **Rate-limited or blocked:** OpenAlex, Semantic Scholar, arXiv API, DBLP and Zenodo (section 1.2). Rerunning those queries with API keys or on another day would improve recall.
- **Under-searched terms:** the final spec's two added terms, "scientific software testing NeuroML" (4 queries) and "LLM computational neuroscience code" (5), were run much less than the others.
- **Screened but not deep-read:** 144 candidates estimated at closeness 2 (`screened_not_deep_read.json`).
- **Flagged for a deep read by the stress test:** Peng et al. 2016 (reuse of simulation experiment specifications during model extension; abstract unavailable) and Ugarte et al. 2025 (mutation-based multi-objective test selection; no abstract in Crossref).
- **Critic round not run:** the third completeness-critic round was interrupted by the session limit.
- **Abstract-only readings:** several rows rest on abstracts only, because full texts were paywalled. Each row's `verification_method` says so.
- **Before any manuscript:** Neel should spot-check the closeness-3 rows and the stress-test verdicts (`AI_USE_LOG.md`: AI-verified is not human-verified).

## 8. Files

| File | Content |
|---|---|
| `docs/novelty_matrix.csv` | 335 verified works with the spec's columns, sorted by closeness |
| `docs/m0_evidence/prior_art/finder_*.json` | Queries, candidates and blocked sources for each finder |
| `docs/m0_evidence/prior_art/deepread_*.json` | Verified rows and rejections |
| `docs/m0_evidence/prior_art/critic_r2.json` | Completeness critic (round 2) |
| `docs/m0_evidence/prior_art/stress_test_r2.json` | Anticipation verdicts and obviousness analysis |
| `docs/m0_evidence/prior_art/screened_not_deep_read.json` | Candidates not deep-read |
| `docs/m0_evidence/prior_art/novelty_matrix_summary.json` | Counts produced by the build script |
| `scripts/build_novelty_matrix.py` | Rebuilds the matrix from the evidence files |
