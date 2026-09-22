# m-scale_conductance-c2b2371643

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na3_all']", "new": "22.5 mS_per_cm2", "old": "25.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "na3_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na3_all']", "attribute": "condDensity", "old": "25.0 mS_per_cm2", "new": "22.5 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 7375.718 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-5666b4f7f44cf4c608b8` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 23.929999999850395 | 0.78 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-4f815599b9280eced4d6` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 52.6300000011488 | 1.12 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-4f815599b9280eced4d6` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 38.0 | 1 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-4f815599b9280eced4d6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 406.99999999950205 | 10.79 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-e5fb4d2947d42b0f02c7` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-529478d655694a3c7160` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 23.88999999985043 | 0.78 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-22d561bf6e3cac8168f7` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 52.68000000114989 | 1.12 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-22d561bf6e3cac8168f7` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 38.0 | 1 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-22d561bf6e3cac8168f7` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 406.9399999995021 | 10.79 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-c7a738357aa8a1920448` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
