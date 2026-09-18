# m-wrong_compatible_component-a38cf2a7ad

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kdr_pyr_soma_group']", "new": "Kahp_pyr", "old": "Kdr_pyr"}], "element_id": "Kdr_pyr_soma_group", "generator_seed": 20260917, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kdr_pyr_soma_group']", "attribute": "ionChannel", "old": "Kdr_pyr", "new": "Kahp_pyr", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1383.97 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.08360766405035329 | None |  | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-09eac888c78ef5db401b` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | -2.464311458042701 | 4.58278 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-09eac888c78ef5db401b` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 9.62487030012003 | 90.4241 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-09eac888c78ef5db401b` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 36.56000000001761 | 3.92 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-09eac888c78ef5db401b` |
| h/1 | P00_canonical | last_isi | definedness | 76.88999999993013 | None |  | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-09eac888c78ef5db401b` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 1.0 | 7 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-09eac888c78ef5db401b` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -72.54793266448974 | 6.33429 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.08196161464380848 | 0.074346 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-cd5de485ab64bb7638f9` |
| h/1 | P04_step_2x | ahp_depth | definedness | -7.019535802205411 | None |  | 0.5 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 98.06893539575677 | None |  | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 25.40999999984905 | None |  | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/1 | P05_long_step | adaptation_index | definedness | -8.519410542851502e-06 | None |  | 0.01 | `r-f6700284baa99a5ef41f` | `r-fc9c0ae7a45abe0f210d` |
| h/1 | P05_long_step | ahp_depth | definedness | -7.059071324666348 | None |  | 0.5 | `r-f6700284baa99a5ef41f` | `r-fc9c0ae7a45abe0f210d` |
| h/1 | P05_long_step | ap_amplitude | definedness | 98.06814575218911 | None |  | 1.96136 | `r-f6700284baa99a5ef41f` | `r-fc9c0ae7a45abe0f210d` |
| h/1 | P05_long_step | first_spike_latency | definedness | 37.16999999983835 | None |  | 0.7434 | `r-f6700284baa99a5ef41f` | `r-fc9c0ae7a45abe0f210d` |
| h/1 | P05_long_step | last_isi | definedness | 586.8900000005651 | None |  | 11.7378 | `r-f6700284baa99a5ef41f` | `r-fc9c0ae7a45abe0f210d` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 0.0 | 4 | 0.5 | `r-f6700284baa99a5ef41f` | `r-fc9c0ae7a45abe0f210d` |
| h/1 | P06_ramp | first_spike_latency | definedness | 501.13999999941643 | None |  | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-71e70060823d34949d11` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-71e70060823d34949d11` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424023132327 | -73.78377530975344 | 2.96954 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-f06a9b613e7652b70659` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.08394194146984126 | None |  | 0.01 | `r-2526a9bbad7e1faa361e` | `r-de05b67705f380a9ce94` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | -2.464228036063062 | 4.57671 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-de05b67705f380a9ce94` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 9.554019927803616 | 90.325 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-de05b67705f380a9ce94` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 32.6300000000156 | 36.550000000017604 | 3.92 | 0.6528 | `r-2526a9bbad7e1faa361e` | `r-de05b67705f380a9ce94` |
| h/2 | P00_canonical | last_isi | definedness | 76.5899999999304 | None |  | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-de05b67705f380a9ce94` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 1.0 | 7 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-de05b67705f380a9ce94` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -72.54793255920409 | 6.33429 | 0.5 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.08196161464380848 | 0.074346 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-fe8f72fb4480ceb857f1` |
| h/2 | P04_step_2x | ahp_depth | definedness | -7.016957875569673 | None |  | 0.5 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 97.6356582663006 | None |  | 1.96138 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 25.359999999849094 | None |  | 0.5082 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |
| h/2 | P05_long_step | adaptation_index | definedness | -8.532786352377084e-06 | None |  | 0.01 | `r-493fa57e11933a720397` | `r-0dc46095b2e0f4e44b62` |
| h/2 | P05_long_step | ahp_depth | definedness | -7.056752797444673 | None |  | 0.5 | `r-493fa57e11933a720397` | `r-0dc46095b2e0f4e44b62` |
| h/2 | P05_long_step | ap_amplitude | definedness | 97.55448913585151 | None |  | 1.96136 | `r-493fa57e11933a720397` | `r-0dc46095b2e0f4e44b62` |
| h/2 | P05_long_step | first_spike_latency | definedness | 37.10999999983841 | None |  | 0.7434 | `r-493fa57e11933a720397` | `r-0dc46095b2e0f4e44b62` |
| h/2 | P05_long_step | last_isi | definedness | 585.9700000005014 | None |  | 11.7378 | `r-493fa57e11933a720397` | `r-0dc46095b2e0f4e44b62` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 0.0 | 4 | 0.5 | `r-493fa57e11933a720397` | `r-0dc46095b2e0f4e44b62` |
| h/2 | P06_ramp | first_spike_latency | definedness | 501.0599999994165 | None |  | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-6f260b17e121575d2217` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-6f260b17e121575d2217` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424049987795 | -73.78377554016116 | 2.96954 | 0.5 | `r-16be743cbc8f0485fd82` | `r-284d8f17504a46d0f1bd` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
