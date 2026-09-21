# Statistical analysis plan

*Status: DRAFT, 2026-09-13. No data exist, and nothing here is a result. This plan becomes
binding only when frozen in the preregistration (`docs/PREREGISTRATION_DRAFT.md`). Items
marked **[decision: Neel]** need the human author's decision. Provisional numbers are
quoted from `configs/*.yaml` (status: provisional). Function names refer to the contracts
in `docs/ARCHITECTURE.md` section 3.8.*

## 1. Hypothesis and endpoints

**Research question (Neel, 2026-09-17; two-sided).** How much scientific protection does canonical regression provide for transformed neuronal models, and under what conditions do additional perturbation protocols provide unique information? The study does not depend on finding silent drift: a result showing that strong canonical regression is adequate is a valid, reportable outcome.

**Primary hypothesis (specification).** A compact protocol battery selected on discovery
models will detect a higher proportion of admissible non-equivalent mutants on held-out
models than a canonical single-protocol regression test.

**Primary endpoint (specification).** Held-out mutant detection rate under the selected
NeuroSem battery versus canonical regression.

**Secondary endpoints (specification, all seven).**

| # | Endpoint | Research question |
|---|---|---|
| S1 | Detection rate versus cost-matched random protocol batteries | RQ3 |
| S2 | Silent-survival rate after canonical testing | RQ1 |
| S3 | False-positive rate on valid transformations | controls |
| S4 | Detection rate by mutation family | RQ5, RQ6 |
| S5 | Protocols required to reach increasing levels of exhaustive-battery coverage | RQ2, RQ6 |
| S6 | Runtime and simulations per detected mutant | RQ2 |
| S7 | Agent-task success under basic versus NeuroSem validation | RQ7 |

Further secondary analyses named in the specification are coverage versus number of
protocols, runtime-adjusted coverage, and robustness to stricter and looser tolerances.

RQ4 (generalisation to held-out models) is answered by the primary endpoint itself.

**Pilot data are exploratory (DECISIONS D-026).** The primary comparison, its confidence
interval and hypothesis test, and generalisation to unseen models and to an unseen mutation
family use only the single confirmatory held-out campaign. Pilot iterations are
development data. They are reported descriptively, labelled exploratory, and never pooled
into any confirmatory estimate. This is enforced in code by the campaign registry.

## 2. What is measured on what

**Unit of analysis.** One admissible non-equivalent mutant (class 5 or 6) of a held-out
base model.

**Strategies compared on the same mutants (paired design).**

- **Canonical:** `P00_canonical` alone.
- **Selected:** the battery frozen by greedy selection on discovery data, with budget
  k = 4 in `configs/study.yaml` (provisional) **[decision: Neel]**.
- **Random count-matched and runtime-matched:** see section 6.
- **Exhaustive:** all implemented candidate protocols plus canonical. This is a reference
  point only (see section 3).

**Detection by a strategy.** A single comparison is a detection when |difference| >
tau(model, p, f), or there is a definedness mismatch, or a categorical mismatch. The
time-step rule decides which comparisons count, and it must be the same for every strategy
and for both selection and evaluation.

**Implemented rule: reproducible per-protocol detection (default).** Mutant i is detected
by strategy S when some protocol p in S has some feature f detected **at h and at h/2**
(the same (p, f) key at both levels). This is what the code does today, for every strategy:

- `validation/fingerprint.py`: `detecting_protocols(det_h, det_h2)` returns the protocols
  in `reproducible_keys(det_h, det_h2)`, the intersection of the h and h/2 detection keys.
- `experiments/campaign.py`: the detection-matrix row of an admissible mutant is
  `detecting_protocols(det_h, det_h2)`. Greedy selection on discovery data is trained on
  this matrix.
- `experiments/heldout.py`: the selected battery detects a held-out mutant when
  `selected & detecting_protocols` is non-empty, and canonical detects it when
  `P00_canonical` is in `detecting_protocols`. So the primary endpoint uses the same rule.

Selection and evaluation therefore already agree. The rule also matches the tolerance
design: a difference seen only at h is exactly the kind the refinement term treats as
untrustworthy.

**Alternative (not implemented): detection at nominal h only.** It would count any
detection at h. Adopting it would need both the campaign detection matrix and
`evaluate_heldout` to change, so that selection and evaluation still use one rule.
Choosing it is a **[decision: Neel]**. Mixing rules (for example canonical at h only and
the battery at h and h/2) would bias the comparison and is not allowed.

**Class 6 and DR_canonical use the same canonical rule.** Since DECISIONS D-021, `classify` calls a mutant silent (class 6) only when no canonical (protocol, feature) is detected reproducibly (at h and at h/2), which is exactly the canonical rule of the detection matrix and of DR_canonical. So 1 - DR_canonical among admissible mutants equals the silent-survival rate (S2) on the same mutants. Canonical detections seen at h only are still reported (`canonical_detected_h` without `canonical_detected_reproducible` in `classification.csv`).

**Clusters.** Mutants from one base model share the model's structure and are correlated.
The **cluster is the base model** (`model_id`). Models that share a `source_family` (same
paper and channel files, e.g. the four Pospischil cells) are correlated too. A sensitivity
analysis therefore clusters by `source_family` whenever more than one held-out model
shares a family.

## 3. The denominator

N = the number of held-out mutants classified 5 (non-equivalent) or 6 (silent) using the
exhaustive battery at h and h/2, under the frozen tolerances.

Excluded from N but reported in the validation cascade:

- class 1 structurally invalid;
- class 2 non-executable (build error, runtime error, timeout);
- class 3 numerically unstable;
- class 4 equivalent within the tested domain;
- tool failures, which are re-run and never classified;
- inapplicable operator sites, which are not mutants.

**Consequences of this definition. State them in every report.**

1. The exhaustive battery detects 100 % of N by construction. Its "detection rate" is a
   ceiling, not a finding.
2. A mutant whose change no tested protocol can reveal is class 4 and invisible. All rates
   are conditional on the tested stimulus domain.
3. Rates are conditional on the **operator distribution chosen by us**. They are not
   estimates of how often real-world edits introduce drift.
4. Changing the tolerances changes N (section 7).

## 4. Primary analysis

### 4.1 Paired counts (always reported first)

|  | canonical detects | canonical misses |
|---|---|---|
| **selected detects** | a (both) | b (only selected) |
| **selected misses** | c (only canonical) | d (neither) |

- DR_selected = (a + b) / N and DR_canonical = (a + c) / N, both under the reproducible
  detection rule of section 2. Because class 6 uses the same canonical rule (section 2,
  DECISIONS D-021), DR_canonical = 1 - silent-survival rate on the same admissible mutants.
- **Paired difference** Delta = DR_selected - DR_canonical = (b - c) / N.
- Also reported for every held-out model j: N_j, a_j, b_j, c_j, d_j and Delta_j.
- Counts are also broken down by mutation family, including the held-out family.

### 4.2 Confidence interval: cluster bootstrap

`analysis.bootstrap.cluster_bootstrap_diff(a, b, clusters, n_boot, seed, ci=0.95)`.

1. Take the K held-out base models that have at least one admissible mutant. Report models
   with N_j = 0 separately, because they carry no information about Delta.
2. Draw K models **with replacement**, keeping all of each drawn model's mutants together.
3. Compute Delta* = sum(b_j - c_j) / sum(N_j) over the drawn models (pooled ratio estimator).
4. Repeat B times with a fixed seed. **[decision: Neel: B and seed]** `experiments/heldout.py`
   reads B = 10000, n_perm = 10000 and seed 20260917 from `configs/study.yaml` (`analysis:
   n_boot, n_perm, seed`) and calls `analysis.bootstrap.paired_comparison` with ci = 0.95.
   Changing them is a configuration change that the preregistration freezes.
5. Report the 2.5th and 97.5th percentiles of Delta* as the 95 % interval.

**Assumptions.** Base models are exchangeable draws from a population of models, and
mutants within a model may be arbitrarily correlated.

**Known weakness with few clusters.** With K clusters there are only C(2K-1, K) distinct
resamples: 35 for K = 4, 126 for K = 5 and 462 for K = 6. Percentile intervals from so few
distinct values are coarse and tend to be too narrow. The per-model Delta_j values
therefore must be shown alongside the interval.

### 4.3 Exact McNemar test (supporting)

`analysis.bootstrap.exact_mcnemar(only_a=b, only_b=c)`: a two-sided exact binomial test on
the discordant pairs,

p = min(1, 2 x sum over i = 0..min(b, c) of C(b + c, i) x 0.5^(b + c)), with p = 1 when
b + c = 0.

**Assumption: discordant mutants are independent. Clustering violates this,** so the test
is reported as supporting evidence, not as the primary inference.

For scale: with c = 0, p < 0.05 needs b >= 6 (p = 0.03125), while b = 5 gives p = 0.0625.

### 4.4 Cluster permutation test (supporting)

`analysis.bootstrap.cluster_permutation_test(a, b, clusters, n_perm, seed)`.

- The statistic is T = sum over clusters of (b_j - c_j).
- Under the null, the labels "selected" and "canonical" are exchangeable **within each
  whole cluster**, so the sign of (b_j - c_j) is flipped for entire clusters.
- The two-sided p is the fraction of sign assignments with |T*| >= |T|. It is enumerated
  exactly when 2^K <= n_perm.
- The ARCHITECTURE phrase "sign-flip within clusters" is interpreted as whole-cluster
  flips. Flipping mutants independently inside a cluster would ignore the clustering.

**Limitation.** The smallest attainable p is 2 / 2^K: 0.125 for K = 4, 0.0625 for K = 5 and
0.03125 for K = 6. **With 4 or 5 held-out models this test can never give p < 0.05,
whatever the data.**

### 4.5 Decision rule **[decision: Neel]**

The specification asks for the selected battery to "materially" outperform canonical
testing, which needs a preregistered meaning. This is a proposal only, not a decision:

- Support for the primary hypothesis requires (i) Delta > 0 with the cluster-bootstrap 95 %
  lower bound > 0, and (ii) Delta_j >= 0 for every held-out model.
- The minimum material Delta is **[decision: Neel]**.
- The exact McNemar and permutation p-values are reported but do not decide.
- If (i) holds but (ii) fails, the result is described as not generalising uniformly.

## 5. Secondary analyses

**S1 Random baselines.** See section 6. Reported per baseline: the random detection-rate
distribution (mean, median, 2.5th and 97.5th percentiles), the selected battery's
percentile rank within it, and p_rand = (1 + #{random rate >= selected rate}) / (1 + M)
for M random sets. The exact fraction is used when all sets are enumerated. Evaluated on
the same held-out admissible mutants.

**S2 Silent-survival rate.** #class 6 / (#class 5 + #class 6). Reported overall, per
family and per model, separately for discovery and held-out. Also as counts, with a
cluster-bootstrap interval. Class 6 uses the same reproducible canonical rule as the primary
endpoint (DECISIONS D-021), so a class-5 mutant is always one the canonical protocol detects
reproducibly. For transparency, also report how many mutants were detected by the canonical
protocol at h only (`canonical_detected_h` without `canonical_detected_reproducible`).

**S3 False-positive rate.**

- Fraction of valid transformations with any detection, for each strategy (canonical,
  selected, exhaustive).
- No-change controls reported separately.
- Broken down by transform type and by model.
- Given as x / n with an exact Clopper-Pearson 95 % interval (descriptive; ignores
  clustering), plus per-model counts.
- **Transforms are never removed because the battery flagged them** (see
  `docs/MUTATION_CATALOG.md` section 4). Their semantic equivalence is established
  independently.

**S4 Family-specific detection.** Detection rate for each strategy within each family,
including the held-out family (RQ5), with counts. The stimulus family can only ever be
detected by the canonical protocol (it changes only the harness), so it cannot contribute
silent mutants and is reported separately **[decision: Neel: exclude it from the primary
population, or keep it and report both]**.

**S5 Coverage versus number of protocols.**

- Coverage curve from greedy selection on discovery: the fraction of discovery admissible
  mutants covered after 1, 2, ... protocols.
- The frozen order is then applied to held-out mutants.
- Reported: the number of protocols needed to reach 50 %, 80 %, 90 % and 100 % of
  exhaustive coverage **[decision: Neel: levels]**.
- Compared with the canonical point and with the random-battery curves.

**S6 Runtime-adjusted coverage and cost per detection.**

- For each strategy: total cell-steps and wall-clock time per variant, and cell-steps per
  detected admissible mutant.
- Canonical cost counts at its shipped step. P03 is charged its search cost.
- Also reported: detection rate against a cumulative cell-step curve.

**S7 Agent study (Milestone 9, separate subsection).** Task-level outcomes under basic
validation (schema, execution, canonical) versus the frozen NeuroSem battery. Counts are
small and descriptive, and claims are restricted to the evaluated Claude Code
configuration.

**Multiplicity.** There is one primary comparison. Secondary endpoints are reported as
estimates with intervals and are not used as confirmatory tests, so no multiplicity
correction is claimed. Any analysis not listed here is labelled exploratory.

## 6. Random baselines

**Common rules.**

- The candidate pool is the same as for greedy selection **[decision: Neel: whether
  `P00_canonical` is a candidate]**.
- Random sets are drawn once with a fixed seed: `selection.seed` = 20260917, `random_draws`
  = 10000 (provisional).

**Count-matched** (`random_count_matched(m, k, draws, seed)`).

- k distinct protocols are sampled uniformly without replacement.
- When the number of possible sets is small, **all sets are enumerated** instead of drawn.
  With 10 candidates and k = 4 there are only C(10, 4) = 210 sets, and 10 000 random draws
  would just repeat them.

**Runtime-matched** (`random_runtime_matched(m, cost_budget, draws, seed)`).

- The budget is the selected battery's cost in cell-steps.
- Proposed algorithm: randomly permute the candidates and add each protocol in turn if the
  running total stays within the budget.
- The exact algorithm must be documented by `selection.greedy` and frozen, and the
  distribution of achieved costs is reported.

**Full candidate battery.** Reported as the ceiling (section 3).

## 7. Tolerance sensitivity

Every tau is multiplied by each value in `sensitivity_multipliers` = [0.5, 1, 2, 4]
(`configs/tolerances.yaml`). Two versions are reported:

1. **Fixed population.** Admissibility, classes and N come from multiplier 1. Only strategy
   detections are recomputed. This isolates the effect on the comparison.
2. **Full recomputation.** Admissibility, classes and N are recomputed at each multiplier,
   showing how the denominator itself moves.

The selected battery stays frozen from multiplier 1. Re-running selection per multiplier on
discovery data is exploratory. Reported at each multiplier: Delta with its interval, the
false-positive rate, and the silent-survival rate. A conclusion that holds only at one
multiplier is reported as fragile.

Tolerance constants are justified from discovery and reference runs only, and are **never
adjusted after held-out results are seen**.

## 8. Undefined features, crashes and equivalent mutants

**Undefined and not-applicable features.**

- Each feature value has a state: `defined`, `undefined` or `not_applicable`. Missing
  values are **never replaced by zero**. A spike count of 0 is a real count, not a fill.
- Both values defined and numeric: detection if |difference| > tau.
- Categorical (`firing_regime`): detection if the labels differ (exact match).
- One value defined and the other not: detection by definedness mismatch
  (`definedness_mismatch_is_detection: true`).
- Both undefined or not applicable: no detection.
- A (model, protocol, feature) whose state or regime label changes under refinement of the
  reference is **excluded** from detection for that model. Exclusions are counted and
  reported.
- Rheobase search status (`ok`, `spontaneous`, `not_found`, `error`) is compared like a
  definedness state.

**Crashes (classes 1-3).**

- Excluded from N. Reported in the validation cascade (total, schema-valid, executable,
  canonical survivors, perturbation detections, unresolved survivors) by family and
  operator.
- A mutant that runs in the shipped harness but fails to build in the generated probe
  (possible for `omit_include`) is class 2 under `classify`, which uses the worst run
  status **[decision: Neel: confirm]**.
- `TOOL_FAILURE` runs are repeated and never classified.

**Equivalent mutants (class 4).**

- Excluded from N and **not counted as misses**. Reported per operator with the reason
  where known, e.g. segment-group changes in single-compartment models.
- Sensitivity check: the number of class 4 mutants that would become class 5 with every tau
  halved.
- The label always means "equivalent within the tested domain", never proven equivalent.

## 9. Limitations (frank)

1. **Few held-out models.**
   - The specification plans 4-6 held-out models, and the manifest has 2 included models so
     far.
   - With K = 4-6 clusters the bootstrap interval is coarse, the cluster permutation test
     cannot reach p < 0.05 for K <= 5, and one unusual model can dominate Delta.
   - Every conclusion about generalisation to "unseen models" rests on those few models, and
     their per-model results must be shown.
2. **Correlated models.** Four manifest models share one paper and byte-identical channel
   files. If source families are split across discovery and held-out, the held-out models
   are not truly unseen. If a family is held out whole, K shrinks further.
3. **One held-out mutation family.** RQ5 rests on a single family, whose operators are
   chosen by us. Success on it does not show robustness to fault types in general.
4. **Constructed fault population.** Detection rates describe the chosen operators, sites
   and factors. They do not describe real-world error frequencies, and several operators
   are expected to produce many equivalent or crashing mutants (`docs/MUTATION_CATALOG.md`).
5. **Admissibility defined by the tested battery.** Behaviour changes outside the tested
   stimuli are invisible. "Non-equivalent" and "equivalent" are both relative to this finite
   battery. An empirical semantic certificate is not a proof.
6. **Numerics.** jLEMS integrates with first-order forward Euler. Fragile features (e.g.
   late LTS spikes in `docs/pilot/dt_probe.md`) receive wide refinement tolerances and are
   nearly unable to detect anything, and results could differ under another simulator.
7. **One simulator.** The pilot and planned study are jNeuroML-only. Cross-simulator
   agreement is an optional extension.
8. **Tolerances.** Absolute and relative floors are provisional choices. The sensitivity
   analysis shows their influence but cannot remove it.
9. **No power analysis.** Model and mutant counts are the specification's planning bounds.
   A pilot-based runtime estimate should precede freezing the sample size.
10. **Transform verification.** False-positive estimates are only meaningful if valid
    transforms are verified independently of the battery (section 5, S3).
11. **Secondary AI study.** Small task counts and one agent configuration. No general claim
    about coding agents is possible.

## 10. Decisions required before freezing

1. Budget k and whether `P00_canonical` is a selection candidate.
2. Detection time-step rule: keep the implemented reproducible (h and h/2) rule, or change
   the matrix and `heldout.py` together (section 2). Also whether class 6 should use
   reproducible canonical detection.
3. Material effect size and decision rule (section 4.5).
4. Bootstrap B, permutation n_perm and seed (currently 10000, 10000 and 20260917 in
   `configs/study.yaml` `analysis`).
5. Whether the stimulus family is in the primary population.
6. Coverage levels for S5.
7. Cost charging for P03 and canonical (`docs/PROTOCOL_CATALOG.md` section 6).
8. Runtime-matched sampling algorithm.
9. Class assignment when the harness runs but the probe does not build.
10. Source-family clustering rule and how families are assigned to splits.
11. Final tolerance constants (from discovery calibration) and multipliers.

## 11. Amendment S-01 (2026-09-18): reporting rules fixed before any result is analysed

*Issued after the pre-launch audit (`docs/PILOT2_PRELAUNCH_DECISION.md` section 11), before any
Pilot 2 outcome was aggregated or inspected. It adds reporting obligations and prohibitions. It
changes no threshold, no denominator, no test and no decision rule.*

### 11.1 The models are the generalization units

The unit of analysis stays one admissible non-equivalent mutant, but **the unit of generalization is
the base model**. Every headline number is therefore reported in two forms:

1. the pooled estimate with a model-clustered interval, and
2. the **per-model values that produced it**, listed individually.

With five models (Pilot 2) or four to six (held out), a cluster interval is coarse by construction:
K clusters admit only C(2K-1, K) distinct bootstrap resamples, so the interval is discrete and tends
to be too narrow. That weakness is already stated in section 4.2 and is now a **reporting
requirement**: a pooled interval is never shown without the per-model values beside it.

### 11.2 Cost-matched comparison is required, not optional

A battery of eight protocols that detects more than one canonical harness is not a finding if it
simply spent more compute. Every canonical-versus-battery comparison is therefore accompanied by a
**runtime-matched random battery** (section 6), not only a protocol-count-matched one. Where the
runtime-matched baseline cannot be constructed for a model, that model is reported as such rather
than silently compared on count alone.

### 11.3 Exposed variants are reported twice

Nine Pilot 2 kinetics mutants had their canonical outcome observed before the campaign (amendment
A-01, `docs/PILOT2_LEAKAGE_ASSESSMENT.md`). Every primary result and the branch classification are
computed **over all admissible primary semantic mutants and over the subset carrying no prior
exposure**, and both are reported. If the two disagree, the disagreement is the result and no branch
is claimed.

### 11.4 Attrition is reported in full

Exact denominators at every stage, never a single percentage without its counts: variants attempted,
generated, structurally valid, executable, numerically stable, admissible, non-equivalent, detected
by each strategy. The 40 valid-transformation controls and the 15 numerical robustness stress tests
are reported **in their own tables** and never pooled into the semantic denominator.

### 11.5 Claims that are prohibited regardless of the numbers

- No claim of **universal behavioural equivalence**: absence of a detected difference is evidence
  about the tested protocols and features, not proof that two models behave identically.
- No claim of **broad biological validation**: the models here are single-compartment or somatic
  cells from a handful of papers, and nothing in this study speaks to biological realism.
- No claim that detection coverage is a property of the method alone: every coverage figure is
  **conditional on the empirical reference battery**, the frozen tolerance table and the models
  tested, and is reported with those conditions attached.
- No confirmatory language for any exploratory campaign, including Pilot 1, Pilot 2, the rehearsal
  and the agent study.
- The AI/agent work is **secondary** to the core method and is never the paper's headline claim.

### 11.6 Seeds and tie-breaking

The site-selection seed, the analysis seed, the bootstrap and permutation counts and the
tie-breaking order are fixed in the frozen configuration and reported verbatim with the results.
A re-run that changes a seed is a new analysis and is labelled as one.
