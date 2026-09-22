# Automated re-check of the audit sample (AI-assisted, not the human audit)

*26 mutants from 2 packs. Generated 2026-09-22T16:25:05+00:00 at commit `cb874532e3bebf30620afd27defe06ce37eb55f7` (tree dirty: False) by `scripts/audit_autocheck.py`. The human verdict columns in each `AUDIT_SHEET.csv` are left empty on purpose: the preregistered audit is done by people.*

## Summary

| check | passed | failed or unchecked |
|---|---|---|
| edit matches label (actual file diff = recorded edit, with the operator's meaning) | 26 | 0 |
| class re-derived from structural record, run status and raw detection rows | 26 | 0 |
| detections recomputed from per-run feature files (and raw traces for spike counts) | 26 | 0 |
| full-trace detections recomputed from raw voltage traces (spike count, spike timing, RMSE) | 26 | 0 |

**Flagged for human attention: 0.**

## What each check does

- *Edit*: the variant's files are compared with the unmodified reference workspace; every attribute change, added or removed element is listed. Passes only if the differences are exactly the recorded edit and have the meaning the operator's name claims.
- *Class*: re-derived with the classification rule; reproducible means the same protocol and feature are detected at h and at h/2.
- *Detections*: each recorded detection is recomputed from the two runs' feature files and compared with its tolerance; spike counts are recounted from the voltage traces (-20 mV upward crossings in the protocol window) without eFEL.

## Per mutant

### `m-scale_conductance-211745202a` (canonical_survivors)

- model `hay2011_soma`, operator `scale_conductance`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: 1 value(s) x1.1, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml condDensity 0.992 mS_per_cm2 -> 1.0912 mS_per_cm2
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P05_long_step:last_isi: 142.97 -> 148.3, |diff| 5.33 vs tau 3.03 OK
  - h/1 P05_long_step:spike_count: 14 -> 13, |diff| 1 vs tau 0.5 OK; raw-trace count 14 -> 13
  - h/2 P05_long_step:last_isi: 143.98 -> 149.34, |diff| 5.36 vs tau 3.03 OK
  - h/2 P05_long_step:spike_count: 14 -> 13, |diff| 1 vs tau 0.5 OK; raw-trace count 14 -> 13
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/1 P06_ramp:spike_timing: 24 spikes, max shift 7.177 ms vs tau 3.955 (recorded 7.177) OK
  - trace h/2 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/2 P06_ramp:spike_timing: 24 spikes, max shift 7.155 ms vs tau 3.955 (recorded 7.155) OK
  - trace h/4 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/4 P06_ramp:spike_timing: 24 spikes, max shift 7.146 ms vs tau 3.955 (recorded 7.146) OK

### `m-scale_conductance-75492a609a` (canonical_survivors)

- model `hay2011_soma`, operator `scale_conductance`, assigned class `4_equivalent_within_tested_domain`
- **edit matches label: yes**: 1 value(s) x0.5, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml condDensity 0.0675 mS_per_cm2 -> 0.03375 mS_per_cm2
- **class re-derived: `4_equivalent_within_tested_domain`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P04_step_2x:spike_timing: 15 spikes, max shift 5.773 ms vs tau 3.496 (recorded 5.773) OK
  - trace h/2 P04_step_2x:spike_timing: 15 spikes, max shift 5.768 ms vs tau 3.496 (recorded 5.768) OK
  - trace h/4 P04_step_2x:spike_timing: 15 spikes, max shift 5.765 ms vs tau 3.496 (recorded 5.765) OK

### `m-scale_gate_time_constant-02eb4e0b90` (canonical_survivors)

- model `hay2011_soma`, operator `scale_gate_time_constant`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: 2 value(s) x1.25, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml rate 0.209per_ms -> 0.26125per_ms
  - diff: attribute neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml rate 0.94per_ms -> 1.175per_ms
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P05_long_step:last_isi: 142.97 -> 153.41, |diff| 10.44 vs tau 3.03 OK
  - h/1 P05_long_step:spike_count: 14 -> 13, |diff| 1 vs tau 0.5 OK; raw-trace count 14 -> 13
  - h/2 P05_long_step:last_isi: 143.98 -> 154.36, |diff| 10.38 vs tau 3.03 OK
  - h/2 P05_long_step:spike_count: 14 -> 13, |diff| 1 vs tau 0.5 OK; raw-trace count 14 -> 13
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/1 P06_ramp:spike_timing: 24 spikes, max shift 13.799 ms vs tau 3.955 (recorded 13.799) OK
  - trace h/2 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/2 P06_ramp:spike_timing: 24 spikes, max shift 13.594 ms vs tau 3.955 (recorded 13.594) OK
  - trace h/4 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/4 P06_ramp:spike_timing: 24 spikes, max shift 13.500 ms vs tau 3.955 (recorded 13.500) OK

### `m-scale_gate_time_constant-31e82d8467` (canonical_survivors)

- model `migliore2005_ca1_soma`, operator `scale_gate_time_constant`, assigned class `4_equivalent_within_tested_domain`
- **edit matches label: yes**: 1 value(s) x0.8, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/kad.channel.nml fixedQ10 1 -> 0.8
- **class re-derived: `4_equivalent_within_tested_domain`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P04_step_2x:trace_rmse: RMSE 12.835 mV vs tau 8.749 (recorded 12.835) OK
  - trace h/1 P04_step_2x:spike_timing: 13 spikes, max shift 2.581 ms vs tau 0.518 (recorded 2.581) OK
  - trace h/1 P05_long_step:spike_timing: 39 spikes, max shift 13.693 ms vs tau 4.506 (recorded 13.693) OK
  - trace h/1 P06_ramp:trace_rmse: RMSE 13.153 mV vs tau 6.268 (recorded 13.153) OK
  - trace h/1 P06_ramp:spike_timing: 16 spikes, max shift 2.402 ms vs tau 0.578 (recorded 2.402) OK
  - trace h/2 P04_step_2x:trace_rmse: RMSE 12.796 mV vs tau 8.749 (recorded 12.796) OK
  - trace h/2 P04_step_2x:spike_timing: 13 spikes, max shift 2.581 ms vs tau 0.518 (recorded 2.581) OK
  - trace h/2 P05_long_step:spike_timing: 39 spikes, max shift 13.725 ms vs tau 4.506 (recorded 13.725) OK
  - trace h/2 P06_ramp:trace_rmse: RMSE 13.109 mV vs tau 6.268 (recorded 13.109) OK
  - trace h/2 P06_ramp:spike_timing: 16 spikes, max shift 2.398 ms vs tau 0.578 (recorded 2.398) OK
  - trace h/4 P04_step_2x:trace_rmse: RMSE 12.779 mV vs tau 8.749 (recorded 12.779) OK
  - trace h/4 P04_step_2x:spike_timing: 13 spikes, max shift 2.582 ms vs tau 0.518 (recorded 2.582) OK
  - trace h/4 P05_long_step:spike_timing: 39 spikes, max shift 13.741 ms vs tau 4.506 (recorded 13.741) OK
  - trace h/4 P06_ramp:trace_rmse: RMSE 13.089 mV vs tau 6.268 (recorded 13.089) OK
  - trace h/4 P06_ramp:spike_timing: 16 spikes, max shift 2.397 ms vs tau 0.578 (recorded 2.397) OK

### `m-scale_gate_time_constant-de97b02e71` (canonical_survivors)

- model `bbp2015_soma`, operator `scale_gate_time_constant`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: 2 value(s) x1.25, same units, nothing else changed
  - diff: attribute NMC/NeuroML2/Ca_HVA.channel.nml rate 0.209per_ms -> 0.26125per_ms
  - diff: attribute NMC/NeuroML2/Ca_HVA.channel.nml rate 0.94per_ms -> 1.175per_ms
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P05_long_step:last_isi: 118.66 -> 127.25, |diff| 8.59 vs tau 2.373 OK
  - h/1 P05_long_step:spike_count: 16 -> 15, |diff| 1 vs tau 0.5 OK; raw-trace count 16 -> 15
  - h/2 P05_long_step:last_isi: 118.89 -> 127.41, |diff| 8.52 vs tau 2.373 OK
  - h/2 P05_long_step:spike_count: 16 -> 15, |diff| 1 vs tau 0.5 OK; raw-trace count 16 -> 15
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P05_long_step:spike_count: raw spikes 16 -> 15 OK
  - trace h/1 P06_ramp:spike_timing: 33 spikes, max shift 8.159 ms vs tau 2.334 (recorded 8.159) OK
  - trace h/2 P05_long_step:spike_count: raw spikes 16 -> 15 OK
  - trace h/2 P06_ramp:spike_timing: 33 spikes, max shift 8.087 ms vs tau 2.334 (recorded 8.087) OK
  - trace h/4 P05_long_step:spike_count: raw spikes 16 -> 15 OK
  - trace h/4 P06_ramp:spike_timing: 33 spikes, max shift 8.052 ms vs tau 2.334 (recorded 8.052) OK

### `m-shift_reversal-e5f14f8fb3` (canonical_survivors)

- model `hay2011_soma`, operator `shift_reversal`, assigned class `4_equivalent_within_tested_domain`
- **edit matches label: yes**: 1 value(s) shifted -10 mV, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml erev -85.0 mV -> -95.0 mV
- **class re-derived: `4_equivalent_within_tested_domain`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P04_step_2x:spike_timing: 15 spikes, max shift 4.622 ms vs tau 3.496 (recorded 4.622) OK
  - trace h/2 P04_step_2x:spike_timing: 15 spikes, max shift 4.635 ms vs tau 3.496 (recorded 4.635) OK
  - trace h/4 P04_step_2x:spike_timing: 15 spikes, max shift 4.642 ms vs tau 3.496 (recorded 4.642) OK

### `m-duplicate_conductance-49ae908693` (random20)

- model `smith2013_singlecomp`, operator `duplicate_conductance`, assigned class `4_equivalent_within_tested_domain`
- **edit matches label: yes**: one element ca_all_dup added, identical to ca_all except id
  - diff: element_added NeuroML2/singleCompAllChans.cell.nml   ->
- **class re-derived: `4_equivalent_within_tested_domain`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: n/a (no trace detections)**

### `m-duplicate_conductance-f1055b2803` (random20)

- model `migliore2005_ca1_soma`, operator `duplicate_conductance`, assigned class `5_non_equivalent`
- **edit matches label: yes**: one element kdr_all_dup added, identical to kdr_all except id
  - diff: element_added neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml   ->
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:ahp_depth: -11.8548 -> -16.4814, |diff| 4.627 vs tau 0.5927 OK
  - h/1 P00_canonical:last_isi: 18.33 -> 19.41, |diff| 1.08 vs tau 0.5 OK
  - h/1 P03_rheobase:rheobase: 0.000580561 -> 0.000683013, |diff| 0.0001025 vs tau 6.83e-05 OK
  - h/1 P04_step_2x:ahp_depth: -14.7758 -> -18.7666, |diff| 3.991 vs tau 0.7388 OK
  - h/1 P04_step_2x:first_spike_latency: 16.07 -> 17.58, |diff| 1.51 vs tau 0.5 OK
  - h/1 P04_step_2x:last_isi: 40.06 -> 41.4, |diff| 1.34 vs tau 0.8012 OK
  - h/1 P04_step_2x:spike_count: 13 -> 12, |diff| 1 vs tau 0.5 OK; raw-trace count 13 -> 12
  - h/1 P05_long_step:ahp_depth: -15.0732 -> -18.9872, |diff| 3.914 vs tau 0.7537 OK
  - h/1 P05_long_step:first_spike_latency: 23.15 -> 26.93, |diff| 3.78 vs tau 0.5 OK
  - h/1 P05_long_step:last_isi: 51.51 -> 54.38, |diff| 2.87 vs tau 1.03 OK
  - h/1 P05_long_step:spike_count: 39 -> 37, |diff| 2 vs tau 0.5 OK; raw-trace count 39 -> 37
  - h/1 P06_ramp:first_spike_latency: 396.21 -> 450.27, |diff| 54.06 vs tau 7.924 OK
  - h/1 P06_ramp:spike_count: 16 -> 15, |diff| 1 vs tau 0.5 OK; raw-trace count 16 -> 15
  - h/1 P09_short_pulse:ahp_depth: -16.0012 -> -19.5895, |diff| 3.588 vs tau 0.8001 OK
  - h/2 P00_canonical:ahp_depth: -11.8041 -> -16.4459, |diff| 4.642 vs tau 0.5927 OK
  - h/2 P00_canonical:last_isi: 18.32 -> 19.4, |diff| 1.08 vs tau 0.5 OK
  - h/2 P03_rheobase:rheobase: 0.000580561 -> 0.000683013, |diff| 0.0001025 vs tau 6.83e-05 OK
  - h/2 P04_step_2x:ahp_depth: -14.5539 -> -18.6131, |diff| 4.059 vs tau 0.7388 OK
  - h/2 P04_step_2x:first_spike_latency: 16.03 -> 17.53, |diff| 1.5 vs tau 0.5 OK
  - h/2 P04_step_2x:last_isi: 40.05 -> 41.38, |diff| 1.33 vs tau 0.8012 OK
  - h/2 P04_step_2x:spike_count: 13 -> 12, |diff| 1 vs tau 0.5 OK; raw-trace count 13 -> 12
  - h/2 P05_long_step:ahp_depth: -14.8568 -> -18.8381, |diff| 3.981 vs tau 0.7537 OK
  - h/2 P05_long_step:first_spike_latency: 23.11 -> 26.89, |diff| 3.78 vs tau 0.5 OK
  - h/2 P05_long_step:last_isi: 51.56 -> 54.4, |diff| 2.84 vs tau 1.03 OK
  - h/2 P05_long_step:spike_count: 39 -> 37, |diff| 2 vs tau 0.5 OK; raw-trace count 39 -> 37
  - h/2 P06_ramp:first_spike_latency: 396.15 -> 450.21, |diff| 54.06 vs tau 7.924 OK
  - h/2 P06_ramp:spike_count: 16 -> 15, |diff| 1 vs tau 0.5 OK; raw-trace count 16 -> 15
  - h/2 P09_short_pulse:ahp_depth: -15.7914 -> -19.4461, |diff| 3.655 vs tau 0.8001 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 21.206 mV vs tau 4.056 (recorded 21.206) OK
  - trace h/1 P00_canonical:spike_count: raw spikes 4 -> 3 OK
  - trace h/1 P04_step_2x:trace_rmse: RMSE 16.812 mV vs tau 8.749 (recorded 16.812) OK
  - trace h/1 P04_step_2x:spike_count: raw spikes 13 -> 12 OK
  - trace h/1 P05_long_step:spike_count: raw spikes 39 -> 37 OK
  - trace h/1 P06_ramp:trace_rmse: RMSE 14.661 mV vs tau 6.268 (recorded 14.661) OK
  - trace h/1 P06_ramp:spike_count: raw spikes 16 -> 15 OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 1.587 mV vs tau 1.226 (recorded 1.587) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 21.192 mV vs tau 4.056 (recorded 21.192) OK
  - trace h/2 P00_canonical:spike_count: raw spikes 4 -> 3 OK
  - trace h/2 P04_step_2x:trace_rmse: RMSE 16.749 mV vs tau 8.749 (recorded 16.749) OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 13 -> 12 OK
  - trace h/2 P05_long_step:spike_count: raw spikes 39 -> 37 OK
  - trace h/2 P06_ramp:trace_rmse: RMSE 14.607 mV vs tau 6.268 (recorded 14.607) OK
  - trace h/2 P06_ramp:spike_count: raw spikes 16 -> 15 OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 1.598 mV vs tau 1.226 (recorded 1.598) OK

### `m-increase_dt-1086ebecdc` (random20)

- model `traub2005_testseg2`, operator `increase_dt`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: harness step x4 and probe dt_factor 4; nothing else
  - diff: attribute neuroConstruct/generatedNeuroML2/LEMS_SomaTest.xml step 0.001ms -> 0.004ms
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P04_step_2x:ahp_depth: -5.43348 -> -9.85705, |diff| 4.424 vs tau 1.145 OK
  - h/1 P04_step_2x:ap_amplitude: 76.6846 -> 79.815, |diff| 3.13 vs tau 1.896 OK
  - h/1 P05_long_step:ahp_depth: -5.30097 -> -9.8301, |diff| 4.529 vs tau 1.153 OK
  - h/1 P05_long_step:ap_amplitude: 77.2699 -> 80.3483, |diff| 3.078 vs tau 1.983 OK
  - h/1 P09_short_pulse:ahp_depth: -8.48818 -> -11.6373, |diff| 3.149 vs tau 1.087 OK
  - h/1 P09_short_pulse:ap_amplitude: definedness defined vs undefined (mismatch counts as detection)
  - h/2 P04_step_2x:ahp_depth: -5.05172 -> -6.41911, |diff| 1.367 vs tau 1.145 OK
  - h/2 P04_step_2x:spike_count: 18 -> 19, |diff| 1 vs tau 0.5 OK; raw-trace count 18 -> 19
  - h/2 P05_long_step:ahp_depth: -4.91679 -> -6.30453, |diff| 1.388 vs tau 1.153 OK
  - h/2 P09_short_pulse:ahp_depth: -8.12593 -> -9.30437, |diff| 1.178 vs tau 1.087 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 21.745 mV vs tau 4.390 (recorded 7.838) OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 2.705 mV vs tau 0.500 (recorded 0.711) OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 18 -> 19 OK

### `m-increase_dt-9ff98cb7be` (random20)

- model `smith2013_singlecomp`, operator `increase_dt`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: harness step x4 and probe dt_factor 4; nothing else
  - diff: attribute NeuroML2/LEMS_singleCompAllChans.xml step 0.001 ms -> 0.004 ms
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P04_step_2x:ahp_depth: -12.9467 -> 134.464, |diff| 147.4 vs tau 0.6473 OK
  - h/1 P09_short_pulse:ahp_depth: -13.721 -> 123.249, |diff| 137 vs tau 0.6861 OK
  - h/1 P09_short_pulse:ap_amplitude: definedness defined vs undefined (mismatch counts as detection)
  - h/2 P09_short_pulse:ap_amplitude: definedness defined vs undefined (mismatch counts as detection)
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 12.024 mV vs tau 3.009 (recorded 4.237) OK
  - trace h/1 P04_step_2x:spike_timing: 29 spikes, max shift 5.715 ms vs tau 3.078 (recorded 5.715) OK
  - trace h/1 P06_ramp:spike_timing: 35 spikes, max shift 5.600 ms vs tau 3.018 (recorded 5.600) OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 4.671 mV vs tau 0.775 (recorded 0.865) OK

### `m-scale_capacitance-8d53b9976a` (random20)

- model `traub2005_testseg_all`, operator `scale_capacitance`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 1 value(s) x0.8, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml value 1.0 uF_per_cm2 -> 0.8 uF_per_cm2
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:adaptation_index: 0.521669 -> 0.596154, |diff| 0.07448 vs tau 0.05217 OK
  - h/1 P00_canonical:ahp_depth: -8.24841 -> -10.3264, |diff| 2.078 vs tau 0.5 OK
  - h/1 P00_canonical:ap_amplitude: 74.7087 -> 80.0473, |diff| 5.339 vs tau 1.494 OK
  - h/1 P00_canonical:first_spike_latency: 2.95 -> 2.27, |diff| 0.68 vs tau 0.5 OK
  - h/1 P04_step_2x:ahp_depth: -3.06435 -> -11.1894, |diff| 8.125 vs tau 1.146 OK
  - h/1 P04_step_2x:first_spike_latency: 29.1 -> 2.61, |diff| 26.49 vs tau 0.582 OK
  - h/1 P05_long_step:ahp_depth: -2.79947 -> -5.09527, |diff| 2.296 vs tau 1.173 OK
  - h/1 P05_long_step:ap_amplitude: 72.99 -> 75.7765, |diff| 2.787 vs tau 1.46 OK
  - h/1 P05_long_step:first_spike_latency: 42.89 -> 41.71, |diff| 1.18 vs tau 0.8578 OK
  - h/1 P05_long_step:last_isi: 24.47 -> 22.67, |diff| 1.8 vs tau 1.11 OK
  - h/1 P05_long_step:spike_count: 83 -> 90, |diff| 7 vs tau 3 OK; raw-trace count 83 -> 90
  - h/1 P06_ramp:spike_count: 70 -> 78, |diff| 8 vs tau 3 OK; raw-trace count 70 -> 78
  - h/1 P09_short_pulse:ahp_depth: -2.69761 -> -4.39459, |diff| 1.697 vs tau 1.327 OK
  - h/1 P09_short_pulse:ap_amplitude: 96.1611 -> 99.1042, |diff| 2.943 vs tau 1.923 OK
  - h/2 P00_canonical:adaptation_index: 0.521488 -> 0.596015, |diff| 0.07453 vs tau 0.05217 OK
  - h/2 P00_canonical:ahp_depth: -8.21359 -> -10.2877, |diff| 2.074 vs tau 0.5 OK
  - h/2 P00_canonical:ap_amplitude: 74.6682 -> 79.9615, |diff| 5.293 vs tau 1.494 OK
  - h/2 P00_canonical:first_spike_latency: 2.95 -> 2.26, |diff| 0.69 vs tau 0.5 OK
  - h/2 P04_step_2x:ahp_depth: -2.68242 -> -10.8177, |diff| 8.135 vs tau 1.146 OK
  - h/2 P04_step_2x:first_spike_latency: 29.03 -> 2.56, |diff| 26.47 vs tau 0.582 OK
  - h/2 P05_long_step:ahp_depth: -2.40833 -> -4.68568, |diff| 2.277 vs tau 1.173 OK
  - h/2 P05_long_step:ap_amplitude: 72.5537 -> 75.2705, |diff| 2.717 vs tau 1.46 OK
  - h/2 P05_long_step:first_spike_latency: 42.82 -> 41.63, |diff| 1.19 vs tau 0.8578 OK
  - h/2 P05_long_step:last_isi: 24.84 -> 23.14, |diff| 1.7 vs tau 1.11 OK
  - h/2 P05_long_step:spike_count: 82 -> 88, |diff| 6 vs tau 3 OK; raw-trace count 82 -> 88
  - h/2 P06_ramp:spike_count: 69 -> 77, |diff| 8 vs tau 3 OK; raw-trace count 69 -> 77
  - h/2 P09_short_pulse:ahp_depth: -2.25538 -> -3.94007, |diff| 1.685 vs tau 1.327 OK
  - h/2 P09_short_pulse:ap_amplitude: 95.5725 -> 98.4828, |diff| 2.91 vs tau 1.923 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 14.867 mV vs tau 1.009 (recorded 14.867) OK
  - trace h/1 P00_canonical:spike_timing: 4 spikes, max shift 3.909 ms vs tau 0.500 (recorded 3.909) OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 2.463 mV vs tau 0.500 (recorded 2.463) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 14.869 mV vs tau 1.009 (recorded 14.869) OK
  - trace h/2 P00_canonical:spike_timing: 4 spikes, max shift 3.903 ms vs tau 0.500 (recorded 3.903) OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 2.451 mV vs tau 0.500 (recorded 2.451) OK

### `m-scale_capacitance-8f1d58bf3d` (random20)

- model `traub2005_testseg_all`, operator `scale_capacitance`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 1 value(s) x0.5, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml value 1.0 uF_per_cm2 -> 0.5 uF_per_cm2
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:adaptation_index: 0.521669 -> 0.0354452, |diff| 0.4862 vs tau 0.05217 OK
  - h/1 P00_canonical:ahp_depth: -8.24841 -> -14.5707, |diff| 6.322 vs tau 0.5 OK
  - h/1 P00_canonical:ap_amplitude: 74.7087 -> 96.1608, |diff| 21.45 vs tau 1.494 OK
  - h/1 P00_canonical:first_spike_latency: 2.95 -> 1.4, |diff| 1.55 vs tau 0.5 OK
  - h/1 P00_canonical:last_isi: 23.7 -> 4.67, |diff| 19.03 vs tau 0.5 OK
  - h/1 P00_canonical:spike_count: 4 -> 6, |diff| 2 vs tau 0.5 OK; raw-trace count 4 -> 6
  - h/1 P04_step_2x:ahp_depth: -3.06435 -> -14.8587, |diff| 11.79 vs tau 1.146 OK
  - h/1 P04_step_2x:ap_amplitude: 71.3325 -> 97.0768, |diff| 25.74 vs tau 1.427 OK
  - h/1 P04_step_2x:first_spike_latency: 29.1 -> 1.43, |diff| 27.67 vs tau 0.582 OK
  - h/1 P04_step_2x:spike_count: 51 -> 63, |diff| 12 vs tau 3 OK; raw-trace count 51 -> 64 (differs from eFEL count)
  - h/1 P05_long_step:ahp_depth: -2.79947 -> -15.3359, |diff| 12.54 vs tau 1.173 OK
  - h/1 P05_long_step:ap_amplitude: 72.99 -> 94.6531, |diff| 21.66 vs tau 1.46 OK
  - h/1 P05_long_step:first_spike_latency: 42.89 -> 2.04, |diff| 40.85 vs tau 0.8578 OK
  - h/1 P05_long_step:last_isi: 24.47 -> 4.97, |diff| 19.5 vs tau 1.11 OK
  - h/1 P05_long_step:spike_count: 83 -> 96, |diff| 13 vs tau 3 OK; raw-trace count 83 -> 96
  - h/1 P06_ramp:spike_count: 70 -> 95, |diff| 25 vs tau 3 OK; raw-trace count 70 -> 95
  - h/1 P09_short_pulse:ahp_depth: -2.69761 -> -7.88659, |diff| 5.189 vs tau 1.327 OK
  - h/1 P09_short_pulse:ap_amplitude: 96.1611 -> 104.435, |diff| 8.274 vs tau 1.923 OK
  - h/2 P00_canonical:adaptation_index: 0.521488 -> 0.0404319, |diff| 0.4811 vs tau 0.05217 OK
  - h/2 P00_canonical:ahp_depth: -8.21359 -> -14.5271, |diff| 6.313 vs tau 0.5 OK
  - h/2 P00_canonical:ap_amplitude: 74.6682 -> 96.1699, |diff| 21.5 vs tau 1.494 OK
  - h/2 P00_canonical:first_spike_latency: 2.95 -> 1.4, |diff| 1.55 vs tau 0.5 OK
  - h/2 P00_canonical:last_isi: 23.72 -> 5.64, |diff| 18.08 vs tau 0.5 OK
  - h/2 P00_canonical:spike_count: 4 -> 6, |diff| 2 vs tau 0.5 OK; raw-trace count 4 -> 6
  - h/2 P04_step_2x:ahp_depth: -2.68242 -> -14.4261, |diff| 11.74 vs tau 1.146 OK
  - h/2 P04_step_2x:ap_amplitude: 71.0038 -> 96.5471, |diff| 25.54 vs tau 1.427 OK
  - h/2 P04_step_2x:first_spike_latency: 29.03 -> 1.41, |diff| 27.62 vs tau 0.582 OK
  - h/2 P04_step_2x:spike_count: 50 -> 60, |diff| 10 vs tau 3 OK; raw-trace count 50 -> 60
  - h/2 P05_long_step:ahp_depth: -2.40833 -> -14.918, |diff| 12.51 vs tau 1.173 OK
  - h/2 P05_long_step:ap_amplitude: 72.5537 -> 94.254, |diff| 21.7 vs tau 1.46 OK
  - h/2 P05_long_step:first_spike_latency: 42.82 -> 2, |diff| 40.82 vs tau 0.8578 OK
  - h/2 P05_long_step:last_isi: 24.84 -> 4.99, |diff| 19.85 vs tau 1.11 OK
  - h/2 P05_long_step:spike_count: 82 -> 95, |diff| 13 vs tau 3 OK; raw-trace count 82 -> 95
  - h/2 P06_ramp:spike_count: 69 -> 93, |diff| 24 vs tau 3 OK; raw-trace count 69 -> 93
  - h/2 P09_short_pulse:ahp_depth: -2.25538 -> -7.41995, |diff| 5.165 vs tau 1.327 OK
  - h/2 P09_short_pulse:ap_amplitude: 95.5725 -> 103.75, |diff| 8.178 vs tau 1.923 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 17.288 mV vs tau 1.009 (recorded 17.288) OK
  - trace h/1 P00_canonical:spike_count: raw spikes 4 -> 6 OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 4.265 mV vs tau 0.500 (recorded 4.265) OK
  - trace h/1 P09_short_pulse:spike_timing: 2 spikes, max shift 0.874 ms vs tau 0.500 (recorded 0.874) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 16.979 mV vs tau 1.009 (recorded 16.979) OK
  - trace h/2 P00_canonical:spike_count: raw spikes 4 -> 6 OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 4.264 mV vs tau 0.500 (recorded 4.264) OK
  - trace h/2 P09_short_pulse:spike_timing: 2 spikes, max shift 0.879 ms vs tau 0.500 (recorded 0.879) OK

### `m-scale_conductance-056f6e95e6` (random20)

- model `migliore2005_ca1_soma`, operator `scale_conductance`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 1 value(s) x2, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml condDensity 0.05 mS_per_cm2 -> 0.1 mS_per_cm2
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:adaptation_index: definedness not_applicable vs defined (mismatch counts as detection)
  - h/1 P00_canonical:ahp_depth: -11.8548 -> -16.2421, |diff| 4.387 vs tau 0.5927 OK
  - h/1 P00_canonical:first_spike_latency: 5.42 -> 2.72, |diff| 2.7 vs tau 0.5 OK
  - h/1 P00_canonical:last_isi: 18.33 -> 17.23, |diff| 1.1 vs tau 0.5 OK
  - h/1 P00_canonical:spike_count: 3 -> 4, |diff| 1 vs tau 0.5 OK; raw-trace count 3 -> 4
  - h/1 P02_weak_step:spike_count: 0 -> 11, |diff| 11 vs tau 0.5 OK; raw-trace count 0 -> 11
  - h/1 P02_weak_step:steady_state_voltage: -65.0228 -> -65.6665, |diff| 0.6437 vs tau 0.5 OK
  - h/1 P03_rheobase:rheobase: definedness defined vs undefined (mismatch counts as detection)
  - h/1 P04_step_2x:ahp_depth: -14.7758 -> -16.6931, |diff| 1.917 vs tau 0.7388 OK
  - h/1 P04_step_2x:first_spike_latency: 16.07 -> 16.9, |diff| 0.83 vs tau 0.5 OK
  - h/1 P04_step_2x:last_isi: 40.06 -> 29.47, |diff| 10.59 vs tau 0.8012 OK
  - h/1 P04_step_2x:spike_count: 13 -> 17, |diff| 4 vs tau 0.5 OK; raw-trace count 13 -> 17
  - h/1 P05_long_step:ahp_depth: -15.0732 -> -16.9737, |diff| 1.9 vs tau 0.7537 OK
  - h/1 P05_long_step:first_spike_latency: 23.15 -> 19.71, |diff| 3.44 vs tau 0.5 OK
  - h/1 P05_long_step:last_isi: 51.51 -> 32.76, |diff| 18.75 vs tau 1.03 OK
  - h/1 P05_long_step:spike_count: 39 -> 61, |diff| 22 vs tau 0.5 OK; raw-trace count 39 -> 61
  - h/1 P06_ramp:first_spike_latency: 396.21 -> 44.63, |diff| 351.6 vs tau 7.924 OK
  - h/1 P06_ramp:spike_count: 16 -> 30, |diff| 14 vs tau 0.5 OK; raw-trace count 16 -> 30
  - h/1 P07_hyperpolarizing_step:steady_state_voltage: -68.1353 -> -65.1411, |diff| 2.994 vs tau 0.5 OK
  - h/1 P08_rebound:first_spike_latency: definedness not_applicable vs defined (mismatch counts as detection)
  - h/1 P08_rebound:spike_count: 0 -> 5, |diff| 5 vs tau 0.5 OK; raw-trace count 0 -> 5
  - h/1 P09_short_pulse:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P09_short_pulse:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P09_short_pulse:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P09_short_pulse:spike_count: 1 -> 0, |diff| 1 vs tau 0.5 OK; raw-trace count 1 -> 0
  - h/2 P00_canonical:adaptation_index: definedness not_applicable vs defined (mismatch counts as detection)
  - h/2 P00_canonical:ahp_depth: -11.8041 -> -16.191, |diff| 4.387 vs tau 0.5927 OK
  - h/2 P00_canonical:first_spike_latency: 5.41 -> 2.72, |diff| 2.69 vs tau 0.5 OK
  - h/2 P00_canonical:last_isi: 18.32 -> 17.23, |diff| 1.09 vs tau 0.5 OK
  - h/2 P00_canonical:spike_count: 3 -> 4, |diff| 1 vs tau 0.5 OK; raw-trace count 3 -> 4
  - h/2 P02_weak_step:spike_count: 0 -> 11, |diff| 11 vs tau 0.5 OK; raw-trace count 0 -> 11
  - h/2 P02_weak_step:steady_state_voltage: -65.0228 -> -65.7906, |diff| 0.7678 vs tau 0.5 OK
  - h/2 P03_rheobase:rheobase: definedness defined vs undefined (mismatch counts as detection)
  - h/2 P04_step_2x:ahp_depth: -14.5539 -> -17.0166, |diff| 2.463 vs tau 0.7388 OK
  - h/2 P04_step_2x:first_spike_latency: 16.03 -> 17.83, |diff| 1.8 vs tau 0.5 OK
  - h/2 P04_step_2x:last_isi: 40.05 -> 29.45, |diff| 10.6 vs tau 0.8012 OK
  - h/2 P04_step_2x:spike_count: 13 -> 17, |diff| 4 vs tau 0.5 OK; raw-trace count 13 -> 17
  - h/2 P05_long_step:ahp_depth: -14.8568 -> -17.3023, |diff| 2.446 vs tau 0.7537 OK
  - h/2 P05_long_step:first_spike_latency: 23.11 -> 20.74, |diff| 2.37 vs tau 0.5 OK
  - h/2 P05_long_step:last_isi: 51.56 -> 32.76, |diff| 18.8 vs tau 1.03 OK
  - h/2 P05_long_step:spike_count: 39 -> 61, |diff| 22 vs tau 0.5 OK; raw-trace count 39 -> 61
  - h/2 P06_ramp:first_spike_latency: 396.15 -> 45.82, |diff| 350.3 vs tau 7.924 OK
  - h/2 P06_ramp:spike_count: 16 -> 30, |diff| 14 vs tau 0.5 OK; raw-trace count 16 -> 30
  - h/2 P07_hyperpolarizing_step:steady_state_voltage: -68.1353 -> -65.1411, |diff| 2.994 vs tau 0.5 OK
  - h/2 P08_rebound:first_spike_latency: definedness not_applicable vs defined (mismatch counts as detection)
  - h/2 P08_rebound:spike_count: 0 -> 5, |diff| 5 vs tau 0.5 OK; raw-trace count 0 -> 5
  - h/2 P09_short_pulse:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P09_short_pulse:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P09_short_pulse:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P09_short_pulse:spike_count: 1 -> 0, |diff| 1 vs tau 0.5 OK; raw-trace count 1 -> 0
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 28.657 mV vs tau 4.056 (recorded 28.657) OK
  - trace h/1 P00_canonical:spike_timing: 4 spikes, max shift 5.987 ms vs tau 0.500 (recorded 5.987) OK
  - trace h/1 P02_weak_step:trace_rmse: RMSE 14.624 mV vs tau 0.500 (recorded 14.624) OK
  - trace h/1 P02_weak_step:spike_count: raw spikes 0 -> 19 OK
  - trace h/1 P04_step_2x:trace_rmse: RMSE 20.184 mV vs tau 8.749 (recorded 20.184) OK
  - trace h/1 P04_step_2x:spike_count: raw spikes 13 -> 25 OK
  - trace h/1 P05_long_step:spike_count: raw spikes 39 -> 69 OK
  - trace h/1 P06_ramp:trace_rmse: RMSE 19.927 mV vs tau 6.268 (recorded 19.927) OK
  - trace h/1 P06_ramp:spike_count: raw spikes 16 -> 38 OK
  - trace h/1 P07_hyperpolarizing_step:trace_rmse: RMSE 9.833 mV vs tau 0.500 (recorded 9.833) OK
  - trace h/1 P07_hyperpolarizing_step:spike_count: raw spikes 0 -> 8 OK
  - trace h/1 P08_rebound:trace_rmse: RMSE 10.459 mV vs tau 0.500 (recorded 10.459) OK
  - trace h/1 P08_rebound:spike_count: raw spikes 0 -> 10 OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 13.680 mV vs tau 1.226 (recorded 13.680) OK
  - trace h/1 P09_short_pulse:spike_count: raw spikes 1 -> 7 OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 28.636 mV vs tau 4.056 (recorded 28.636) OK
  - trace h/2 P00_canonical:spike_timing: 4 spikes, max shift 5.981 ms vs tau 0.500 (recorded 5.981) OK
  - trace h/2 P02_weak_step:trace_rmse: RMSE 14.577 mV vs tau 0.500 (recorded 14.577) OK
  - trace h/2 P02_weak_step:spike_count: raw spikes 0 -> 19 OK
  - trace h/2 P04_step_2x:trace_rmse: RMSE 20.061 mV vs tau 8.749 (recorded 20.061) OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 13 -> 25 OK
  - trace h/2 P05_long_step:spike_count: raw spikes 39 -> 69 OK
  - trace h/2 P06_ramp:trace_rmse: RMSE 19.531 mV vs tau 6.268 (recorded 19.531) OK
  - trace h/2 P06_ramp:spike_count: raw spikes 16 -> 38 OK
  - trace h/2 P07_hyperpolarizing_step:trace_rmse: RMSE 9.803 mV vs tau 0.500 (recorded 9.803) OK
  - trace h/2 P07_hyperpolarizing_step:spike_count: raw spikes 0 -> 8 OK
  - trace h/2 P08_rebound:trace_rmse: RMSE 10.427 mV vs tau 0.500 (recorded 10.427) OK
  - trace h/2 P08_rebound:spike_count: raw spikes 0 -> 10 OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 13.628 mV vs tau 1.226 (recorded 13.628) OK
  - trace h/2 P09_short_pulse:spike_count: raw spikes 1 -> 7 OK

### `m-scale_conductance-2956a62118` (random20)

- model `bbp2015_soma`, operator `scale_conductance`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: 1 value(s) x0.9, same units, nothing else changed
  - diff: attribute NMC/NeuroML2/Soma_AllNML2.cell.nml condDensity 3.43 mS_per_cm2 -> 3.087 mS_per_cm2
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P04_step_2x:spike_count: 30 -> 29, |diff| 1 vs tau 0.5 OK; raw-trace count 30 -> 29
  - h/2 P04_step_2x:spike_count: 30 -> 29, |diff| 1 vs tau 0.5 OK; raw-trace count 30 -> 29
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 7.042 mV vs tau 1.567 (recorded 7.042) OK
  - trace h/1 P00_canonical:spike_timing: 5 spikes, max shift 2.613 ms vs tau 0.500 (recorded 2.613) OK
  - trace h/1 P04_step_2x:spike_count: raw spikes 30 -> 29 OK
  - trace h/1 P05_long_step:spike_timing: 16 spikes, max shift 21.706 ms vs tau 9.523 (recorded 21.706) OK
  - trace h/1 P06_ramp:spike_timing: 33 spikes, max shift 3.080 ms vs tau 2.334 (recorded 3.080) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 7.045 mV vs tau 1.567 (recorded 7.045) OK
  - trace h/2 P00_canonical:spike_timing: 5 spikes, max shift 2.615 ms vs tau 0.500 (recorded 2.615) OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 30 -> 29 OK
  - trace h/2 P05_long_step:spike_timing: 16 spikes, max shift 21.774 ms vs tau 9.523 (recorded 21.774) OK
  - trace h/2 P06_ramp:spike_timing: 33 spikes, max shift 3.097 ms vs tau 2.334 (recorded 3.097) OK
  - trace h/4 P00_canonical:trace_rmse: RMSE 7.046 mV vs tau 1.567 (recorded 7.046) OK
  - trace h/4 P00_canonical:spike_timing: 5 spikes, max shift 2.616 ms vs tau 0.500 (recorded 2.616) OK
  - trace h/4 P04_step_2x:spike_timing: 30 spikes, max shift 7.297 ms vs tau 3.458 (recorded 7.297) OK
  - trace h/4 P05_long_step:spike_timing: 16 spikes, max shift 21.807 ms vs tau 9.523 (recorded 21.807) OK
  - trace h/4 P06_ramp:spike_timing: 33 spikes, max shift 3.104 ms vs tau 2.334 (recorded 3.104) OK

### `m-scale_conductance-c2b2371643` (random20)

- model `migliore2005_ca1_soma`, operator `scale_conductance`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: 1 value(s) x0.9, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml condDensity 25.0 mS_per_cm2 -> 22.5 mS_per_cm2
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P04_step_2x:spike_count: 13 -> 12, |diff| 1 vs tau 0.5 OK; raw-trace count 13 -> 12
  - h/1 P05_long_step:first_spike_latency: 23.15 -> 23.93, |diff| 0.78 vs tau 0.5 OK
  - h/1 P05_long_step:last_isi: 51.51 -> 52.63, |diff| 1.12 vs tau 1.03 OK
  - h/1 P05_long_step:spike_count: 39 -> 38, |diff| 1 vs tau 0.5 OK; raw-trace count 39 -> 38
  - h/1 P06_ramp:first_spike_latency: 396.21 -> 407, |diff| 10.79 vs tau 7.924 OK
  - h/2 P04_step_2x:spike_count: 13 -> 12, |diff| 1 vs tau 0.5 OK; raw-trace count 13 -> 12
  - h/2 P05_long_step:first_spike_latency: 23.11 -> 23.89, |diff| 0.78 vs tau 0.5 OK
  - h/2 P05_long_step:last_isi: 51.56 -> 52.68, |diff| 1.12 vs tau 1.03 OK
  - h/2 P05_long_step:spike_count: 39 -> 38, |diff| 1 vs tau 0.5 OK; raw-trace count 39 -> 38
  - h/2 P06_ramp:first_spike_latency: 396.15 -> 406.94, |diff| 10.79 vs tau 7.924 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 4.960 mV vs tau 4.056 (recorded 4.960) OK
  - trace h/1 P04_step_2x:trace_rmse: RMSE 15.206 mV vs tau 8.749 (recorded 15.206) OK
  - trace h/1 P04_step_2x:spike_timing: 13 spikes, max shift 6.707 ms vs tau 0.518 (recorded 6.707) OK
  - trace h/1 P05_long_step:spike_count: raw spikes 39 -> 38 OK
  - trace h/1 P06_ramp:trace_rmse: RMSE 15.690 mV vs tau 6.268 (recorded 15.690) OK
  - trace h/1 P06_ramp:spike_timing: 16 spikes, max shift 10.793 ms vs tau 0.578 (recorded 10.793) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 4.952 mV vs tau 4.056 (recorded 4.952) OK
  - trace h/2 P04_step_2x:trace_rmse: RMSE 15.161 mV vs tau 8.749 (recorded 15.161) OK
  - trace h/2 P04_step_2x:spike_timing: 13 spikes, max shift 6.596 ms vs tau 0.518 (recorded 6.596) OK
  - trace h/2 P05_long_step:spike_count: raw spikes 39 -> 38 OK
  - trace h/2 P06_ramp:trace_rmse: RMSE 15.635 mV vs tau 6.268 (recorded 15.635) OK
  - trace h/2 P06_ramp:spike_timing: 16 spikes, max shift 10.793 ms vs tau 0.578 (recorded 10.793) OK
  - trace h/4 P00_canonical:trace_rmse: RMSE 4.950 mV vs tau 4.056 (recorded 4.950) OK
  - trace h/4 P04_step_2x:trace_rmse: RMSE 15.141 mV vs tau 8.749 (recorded 15.141) OK
  - trace h/4 P04_step_2x:spike_timing: 13 spikes, max shift 6.543 ms vs tau 0.518 (recorded 6.543) OK
  - trace h/4 P05_long_step:spike_count: raw spikes 39 -> 38 OK
  - trace h/4 P06_ramp:trace_rmse: RMSE 15.610 mV vs tau 6.268 (recorded 15.610) OK
  - trace h/4 P06_ramp:spike_timing: 16 spikes, max shift 10.793 ms vs tau 0.578 (recorded 10.793) OK

### `m-scale_conductance-c9ac5a125c` (random20)

- model `traub2005_testseg2`, operator `scale_conductance`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 1 value(s) x0.5, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml condDensity 15.0 mS_per_cm2 -> 7.5 mS_per_cm2
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:ahp_depth: -7.97745 -> -6.88505, |diff| 1.092 vs tau 0.5 OK
  - h/1 P00_canonical:ap_amplitude: 76.0384 -> 80.3257, |diff| 4.287 vs tau 1.521 OK
  - h/1 P00_canonical:first_spike_latency: 2.91 -> 2.33, |diff| 0.58 vs tau 0.5 OK
  - h/1 P00_canonical:last_isi: 7.59 -> 6.74, |diff| 0.85 vs tau 0.5 OK
  - h/1 P00_canonical:spike_count: 9 -> 10, |diff| 1 vs tau 0.5 OK; raw-trace count 9 -> 10
  - h/1 P02_weak_step:spike_count: 0 -> 2, |diff| 2 vs tau 0.5 OK; raw-trace count 0 -> 2
  - h/1 P02_weak_step:steady_state_voltage: -63.1131 -> -59.6138, |diff| 3.499 vs tau 0.5 OK
  - h/1 P03_rheobase:rheobase: 0.0171095 -> 0.00706919, |diff| 0.01004 vs tau 0.0003422 OK
  - h/1 P04_step_2x:ahp_depth: -5.43348 -> -6.81909, |diff| 1.386 vs tau 1.145 OK
  - h/1 P04_step_2x:first_spike_latency: 53.73 -> 21.86, |diff| 31.87 vs tau 1.075 OK
  - h/1 P04_step_2x:last_isi: 25.63 -> 15.8, |diff| 9.83 vs tau 1.29 OK
  - h/1 P04_step_2x:spike_count: 18 -> 32, |diff| 14 vs tau 0.5 OK; raw-trace count 18 -> 32
  - h/1 P05_long_step:ahp_depth: -5.30097 -> -6.69849, |diff| 1.398 vs tau 1.153 OK
  - h/1 P05_long_step:first_spike_latency: 86.5 -> 30.79, |diff| 55.71 vs tau 1.73 OK
  - h/1 P05_long_step:last_isi: 46.56 -> 22.43, |diff| 24.13 vs tau 2.61 OK
  - h/1 P05_long_step:spike_count: 42 -> 89, |diff| 47 vs tau 3 OK; raw-trace count 42 -> 89
  - h/1 P06_ramp:first_spike_latency: 435.04 -> 235.48, |diff| 199.6 vs tau 8.701 OK
  - h/1 P06_ramp:spike_count: 27 -> 46, |diff| 19 vs tau 3 OK; raw-trace count 27 -> 46
  - h/1 P07_hyperpolarizing_step:steady_state_voltage: -69.12 -> -68.5962, |diff| 0.5238 vs tau 0.5 OK
  - h/1 P09_short_pulse:ahp_depth: -8.48818 -> -6.30158, |diff| 2.187 vs tau 1.087 OK
  - h/2 P00_canonical:ahp_depth: -7.91186 -> -6.81019, |diff| 1.102 vs tau 0.5 OK
  - h/2 P00_canonical:ap_amplitude: 75.9728 -> 80.2048, |diff| 4.232 vs tau 1.521 OK
  - h/2 P00_canonical:first_spike_latency: 2.9 -> 2.32, |diff| 0.58 vs tau 0.5 OK
  - h/2 P00_canonical:last_isi: 7.61 -> 6.75, |diff| 0.86 vs tau 0.5 OK
  - h/2 P00_canonical:spike_count: 9 -> 10, |diff| 1 vs tau 0.5 OK; raw-trace count 9 -> 10
  - h/2 P02_weak_step:spike_count: 0 -> 2, |diff| 2 vs tau 0.5 OK; raw-trace count 0 -> 2
  - h/2 P02_weak_step:steady_state_voltage: -63.1131 -> -59.7487, |diff| 3.364 vs tau 0.5 OK
  - h/2 P03_rheobase:rheobase: 0.0171095 -> 0.00706919, |diff| 0.01004 vs tau 0.0003422 OK
  - h/2 P04_step_2x:ahp_depth: -5.05172 -> -6.43544, |diff| 1.384 vs tau 1.145 OK
  - h/2 P04_step_2x:first_spike_latency: 53.65 -> 21.8, |diff| 31.85 vs tau 1.075 OK
  - h/2 P04_step_2x:last_isi: 26.06 -> 16.1, |diff| 9.96 vs tau 1.29 OK
  - h/2 P04_step_2x:spike_count: 18 -> 31, |diff| 13 vs tau 0.5 OK; raw-trace count 18 -> 31
  - h/2 P05_long_step:ahp_depth: -4.91679 -> -6.31222, |diff| 1.395 vs tau 1.153 OK
  - h/2 P05_long_step:first_spike_latency: 86.42 -> 30.72, |diff| 55.7 vs tau 1.73 OK
  - h/2 P05_long_step:last_isi: 47.43 -> 22.85, |diff| 24.58 vs tau 2.61 OK
  - h/2 P05_long_step:spike_count: 41 -> 87, |diff| 46 vs tau 3 OK; raw-trace count 41 -> 87
  - h/2 P06_ramp:first_spike_latency: 434.96 -> 235.4, |diff| 199.6 vs tau 8.701 OK
  - h/2 P06_ramp:spike_count: 26 -> 46, |diff| 20 vs tau 3 OK; raw-trace count 26 -> 46
  - h/2 P07_hyperpolarizing_step:steady_state_voltage: -69.12 -> -68.5962, |diff| 0.5238 vs tau 0.5 OK
  - h/2 P09_short_pulse:ahp_depth: -8.12593 -> -5.87513, |diff| 2.251 vs tau 1.087 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 22.321 mV vs tau 4.390 (recorded 22.321) OK
  - trace h/1 P00_canonical:spike_count: raw spikes 9 -> 10 OK
  - trace h/1 P02_weak_step:trace_rmse: RMSE 3.586 mV vs tau 0.500 (recorded 3.586) OK
  - trace h/1 P02_weak_step:spike_count: raw spikes 0 -> 2 OK
  - trace h/1 P04_step_2x:spike_count: raw spikes 18 -> 32 OK
  - trace h/1 P07_hyperpolarizing_step:trace_rmse: RMSE 0.998 mV vs tau 0.500 (recorded 0.998) OK
  - trace h/1 P08_rebound:trace_rmse: RMSE 0.935 mV vs tau 0.500 (recorded 0.935) OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 1.941 mV vs tau 0.500 (recorded 1.941) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 22.335 mV vs tau 4.390 (recorded 22.335) OK
  - trace h/2 P00_canonical:spike_count: raw spikes 9 -> 10 OK
  - trace h/2 P02_weak_step:trace_rmse: RMSE 3.584 mV vs tau 0.500 (recorded 3.584) OK
  - trace h/2 P02_weak_step:spike_count: raw spikes 0 -> 2 OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 18 -> 31 OK
  - trace h/2 P07_hyperpolarizing_step:trace_rmse: RMSE 0.998 mV vs tau 0.500 (recorded 0.998) OK
  - trace h/2 P08_rebound:trace_rmse: RMSE 0.935 mV vs tau 0.500 (recorded 0.935) OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 1.919 mV vs tau 0.500 (recorded 1.919) OK

### `m-scale_gate_slope-039828a4db` (random20)

- model `bbp2015_soma`, operator `scale_gate_slope`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 2 value(s) x0.8, same units, nothing else changed
  - diff: attribute NMC/NeuroML2/Ih.channel.nml scale -11.9mV -> -9.52mV
  - diff: attribute NMC/NeuroML2/Ih.channel.nml scale 33.1mV -> 26.48mV
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:ahp_depth: -0.540113 -> 0.655864, |diff| 1.196 vs tau 0.5 OK
  - h/1 P00_canonical:last_isi: 23.59 -> 24.1, |diff| 0.51 vs tau 0.5 OK
  - h/1 P04_step_2x:ahp_depth: 0.87351 -> 3.66989, |diff| 2.796 vs tau 0.5 OK
  - h/1 P05_long_step:ahp_depth: 0.504896 -> 3.21421, |diff| 2.709 vs tau 0.5 OK
  - h/1 P05_long_step:first_spike_latency: 10.13 -> 10.9, |diff| 0.77 vs tau 0.5 OK
  - h/1 P07_hyperpolarizing_step:steady_state_voltage: -97.965 -> -99.3951, |diff| 1.43 vs tau 0.5 OK
  - h/1 P09_short_pulse:ahp_depth: -0.966387 -> 1.85451, |diff| 2.821 vs tau 0.5 OK
  - h/2 P00_canonical:ahp_depth: -0.544305 -> 0.65161, |diff| 1.196 vs tau 0.5 OK
  - h/2 P00_canonical:last_isi: 23.58 -> 24.1, |diff| 0.52 vs tau 0.5 OK
  - h/2 P04_step_2x:ahp_depth: 0.855008 -> 3.65081, |diff| 2.796 vs tau 0.5 OK
  - h/2 P05_long_step:ahp_depth: 0.51788 -> 3.23192, |diff| 2.714 vs tau 0.5 OK
  - h/2 P05_long_step:first_spike_latency: 10.1 -> 10.87, |diff| 0.77 vs tau 0.5 OK
  - h/2 P07_hyperpolarizing_step:steady_state_voltage: -97.965 -> -99.3951, |diff| 1.43 vs tau 0.5 OK
  - h/2 P09_short_pulse:ahp_depth: -0.994976 -> 1.81809, |diff| 2.813 vs tau 0.5 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 3.809 mV vs tau 1.567 (recorded 3.809) OK
  - trace h/1 P00_canonical:spike_timing: 5 spikes, max shift 0.629 ms vs tau 0.500 (recorded 0.629) OK
  - trace h/1 P02_weak_step:trace_rmse: RMSE 1.633 mV vs tau 0.500 (recorded 1.633) OK
  - trace h/1 P04_step_2x:spike_timing: 30 spikes, max shift 4.530 ms vs tau 3.458 (recorded 4.530) OK
  - trace h/1 P05_long_step:spike_timing: 16 spikes, max shift 22.072 ms vs tau 9.523 (recorded 22.072) OK
  - trace h/1 P06_ramp:spike_timing: 33 spikes, max shift 3.322 ms vs tau 2.334 (recorded 3.322) OK
  - trace h/1 P07_hyperpolarizing_step:trace_rmse: RMSE 2.063 mV vs tau 0.500 (recorded 2.063) OK
  - trace h/1 P08_rebound:trace_rmse: RMSE 1.517 mV vs tau 0.500 (recorded 1.517) OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 1.848 mV vs tau 0.647 (recorded 1.848) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 3.805 mV vs tau 1.567 (recorded 3.805) OK
  - trace h/2 P00_canonical:spike_timing: 5 spikes, max shift 0.627 ms vs tau 0.500 (recorded 0.627) OK
  - trace h/2 P02_weak_step:trace_rmse: RMSE 1.633 mV vs tau 0.500 (recorded 1.633) OK
  - trace h/2 P04_step_2x:spike_timing: 30 spikes, max shift 4.510 ms vs tau 3.458 (recorded 4.510) OK
  - trace h/2 P05_long_step:spike_timing: 16 spikes, max shift 22.096 ms vs tau 9.523 (recorded 22.096) OK
  - trace h/2 P06_ramp:spike_timing: 33 spikes, max shift 3.322 ms vs tau 2.334 (recorded 3.322) OK
  - trace h/2 P07_hyperpolarizing_step:trace_rmse: RMSE 2.063 mV vs tau 0.500 (recorded 2.063) OK
  - trace h/2 P08_rebound:trace_rmse: RMSE 1.518 mV vs tau 0.500 (recorded 1.518) OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 1.853 mV vs tau 0.647 (recorded 1.853) OK

### `m-scale_gate_time_constant-02eb4e0b90` (random20)

- model `hay2011_soma`, operator `scale_gate_time_constant`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: 2 value(s) x1.25, same units, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml rate 0.209per_ms -> 0.26125per_ms
  - diff: attribute neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml rate 0.94per_ms -> 1.175per_ms
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P05_long_step:last_isi: 142.97 -> 153.41, |diff| 10.44 vs tau 3.03 OK
  - h/1 P05_long_step:spike_count: 14 -> 13, |diff| 1 vs tau 0.5 OK; raw-trace count 14 -> 13
  - h/2 P05_long_step:last_isi: 143.98 -> 154.36, |diff| 10.38 vs tau 3.03 OK
  - h/2 P05_long_step:spike_count: 14 -> 13, |diff| 1 vs tau 0.5 OK; raw-trace count 14 -> 13
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/1 P06_ramp:spike_timing: 24 spikes, max shift 13.799 ms vs tau 3.955 (recorded 13.799) OK
  - trace h/2 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/2 P06_ramp:spike_timing: 24 spikes, max shift 13.594 ms vs tau 3.955 (recorded 13.594) OK
  - trace h/4 P05_long_step:spike_count: raw spikes 14 -> 13 OK
  - trace h/4 P06_ramp:spike_timing: 24 spikes, max shift 13.500 ms vs tau 3.955 (recorded 13.500) OK

### `m-scale_gate_time_constant-97ff619aea` (random20)

- model `smith2013_singlecomp`, operator `scale_gate_time_constant`, assigned class `6_silent_under_canonical`
- **edit matches label: yes**: q10Settings fixedQ10=0.5 inserted on gate[@id='h']; nothing else
  - diff: element_added NeuroML2/it.channel.nml   ->
- **class re-derived: `6_silent_under_canonical`** (matches)
- **detections recomputed: yes**
  - h/1 P03_rheobase:rheobase: 0.0216515 -> 0.0223687, |diff| 0.0007172 vs tau 0.000433 OK
  - h/1 P06_ramp:first_spike_latency: 403.09 -> 389.2, |diff| 13.89 vs tau 8.062 OK
  - h/1 P06_ramp:spike_count: 35 -> 36, |diff| 1 vs tau 0.5 OK; raw-trace count 35 -> 36
  - h/2 P03_rheobase:rheobase: 0.0216515 -> 0.0223687, |diff| 0.0007172 vs tau 0.000433 OK
  - h/2 P06_ramp:first_spike_latency: 403.01 -> 389.13, |diff| 13.88 vs tau 8.062 OK
  - h/2 P06_ramp:spike_count: 35 -> 36, |diff| 1 vs tau 0.5 OK; raw-trace count 35 -> 36
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 6.327 mV vs tau 3.009 (recorded 6.327) OK
  - trace h/1 P06_ramp:spike_count: raw spikes 35 -> 36 OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 6.328 mV vs tau 3.009 (recorded 6.328) OK
  - trace h/2 P06_ramp:spike_count: raw spikes 35 -> 36 OK
  - trace h/4 P00_canonical:trace_rmse: RMSE 6.328 mV vs tau 3.009 (recorded 6.328) OK
  - trace h/4 P06_ramp:spike_count: raw spikes 35 -> 36 OK

### `m-shift_forward_rate_midpoint-3567e7da5d` (random20)

- model `traub2005_testseg_all`, operator `shift_forward_rate_midpoint`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 1 value(s) shifted +5 mV, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/cal.channel.nml midpoint 5mV -> 10mV
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:ahp_depth: -8.24841 -> -8.9596, |diff| 0.7112 vs tau 0.5 OK
  - h/1 P02_weak_step:steady_state_voltage: -63.1905 -> -62.1472, |diff| 1.043 vs tau 0.5 OK
  - h/1 P03_rheobase:rheobase: 0.0614371 -> 0.0453521, |diff| 0.01608 vs tau 0.001229 OK
  - h/1 P04_step_2x:ahp_depth: -3.06435 -> -9.66679, |diff| 6.602 vs tau 1.146 OK
  - h/1 P04_step_2x:ap_amplitude: 71.3325 -> 68.961, |diff| 2.372 vs tau 1.427 OK
  - h/1 P04_step_2x:first_spike_latency: 29.1 -> 3.03, |diff| 26.07 vs tau 0.582 OK
  - h/1 P05_long_step:ahp_depth: -2.79947 -> -5.16902, |diff| 2.37 vs tau 1.173 OK
  - h/1 P05_long_step:first_spike_latency: 42.89 -> 26.93, |diff| 15.96 vs tau 0.8578 OK
  - h/1 P06_ramp:first_spike_latency: 382.87 -> 288.04, |diff| 94.83 vs tau 7.657 OK
  - h/2 P00_canonical:ahp_depth: -8.21359 -> -8.92438, |diff| 0.7108 vs tau 0.5 OK
  - h/2 P02_weak_step:steady_state_voltage: -63.1905 -> -62.1472, |diff| 1.043 vs tau 0.5 OK
  - h/2 P03_rheobase:rheobase: 0.0614371 -> 0.0453521, |diff| 0.01608 vs tau 0.001229 OK
  - h/2 P04_step_2x:ahp_depth: -2.68242 -> -9.32168, |diff| 6.639 vs tau 1.146 OK
  - h/2 P04_step_2x:ap_amplitude: 71.0038 -> 68.7999, |diff| 2.204 vs tau 1.427 OK
  - h/2 P04_step_2x:first_spike_latency: 29.03 -> 2.98, |diff| 26.05 vs tau 0.582 OK
  - h/2 P05_long_step:ahp_depth: -2.40833 -> -4.79679, |diff| 2.388 vs tau 1.173 OK
  - h/2 P05_long_step:first_spike_latency: 42.82 -> 26.85, |diff| 15.97 vs tau 0.8578 OK
  - h/2 P06_ramp:first_spike_latency: 382.79 -> 287.96, |diff| 94.83 vs tau 7.657 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 12.842 mV vs tau 1.009 (recorded 12.842) OK
  - trace h/1 P00_canonical:spike_timing: 4 spikes, max shift 1.068 ms vs tau 0.500 (recorded 1.068) OK
  - trace h/1 P02_weak_step:trace_rmse: RMSE 1.021 mV vs tau 0.500 (recorded 1.021) OK
  - trace h/1 P07_hyperpolarizing_step:trace_rmse: RMSE 0.654 mV vs tau 0.500 (recorded 0.654) OK
  - trace h/1 P08_rebound:trace_rmse: RMSE 0.681 mV vs tau 0.500 (recorded 0.681) OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 1.064 mV vs tau 0.500 (recorded 1.064) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 12.855 mV vs tau 1.009 (recorded 12.855) OK
  - trace h/2 P00_canonical:spike_timing: 4 spikes, max shift 1.071 ms vs tau 0.500 (recorded 1.071) OK
  - trace h/2 P02_weak_step:trace_rmse: RMSE 1.021 mV vs tau 0.500 (recorded 1.021) OK
  - trace h/2 P07_hyperpolarizing_step:trace_rmse: RMSE 0.654 mV vs tau 0.500 (recorded 0.654) OK
  - trace h/2 P08_rebound:trace_rmse: RMSE 0.681 mV vs tau 0.500 (recorded 0.681) OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 1.063 mV vs tau 0.500 (recorded 1.063) OK

### `m-shift_gate_midpoint-0bf496636d` (random20)

- model `traub2005_testseg2`, operator `shift_gate_midpoint`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 2 value(s) shifted +10 mV, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/km.channel.nml midpoint -20mV -> -10mV
  - diff: attribute neuroConstruct/generatedNeuroML2/km.channel.nml midpoint -43mV -> -33mV
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:adaptation_index: 0.0179369 -> 0.00382955, |diff| 0.01411 vs tau 0.01 OK
  - h/1 P00_canonical:last_isi: 7.59 -> 6.13, |diff| 1.46 vs tau 0.5 OK
  - h/1 P00_canonical:spike_count: 9 -> 10, |diff| 1 vs tau 0.5 OK; raw-trace count 9 -> 10
  - h/1 P04_step_2x:adaptation_index: 0.00486135 -> -0.0113167, |diff| 0.01618 vs tau 0.01 OK
  - h/1 P04_step_2x:last_isi: 25.63 -> 12.13, |diff| 13.5 vs tau 1.29 OK
  - h/1 P04_step_2x:spike_count: 18 -> 28, |diff| 10 vs tau 0.5 OK; raw-trace count 18 -> 28
  - h/1 P05_long_step:last_isi: 46.56 -> 27.7, |diff| 18.86 vs tau 2.61 OK
  - h/1 P05_long_step:spike_count: 42 -> 70, |diff| 28 vs tau 3 OK; raw-trace count 42 -> 70
  - h/1 P06_ramp:spike_count: 27 -> 41, |diff| 14 vs tau 3 OK; raw-trace count 27 -> 41
  - h/2 P00_canonical:adaptation_index: 0.0180201 -> 0.00406901, |diff| 0.01395 vs tau 0.01 OK
  - h/2 P00_canonical:last_isi: 7.61 -> 6.14, |diff| 1.47 vs tau 0.5 OK
  - h/2 P00_canonical:spike_count: 9 -> 10, |diff| 1 vs tau 0.5 OK; raw-trace count 9 -> 10
  - h/2 P04_step_2x:adaptation_index: 0.00495224 -> -0.0111253, |diff| 0.01608 vs tau 0.01 OK
  - h/2 P04_step_2x:last_isi: 26.06 -> 12.19, |diff| 13.87 vs tau 1.29 OK
  - h/2 P04_step_2x:spike_count: 18 -> 28, |diff| 10 vs tau 0.5 OK; raw-trace count 18 -> 28
  - h/2 P05_long_step:last_isi: 47.43 -> 27.67, |diff| 19.76 vs tau 2.61 OK
  - h/2 P05_long_step:spike_count: 41 -> 70, |diff| 29 vs tau 3 OK; raw-trace count 41 -> 70
  - h/2 P06_ramp:spike_count: 26 -> 41, |diff| 15 vs tau 3 OK; raw-trace count 26 -> 41
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 20.104 mV vs tau 4.390 (recorded 20.104) OK
  - trace h/1 P00_canonical:spike_count: raw spikes 9 -> 10 OK
  - trace h/1 P04_step_2x:spike_count: raw spikes 18 -> 28 OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 20.181 mV vs tau 4.390 (recorded 20.181) OK
  - trace h/2 P00_canonical:spike_count: raw spikes 9 -> 10 OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 18 -> 28 OK

### `m-shift_gate_midpoint-f1b7d12414` (random20)

- model `migliore2005_ca1_soma`, operator `shift_gate_midpoint`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 2 value(s) shifted +10 mV, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/nax.channel.nml midpoint -30mV -> -20mV
  - diff: attribute neuroConstruct/generatedNeuroML2/nax.channel.nml midpoint -30mV -> -20mV
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:ap_amplitude: 100.14 -> 93.2404, |diff| 6.9 vs tau 2.003 OK
  - h/1 P00_canonical:first_spike_latency: 5.42 -> 15.44, |diff| 10.02 vs tau 0.5 OK
  - h/1 P00_canonical:last_isi: 18.33 -> 30.16, |diff| 11.83 vs tau 0.5 OK
  - h/1 P00_canonical:spike_count: 3 -> 2, |diff| 1 vs tau 0.5 OK; raw-trace count 3 -> 2
  - h/1 P02_weak_step:steady_state_voltage: -65.0228 -> -65.9875, |diff| 0.9647 vs tau 0.5 OK
  - h/1 P03_rheobase:rheobase: 0.000580561 -> 0.00273205, |diff| 0.002151 vs tau 6.83e-05 OK
  - h/1 P04_step_2x:adaptation_index: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P04_step_2x:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P04_step_2x:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P04_step_2x:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P04_step_2x:last_isi: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P04_step_2x:spike_count: 13 -> 0, |diff| 13 vs tau 0.5 OK; raw-trace count 13 -> 0
  - h/1 P05_long_step:adaptation_index: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P05_long_step:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P05_long_step:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P05_long_step:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P05_long_step:last_isi: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P05_long_step:spike_count: 39 -> 0, |diff| 39 vs tau 0.5 OK; raw-trace count 39 -> 0
  - h/1 P06_ramp:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P06_ramp:spike_count: 16 -> 0, |diff| 16 vs tau 0.5 OK; raw-trace count 16 -> 0
  - h/1 P09_short_pulse:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P09_short_pulse:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P09_short_pulse:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P09_short_pulse:spike_count: 1 -> 0, |diff| 1 vs tau 0.5 OK; raw-trace count 1 -> 0
  - h/2 P00_canonical:ap_amplitude: 100.077 -> 93.1884, |diff| 6.888 vs tau 2.003 OK
  - h/2 P00_canonical:first_spike_latency: 5.41 -> 15.43, |diff| 10.02 vs tau 0.5 OK
  - h/2 P00_canonical:last_isi: 18.32 -> 30.16, |diff| 11.84 vs tau 0.5 OK
  - h/2 P00_canonical:spike_count: 3 -> 2, |diff| 1 vs tau 0.5 OK; raw-trace count 3 -> 2
  - h/2 P02_weak_step:steady_state_voltage: -65.0228 -> -65.9875, |diff| 0.9647 vs tau 0.5 OK
  - h/2 P03_rheobase:rheobase: 0.000580561 -> 0.00273205, |diff| 0.002151 vs tau 6.83e-05 OK
  - h/2 P04_step_2x:adaptation_index: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P04_step_2x:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P04_step_2x:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P04_step_2x:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P04_step_2x:last_isi: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P04_step_2x:spike_count: 13 -> 0, |diff| 13 vs tau 0.5 OK; raw-trace count 13 -> 0
  - h/2 P05_long_step:adaptation_index: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P05_long_step:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P05_long_step:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P05_long_step:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P05_long_step:last_isi: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P05_long_step:spike_count: 39 -> 0, |diff| 39 vs tau 0.5 OK; raw-trace count 39 -> 0
  - h/2 P06_ramp:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P06_ramp:spike_count: 16 -> 0, |diff| 16 vs tau 0.5 OK; raw-trace count 16 -> 0
  - h/2 P09_short_pulse:ahp_depth: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P09_short_pulse:ap_amplitude: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P09_short_pulse:first_spike_latency: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P09_short_pulse:spike_count: 1 -> 0, |diff| 1 vs tau 0.5 OK; raw-trace count 1 -> 0
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 24.753 mV vs tau 4.056 (recorded 24.753) OK
  - trace h/1 P00_canonical:spike_count: raw spikes 4 -> 2 OK
  - trace h/1 P02_weak_step:trace_rmse: RMSE 0.813 mV vs tau 0.500 (recorded 0.813) OK
  - trace h/1 P04_step_2x:trace_rmse: RMSE 11.882 mV vs tau 8.749 (recorded 11.882) OK
  - trace h/1 P04_step_2x:spike_count: raw spikes 13 -> 0 OK
  - trace h/1 P05_long_step:spike_count: raw spikes 39 -> 0 OK
  - trace h/1 P06_ramp:trace_rmse: RMSE 10.766 mV vs tau 6.268 (recorded 10.766) OK
  - trace h/1 P06_ramp:spike_count: raw spikes 16 -> 0 OK
  - trace h/1 P09_short_pulse:trace_rmse: RMSE 4.607 mV vs tau 1.226 (recorded 4.607) OK
  - trace h/1 P09_short_pulse:spike_count: raw spikes 1 -> 0 OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 24.738 mV vs tau 4.056 (recorded 24.738) OK
  - trace h/2 P00_canonical:spike_count: raw spikes 4 -> 2 OK
  - trace h/2 P02_weak_step:trace_rmse: RMSE 0.813 mV vs tau 0.500 (recorded 0.813) OK
  - trace h/2 P04_step_2x:trace_rmse: RMSE 11.838 mV vs tau 8.749 (recorded 11.838) OK
  - trace h/2 P04_step_2x:spike_count: raw spikes 13 -> 0 OK
  - trace h/2 P05_long_step:spike_count: raw spikes 39 -> 0 OK
  - trace h/2 P06_ramp:trace_rmse: RMSE 10.726 mV vs tau 6.268 (recorded 10.726) OK
  - trace h/2 P06_ramp:spike_count: raw spikes 16 -> 0 OK
  - trace h/2 P09_short_pulse:trace_rmse: RMSE 4.587 mV vs tau 1.226 (recorded 4.587) OK
  - trace h/2 P09_short_pulse:spike_count: raw spikes 1 -> 0 OK

### `m-shift_reversal-293fd11ac3` (random20)

- model `traub2005_testseg_all`, operator `shift_reversal`, assigned class `5_non_equivalent`
- **edit matches label: yes**: 1 value(s) shifted -5 mV, nothing else changed
  - diff: attribute neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml erev 50.0 mV -> 45.0 mV
- **class re-derived: `5_non_equivalent`** (matches)
- **detections recomputed: yes**
  - h/1 P00_canonical:adaptation_index: definedness defined vs not_applicable (mismatch counts as detection)
  - h/1 P00_canonical:last_isi: 23.7 -> 7.61, |diff| 16.09 vs tau 0.5 OK
  - h/1 P00_canonical:spike_count: 4 -> 3, |diff| 1 vs tau 0.5 OK; raw-trace count 4 -> 3
  - h/1 P05_long_step:first_spike_latency: 42.89 -> 43.83, |diff| 0.94 vs tau 0.8578 OK
  - h/2 P00_canonical:adaptation_index: definedness defined vs not_applicable (mismatch counts as detection)
  - h/2 P00_canonical:last_isi: 23.72 -> 7.61, |diff| 16.11 vs tau 0.5 OK
  - h/2 P00_canonical:spike_count: 4 -> 3, |diff| 1 vs tau 0.5 OK; raw-trace count 4 -> 3
  - h/2 P05_long_step:first_spike_latency: 42.82 -> 43.76, |diff| 0.94 vs tau 0.8578 OK
- **full-trace detections recomputed from raw traces: yes**
  - trace h/1 P00_canonical:trace_rmse: RMSE 13.125 mV vs tau 1.009 (recorded 13.125) OK
  - trace h/1 P00_canonical:spike_timing: 4 spikes, max shift 2.773 ms vs tau 0.500 (recorded 2.773) OK
  - trace h/2 P00_canonical:trace_rmse: RMSE 13.134 mV vs tau 1.009 (recorded 13.134) OK
  - trace h/2 P00_canonical:spike_timing: 4 spikes, max shift 2.778 ms vs tau 0.500 (recorded 2.778) OK

### `m-solver_config-c16c7918b3` (random20)

- model `bbp2015_soma`, operator `solver_config`, assigned class `4_equivalent_within_tested_domain`
- **edit matches label: yes**: integrator eulertree set in harness Meta and probe override
  - diff: element_added NMC/NeuroML2/LEMS_Soma_AllNML2.xml   ->
- **class re-derived: `4_equivalent_within_tested_domain`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: n/a (no trace detections)**

### `m-wrong_channel-36578b9f51` (random20)

- model `hay2011_soma`, operator `wrong_channel`, assigned class `2_non_executable`
- **edit matches label: yes**: ionChannel Ca_LVAst -> pas; target channel is defined in the model files
  - diff: attribute neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml ionChannel Ca_LVAst -> pas
- **class re-derived: `2_non_executable`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: n/a (no trace detections)**

### `m-wrong_compatible_component-0638e400a0` (random20)

- model `migliore2005_ca1_soma`, operator `wrong_compatible_component`, assigned class `3_numerically_unstable`
- **edit matches label: yes**: ionChannel kdr -> kap; target channel is defined in the model files
  - diff: attribute neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml ionChannel kdr -> kap
- **class re-derived: `3_numerically_unstable`** (matches)
- **detections recomputed: n/a (no detections)**
- **full-trace detections recomputed from raw traces: n/a (no trace detections)**

