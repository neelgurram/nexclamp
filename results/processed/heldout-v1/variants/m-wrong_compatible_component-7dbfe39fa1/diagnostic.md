# m-wrong_compatible_component-7dbfe39fa1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "new": "napf_tcr", "old": "nap"}], "element_id": "nap_all", "generator_seed": 20260917, "new_species": "na", "old_species": "na"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "attribute": "ionChannel", "old": "nap", "new": "napf_tcr", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4564.609 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-1efd16a63ac021cf83a8` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -63.80748185043327 | 0.694375 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-989914a722b2d239abee` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.020592855679256884 | 0.00348337 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-632bee03c4278ccb05e5` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 67.88999999981041 | 14.16 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-989914a722b2d239abee` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 31.219999999971606 | 5.59 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-989914a722b2d239abee` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 15.0 | 3 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-989914a722b2d239abee` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 125.6299999997579 | 39.13 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-6c3f930db324f2d37865` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 72.13000000157444 | 25.57 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-6c3f930db324f2d37865` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 27.0 | 15 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-6c3f930db324f2d37865` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 501.97999999941567 | 66.94 | 8.7008 | `r-8c44150a9a017555d35c` | `r-c3b51cc570d5b8c7a727` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 22.0 | 5 | 3 | `r-8c44150a9a017555d35c` | `r-c3b51cc570d5b8c7a727` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-82914471c1c753634231` | `r-7a28c65a9350a2121158` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.11310686187736 | -63.807481494140546 | 0.694375 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-5152c06a0758f95d3138` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.020592855679256884 | 0.00348337 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-fca181d0f5f08fbdac26` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 67.81999999981048 | 14.17 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-5152c06a0758f95d3138` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 31.789999999971087 | 5.73 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-5152c06a0758f95d3138` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 14.0 | 4 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-5152c06a0758f95d3138` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 125.53999999975798 | 39.12 | 1.73 | `r-c41be102b8e8611b929c` | `r-b2b9b44bfdf67028d033` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 73.60000000160653 | 26.17 | 2.61 | `r-c41be102b8e8611b929c` | `r-b2b9b44bfdf67028d033` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 26.0 | 15 | 3 | `r-c41be102b8e8611b929c` | `r-b2b9b44bfdf67028d033` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 501.88999999941575 | 66.93 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-3e6dd016cec50bac907f` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 22.0 | 4 | 3 | `r-11d8f8c83600b900cadc` | `r-3e6dd016cec50bac907f` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
