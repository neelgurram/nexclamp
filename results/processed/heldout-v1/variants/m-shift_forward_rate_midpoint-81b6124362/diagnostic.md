# m-shift_forward_rate_midpoint-81b6124362

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "new": "-25mV", "old": "-20mV"}], "channel": "km", "delta_mV": -5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-20mV", "new": "-25mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4599.896 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 8.13000000000416 | 0.54 | 0.5 | `r-a309e30f4eac6329447d` | `r-e305703d47e018955f0e` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-a309e30f4eac6329447d` | `r-e305703d47e018955f0e` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 29.099999999973534 | 3.47 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-f1ca5122eddbec0f882a` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 16.0 | 2 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-f1ca5122eddbec0f882a` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 88.3599999997918 | 1.86 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-d86a9816653f2efadf5b` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 54.33000000118591 | 7.77 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-d86a9816653f2efadf5b` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 36.0 | 6 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-d86a9816653f2efadf5b` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 8.15000000000417 | 0.54 | 0.5 | `r-82914471c1c753634231` | `r-8866cde868d5443df5d2` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-82914471c1c753634231` | `r-8866cde868d5443df5d2` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 29.589999999973088 | 3.53 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-7e01508203a88dbaa00f` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 16.0 | 2 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-7e01508203a88dbaa00f` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 88.27999999979187 | 1.86 | 1.73 | `r-c41be102b8e8611b929c` | `r-f1b3361d3bad7ed0e35a` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 55.3100000012073 | 7.88 | 2.61 | `r-c41be102b8e8611b929c` | `r-f1b3361d3bad7ed0e35a` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 35.0 | 6 | 3 | `r-c41be102b8e8611b929c` | `r-f1b3361d3bad7ed0e35a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
