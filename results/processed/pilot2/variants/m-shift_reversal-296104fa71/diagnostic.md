# m-shift_reversal-296104fa71

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "-80.0 mV", "old": "-70.0 mV"}], "element": "channelDensity", "element_id": "LeakConductance_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "erev", "old": "-70.0 mV", "new": "-80.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1397.804 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.0 | None |  | 0.01 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | ahp_depth | definedness | -4.832305908199814 | None |  | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | ap_amplitude | definedness | 87.45660400498362 | None |  | 1.74913 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | first_spike_latency | definedness | 17.199999999856516 | None |  | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | last_isi | definedness | 20.21999999998161 | None |  | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 0.0 | 20 | 0.5 | `r-4cceac4cec0eb866659f` | `r-2efd7faf9e7ad0b0269c` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.91402953033431 | -70.91663496704085 | 10.0026 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.595895089133256 | 0.211598 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-5c2fd06b8d08dac27de0` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | 4.6017837524567256 | 9.21469 | 1.51774 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 15.679999999857898 | 7.67 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 16.539999999984957 | 6 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P04_step_2x | spike_count | exceeds | 47.0 | 30.0 | 17 | 3 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P05_long_step | adaptation_index | definedness | 2.5632810906290527e-06 | None |  | 0.01 | `r-d95212df9ca6b2b4efff` | `r-04959c0d6787b6845ea6` |
| h/1 | P05_long_step | ahp_depth | definedness | -5.324134826653506 | None |  | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-04959c0d6787b6845ea6` |
| h/1 | P05_long_step | ap_amplitude | definedness | 87.90636062789724 | None |  | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-04959c0d6787b6845ea6` |
| h/1 | P05_long_step | first_spike_latency | definedness | 12.669999999860636 | None |  | 0.5 | `r-d95212df9ca6b2b4efff` | `r-04959c0d6787b6845ea6` |
| h/1 | P05_long_step | last_isi | definedness | 15.610000000340733 | None |  | 0.5 | `r-d95212df9ca6b2b4efff` | `r-04959c0d6787b6845ea6` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 0.0 | 128 | 3 | `r-d95212df9ca6b2b4efff` | `r-04959c0d6787b6845ea6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 363.4899999995416 | 546.9799999993747 | 183.49 | 7.2698 | `r-5888f8cf54a64bb2eb2f` | `r-b242292e4d40eef1fa8d` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 36.0 | 25 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-b242292e4d40eef1fa8d` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -88.16673006286652 | -98.16673006286652 | 10 | 0.5 | `r-54e05e4e4388308e9268` | `r-784aab310d80ae66255a` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | 0.00379180908203125 | 3.47003 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-9fd6bc7ce5f7076e4870` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 118.24569702145673 | 128.1719284055948 | 9.92623 | 2.36491 | `r-534f36c941e5711ea7a5` | `r-9fd6bc7ce5f7076e4870` |
| h/2 | P00_canonical | adaptation_index | definedness | -1.4563884479268312e-05 | None |  | 0.01 | `r-c9243a4c0b8a67de36a8` | `r-ec08ca0d3977149e48f9` |
| h/2 | P00_canonical | ahp_depth | definedness | -4.734680175792306 | None |  | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-ec08ca0d3977149e48f9` |
| h/2 | P00_canonical | ap_amplitude | definedness | 87.36877822947855 | None |  | 1.74913 | `r-c9243a4c0b8a67de36a8` | `r-ec08ca0d3977149e48f9` |
| h/2 | P00_canonical | first_spike_latency | definedness | 17.189999999856525 | None |  | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-ec08ca0d3977149e48f9` |
| h/2 | P00_canonical | last_isi | definedness | 20.189999999981637 | None |  | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-ec08ca0d3977149e48f9` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 0.0 | 20 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-ec08ca0d3977149e48f9` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -60.91402884902938 | -70.91663428649886 | 10.0026 | 0.5 | `r-e087238cb438e653e31d` | `r-5ceada61b1e86c945488` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.595895089133256 | 0.211598 | 0.00768595 | `s-a5d560731591d7405a9c` | `s-809417d72345708e8e01` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | 5.097526550296465 | 9.20452 | 1.51774 | `r-e087238cb438e653e31d` | `r-5ceada61b1e86c945488` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.989999999864892 | 15.649999999857926 | 7.66 | 0.5 | `r-e087238cb438e653e31d` | `r-5ceada61b1e86c945488` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 16.399999999985084 | 5.96 | 0.5 | `r-e087238cb438e653e31d` | `r-5ceada61b1e86c945488` |
| h/2 | P04_step_2x | spike_count | exceeds | 48.0 | 30.0 | 18 | 3 | `r-e087238cb438e653e31d` | `r-5ceada61b1e86c945488` |
| h/2 | P05_long_step | adaptation_index | definedness | 9.022764855517059e-14 | None |  | 0.01 | `r-880359fc85650f897997` | `r-040f7e3668b03d317614` |
| h/2 | P05_long_step | ahp_depth | definedness | -4.827239990238667 | None |  | 1.49068 | `r-880359fc85650f897997` | `r-040f7e3668b03d317614` |
| h/2 | P05_long_step | ap_amplitude | definedness | 87.76913070748881 | None |  | 1.75813 | `r-880359fc85650f897997` | `r-040f7e3668b03d317614` |
| h/2 | P05_long_step | first_spike_latency | definedness | 12.629999999860672 | None |  | 0.5 | `r-880359fc85650f897997` | `r-040f7e3668b03d317614` |
| h/2 | P05_long_step | last_isi | definedness | 15.480000000337895 | None |  | 0.5 | `r-880359fc85650f897997` | `r-040f7e3668b03d317614` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 0.0 | 129 | 3 | `r-880359fc85650f897997` | `r-040f7e3668b03d317614` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 363.43999999954167 | 546.9299999993748 | 183.49 | 7.2698 | `r-b0adc3019253aae3e3e8` | `r-34e36e0439d24fee56b9` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 37.0 | 24 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-34e36e0439d24fee56b9` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -88.16673142547639 | -98.16673142700226 | 10 | 0.5 | `r-e087238cb438e653e31d` | `r-5ceada61b1e86c945488` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | 0.00420379638671875 | 4.03814 | 1.70556 | `r-84e85309a66928a29934` | `r-4686ae912af77dc6f895` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 118.07249069170416 | 127.99415969793048 | 9.92167 | 2.36491 | `r-84e85309a66928a29934` | `r-4686ae912af77dc6f895` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
