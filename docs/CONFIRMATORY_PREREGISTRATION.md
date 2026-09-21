# Confirmatory preregistration (submission-ready)

*Prepared 2026-09-18 from `docs/PREREGISTRATION_DRAFT.md`, which stays as the working document.
Every field the assistant could resolve from recorded evidence is resolved here, with the reasoning
stated, so the researcher confirms rather than invents. Fields marked **[NEEL]** genuinely require a
person. Submit through AsPredicted (D-036); OSF may mirror it later, never as the original
time-stamp.*

> **Nothing in the confirmatory study may run before this is submitted and verified.** The
> authorisation sentence that releases the run is quoted in section 18.

## What is still needed from Neel

1. Title (section 0). Author list: done 2026-09-20.
2. An AsPredicted account and the submission itself.
3. Confirmation of the two numeric judgements in sections 1 and 14 (a material effect of **0.10**,
   and the held-out set size of **4–6 models**), or different numbers of his choosing.
4. The held-out model list, which does not exist until the screening campaign finishes
   (`docs/HELDOUT_POOL_PLAN.md`). It is filled in at submission and hashed.
5. Sign-off in section 18.

Everything else below is answered.

## 0. Administrative information

| Field | Value |
|---|---|
| Title | **[NEEL]** |
| Authors, affiliation | 1. **Neel Gurram**, FAU High School, Florida Atlantic University, Jupiter, FL, USA (corresponding)<br>2. **Samyak Singh**, FAU High School, Florida Atlantic University, Jupiter, FL, USA<br>3. **Naithik Somisetti**, FAU High School, Florida Atlantic University, Boca Raton, FL, USA<br>*Authors 2 and 3 were added on 2026-09-20, after the AsPredicted submission, which lists Neel Gurram only. This changes no hypothesis, endpoint, split or analysis; it is disclosed in the manuscript.* |
| Registry | **AsPredicted** (D-036). OSF is an optional later mirror and is never presented as the original registration |
| Internal study identifier | `neuron_model_behavioral_validation` (permanent, brand-independent) |
| Public name | undecided (D-050); no brand appears in the registration |
| Repository commit frozen for the study | filled at submission from `git rev-parse HEAD`, tree clean |
| Configuration hashes | `configs/study.yaml`, `features.yaml`, `tolerances.yaml`, recorded by `config_set_sha256()` |
| Matrix hashes | the held-out pre-run manifest, built exactly as `manifests/PILOT2_PRE_RUN.sha256` was |
| Software environment | Python 3.12.10; pyNeuroML 1.3.22; libNeuroML 0.6.7; eFEL 5.7.34; jNeuroML 0.14.0 / jLEMS 0.12.0 (jar SHA-256 recorded per run); Temurin JDK 21.0.12.1+1 |
| **Data already seen at registration** | Pilot 1 (2 models, complete), Pilot 2 (5 models, complete), the pipeline rehearsal, model screening for every candidate, and operator-validation outcomes on four Pilot 2 models. **No held-out model has been mutated, and no held-out outcome of any kind has been generated or inspected.** Details in section 15 |

## 1. Primary hypothesis

**Research question (two-sided).** How much scientific protection does canonical regression provide
for transformed neuronal models, and under what conditions do additional perturbation protocols
provide unique information?

**Directional statement under test.** A compact protocol battery, selected on development models,
detects a higher proportion of admissible non-equivalent mutants on held-out models than a canonical
single-protocol regression test.

- **The study does not depend on this being true.** A result showing canonical regression is
  adequate is a complete, reportable finding, and is the outcome the development data currently
  points toward (section 15). Both outcomes are pre-committed to publication.
- **Compact** means budget *k* = **4** protocols (`selection.budget_k`), chosen before any held-out
  data exists and never enlarged afterwards.
- **Material effect** (the smallest difference worth claiming): **Δ ≥ 0.10**, ten percentage points
  of detection rate. *Reasoning:* the battery costs several times the canonical harness in compute;
  a smaller advantage would not justify recommending it, so a difference below 0.10 is reported as
  "no material advantage" even if a test is nominally significant. **[NEEL to confirm]**
- **Adequacy criterion** (the other side): canonical regression is called adequate when it detects
  **≥ 0.95** of admissible mutants, the threshold already fixed in `BRANCH_RULES`.
- Tests are reported two-sided throughout.

## 2. Primary endpoint

**Δ = DR_selected − DR_canonical**, on held-out admissible mutants.

- **Population.** All admissible non-equivalent mutants of held-out models, pooled across mutation
  families. The kinetics family is additionally reported on its own, because it is the family
  excluded from protocol selection and therefore the genuinely unseen one.
- **Detection rule** (identical for every strategy, in selection and in evaluation): a strategy
  detects a mutant when one of its protocols shows the same (protocol, feature) difference beyond
  tolerance at step *h* **and** at *h/2*. This is the implemented rule
  (`detecting_protocols` / `reproducible_keys`); it is not changed for this study.
- **Unit of analysis** is the mutant; **the unit of generalization is the model** (amendment S-01).
  Pooled figures are always reported with their per-model values.

## 3. Secondary endpoints

1. Unique contribution per protocol: mutants that only that protocol detected.
2. Canonical feature regression (level B) versus canonical full-trace regression (level C), never
   merged.
3. Detection by mutation family and by severity (mild, strong).
4. False-positive rate on valid-transformation controls.
5. Numerical robustness stratum, reported separately and never as semantic drift.
6. Cross-simulator agreement where a NEURON runtime is available (descriptive only).

## 4. Inclusion and exclusion rules

Screening applies the thirteen criteria C01–C13 in `docs/MODEL_CURATION_FINAL_TABLE.md`, with the
runtime budget raised to 4,200 s per variant by amendment H-01 (D-056), a decision made on compute
grounds before any held-out candidate was mutated. Screening may look at a model's *reference*
behaviour only; a model's mutation outcomes stay sealed until the confirmatory run
(`docs/HELDOUT_POOL_PLAN.md`).

## 5. Model and mutation splits

- **Development sources, permanently ineligible as held out:** `pospischil2008`,
  `neuroml2_examples`, `acnet2_traub1991`, `migliore2014`, `osb_allen_hh2`.
- **Held-out set:** 4–6 models from at least three sources not used in development. The list is
  filled in at submission and hashed. **[NEEL, from the screening result]**
- **Pilot models are never held out.** Settled; no exception is available.
- **Unseen family:** kinetics remains excluded from protocol selection
  (`SELECTION_EXCLUDED_FAMILIES`, enforced in code and tested).

## 6–9. Protocols, features, tolerances

Unchanged from the frozen development study and carried over verbatim: the canonical comparator is
each model's shipped simulation; the candidate protocols, the eight primary features, the eFEL
settings and the tolerance rule τ = max(abs_floor, rel·|f_h|, 3·|f_h − f_h/2|) are exactly those in
`configs/`. Tolerance constants are **not** re-derived on held-out data.

**Known limitation, pre-registered rather than discovered later:** on heavily spiking protocols the
reference's own h-versus-h/2 difference is large, so the calibrated trace-RMSE threshold is loose and
RMSE contributes little; full-trace detection there rests on spike count and spike timing. Measured
values are in `docs/PILOT2_PRELAUNCH_DECISION.md` section 10. A time-aligned or spike-aware distance
is prespecified as a **secondary sensitivity analysis only**; the primary rule does not change.

## 10. Primary statistical comparison

Paired counts on the same mutants; cluster bootstrap by `model_id` (by `source_family` where models
share a paper) for the interval; exact McNemar and a cluster permutation test as supporting evidence;
B = 10,000, n_perm = 10,000, seed 20260917. With four to six clusters the interval is coarse by
construction, so per-model values are always reported beside it (amendment S-01).

## 11–13. Undefined features, crashes, equivalent mutants, sensitivity

Carried over unchanged. Undefined features stay undefined and are never replaced by zero; a
definedness mismatch is itself a detection. Structurally invalid, non-executable and numerically
unstable mutants are excluded from the admissible denominator and reported with exact counts.
Tolerance multipliers 0.5, 1, 2, 4 are reported as sensitivity analyses.

## 14. Sample size and stopping

- **Held-out set: 4–6 models**, about 25 variants each, giving roughly 100–150 planned variants.
  **[NEEL to confirm]**
- **Basis:** feasibility, not power. At the amended 4,200 s budget this is roughly 139 CPU-hours,
  about 12 hours on 12 workers. No power analysis is claimed; the interval is reported and
  interpreted as coarse.
- **If fewer than four eligible held-out models exist**, the study stops and reports that the
  held-out design is not feasible with the current candidate pool. A criterion is never lowered to
  reach four.
- **Stopping and inconclusive rules**, fixed in advance: control false-positive rate > 0.10; more
  than half of apparent survivors failing their h/4 confirmation; or ≥ 25% of tolerance entries
  refinement-excluded — any of these makes the result **inconclusive**, reported as such.

## 15. Relationship to the development work, stated honestly

- **Pilot 1** (2 models, 22 admissible model edits): canonical regression detected 22 of 22; the
  battery detected 19. Three cases once described as "silent" were numerical, not semantic.
- **Pipeline rehearsal** on a Pilot 1 model: canonical detection 1.0, zero control false positives,
  branch `C_canonical_adequacy`.
- **Pilot 2** (5 models, 88 primary semantic mutants, 40 controls, 15 numerical stress tests):
  results filled in at submission from `results/processed/pilot2/pilot_v2_outputs/`, including the
  branch classification and the unique-protocol contribution table.
- **Known exposure.** Operator validation simulated four of the five Pilot 2 models before that
  campaign, and nine frozen Pilot 2 mutants share an exact edit with a validated site, so their
  canonical outcome was known in advance (amendment A-01,
  `docs/PILOT2_LEAKAGE_ASSESSMENT.md`). Pilot 2 results are therefore reported both over all
  mutants and over the 79 with no prior exposure. **No held-out model is affected.**
- **Direction of the development evidence.** It currently points toward canonical regression being
  highly protective. This is stated *before* registration precisely so that a confirmatory result in
  the same direction cannot be presented as a surprise, and a result in the other direction cannot
  be presented as expected.

## 16. Deviations

Every deviation is recorded in `docs/DEVIATION_LOG.md` with its reason and its effect, reported in
the manuscript, and appended to the registration. Existing deviations X-01 to X-25 are part of the
public record.

## 17. AI-assisted development and the agent study

The method, code and documents were built with AI assistance, logged in `AI_USE_LOG.md` and
disclosed per `docs/AI_DISCLOSURE.md`. The agent study is a **separate secondary experiment** with
its own frozen prompts, hidden evaluators and registration; it is never the headline claim, and its
current status is a feasibility pilot only (`docs/AGENT_STUDY_PILOT.md`).

## 18. Sign-off and the authorisation sentence

I confirm that no held-out outcome was generated or inspected before this registration, and that
every **[NEEL]** field was completed by me.

Name: ______________________  Date: ____________  AsPredicted URL: ______________________

When the registration is submitted and verified, release the run by sending exactly:

> THE ASPREDICTED PREREGISTRATION HAS BEEN SUBMITTED AND VERIFIED. BEGIN THE FROZEN HELD-OUT
> EVALUATION.

Nothing in the held-out evaluation starts before that sentence arrives with the time-stamped PDF and
the verification URL.
