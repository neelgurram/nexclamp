# m-shift_reversal-513c92c08b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "new": "-56.0 mV", "old": "-66.0 mV"}], "element": "channelDensity", "element_id": "LeakConductance_pyr_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "attribute": "erev", "old": "-66.0 mV", "new": "-56.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 576.856 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.0038040393524786894 | 0.0874117 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-4a4869cebde203d1d89a` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | -1.3443191201346423 | 5.70277 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-4a4869cebde203d1d89a` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 97.40631103504982 | 2.6427 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-4a4869cebde203d1d89a` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 34.890000000016755 | 2.25 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-4a4869cebde203d1d89a` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 67.29999999993885 | 9.59 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-4a4869cebde203d1d89a` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 2.0 | 2 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-9cd54835ebb831e0d45e` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0 | 0.0076156 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-b972516c88eb222ce888` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 26.52999999984803 | 1.12 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-9cd54835ebb831e0d45e` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 311.71999999971655 | 139.4 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-9cd54835ebb831e0d45e` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 331.5099999996985 | 255.38 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-a7891c90cb10f9ebcdfc` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 6.0 | 2 | 0.5 | `r-f6700284baa99a5ef41f` | `r-a7891c90cb10f9ebcdfc` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 106.62999999977518 | 394.51 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-1e2136cd545de1dad40e` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-1e2136cd545de1dad40e` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424023132327 | -64.06190358276368 | 6.75234 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-9cd54835ebb831e0d45e` |
| h/1 | P08_rebound | first_spike_latency | definedness | None | 21.159999999398224 |  | inf | `r-2d208cbc545dcf997d15` | `r-91c3a22f66f5ccbdfd59` |
| h/1 | P08_rebound | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-2d208cbc545dcf997d15` | `r-91c3a22f66f5ccbdfd59` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.0030553682454783197 | 0.0869973 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-ca4db41ab1835932f008` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | -1.3477965327670631 | 5.69315 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-ca4db41ab1835932f008` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 97.221569061033 | 2.65746 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-ca4db41ab1835932f008` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 32.6300000000156 | 34.870000000016745 | 2.24 | 0.6528 | `r-2526a9bbad7e1faa361e` | `r-ca4db41ab1835932f008` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 67.0199999999391 | 9.57 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-ca4db41ab1835932f008` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 2.0 | 2 | 0.5 | `r-16be743cbc8f0485fd82` | `r-b120d102421e4bb29187` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0 | 0.0076156 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-657d7c25c64cfe29df49` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 26.109999999848412 | 0.75 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-b120d102421e4bb29187` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 310.7899999997174 | 139.39 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-b120d102421e4bb29187` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 36.3499999998391 | 0.76 | 0.7434 | `r-493fa57e11933a720397` | `r-9759e49c30d1be3e3886` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 330.6099999996993 | 255.36 | 11.7378 | `r-493fa57e11933a720397` | `r-9759e49c30d1be3e3886` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 6.0 | 2 | 0.5 | `r-493fa57e11933a720397` | `r-9759e49c30d1be3e3886` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 105.81999999977592 | 395.24 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-fa45ce5a7d02b544ca96` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-fa45ce5a7d02b544ca96` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424049987795 | -64.06182834167481 | 6.75241 | 0.5 | `r-16be743cbc8f0485fd82` | `r-b120d102421e4bb29187` |
| h/2 | P08_rebound | first_spike_latency | definedness | None | 21.10999999939827 |  | inf | `r-9a4410c4bbb6d01c1bee` | `r-8be932858b6c6d630b9d` |
| h/2 | P08_rebound | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-9a4410c4bbb6d01c1bee` | `r-8be932858b6c6d630b9d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
