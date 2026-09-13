# Pilot iteration 2 (`pilot-v2`): design proposal

*Status: DRAFT for Neel's approval (DECISIONS N-14, N-15). Not run. Exploratory/developmental
(D-026). Draft configuration: `configs/pilot_v2_draft/`. The choices below use iteration-1
data, which the pilot phase is allowed to do; they are recorded so the manuscript can report
them.*

## In plain English

- Iteration 1 used more tests and more measurements than the pilot bounds allow. It also only
  looked at two closely related cells, whose own standard test was already strong.
- Iteration 2 stays inside the bounds and adds two cells from different sources.
- It keeps the protocols that did the work in iteration 1, plus the ones that probe mechanisms
  iteration 1 barely exercised (hyperpolarisation and rebound).
- It removes the time-step mutation that made "hidden" changes appear only because two tests
  started from different step sizes.

## 1. Models (4; bound 2-6)

| model | source | why |
|---|---|---|
| `pospischil2008_rs` | Pospischil 2008 | continuity with iteration 1 |
| `pospischil2008_lts` | Pospischil 2008 | continuity; T-current cell |
| `wangbuzsaki1996_wb` | Wang and Buzsaki 1996 | independent source; fast-spiking interneuron |
| `nml2_hh_example` | NeuroML2 examples | independent source; minimal HH cell with a simple shipped harness (LGPL-3.0, L-01) |

All four are already in `data/model_manifest.csv` with commit-pinned, hash-verified snapshots.
The Prinz, Smith, Migliore and Maex candidates stay unseen, so they remain available for the
held-out split (N-02, N-09). WB and HH have not yet passed the reference stage in a campaign; a
failure there is recorded, not worked around.

## 2. Protocols (7; bound 4-8)

Evidence from iteration 1 (`results/processed/pilot/detection_matrix.csv`, 28 admissible mutants):

| protocol | detected | detected by no other protocol | iteration 2 |
|---|---|---|---|
| P00 canonical | 25 | 4 | comparator (not counted) |
| P05 long step | 24 | 0 | keep |
| P04 step 2x | 21 | 0 | keep |
| P06 ramp | 10 | 0 | keep |
| P09 short pulse | 8 | 0 | keep |
| P03 rheobase | 8 | 0 | keep (needed to scale every protocol) |
| P02 weak step | 4 | 0 | drop |
| P07 hyperpolarising step | 3 | 0 | keep: only subthreshold/Ih probe |
| P10 paired pulses | 3 | 0 | drop |
| P01 baseline | 2 | 0 | drop (both detections were reference crashes) |
| P08 rebound | 2 | 0 | keep: only T-current/rebound probe |

No battery protocol detected anything alone in iteration 1. P07 and P08 are kept on mechanistic
grounds, not detection counts, because counts from two cells with weak rebound responses would
bias the battery toward protocols that resemble the canonical step.

## 3. Features (8; bound 3-8)

Reproducible detections in iteration 1 (hits across protocols / distinct admissible mutants):
last ISI 43/22, first ISI 37/20, AHP depth 45/19, adaptation index 25/19, mean frequency 41/18,
spike count 49/16, AP amplitude 25/10, AP half-width 25/10, first-spike latency 29/9, rheobase
8/8, steady-state voltage 7/4. Greedy cover: last ISI, AP amplitude, AHP depth and adaptation
index together cover all 28.

Proposed: `spike_count`, `first_spike_latency`, `last_isi`, `adaptation_index`, `ap_amplitude`,
`ahp_depth`, `steady_state_voltage` (the only subthreshold feature, needed for P07), and
`rheobase`. The canonical harness is compared on the same features where they apply
(`canonical.features`), so the comparison with the battery stays like for like (N-06).

| protocol | features compared |
|---|---|
| P00 canonical | spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth |
| P03 | rheobase |
| P04, P05 | spike_count, first_spike_latency, last_isi, adaptation_index, ap_amplitude, ahp_depth |
| P06, P08 | spike_count, first_spike_latency |
| P07 | steady_state_voltage, spike_count |
| P09 | spike_count, first_spike_latency, ap_amplitude, ahp_depth |

Caveat: choosing features by iteration-1 detections favours features that already detect what
the canonical test detects. Iteration 2 is where that is checked on new cells.

## 4. Mutation families and operators (3 families; about 44 mutants)

One site per operator per model:
- biophysical: scale_conductance, scale_capacitance, shift_reversal, shift_initial_voltage,
  scale_gate_time_constant;
- reference: wrong_channel, wrong_compatible_component, omit_include, duplicate_conductance;
- numerical: recording_resolution, reduce_spatial_discretization (yields nothing on
  single-compartment cells).

That gives about 11 mutants per model, about 44 in total. Dropped with evidence:
- `wrong_segment_group` (4/4 equivalent) and `solver_config` (4/4 equivalent; jLEMS ignores
  `Meta`) are inert on these simulator and cell types;
- `increase_dt` is dropped because its silent mutants came mainly from the canonical and battery
  runs starting at different base steps (N-15).

**Not yet implemented.** An operator exclusion option in `configs/study.yaml`. The current
configuration selects families only, so the draft still generates the dropped operators until
that option is added. It is a small change and will come with tests.

Valid transformations: one site per transform operator, about 8 per model, about 32 in total.

## 5. Runtime estimate

Iteration 1 took 1 h 44 min wall time for 68 variants on 2 models (12 workers). Simulation CPU
time was about 3.3 h for probes and 1.7 h for canonical runs. The proposed battery costs about 75%
of iteration 1's per variant (1.52 M vs 2.02 M cell-steps). With about 76 variants and the
unknown cost of the WB and HH harnesses, expect roughly 2-3 h. The real figure will be recorded.

## 6. What iteration 2 can and cannot show

- **Can:** whether behaviour-changing model edits survive the canonical test on cells from
  other sources, with numerical artefacts removed. It also gives false-positive behaviour on
  more controls, runtime per model, and stability of the reduced feature set.
- **Cannot:** any confirmatory detection-rate comparison, which comes only from the frozen
  held-out study (D-026).

## 7. How it would run (after approval)

```bash
NEUROSEM_CONFIG_DIR=configs/pilot_v2_draft .venv/Scripts/python -m neurosem.cli pilot --campaign pilot-v2
```
