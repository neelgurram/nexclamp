# m-scale_conductance-056f6e95e6

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "new": "0.1 mS_per_cm2", "old": "0.05 mS_per_cm2"}], "element": "channelDensity", "element_id": "hd_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "attribute": "condDensity", "old": "0.05 mS_per_cm2", "new": "0.1 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1117.288 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 2.134102529053085e-13 |  | inf | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -16.242066207809827 | 4.38724 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 2.720000000000752 | 2.7 | 0.5 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 17.230000000003926 | 1.1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-966f5de15e3931bbd9fe` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 11.0 | 11 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -65.66653187537734 | 0.643705 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0 | 0.000580561 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-65fd674d2d18de2cb284` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -16.69309456624417 | 1.91734 | 0.738788 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 16.89999999985679 | 0.83 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 29.469999999973197 | 10.59 | 0.8012 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 17.0 | 4 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -16.97372658528714 | 1.9005 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-bb4a8010808317f070ac` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 19.709999999854233 | 3.44 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-bb4a8010808317f070ac` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 32.76000000071508 | 18.75 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-bb4a8010808317f070ac` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 61.0 | 22 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-bb4a8010808317f070ac` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 44.62999999983157 | 351.58 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-14b3c507f4d617f1c6b1` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 30.0 | 14 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-14b3c507f4d617f1c6b1` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533750000003 | -65.14110532226566 | 2.99423 | 0.5 | `r-0925b86f96a976919154` | `r-9d0fbecae44384747ef9` |
| h/1 | P08_rebound | first_spike_latency | definedness | None | 23.97999999939566 |  | inf | `r-ff3ac53d55743f982ac3` | `r-6d2d1eeea42987c03bee` |
| h/1 | P08_rebound | spike_count | exceeds | 0.0 | 5.0 | 5 | 0.5 | `r-ff3ac53d55743f982ac3` | `r-6d2d1eeea42987c03bee` |
| h/1 | P09_short_pulse | ahp_depth | definedness | -16.001159667968338 | None |  | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-e6f9b58038280dfae9d1` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 100.17234039630091 | None |  | 2.00345 | `r-86c7a89ca0bbba8e93d0` | `r-e6f9b58038280dfae9d1` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | 3.9799999998685394 | None |  | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-e6f9b58038280dfae9d1` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-e6f9b58038280dfae9d1` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.00029027576218666686 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-2005c487ab12b5cd7d17` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -16.1910040176923 | 4.38694 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-2005c487ab12b5cd7d17` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 2.720000000000752 | 2.69 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-2005c487ab12b5cd7d17` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 17.230000000003905 | 1.09 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-2005c487ab12b5cd7d17` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-2005c487ab12b5cd7d17` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 11.0 | 11 | 0.5 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -65.79057888645063 | 0.767752 | 0.5 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0 | 0.000580561 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-05198b1e51020715082a` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -17.016649630834593 | 2.46276 | 0.738788 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 17.829999999855943 | 1.8 | 0.5 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 29.449999999973215 | 10.6 | 0.8012 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 17.0 | 4 | 0.5 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -17.30230179147867 | 2.44551 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-20e9c1be5766b3f13fc0` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 20.739999999853296 | 2.37 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-20e9c1be5766b3f13fc0` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 32.76000000071508 | 18.8 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-20e9c1be5766b3f13fc0` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 61.0 | 22 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-20e9c1be5766b3f13fc0` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 45.819999999830486 | 350.33 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-6c69f55b720bbf1517f9` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 30.0 | 14 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-6c69f55b720bbf1517f9` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533766326908 | -65.14110548706059 | 2.99423 | 0.5 | `r-6797defd923ff2562240` | `r-47184730e4a93fbafa99` |
| h/2 | P08_rebound | first_spike_latency | definedness | None | 23.939999999395695 |  | inf | `r-5841cbe01fb53bd3f5cf` | `r-0cec2dc1daf0e800fb1c` |
| h/2 | P08_rebound | spike_count | exceeds | 0.0 | 5.0 | 5 | 0.5 | `r-5841cbe01fb53bd3f5cf` | `r-0cec2dc1daf0e800fb1c` |
| h/2 | P09_short_pulse | ahp_depth | definedness | -15.791358947753906 | None |  | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-2108e465e3db262b0a43` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 99.86314392274174 | None |  | 2.00345 | `r-2e410d8c71a4df0466e8` | `r-2108e465e3db262b0a43` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | 3.9399999998685757 | None |  | 0.5 | `r-2e410d8c71a4df0466e8` | `r-2108e465e3db262b0a43` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-2108e465e3db262b0a43` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
