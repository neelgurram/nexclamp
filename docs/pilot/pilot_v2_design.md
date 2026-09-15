# Pilot 2 (`pilot-v2`): design

*Status: APPROVED WITH MODIFICATIONS by Neel (N-14, N-15); revised as requested; **not run**.
Awaiting Neel's go-ahead to execute. Configuration: `configs/pilot_protocol_v1/study.yaml`.*

*Pilot 2 is a **second development iteration**. Its design was informed by Pilot 1, so it is not
independent confirmation. Its purpose is to test whether Pilot 1's choices hold up on new cell
types and to finalise the later confirmatory design. Its data are exploratory and never enter the
confirmatory held-out estimate (D-026).*

## In plain English

- **Think of Pilot 1 as practising on two closely related patients.** Pilot 2 practises on four,
  two of them from different families. If the tools we picked still work, we can lock them in for
  the real test.
- **There are four kinds of thing in the design, kept apart:**
  - calibration: finding the right stimulus strength;
  - the tests themselves;
  - the eight measurements that decide results;
  - extra measurements we look at but never use to decide.
- **Step-size changes are no longer counted as hidden model changes.** They are studied on their
  own.
- **What Pilot 1 actually showed:** once step-size changes are set aside, the standard test caught
  every real model change. Pilot 2 asks whether that is still true on cells from other sources.

## 1. Rheobase: calibration procedure *and* a detection measurement

There are two separate uses of the same search (500 ms steps, bracketing grid; `configs/study.yaml`
`rheobase`):

| Use | On which model | Role | Counted as a detection protocol? |
|---|---|---|---|
| Rheobase search on the **reference** | reference only, once per model | **Calibration procedure.** Sets the amplitude of P04-P09 (for example P04 = 2 x rheobase), so every variant of a model receives exactly the same stimulus. | No |
| Rheobase search on each **variant** (`P03_rheobase`) | every variant | **Detection measurement.** Its result, the variant's rheobase, is compared with the reference's under the tolerance rule. | Yes |

The variant's own rheobase never rescales its stimuli. The amplitudes stay those calibrated on the
reference.

## 2. The canonical protocol is additional, not one of P03-P09

`P00_canonical` is the simulation shipped with each model, run unchanged. It is the **comparator**,
the conventional regression test NeuroSem is compared against. It is not part of the battery and not
counted among the seven.

## 3. Exact protocol count

| Category | Protocols | Count |
|---|---|---|
| Calibration procedure | reference rheobase search | 1 (not a detection protocol) |
| Comparator | P00 canonical | 1 (not in the battery) |
| **Distinct model-evaluation (detection) protocols** | P03 variant rheobase, P04, P05, P06, P07, P08, P09 | **7** |
| of which current-clamp stimulus waveforms | P04 step 2x, P05 long step 1.5x, P06 ramp, P07 hyperpolarising step, P08 hyperpolarise-and-release, P09 short pulse | 6 |
| of which derived threshold measurement | P03 variant rheobase | 1 |

**Duplicates.** None of the seven is a duplicate *stimulus*. P04 and P05 are both depolarising
steps, but they differ in amplitude (2x vs 1.5x rheobase) and length (0.5 s vs 2 s). In Pilot 1's
*detections*, however, several were fully redundant (`detection_matrix.csv`, 28 admissible mutants
including numerical):
- P04's detections were a subset of P05's;
- so were those of P06, P07, P08, P09 and P03;
- on the 22 semantic mutants, P05 alone detected 19.

So the honest count is 7 distinct protocols, of which Pilot 1 could show only P05 as
non-redundant. Pilot 2 keeps the other six because Pilot 1's two correlated cells cannot tell us
whether they are redundant in general (section 4).

## 4. Why each selected protocol remains necessary

"Necessary" here means needed to test a mechanism that Pilot 1 could not evaluate, not proven
useful. Any protocol that stays fully redundant on Pilot 2's four cells is a candidate for removal
from the confirmatory battery, and that decision is made before the freeze.

| Protocol | What it probes | Why it stays for Pilot 2 |
|---|---|---|
| P03 variant rheobase | excitability threshold | the only direct threshold measure; detected 8 Pilot 1 mutants; the comparison is independent of any fixed amplitude |
| P04 step 2x, 0.5 s | strong-drive firing and spike shape | detections were a subset of P05's on two similar cells; kept to test whether strong-drive responses separate from moderate drive on the fast-spiking WB and minimal HH cells |
| P05 long step 1.5x, 2 s | sustained firing, adaptation | the most detecting protocol in Pilot 1 (24 of 28) |
| P06 ramp 0 to 3x, 1 s | spike onset under slowly rising drive, accommodation | the only protocol where the input changes continuously; sensitive to sodium inactivation and threshold dynamics that steps can hide |
| P07 hyperpolarising step | passive and subthreshold properties, Ih sag | the only subthreshold protocol left after dropping P01 and P02; nothing else measures below-threshold behaviour |
| P08 hyperpolarise and release | rebound (T-type, Ih) | the only rebound test; the LTS T-current was barely exercised in Pilot 1, so its low count reflects weak drive, not proven redundancy |
| P09 short 3 ms pulse | single-spike shape and AHP without sustained drive | isolates spike generation from adaptation; the cheapest protocol (0.1 M cell-steps) |

Not carried forward: P01 baseline, P02 weak step and P10 paired pulses. Pilot 1 recorded them and
their data remain available. Adding them back costs about 33% more battery simulation and is a
decision for Neel if wanted.

## 5. Models: Pilot 1 versus new

| Model | Source | In Pilot 1? | In Pilot 2? | Status |
|---|---|---|---|---|
| `pospischil2008_rs`, regular-spiking | Pospischil et al. 2008 | yes | yes | **repeated** |
| `pospischil2008_lts`, low-threshold spiking | Pospischil et al. 2008 (same source as RS) | yes | yes | **repeated** |
| `wangbuzsaki1996_wb`, fast-spiking interneuron | Wang and Buzsáki 1996 | no | yes | **new**, independent source |
| `nml2_hh_example`, Hodgkin-Huxley example cell | NeuroML2 examples | no | yes | **new**, independent source (LGPL-3.0, L-01) |

The two new models are the real test of generalisation. Results on RS and LTS repeat cells whose
data informed the design, so they are reported separately from the two new models. The Prinz,
Smith, Migliore and Maex candidates stay unseen, so they remain available for the held-out split
(N-02, N-09).

## 6. Feature policy

| Category | Features | Role |
|---|---|---|
| **Primary prespecified panel** (8) | spike count, first-spike latency, last ISI, adaptation index, AP amplitude, AHP depth, steady-state voltage, rheobase | The only features that decide any Pilot 2 classification, criterion or success result |
| **Secondary exploratory** (10) | mean frequency, AP half-width, first ISI, burst count, firing regime, baseline voltage, voltage deflection, sag ratio, minimum voltage, maximum voltage | Extracted from the same traces, reported, never used to change a primary result |

Per protocol, the secondary features are exactly the rest of that protocol's Pilot 1 feature
list, so together the two panels reproduce all 18 Pilot 1 features:

| Protocol | Primary | Secondary |
|---|---|---|
| P00 canonical | spike count, latency, last ISI, adaptation, AP amplitude, AHP | baseline voltage, mean frequency, AP half-width, first ISI, firing regime |
| P03 | rheobase | none |
| P04, P05 | spike count, latency, last ISI, adaptation, AP amplitude, AHP | mean frequency, AP half-width, first ISI, burst count, firing regime |
| P06 | spike count, latency | mean frequency, firing regime |
| P07 | steady-state voltage, spike count | baseline voltage, voltage deflection, sag ratio, minimum voltage |
| P08 | spike count, latency | maximum voltage, firing regime |
| P09 | spike count, latency, AP amplitude, AHP | AP half-width |

Rules, enforced in code (`experiments/strata.py`, `campaign.py`, `pilot.py`):
1. **Classification.** Detections are split by panel before classification. The class, the
   detection matrix, the silent list and all three pilot criteria use primary detections only. The
   refinement-exclusion criterion also counts primary tolerance entries only.
2. **Reporting.** Secondary detections go to `detections_secondary.csv` and
   `secondary_feature_report.csv`. The report states how many mutants the primary panel classed as
   equivalent but a secondary feature detected reproducibly. It also flags canonical detections that
   come only from secondary features.
3. **Cost.** Extraction reuses the same traces, so no extra simulation. The one added cost: the
   h/2 run also happens when only a secondary feature detects at h, so that feature's
   reproducibility can be reported. The primary class still ignores that run.
4. **No permanent removal.** No feature is removed because Pilot 1 found it unhelpful. The final
   confirmatory panel is proposed only after Pilot 2, from both pilots, and frozen before held-out
   evaluation.
5. **Generalisation check.** Pilot 2 reports, separately for repeated and new models, whether the
   primary panel still covers what the full 18 detect.

## 7. Mutations: primary semantic corpus and separate numerical experiment

From a generation-only dry run (no simulation) with seed 20260913 and one site per operator.

**Primary semantic corpus: 32 mutants.**
- biophysical (5 operators): scale_conductance, scale_capacitance, shift_reversal,
  shift_initial_voltage, scale_gate_time_constant;
- reference (4 operators): wrong_channel, wrong_compatible_component, omit_include,
  duplicate_conductance.

| Model | Biophysical | Reference | Total |
|---|---|---|---|
| RS | 5 | 4 | 9 |
| LTS | 5 | 4 | 9 |
| WB | 5 | 2 | 7 |
| HH | 5 | 2 | 7 |

WB and HH have no included files, so `omit_include` and `wrong_compatible_component` have no site.

Excluded: `wrong_segment_group` (inert on single-compartment cells; 4 of 4 equivalent in Pilot 1).
It is kept in the code and can be re-enabled.

**Numerical robustness and convergence stress tests: 12 mutants**, 3 per model (increase_dt,
recording_resolution, solver_config). `reduce_spatial_discretization` has no site on
single-compartment cells.
- They are never in the primary denominator (`primary_admissible`, tested).
- Every numerical stress test runs at h, h/2 and h/4. Its deviations are compared with the
  reference's own discretisation error and observed order (`numerical_robustness.csv`).
- Results are labelled numerical sensitivity, never semantic drift.

**Controls: 32** valid transformations and no-change controls (8 per model).

**Identical numerics.** Every primary semantic mutant and control is checked before simulation:
no execution overrides, and no change to step, solver method or discretisation
(`check_identical_numerics`). The reference and the variant therefore always run each protocol
with identical settings.

A remaining difference, disclosed: the canonical harness runs at its shipped step (0.001 ms for
RS and LTS) while the battery runs at 0.005 ms. This does not affect any reference-versus-variant
comparison, because both run identically within each protocol. It does mean the canonical run is
numerically more accurate than the battery.

**Families (note for Neel).** The primary semantic corpus has **2 families**, biophysical and
reference. Numerical is now separate and stimulus mutations edit only the test harness. This
matters later: the confirmatory study must test generalisation to an *unseen* semantic mutation
family. With two, holding one out leaves one for discovery. A third semantic family is needed
before the freeze, or the held-out-family aim must be revised.

## 8. What Pilot 2 can and cannot establish

**Can:**
- whether behaviour-changing model edits survive the canonical test on cells from independent
  sources (WB, HH), reported separately for repeated and new models;
- whether Pilot 1's protocols and the 8-feature primary panel still capture what the full 18
  features detect on new cell types;
- the false-positive behaviour of 32 controls;
- how the numerical stress tests behave against measured convergence;
- runtimes per model, for planning the confirmatory study.

**Cannot:**
- confirm anything: its design used Pilot 1 data, so it is a development iteration;
- give a detection-rate comparison, confidence interval or hypothesis test for the paper's primary
  claim, which come only from the frozen held-out study;
- show generalisation to unseen models or an unseen mutation family: RS and LTS are repeated, and
  every family was seen;
- say much about rates: with 32 semantic mutants on 4 cells, and 2 from one source, any rate has a
  wide interval, and the analysis flags it as unreliable.

## 9. Runtime estimate

Pilot 1 took 1 h 44 min wall time for 68 variants on 2 models (12 workers).

For Pilot 2 (76 variants on 4 models):
- the battery costs about 75% of Pilot 1's per variant;
- secondary features add extraction time only;
- every numerical stress test runs h, h/2 and h/4 (about 7 times one nominal run each).

The WB and HH harness costs are not yet measured. Expect roughly **3-4 h**. The real figure will
be recorded.

## 10. How it will run (only after Neel's go-ahead)

```bash
NEUROSEM_CONFIG_DIR=configs/pilot_protocol_v1 .venv/Scripts/python -m neurosem.cli pilot --campaign pilot-v2
```

It must run on a clean commit. When finished, it is sealed with `scripts/archive_campaign.py`,
and archived and verified like Pilot 1.
