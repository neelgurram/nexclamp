# m-wrong_channel-5a74a3ef79

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pasCA1_all']", "new": "na3", "old": "pasCA1"}], "element_id": "pasCA1_all", "generator_seed": 20260917, "new_species": "na", "old_species": "non_specific"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pasCA1_all']", "attribute": "ionChannel", "old": "pasCA1", "new": "na3", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3666.551 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -10.297205227524486 | 1.55763 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-bbeda35dd58254fa1dac` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 7.040000000001427 | 1.62 | 0.5 | `r-1855c6a207dcec8ed210` | `r-bbeda35dd58254fa1dac` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 20.11999999999825 | 1.79 | 0.5 | `r-1855c6a207dcec8ed210` | `r-bbeda35dd58254fa1dac` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -67.17978684844968 | 2.15696 | 0.5 | `r-0925b86f96a976919154` | `r-d27fb9282dd6c285b3d4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0008537668192063383 | 0.000273205 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-07c45815343f75bf4c3d` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 24.139999999850204 | 8.07 | 0.5 | `r-0925b86f96a976919154` | `r-d27fb9282dd6c285b3d4` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 54.48999999995044 | 14.43 | 0.8012 | `r-0925b86f96a976919154` | `r-d27fb9282dd6c285b3d4` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 9.0 | 4 | 0.5 | `r-0925b86f96a976919154` | `r-d27fb9282dd6c285b3d4` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 48.61999999982794 | 25.47 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-43ba59b5b62a8563ead6` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 105.0400000022928 | 53.53 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-43ba59b5b62a8563ead6` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 19.0 | 20 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-43ba59b5b62a8563ead6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 570.0299999993538 | 173.82 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-7771f4844739bb970c53` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 10.0 | 6 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-7771f4844739bb970c53` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533750000003 | -70.60262265472416 | 2.46729 | 0.5 | `r-0925b86f96a976919154` | `r-d27fb9282dd6c285b3d4` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 3.9799999998685394 | 6.549999999866202 | 2.57 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-76fb7dab8250114f02bb` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -10.246796641183764 | 1.55727 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-d339cbca6c4aaf2342ca` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 7.030000000001426 | 1.62 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-d339cbca6c4aaf2342ca` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 20.10999999999823 | 1.79 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-d339cbca6c4aaf2342ca` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -67.17978676605222 | 2.15696 | 0.5 | `r-6797defd923ff2562240` | `r-e4888f173db64c5ca7a3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0008537668192063383 | 0.000273205 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-242fac0583c66381eb34` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 24.09999999985024 | 8.07 | 0.5 | `r-6797defd923ff2562240` | `r-e4888f173db64c5ca7a3` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 54.539999999950396 | 14.49 | 0.8012 | `r-6797defd923ff2562240` | `r-e4888f173db64c5ca7a3` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 9.0 | 4 | 0.5 | `r-6797defd923ff2562240` | `r-e4888f173db64c5ca7a3` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 48.579999999827976 | 25.47 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-593d6f7d4bb3cadb9de1` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 106.88000000233296 | 55.32 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-593d6f7d4bb3cadb9de1` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 19.0 | 20 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-593d6f7d4bb3cadb9de1` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 569.9799999993538 | 173.83 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-ed331cb3f97894b12d67` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 10.0 | 6 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-ed331cb3f97894b12d67` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533766326908 | -70.60262282104496 | 2.46729 | 0.5 | `r-6797defd923ff2562240` | `r-e4888f173db64c5ca7a3` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 3.9399999998685757 | 6.499999999866247 | 2.56 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-1989c47edab302e00f63` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
