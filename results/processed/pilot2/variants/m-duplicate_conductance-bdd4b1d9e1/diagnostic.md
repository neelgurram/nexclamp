# m-duplicate_conductance-bdd4b1d9e1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "Kdr_pyr_soma_group_dup", "source_id": "Kdr_pyr_soma_group"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kdr_pyr_soma_group_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"80.0 mS_per_cm2\" id=\"Kdr_pyr_soma_group_dup\" ionChannel=\"Kdr_pyr\" segmentGroup=\"soma_group\" ion=\"k\" erev=\"-75.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1831.071 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | 0.05605949617069592 | 0.0275482 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-3acc6d26320bf94ac166` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | -6.343875743321021 | 0.703214 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-3acc6d26320bf94ac166` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 95.11141967739803 | 4.9376 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-3acc6d26320bf94ac166` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 56.749999999948386 | 20.14 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-3acc6d26320bf94ac166` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 11.0 | 3 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-3acc6d26320bf94ac166` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -67.06746202697752 | 0.853817 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-3a4614e30cf1c7b265d2` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.016392322928761697 | 0.00877672 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-7c519fa8cc32d3a812b3` |
| h/1 | P04_step_2x | ahp_depth | definedness | -7.019535802205411 | None |  | 0.5 | `r-85c49aecb0e07f4c5069` | `r-3a4614e30cf1c7b265d2` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 98.06893539575677 | None |  | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-3a4614e30cf1c7b265d2` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 25.40999999984905 | None |  | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-3a4614e30cf1c7b265d2` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-3a4614e30cf1c7b265d2` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-3a4614e30cf1c7b265d2` |
| h/1 | P05_long_step | adaptation_index | definedness | -8.519410542851502e-06 | None |  | 0.01 | `r-f6700284baa99a5ef41f` | `r-61ce1168e07b09c9ea20` |
| h/1 | P05_long_step | ahp_depth | definedness | -7.059071324666348 | None |  | 0.5 | `r-f6700284baa99a5ef41f` | `r-61ce1168e07b09c9ea20` |
| h/1 | P05_long_step | ap_amplitude | definedness | 98.06814575218911 | None |  | 1.96136 | `r-f6700284baa99a5ef41f` | `r-61ce1168e07b09c9ea20` |
| h/1 | P05_long_step | first_spike_latency | definedness | 37.16999999983835 | None |  | 0.7434 | `r-f6700284baa99a5ef41f` | `r-61ce1168e07b09c9ea20` |
| h/1 | P05_long_step | last_isi | definedness | 586.8900000005651 | None |  | 11.7378 | `r-f6700284baa99a5ef41f` | `r-61ce1168e07b09c9ea20` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 0.0 | 4 | 0.5 | `r-f6700284baa99a5ef41f` | `r-61ce1168e07b09c9ea20` |
| h/1 | P06_ramp | first_spike_latency | definedness | 501.13999999941643 | None |  | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-475c39f9fc77f29731ef` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-475c39f9fc77f29731ef` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | 0.05590439159657014 | 0.0280375 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-f8d50c7c971a467b94c0` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | -6.338252683367045 | 0.702689 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-f8d50c7c971a467b94c0` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 94.82928848232277 | 5.04974 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-f8d50c7c971a467b94c0` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 56.46999999994864 | 20.12 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-f8d50c7c971a467b94c0` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 11.0 | 3 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-f8d50c7c971a467b94c0` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -67.06746165771483 | 0.853818 | 0.5 | `r-16be743cbc8f0485fd82` | `r-f7d6311036d9f9ccf9db` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.016392322928761697 | 0.00877672 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-11cf26b2b8dfa49301c5` |
| h/2 | P04_step_2x | ahp_depth | definedness | -7.016957875569673 | None |  | 0.5 | `r-16be743cbc8f0485fd82` | `r-f7d6311036d9f9ccf9db` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 97.6356582663006 | None |  | 1.96138 | `r-16be743cbc8f0485fd82` | `r-f7d6311036d9f9ccf9db` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 25.359999999849094 | None |  | 0.5082 | `r-16be743cbc8f0485fd82` | `r-f7d6311036d9f9ccf9db` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-f7d6311036d9f9ccf9db` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-16be743cbc8f0485fd82` | `r-f7d6311036d9f9ccf9db` |
| h/2 | P05_long_step | adaptation_index | definedness | -8.532786352377084e-06 | None |  | 0.01 | `r-493fa57e11933a720397` | `r-fc88d2d98d2a41a99a58` |
| h/2 | P05_long_step | ahp_depth | definedness | -7.056752797444673 | None |  | 0.5 | `r-493fa57e11933a720397` | `r-fc88d2d98d2a41a99a58` |
| h/2 | P05_long_step | ap_amplitude | definedness | 97.55448913585151 | None |  | 1.96136 | `r-493fa57e11933a720397` | `r-fc88d2d98d2a41a99a58` |
| h/2 | P05_long_step | first_spike_latency | definedness | 37.10999999983841 | None |  | 0.7434 | `r-493fa57e11933a720397` | `r-fc88d2d98d2a41a99a58` |
| h/2 | P05_long_step | last_isi | definedness | 585.9700000005014 | None |  | 11.7378 | `r-493fa57e11933a720397` | `r-fc88d2d98d2a41a99a58` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 0.0 | 4 | 0.5 | `r-493fa57e11933a720397` | `r-fc88d2d98d2a41a99a58` |
| h/2 | P06_ramp | first_spike_latency | definedness | 501.0599999994165 | None |  | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-15c3e69a5a860938b21e` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-15c3e69a5a860938b21e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
