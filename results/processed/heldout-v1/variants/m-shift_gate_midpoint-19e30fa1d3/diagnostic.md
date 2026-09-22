# m-shift_gate_midpoint-19e30fa1d3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "new": "-30mV", "old": "-20mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "new": "-53mV", "old": "-43mV"}], "channel": "km", "delta_mV": -10.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-20mV", "new": "-30mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml[@id='km']/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-43mV", "new": "-53mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8037.529 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.5216693418942094 | None |  | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-ca793cca85b271f964d7` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 24.74000000000501 | 1.04 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-ca793cca85b271f964d7` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-ca793cca85b271f964d7` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.06444231951369442 | 0.00300526 | 0.00122874 | `s-fa4d0c2502716e8c3739` | `s-1bfb2824dd9584071c80` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.004339763314966122 | 0.027370403653273943 | 0.0230306 | 0.0101709 | `r-96e71f2e3b8549494d50` | `r-e0bde9ee3df238c72ac7` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 29.879999999844983 | 0.78 | 0.582 | `r-96e71f2e3b8549494d50` | `r-e0bde9ee3df238c72ac7` |
| h/1 | P04_step_2x | last_isi | exceeds | 8.209999999992533 | 21.729999999980237 | 13.52 | 8.67 | `r-96e71f2e3b8549494d50` | `r-e0bde9ee3df238c72ac7` |
| h/1 | P04_step_2x | spike_count | exceeds | 51.0 | 25.0 | 26 | 3 | `r-96e71f2e3b8549494d50` | `r-e0bde9ee3df238c72ac7` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 44.38999999983179 | 1.5 | 0.8578 | `r-74af15e68cf19cbae102` | `r-d2e8a84f94bc83a1e3d0` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 58.190000001270164 | 33.72 | 1.11 | `r-74af15e68cf19cbae102` | `r-d2e8a84f94bc83a1e3d0` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 36.0 | 47 | 3 | `r-74af15e68cf19cbae102` | `r-d2e8a84f94bc83a1e3d0` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 382.869999999524 | 399.379999999509 | 16.51 | 7.6574 | `r-6afcc4c87334b55f282e` | `r-22cc9606784b0af00f5d` |
| h/1 | P06_ramp | spike_count | exceeds | 70.0 | 40.0 | 30 | 3 | `r-6afcc4c87334b55f282e` | `r-22cc9606784b0af00f5d` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.5214881334190068 | None |  | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-cf0aaf1c4987e344d59a` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 24.780000000005025 | 1.06 | 0.5 | `r-87bcc3cd30685deaf603` | `r-cf0aaf1c4987e344d59a` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-87bcc3cd30685deaf603` | `r-cf0aaf1c4987e344d59a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.06444231951369442 | 0.00300526 | 0.00122874 | `s-54b0d60082a59a1582ae` | `s-7896cdc689eec73b09f5` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.007730072408027383 | 0.027692168561442264 | 0.0199621 | 0.0101709 | `r-6290d36f97e6ddeb2b58` | `r-ca13f08baa8eb7e940f7` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 29.029999999845757 | 29.799999999845056 | 0.77 | 0.582 | `r-6290d36f97e6ddeb2b58` | `r-ca13f08baa8eb7e940f7` |
| h/2 | P04_step_2x | last_isi | exceeds | 11.099999999989905 | 22.039999999979955 | 10.94 | 8.67 | `r-6290d36f97e6ddeb2b58` | `r-ca13f08baa8eb7e940f7` |
| h/2 | P04_step_2x | spike_count | exceeds | 50.0 | 25.0 | 25 | 3 | `r-6290d36f97e6ddeb2b58` | `r-ca13f08baa8eb7e940f7` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 44.31999999983185 | 1.5 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-be1c86c834ab5eef2032` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 58.940000001286535 | 34.1 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-be1c86c834ab5eef2032` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 36.0 | 46 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-be1c86c834ab5eef2032` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 382.78999999952407 | 399.29999999950905 | 16.51 | 7.6574 | `r-ce6273bb85e534e50ecc` | `r-4d18d243cd1e8b1262b4` |
| h/2 | P06_ramp | spike_count | exceeds | 69.0 | 39.0 | 30 | 3 | `r-ce6273bb85e534e50ecc` | `r-4d18d243cd1e8b1262b4` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
