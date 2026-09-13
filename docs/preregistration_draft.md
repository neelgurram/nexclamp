# NeuroSem preregistration: DRAFT TEMPLATE

> **This is not a preregistration.** It is a template to be completed and frozen by Neel
> before any held-out data are accessed (Milestone 8). Nothing here is registered, frozen
> or hashed.
>
> **How to read the fields.**
>
> - `[NEEL DECISION REQUIRED: ...]` marks a value only the human author may set. These
>   fields are deliberately left blank and must not be filled by an AI assistant.
> - "Current draft proposal" quotes the working documents
>   (`docs/statistical_plan.md`, `docs/protocol_catalog.md`, `docs/mutation_catalog.md`,
>   `docs/model_selection.md`) or `configs/*.yaml`, all of which are **provisional**.
> - A proposal is not a decision.
> - No held-out split exists yet. This template names no held-out model or family.

---

## 0. Administrative information

| Field | Value |
|---|---|
| Title | [NEEL DECISION REQUIRED: title] |
| Author(s) and affiliation | [NEEL DECISION REQUIRED] |
| Registry | [NEEL DECISION REQUIRED: e.g. OSF Registries; M0 evidence notes an OSF "Simulation Studies" template exists, and that registrations are frozen and time-stamped, with embargo up to 4 years] |
| Registration date | [NEEL DECISION REQUIRED] |
| Repository commit frozen for the study | [NEEL DECISION REQUIRED: commit SHA] |
| `configs/FROZEN.lock` SHA-256 | [NEEL DECISION REQUIRED: fill in when created] |
| SHA-256 of `configs/study.yaml`, `features.yaml`, `tolerances.yaml` | [NEEL DECISION REQUIRED: fill in at freeze] |
| SHA-256 of `data/model_manifest.csv`, `data/protocol_manifest.csv`, `data/mutation_manifest.csv`, `data/valid_transforms.csv` | [NEEL DECISION REQUIRED: fill in at freeze] |
| `data/splits/SPLITS.sha256` content | [NEEL DECISION REQUIRED: fill in at freeze] |
| Software environment (Python, pyNeuroML, libNeuroML, eFEL, jNeuroML jar SHA-256, Java) | [NEEL DECISION REQUIRED: fill in from the frozen lock file] |
| Data already seen at registration | [NEEL DECISION REQUIRED: describe discovery and pilot data inspected; state that no held-out data were accessed] |

## 1. Primary hypothesis

**Specification text.** A compact protocol battery selected on discovery models will detect
a higher proportion of admissible non-equivalent mutants on held-out models than a
canonical single-protocol regression test.

- Direction: one-sided in substance (selected > canonical). Tests are reported two-sided.
  [NEEL DECISION REQUIRED: confirm]
- Meaning of "compact": budget k = [NEEL DECISION REQUIRED] protocols. Current provisional
  config value: `selection.budget_k: 4`.
- Meaning of "materially" (minimum effect worth claiming): Delta >= [NEEL DECISION REQUIRED]

## 2. Primary endpoint

**Specification text.** Held-out mutant detection rate under the selected NeuroSem battery
versus canonical regression.

- **Estimand.** Delta = DR_selected - DR_canonical on held-out admissible mutants.
- Population: held-out models only, or also held-out-family mutants on held-out models.
  [NEEL DECISION REQUIRED]
- Rule for "strategy S detects mutant i": [NEEL DECISION REQUIRED: confirm]. Current
  implementation: some protocol of S has the same (protocol, feature) detected at h and at
  h/2 (`detecting_protocols` / `reproducible_keys`). It is used for every strategy, both in
  the discovery detection matrix that selection is trained on and in `evaluate_heldout`.
  Detection at nominal h only is an alternative, but it would need the matrix and
  `heldout.py` to change together, so that selection and evaluation keep one rule.
- Class 6 (silent) uses the same reproducible canonical rule as DR_canonical (DECISIONS D-021), so the silent-survival rate and 1 - DR_canonical agree on the same admissible mutants. [NEEL DECISION REQUIRED: confirm]
- Nominal time step h = [NEEL DECISION REQUIRED] ms. Current provisional: 0.005 ms,
  refinement factors [1, 2, 4].

## 3. Secondary endpoints

For each, state estimator and reporting. Current draft proposals are in
`docs/statistical_plan.md` section 5.

| # | Endpoint | Estimator / reporting | Final |
|---|---|---|---|
| S1 | Detection rate versus cost-matched random batteries | percentile rank, p_rand = (1 + #>=) / (1 + M) | [NEEL DECISION REQUIRED] |
| S2 | Silent-survival rate after canonical testing | #6 / (#5 + #6), overall, per family, per model | [NEEL DECISION REQUIRED] |
| S3 | False-positive rate on valid transformations | x / n per strategy, Clopper-Pearson interval, per transform type | [NEEL DECISION REQUIRED] |
| S4 | Detection rate by mutation family | per strategy, per family, counts | [NEEL DECISION REQUIRED] |
| S5 | Protocols needed for increasing exhaustive coverage | levels [NEEL DECISION REQUIRED: e.g. which percentages] | [NEEL DECISION REQUIRED] |
| S6 | Runtime and simulations per detected mutant | cell-steps and wall time per detection | [NEEL DECISION REQUIRED] |
| S7 | Agent-task success, basic versus NeuroSem validation | descriptive, separate subsection | [NEEL DECISION REQUIRED: whether M9 is run] |

## 4. Inclusion and exclusion rules

### 4.1 Models

- Criteria (specification): traceable public source; license permitting use or handling
  without redistribution; passes current NeuroML validation; deterministic execution;
  practical runtime; interpretable voltage output; meaningful current response; scientific
  provenance; no proprietary dependency.
- Structural-validity oracle: [NEEL DECISION REQUIRED: confirm `jnml -validate`, jNeuroML
  version ____; libNeuroML informational only]
- Operational threshold for "practical runtime": [NEEL DECISION REQUIRED]
- Operational rule for "meaningful current response" (e.g. rheobase status `ok` within
  32 nA): [NEEL DECISION REQUIRED]
- Rule when a reference is spontaneously active or rheobase is `not_found`: [NEEL DECISION
  REQUIRED]. Current provisional: fallback 0.1 nA when spontaneous; `not_found` has no rule
  yet.
- Final list of reference models with source families: [NEEL DECISION REQUIRED]
- What happens if a model fails inclusion checks after the freeze: [NEEL DECISION REQUIRED]

### 4.2 Mutants and transformations

- Mutation families and operators in the primary study: [NEEL DECISION REQUIRED]
- Operator parameters (factors, shifts): [NEEL DECISION REQUIRED]. The draft notes
  `increase_dt` factor 2 can never be admissible under the current rules.
- Sites per operator and mutants per model (sampling rule and seed): [NEEL DECISION
  REQUIRED]
- Whether the stimulus family enters the primary population: [NEEL DECISION REQUIRED]
- Valid transformations and no-change controls included: [NEEL DECISION REQUIRED]
- How valid transformations are verified before inclusion, independently of battery
  outcomes: [NEEL DECISION REQUIRED]
- Single-fault enforcement: every mutant passes `enforce_single_operator`. Compound faults
  are excluded from the primary study.

## 5. Model and mutation splits

- Method of assigning models to discovery or held-out: [NEEL DECISION REQUIRED: e.g. by
  source family, random with seed ____, or stratified by firing regime]
- Treatment of correlated source families (e.g. the four Pospischil cells): [NEEL DECISION
  REQUIRED]
- Number of discovery models: [NEEL DECISION REQUIRED]. Number of held-out models: [NEEL
  DECISION REQUIRED]
- Held-out mutation family: [NEEL DECISION REQUIRED]
- Second lockbox, if any: [NEEL DECISION REQUIRED]
- Split files, stored as `data/splits/discovery_models.txt` and
  `data/splits/heldout/heldout_models.txt`, `heldout_families.txt`. Hashed in
  `data/splits/SPLITS.sha256`, whose content is recorded in section 0.
- Leakage controls: selection code cannot open `data/splits/heldout/` (static and runtime
  tests); every held-out access is logged in `results/heldout_access.log` through
  `HeldoutGate`; held-out failures are not repeatedly inspected and designed around.

## 6. Canonical protocol

- Definition: the simulation shipped with each model (`harness_lems`), analysed as
  `P00_canonical` with features [NEEL DECISION REQUIRED: confirm list; current draft: the 11
  `CANONICAL_FEATURES`] and the same tolerances as other protocols.
- Analysis window rule: first `pulseGenerator` of the reference harness, clipped to the
  simulation length. [NEEL DECISION REQUIRED: confirm]
- Canonical time step: shipped harness step divided by the refinement factor. [NEEL
  DECISION REQUIRED: confirm]
- Whether `P00_canonical` is also a selection candidate: [NEEL DECISION REQUIRED]

## 7. Candidate protocols

- The candidate list is `data/protocol_manifest.csv`, SHA-256 [NEEL DECISION REQUIRED:
  fill at freeze]. Current draft: P01-P10 implemented (including P03 rheobase search);
  P11 chirp and P12 frozen noise not implemented.
- **The manifest alone does not define the protocols.** It holds each template's kind,
  parameters and features, but not the settling time that every stimulus onset and window
  depends on (`numerics.settle_ms`), the time step (`numerics.dt_nominal_ms`,
  `refinement_factors`) or the rheobase search procedure (the `rheobase:` block: step
  duration, initial_hi_nA, grid, rounds, expand, max_hi_nA, spike threshold, fallback). For
  P03 the manifest's `params_json` is only the step duration. The protocol definition is
  therefore the manifest **together with** `configs/study.yaml`, and both SHA-256 hashes in
  section 0 are required.
- Protocol parameters (multiples, durations, settle time): [NEEL DECISION REQUIRED:
  confirm or change `configs/study.yaml`]. Current provisional: settle 300 ms; values in
  `docs/protocol_catalog.md` section 2.
- Protocol cost measure and charging (P03 search cost; canonical): [NEEL DECISION REQUIRED]
- Selection algorithm: greedy maximum coverage on discovery admissible mutants; ties by
  lower cost, then protocol id. Optional cost-sensitive variant: [NEEL DECISION REQUIRED:
  primary or secondary]
- Comparators: canonical alone; random count-matched; random runtime-matched; full
  candidate battery (ceiling).
- Random-set sampling (algorithm, number of draws, seed; enumeration when feasible): [NEEL
  DECISION REQUIRED]. Current provisional: 10000 draws, seed 20260913.

## 8. Features and extraction settings

- Feature list per protocol: frozen as in `data/protocol_manifest.csv` [NEEL DECISION
  REQUIRED: confirm; note the open issue that `ahp_depth` in P09 is not applicable by
  configuration]
- eFEL version and settings (`configs/features.yaml`): [NEEL DECISION REQUIRED: confirm]
- Spike threshold (global -20 mV or per model): [NEEL DECISION REQUIRED]
- Firing-regime rules and thresholds: [NEEL DECISION REQUIRED: confirm]

## 9. Tolerance policy

- **Rule.** tau(m, p, f) = max(abs_floor_f, rel_f x |f_h|, c x |f_h - f_h/2|), computed on
  the reference model at h and h/2; h/4 reported for convergence.
- Constants c, abs_floor_f and rel_f: [NEEL DECISION REQUIRED: values from discovery
  calibration, with justification]. Current provisional: c = 3; floors in
  `configs/tolerances.yaml`.
- Rheobase floor rule (resolution multiple): [NEEL DECISION REQUIRED]
- Exclusion of (model, protocol, feature) whose state or regime flips under refinement:
  [NEEL DECISION REQUIRED: confirm]
- Categorical comparison: exact label match. Definedness mismatch counts as detection:
  [NEEL DECISION REQUIRED: confirm]
- Sensitivity multipliers: [NEEL DECISION REQUIRED]. Current provisional: 0.5, 1, 2, 4.
- **Commitment.** Tolerances are frozen before held-out evaluation and never adjusted after
  held-out results are seen.

## 10. Primary statistical comparison

- **Primary analysis.** Paired counts (a, b, c, d), Delta = (b - c) / N, per-model
  Delta_j, and a cluster-bootstrap 95 % interval resampling base models.
- Bootstrap resamples B, permutations and seed: [NEEL DECISION REQUIRED]. Current values in
  `configs/study.yaml` `analysis`: B = 10000, n_perm = 10000, seed 20260913, ci 0.95
  (`experiments/heldout.py` reads them and calls `paired_comparison`).
- Detection rule for both strategies: reproducible per-protocol detection at h and h/2, as
  in section 2.
- Cluster unit: base model; sensitivity by source family. [NEEL DECISION REQUIRED: confirm]
- Supporting tests: exact McNemar on discordant pairs (assumes independence, violated by
  clustering); whole-cluster sign-flip permutation (minimum p = 2 / 2^K). [NEEL DECISION
  REQUIRED: confirm both are supporting only]
- Decision rule for supporting the primary hypothesis: [NEEL DECISION REQUIRED]. Current
  draft proposal: Delta > 0 with the bootstrap lower bound > 0, and Delta_j >= 0 for every
  held-out model.
- Multiplicity: one primary comparison; secondary endpoints descriptive. [NEEL DECISION
  REQUIRED: confirm]

## 11. Handling of undefined features

- States `defined`, `undefined`, `not_applicable`. Never replaced by zero.
- One defined and one not: detection (definedness mismatch). Both undefined or not
  applicable: no detection. [NEEL DECISION REQUIRED: confirm]
- `min_spikes` per feature as in `configs/features.yaml`. [NEEL DECISION REQUIRED: confirm]
- Rheobase status compared as a definedness state. [NEEL DECISION REQUIRED: confirm]
- Reporting of excluded features: counts per model, protocol and feature.

## 12. Treatment of crashes and equivalent mutants

- Classes 1 (invalid), 2 (non-executable), 3 (unstable): excluded from the detection-rate
  denominator; reported in the validation cascade. [NEEL DECISION REQUIRED: confirm]
- Harness runs but generated probe fails to build: class [NEEL DECISION REQUIRED]
- Timeout limit: [NEEL DECISION REQUIRED]. Current provisional: 7200 s.
- Physical voltage bound for instability: [NEEL DECISION REQUIRED]. Current code: +-10 000 mV (10 V); non-finite output and runs jLEMS aborts with its time-step hint are unstable (DECISIONS D-020, D-021).
- Tool failures: re-run, never classified; maximum retries [NEEL DECISION REQUIRED].
- Class 4 (equivalent within tested domain): excluded from the denominator, not counted as
  misses, reported per operator. [NEEL DECISION REQUIRED: confirm]
- Class 5 and 6 definitions as in `classify`: non-equivalent iff some (protocol, feature)
  is detected at h and at h/2; silent iff non-equivalent through a battery protocol and no canonical (protocol, feature) detected at h and at h/2.
  [NEEL DECISION REQUIRED: confirm]

## 13. Secondary and sensitivity analyses

- Tolerance sensitivity, fixed-population and full-recomputation versions: [NEEL DECISION
  REQUIRED: confirm]
- Source-family clustering sensitivity: [NEEL DECISION REQUIRED: confirm]
- Ablations (e.g. selection without P03, or without canonical as candidate): [NEEL
  DECISION REQUIRED]
- All other analyses are labelled exploratory.

## 14. Sample size and stopping

- Planning bounds (specification): 12-16 reference models (8-10 discovery, 4-6 held-out);
  100-160 admissible mutants; 24-40 valid transformations. These are not a power analysis.
- Target numbers for this study: [NEEL DECISION REQUIRED]
- Basis (pilot runtime estimate, feasibility): [NEEL DECISION REQUIRED]
- Rule if the number of admissible held-out mutants is very small: [NEEL DECISION REQUIRED]
- Pivot or stop criteria (specification): existing validation catches nearly everything;
  most mutations only crash; selection does not beat random on held-out; false positives
  remain high; results depend on one unstable model; findings vanish under refinement.
  [NEEL DECISION REQUIRED: operational thresholds]

## 15. Relationship to the pilot

- What the pilot (Milestone 6) was allowed to inform: operators, features, tolerance
  constants, protocol parameters (discovery and pilot models only).
- Pilot models and whether they may appear in the held-out set: [NEEL DECISION REQUIRED]
- Pilot outcomes known at registration: [NEEL DECISION REQUIRED: summarise honestly]

## 16. Deviations

- Any deviation from this registration is reported with its reason and its effect on
  results, in the manuscript and in a public update. OSF supports appended updates without
  altering the original. [NEEL DECISION REQUIRED: confirm process]

## 17. AI-assisted development and the agent study

- AI use during development is logged in `AI_USE_LOG.md` and disclosed per
  `docs/ai_disclosure.md`.
- The agent study (if run) is a separately identified secondary experiment with frozen
  prompts and hidden evaluators. Its protocol is registered: [NEEL DECISION REQUIRED:
  here or separately]

## 18. Sign-off

- I confirm that no held-out data were accessed before this registration, and that every
  `[NEEL DECISION REQUIRED]` field above was completed by me.
- Name: ____________________ Date: ____________ Signature / registry confirmation:
  ____________
