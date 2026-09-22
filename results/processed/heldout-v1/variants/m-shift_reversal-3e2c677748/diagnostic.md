# m-shift_reversal-3e2c677748

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "new": "-20.0 mV", "old": "-30.0 mV"}], "element": "channelDensity", "element_id": "hd_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "attribute": "erev", "old": "-30.0 mV", "new": "-20.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3156.397 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | -0.0002780094520340794 |  | inf | `r-1855c6a207dcec8ed210` | `r-c8224a917591165a9c74` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -12.890816494007012 | 1.03599 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-c8224a917591165a9c74` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 4.680000000001058 | 0.74 | 0.5 | `r-1855c6a207dcec8ed210` | `r-c8224a917591165a9c74` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-c8224a917591165a9c74` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -63.89578263626096 | 1.12704 | 0.5 | `r-0925b86f96a976919154` | `r-8c5ba01c6072801b4659` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0003756574004507889 | 0.000204904 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-ca8dccca0fca8c90ca8a` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -15.682075500487414 | 0.906319 | 0.738788 | `r-0925b86f96a976919154` | `r-8c5ba01c6072801b4659` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 12.339999999860936 | 3.73 | 0.5 | `r-0925b86f96a976919154` | `r-8c5ba01c6072801b4659` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 35.58999999996763 | 4.47 | 0.8012 | `r-0925b86f96a976919154` | `r-8c5ba01c6072801b4659` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 14.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-8c5ba01c6072801b4659` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -15.975334167479573 | 0.902107 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-6fb7e3e884a27d8df55a` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 16.24999999985738 | 6.9 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-6fb7e3e884a27d8df55a` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 42.35000000092441 | 9.16 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-6fb7e3e884a27d8df55a` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 47.0 | 8 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-6fb7e3e884a27d8df55a` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 282.4899999996153 | 113.72 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-8e3f5727e038f74571dc` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 20.0 | 4 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-8e3f5727e038f74571dc` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533750000003 | -67.1976086181641 | 0.937729 | 0.5 | `r-0925b86f96a976919154` | `r-8c5ba01c6072801b4659` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -16.88970947265625 | 0.88855 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-9872f0b742efc6f82a1b` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 3.9799999998685394 | 3.4599999998690123 | 0.52 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-9872f0b742efc6f82a1b` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.0002781641171156358 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-4e8d62b2e86507dcc4da` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -12.839822076446382 | 1.03575 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-4e8d62b2e86507dcc4da` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 4.670000000001057 | 0.74 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-4e8d62b2e86507dcc4da` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-4e8d62b2e86507dcc4da` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -63.89578255310056 | 1.12704 | 0.5 | `r-6797defd923ff2562240` | `r-e85c094845e8176f18c6` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0003756574004507889 | 0.000204904 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-9d5ebd3110a1b5dc08aa` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -15.45764923095659 | 0.903755 | 0.738788 | `r-6797defd923ff2562240` | `r-e85c094845e8176f18c6` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 12.299999999860972 | 3.73 | 0.5 | `r-6797defd923ff2562240` | `r-e85c094845e8176f18c6` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 35.57999999996764 | 4.47 | 0.8012 | `r-6797defd923ff2562240` | `r-e85c094845e8176f18c6` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 14.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-e85c094845e8176f18c6` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -15.757034301757812 | 0.900238 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-bdd82c1ec8d189e197bd` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 16.209999999857416 | 6.9 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-bdd82c1ec8d189e197bd` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 42.36000000092463 | 9.2 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-bdd82c1ec8d189e197bd` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 47.0 | 8 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-bdd82c1ec8d189e197bd` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 282.42999999961535 | 113.72 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-a3f9b0fb53c2aff10a8b` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 20.0 | 4 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-a3f9b0fb53c2aff10a8b` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533766326908 | -67.1976087844849 | 0.937729 | 0.5 | `r-6797defd923ff2562240` | `r-e85c094845e8176f18c6` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -15.791358947753906 | -16.676849365233963 | 0.88549 | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-8018f20ec1a2f99559b2` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 3.9399999998685757 | 3.4199999998690487 | 0.52 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-8018f20ec1a2f99559b2` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
