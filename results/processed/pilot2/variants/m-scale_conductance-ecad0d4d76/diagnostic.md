# m-scale_conductance-ecad0d4d76

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "new": "720 S_per_m2", "old": "360 S_per_m2"}], "element": "channelDensity", "element_id": "kChans", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='kChans']", "attribute": "condDensity", "old": "360 S_per_m2", "new": "720 S_per_m2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 606.475 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | -7.74713208133793e-05 | None |  | 0.01 | `r-5f0a94c66ff17cd98a0a` | `r-14538a484e5a4f9e53ef` |
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -8.686027526854843 | 1.65711 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-14538a484e5a4f9e53ef` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 87.70999908427004 | 7.42948 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-14538a484e5a4f9e53ef` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.5200000000155427 | 3.400000000015993 | 0.88 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-14538a484e5a4f9e53ef` |
| h/1 | P00_canonical | last_isi | definedness | 16.12999999998533 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-14538a484e5a4f9e53ef` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-14538a484e5a4f9e53ef` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -66.58812825927721 | 2.50502 | 0.5 | `r-66b1007575e04915ac55` | `r-e8ceec13f97b813ccc54` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.05829519841540879 | 0.0358582 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-edba8169430ff96b820b` |
| h/1 | P04_step_2x | ahp_depth | definedness | -10.697937011716306 | None |  | 0.534897 | `r-66b1007575e04915ac55` | `r-e8ceec13f97b813ccc54` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 92.72434234740876 | None |  | 1.85449 | `r-66b1007575e04915ac55` | `r-e8ceec13f97b813ccc54` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 3.5399999998689395 | None |  | 0.5 | `r-66b1007575e04915ac55` | `r-e8ceec13f97b813ccc54` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-66b1007575e04915ac55` | `r-e8ceec13f97b813ccc54` |
| h/1 | P05_long_step | ahp_depth | definedness | -10.81385040282855 | None |  | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-19ac20d0f6b5f40acb03` |
| h/1 | P05_long_step | ap_amplitude | definedness | 91.2126808181487 | None |  | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-19ac20d0f6b5f40acb03` |
| h/1 | P05_long_step | first_spike_latency | definedness | 4.42999999986813 | None |  | 0.5 | `r-940eedfaa66e3fa96c16` | `r-19ac20d0f6b5f40acb03` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-19ac20d0f6b5f40acb03` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -69.0425774063113 | 1.77996 | 0.5 | `r-66b1007575e04915ac55` | `r-e8ceec13f97b813ccc54` |
| h/1 | P08_rebound | first_spike_latency | definedness | 5.219999999412721 | None |  | 0.5 | `r-011ab0e03522b12f620c` | `r-c5a2180fe5a75166e45b` |
| h/1 | P08_rebound | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-011ab0e03522b12f620c` | `r-c5a2180fe5a75166e45b` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -9.241149902342741 | 1.98543 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-74ba038669c7ba4182a2` |
| h/2 | P00_canonical | adaptation_index | definedness | -1.02201355559918e-13 | None |  | 0.01 | `r-d4235ef154cdc2eeb44c` | `r-2efc3d5325d681e22003` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -8.675126928430316 | 1.65257 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-2efc3d5325d681e22003` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 88.00579071031586 | 7.29128 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-2efc3d5325d681e22003` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.460000000015512 | 3.330000000015957 | 0.87 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-2efc3d5325d681e22003` |
| h/2 | P00_canonical | last_isi | definedness | 16.059999999985394 | None |  | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-2efc3d5325d681e22003` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-2efc3d5325d681e22003` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -66.58812769927965 | 2.50502 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-a149378a0c90bc9509b6` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.05822689706987228 | 0.0358241 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-e14b4bafc8a83b92dda0` |
| h/2 | P04_step_2x | ahp_depth | definedness | -10.691650390625 | None |  | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-a149378a0c90bc9509b6` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 92.82558822777118 | None |  | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-a149378a0c90bc9509b6` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 3.509999999868967 | None |  | 0.5 | `r-8d6f46142acd4ec898a7` | `r-a149378a0c90bc9509b6` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-a149378a0c90bc9509b6` |
| h/2 | P05_long_step | ahp_depth | definedness | -10.808036804201677 | None |  | 0.540693 | `r-a455ac42295a97429d02` | `r-3d3d2d06c109041ba48e` |
| h/2 | P05_long_step | ap_amplitude | definedness | 91.37988662862392 | None |  | 1.82425 | `r-a455ac42295a97429d02` | `r-3d3d2d06c109041ba48e` |
| h/2 | P05_long_step | first_spike_latency | definedness | 4.3899999998681665 | None |  | 0.5 | `r-a455ac42295a97429d02` | `r-3d3d2d06c109041ba48e` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-a455ac42295a97429d02` | `r-3d3d2d06c109041ba48e` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -69.04257852935817 | 1.77996 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-a149378a0c90bc9509b6` |
| h/2 | P08_rebound | first_spike_latency | definedness | 5.189999999412748 | None |  | 0.5 | `r-a628bd90e08153ec217d` | `r-7d3265a7a65959603af6` |
| h/2 | P08_rebound | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-a628bd90e08153ec217d` | `r-7d3265a7a65959603af6` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -9.23831939697186 | 1.98417 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-38856f6e8732ae6f0fca` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
