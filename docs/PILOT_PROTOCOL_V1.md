# Neuraxis development pilot protocol, version 1 (PILOT_PROTOCOL_V1)

| | |
|---|---|
| Project name | **Neuraxis** (the software package keeps the working name `neurosem` until a rename is done, N-10) |
| Protocol fixed | 2026-09-15 00:20 UTC (2026-09-14 local), before any Pilot 2 data were generated |
| Status | **Development / exploratory.** A second development iteration informed by Pilot 1. Not independent confirmation. Never pooled with the confirmatory held-out estimate (DECISIONS D-026). |
| Records | `study_phase = "development_pilot"`, `project_name = "Neuraxis"`, `protocol_version = "PILOT_PROTOCOL_V1"` in every run record, table, report and figure |
| Campaign | `pilot-v2` (role `exploratory_pilot`) |
| Executable settings | `configs/pilot_protocol_v1/` (must agree with section 13; enforced by `tests/unit/test_pilot_protocol_v1.py`) |
| Design rationale | `docs/pilot/pilot_v2_design.md` (approved with modifications, N-14 and N-15) |
| Pre-run hashes | `manifests/pilot_pre_run_sha256.txt`; commit and push record in `manifests/pilot_pre_run_push_record.json` |
| Deviations | `docs/pilot/PILOT_PROTOCOL_V1_DEVIATIONS.md` |

## 1. Purpose

Test whether the Pilot 1 design (protocols, primary feature panel, mutation operators) still works
on four models, two of them from sources not used in Pilot 1. Finalise the later confirmatory design.
All findings are exploratory.

## 2. Included models

| Model | Source (commit-pinned) | License | Set | Shipped harness step, length |
|---|---|---|---|---|
| `pospischil2008_rs` | OpenSourceBrain/PospischilEtAl2008 @ `049081c3` (Pospischil et al. 2008) | MIT | repeated from Pilot 1 | 0.001 ms |
| `pospischil2008_lts` | OpenSourceBrain/PospischilEtAl2008 @ `049081c3` (same source) | MIT | repeated from Pilot 1 | 0.001 ms |
| `wangbuzsaki1996_wb` | OpenSourceBrain/WangBuzsaki1996 @ `c5322844` (Wang and Buzsáki 1996) | MIT | new, independent source | 0.001 ms, 100 ms |
| `nml2_hh_example` | NeuroML/NeuroML2 @ `a5f5dadc` (Hodgkin and Huxley 1952 example cell) | LGPL-3.0 | new, independent source | 0.01 ms, 300 ms |

Snapshots are stored under `models/raw/` with hashes in `data/model_manifest.csv` and the pre-run
manifest. Repeated and new models are reported separately.

## 3. Stimulation protocols

| Role | Protocol |
|---|---|
| Calibration procedure (not a detection protocol) | rheobase search on each **reference** model: 500 ms steps, 12-point bracketing grid, 4 rounds, initial upper 0.5 nA, expansion x4 to at most 32 nA, spike threshold −20 mV. Sets every stimulus amplitude. |
| Comparator (not in the battery) | `P00_canonical`: the model's shipped harness, run unchanged |
| Detection protocols (7) | `P03_rheobase` (variant rheobase measurement); `P04_step_2x` (2x rheobase, 500 ms); `P05_long_step` (1.5x, 2000 ms); `P06_ramp` (0 to 3x over 1000 ms); `P07_hyperpolarizing_step` (−1x, 500 ms); `P08_rebound` (−2x for 500 ms, then 300 ms after release); `P09_short_pulse` (10x for 3 ms, 60 ms window) |

All timing is in whole milliseconds, with a 300 ms settle period before each stimulus. Parameters
are the defaults in `src/neurosem/protocols/definitions.py` at the pre-run commit.

## 4. Features

- **Primary panel (8; decides every classification and pilot criterion):** spike count, first-spike
  latency, last ISI, adaptation index, AP amplitude, AHP depth, steady-state voltage, rheobase.
- **Secondary (10; exploratory; reported, never decisive):** mean frequency, AP half-width, first
  ISI, burst count, firing regime, baseline voltage, voltage deflection, sag ratio, minimum voltage,
  maximum voltage.
- **Assignment:** per protocol as in section 13. eFEL 5.7.34 variants and settings are as in
  `configs/pilot_protocol_v1/features.yaml`.
- **Tolerance:** τ = max(abs floor, rel·|f|, 3·|f(h) − f(h/2)|), calibrated on each reference, with
  constants from `tolerances.yaml`.
- **Refinement exclusion:** a reference entry whose defined state or category changes between h and
  h/2 is excluded.

## 5. Mutation families (strata)

| Stratum | Families and operators (1 site per operator per model) | Planned count |
|---|---|---|
| Primary semantic model mutants | biophysical: scale_conductance, scale_capacitance, shift_reversal, shift_initial_voltage, scale_gate_time_constant; reference: wrong_channel, wrong_compatible_component, omit_include, duplicate_conductance (`wrong_segment_group` excluded) | 32 (RS 9, LTS 9, WB 7, HH 7) |
| Numerical robustness and convergence stress tests (separate; never semantic drift) | increase_dt, recording_resolution, solver_config (reduce_spatial_discretization has no site) | 12 (3 per model) |

- **Identical numerics.** Primary mutants carry no execution overrides and no step, solver or
  discretisation change (checked before simulation).
- **Seed.** Generation seed 20260913. The dry run on 2026-09-14 gave the counts above.

## 6. Valid transformations (controls)

One site per transform operator per model gives 32 controls (8 per model): factor_file,
reorder_independent, xml_formatting, add_comments, rename_identifier, unit_conversion,
numeric_literal_format, explicit_default. Any primary detection on a control is reported.

## 7. Simulator, dependencies, numerics

- **Simulator:** jNeuroML 0.14.0 (jar SHA-256 `45ee565a65a66008a3b41935358d11b7c19cb6b5a67bbec22481d519f53db931`), jLEMS 0.12.0, org.neuroml.export 1.11.0, Eclipse Temurin OpenJDK 21.0.12.1+1.
- **Python:** 3.12.10, with pyNeuroML 1.3.22, libNeuroML 0.6.7, eFEL 5.7.34, numpy 2.5.3, scipy 1.18.1, pandas 3.0.5, matplotlib 3.11.2, lxml 6.1.3, neuromllite 0.6.1. Full pins are in `requirements.lock`.
- **Platform:** Windows 11 (10.0.22631), 12 workers.
- **Time steps:** the battery runs at nominal h = 0.005 ms, with refinement h/2 = 0.0025 ms and h/4 = 0.00125 ms. Canonical harnesses run at their shipped step (section 2) and are refined by the same factors.
  - A detection is non-equivalent only if the same (protocol, feature) is detected at h and h/2.
  - References run at h, h/2 and h/4.
  - Every numerical stress test runs at h, h/2 and h/4.
- **Disclosed difference:** the canonical harness step differs from the battery step (0.001 ms or 0.01 ms vs 0.005 ms). Reference and variant always share settings within a protocol.

## 8. Technical readiness gate (all must pass before data generation)

1. The full test suite passes at the pre-run commit.
2. This protocol agrees with `configs/pilot_protocol_v1/` (`tests/unit/test_pilot_protocol_v1.py`), and `python scripts/pre_run_manifest.py ... --verify` passes.
3. `neurosem validate-models --models <4 models>` reports all four as jnml-valid.
4. `neurosem smoke --models <4 models>` exits 0. This is a plumbing check with scratch output only, not pilot data.
5. The pre-run commit is clean for provenance paths and pushed to the private GitHub remote; the push record is written.
6. The compressed pre-run package exists and its hash is recorded.
7. At least 20 GB of disk is free; the jar hash equals section 7.
8. Campaign `pilot-v2` is unused: no raw or processed data, and not in `results/campaign_registry.json`.

If any item fails, no data are generated. The failure is documented. A fix that changes the design
needs Neel's approval.

## 9. Fixed pilot matrix and planned analyses

**Matrix.**

```bash
NEUROSEM_CONFIG_DIR=configs/pilot_protocol_v1 neurosem pilot --campaign pilot-v2
```

This runs 4 references and 76 variants (32 semantic, 12 numerical, 32 controls). Nothing is added
because time remains.

**Planned analyses** (all exploratory):
1. **Pipeline outputs** (`results/processed/pilot-v2/`): classification with stratum, detections
   (primary and secondary), detection matrices, cascades, tolerances, convergence, false
   positives, the secondary-feature report, `numerical_robustness.csv` and per-variant diagnostics.
2. **Reproducibility check** (`scripts/reproducibility_check.py`). 6 mutants and 2 controls,
   selected by SHA-256 of "20260913:<variant_id>" among executable variants, are re-simulated as
   replicate 1 and compared bit for bit.
3. **Prespecified outputs** (`scripts/pilot_outputs.py`):
   1. flow counts: generated → valid → executable → canonical detected/undetected → battery
      detected/undetected;
   2. results by group: repeated vs new models × model mutants, controls and numerical stress tests;
   3. case lists:
      - canonical passed but a battery protocol detected;
      - canonical detected but the battery missed;
      - controls with any primary-feature detection;
      - secondary features detecting what the primary panel missed;
   4. protocol-by-mutant matrix;
   5. feature-by-mutant matrix;
   6. trace plots for every candidate case;
   7. numerical convergence summaries;
   8. runtime and failure logs;
   9. completed mutant audit sheet, with automated single-change and identical-numerics checks
      (human audit remains pending);
   10. P05 dominance: detections, unique detections, subset of P05, share of the battery union, and
       greedy order, overall and for repeated and new models.
4. **In-sample figures** (`neurosem analyze --campaign pilot-v2`), carrying the designation footer.
5. **Preservation.** Seal, archive and verify the campaign (`scripts/archive_campaign.py`,
   `scripts/verify_archive.py`).

**Definition.** A **candidate hidden-drift case** is a primary semantic mutant with a reproducible
primary-panel detection by at least one battery protocol and no reproducible canonical detection
(class 6).

**Decision guidance** (stated before the data; Neel decides):
- **Technical adequacy:**
  - all four references pass;
  - controls classified non-equivalent ≤ 10% (provisional, N-04);
  - refinement-excluded primary tolerance entries < 25%;
  - the reproducibility check is identical.
- **Continue** toward the freeze: technical adequacy holds, and the semantic stratum contains at
  least one candidate hidden-drift case on a new model.
- **Redesign:** technical adequacy fails, or most new-model mutants are invalid or non-executable.
- **Reframe or stop** (the specification's "do not manufacture drift"): technical adequacy holds but
  there are no candidate hidden-drift cases in either pilot's semantic stratum. The study would then
  be reframed as an evaluation of existing validation adequacy.

## 10. Stopping rule and retry policy

- **Stopping rule.** The pilot ends when the fixed matrix has run once to completion and the
  planned analyses (section 9) are produced. Remaining time is used only for:
  - permitted retries;
  - the reproducibility check;
  - convergence runs already in the plan;
  - integrity verification;
  - audit materials;
  - documentation;
  - backups.
- **Retry policy.** A retry re-invokes the same command at the same commit and configuration, up to
  2 times.
  - **Permitted only after an infrastructure or toolchain abort:** ToolFailure, Java crash, out of
    memory, disk full, the machine sleeping or losing power, or the process being killed.
  - **Completed runs are reused** by content address and never overwritten. If a re-simulated trace
    hash differs, the run stops (ReproducibilityError).
  - **Model-attributable outcomes are results and are never retried:** invalid, build error, runtime
    error, timeout, numerically unstable.
- **During a running batch**, no threshold, exclusion, protocol, feature, mutant or classification
  change is made. Proposed changes go to the deviation log for a later protocol version.
- **Design-changing failures.** Stop the affected analysis, preserve its outputs, document it, and
  ask Neel before rerunning with a modified design.

## 11. Known unresolved decisions

- **N-17:** add an ion-channel kinetics mutation family before the final freeze. It is excluded from
  protocol selection and not part of this pilot.
- **N-10:** the name "Neuraxis" has not had a name-conflict search; the package rename is pending.
- **N-16:** the second independent copy of the Pilot 1 archive is not yet made. OSF is unavailable
  and is now an optional later mirror; this does not block the pilot.
- **N-02, N-09:** held-out split and final model set.
- **N-03, N-04:** final tolerance constants and pilot thresholds.
- **N-05:** code licence.
- **N-06:** canonical metric.
- **N-07:** amplitudes for low-rheobase cells.
- **N-12:** agent-study evaluators.
- **Protocol redundancy:** Pilot 1 detections of P03, P04, P06, P07, P08 and P09 were subsets of
  P05's. To be reassessed before the freeze.
- **Battery scope:** P01, P02 and P10 are not in this battery.
- **Numerics:** the canonical harness and battery steps differ (section 7).

## 12. Reporting rules

Every report states:
- which findings are exploratory (all of Pilot 2) and which are confirmatory (none);
- whether each analysis was specified before its data were inspected (sections 9 and 10: yes);
- the protocol version and Git commit used;
- whether any deviation occurred.

Pilot 1 is reported only in its corrected form:
- 22 real model edits, all detected by the canonical test and 19 by the battery;
- no hidden semantic drift;
- the three previously silent cases were numerical stress cases.

## 13. Executable settings (must equal `configs/pilot_protocol_v1/study.yaml`)

<!-- executable-settings -->
```yaml
study_metadata:
  project_name: Neuraxis
  study_phase: development_pilot
  protocol_version: PILOT_PROTOCOL_V1
  designation: "Development study informed by Pilot 1; exploratory; not independent confirmation; never pooled with the confirmatory held-out estimate"
models: [pospischil2008_rs, pospischil2008_lts, wangbuzsaki1996_wb, nml2_hh_example]
repeated_models: [pospischil2008_rs, pospischil2008_lts]
new_models: [wangbuzsaki1996_wb, nml2_hh_example]
mutation_families: [biophysical, reference, numerical]
exclude_operators: [wrong_segment_group]
mutants_per_operator: 1
transforms_per_operator: 1
seed: 20260913
numerics: {dt_nominal_ms: 0.005, refinement_factors: [1, 2, 4], admissibility_factor: 2, settle_ms: 300, timeout_s: 7200}
rheobase: {step_duration_ms: 500, initial_hi_nA: 0.5, grid: 12, rounds: 4, expand: 4.0, max_hi_nA: 32.0, spike_threshold_mV: -20.0, fallback_rheobase_nA: 0.1}
canonical:
  features: [spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth]
  secondary_features: [baseline_voltage, mean_frequency, ap_half_width, first_isi, firing_regime]
protocols:
  - {protocol_id: P03_rheobase}
  - {protocol_id: P04_step_2x, features: [spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth], secondary_features: [mean_frequency, ap_half_width, first_isi, burst_count, firing_regime]}
  - {protocol_id: P05_long_step, features: [spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth], secondary_features: [mean_frequency, ap_half_width, first_isi, burst_count, firing_regime]}
  - {protocol_id: P06_ramp, features: [spike_count, first_spike_latency], secondary_features: [mean_frequency, firing_regime]}
  - {protocol_id: P07_hyperpolarizing_step, features: [steady_state_voltage, spike_count], secondary_features: [baseline_voltage, voltage_deflection, sag_ratio, minimum_voltage]}
  - {protocol_id: P08_rebound, features: [spike_count, first_spike_latency], secondary_features: [maximum_voltage, firing_regime]}
  - {protocol_id: P09_short_pulse, features: [spike_count, first_spike_latency, ap_amplitude, ahp_depth], secondary_features: [ap_half_width]}
dependencies: {pyNeuroML: 1.3.22, libNeuroML: 0.6.7, efel: 5.7.34, numpy: 2.5.3, scipy: 1.18.1, pandas: 3.0.5, matplotlib: 3.11.2, lxml: 6.1.3, neuromllite: 0.6.1}
```
