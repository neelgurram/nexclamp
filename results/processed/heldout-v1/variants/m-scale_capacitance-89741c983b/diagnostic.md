# m-scale_capacitance-89741c983b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3111.602 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 1.5941661510830707e-13 |  | inf | `r-1855c6a207dcec8ed210` | `r-43fe816df27fd2218da9` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -16.885810814093617 | 5.03098 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-43fe816df27fd2218da9` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.14028549194009 | 102.55198287966994 | 2.4117 | 2.00281 | `r-1855c6a207dcec8ed210` | `r-43fe816df27fd2218da9` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 2.930000000000785 | 2.49 | 0.5 | `r-1855c6a207dcec8ed210` | `r-43fe816df27fd2218da9` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 13.260000000005817 | 5.07 | 0.5 | `r-1855c6a207dcec8ed210` | `r-43fe816df27fd2218da9` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 5.0 | 2 | 0.5 | `r-1855c6a207dcec8ed210` | `r-43fe816df27fd2218da9` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -18.99810028075983 | 4.22234 | 0.738788 | `r-0925b86f96a976919154` | `r-a5b54f0090de5540ed02` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 100.46828841971717 | 102.64760969985126 | 2.17932 | 2.00937 | `r-0925b86f96a976919154` | `r-a5b54f0090de5540ed02` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 8.459999999864465 | 7.61 | 0.5 | `r-0925b86f96a976919154` | `r-a5b54f0090de5540ed02` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 27.099999999975353 | 12.96 | 0.8012 | `r-0925b86f96a976919154` | `r-a5b54f0090de5540ed02` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 19.0 | 6 | 0.5 | `r-0925b86f96a976919154` | `r-a5b54f0090de5540ed02` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -19.216369628906676 | 4.14314 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-585cf49e62af00601f20` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 100.41315077975412 | 102.62144469209578 | 2.20829 | 2.00826 | `r-4ab59c3e1336e488abd6` | `r-585cf49e62af00601f20` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 11.969999999861272 | 11.18 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-585cf49e62af00601f20` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 35.05000000076507 | 16.46 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-585cf49e62af00601f20` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 57.0 | 18 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-585cf49e62af00601f20` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 372.14999999953375 | 24.06 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-ee947077f305902cec84` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 24.0 | 8 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-ee947077f305902cec84` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -20.017547607422486 | 4.01639 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-c9ca4459bc070b85e776` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 100.17234039630091 | 103.9221420296081 | 3.7498 | 2.00345 | `r-86c7a89ca0bbba8e93d0` | `r-c9ca4459bc070b85e776` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 3.9799999998685394 | 2.099999999870249 | 1.88 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-c9ca4459bc070b85e776` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.00018860807258438058 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-9cde5bbcfc6c21cc52dd` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -16.847518503369358 | 5.04345 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-9cde5bbcfc6c21cc52dd` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 100.07681274416072 | 102.51089096066909 | 2.43408 | 2.00281 | `r-1c8cea9109ae2bf6fdec` | `r-9cde5bbcfc6c21cc52dd` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 2.930000000000785 | 2.48 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-9cde5bbcfc6c21cc52dd` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 13.260000000005789 | 5.06 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-9cde5bbcfc6c21cc52dd` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 5.0 | 2 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-9cde5bbcfc6c21cc52dd` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -18.84056091308551 | 4.28667 | 0.738788 | `r-6797defd923ff2562240` | `r-a199b44fb12f64a8768f` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 100.0564460769101 | 102.27047728538103 | 2.21403 | 2.00937 | `r-6797defd923ff2562240` | `r-a199b44fb12f64a8768f` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 8.419999999864501 | 7.61 | 0.5 | `r-6797defd923ff2562240` | `r-a199b44fb12f64a8768f` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 27.05999999997539 | 12.99 | 0.8012 | `r-6797defd923ff2562240` | `r-a199b44fb12f64a8768f` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 19.0 | 6 | 0.5 | `r-6797defd923ff2562240` | `r-a199b44fb12f64a8768f` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -19.065933227538196 | 4.20914 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-ca0c31c548fea2a11e8a` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 100.03872680731578 | 102.29034042154893 | 2.25161 | 2.00826 | `r-a3b84bbc3dc843d0e573` | `r-ca0c31c548fea2a11e8a` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 11.929999999861309 | 11.18 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-ca0c31c548fea2a11e8a` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 35.03000000076463 | 16.53 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-ca0c31c548fea2a11e8a` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 57.0 | 18 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-ca0c31c548fea2a11e8a` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 372.0899999995338 | 24.06 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-badb83b00b6793a2c2f9` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 24.0 | 8 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-badb83b00b6793a2c2f9` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -15.791358947753906 | -19.882354736328935 | 4.091 | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-032c17dbba497444d428` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 99.86314392274174 | 103.6148033144069 | 3.75166 | 2.00345 | `r-2e410d8c71a4df0466e8` | `r-032c17dbba497444d428` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 3.9399999998685757 | 2.0699999998702765 | 1.87 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-032c17dbba497444d428` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
