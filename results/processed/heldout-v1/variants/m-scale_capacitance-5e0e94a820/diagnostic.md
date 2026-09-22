# m-scale_capacitance-5e0e94a820

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4623.528 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -14.954763991322906 | 6.97731 | 0.5 | `r-a309e30f4eac6329447d` | `r-06f673c0ff09ca412e27` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 76.03836822509587 | 97.35712432861474 | 21.3188 | 1.52077 | `r-a309e30f4eac6329447d` | `r-06f673c0ff09ca412e27` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.9100000000007817 | 1.4100000000005473 | 1.5 | 0.5 | `r-a309e30f4eac6329447d` | `r-06f673c0ff09ca412e27` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 5.260000000002691 | 2.33 | 0.5 | `r-a309e30f4eac6329447d` | `r-06f673c0ff09ca412e27` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 13.0 | 4 | 0.5 | `r-a309e30f4eac6329447d` | `r-06f673c0ff09ca412e27` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -5.43348429870143 | -13.215004946411867 | 7.78152 | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-addc695d64255bb847a5` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 76.68460655583269 | 85.02381896503375 | 8.33921 | 1.89637 | `r-531ed8bf9e8ec22d7778` | `r-addc695d64255bb847a5` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 48.25999999982827 | 5.47 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-addc695d64255bb847a5` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 6.019999999994525 | 19.61 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-addc695d64255bb847a5` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 21.0 | 3 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-addc695d64255bb847a5` |
| h/1 | P05_long_step | adaptation_index | exceeds | 0.0003686992675871277 | -0.018327167580821025 | 0.0186959 | 0.01 | `r-c181d8dc3f2e9e1a86cf` | `r-7b02d0222fd8d578fc67` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.300969345084837 | -13.106377626936535 | 7.80541 | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-7b02d0222fd8d578fc67` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 77.26993942349823 | 85.61004256641564 | 8.3401 | 1.98255 | `r-c181d8dc3f2e9e1a86cf` | `r-7b02d0222fd8d578fc67` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 78.71999999980056 | 7.78 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-7b02d0222fd8d578fc67` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 6.8700000001499575 | 39.69 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-7b02d0222fd8d578fc67` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 48.0 | 6 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-7b02d0222fd8d578fc67` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 425.69999999948504 | 9.34 | 8.7008 | `r-8c44150a9a017555d35c` | `r-8ee5881afa8715194b03` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 32.0 | 5 | 3 | `r-8c44150a9a017555d35c` | `r-8ee5881afa8715194b03` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -14.801117922508496 | 6.31294 | 1.08676 | `r-f411679bd6f2a1231337` | `r-cb23d153fd47e8c5b80a` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 90.83680152686651 | 99.65075301581354 | 8.81395 | 1.81674 | `r-f411679bd6f2a1231337` | `r-cb23d153fd47e8c5b80a` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.7799999998705403 | 0.959999999871286 | 0.82 | 0.5 | `r-f411679bd6f2a1231337` | `r-cb23d153fd47e8c5b80a` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.911862463500448 | -14.875815965642843 | 6.96395 | 0.5 | `r-82914471c1c753634231` | `r-92e285e65356c48f4c31` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 75.97283554077825 | 97.1079711913786 | 21.1351 | 1.52077 | `r-82914471c1c753634231` | `r-92e285e65356c48f4c31` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.90000000000078 | 1.4100000000005473 | 1.49 | 0.5 | `r-82914471c1c753634231` | `r-92e285e65356c48f4c31` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 5.270000000002696 | 2.34 | 0.5 | `r-82914471c1c753634231` | `r-92e285e65356c48f4c31` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 13.0 | 4 | 0.5 | `r-82914471c1c753634231` | `r-92e285e65356c48f4c31` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -5.051723726911618 | -12.8356554336806 | 7.78393 | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-c2397b8a6e67bb3cb02c` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 76.05248450904598 | 84.25002670511932 | 8.19754 | 1.89637 | `r-c4e93fb668595b0fb26c` | `r-c2397b8a6e67bb3cb02c` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 48.17999999982834 | 5.47 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-c2397b8a6e67bb3cb02c` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 6.029999999994516 | 20.03 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-c2397b8a6e67bb3cb02c` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 21.0 | 3 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-c2397b8a6e67bb3cb02c` |
| h/2 | P05_long_step | adaptation_index | exceeds | 0.0003457083960339961 | -0.01836034037567676 | 0.018706 | 0.01 | `r-c41be102b8e8611b929c` | `r-91436a949874de8eb4a3` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.916790255219169 | -12.727836830167888 | 7.81105 | 1.15254 | `r-c41be102b8e8611b929c` | `r-91436a949874de8eb4a3` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 76.60908890083579 | 84.92325592298238 | 8.31417 | 1.98255 | `r-c41be102b8e8611b929c` | `r-91436a949874de8eb4a3` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 78.62999999980065 | 7.79 | 1.73 | `r-c41be102b8e8611b929c` | `r-91436a949874de8eb4a3` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 6.910000000150831 | 40.52 | 2.61 | `r-c41be102b8e8611b929c` | `r-91436a949874de8eb4a3` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 48.0 | 7 | 3 | `r-c41be102b8e8611b929c` | `r-91436a949874de8eb4a3` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 425.59999999948514 | 9.36 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-c738ee731572f560d598` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 31.0 | 5 | 3 | `r-11d8f8c83600b900cadc` | `r-c738ee731572f560d598` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -14.392669898945698 | 6.26674 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-dc0bcbf0198c532d35ba` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 90.35200882226567 | 98.9929161061888 | 8.64091 | 1.81674 | `r-4bcc4e2fdcca97c21eee` | `r-dc0bcbf0198c532d35ba` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.7599999998705584 | 0.9399999998713042 | 0.82 | 0.5 | `r-4bcc4e2fdcca97c21eee` | `r-dc0bcbf0198c532d35ba` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
