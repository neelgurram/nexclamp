# m-shift_gate_midpoint-0bf496636d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "new": "-10mV", "old": "-20mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "new": "-33mV", "old": "-43mV"}], "channel": "km", "delta_mV": 10.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-20mV", "new": "-10mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-43mV", "new": "-33mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4577.422 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.017936897992228234 | 0.003829550021039614 | 0.0141073 | 0.01 | `r-a309e30f4eac6329447d` | `r-7da34e325896436ec767` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 6.130000000003136 | 1.46 | 0.5 | `r-a309e30f4eac6329447d` | `r-7da34e325896436ec767` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-7da34e325896436ec767` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.004861353302673796 | -0.01131672312993306 | 0.0161781 | 0.01 | `r-531ed8bf9e8ec22d7778` | `r-e3d9e11af34e87ec95a9` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 12.129999999988968 | 13.5 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-e3d9e11af34e87ec95a9` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 28.0 | 10 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-e3d9e11af34e87ec95a9` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 27.700000000604632 | 18.86 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-889219cf337d75647944` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 70.0 | 28 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-889219cf337d75647944` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 41.0 | 14 | 3 | `r-8c44150a9a017555d35c` | `r-c38f4045b1daaf185580` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.018020148454594893 | 0.004069014951416039 | 0.0139511 | 0.01 | `r-82914471c1c753634231` | `r-b7ea2c237da7ffe9401b` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 6.140000000003141 | 1.47 | 0.5 | `r-82914471c1c753634231` | `r-b7ea2c237da7ffe9401b` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-82914471c1c753634231` | `r-b7ea2c237da7ffe9401b` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.004952237915862522 | -0.011125329208585394 | 0.0160776 | 0.01 | `r-c4e93fb668595b0fb26c` | `r-90554d5e4a830b771821` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 12.189999999988913 | 13.87 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-90554d5e4a830b771821` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 28.0 | 10 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-90554d5e4a830b771821` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 27.670000000603977 | 19.76 | 2.61 | `r-c41be102b8e8611b929c` | `r-4869b71621f1bf732e73` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 70.0 | 29 | 3 | `r-c41be102b8e8611b929c` | `r-4869b71621f1bf732e73` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 41.0 | 15 | 3 | `r-11d8f8c83600b900cadc` | `r-8f8cf24ac6946fc8f8db` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
