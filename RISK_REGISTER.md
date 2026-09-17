# NeuroSem risk register (Milestone 0, item 5)

*Status: draft, 2026-09-13. Branch `m0-audit`. Author of record: Neel Gurram (decision-maker). Compiled by
Claude Code from repository evidence only. It contains no study results and makes no novelty claims.
A Milestone 6 pilot was running in the background while this was written. Nothing under `results/` was
used as evidence.*

## In plain English

- NeuroSem asks one question: does a small set of test stimuli catch hidden model changes that the usual single test misses?
- The biggest danger is having too few truly independent models to test on. Four of our models come from the same paper and share channel files.
- The second danger is fooling ourselves. The same battery defines which mutants "count", and it helps to compute the tolerances, so numbers can look better than they are.
- The third danger is leakage. Held-out data, and hidden agent-study answers, sit on a machine where an AI assistant can read files.
- Many risks already have code-level fixes. Most of the rest need a decision from you, Neel, before preregistration.
- Six risk groups line up with the spec's "pivot or stop" rules. They are marked **PIVOT** below.
- Docker and CI have never actually run. Treat reproducibility as unproven until they do.
- Severity means "how bad if ignored". Residual risk means "how bad after what is already built".

## How to read this register

- **Sources.** Critique issues come from `docs/m0_evidence/critique/<LENS>.json`. Only issues the skeptic
  (`<LENS>.skeptic.json`) upheld or softened are used, with the skeptic's revised severity and revised
  recommendation. All 67 issues across the five lenses were upheld (33) or softened (34); none was rejected.
  Implementation findings come from `DECISIONS.md`, `docs/build_notes/*.md` and the code under `src/neuraxis/`.
- **Severity.** Where a critique issue is linked, severity is the highest skeptic-revised severity among the
  linked issues. For implementation-only findings: high likelihood with high impact gives high; medium with
  high, or high with medium, gives medium unless the impact is study-level; otherwise low.
- **PIVOT tags** map to the spec's "Failure and pivot criteria"
  (`docs/handoff/NEUROSEM_FINAL_SPEC.extracted.md`, lines 880-887):
  - **P1** Existing validation detects nearly every meaningful mutation.
  - **P2** Most mutations only crash or violate schema.
  - **P3** Selected protocols do not beat random protocols on held-out models.
  - **P4** False positives remain high.
  - **P5** The result depends on one unstable model.
  - **P6** Findings vanish under numerical refinement.
- **INVALIDATES** marks risks that are not spec pivot criteria but could still invalidate the confirmatory
  claim (leakage, conflict of interest, outcome-dependent analysis).

## Summary

| severity | count | ids |
|---|---|---|
| high | 19 | R-01 to R-19 |
| medium | 20 | R-20 to R-39 |
| low | 6 | R-40 to R-45 |

Pivot or stop mapping: **P1** R-07, R-08, R-18 · **P2** R-20, R-21, R-22, R-23 · **P3** R-01, R-09, R-13, R-24 ·
**P4** R-06 · **P5** R-01, R-02, R-04, R-25 · **P6** R-03, R-04, R-05.
Also could invalidate the study: R-10, R-11, R-12, R-14.

---

## Handoff assumptions that are outdated, uncertain, infeasible or scientifically weak

These are the critique issues whose category is `outdated`, `uncertain`, `infeasible`,
`technically_infeasible` or `scientifically_weak`, restricted to issues the skeptic upheld or softened.
Issues categorised only as `underspecified` are in the register but not in this table. "Addressed" means
addressed in the implementation or decision log, not resolved scientifically.

Key: **Yes** = implemented with file evidence · **Partly** = some parts implemented, the rest open ·
**No** = nothing implemented yet · **Neel** = waiting on a decision.

### Outdated

| issue (revised sev.) | handoff assumption, short | addressed? | evidence |
|---|---|---|---|
| INTEG-01 (low) | Journal is "IEEE/ACM TCBB"; only IEEE Access fees matter | No (not needed before pilot) | Venue facts not yet in `DECISIONS.md`; handoff says do not commit to a venue before the pilot |
| INTEG-03 (low) | Only "substantive" AI use must be disclosed | Partly | `AI_USE_LOG.md`, `docs/AI_DISCLOSURE.md` exist; per-artefact provenance column not added |

### Uncertain

| issue (revised sev.) | handoff assumption, short | addressed? | evidence |
|---|---|---|---|
| NEURO-07 (high) | Enough independent, licensed single-compartment models exist | Partly | `docs/model_curation_candidates.md` s.1: 7 candidates in 4 new families; pool would be 13 models in 7 families; strong-sag gap still open |
| INTEG-02 (medium) | A CIBCB conference route can be checked later | No | Cost against the zero budget not recorded in `DECISIONS.md` |
| NUM-01 (medium) | jNeuroML integration method is a non-issue | Yes | `docs/build_notes/core.md` ("jLEMS ignores Meta", first-order evidence); `configs/study.yaml` `numerics` comment; D-007 |
| NUM-04 (low) | Refinement runs share an identical stimulus timing | Partly | `docs/build_notes/core.md` (pulse onsets visible within 2 dt); switch-step logging per dt not implemented |
| SWT-06 (low) | Single-fault detection transfers to real multi-edit changes | No (claim scope) | Primary study is single-fault by design (`docs/MUTATION_CATALOG.md`) |

### Infeasible or technically infeasible

| issue (revised sev.) | handoff assumption, short | addressed? | evidence |
|---|---|---|---|
| STATS-03 (high) | Cluster bootstrap with 4-6 held-out models gives a meaningful CI and test | Partly | `docs/STATISTICAL_ANALYSIS_PLAN.md` s.4.2-4.4 states the limits; `analysis/bootstrap.py:246,278` implement two-sided tests only; the one-sided preregistered sign-flip test is not implemented |
| NUM-07 (high) | Docker and Java are readily available on the laptop | Partly | Portable Temurin in `.tools/` (D-004); direct jar call (D-005); `docs/REPRODUCING.md:17` "Dockerfile never built" |
| INTEG-04 (high) | Hidden tests stay hidden if not public and trials start from a clean commit | Partly | `.gitignore:28,31`; `agent_study/HIDDEN_MANIFEST.sha256` (D-022); exports without Git history (`docs/build_notes/agent-study.md`); OS-level isolation left to a human |
| INTEG-12 (high) | One student can curate 12-16 licensed models and 100-160 mutants, with no calendar | Partly | Manifest has 6 models, 2 included (`docs/model_selection.md` s.3); curation screen (above); no calendar or stop date |
| NEURO-04 (medium) | Wrong-segment-group and spatial-discretisation operators give meaningful mutants | Partly | `reduce_spatial_discretization` reports no sites for single-compartment models (`docs/build_notes/mutations.md` s.2); `wrong_segment_group` still generates expected-equivalent mutants |
| NUM-06 (medium) | The exhaustive battery and immutable raw traces are practical on one laptop | Partly | Content-addressed float32 traces, Git-ignored, hashes tracked (D-012); no measured compute/storage budget yet |
| SWT-03 (medium) | Stimulus and numerical mutants are detectable by other protocols like biophysical ones | Partly | D-009 (stimulus mutants edit only the harness and are excluded from pilot families); numerical family still in `data/splits/discovery_families.txt` |
| INTEG-11 (medium) | Full per-run provenance with immutable raw traces fits in the repository and archive | Partly | `provenance.py` hashing and environment digest; D-012, D-023; budget from measured runs not yet published |
| NUM-05 (low) | Recorded traces are precise enough to align across refinement levels | Yes | `simulators/jneuroml.py:199-230` `regularize_time`; uniform-grid checks (`docs/build_notes/features.md` item 12); `interp_step = 0.01 ms` frozen (D-016) |

### Scientifically weak

| issue (revised sev.) | handoff assumption, short | addressed? | evidence |
|---|---|---|---|
| STATS-01, NEURO-05, SWT-01 (high) | Battery-defined admissibility is a neutral denominator; exhaustive battery is a comparator | Partly | `docs/STATISTICAL_ANALYSIS_PLAN.md` s.3 lists the consequences; canonical is not a selection candidate (`experiments/discovery.py:31`); cascade reporting planned; "full candidate battery (labelling upper bound)" renaming not done |
| STATS-04 (high) | Exact McNemar is appropriate for the paired comparison | Partly | Reported as supporting only (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.4.3); canonical not force-included (`discovery.py:31`) |
| STATS-05, SWT-10 (high) | False-positive rate on battery-verified transforms is unbiased and informative | Partly | Plan forbids filtering transforms on battery results (`docs/STATISTICAL_ANALYSIS_PLAN.md` S3); near-null controls not implemented; formatting transforms were bit-identical in development (`docs/build_notes/transforms.md` s.5) |
| STATS-06 (high, underspecified) | Battery vs canonical isolates the value of added stimuli | Yes (primary), Neel (secondary OMV) | Same features and tolerances for canonical (D-008, D-021); N-06 open |
| STATS-08 (high) | Greedy coverage on curated mutants transfers without curation bias | Partly | Seeded generation, documented grids (`docs/build_notes/mutations.md` s.3); tie-break `[cost, protocol_id]` (`configs/study.yaml`); magnitude grid not preregistered |
| STATS-10, NUM-02, SWT-04 (high) | Numerical mutants are ordinary faults and could be the held-out family | Partly | x2 factor removed, grid x4/x10/x20 (D-021, `mutations/numerical.py:77`); numerical still a discovery and pilot family (`data/splits/discovery_families.txt`, `configs/study.yaml` `pilot`) |
| STATS-11 (high) | Two-model pilot with "at least one silent mutant" supports go/no-go | Partly | Provisional thresholds in `experiments/pilot.py:44-46` (N-04); criterion 1 is still "at least one" |
| NEURO-01 (high) | Rheobase normalisation is harmless for mutants | Yes | Mutants receive the reference's concrete stimuli (D-010) |
| NEURO-11 (high) | Refinement tolerance is meaningful for near-threshold and count features | Partly | Definedness and regime changes under refinement are excluded (D-014); count features use the same max rule (`validation/convergence.py:152-160`); no amplitude-jitter robustness, no observed-order report |
| SWT-09 (high) | Hand-curated mutants and one held-out family give an unbiased generalisation test | Partly | Seeded sampling; held-out family not chosen (N-02); `data/splits/heldout/` holds only a README |
| INTEG-08 (high) | Separating Claude's roles in the manuscript manages the conflict of interest | Partly | D-003 (builder does not run trials); D-022 and N-12 (Neel to review evaluators); no independent check of detection decisions yet |
| NEURO-03 (medium) | Sag and rebound are meaningful for all models; models provide that diversity | Partly | Rebound window handled (`docs/build_notes/features.md` item 3); sag gap open (`docs/model_selection.md` s.7) |
| NEURO-09 (medium) | Detected differences support biological interpretation | No (framing) | Claim taxonomy not yet written |
| NUM-10 (medium) | NEURON export can reuse jLEMS-calibrated tolerances | Not applicable yet | Cross-simulator deferred (N-08) |
| SWT-08 (medium) | Greedy has room to beat random; raw counts measure coverage | Partly | Exact and seeded random baselines, shortfall handling (`docs/build_notes/selection.md` s.3; `discovery.py:34-35`); no preregistered ceiling criterion |
| INTEG-06 (medium) | Logging model and version makes the agent study reproducible | Partly | Freeze hashes in the agent harness (`docs/build_notes/agent-study.md`); CLI version pinning and repeats not fixed |
| NEURO-12 (low) | One silent mutant is informative for proceeding | Partly | Same evidence as STATS-11 |
| SWT-11, SWT-13, SWT-14 (low) | Metamorphic framing; reference divergence as defect oracle; "certificate" wording | No (manuscript framing) | Recommendations not yet applied |

---

## Register

Field order for each risk: description · category · likelihood · impact · mitigation (implemented?) ·
residual · owner · trigger or monitoring signal · evidence.

### High severity

#### R-01 Too few independent held-out clusters **PIVOT P5, P3**
- **Description.** Held-out inference rests on 4-6 base models, fewer once correlated models are grouped. With K clusters the bootstrap has only C(2K-1, K) distinct resamples (35 for K = 4). The two-sided cluster permutation test cannot reach p < 0.05 for K ≤ 5. One unusual model can dominate the difference.
- **Category.** statistics
- **Likelihood: high.** The manifest has 3 source families. The candidate pool would give 7 families, and 4 of those hold only 1-2 models.
- **Impact: high.** The primary generalisation claim (RQ4) could be uninterpretable.
- **Mitigation.** Implemented: `source_family` column and family-level sensitivity clustering (`docs/model_selection.md` s.2, `docs/STATISTICAL_ANALYSIS_PLAN.md` s.2); exact enumeration of sign patterns (`analysis/bootstrap.py:37,291`); 7 new candidates from 4 families (`docs/model_curation_candidates.md` s.1). Not implemented: a preregistered one-sided exact sign-flip test (STATS-03; `bootstrap.py:278` is two-sided); a group rule hashed before splitting (STATS-02); simulation-based precision analysis after the pilot.
- **Residual: high.**
- **Owner.** Neel (N-02, N-09); implementation for the one-sided test.
- **Trigger.** Fewer than 6 independent held-out groups at split freeze. If fewer than about 3-4, preregister held-out results as descriptive or exploratory (STATS-02, INTEG-12).
- **Evidence.** STATS-02, STATS-03, NEURO-07, INTEG-12 (`docs/m0_evidence/critique/`); `docs/STATISTICAL_ANALYSIS_PLAN.md` s.4.2, s.4.4, s.9.1; `docs/model_curation_candidates.md` s.1.

#### R-02 Correlated Pospischil fixtures **PIVOT P5**
- **Description.** RS, LTS, FS and IB share one paper, repository, commit and byte-identical Na, Kd, IM and Leak channel files. A channel-file mutant is nearly the same experiment in sibling cells. A Pospischil cell in held-out is not an unseen model if a sibling is in discovery. Both pilot fixtures are Pospischil cells.
- **Category.** scientific validity
- **Likelihood: high.** Correlation is verified by file hashes.
- **Impact: high.** Overstated generalisation, and dependence on one source family.
- **Mitigation.** Implemented: pilot fixtures are discovery-only (`data/splits/discovery_models.txt`); correlation documented (D-017; `docs/model_selection.md` s.5). Not implemented: rule for splitting families across discovery and held-out (N-09).
- **Residual: high** until at least two independent families are in discovery and held-out models come from other families.
- **Owner.** Neel (N-02, N-09).
- **Trigger.** Any split file placing a Pospischil cell in held-out while another is in discovery.
- **Evidence.** D-017; `docs/model_selection.md` s.5; STATS-02.

#### R-03 Tolerance rule unreliable for count, event and near-threshold features **PIVOT P6**
- **Description.** τ = max(floor, r|f|, c|f_h − f_h/2|) uses one refinement difference. That cannot show asymptotic behaviour. It degenerates for integer counts (zero, or a jump when a spike appears), and near rheobase counts and ISIs are discontinuous. Detections could be numerical artefacts, or vanish under refinement.
- **Category.** numerics
- **Likelihood: high.** Discontinuity near threshold is structural (NEURO-11).
- **Impact: high.** Directly tests the "findings vanish under refinement" stop rule.
- **Mitigation.** Implemented: h, h/2, h/4 levels (`configs/study.yaml` `refinement_factors: [1, 2, 4]`); detection must reproduce at h and h/2 (D-013, D-021); features whose state or regime changes under refinement are excluded and counted (D-014; `validation/convergence.py:136-151`). Not implemented: a separate integer or event rule (counts share the numeric max rule, `convergence.py:152-160`; `spike_count` floor 0.5 in `configs/tolerances.yaml`); per-feature observed order; margin-triggered h/2 confirmation audit; amplitude-jitter robustness (NEURO-11 recommendation 4).
- **Residual: medium-high.**
- **Owner.** Neel (NUM-03 decision, N-03); implementation.
- **Trigger.** Pilot `tolerances.csv` shows many `refinement`-limited entries, or excluded share ≥ 25% (`experiments/pilot.py:45`).
- **Evidence.** NUM-03, NEURO-11; D-013, D-014; `validation/convergence.py`.

#### R-04 Step-sensitive features and the unstable LTS response **PIVOT P6, P5**
- **Description.** jLEMS uses first-order forward Euler. The LTS third spike moves about 50 ms across the tested dt range (4th spike 712-755 ms). Late-spike features get very wide tolerances, or results hinge on one numerically fragile model.
- **Category.** numerics
- **Likelihood: high.** Observed in the development probe.
- **Impact: high.** The result could depend on one unstable model, or on dt.
- **Mitigation.** Implemented: nominal h = 0.005 ms with h/2 and h/4 (D-007); exclusion rule (D-014); per-model results required (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.4.1). Not implemented: model inclusion criterion "reference converges on all candidate protocols" (SWT-13 recommendation 3).
- **Residual: medium.**
- **Owner.** Neel (N-03); implementation for reporting.
- **Trigger.** In the pilot, a single model contributes most silent mutants, or LTS features are mostly `refinement`-limited.
- **Evidence.** `docs/pilot/dt_probe.md`; D-007; `docs/STATISTICAL_ANALYSIS_PLAN.md` s.9.6; NUM-01.

#### R-05 Numerical mutants are circular with tolerance calibration **PIVOT P6**
- **Description.** A dt-multiplier mutant is detected or not largely according to c, the floors and the multiplier, not protocol informativeness. Pooling such mutants in the detection matrix biases greedy selection. Making them the held-out family leaks calibration information.
- **Category.** scientific validity
- **Likelihood: high.** `numerical` is listed in `data/splits/discovery_families.txt` and in `configs/study.yaml` `pilot.mutation_families`.
- **Impact: high.** Biases selection and the primary pooled denominator.
- **Mitigation.** Implemented: factor 2 removed (never admissible, `docs/MUTATION_CATALOG.md` s.5.2); grid x4, x10, x20 (`mutations/numerical.py:77`, D-021); `recording_resolution` is configuration-only (D-009). Not implemented: separate numerical-robustness analysis outside the primary denominator and outside held-out family choice (NUM-02, STATS-10, SWT-04).
- **Residual: high.**
- **Owner.** Neel.
- **Trigger.** Pilot detection matrix shows numerical mutants covering a large share of rows.
- **Evidence.** NUM-02, STATS-10, SWT-04; D-021; `docs/build_notes/science-docs.md` s.1.

#### R-06 False-positive estimate is biased or uninformative **PIVOT P4**
- **Description.** If transforms flagged by the battery are dropped, the false-positive rate is zero by construction. Formatting-type transforms are expected to be bit-identical, so near-zero rates say little about tolerances. A multi-protocol battery makes more comparisons than canonical, which raises its false-positive rate. Clopper-Pearson upper bounds are wide (0/6 gives 0.459).
- **Category.** statistics
- **Likelihood: high.** Development probes were bitwise identical for every compared transform.
- **Impact: high.** "False positives remain high" cannot be judged either way.
- **Mitigation.** Implemented: transforms verified independently, never filtered on battery outcome (`docs/STATISTICAL_ANALYSIS_PLAN.md` S3; `docs/build_notes/science-docs.md` s.7); byte-preserving edits (`docs/build_notes/transforms.md` s.3); pilot threshold ≤ 10% (`experiments/pilot.py:46`, provisional, N-04). Not implemented: near-null controls (h/8, 1e-9 perturbations, second-platform rerun); false positives per comparison and per battery size (SWT-10).
- **Residual: high.**
- **Owner.** Neel (N-04); implementation.
- **Trigger.** All pilot transforms bit-identical, giving 0/n with no information about tolerance scale.
- **Evidence.** STATS-05, SWT-10; `docs/build_notes/transforms.md` s.5.

#### R-07 Canonical baseline definition and window **PIVOT P1**
- **Description.** "Silent" is defined against canonical testing. If the canonical protocol or its analysis window is wrong, P1 is mis-measured. The earlier window rule (earliest pulse) picked non-targeting pulses in three candidates. The Maex models ship no single-cell harness. An OMV-style spike-time baseline, which reflects conventional practice, is not included.
- **Category.** scientific validity
- **Likelihood: medium.** Fixed for current models; candidates remain affected.
- **Impact: high.** Defines the primary contrast and class 6.
- **Mitigation.** Implemented: canonical = shipped harness scored with the same features and tolerances (D-008); union window of pulses targeting the recorded population (`validation/canonical.py:80`, D-021); one reproducible detection rule for canonical and battery (D-021). Not implemented: canonical rule for models without a harness (`docs/build_notes/model-curation.md` s.5); secondary OMV baseline (N-06); baseline windows for Wang-Buzsaki and IB (`docs/build_notes/science-docs.md` s.6).
- **Residual: medium.**
- **Owner.** Neel (N-06); implementation.
- **Trigger.** A candidate whose canonical features are undefined at the reference, or has no harness.
- **Evidence.** STATS-06, SWT-12; D-008, D-021; `docs/build_notes/model-curation.md` s.4-5.

#### R-08 Pilot go/no-go gate is too weak **PIVOT P1, P4 (gate)**
- **Description.** Pilot success needs only "at least one" silent mutant. A predicted-by-construction silent mutant can pass it trivially. The spec's pilot size is inconsistent (2 models with 5-10 mutants per model in Solo scope, versus 2-6 models with 20-60 mutants in M6). The pilot uses 2 mutants per operator per model (`configs/study.yaml`).
- **Category.** statistics
- **Likelihood: high.** `experiments/pilot.py:44` `crit1 = len(silent) >= 1`.
- **Impact: medium-high.** A weak gate could pass a study that should pivot under P1.
- **Mitigation.** Implemented: provisional thresholds for excluded features and false positives (`pilot.py:45-46`). Not implemented: a mechanistic prediction per pilot mutant with predicted-silent cases labelled positive controls (NEURO-12); counts and proportions reported as the progression criterion (SWT-09).
- **Residual: medium.**
- **Owner.** Neel (N-04).
- **Trigger.** Pilot report where every silent mutant was predictable from which voltage range the canonical protocol visits.
- **Evidence.** STATS-11, NEURO-12, SWT-09; `experiments/pilot.py`.

#### R-09 Held-out mutation family is too small and not yet chosen **PIVOT P3**
- **Description.** RQ5 rests on one family. With an even spread, about 3-13 of its mutants land on held-out models (Clopper-Pearson 3/4 gives 0.19-0.99). The choice of family is not made.
- **Category.** statistics
- **Likelihood: high.**
- **Impact: medium-high.** RQ5 is uninformative or depends on the family chosen.
- **Mitigation.** Implemented: `HeldoutGate`, split hashing (`docs/build_notes/selection.md` s.1). Not implemented: family choice, and hashing it before building the discovery matrix (SWT-09).
- **Residual: high.**
- **Owner.** Neel (N-02).
- **Trigger.** The discovery detection matrix is built before a held-out family is hashed.
- **Evidence.** STATS-09, SWT-09; `data/splits/heldout/` (README only).

#### R-10 Held-out leakage in an AI-assisted solo repository **INVALIDATES**
- **Description.** The planned held-out location `data/splits/heldout/` is inside the repository that Claude Code sessions open. Read tools need no approval there. The access log is self-appended. Auto memory from another project loads into sessions (it loaded into the critique review and into this compilation). NeuroSem has no `CLAUDE.md` or `.claude/` settings.
- **Category.** integrity
- **Likelihood: medium.** No held-out files exist yet, but the default workflow would place them inside the repository.
- **Impact: high.** Leakage voids the confirmatory held-out claim.
- **Mitigation.** Implemented: code-level gate (`selection/splits.py` `HeldoutGate`, `LeakageError`; static test that no held-out access happens outside `splits.py`); `SPLITS.sha256` and access log format (`docs/build_notes/selection.md` s.1); D-003 (no held-out evaluation). Not implemented: held-out files outside the repository and outside any session directory; auto memory disabled for NeuroSem; hash-chained log; external timestamp (INTEG-13, INTEG-09).
- **Residual: high.**
- **Owner.** Neel.
- **Trigger.** Any held-out model or manifest file created under the repository root.
- **Evidence.** INTEG-13, INTEG-09, STATS-13; `data/splits/README.md`; `ls` of the repository root (no `CLAUDE.md` or `.claude`).

#### R-11 Conflict of interest: the builder wrote the instruments and the hidden evaluators **INVALIDATES**
- **Description.** The same assistant wrote the mutation operators, classifier, selection, analysis, agent harness and hidden evaluator specs. Benchmark design choices could favour NeuroSem, and agent-study scoring could favour Claude.
- **Category.** integrity
- **Likelihood: medium.** No evidence of bias. The structure of the work creates the risk.
- **Impact: high.** Credibility of the benchmark and the agent study.
- **Mitigation.** Implemented: builder does not run trials (D-003); hidden evaluators Git-ignored with a committed hash manifest (D-022; `.gitignore:28,31`). Not implemented: Neel reviews and signs off operators and classifier before M8; independent hand check of a random sample of detection decisions (INTEG-08); Neel revises hidden specs (N-12).
- **Residual: high.**
- **Owner.** Neel.
- **Trigger.** Reaching M8 or M9 with no logged review in `DECISIONS.md`.
- **Evidence.** INTEG-08; D-003, D-022, N-12; `AI_USE_LOG.md`.

#### R-12 Preregistration timing and analytic forking paths **INVALIDATES**
- **Description.** The planned single preregistration comes after splits, tolerances and selection. Primary k, the minimum material effect, the decision rule and the multiplicity strategy are not fixed. "Most of" nine success criteria is qualitative. The detection-versus-cost curve invites choosing k after the fact.
- **Category.** statistics
- **Likelihood: medium.**
- **Impact: high.**
- **Mitigation.** Implemented: draft plan with a single primary comparison and no confirmatory secondaries (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.4.5, s.5, s.10); `docs/PREREGISTRATION_DRAFT.md`; provisional `budget_k: 4`, B, n_perm and seed (`configs/study.yaml`); freeze lock mechanism (`configs/FROZEN.lock` via `HeldoutGate`). Not implemented: two-stage embargoed OSF registration (INTEG-09, STATS-13); fixed-sequence hierarchy (STATS-12).
- **Residual: high.**
- **Owner.** Neel.
- **Trigger.** Any held-out mutant generated before a stage-1 registration exists.
- **Evidence.** STATS-12, STATS-13, INTEG-09; `docs/STATISTICAL_ANALYSIS_PLAN.md` s.10.

#### R-13 Outcome-dependent mutant curation and magnitude grid **PIVOT P3**
- **Description.** "Carefully curated admissible mutants", combined with admissibility defined by detection, allows keep or drop decisions after outcomes are seen. The magnitude grid and τ jointly control the denominator. Several magnitudes of the same parameter create subsumed mutants. Models with more admissible mutants dominate greedy coverage.
- **Category.** scientific validity
- **Likelihood: medium.**
- **Impact: high.**
- **Mitigation.** Implemented: seeded generation with seed recorded (`docs/build_notes/mutations.md` s.1.1); documented default grids (s.3); single-operator enforcement (s.1.3); deterministic tie-break (`configs/study.yaml` `tie_break`). Not implemented: grid preregistered before detection outcomes; per-parameter (subsumption-reduced) results; redundancy-robust score (SWT-08, NEURO-05).
- **Residual: medium.**
- **Owner.** Neel.
- **Trigger.** Any manual exclusion of a mutant not justified by a rule-based class.
- **Evidence.** STATS-08, SWT-09, SWT-02, NEURO-05.

#### R-14 Battery-conditional denominator (circularity) **INVALIDATES (absolute rates)**
- **Description.** Admissibility is labelled by the same battery, features and tolerances. The full battery scores 100% by construction. Absolute rates and RQ1 silent-drift rates are conditional on the pool and shift with pool size and tolerance. The skeptic notes that paired contrasts are not biased by this.
- **Category.** scientific validity
- **Likelihood: high.** By design.
- **Impact: medium-high.** Misleading absolute claims if not labelled.
- **Mitigation.** Implemented: consequences stated (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.3); fixed and re-derived denominators in sensitivity (s.7); canonical not a selection candidate (`experiments/discovery.py:31`). Not implemented: relabelling the exhaustive battery as a "labelling upper bound"; optional frozen extension set.
- **Residual: medium.**
- **Owner.** Neel (wording); implementation (reports).
- **Trigger.** Any report or draft presenting exhaustive-battery detection as a finding.
- **Evidence.** STATS-01, NEURO-05, SWT-01.

#### R-15 Paired test degenerate or invalid under clustering
- **Description.** McNemar's size can greatly exceed nominal under intracluster correlation. If canonical were in the selected set, one discordant cell would be zero and the test would only restate RQ1.
- **Category.** statistics
- **Likelihood: medium.**
- **Impact: medium-high.**
- **Mitigation.** Implemented: McNemar is supporting only (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.4.3); canonical excluded from candidates (`experiments/discovery.py:31`); cluster bootstrap primary. Not decided: whether to augment or replace (STATS-04).
- **Residual: medium.**
- **Owner.** Neel.
- **Trigger.** A draft report citing McNemar p as primary evidence.
- **Evidence.** STATS-04; `analysis/bootstrap.py:246`.

#### R-16 Agent-study isolation
- **Description.** Trials could see hidden checks through the filesystem, Git history, web tools, loaded memory or `CLAUDE.md`, or training exposure. Sandboxing covers only Bash.
- **Category.** integrity
- **Likelihood: medium.**
- **Impact: high** for the agent study (secondary, claim-bearing).
- **Mitigation.** Implemented: exports without framework or Git history, normalised timestamps, refusal of unsafe private locations, freeze hashes (`docs/build_notes/agent-study.md`); hidden files Git-ignored (D-022). Not implemented: OS-level isolation (human responsibility); WebFetch and WebSearch denied; canary strings; clean `CLAUDE_CONFIG_DIR` and disabled auto memory (INTEG-04, INTEG-05). CI secrecy: hidden assets must stay out of any CI-readable path (NUM-09).
- **Residual: high.**
- **Owner.** Neel (N-12).
- **Trigger.** Any trial launched from a directory with an ancestor `CLAUDE.md` or with auto memory on.
- **Evidence.** INTEG-04, INTEG-05, NUM-09; D-022.

#### R-17 Docker and CI never built or run; reference platform undecided
- **Description.** The Dockerfile was never built (Docker is not installed; Windows 11 Home is not listed for Docker Desktop's WSL 2 backend). `.github/workflows/ci.yml` exists, but there is no Git remote, so CI has never run. The Linux lock was checked on paper only.
- **Category.** reproducibility
- **Likelihood: high.**
- **Impact: medium-high.** Frozen-study data need one reference platform. "Code reproduces tables" is a success criterion.
- **Mitigation.** Implemented: portable, hash-verified Temurin (D-004); direct jar invocation (D-005); emulated build context test run, 764 passed (`docs/REPRODUCING.md:16`). Not implemented: a real Docker or Linux run; reference platform choice (NUM-07); remote repository (N-01).
- **Residual: high.**
- **Owner.** Neel (platform, N-01); implementation.
- **Trigger.** Preregistration freeze attempted without a successful Linux or container run.
- **Evidence.** NUM-07; `docs/REPRODUCING.md:13-21`; `git remote -v` (empty).

#### R-18 Stimulus family cannot be silent; unit under test **PIVOT P1 (bias)**
- **Description.** Stimulus mutants edit only the shipped harness, so only canonical can see them and they can never be class 6. If pooled, they bias the primary contrast toward canonical.
- **Category.** scientific validity
- **Likelihood: high.** Structural.
- **Impact: medium.** Direction is against the hypothesis, but it distorts P1.
- **Mitigation.** Implemented: excluded from pilot families (D-009; `data/splits/discovery_families.txt`); stimulus-only mutants reuse the reference battery (D-012). Not decided: exclude from the primary population, or report both (`docs/STATISTICAL_ANALYSIS_PLAN.md` S4).
- **Residual: low-medium.**
- **Owner.** Neel.
- **Trigger.** Stimulus family added to discovery or held-out lists.
- **Evidence.** NEURO-10, SWT-03; D-009; `docs/build_notes/science-docs.md` s.3.

#### R-19 Rheobase definition and normalisation
- **Description.** Rheobase may be non-positive (spontaneously active cells), non-monotone, or crash small cells at the default bracket. Per-mutant renormalisation would absorb excitability faults. The rheobase counter and eFEL use slightly different spike rules.
- **Category.** scientific validity
- **Likelihood: medium.** Prinz and Maex Golgi candidates fire spontaneously; small-soma cells crashed at 0.05 nA.
- **Impact: high** if mishandled.
- **Mitigation.** Implemented: reference-anchored concrete stimuli for all variants (D-010); 12-point, 4-round search with recorded resolution; retries with a smaller upper amplitude (D-021); spontaneous fallback 0.1 nA (`configs/study.yaml`); rheobase floor ≥ 2x search resolution (`configs/tolerances.yaml`, `convergence.py:153-156`); inverted-bracket defect fixed (D-021). Not implemented: unit test on a near-threshold trace comparing both spike rules (`docs/build_notes/science-docs.md` s.9); rules for spontaneously active models beyond the fallback.
- **Residual: low-medium.**
- **Owner.** Implementation; Neel (N-07).
- **Trigger.** Rheobase status `spontaneous` or `error` for an included model.
- **Evidence.** NEURO-01, NEURO-02, NUM-12, STATS-14; D-010, D-021.

### Medium severity

#### R-20 Blow-up classification (non-executable vs numerically unstable) **PIVOT P2**
- **Description.** jLEMS aborts inside rate expressions before writing output. Class 2 versus class 3 therefore depends on log text. Runaway voltage in high-input-resistance cells (Ih-block runs) aborts mid-run. Classes are dt-dependent.
- **Category.** numerics
- **Likelihood: medium.**
- **Impact: medium.** Shifts the cascade proportions used by P2.
- **Mitigation.** Implemented: started-and-hint gives `UNSTABLE`, started without hint gives `RUNTIME_ERROR`, otherwise `BUILD_ERROR` (`simulators/jneuroml.py:166-176`; `_DT_HINT` at line 33 matches "too large a time step", NaN or Infinity; D-020); non-finite or |V| > 10 V output check (`simulators/base.py:20`, D-021). Not verified: coverage of every divergence mode (evidence is from Kd-rate and HH-rate failures only, `docs/build_notes/core.md` s.2); category change under refinement not reported (NUM-11).
- **Residual: medium.**
- **Owner.** Implementation.
- **Trigger.** Pilot cascade where class 2 counts are dominated by mid-run aborts.
- **Evidence.** NUM-11; D-020; `docs/build_notes/model-curation.md` s.1, s.7.

#### R-21 Structural validator coverage gaps **PIVOT P2**
- **Description.** `jnml -validate` does not schema-check included files. Test 10025 misses `channelDensityVShift` and concentration-model references. Upstream LTS files fail standalone validation by design. Structurally invalid mutants can pass as valid.
- **Category.** tooling
- **Likelihood: high.** Verified.
- **Impact: medium.** Misclassification between classes 1 and 2.
- **Mitigation.** Implemented: relative oracle over the whole include closure (`validation/structural.py:4-17`, D-006); such variants become class 2 and are flagged `canonical_runs_but_battery_failed` (`experiments/campaign.py:285`, D-020); warnings are not failures and a jNeuroML load crash is `valid=False` (D-021). Open: report the gap upstream (N-11); confirm `jnml -validate` as the frozen oracle (`docs/model_selection.md` s.10.8).
- **Residual: low-medium.**
- **Owner.** Neel (N-11); implementation.
- **Trigger.** Structurally "valid" mutants that fail to build in probes.
- **Evidence.** D-006, D-020; `docs/build_notes/mutations.md` s.4; SWT-05.

#### R-22 `omit_include` masked by the shipped harness **PIVOT P2**
- **Description.** `LEMS_RS.xml` and `LEMS_LTS.xml` include channel files directly. The canonical run may build while the generated probe fails, so the mutant becomes class 2 (worst run status).
- **Category.** scientific validity
- **Likelihood: high.**
- **Impact: medium.** Inflates "crash" counts and hides a real canonical miss.
- **Mitigation.** Implemented: worst-status classification with a flag (D-020; `campaign.py:285`). Not decided: intended class (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.8, decision 9).
- **Residual: medium.**
- **Owner.** Neel.
- **Trigger.** Pilot shows `canonical_runs_but_battery_failed` mutants.
- **Evidence.** `docs/build_notes/science-docs.md` s.4; D-020.

#### R-23 Equivalent mutants distort the cascade and the budget **PIVOT P2**
- **Description.** `wrong_segment_group` on single-compartment cells, `solver_config` (Meta ignored, bit-identical traces), lengthened `sim_length` or `stim_duration`, `shift_initial_voltage`, and IM mutants in FS are equivalent or expected to be. They waste budget and could distort the "most faults merely crash" judgement.
- **Category.** scientific validity
- **Likelihood: high.**
- **Impact: medium.**
- **Mitigation.** Implemented: class 4 excluded from N and reported per operator (`docs/MUTATION_CATALOG.md` s.5.1); no sites for spatial discretisation in single-compartment cells (`docs/build_notes/mutations.md` s.2); Meta no-op pinned by test (`docs/build_notes/core.md`, "jLEMS ignores Meta"). Not implemented: mark by-construction-equivalent operators inapplicable (NEURO-04); static dead-element check (SWT-02). Unverified: the skeptic's source reading says `eulertree` changes the jLEMS path, but executed runs were bit-identical for RS and LTS.
- **Residual: medium.**
- **Owner.** Implementation; Neel.
- **Trigger.** Class 4 above half of pilot mutants for an operator.
- **Evidence.** SWT-02, NEURO-04; `docs/MUTATION_CATALOG.md` s.5.1.

#### R-24 Random baselines and the "cannot beat random" outcome **PIVOT P3**
- **Description.** A dense or redundant detection matrix leaves greedy no room to beat random. Treatment of canonical, prerequisites and ties changes the baselines. Relabelling a loss as a "ceiling effect" after the data are seen would be post hoc.
- **Category.** statistics
- **Likelihood: medium.**
- **Impact: high** if it triggers P3; the specification gaps themselves are medium.
- **Mitigation.** Implemented: count-matched uses the actual battery size, with shortfall recorded (`experiments/discovery.py:34`; `docs/build_notes/selection.md` s.3.1); runtime-matched random-order first fit (s.3.2); enumeration when small (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.6); cost in cell-steps (D-015). Not implemented: preregistered ceiling criterion; exact optimum and greedy gap report (SWT-07); redundancy-collapsed score.
- **Residual: medium.**
- **Owner.** Neel; implementation.
- **Trigger.** Discovery expected random coverage close to greedy coverage.
- **Evidence.** STATS-07, SWT-08, SWT-07.

#### R-25 LTS responds weakly to several battery protocols **PIVOT P5**
- **Description.** For LTS (rheobase about 0.039 nA) the 3 ms 10x pulses and the 0-3x ramp evoke no spikes, and the -2x rebound protocol shows no rebound. Much of the battery may be uninformative for one of only two pilot models.
- **Category.** scientific validity
- **Likelihood: high.** Observed in the smoke run.
- **Impact: medium.**
- **Mitigation.** Implemented: undefined-at-reference features are detectable only by becoming defined, and are counted in the pilot report (`experiments/pilot.py` report lines). Not decided: amplitude rules for low-rheobase models (N-07); per-reference applicability matrix (NEURO-03).
- **Residual: medium.**
- **Owner.** Neel (N-07).
- **Trigger.** Pilot report lists many LTS protocols with zero reference spikes.
- **Evidence.** D-010, N-07.

#### R-26 Compute and storage budget
- **Description.** Models × protocols × variants × refinement levels, plus rheobase searches, may exceed laptop time or disk. No measured budget exists.
- **Category.** schedule
- **Likelihood: medium.**
- **Impact: medium.**
- **Mitigation.** Implemented: float32 traces, Git-ignored, hash-tracked, re-simulated on demand (D-012); cache reuse for identical inputs; batched probes (D-011); byte-deterministic trace packing (`docs/build_notes/features.md`). Not implemented: budget from measured pilot numbers before M8 (INTEG-11, NUM-06).
- **Residual: medium.**
- **Owner.** Implementation; Neel (approve storage policy).
- **Trigger.** Pilot wall time or disk growth extrapolates beyond a stated budget (for example 72 h, NUM-06).
- **Evidence.** NUM-06, INTEG-11; D-012.

#### R-27 Schedule: no calendar, time boxes or stop date
- **Description.** The full study (12-16 models, 100-160 mutants, agent study) has no calendar. Blocking curation issues remain.
- **Category.** schedule
- **Likelihood: high.**
- **Impact: medium.**
- **Mitigation.** Not implemented: time boxes, stop date, predefined minimum viable study that cuts mutants per model first (INTEG-12).
- **Residual: medium.**
- **Owner.** Neel.
- **Trigger.** Pilot-to-preregistration interval slips without a written cut-down plan.
- **Evidence.** INTEG-12; `docs/model_curation_candidates.md` s.1 (blocking issues).

#### R-28 No licensed single-compartment Ih / sag model
- **Description.** No manifest model has Ih. Candidate sags are weak (granule) or in a spontaneously active cell (LP). Sag features will carry little information, and non-zero sag appears without Ih (RS about 0.015).
- **Category.** scientific validity
- **Likelihood: high.**
- **Impact: medium.** Diversity claim and informativeness of P07.
- **Mitigation.** Implemented: search documented; Ih-block controls run on candidates (`docs/model_curation_candidates.md` s.1). Not decided: continue search, keep sag as uninformative, or drop it from diversity goals (`docs/model_selection.md` s.7).
- **Residual: medium.**
- **Owner.** Neel.
- **Trigger.** Preregistration still lists sag diversity without an Ih model.
- **Evidence.** NEURO-03; `docs/model_selection.md` s.7; `docs/build_notes/features.md` (observed facts).

#### R-29 Firing-regime labels are ill-defined
- **Description.** eFEL has no regime classifier. Burst metrics disagree. Regime depends on stimulus intensity. A single fixed block voltage (-40 mV) mislabelled an HH plateau at -40.8 mV.
- **Category.** scientific validity
- **Likelihood: medium.**
- **Impact: medium.** Categorical detections and "interpretable regime change" claims.
- **Mitigation.** Implemented: frozen label order and rules (`features/regimes.py`; `docs/build_notes/features.md` item 9); explicit config key `depolarization_block_v_mV` (D-021); regime changes under refinement excluded (D-014). Not decided: per-model or relative block voltage.
- **Residual: medium.**
- **Owner.** Neel; implementation.
- **Trigger.** Regime detections concentrated near the block-voltage cut-off.
- **Evidence.** NEURO-08; `docs/build_notes/features.md`.

#### R-30 Settling and initial state
- **Description.** Initial-voltage and onset mutants need a stable rest. LTS may keep slow state (T-current inactivation, Ca pool) beyond the 300 ms settle.
- **Category.** scientific validity
- **Likelihood: medium.**
- **Impact: medium.**
- **Mitigation.** Implemented: `settle_ms: 300` (`configs/study.yaml`); integer-ms edges on refinement grids (`docs/build_notes/core.md`). Not implemented: settling criterion check (NEURO-06); integer `settle_ms` enforcement (core.md hazards).
- **Residual: low-medium.**
- **Owner.** Implementation.
- **Trigger.** `shift_initial_voltage` mutants detected in LTS baseline features.
- **Evidence.** NEURO-06; `docs/MUTATION_CATALOG.md` (shift_initial_voltage row).

#### R-31 Container provenance
- **Description.** Inside the image there is no `git`, so the commit would be unknown and the run marked dirty. An image cannot know its own digest.
- **Category.** reproducibility
- **Likelihood: medium.**
- **Impact: medium.** Spec requires a commit for every simulation.
- **Mitigation.** Implemented: `NEUROSEM_GIT_COMMIT` fallback (`provenance.py:68`, which still returns dirty = True); `NEUROSEM_CONTAINER_IMAGE` included in the digest (`provenance.py:87`). Unverified: never exercised in a real container (R-17).
- **Residual: medium.**
- **Owner.** Implementation.
- **Trigger.** Container run records with `dirty=True`.
- **Evidence.** `docs/build_notes/infra.md` items 2-3.

#### R-32 "Exactly one fault" and validity oracles
- **Description.** A textual diff cannot define one change for includes, references or unit rewrites. lxml re-serialisation is not byte-minimal.
- **Category.** tooling
- **Likelihood: low.** Now largely enforced.
- **Impact: medium.**
- **Mitigation.** Implemented: typed-edit footprints, per-operator `check_record`, tamper tests, `xml_changes` for audit (`docs/build_notes/mutations.md` s.1.3, s.4); byte-minimal seeds for agent exports (`docs/build_notes/agent-study.md`).
- **Residual: low.**
- **Owner.** Implementation.
- **Trigger.** Manual 20-mutant audit finds a multi-fault mutant.
- **Evidence.** SWT-05.

#### R-33 License open items
- **Description.** L-01 to L-12 are open. They cover docs and data licenses, LGPL mutants of the HH example, five carve-out `.mep` files tracked in Git, the GPL text next to `LICENSE.lesser`, image publication duties, REUSE metadata and a human review.
- **Category.** licensing
- **Likelihood: medium.** Only matters at release.
- **Impact: medium.**
- **Mitigation.** Implemented: model files keep their own licenses (D-018); fail-closed license gate for candidates (`docs/model_curation_candidates.md` s.2); no release without Neel (D-003). Not implemented: every row of `LICENSE_AUDIT.md` s.11.
- **Residual: medium.**
- **Owner.** Neel (N-05, L-01 to L-12).
- **Trigger.** First public push (N-01).
- **Evidence.** `LICENSE_AUDIT.md` s.11; INTEG-10.

#### R-34 Name conflict
- **Description.** "NeuroSEM" is a 2025 CMAME simulation framework with code, an active GPL-3.0 GitHub project spelled "NeuroSem", and a neuromarketing company holding neurosem.com.
- **Category.** licensing
- **Likelihood: high.**
- **Impact: medium.** Discoverability, confusion, possible trademark issue. The audit is not legal clearance.
- **Mitigation.** Recommendation only: rename before public release (PerturbPrint preferred). Code keeps `neurosem` (N-10).
- **Residual: medium.**
- **Owner.** Neel (N-10).
- **Trigger.** Any public artefact under the working name.
- **Evidence.** `docs/NAME_CONFLICT_AUDIT.md` s.8; DECISIONS N-10.

#### R-35 Agent-study reproducibility and cost
- **Description.** The Claude Code CLI updates often. Models retire. The cleanest isolation mode (`--bare`) needs an API key, which conflicts with the zero budget. One run per task is uninformative. Nine task definitions are not a sample size.
- **Category.** reproducibility
- **Likelihood: high.**
- **Impact: medium.** Secondary study.
- **Mitigation.** Implemented: frozen hashes of policy, tasks and runner; provisional budgets (`configs/agent_policy.yaml`; `docs/build_notes/agent-study.md`). Not implemented: pinned CLI version, repeats per task, funding decision, void-and-rerun rule (INTEG-06, INTEG-07).
- **Residual: medium.**
- **Owner.** Neel.
- **Trigger.** M9 planning without a funding route.
- **Evidence.** INTEG-06, INTEG-07.

#### R-36 Cross-simulator comparisons
- **Description.** NEURON's default step is first-order implicit, while jLEMS is explicit Euler. Reusing jLEMS tolerances for NEURON-translated models inflates false positives.
- **Category.** numerics
- **Likelihood: low.** Deferred.
- **Impact: medium.**
- **Mitigation.** Deferred (N-08). Recommendation: separate transformation class with NEURON's own refinement.
- **Residual: low.**
- **Owner.** Neel (N-08).
- **Trigger.** NEURON added to scope.
- **Evidence.** NUM-10.

#### R-37 Integrator identity and Meta handling
- **Description.** The handoff implicitly treats the integrator as a non-issue. A fixture setting `simultaneous` or a future jar honouring Meta would change the method.
- **Category.** numerics
- **Likelihood: low.**
- **Impact: medium.**
- **Mitigation.** Implemented: forward-Euler evidence and Meta no-op pinned by test (`test_probe_battery.py::test_meta_integrator_method_does_not_change_trace`, `docs/build_notes/core.md`); jar hash and version recorded (D-004). Not implemented: grep of fixtures for `simultaneous` (NUM-01).
- **Residual: low.**
- **Owner.** Implementation.
- **Trigger.** The pinned Meta test fails after a jar update.
- **Evidence.** NUM-01; D-004, D-007.

#### R-38 Claim scope and biological interpretation
- **Description.** "Biological interpretation" and "neuroscience case studies" could be read as biological validity. Tolerances come from numerics, not experimental variability. Terms such as "certificate" and "metamorphic" may mislead reviewers.
- **Category.** scientific validity
- **Likelihood: medium.**
- **Impact: medium.**
- **Mitigation.** Handoff's final decision rule forbids unsupported biological claims (NEURO-09 skeptic). Not implemented: claim taxonomy; differential-testing framing (SWT-11, SWT-13, SWT-14).
- **Residual: low-medium.**
- **Owner.** Neel.
- **Trigger.** Manuscript drafting.
- **Evidence.** NEURO-09, SWT-11, SWT-13, SWT-14.

#### R-39 Conference route cost
- **Description.** CIBCB is in person only (EUR 700-930 registration plus travel), which conflicts with the zero budget.
- **Category.** schedule
- **Likelihood: high** if pursued.
- **Impact: medium.**
- **Mitigation.** None recorded. Handoff says no venue commitment before the pilot.
- **Residual: low.**
- **Owner.** Neel.
- **Trigger.** Venue decision after the pilot.
- **Evidence.** INTEG-02.

### Low severity

#### R-40 `record_wrong_variable` scaling
- **Description.** `load_dat` multiplies every column by 1000, so a gating variable in [0, 1] becomes 0-1000 "mV". The earlier 250 mV bound would have made these class 3. With the 10 V bound they are compared behaviourally, but voltage features on a non-voltage column have no clear meaning.
- **Category.** tooling
- **Likelihood: high.**
- **Impact: low.** Stimulus family only, outside pilot families.
- **Mitigation.** Implemented: bound raised to 10 V (`simulators/base.py:20`, D-021). Open: classification rule (`docs/build_notes/science-docs.md` s.2).
- **Residual: low.**
- **Owner.** Neel.
- **Trigger.** Stimulus family re-enters scope.
- **Evidence.** `docs/build_notes/science-docs.md` s.2; `docs/build_notes/mutations.md` s.2.

#### R-41 Time-label and onset precision
- **Description.** jLEMS prints time labels with about 7 significant digits. Pulse switches are evaluated after the Euler update (at most one step off).
- **Category.** numerics
- **Likelihood: medium.**
- **Impact: low.**
- **Mitigation.** Implemented: labels replaced by the exact grid t0 + i·dt, rejecting jitter above 0.25 step (`simulators/jneuroml.py:199-230`); uniform-grid position check (`docs/build_notes/features.md` item 12); integer-ms stimulus edges. Not implemented: logging the actual switch step per dt level (NUM-04).
- **Residual: low.**
- **Owner.** Implementation.
- **Trigger.** `regularize_time` rejects a trace.
- **Evidence.** NUM-04, NUM-05; `docs/build_notes/core.md` ("jLEMS OutputFile format").

#### R-42 Determinism across hosts
- **Description.** jLEMS uses `java.lang.Math`, which is not bit-for-bit identical across platforms.
- **Category.** reproducibility
- **Likelihood: medium.**
- **Impact: low.** Absorbed by tolerances if hashes are compared only within one platform.
- **Mitigation.** Implemented: bitwise reference determinism check in the pilot (`experiments/pilot.py:40`); trace hash re-verification on re-simulation (D-012). Not implemented: written cross-host policy (NUM-08).
- **Residual: low.**
- **Owner.** Implementation.
- **Trigger.** Hash mismatch on re-simulation on a different machine.
- **Evidence.** NUM-08.

#### R-43 Protocol cost definition
- **Description.** Wall time is noisy (JVM start-up, load).
- **Category.** tooling
- **Likelihood: low.**
- **Impact: low.**
- **Mitigation.** Implemented: cost = simulated cell-steps, including the whole rheobase search, with wall time recorded (D-015; `selection/matrix.py` `cell_step_costs`). Open: P03 and canonical charging (`docs/STATISTICAL_ANALYSIS_PLAN.md` s.10.7).
- **Residual: low.**
- **Owner.** Neel.
- **Trigger.** None before freeze.
- **Evidence.** NUM-13; D-015.

#### R-44 Coupling effect not tested
- **Description.** Detecting single faults may not transfer to compensating multi-edits.
- **Category.** scientific validity
- **Likelihood: medium.**
- **Impact: low.** Claim scope only.
- **Mitigation.** Primary claims restricted to single-fault mutants (spec). Not implemented: threats-to-validity statement.
- **Residual: low.**
- **Owner.** Neel.
- **Trigger.** Manuscript drafting.
- **Evidence.** SWT-06.

#### R-45 Venue naming, AI disclosure wording and preprint path
- **Description.** TCBB title changed. The IEEE AI policy requires disclosure of all AI-generated content. arXiv needs endorsement. JOSS needs 6 months of public history.
- **Category.** integrity
- **Likelihood: medium.**
- **Impact: low.**
- **Mitigation.** Implemented: `AI_USE_LOG.md`, `docs/AI_DISCLOSURE.md`; no public release without Neel (D-003). Not implemented: provenance column, N-01 notes.
- **Residual: low.**
- **Owner.** Neel.
- **Trigger.** Submission planning.
- **Evidence.** INTEG-01, INTEG-03, INTEG-14.

---

## Unverified items and documentation inconsistencies found while compiling

- **`eulertree` behaviour.** Skeptic source readings (SWT-02, SWT-04, STATS-10) say it changes the jLEMS path. Executed runs were bit-identical for RS and LTS (`docs/build_notes/mutations.md` s.4). Not settled for other models.
- **Divergence classification coverage.** `_DT_HINT` was checked against Kd and HH rate failures only.
- **Container fallbacks** (`provenance.py:68,87`) have never run inside a real container. CI has never run.
- **OMV `compare_arrays` semantics** as a detection oracle were not checked (STATS-06, INTEG-08 skeptics).
- **Licensed model shortfall** is uncertain: NeuroML-DB per-model licenses were not examined (NEURO-07).
- **`docs/STATISTICAL_ANALYSIS_PLAN.md` contradicts itself.** Section 2 says 1 − DR_canonical equals the silent-survival rate since D-021. Section 4.1 still says "DR_canonical is not 1 - silent-survival rate". `docs/build_notes/science-docs.md` s.10 describes the pre-D-021 mismatch.
- **Stale build notes.** `docs/build_notes/features.md` item 11 still cites a 250 mV bound; the code uses 10 V (`simulators/base.py:20`). `docs/build_notes/mutations.md` s.3 lists `increase_dt` x2 and x5; the code uses x4, x10, x20 (`mutations/numerical.py:77`). `docs/build_notes/core.md` s.2 describes the old `BUILD_ERROR` behaviour, which `jneuroml.py:166-176` has replaced.
- **Milestone 6 pilot** outcomes were not read. Every "trigger" that names a pilot output is still to be checked when the pilot finishes.
