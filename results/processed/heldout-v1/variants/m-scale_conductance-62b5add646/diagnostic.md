# m-scale_conductance-62b5add646

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pasCA1_all']", "new": "0.02857144 mS_per_cm2", "old": "0.0357143 mS_per_cm2"}], "element": "channelDensity", "element_id": "pasCA1_all", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pasCA1_all']", "attribute": "condDensity", "old": "0.0357143 mS_per_cm2", "new": "0.02857144 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 7212.767 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006488627825968173 | 6.83013e-05 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-762107b512f299920a70` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 17.329999999856398 | 1.26 | 0.5 | `r-0925b86f96a976919154` | `r-16614607a391d07a337b` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 42.2199999999616 | 2.16 | 0.8012 | `r-0925b86f96a976919154` | `r-16614607a391d07a337b` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-16614607a391d07a337b` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 25.779999999848712 | 2.63 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-a6daf173444c043611f6` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 55.76000000121712 | 4.25 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-a6daf173444c043611f6` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 36.0 | 3 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-a6daf173444c043611f6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 429.62999999948147 | 33.42 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-661c32a59bd6b5bd8302` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-661c32a59bd6b5bd8302` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006488627825968173 | 6.83013e-05 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-da17db52750a8d63de97` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 17.289999999856434 | 1.26 | 0.5 | `r-6797defd923ff2562240` | `r-ae4bad0d02e6899cf307` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 42.20999999996161 | 2.16 | 0.8012 | `r-6797defd923ff2562240` | `r-ae4bad0d02e6899cf307` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-ae4bad0d02e6899cf307` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 25.729999999848758 | 2.62 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-7cc791b3487f24cb8c00` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 55.84000000121887 | 4.28 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-7cc791b3487f24cb8c00` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 36.0 | 3 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-7cc791b3487f24cb8c00` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 429.5699999994815 | 33.42 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-e21d99402c6b1fdd2ad1` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-e21d99402c6b1fdd2ad1` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
