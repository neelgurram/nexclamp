# Pilot 2 protocol (`PILOT2_PROTOCOL`, campaign `pilot2`)

*Written and frozen on 2026-09-17, before the Pilot 2 **campaign** was executed. Executable
settings: `configs/pilot2_frozen.yaml`. Fixed matrix: `manifests/PILOT2_MODELS.csv`,
`manifests/PILOT2_VARIANTS.csv`, `manifests/PILOT2_EXPERIMENT_MATRIX.csv`, hashed in
`manifests/PILOT2_PRE_RUN.sha256`.*

> **Correction (amendment A-01, 2026-09-18).** An earlier version of this line said "before any
> Pilot 2 simulation was executed". That was wrong. Operator-validation simulations of four of the
> five models ran before this document was last edited, and nine of their edits are identical to
> frozen mutants of this matrix. See section 14. The design — models, protocols, families,
> severities, thresholds, exclusions and branch rules — was nonetheless fixed before those
> simulations, at 16:41 on 2026-09-17, and has not changed since.*

> **EXPLORATORY DEVELOPMENT DATA.** Pilot 2 is a second development iteration informed by Pilot 1.
> It is **not** independent confirmation, it is **never** pooled with the confirmatory held-out
> estimate, and no result in it may be reported as a confirmed finding. Every table, figure and run
> record carries `study_phase: development_pilot` and the designation string in the configuration.

Internal study identifier: `neuron_model_behavioral_validation` (permanent, independent of
branding). The public name is undecided (D-050); nothing here may be published under a brand.

This protocol supersedes `docs/PILOT_PROTOCOL_V1.md`, which described a four-model plan that was
never executed (Wang-Buzsaki is excluded by D-051, and the two Pilot 1 models are not repeated).
`configs/pilot_protocol_v1/` is kept unchanged as a record of that superseded plan.

## 1. Research question (two-sided, N-17)

> How much scientific protection does canonical regression provide for transformed neuronal models,
> and under what conditions do additional perturbation protocols provide unique information?

Both answers are publishable. If canonical regression catches essentially everything, that is the
finding. Pilot 2 is designed so that neither outcome is easier to obtain than the other: the
detection thresholds, the exclusions and the branch rules below are fixed before the data exist.

## 2. What Pilot 1 established (and what it did not)

- Pilot 1 (campaign `pilot`, 2 models) produced **22 admissible real model edits; the canonical
  harness detected all 22**; the perturbation battery detected 19. No hidden semantic drift.
- Its canonical comparison was **feature-level only** (11 features, no full-trace comparison and no
  spike-time list): `docs/CANONICAL_BASELINE_AUDIT.md`. Pilot 2 therefore separates level B
  (canonical features) from level C (canonical full trace) and never merges them.
- Three Pilot 1 cases previously described as "silent" were **numerical** (time step, recording
  resolution). Under N-15 they are numerical robustness stress tests, reported in their own stratum,
  and are never called hidden semantic drift.

## 3. Models (five, all new to this study)

Selected from `docs/MODEL_CURATION_REPORT.md` (campaign `curation-v3`: 23 candidates, 13 criteria,
7 eligible, 14 excluded, 2 needing human judgement). Six eligible models had not been used in
Pilot 1, so the selection rule "if six or more new eligible models exist, select four to six"
applies. Selection used provenance, licensing, response type, channel composition, numerical
stability and mutation-operator coverage **only**; no preliminary detection outcome was consulted,
and none exists for these models.

| model_id | cell | source paper | snapshot | licence | response at 2x rheobase | ion channels | operators with a site |
|---|---|---|---|---|---|---|---|
| `acnet2_pyr_soma` | ACnet2 pyramidal soma (Traub 1991 channels) | Beeman 2013 | `NeuroML2@a5f5dadc` | LGPL-3.0 | tonic, sag ratio 0.076 | Na_pyr, Kdr_pyr, Kahp_pyr, Ca_pyr, leak | 10 |
| `migliore2014_mt_soma` | olfactory-bulb mitral-cell soma | Migliore et al. 2014 | `MiglioreEtAl14_OlfactoryBulb3D@eaad1c8f` | MIT | tonic | nax__sh10, kamt, kdrmt, pas | 9 |
| `nml2_hh_example` | single-compartment Hodgkin-Huxley example | Hodgkin & Huxley 1952 | `NeuroML2@a5f5dadc` | LGPL-3.0 | single spike; rebound spike 1; sag ratio 0.346 | naChan, kChan, passiveChan | 8 |
| `osb_hh2_477127614` | HH2 point neuron tuned to Allen specimen 477127614 | OSB MultiscaleISN | `MultiscaleISN@f0783475` | MIT | tonic | Na, Kd, IM, IL, leak | 10 |
| `pospischil2008_fs` | fast-spiking cortical interneuron | Pospischil et al. 2008 | `PospischilEtAl2008@049081c3` | MIT | tonic (fast-spiking) | Na, Kd, leak | 10 |

Five source papers, five distinct channel compositions, two response types (one single-spike /
rebound cell, four tonic cells including one fast-spiking), all deterministic, all numerically
stable under refinement, all with a declared repository licence.

**Recorded licence caveats** (not exclusions; carried into every release check): `acnet2_pyr_soma`
is distributed under the NeuroML2 repository's LGPL-3.0 while the originating publication states no
licence of its own; `osb_hh2_477127614` is MIT in its OSB repository but was tuned to Allen Cell
Types Database data, whose own terms apply to that data rather than to the NeuroML file.
Full details: `docs/LICENSING_MATRIX.md`.

**Eligible but not selected:** `migliore2014_gc_soma` (same source paper as the selected mitral
cell; one model per paper maximises source diversity) and `pospischil2008_rs` (used in Pilot 1).
**Needing human judgement:** `prinz2004_abpd`, `prinz2004_lp` (spontaneously bursting pacemakers;
criterion C08 is open because rheobase is undefined for a spontaneously active cell).
**Excluded:** 14 models, each with its exact failing criterion in the curation report; among them
`wangbuzsaki1996_wb` (C04 only; D-051 excludes it from the primary study and forbids hand-repair).

Held-out isolation: no model, source repository or snapshot used in Pilot 2 may appear in the
confirmatory held-out pool (N-02). The Pilot 2 sources are hereby development sources.

## 4. Protocols

**Calibration procedure, not a detection protocol.** The reference model's rheobase search
(500 ms steps, bracketing grid of 12, 4 rounds, expansion 4.0, spike threshold -20 mV) sets the
amplitude of every current-driven protocol. A spontaneously active reference would use the
fallback 0.1 nA; no selected model is spontaneously active.

**Comparator, not one of the eight.** `P00_canonical` is the simulation shipped with each model
(`source: shipped_harness`). It stands for what a conventional regression test would do.

**Eight detection protocols** (within the prespecified 6-10):

| id | stimulus | why it is necessary |
|---|---|---|
| `P02_weak_step` | 0.5x rheobase, 500 ms | subthreshold probe: passive and leak changes that spiking protocols hide |
| `P03_rheobase` | rheobase search on the variant | excitability threshold as a measurement in its own right |
| `P04_step_2x` | 2x rheobase, 500 ms | the standard suprathreshold response; the canonical-like condition |
| `P05_long_step` | 1.5x rheobase, 2 s | slow adaptation and late failure that 500 ms cannot show |
| `P06_ramp` | slow current ramp | continuous threshold crossing; recruitment dynamics |
| `P07_hyperpolarizing_step` | negative step | input resistance, sag, h-like and leak conductances |
| `P08_rebound` | release from hyperpolarisation | post-inhibitory rebound; de-inactivation kinetics |
| `P09_short_pulse` | brief suprathreshold pulse | single-spike waveform, AHP, fast kinetics |

Feature panels are fixed per protocol in the executable settings: **8 primary features**
(`spike_count`, `first_spike_latency`, `last_isi`, `adaptation_index`, `ap_amplitude`, `ahp_depth`,
`steady_state_voltage`, `rheobase`) decide every primary classification; the remaining catalogued
features are **secondary exploratory** outputs (D-029) that are reported but never change a primary
result. Secondary features that detect something the primary panel missed are reported explicitly
as an exploratory observation.

## 5. Mutations

Six prespecified, scientifically interpretable analysis families in the **primary semantic
stratum**:

| analysis family | operators | severity |
|---|---|---|
| maximal_conductance | `scale_conductance` | mild and strong |
| reversal_potential | `shift_reversal` | mild and strong |
| passive_membrane | `scale_capacitance` | mild and strong |
| gating_time_constant | `scale_gate_time_constant` | mild and strong |
| gating_voltage_dependence (kinetics) | `shift_gate_midpoint`, `scale_gate_slope`, `shift_forward_rate_midpoint`, `shift_channel_vshift` | see 5.2 |
| mechanism_composition | `wrong_channel`, `omit_include`, `duplicate_conductance`, `wrong_compatible_component` | no magnitude |

**Severity is defined by the recorded magnitude alone, never by any result:** multiplicative faults
are *mild* when |ln k| <= ln 1.25 and *strong* when |ln k| >= ln 2; voltage shifts are *mild* at
|d| <= 5 mV and *strong* at |d| >= 10 mV; operators without a magnitude are `not_applicable`.
Sites are drawn with a seed per operator and severity (`selection.seed: 20260917`), so one
operator's choice never depends on another's.

**Prespecified operator exclusions** (fixed before data, with the reason): `wrong_segment_group`
is inert on single-compartment somatic cells (Pilot 1: 4 of 4 equivalent); `shift_initial_voltage`
is erased by the 300 ms settling window by construction (Pilot 1: 3 of 4 equivalent). Neither
operator is removed from the code base, and both remain available for later designs.

### 5.1 Fixed variant matrix

| model | primary semantic mutants | numerical stress tests | valid-transformation controls |
|---|---|---|---|
| `acnet2_pyr_soma` | 20 | 3 | 8 |
| `migliore2014_mt_soma` | 17 | 3 | 8 |
| `nml2_hh_example` | 18 | 3 | 8 |
| `osb_hh2_477127614` | 17 | 3 | 8 |
| `pospischil2008_fs` | 16 | 3 | 8 |
| **total** | **88** | **15** | **40** |

By family: maximal_conductance 20, reversal_potential 20, mechanism_composition 18,
gating_voltage_dependence 12, passive_membrane 10, gating_time_constant 8. By severity: 38 mild,
32 strong, 18 without a magnitude. Every variant is listed with its edit, parameters and tree hash
in `manifests/PILOT2_VARIANTS.csv`; the matrix of simulation units is
`manifests/PILOT2_EXPERIMENT_MATRIX.csv`. **No model, protocol, operator or variant may be added
after execution begins.**

### 5.2 Kinetics: atomic and compound edits, reported separately

The split is made on the recorded edits, not on intent:

- **Atomic**: one attribute of one element. `shift_forward_rate_midpoint` moves only the opening
  rate of one gate, which changes the shapes of both the steady state and the time constant.
  `shift_channel_vshift` is also a single attribute, although its effect is channel-wide: NeuroML
  `channelDensityVShift` passes `vShift` to every gate of that channel that reads it. Scope is
  reported beside atomicity so the two are never confused.
- **Compound**: several attributes that together make one documented change of one gate.
  `shift_gate_midpoint` and `scale_gate_slope` move the alpha rate, the beta rate and any
  steady-state element of one gate together (a rigid shift, or a slope change, of that gate).

Results are reported for atomic and compound edits separately and never pooled into one "kinetics"
number. Operator correctness, the equations changed and the before/after gating curves are in
`docs/KINETICS_OPERATOR_VALIDATION.md`.

Applicability is a property of the model's encoding, not a model failure: a gate whose rates are
custom LEMS ComponentTypes has no core midpoint or slope parameter, so the gate-level operators
report `Inapplicable`. This is the case for every gate of the Pospischil 2008 channels, which is
why `pospischil2008_fs` carries no gating_voltage_dependence variants. Per-model applicability
(number of eligible sites; `-` means the operator does not apply to that model):

| model | shift_gate_midpoint | scale_gate_slope | shift_forward_rate_midpoint | shift_channel_vshift |
|---|---|---|---|---|
| `acnet2_pyr_soma` | 16 (6 validated) | 8 (6) | 8 (6) | not applicable: no `channelDensityVShift` |
| `migliore2014_mt_soma` | 8 (6) | 4 (4) | not applicable: the gate has a steady-state element, which would override a forward-only shift | not applicable |
| `nml2_hh_example` | 12 (6) | 6 (6) | 6 (6) | not applicable |
| `osb_hh2_477127614` | not applicable: gate type `gateHHtauInf` has no core rate or steady state with a midpoint | not applicable (same reason, no `scale`) | not applicable: not a rate gate | 2 (2) |
| `pospischil2008_fs` | not applicable: the Kd rates are custom LEMS types, not core rate types | not applicable (same reason) | not applicable (same reason) | not applicable |

All 48 validated sites passed every check on 2026-09-17: one documented change only, the shipped
simulation file byte-identical, no execution override, still schema-valid, and the model still runs
(`results/audits/kinetics_pilot2/`, with a before/after plot per site). The changes are behaviourally
real, not cosmetic: the largest absolute voltage difference from the reference was 99-118 mV per
model, and spike counts moved, for example, from 7 to 30 (`nml2_hh_example`) and from 28 to 0
(`osb_hh2_477127614`).

Because the prespecified magnitude sets are `MIDPOINT_DELTAS_MV = (-10, -5, 5, 10)`,
`SLOPE_FACTORS = (0.8, 1.25)`, `FORWARD_DELTAS_MV = (-5, 5)` and `VSHIFT_DELTAS_MV = (-5, 5)`, only
`shift_gate_midpoint` offers strong-severity sites; the other three kinetics operators are
mild-only by construction. This is recorded here before the data and is not adjusted afterwards.

## 6. Controls

Eight **valid transformations** per model (`unit_conversion`, `xml_formatting`, `add_comments`,
`numeric_literal_format`, `rename_identifier`, `factor_file`, `reorder_independent`,
`explicit_default`), 40 in total, well above the required five per model. A control that is
classified non-equivalent is a **false positive** of the method and is reported as such.

## 7. Numerical robustness stratum (never semantic drift)

`increase_dt`, `solver_config` and `recording_resolution` variants (3 per model, 15 total) run in a
**separate stratum**. They never enter the primary semantic-drift denominator, they never make a
mutant "silent", and a numerical result is never described as hidden semantic drift (N-15). Primary
semantic mutants and controls run with **exactly the reference's solver and time step**; this is
enforced in code (`strata.check_identical_numerics`, tested). The separate convergence workflow
compares each numerical variant against the reference's own discretisation error at h, h/2 and h/4
and writes `numerical_robustness.csv`.

## 8. Validation levels A-E (B and C never merged)

- **A basic validation**: the variant is structurally valid, executable and numerically stable.
- **B canonical feature regression**: the canonical harness detects it with the primary feature panel
  (what Pilot 1's canonical test did).
- **C canonical full-trace regression**: the canonical harness detects it by full-trace RMSE, spike
  count or spike timing, with thresholds calibrated on the unedited reference at h and h/2
  (tau_rmse = max(0.5 mV, 3 x RMSE(ref_h, ref_h/2)); tau_shift = max(0.5 ms, 3 x max spike shift)).
- **D multi-protocol perturbation testing**: any non-canonical protocol detects it (features or trace).
- **E full candidate battery**: any detection at all, including secondary exploratory features.

Two survivor definitions, kept apart: a **feature-level canonical survivor** passes B but is
detected at D; a **full-trace canonical survivor** passes both B and C and is still detected at D.
Every apparent canonical survivor is re-checked at h/4; a survivor that does not reproduce at h/4 is
reported as **unconfirmed** and never counted as hidden drift.

## 9. Thresholds, exclusions, retries, stopping rules and analysis definitions

*All fixed before execution.*

- **Detection (features)**: tau(m, p, f) = max(abs_floor_f, rel_f x |f_h|, 3 x |f_h - f_h/2|) from
  `configs/tolerances.yaml`, calibrated on the unedited reference model. A detection counts only if
  it **reproduces at h and h/2**.
- **Detection (traces)**: section 8, reproducible at h and h/2, same rule.
- **Categorical features**: exact match; a defined/undefined mismatch is a detection.
- **Refinement exclusion**: a (protocol, feature) entry whose state or category changes between h
  and h/2 is excluded from tolerance calibration and **recorded**, never silently dropped. A
  protocol whose reference spike count changes between h and h/2 is excluded from trace regression
  and recorded.
- **Retries**: a unit that ends in `TOOL_FAILURE` (Java or jNeuroML infrastructure failure, not the
  model) is preserved under `_tool_failures/` and may be retried by re-invoking the campaign, at
  most twice per unit; the attempts are kept. `INVALID`, `BUILD_ERROR` and `RUNTIME_ERROR` are
  **results about the variant** and are never retried away.
- **No mid-run changes**: no threshold, exclusion, tolerance, protocol, operator or model may be
  changed once execution begins. Any deviation forced by an error stops the run and is written to
  `docs/DEVIATION_LOG.md` before anything is re-run.
- **Stopping rules**: stop and report, rather than continue, if (a) a reference model fails to
  produce a fingerprint at h, h/2 or h/4; (b) determinism fails for any reference (re-executed
  battery traces not bitwise identical); (c) more than 25% of a model's (protocol, feature)
  tolerance entries are refinement-excluded; (d) the control false-positive rate exceeds 10%; or
  (e) any write-once raw result would be overwritten.
- **Data integrity**: campaign `pilot2` is registered with role `exploratory_pilot`; raw results are
  write-once and content-addressed; each run records its run id, execution id, timestamp,
  configuration hash, model tree hash, cache key, software commit, simulator and Java build. Pilot 1
  raw data is untouched and its hashes are verified before the run.

## 10. Prespecified outputs

1. Per-model, per-family, per-severity detection tables at every validation level A-E.
2. Canonical-versus-battery comparison, with B and C reported separately.
3. Feature-level and full-trace canonical survivors, each with its h/4 confirmation status.
4. **Unique protocol contribution**: for each protocol, the variants that only it detected.
5. False-positive table for the 40 valid-transformation controls.
6. Numerical robustness and convergence results, in their own stratum and their own tables.
7. Kinetics results split into atomic and compound edits, with per-model applicability.
8. Secondary exploratory feature report, including anything the primary panel missed.
9. Uncertain or unclassifiable cases, listed explicitly rather than forced into a class.
10. Human audit sheet of at least 20 mutants, and a diagnostic for every detection.

These are produced by `scripts/pilot_v2_outputs.py` into
`results/processed/pilot2/pilot_v2_outputs/`, one file per item: `01_validation_level_counts.csv`,
`02_feature_level_canonical_survivors.csv`, `03_full_trace_canonical_survivors.csv`,
`04_multi_protocol_detections.csv`, `05_detection_by_model.csv`, `06_detection_by_family.csv`,
`06_detection_by_family_and_severity.csv`, `07_valid_transformation_false_positives.csv`,
`08_convergence.csv`, `08_survivor_refinement_checks.csv`, `09_run_status_counts.csv`,
`09_runtime.csv`, `09_failed_runs.csv`, `10_detection_matrix_complete.csv`,
`11_random_audit_cases.csv`, `12_canonical_survival_cases.csv`,
`13_failed_valid_transformations.csv`, `14_unique_protocol_contribution.csv`,
`15_kinetics_atomic_vs_compound.csv`, `16_uncertain_cases.csv` and `summary.json` (branch
classification), plus `numerical_robustness.csv` for the separate stratum.

## 11. Branch classification (prespecified; A is never forced)

Precedence **D > A > B > C**.

- **Branch D - inconclusive** if any of: control false-positive rate > 0.10; more than half of the
  apparent survivors fail their h/4 confirmation; or refinement-excluded entries >= 25%.
- **Branch A - hidden drift exists** if at least 2 confirmed **full-trace** canonical survivors occur
  across at least 2 different models.
- **Branch B - canonical regression is feature-limited** if at least 2 confirmed feature-level
  canonical survivors are caught by full-trace canonical regression (level C).
- **Branch C - canonical regression is adequate** if canonical regression (B or C) detects at least
  95% of admissible primary semantic mutants.

If none of A, B or C is met and D does not apply, the result is reported as **no branch met**, with
the numbers. The rules are not re-tuned after the data are seen.

## 12. After Pilot 2: stop

When the outputs above exist, the study **stops for review**. No scope expansion, no held-out
access, no preregistration submission, no result claims, no threshold tuning, and no rename or
publication step until Neel decides.

## 13. Environment

jNeuroML 0.14.0 (jLEMS 0.12.0), Temurin JDK 21.0.12.1+1, Python 3.12.10, and the pinned packages in
`requirements.lock`. The environment files, the analysis code, the model snapshots, this protocol
and the configuration are all hashed in `manifests/PILOT2_PRE_RUN.sha256` before the run.

<!-- executable-settings -->
```yaml
study_metadata:
  study_id: neuron_model_behavioral_validation
  project_name: Neuraxis
  study_phase: development_pilot
  protocol_version: PILOT2_PROTOCOL
  designation: "Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate"

campaign: pilot2
seed: 20260917

models: [acnet2_pyr_soma, migliore2014_mt_soma, nml2_hh_example, osb_hh2_477127614, pospischil2008_fs]
new_models: [acnet2_pyr_soma, migliore2014_mt_soma, nml2_hh_example, osb_hh2_477127614, pospischil2008_fs]
repeated_models: []

mutation_families: [biophysical, reference, kinetics, numerical]
exclude_operators: [wrong_segment_group, shift_initial_voltage]
mutants_per_operator: 1
transforms_per_operator: 1
severity_levels: [mild, strong]
sites_per_severity:
  default: 1
  scale_conductance: 2
  shift_reversal: 2
sites_without_severity: 1

numerics:
  dt_nominal_ms: 0.005
  refinement_factors: [1, 2, 4]
  admissibility_factor: 2
  settle_ms: 300
  timeout_s: 7200
  java_max_memory: 2G

rheobase:
  step_duration_ms: 500
  initial_hi_nA: 0.5
  grid: 12
  rounds: 4
  expand: 4.0
  max_hi_nA: 32.0
  spike_threshold_mV: -20.0
  fallback_rheobase_nA: 0.1

canonical:
  protocol_id: P00_canonical
  source: shipped_harness
  features: [spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth]
  secondary_features: [baseline_voltage, mean_frequency, ap_half_width, first_isi, firing_regime]

validation_levels:
  enabled: true

protocols:
  - protocol_id: P02_weak_step
    features: [steady_state_voltage, spike_count]
    secondary_features: [baseline_voltage, voltage_deflection]
  - protocol_id: P03_rheobase
  - protocol_id: P04_step_2x
    features: [spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth]
    secondary_features: [mean_frequency, ap_half_width, first_isi, burst_count, firing_regime]
  - protocol_id: P05_long_step
    features: [spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth]
    secondary_features: [mean_frequency, ap_half_width, first_isi, burst_count, firing_regime]
  - protocol_id: P06_ramp
    features: [spike_count, first_spike_latency]
    secondary_features: [mean_frequency, firing_regime]
  - protocol_id: P07_hyperpolarizing_step
    features: [steady_state_voltage, spike_count]
    secondary_features: [baseline_voltage, voltage_deflection, sag_ratio, minimum_voltage]
  - protocol_id: P08_rebound
    features: [spike_count, first_spike_latency]
    secondary_features: [maximum_voltage, firing_regime]
  - protocol_id: P09_short_pulse
    features: [spike_count, first_spike_latency, ap_amplitude, ahp_depth]
    secondary_features: [ap_half_width]

branch_rules:
  control_false_positive_rate_max: 0.10
  unconfirmed_survivor_fraction_max: 0.50
  refinement_excluded_fraction_max: 0.25
  hidden_drift_min_confirmed_full_trace_survivors: 2
  hidden_drift_min_models: 2
  feature_insufficiency_min_cases: 2
  canonical_adequacy_min_detection: 0.95
  audit_sample_size: 20

dependencies:
  pyNeuroML: 1.3.22
  libNeuroML: 0.6.7
  efel: 5.7.34
  numpy: 2.5.3
  scipy: 1.18.1
  pandas: 3.0.5
  matplotlib: 3.11.2
  lxml: 6.1.3
  PyYAML: 6.0.3
  pytest: 9.1.1
  ruff: 0.16.7
  mypy: 2.3.1
```

## 14. Amendment A-01 (2026-09-18): pre-campaign outcome exposure

*Numbered, timestamped amendment issued after Neel's pre-launch audit. It changes no threshold, no
denominator, no variant and no rule. It corrects a false statement and adds a reporting obligation.
Evidence: `docs/PILOT2_LEAKAGE_ASSESSMENT.md`, `docs/PILOT2_PRELAUNCH_DECISION.md`,
`results/audits/PILOT2_KINETICS_OVERLAP_AUDIT.csv`.*

### 14.1 What happened

Kinetics operator validation was run on the five Pilot 2 models on 2026-09-17 (21:14-21:19 UTC),
48 sites, each simulating the model's **canonical shipped harness** before and after the edit. The
spike counts and maximum voltage differences were printed, read by the assistant and reported to
Neel. One minute later this protocol's section 5.2 was edited with the resulting applicability
table, and its atomic/compound definition was corrected because the recorded output contradicted
the earlier text.

Audit classification: **L5** (the campaign subsequently began before the audit) with an **L4**
component (outcome exposure with possible design influence).

### 14.2 The nine exposed variants

Nine frozen primary semantic mutants are the *same edit* (model, operator, channel, gate, magnitude)
as a validated site whose canonical-harness outcome is known:

| model | operator | severity | canonical spikes before -> after |
|---|---|---|---|
| `acnet2_pyr_soma` | `shift_gate_midpoint` | mild | 8 -> 10 |
| `acnet2_pyr_soma` | `scale_gate_slope` | mild | 8 -> 7 |
| `acnet2_pyr_soma` | `shift_forward_rate_midpoint` | mild | 8 -> 8 |
| `migliore2014_mt_soma` | `shift_gate_midpoint` | mild | 1 -> 1 |
| `migliore2014_mt_soma` | `scale_gate_slope` | mild | 1 -> 2 |
| `nml2_hh_example` | `shift_gate_midpoint` | mild | 7 -> 0 |
| `nml2_hh_example` | `scale_gate_slope` | mild | 7 -> 19 |
| `nml2_hh_example` | `shift_forward_rate_midpoint` | mild | 7 -> 1 |
| `osb_hh2_477127614` | `shift_channel_vshift` | mild | 28 -> 41 |

That is 9 of 88 primary semantic mutants (10.2%) and 9 of 12 kinetics mutants. The 76 non-kinetics
mutants, the 40 controls and the 15 numerical stress tests carry no exposure, and
`pospischil2008_fs` carries none at all.

### 14.3 Binding rules added by this amendment

1. **No variant is removed or replaced.** The frozen matrix is unchanged. Exposed variants are not
   dropped, because dropping them would be a selection made with their outcomes in hand.
2. **Every primary result is reported twice**: over all admissible primary semantic mutants, and
   over the 79 that carry no prior outcome exposure. Both numbers appear in the outputs; neither is
   presented alone.
3. **Branch classification is computed on both sets** and both are reported. If they disagree, the
   disagreement is the result, and no branch is claimed.
4. **Pilot 2 is exploratory development data.** It is never described as confirmatory, untouched,
   independent confirmation, or held out. It is never pooled with the confirmatory estimate.
5. **These five models and their five source repositories are permanently development sources** and
   can never serve as held-out confirmatory models.
6. **Resumption rule.** The campaign may continue on the frozen matrix. Because runs are
   content-addressed, re-invoking the campaign reuses completed runs and re-derives nothing; no
   variant is re-selected, and no threshold changes.

### 14.4 What this amendment does not do

It does not change the tolerance rule, the RMSE calibration, the branch thresholds, the protocol
battery, the severity bands, the seed, or the set of variants. Options for the RMSE limitation are
presented for Neel's decision in `docs/PILOT2_PRELAUNCH_DECISION.md` section 10; none is applied.
