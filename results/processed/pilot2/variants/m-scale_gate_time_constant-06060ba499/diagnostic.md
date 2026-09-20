# m-scale_gate_time_constant-06060ba499

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "new": "0.8per_ms", "old": "1per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "new": "3.2per_ms", "old": "4per_ms"}], "channel": "naChan", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "attribute": "rate", "old": "1per_ms", "new": "0.8per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "attribute": "rate", "old": "4per_ms", "new": "3.2per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 594.257 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 91.06696701032519 | 4.07251 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-b16953fd241b4ec6c6fa` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 17.13999999998441 | 1.01 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-b16953fd241b4ec6c6fa` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-b16953fd241b4ec6c6fa` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.02387132026500922 | 0.00143433 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-38bf4f956c230b370785` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 88.27207565449204 | 4.45227 | 1.85449 | `r-66b1007575e04915ac55` | `r-b67d59f82321dd3c1e21` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 86.39547348131507 | 4.81721 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-1fe5fd86c0b576758e6e` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 103.7668380735503 | 2.69129 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-2da8b4900ab5dbc22a34` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 91.26408767681451 | 4.03298 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-3ef6e399186a980fef7f` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 17.069999999984475 | 1.01 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-3ef6e399186a980fef7f` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-3ef6e399186a980fef7f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.02383716959224097 | 0.00143433 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-5ea5f86a68fb970411eb` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 88.40050506693555 | 4.42508 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-08e0880f835a6b1f53cd` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 86.58028411973665 | 4.7996 | 1.82425 | `r-a455ac42295a97429d02` | `r-932d409146f2c8304b6d` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 103.7640380856736 | 2.67562 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-78b50c56ce5d4a051c7e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
