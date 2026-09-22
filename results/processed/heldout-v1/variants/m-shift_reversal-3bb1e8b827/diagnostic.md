# m-shift_reversal-3bb1e8b827

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_all']", "new": "52.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "nax_all", "generator_seed": 20260917, "shift_mV": 2.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_all']", "attribute": "erev", "old": "50.0 mV", "new": "52.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3104.719 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -12.62867672289191 | 0.773846 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-aefd7ed7bf9369676b6a` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 22.509999999851686 | 0.64 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-32063b81a850154642d1` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 50.450000001101216 | 1.06 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-32063b81a850154642d1` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 40.0 | 1 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-32063b81a850154642d1` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 386.77999999952044 | 9.43 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-46c2b0f704e468362c7b` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -12.578660613861814 | 0.774592 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-a317486e1b636cb3f2ea` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 22.459999999851732 | 0.65 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-4763d4186292283a0c4e` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 50.48000000110187 | 1.08 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-4763d4186292283a0c4e` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 40.0 | 1 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-4763d4186292283a0c4e` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 386.7299999995205 | 9.42 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-438aa70739437a5bf371` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
