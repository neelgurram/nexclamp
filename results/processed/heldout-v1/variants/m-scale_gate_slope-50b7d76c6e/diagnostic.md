# m-scale_gate_slope-50b7d76c6e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='ka']/ionChannel[@id='ka']/gate[@id='m']/steadyState[1]", "new": "6.8mV", "old": "8.5mV"}], "channel": "ka", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/ka.channel.nml", "locator": "/neuroml[@id='ka']/ionChannel[@id='ka']/gate[@id='m']/steadyState[1]", "attribute": "scale", "old": "8.5mV", "new": "6.8mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 10965.97 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -62.49340325164787 | 0.619704 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-a59668b085d45325ec21` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.018031555221637866 | 0.000922068 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-64cda756f5dc8e4a9444` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 56.69999999982059 | 2.97 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-a59668b085d45325ec21` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 28.81999999997379 | 3.19 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-a59668b085d45325ec21` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 16.0 | 2 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-a59668b085d45325ec21` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 94.56999999978615 | 8.07 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-d2ea1cefc9b66ba52aae` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 55.47000000121079 | 8.91 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-d2ea1cefc9b66ba52aae` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 35.0 | 7 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-d2ea1cefc9b66ba52aae` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 452.149999999461 | 17.11 | 8.7008 | `r-8c44150a9a017555d35c` | `r-b383f191e0dfafebbd9b` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.1199735717775 | -68.55688347930925 | 0.56309 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-a59668b085d45325ec21` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.11310686187736 | -62.49340290679923 | 0.619704 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-c3387a47a4e5d3ccc343` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.018031555221637866 | 0.000922068 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-04b07deeffff183d4329` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 56.619999999820664 | 2.97 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-c3387a47a4e5d3ccc343` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 29.27999999997337 | 3.22 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-c3387a47a4e5d3ccc343` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 16.0 | 2 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-c3387a47a4e5d3ccc343` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 94.48999999978622 | 8.07 | 1.73 | `r-c41be102b8e8611b929c` | `r-9c1fa0b7bed7d6f4608d` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 56.440000001231965 | 9.01 | 2.61 | `r-c41be102b8e8611b929c` | `r-9c1fa0b7bed7d6f4608d` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 34.0 | 7 | 3 | `r-c41be102b8e8611b929c` | `r-9c1fa0b7bed7d6f4608d` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 452.05999999946107 | 17.1 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-3faa244070f89cc76265` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.11997425689714 | -68.55688416748063 | 0.56309 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-c3387a47a4e5d3ccc343` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
