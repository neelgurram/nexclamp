# m-shift_forward_rate_midpoint-8e309ecd33

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/forwardRate[1]", "new": "-25mV", "old": "-30mV"}], "channel": "na3", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/na3.channel.nml", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-25mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 5453.02 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0007171641281333242 | 0.000136603 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-c939a3232a042bb2e11f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 19.589999999854342 | 3.52 | 0.5 | `r-0925b86f96a976919154` | `r-8346030b0b790d3c7519` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 44.809999999959246 | 4.75 | 0.8012 | `r-0925b86f96a976919154` | `r-8346030b0b790d3c7519` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 11.0 | 2 | 0.5 | `r-0925b86f96a976919154` | `r-8346030b0b790d3c7519` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 32.25999999984282 | 9.11 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-3e8788ed708c3c424a70` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 65.63000000143256 | 14.12 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-3e8788ed708c3c424a70` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 30.0 | 9 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-3e8788ed708c3c424a70` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 489.11999999942736 | 92.91 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-1c335d3f98dffb5c72a1` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 13.0 | 3 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-1c335d3f98dffb5c72a1` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0007171641281333242 | 0.000136603 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-92e71cf21657dc094de3` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 19.54999999985438 | 3.52 | 0.5 | `r-6797defd923ff2562240` | `r-fccf835dff9004b63eb7` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 44.809999999959246 | 4.76 | 0.8012 | `r-6797defd923ff2562240` | `r-fccf835dff9004b63eb7` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 11.0 | 2 | 0.5 | `r-6797defd923ff2562240` | `r-fccf835dff9004b63eb7` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 32.209999999842864 | 9.1 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-0c0e3ba352f0d2ff3625` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 65.77000000143562 | 14.21 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-0c0e3ba352f0d2ff3625` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 30.0 | 9 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-0c0e3ba352f0d2ff3625` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 489.0599999994274 | 92.91 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-1254024d56f295a57370` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 13.0 | 3 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-1254024d56f295a57370` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
