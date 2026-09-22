# m-shift_reversal-430bfde1a2

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='km_all']", "new": "-90.0 mV", "old": "-95.0 mV"}], "element": "channelDensity", "element_id": "km_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='km_all']", "attribute": "erev", "old": "-95.0 mV", "new": "-90.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4629.571 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 7.080000000003622 | 0.51 | 0.5 | `r-a309e30f4eac6329447d` | `r-ce076069c34d480f7325` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 23.389999999978727 | 2.24 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-21aa16650565d4474528` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 20.0 | 2 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-21aa16650565d4474528` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 41.93000000091524 | 4.63 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-fa1f2a2db527ce87a8f2` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 46.0 | 4 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-fa1f2a2db527ce87a8f2` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 7.100000000003632 | 0.51 | 0.5 | `r-82914471c1c753634231` | `r-0ed34a4df9e9feb4e710` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 23.689999999978454 | 2.37 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-1cbfaed27180c900055b` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 20.0 | 2 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-1cbfaed27180c900055b` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 42.58000000092943 | 4.85 | 2.61 | `r-c41be102b8e8611b929c` | `r-58a862a64765d81f9495` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 46.0 | 5 | 3 | `r-c41be102b8e8611b929c` | `r-58a862a64765d81f9495` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
