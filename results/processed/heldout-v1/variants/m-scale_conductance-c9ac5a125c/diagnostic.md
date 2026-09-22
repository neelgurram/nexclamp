# m-scale_conductance-c9ac5a125c

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "new": "7.5 mS_per_cm2", "old": "15.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "ka_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "attribute": "condDensity", "old": "15.0 mS_per_cm2", "new": "7.5 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4601.371 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -6.88505470693412 | 1.0924 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 76.03836822509587 | 80.32566833494114 | 4.2873 | 1.52077 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.9100000000007817 | 2.330000000000691 | 0.58 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 6.740000000003448 | 0.85 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-8383195efdf2bd1f1e62` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 2.0 | 2 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -59.61384217454062 | 3.49927 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.007069189263028482 | 0.0100403 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-26dc8b71a984b4cd102d` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -5.43348429870143 | -6.8190852063496905 | 1.3856 | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 21.859999999852278 | 31.87 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 15.79999999998563 | 9.83 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 32.0 | 14 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.300969345084837 | -6.698494996383481 | 1.39753 | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-5675e1f1eecffc733167` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 30.789999999844156 | 55.71 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-5675e1f1eecffc733167` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 22.4300000004896 | 24.13 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-5675e1f1eecffc733167` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 89.0 | 47 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-5675e1f1eecffc733167` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 235.47999999965805 | 199.56 | 8.7008 | `r-8c44150a9a017555d35c` | `r-d50504d4c82f692cf490` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 46.0 | 19 | 3 | `r-8c44150a9a017555d35c` | `r-d50504d4c82f692cf490` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.1199735717775 | -68.5961770446779 | 0.523797 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-1b0454bcf47d8bacfba4` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -6.301575745890538 | 2.1866 | 1.08676 | `r-f411679bd6f2a1231337` | `r-84893f0603cbc8f9724c` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.911862463500448 | -6.810185332796536 | 1.10168 | 0.5 | `r-82914471c1c753634231` | `r-a8c261dce0af680b4ec9` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 75.97283554077825 | 80.20478439330157 | 4.23195 | 1.52077 | `r-82914471c1c753634231` | `r-a8c261dce0af680b4ec9` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.90000000000078 | 2.3200000000006895 | 0.58 | 0.5 | `r-82914471c1c753634231` | `r-a8c261dce0af680b4ec9` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 6.750000000003453 | 0.86 | 0.5 | `r-82914471c1c753634231` | `r-a8c261dce0af680b4ec9` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-82914471c1c753634231` | `r-a8c261dce0af680b4ec9` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 2.0 | 2 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.11310686187736 | -59.74865330811291 | 3.36445 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.007069189263028482 | 0.0100403 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-0cb9112d0c625cf3b441` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -5.051723726911618 | -6.435438404082795 | 1.38371 | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 21.799999999852332 | 31.85 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 16.099999999985357 | 9.96 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 31.0 | 13 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.916790255219169 | -6.312223682394453 | 1.39543 | 1.15254 | `r-c41be102b8e8611b929c` | `r-41229a3c6f5679224dad` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 30.71999999984422 | 55.7 | 1.73 | `r-c41be102b8e8611b929c` | `r-41229a3c6f5679224dad` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 22.850000000498767 | 24.58 | 2.61 | `r-c41be102b8e8611b929c` | `r-41229a3c6f5679224dad` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 87.0 | 46 | 3 | `r-c41be102b8e8611b929c` | `r-41229a3c6f5679224dad` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 235.39999999965812 | 199.56 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-9f5a40d61df0cbff4a36` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 46.0 | 20 | 3 | `r-11d8f8c83600b900cadc` | `r-9f5a40d61df0cbff4a36` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.11997425689714 | -68.59617776947037 | 0.523796 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-be9837758c7c4c91f5ae` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -5.875128040288665 | 2.2508 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-078dea34627608818179` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
