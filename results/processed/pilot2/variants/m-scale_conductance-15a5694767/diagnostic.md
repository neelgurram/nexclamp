# m-scale_conductance-15a5694767

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_pyr_soma_group']", "new": "96.0 mS_per_cm2", "old": "120.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Na_pyr_soma_group", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_pyr_soma_group']", "attribute": "condDensity", "old": "120.0 mS_per_cm2", "new": "96.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1482.178 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 96.38759231545106 | 3.66142 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-ba5ebf2c70d08e6d878f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.009937845775561779 | 0.00232225 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-3671158570d9279efaf0` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 98.06893539575677 | 94.3179626488064 | 3.75097 | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-6dc406f1fda17a3970d6` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 31.36999999984363 | 5.96 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-6dc406f1fda17a3970d6` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-6dc406f1fda17a3970d6` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-6dc406f1fda17a3970d6` |
| h/1 | P05_long_step | adaptation_index | definedness | -8.519410542851502e-06 | None |  | 0.01 | `r-f6700284baa99a5ef41f` | `r-863c3d9774e0a62d793d` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 98.06814575218911 | 94.19318390079698 | 3.87496 | 1.96136 | `r-f6700284baa99a5ef41f` | `r-863c3d9774e0a62d793d` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 53.89999999982314 | 16.73 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-863c3d9774e0a62d793d` |
| h/1 | P05_long_step | last_isi | definedness | 586.8900000005651 | None |  | 11.7378 | `r-f6700284baa99a5ef41f` | `r-863c3d9774e0a62d793d` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 1.0 | 3 | 0.5 | `r-f6700284baa99a5ef41f` | `r-863c3d9774e0a62d793d` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 691.889999999243 | 190.75 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-c0de12fddd2bd743795c` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-c0de12fddd2bd743795c` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 96.18842697122393 | 3.6906 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-539fdd9e605c979bdec6` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.009937845775561779 | 0.00232225 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-708bba3c380236b3f70e` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 97.6356582663006 | 93.81272125295516 | 3.82294 | 1.96138 | `r-16be743cbc8f0485fd82` | `r-4fbf9adbd0518ad1278d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 31.309999999843683 | 5.95 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-4fbf9adbd0518ad1278d` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-4fbf9adbd0518ad1278d` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-16be743cbc8f0485fd82` | `r-4fbf9adbd0518ad1278d` |
| h/2 | P05_long_step | adaptation_index | definedness | -8.532786352377084e-06 | None |  | 0.01 | `r-493fa57e11933a720397` | `r-a2b160546175a6ecd619` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 97.55448913585151 | 93.72512817561869 | 3.82936 | 1.96136 | `r-493fa57e11933a720397` | `r-a2b160546175a6ecd619` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 53.8299999998232 | 16.72 | 0.7434 | `r-493fa57e11933a720397` | `r-a2b160546175a6ecd619` |
| h/2 | P05_long_step | last_isi | definedness | 585.9700000005014 | None |  | 11.7378 | `r-493fa57e11933a720397` | `r-a2b160546175a6ecd619` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 1.0 | 3 | 0.5 | `r-493fa57e11933a720397` | `r-a2b160546175a6ecd619` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 691.799999999243 | 190.74 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-955de6e3c4193b290401` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-955de6e3c4193b290401` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
