# m-scale_conductance-2dc7e425d7

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ca_pyr_soma_group']", "new": "20.0 mS_per_cm2", "old": "10.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Ca_pyr_soma_group", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ca_pyr_soma_group']", "attribute": "condDensity", "old": "10.0 mS_per_cm2", "new": "20.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1416.901 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.002924664672067675 | 0.0865323 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-5930454d481e53940212` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 148.29999999986518 | 71.41 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-5930454d481e53940212` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 4.0 | 4 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-5930454d481e53940212` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -67.17584812622069 | 0.962204 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-43bfb2e52ad234532b8e` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.010450105867085582 | 0.00283451 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-02e49cab2bc44fd815d9` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -6.265901781717943 | 0.753634 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-43bfb2e52ad234532b8e` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 32.58999999984252 | 7.18 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-43bfb2e52ad234532b8e` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-43bfb2e52ad234532b8e` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-43bfb2e52ad234532b8e` |
| h/1 | P05_long_step | adaptation_index | definedness | -8.519410542851502e-06 | None |  | 0.01 | `r-f6700284baa99a5ef41f` | `r-5c7252a122a3efd754f0` |
| h/1 | P05_long_step | ahp_depth | exceeds | -7.059071324666348 | -6.304720141092943 | 0.754351 | 0.5 | `r-f6700284baa99a5ef41f` | `r-5c7252a122a3efd754f0` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 58.56999999981889 | 21.4 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-5c7252a122a3efd754f0` |
| h/1 | P05_long_step | last_isi | definedness | 586.8900000005651 | None |  | 11.7378 | `r-f6700284baa99a5ef41f` | `r-5c7252a122a3efd754f0` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 1.0 | 3 | 0.5 | `r-f6700284baa99a5ef41f` | `r-5c7252a122a3efd754f0` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 972.9699999989873 | 471.83 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-961e77a44163320f453b` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-961e77a44163320f453b` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.0030321406913279805 | 0.0869741 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-e98d1a626d036379099e` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 147.9599999998655 | 71.37 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-e98d1a626d036379099e` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 4.0 | 4 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-e98d1a626d036379099e` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -67.17584783325194 | 0.962204 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2493dc2c5a977c0f843e` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.010450105867085582 | 0.00283451 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-220cb68968522d633e71` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -7.016957875569673 | -6.26378640238444 | 0.753171 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2493dc2c5a977c0f843e` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 32.52999999984257 | 7.17 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-2493dc2c5a977c0f843e` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-2493dc2c5a977c0f843e` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2493dc2c5a977c0f843e` |
| h/2 | P05_long_step | adaptation_index | definedness | -8.532786352377084e-06 | None |  | 0.01 | `r-493fa57e11933a720397` | `r-a01083ba7f4ad57483ac` |
| h/2 | P05_long_step | ahp_depth | exceeds | -7.056752797444673 | -6.302826014200846 | 0.753927 | 0.5 | `r-493fa57e11933a720397` | `r-a01083ba7f4ad57483ac` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 58.48999999981896 | 21.38 | 0.7434 | `r-493fa57e11933a720397` | `r-a01083ba7f4ad57483ac` |
| h/2 | P05_long_step | last_isi | definedness | 585.9700000005014 | None |  | 11.7378 | `r-493fa57e11933a720397` | `r-a01083ba7f4ad57483ac` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 1.0 | 3 | 0.5 | `r-493fa57e11933a720397` | `r-a01083ba7f4ad57483ac` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 972.8599999989874 | 471.8 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-28570166f27e855eeaaf` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-28570166f27e855eeaaf` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
