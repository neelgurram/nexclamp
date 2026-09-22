# m-scale_capacitance-6684c04454

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4630.548 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -10.24434436019957 | 2.26689 | 0.5 | `r-a309e30f4eac6329447d` | `r-26628626532fa97921d0` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 76.03836822509587 | 81.37387847898549 | 5.33551 | 1.52077 | `r-a309e30f4eac6329447d` | `r-26628626532fa97921d0` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.9100000000007817 | 2.26000000000068 | 0.65 | 0.5 | `r-a309e30f4eac6329447d` | `r-26628626532fa97921d0` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 6.750000000003453 | 0.84 | 0.5 | `r-a309e30f4eac6329447d` | `r-26628626532fa97921d0` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-26628626532fa97921d0` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.004861353302673796 | -0.009682773537839511 | 0.0145441 | 0.01 | `r-531ed8bf9e8ec22d7778` | `r-fb53890b65ab6113a90a` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -5.43348429870143 | -7.875445861825526 | 2.44196 | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-fb53890b65ab6113a90a` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 76.68460655583269 | 79.56954765409824 | 2.88494 | 1.89637 | `r-531ed8bf9e8ec22d7778` | `r-fb53890b65ab6113a90a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 51.68999999982515 | 2.04 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-fb53890b65ab6113a90a` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 24.219999999977972 | 1.41 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-fb53890b65ab6113a90a` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 19.0 | 1 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-fb53890b65ab6113a90a` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.300969345084837 | -7.735797424295129 | 2.43483 | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-09dfc52ef5b654a85aca` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 77.26993942349823 | 80.12961005665511 | 2.85967 | 1.98255 | `r-c181d8dc3f2e9e1a86cf` | `r-09dfc52ef5b654a85aca` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 83.57999999979614 | 2.92 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-09dfc52ef5b654a85aca` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -10.556918640160532 | 2.06874 | 1.08676 | `r-f411679bd6f2a1231337` | `r-e7ece67bb2d6e559e40b` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 90.83680152686651 | 93.85574722024688 | 3.01895 | 1.81674 | `r-f411679bd6f2a1231337` | `r-e7ece67bb2d6e559e40b` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.911862463500448 | -10.173376814050044 | 2.26151 | 0.5 | `r-82914471c1c753634231` | `r-eab871577b686166347b` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 75.97283554077825 | 81.25011825560814 | 5.27728 | 1.52077 | `r-82914471c1c753634231` | `r-eab871577b686166347b` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.90000000000078 | 2.2500000000006786 | 0.65 | 0.5 | `r-82914471c1c753634231` | `r-eab871577b686166347b` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 6.750000000003453 | 0.86 | 0.5 | `r-82914471c1c753634231` | `r-eab871577b686166347b` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-82914471c1c753634231` | `r-eab871577b686166347b` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.004952237915862522 | -0.009399149633386006 | 0.0143514 | 0.01 | `r-c4e93fb668595b0fb26c` | `r-7aceaa0aeb75f58a34d0` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -5.051723726911618 | -7.49249518585313 | 2.44077 | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-7aceaa0aeb75f58a34d0` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 76.05248450904598 | 78.89500045306346 | 2.84252 | 1.89637 | `r-c4e93fb668595b0fb26c` | `r-7aceaa0aeb75f58a34d0` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 51.60999999982522 | 2.04 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-7aceaa0aeb75f58a34d0` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 24.74999999997749 | 1.31 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-7aceaa0aeb75f58a34d0` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 19.0 | 1 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-7aceaa0aeb75f58a34d0` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.916790255219169 | -7.351458198546112 | 2.43467 | 1.15254 | `r-c41be102b8e8611b929c` | `r-8faa42aaa53aaf6e3d39` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 76.60908890083579 | 79.51616478158311 | 2.90708 | 1.98255 | `r-c41be102b8e8611b929c` | `r-8faa42aaa53aaf6e3d39` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 83.49999999979622 | 2.92 | 1.73 | `r-c41be102b8e8611b929c` | `r-8faa42aaa53aaf6e3d39` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -10.173166877768807 | 2.04724 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-ba540c765cf4f31af68d` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 90.35200882226567 | 93.31648826827252 | 2.96448 | 1.81674 | `r-4bcc4e2fdcca97c21eee` | `r-ba540c765cf4f31af68d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
