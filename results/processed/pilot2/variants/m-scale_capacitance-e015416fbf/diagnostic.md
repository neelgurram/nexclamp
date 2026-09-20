# m-scale_capacitance-e015416fbf

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 606.371 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 106.54727935768 | 11.4078 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-05ee1b09bc7fa73032b3` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.5200000000155427 | 1.6500000000150976 | 0.87 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-05ee1b09bc7fa73032b3` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 14.939999999986412 | 1.19 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-05ee1b09bc7fa73032b3` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.015777610818933134 | 0.00665938 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-f82fa8fc0fcda59eeaee` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 97.59160614109814 | 4.86726 | 1.85449 | `r-66b1007575e04915ac55` | `r-84ec206da21c9b4d9c32` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 2.1999999998701583 | 1.34 | 0.5 | `r-66b1007575e04915ac55` | `r-84ec206da21c9b4d9c32` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 96.6381721508676 | 5.42549 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-a4f61a55211f85270455` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 2.639999999869758 | 1.79 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-a4f61a55211f85270455` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 2.929999999414804 | 2.29 | 0.5 | `r-011ab0e03522b12f620c` | `r-846fba9437a8895f47af` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 106.67462158180226 | 11.3776 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-714e0c8a0a3353751312` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.460000000015512 | 1.600000000015072 | 0.86 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-714e0c8a0a3353751312` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 14.859999999986485 | 1.2 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-714e0c8a0a3353751312` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.01574346014616488 | 0.00665938 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-e609e3b2caf1c8c7da7d` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 97.75154495339021 | 4.92596 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-13c2dbfc23b30baf32b9` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 2.1699999998701855 | 1.34 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-13c2dbfc23b30baf32b9` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 96.6611557021804 | 5.28127 | 1.82425 | `r-a455ac42295a97429d02` | `r-932da7ca296d5ee1fccb` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 2.6099999998697854 | 1.78 | 0.5 | `r-a455ac42295a97429d02` | `r-932da7ca296d5ee1fccb` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 2.899999999414831 | 2.29 | 0.5 | `r-a628bd90e08153ec217d` | `r-7aecf1665cf17aa1f60d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
