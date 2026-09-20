# m-scale_conductance-de26f4d2e1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "new": "0.1666666 mS_per_cm2", "old": "0.0833333 mS_per_cm2"}], "element": "channelDensity", "element_id": "pas_ModelViewParmSubset_1", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "attribute": "condDensity", "old": "0.0833333 mS_per_cm2", "new": "0.1666666 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1796.093 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 19.46000000000072 | 3.88 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-b963c182c883b7f60e0a` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -59.772974020385696 | 1.3234 | 0.5 | `r-007bacc26e9c06940666` | `r-3d46c0f1b5b7429bd43f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.04033194453930743 | 0.015641 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-40cc0153573d58a447dd` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.0076978106032479145 | 0.021293179805137084 | 0.0135954 | 0.01 | `r-007bacc26e9c06940666` | `r-3d46c0f1b5b7429bd43f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 27.809999999846866 | 8.61 | 0.5 | `r-007bacc26e9c06940666` | `r-3d46c0f1b5b7429bd43f` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 144.12999999986891 | 64.6 | 1.5906 | `r-007bacc26e9c06940666` | `r-3d46c0f1b5b7429bd43f` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 4.0 | 3 | 0.5 | `r-007bacc26e9c06940666` | `r-3d46c0f1b5b7429bd43f` |
| h/1 | P05_long_step | adaptation_index | definedness | 0.005414466597953451 | None |  | 0.01 | `r-2e016fe90119b688bc84` | `r-151657a1d30cfdb58553` |
| h/1 | P05_long_step | ahp_depth | definedness | -14.216171264648949 | None |  | 0.710809 | `r-2e016fe90119b688bc84` | `r-151657a1d30cfdb58553` |
| h/1 | P05_long_step | ap_amplitude | definedness | 84.2643203750593 | None |  | 1.68529 | `r-2e016fe90119b688bc84` | `r-151657a1d30cfdb58553` |
| h/1 | P05_long_step | first_spike_latency | definedness | 27.809999999846866 | None |  | 0.5562 | `r-2e016fe90119b688bc84` | `r-151657a1d30cfdb58553` |
| h/1 | P05_long_step | last_isi | definedness | 112.64000000245869 | None |  | 2.2528 | `r-2e016fe90119b688bc84` | `r-151657a1d30cfdb58553` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 0.0 | 19 | 0.5 | `r-2e016fe90119b688bc84` | `r-151657a1d30cfdb58553` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 620.419999999308 | 219.69 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-4de5fbcdc7899e8bf075` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 5.0 | 4 | 0.5 | `r-0cd5f319bb80295395e1` | `r-4de5fbcdc7899e8bf075` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -81.01395223693858 | -71.92813785858165 | 9.08581 | 0.5 | `r-007bacc26e9c06940666` | `r-3d46c0f1b5b7429bd43f` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -16.79777735900879 | 1.10823 | 0.8953 | `r-35777975476ff8854a8b` | `r-60839140814628eb473c` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 19.390000000000732 | 3.87 | 0.5 | `r-05c666388af07453703e` | `r-11b167dc4373c8f23b2c` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -59.772973808288526 | 1.3234 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d50e9d4495b5c963d0a4` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.04033194453930743 | 0.015641 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-e81546959d38057e1d49` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.007682093803921673 | 0.021228337527022512 | 0.0135462 | 0.01 | `r-0241c17b5ff2297d2a17` | `r-d50e9d4495b5c963d0a4` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 27.769999999846902 | 8.6 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d50e9d4495b5c963d0a4` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 144.07999999986896 | 64.56 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-d50e9d4495b5c963d0a4` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 4.0 | 3 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d50e9d4495b5c963d0a4` |
| h/2 | P05_long_step | adaptation_index | definedness | 0.0054122174080685195 | None |  | 0.01 | `r-002bf860824963a1f621` | `r-2455d44faad252e65d04` |
| h/2 | P05_long_step | ahp_depth | definedness | -14.199851989746094 | None |  | 0.710809 | `r-002bf860824963a1f621` | `r-2455d44faad252e65d04` |
| h/2 | P05_long_step | ap_amplitude | definedness | 84.2574310317606 | None |  | 1.68529 | `r-002bf860824963a1f621` | `r-2455d44faad252e65d04` |
| h/2 | P05_long_step | first_spike_latency | definedness | 27.769999999846902 | None |  | 0.5562 | `r-002bf860824963a1f621` | `r-2455d44faad252e65d04` |
| h/2 | P05_long_step | last_isi | definedness | 112.62000000245826 | None |  | 2.2528 | `r-002bf860824963a1f621` | `r-2455d44faad252e65d04` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 0.0 | 19 | 0.5 | `r-002bf860824963a1f621` | `r-2455d44faad252e65d04` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 620.359999999308 | 219.68 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-ccbf82f2366facfd7561` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 5.0 | 4 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-ccbf82f2366facfd7561` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -81.01395266571055 | -71.92813829498301 | 9.08581 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d50e9d4495b5c963d0a4` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -16.78431911468506 | 1.1085 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-d694fd93d40eae4dc44a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
