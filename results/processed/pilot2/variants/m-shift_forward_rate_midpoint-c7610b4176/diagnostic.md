# m-shift_forward_rate_midpoint-c7610b4176

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='h']/forwardRate[1]", "new": "-70mV", "old": "-65mV"}], "channel": "naChan", "delta_mV": -5.0, "gate": "h", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='h']/forwardRate[1]", "attribute": "midpoint", "old": "-65mV", "new": "-70mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 585.058 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | -7.74713208133793e-05 | None |  | 0.01 | `r-5f0a94c66ff17cd98a0a` | `r-285828059396e31e9dae` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 93.20496368385139 | 1.93451 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-285828059396e31e9dae` |
| h/1 | P00_canonical | last_isi | definedness | 16.12999999998533 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-285828059396e31e9dae` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-285828059396e31e9dae` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.02673997677754252 | 0.00430298 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-707f1654e3017c324f36` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 90.14554977562213 | 2.57879 | 1.85449 | `r-66b1007575e04915ac55` | `r-ad68ab64e19c65513c12` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 87.91174698008928 | 3.30093 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-67442acc2497737be74d` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 5.0199999998675935 | 0.59 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-67442acc2497737be74d` |
| h/2 | P00_canonical | adaptation_index | definedness | -1.02201355559918e-13 | None |  | 0.01 | `r-d4235ef154cdc2eeb44c` | `r-527fe532a0690ebf792f` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 93.37361526471864 | 1.92345 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-527fe532a0690ebf792f` |
| h/2 | P00_canonical | last_isi | definedness | 16.059999999985394 | None |  | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-527fe532a0690ebf792f` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-527fe532a0690ebf792f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.026705826104774268 | 0.00430298 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-edc2a1cf07df1d5f7415` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 90.25291824446273 | 2.57267 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-fc8c785c1e1e5a225b20` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 88.05835724030793 | 3.32153 | 1.82425 | `r-a455ac42295a97429d02` | `r-066477017318d3b90778` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 4.97999999986763 | 0.59 | 0.5 | `r-a455ac42295a97429d02` | `r-066477017318d3b90778` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
