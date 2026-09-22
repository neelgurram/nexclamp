# m-scale_capacitance-ae20afa58b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3104.757 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 0.00030609121538585085 |  | inf | `r-1855c6a207dcec8ed210` | `r-0fdb16624e73aa15e07c` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -13.498267671955162 | 1.64344 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-0fdb16624e73aa15e07c` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 4.4500000000010225 | 0.97 | 0.5 | `r-1855c6a207dcec8ed210` | `r-0fdb16624e73aa15e07c` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 16.340000000003407 | 1.99 | 0.5 | `r-1855c6a207dcec8ed210` | `r-0fdb16624e73aa15e07c` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-0fdb16624e73aa15e07c` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -16.295417785644744 | 1.51966 | 0.738788 | `r-0925b86f96a976919154` | `r-075e4fa58ef5ed447f02` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 13.019999999860318 | 3.05 | 0.5 | `r-0925b86f96a976919154` | `r-075e4fa58ef5ed447f02` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 34.81999999996833 | 5.24 | 0.8012 | `r-0925b86f96a976919154` | `r-075e4fa58ef5ed447f02` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 14.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-075e4fa58ef5ed447f02` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -16.580474853515625 | 1.50725 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-04491b81e26b0db74699` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 18.619999999855224 | 4.53 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-04491b81e26b0db74699` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 44.81000000097811 | 6.7 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-04491b81e26b0db74699` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 45.0 | 6 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-04491b81e26b0db74699` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 387.29999999951997 | 8.91 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-3765d9f27b166163459b` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 18.0 | 2 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-3765d9f27b166163459b` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -17.490432739257812 | 1.48927 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-8dc1416efa17821d9eb4` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 3.9799999998685394 | 3.1399999998693033 | 0.84 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-8dc1416efa17821d9eb4` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.0003062787138326014 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-85f47554196a18922114` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -13.45001285230343 | 1.64594 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-85f47554196a18922114` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 4.440000000001021 | 0.97 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-85f47554196a18922114` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 16.330000000003388 | 1.99 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-85f47554196a18922114` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-85f47554196a18922114` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -16.089004516602444 | 1.53511 | 0.738788 | `r-6797defd923ff2562240` | `r-93c97627eae4b8c76afe` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 12.979999999860354 | 3.05 | 0.5 | `r-6797defd923ff2562240` | `r-93c97627eae4b8c76afe` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 34.79999999996835 | 5.25 | 0.8012 | `r-6797defd923ff2562240` | `r-93c97627eae4b8c76afe` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 14.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-93c97627eae4b8c76afe` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -16.37900543212845 | 1.52221 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-aa769a95a2c94bc28849` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 18.57999999985526 | 4.53 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-aa769a95a2c94bc28849` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 44.83000000097854 | 6.73 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-aa769a95a2c94bc28849` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 45.0 | 6 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-aa769a95a2c94bc28849` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 387.24999999952 | 8.9 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-57bbb84e43a037c1c47e` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 18.0 | 2 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-57bbb84e43a037c1c47e` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -15.791358947753906 | -17.293289184570312 | 1.50193 | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-e64836d43ee1699ff0c7` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 3.9399999998685757 | 3.1099999998693306 | 0.83 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-e64836d43ee1699ff0c7` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
