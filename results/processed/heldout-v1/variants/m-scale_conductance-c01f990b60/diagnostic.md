# m-scale_conductance-c01f990b60

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='napf_tcr_all']", "new": "0.045 mS_per_cm2", "old": "0.05 mS_per_cm2"}], "element": "channelDensity", "element_id": "napf_tcr_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='napf_tcr_all']", "attribute": "condDensity", "old": "0.05 mS_per_cm2", "new": "0.045 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 10685.629 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.018407212622088658 | 0.00129773 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-bc81f08f36b1dc8507ce` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 58.67999999981879 | 4.95 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-e486f6b4dd883a0c4269` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 27.489999999974998 | 1.86 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-e486f6b4dd883a0c4269` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 17.0 | 1 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-e486f6b4dd883a0c4269` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 98.48999999978258 | 11.99 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-78b6da9fc52f10d46cc0` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 53.68000000117172 | 7.12 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-78b6da9fc52f10d46cc0` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 36.0 | 6 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-78b6da9fc52f10d46cc0` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 460.2499999994536 | 25.21 | 8.7008 | `r-8c44150a9a017555d35c` | `r-e364c1977bf910175ac9` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.018407212622088658 | 0.00129773 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-d680da1e594372f9674b` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 58.59999999981886 | 4.95 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-1e3d4db58b5f93a9d88e` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 27.96999999997456 | 1.91 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-1e3d4db58b5f93a9d88e` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 17.0 | 1 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-1e3d4db58b5f93a9d88e` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 98.40999999978266 | 11.99 | 1.73 | `r-c41be102b8e8611b929c` | `r-8abcfdf3f1148dff62c3` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 54.7100000011942 | 7.28 | 2.61 | `r-c41be102b8e8611b929c` | `r-8abcfdf3f1148dff62c3` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 35.0 | 6 | 3 | `r-c41be102b8e8611b929c` | `r-8abcfdf3f1148dff62c3` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 460.1599999994537 | 25.2 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-a989763e31b3e865882f` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
