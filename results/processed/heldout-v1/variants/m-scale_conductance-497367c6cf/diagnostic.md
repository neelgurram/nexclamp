# m-scale_conductance-497367c6cf

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "new": "30.0 mS_per_cm2", "old": "15.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "ka_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "attribute": "condDensity", "old": "15.0 mS_per_cm2", "new": "30.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4547.086 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.017936897992228234 | None |  | 0.01 | `r-a309e30f4eac6329447d` | `r-00fb0bfc89a1d3251463` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -4.794810546571355 | 3.18264 | 0.5 | `r-a309e30f4eac6329447d` | `r-00fb0bfc89a1d3251463` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 76.03836822509587 | 73.71942138672125 | 2.31895 | 1.52077 | `r-a309e30f4eac6329447d` | `r-00fb0bfc89a1d3251463` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.9100000000007817 | 27.719999999999075 | 24.81 | 0.5 | `r-a309e30f4eac6329447d` | `r-00fb0bfc89a1d3251463` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 6.529999999998701 | 1.06 | 0.5 | `r-a309e30f4eac6329447d` | `r-00fb0bfc89a1d3251463` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 3.0 | 6 | 0.5 | `r-a309e30f4eac6329447d` | `r-00fb0bfc89a1d3251463` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -65.26699990539542 | 2.15389 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.03872686291919951 | 0.0216174 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-d0f63a18616f7580808c` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.004861353302673796 | None |  | 0.01 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P04_step_2x | ahp_depth | definedness | -5.43348429870143 | None |  | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 76.68460655583269 | None |  | 1.89637 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 53.72999999982329 | None |  | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P04_step_2x | last_isi | definedness | 25.62999999997669 | None |  | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 0.0 | 18 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P05_long_step | adaptation_index | definedness | 0.0003686992675871277 | None |  | 0.01 | `r-c181d8dc3f2e9e1a86cf` | `r-2e48f7da8cb94e3c5156` |
| h/1 | P05_long_step | ahp_depth | definedness | -5.300969345084837 | None |  | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-2e48f7da8cb94e3c5156` |
| h/1 | P05_long_step | ap_amplitude | definedness | 77.26993942349823 | None |  | 1.98255 | `r-c181d8dc3f2e9e1a86cf` | `r-2e48f7da8cb94e3c5156` |
| h/1 | P05_long_step | first_spike_latency | definedness | 86.49999999979349 | None |  | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-2e48f7da8cb94e3c5156` |
| h/1 | P05_long_step | last_isi | definedness | 46.560000001016306 | None |  | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-2e48f7da8cb94e3c5156` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 0.0 | 42 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-2e48f7da8cb94e3c5156` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 863.8199999990866 | 428.78 | 8.7008 | `r-8c44150a9a017555d35c` | `r-56c3863f714855c2f19c` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 4.0 | 23 | 3 | `r-8c44150a9a017555d35c` | `r-56c3863f714855c2f19c` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.1199735717775 | -69.89106764221208 | 0.771094 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-6b9bc748034cee732f5b` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -15.30523499295792 | 6.81706 | 1.08676 | `r-f411679bd6f2a1231337` | `r-90dc2a52ebdd7acb1a35` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 90.83680152686651 | 81.87013626268238 | 8.96667 | 1.81674 | `r-f411679bd6f2a1231337` | `r-90dc2a52ebdd7acb1a35` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.7799999998705403 | 2.539999999869849 | 0.76 | 0.5 | `r-f411679bd6f2a1231337` | `r-90dc2a52ebdd7acb1a35` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.018020148454594893 | None |  | 0.01 | `r-82914471c1c753634231` | `r-5e6cd3251c10b88195e8` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.911862463500448 | -4.727649404041756 | 3.18421 | 0.5 | `r-82914471c1c753634231` | `r-5e6cd3251c10b88195e8` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 75.97283554077825 | 73.56612777712292 | 2.40671 | 1.52077 | `r-82914471c1c753634231` | `r-5e6cd3251c10b88195e8` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.90000000000078 | 27.709999999999077 | 24.81 | 0.5 | `r-82914471c1c753634231` | `r-5e6cd3251c10b88195e8` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 6.539999999998699 | 1.07 | 0.5 | `r-82914471c1c753634231` | `r-5e6cd3251c10b88195e8` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 3.0 | 6 | 0.5 | `r-82914471c1c753634231` | `r-5e6cd3251c10b88195e8` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.11310686187736 | -65.26699956359855 | 2.15389 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.03872686291919951 | 0.0216174 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-1f3e8515493191290cde` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.004952237915862522 | None |  | 0.01 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P04_step_2x | ahp_depth | definedness | -5.051723726911618 | None |  | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 76.05248450904598 | None |  | 1.89637 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 53.649999999823365 | None |  | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P04_step_2x | last_isi | definedness | 26.0599999999763 | None |  | 1.29 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 0.0 | 18 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P05_long_step | adaptation_index | definedness | 0.0003457083960339961 | None |  | 0.01 | `r-c41be102b8e8611b929c` | `r-8b92c14a9c9ef7b43f52` |
| h/2 | P05_long_step | ahp_depth | definedness | -4.916790255219169 | None |  | 1.15254 | `r-c41be102b8e8611b929c` | `r-8b92c14a9c9ef7b43f52` |
| h/2 | P05_long_step | ap_amplitude | definedness | 76.60908890083579 | None |  | 1.98255 | `r-c41be102b8e8611b929c` | `r-8b92c14a9c9ef7b43f52` |
| h/2 | P05_long_step | first_spike_latency | definedness | 86.41999999979356 | None |  | 1.73 | `r-c41be102b8e8611b929c` | `r-8b92c14a9c9ef7b43f52` |
| h/2 | P05_long_step | last_isi | definedness | 47.430000001035296 | None |  | 2.61 | `r-c41be102b8e8611b929c` | `r-8b92c14a9c9ef7b43f52` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 0.0 | 41 | 3 | `r-c41be102b8e8611b929c` | `r-8b92c14a9c9ef7b43f52` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 863.7299999990867 | 428.77 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-7f88eed63ff2ea6eeba1` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 4.0 | 22 | 3 | `r-11d8f8c83600b900cadc` | `r-7f88eed63ff2ea6eeba1` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.11997425689714 | -69.89106831665056 | 0.771094 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-7fd8268540589a2021da` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -15.013402974429383 | 6.88748 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-d9e984dbf47473834843` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 90.35200882226567 | 81.8927469282428 | 8.45926 | 1.81674 | `r-4bcc4e2fdcca97c21eee` | `r-d9e984dbf47473834843` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.7599999998705584 | 2.4999999998698854 | 0.74 | 0.5 | `r-4bcc4e2fdcca97c21eee` | `r-d9e984dbf47473834843` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
