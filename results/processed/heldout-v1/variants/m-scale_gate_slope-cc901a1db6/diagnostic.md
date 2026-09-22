# m-scale_gate_slope-cc901a1db6

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/forwardRate[1]", "new": "5.76mV", "old": "7.2mV"}, {"attribute": "scale", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/reverseRate[1]", "new": "-5.76mV", "old": "-7.2mV"}], "channel": "na3", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/na3.channel.nml", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/forwardRate[1]", "attribute": "scale", "old": "7.2mV", "new": "5.76mV", "action": "set", "note": "scale_gate_slope"}, {"file": "neuroConstruct/generatedNeuroML2/na3.channel.nml", "locator": "/neuroml[@id='na3']/ionChannel[@id='na3']/gate[@id='m']/reverseRate[1]", "attribute": "scale", "old": "-7.2mV", "new": "-5.76mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3115.432 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 5.97000000000126 | 0.55 | 0.5 | `r-1855c6a207dcec8ed210` | `r-d6c235a4156b58ab3147` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 18.94999999999623 | 0.62 | 0.5 | `r-1855c6a207dcec8ed210` | `r-d6c235a4156b58ab3147` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0007513148009015778 | 0.000170753 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-e99f47c737df56fdd34b` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 20.519999999853496 | 4.45 | 0.5 | `r-0925b86f96a976919154` | `r-c92f8d36ed853eaa2f71` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 46.139999999958036 | 6.08 | 0.8012 | `r-0925b86f96a976919154` | `r-c92f8d36ed853eaa2f71` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 11.0 | 2 | 0.5 | `r-0925b86f96a976919154` | `r-c92f8d36ed853eaa2f71` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 35.55999999983982 | 12.41 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-f6e9a6e186b1c40d6fb5` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 71.66000000156419 | 20.15 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-f6e9a6e186b1c40d6fb5` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 28.0 | 11 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-f6e9a6e186b1c40d6fb5` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 509.5099999994088 | 113.3 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-46429ca71ea5a1d25439` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 12.0 | 4 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-46429ca71ea5a1d25439` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 3.9799999998685394 | 4.5999999998679755 | 0.62 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-c615173ffc6adc5beabb` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 5.97000000000126 | 0.56 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-f0fab0ac1b61083ee7cc` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 18.939999999996232 | 0.62 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-f0fab0ac1b61083ee7cc` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0007513148009015778 | 0.000170753 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-61158d11cee85f06d490` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 20.479999999853533 | 4.45 | 0.5 | `r-6797defd923ff2562240` | `r-5dd22cfb9c10cafb0252` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 46.14999999995803 | 6.1 | 0.8012 | `r-6797defd923ff2562240` | `r-5dd22cfb9c10cafb0252` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 11.0 | 2 | 0.5 | `r-6797defd923ff2562240` | `r-5dd22cfb9c10cafb0252` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 35.519999999839854 | 12.41 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-fbaa1b135f5dc0f1e0a4` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 71.86000000156855 | 20.3 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-fbaa1b135f5dc0f1e0a4` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 28.0 | 11 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-fbaa1b135f5dc0f1e0a4` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 509.4499999994089 | 113.3 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-95aef1c3b68dcf11a489` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 12.0 | 4 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-95aef1c3b68dcf11a489` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 3.9399999998685757 | 4.559999999868012 | 0.62 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-d56f6be03cac74f6c9f7` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
