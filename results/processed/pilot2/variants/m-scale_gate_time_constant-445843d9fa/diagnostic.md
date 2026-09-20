# m-scale_gate_time_constant-445843d9fa

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/forwardRate[1]", "new": "0.2per_ms", "old": "0.1per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "new": "0.25per_ms", "old": "0.125per_ms"}], "channel": "kChan", "factor": 2.0, "gate": "n", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/forwardRate[1]", "attribute": "rate", "old": "0.1per_ms", "new": "0.2per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "attribute": "rate", "old": "0.125per_ms", "new": "0.25per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 590.308 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | -7.74713208133793e-05 | None |  | 0.01 | `r-5f0a94c66ff17cd98a0a` | `r-ba63a7ac600e78163ca1` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 82.68288040134473 | 12.4566 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-ba63a7ac600e78163ca1` |
| h/1 | P00_canonical | last_isi | definedness | 16.12999999998533 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-ba63a7ac600e78163ca1` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-ba63a7ac600e78163ca1` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.03712178129909159 | 0.0146848 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-a810dba0f0d0cd6ad968` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 76.93221664566371 | 15.7921 | 1.85449 | `r-66b1007575e04915ac55` | `r-313113e82b24975d1f16` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 4.269999999868276 | 0.73 | 0.5 | `r-66b1007575e04915ac55` | `r-313113e82b24975d1f16` |
| h/1 | P05_long_step | ahp_depth | definedness | -10.81385040282855 | None |  | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-6d79253f360c8c73504c` |
| h/1 | P05_long_step | ap_amplitude | definedness | 91.2126808181487 | None |  | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-6d79253f360c8c73504c` |
| h/1 | P05_long_step | first_spike_latency | definedness | 4.42999999986813 | None |  | 0.5 | `r-940eedfaa66e3fa96c16` | `r-6d79253f360c8c73504c` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-6d79253f360c8c73504c` |
| h/1 | P08_rebound | first_spike_latency | definedness | 5.219999999412721 | None |  | 0.5 | `r-011ab0e03522b12f620c` | `r-899f2ae1e670971f9f6c` |
| h/1 | P08_rebound | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-011ab0e03522b12f620c` | `r-899f2ae1e670971f9f6c` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 96.93506240798342 | 9.52307 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-8f613af3fb5fc59f4025` |
| h/2 | P00_canonical | adaptation_index | definedness | -1.02201355559918e-13 | None |  | 0.01 | `r-d4235ef154cdc2eeb44c` | `r-a37e92ebfea1d8fcdf5c` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 82.95370101907058 | 12.3434 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-a37e92ebfea1d8fcdf5c` |
| h/2 | P00_canonical | last_isi | definedness | 16.059999999985394 | None |  | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-a37e92ebfea1d8fcdf5c` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-a37e92ebfea1d8fcdf5c` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.037087630626323344 | 0.0146848 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-15785c54b168c331ab7a` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 77.0857467666844 | 15.7398 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-cca104b0a313e73aea89` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 4.229999999868312 | 0.72 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-cca104b0a313e73aea89` |
| h/2 | P05_long_step | ahp_depth | definedness | -10.808036804201677 | None |  | 0.540693 | `r-a455ac42295a97429d02` | `r-d56f0717ee25658594a5` |
| h/2 | P05_long_step | ap_amplitude | definedness | 91.37988662862392 | None |  | 1.82425 | `r-a455ac42295a97429d02` | `r-d56f0717ee25658594a5` |
| h/2 | P05_long_step | first_spike_latency | definedness | 4.3899999998681665 | None |  | 0.5 | `r-a455ac42295a97429d02` | `r-d56f0717ee25658594a5` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-a455ac42295a97429d02` | `r-d56f0717ee25658594a5` |
| h/2 | P08_rebound | first_spike_latency | definedness | 5.189999999412748 | None |  | 0.5 | `r-a628bd90e08153ec217d` | `r-3321153f4a69bca3c5fd` |
| h/2 | P08_rebound | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-a628bd90e08153ec217d` | `r-3321153f4a69bca3c5fd` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 96.9385852808332 | 9.50108 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-91306cc7baae45a60967` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
