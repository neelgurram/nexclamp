# m-scale_conductance-1b265d3832

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='leak']", "new": "1.5 S_per_m2", "old": "3.0 S_per_m2"}], "element": "channelDensity", "element_id": "leak", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='leak']", "attribute": "condDensity", "old": "3.0 S_per_m2", "new": "1.5 S_per_m2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 589.814 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -8.873893737792486 | 1.46925 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-5e4602f7a5fde45ad8c0` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 99.343551635518 | 4.20407 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-5e4602f7a5fde45ad8c0` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 15.559999999985848 | 0.57 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-5e4602f7a5fde45ad8c0` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -65.46508901214587 | 1.38198 | 0.5 | `r-66b1007575e04915ac55` | `r-c1a9df196abc768929bb` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.018475513967625163 | 0.00396148 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-4be126023de633a08f88` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -9.237709045410568 | 1.46023 | 0.534897 | `r-66b1007575e04915ac55` | `r-c1a9df196abc768929bb` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 96.86502838224905 | 4.14069 | 1.85449 | `r-66b1007575e04915ac55` | `r-c1a9df196abc768929bb` |
| h/1 | P04_step_2x | last_isi | definedness | None | 21.389999999980546 |  | inf | `r-66b1007575e04915ac55` | `r-c1a9df196abc768929bb` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-66b1007575e04915ac55` | `r-c1a9df196abc768929bb` |
| h/1 | P05_long_step | ahp_depth | exceeds | -10.81385040282855 | -9.358627319333678 | 1.45522 | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-9e5fe736df5c5bea743d` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 95.70197296221296 | 4.48929 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-9e5fe736df5c5bea743d` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -71.52004780426051 | 4.25743 | 0.5 | `r-66b1007575e04915ac55` | `r-c1a9df196abc768929bb` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 9.249999999409056 | 4.03 | 0.5 | `r-011ab0e03522b12f620c` | `r-d3209ec16b2076623fa3` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -9.75894927978375 | 1.46763 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-c2e1c6a3b76825cae70f` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 110.71009826675912 | 4.25197 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-c2e1c6a3b76825cae70f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -8.861329938981442 | 1.46637 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-fbb1c18b3a3edeb5bd90` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 99.50832748399026 | 4.21126 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-fbb1c18b3a3edeb5bd90` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 15.489999999985912 | 0.57 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-fbb1c18b3a3edeb5bd90` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -65.46508845214831 | 1.38198 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-bade57540971c422b072` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.018475513967625163 | 0.00392733 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-b4c9a47c9ea9af884c5a` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -9.232978820801591 | 1.45867 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-bade57540971c422b072` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 96.87511825655773 | 4.04953 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-bade57540971c422b072` |
| h/2 | P04_step_2x | last_isi | definedness | None | 21.379999999980555 |  | inf | `r-8d6f46142acd4ec898a7` | `r-bade57540971c422b072` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-bade57540971c422b072` |
| h/2 | P05_long_step | ahp_depth | exceeds | -10.808036804201677 | -9.354431152343338 | 1.45361 | 0.540693 | `r-a455ac42295a97429d02` | `r-1fb8c348916118c23921` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 95.7899093639009 | 4.41002 | 1.82425 | `r-a455ac42295a97429d02` | `r-1fb8c348916118c23921` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -71.52004892730739 | 4.25743 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-bade57540971c422b072` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 9.219999999409083 | 4.03 | 0.5 | `r-a628bd90e08153ec217d` | `r-eac65a1604b0e5a7d573` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -9.756576538086335 | 1.46591 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-6378979095dfd7c5bd36` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 110.689941406277 | 4.25028 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-6378979095dfd7c5bd36` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
