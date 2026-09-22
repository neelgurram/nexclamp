# m-shift_gate_midpoint-81196088fb

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/forwardRate[1]", "new": "-35mV", "old": "-30mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/reverseRate[1]", "new": "-35mV", "old": "-30mV"}], "channel": "na3", "delta_mV": -5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/na3.channel.nml", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-35mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/na3.channel.nml", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-35mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1081.467 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 1.354866896513827e-13 |  | inf | `r-1855c6a207dcec8ed210` | `r-1ce2b5f7276c48a18f08` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -16.65012646195902 | 4.7953 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-1ce2b5f7276c48a18f08` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.14028549194009 | 102.16909790037448 | 2.02881 | 2.00281 | `r-1855c6a207dcec8ed210` | `r-1ce2b5f7276c48a18f08` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 1.280000000000527 | 4.14 | 0.5 | `r-1855c6a207dcec8ed210` | `r-1ce2b5f7276c48a18f08` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 16.310000000001175 | 2.02 | 0.5 | `r-1855c6a207dcec8ed210` | `r-1ce2b5f7276c48a18f08` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-1ce2b5f7276c48a18f08` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 11.0 | 11 | 0.5 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -67.41837256275734 | 2.39555 | 0.5 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0 | 0.000580561 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-1a95cf1515a27388a6f3` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -11.182989466563356 | 3.59277 | 0.738788 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 100.46828841971717 | 102.51179504303363 | 2.04351 | 2.00937 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 10.229999999862855 | 5.84 | 0.5 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 29.04999999997358 | 11.01 | 0.8012 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 17.0 | 4 | 0.5 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -11.497091639414464 | 3.57614 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-be81cda10cea2b352c37` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 12.109999999861145 | 11.04 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-be81cda10cea2b352c37` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 32.65000000071268 | 18.86 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-be81cda10cea2b352c37` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 61.0 | 22 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-be81cda10cea2b352c37` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 32.8299999998423 | 363.38 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-1221edf44aedfff579d8` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 30.0 | 14 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-1221edf44aedfff579d8` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533750000003 | -67.58251920166019 | 0.552818 | 0.5 | `r-0925b86f96a976919154` | `r-280afe8fe4931ef54c72` |
| h/1 | P08_rebound | first_spike_latency | definedness | None | 24.829999999394886 |  | inf | `r-ff3ac53d55743f982ac3` | `r-9b63203f87866f511289` |
| h/1 | P08_rebound | spike_count | exceeds | 0.0 | 5.0 | 5 | 0.5 | `r-ff3ac53d55743f982ac3` | `r-9b63203f87866f511289` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -12.40209041871222 | 3.59907 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-d6892dbc481d5fb252d2` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.0003068425898861555 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-a0facf959f60d525b261` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -16.599610266993906 | 4.79554 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-a0facf959f60d525b261` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 1.2700000000005254 | 4.14 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-a0facf959f60d525b261` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 16.30000000000115 | 2.02 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-a0facf959f60d525b261` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-a0facf959f60d525b261` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 11.0 | 11 | 0.5 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -67.3877360424673 | 2.36491 | 0.5 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0 | 0.000580561 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-52a18ad25a138c11334c` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -11.123736276381166 | 3.43016 | 0.738788 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 100.0564460769101 | 102.11405944718248 | 2.05761 | 2.00937 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 10.339999999862755 | 5.69 | 0.5 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 28.989999999973634 | 11.06 | 0.8012 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 17.0 | 4 | 0.5 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -11.443903817885499 | 3.41289 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-7c21ef9fcd0490463caf` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 12.249999999861018 | 10.86 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-7c21ef9fcd0490463caf` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 32.620000000712025 | 18.94 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-7c21ef9fcd0490463caf` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 61.0 | 22 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-7c21ef9fcd0490463caf` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 33.25999999984191 | 362.89 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-8042db11894642a96a96` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 30.0 | 14 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-8042db11894642a96a96` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533766326908 | -67.58251936798099 | 0.552818 | 0.5 | `r-6797defd923ff2562240` | `r-9af43dd1108db1d9954d` |
| h/2 | P08_rebound | first_spike_latency | definedness | None | 24.789999999394922 |  | inf | `r-5841cbe01fb53bd3f5cf` | `r-b9cab24d3623e94a8bbe` |
| h/2 | P08_rebound | spike_count | exceeds | 0.0 | 5.0 | 5 | 0.5 | `r-5841cbe01fb53bd3f5cf` | `r-b9cab24d3623e94a8bbe` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -15.791358947753906 | -12.357020272964064 | 3.43434 | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-05c6732885d6857920af` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
