# m-shift_reversal-754db6a01c

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "new": "-87mV", "old": "-77mV"}], "element": "channelDensity", "element_id": "kChans", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "attribute": "erev", "old": "-77mV", "new": "-87mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 603.431 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | -7.74713208133793e-05 | None |  | 0.01 | `r-5f0a94c66ff17cd98a0a` | `r-a040d88c7eb8310ebb81` |
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -17.597587585449148 | 7.25445 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-a040d88c7eb8310ebb81` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 97.2597160337371 | 2.12024 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-a040d88c7eb8310ebb81` |
| h/1 | P00_canonical | last_isi | definedness | 16.12999999998533 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-a040d88c7eb8310ebb81` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-a040d88c7eb8310ebb81` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -66.51249044036852 | 2.42938 | 0.5 | `r-66b1007575e04915ac55` | `r-7b06c29970edadbead68` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.036097261116043985 | 0.0136603 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-2cdc45ea88f95dd5d50d` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -17.929626464843338 | 7.23169 | 0.534897 | `r-66b1007575e04915ac55` | `r-7b06c29970edadbead68` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 4.509999999868057 | 0.97 | 0.5 | `r-66b1007575e04915ac55` | `r-7b06c29970edadbead68` |
| h/1 | P05_long_step | ahp_depth | definedness | -10.81385040282855 | None |  | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-9fbe90a1f98a6425f141` |
| h/1 | P05_long_step | ap_amplitude | definedness | 91.2126808181487 | None |  | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-9fbe90a1f98a6425f141` |
| h/1 | P05_long_step | first_spike_latency | definedness | 4.42999999986813 | None |  | 0.5 | `r-940eedfaa66e3fa96c16` | `r-9fbe90a1f98a6425f141` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-9fbe90a1f98a6425f141` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -69.38664021301295 | 2.12402 | 0.5 | `r-66b1007575e04915ac55` | `r-7b06c29970edadbead68` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 8.389999999409838 | 3.17 | 0.5 | `r-011ab0e03522b12f620c` | `r-f75936e874900756853b` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -18.492134094239887 | 7.26556 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-b340113ce1f31dc049e2` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 110.62486267049181 | 4.16673 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-b340113ce1f31dc049e2` |
| h/2 | P00_canonical | adaptation_index | definedness | -1.02201355559918e-13 | None |  | 0.01 | `r-d4235ef154cdc2eeb44c` | `r-e93bdc9328cbe9377bae` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -17.572259801965075 | 7.24456 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-e93bdc9328cbe9377bae` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 97.41097640977611 | 2.11391 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-e93bdc9328cbe9377bae` |
| h/2 | P00_canonical | last_isi | definedness | 16.059999999985394 | None |  | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-e93bdc9328cbe9377bae` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-e93bdc9328cbe9377bae` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -66.51248988037096 | 2.42938 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-ef56154345f1d065e7d1` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.036097261116043985 | 0.0136944 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-534561534a6c4980345f` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -17.918846130365353 | 7.2272 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-ef56154345f1d065e7d1` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 4.469999999868094 | 0.96 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-ef56154345f1d065e7d1` |
| h/2 | P05_long_step | ahp_depth | definedness | -10.808036804201677 | None |  | 0.540693 | `r-a455ac42295a97429d02` | `r-c9a5c024078070d1c9b4` |
| h/2 | P05_long_step | ap_amplitude | definedness | 91.37988662862392 | None |  | 1.82425 | `r-a455ac42295a97429d02` | `r-c9a5c024078070d1c9b4` |
| h/2 | P05_long_step | first_spike_latency | definedness | 4.3899999998681665 | None |  | 0.5 | `r-a455ac42295a97429d02` | `r-c9a5c024078070d1c9b4` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-a455ac42295a97429d02` | `r-c9a5c024078070d1c9b4` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -69.38664133453395 | 2.12402 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-ef56154345f1d065e7d1` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 8.329999999409893 | 3.14 | 0.5 | `r-a628bd90e08153ec217d` | `r-eb45175d54e6318335fb` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -18.484344482422273 | 7.26186 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-9d2449c256c8540f13d1` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 110.60368347188374 | 4.16402 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-9d2449c256c8540f13d1` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
