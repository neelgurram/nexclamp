# m-shift_reversal-2c628fb0f6

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "new": "-61.0 mV", "old": "-66.0 mV"}], "element": "channelDensity", "element_id": "LeakConductance_pyr_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "attribute": "erev", "old": "-66.0 mV", "new": "-61.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1495.592 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.013803017073637663 | 0.0974107 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | -0.615015553065831 | 6.43207 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 97.19705963123461 | 2.85196 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 35.41000000001702 | 2.77 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 71.91999999993465 | 4.97 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-a2a47d0560066a50aee0` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -69.32851186372204 | 3.11487 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0025271497848507614 | 0.00508845 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-5dd600ac3c198b3ab039` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -5.050780899047098 | 1.96875 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 68.08999999981023 | 42.68 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 361.3599999996714 | 89.76 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P05_long_step | ahp_depth | exceeds | -7.059071324666348 | -5.08797419738724 | 1.9711 | 0.5 | `r-f6700284baa99a5ef41f` | `r-33802259fdf4ebeb0ff1` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 100.34999999978089 | 63.18 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-33802259fdf4ebeb0ff1` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 392.22999999964327 | 194.66 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-33802259fdf4ebeb0ff1` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-f6700284baa99a5ef41f` | `r-33802259fdf4ebeb0ff1` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 210.56999999968065 | 290.57 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-8c27f3a2840f4439e847` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-8c27f3a2840f4439e847` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424023132327 | -67.20566532897952 | 3.60857 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-dc905c17af1e27b88607` |
| h/1 | P08_rebound | first_spike_latency | definedness | None | 50.74999999937131 |  | inf | `r-2d208cbc545dcf997d15` | `r-68ca7cfdd63afceef5f0` |
| h/1 | P08_rebound | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-2d208cbc545dcf997d15` | `r-68ca7cfdd63afceef5f0` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.013479627216693277 | 0.0974216 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-bed3817d91c9b8c6e9e4` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | -0.6163664899551407 | 6.42458 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-bed3817d91c9b8c6e9e4` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 96.97681808437832 | 2.90221 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-bed3817d91c9b8c6e9e4` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 32.6300000000156 | 35.39000000001701 | 2.76 | 0.6528 | `r-2526a9bbad7e1faa361e` | `r-bed3817d91c9b8c6e9e4` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 71.62999999993491 | 4.96 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-bed3817d91c9b8c6e9e4` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-16be743cbc8f0485fd82` | `r-14bd4cb4aac631f574ae` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -69.2759501464975 | 3.06231 | 0.5 | `r-16be743cbc8f0485fd82` | `r-14bd4cb4aac631f574ae` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0025271497848507614 | 0.00508845 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-0e004d14d58891327bcd` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -7.016957875569673 | -5.071442481994168 | 1.94552 | 0.5 | `r-16be743cbc8f0485fd82` | `r-14bd4cb4aac631f574ae` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 67.03999999981119 | 41.68 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-14bd4cb4aac631f574ae` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 360.42999999967225 | 89.75 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-14bd4cb4aac631f574ae` |
| h/2 | P05_long_step | ahp_depth | exceeds | -7.056752797444673 | -5.108872291564481 | 1.94788 | 0.5 | `r-493fa57e11933a720397` | `r-d1feda6b709b7e47c6a3` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 99.20999999978193 | 62.1 | 0.7434 | `r-493fa57e11933a720397` | `r-d1feda6b709b7e47c6a3` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 391.3299999996441 | 194.64 | 11.7378 | `r-493fa57e11933a720397` | `r-d1feda6b709b7e47c6a3` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-493fa57e11933a720397` | `r-d1feda6b709b7e47c6a3` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 209.91999999968124 | 291.14 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-4f80128d62dead424bc0` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-4f80128d62dead424bc0` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424049987795 | -67.20561691131594 | 3.60862 | 0.5 | `r-16be743cbc8f0485fd82` | `r-14bd4cb4aac631f574ae` |
| h/2 | P08_rebound | first_spike_latency | definedness | None | 50.689999999371366 |  | inf | `r-9a4410c4bbb6d01c1bee` | `r-9781c1ea561910401d14` |
| h/2 | P08_rebound | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-9a4410c4bbb6d01c1bee` | `r-9781c1ea561910401d14` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
