# m-scale_gate_slope-6f355edc68

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "new": "12.5mV", "old": "10mV"}, {"attribute": "scale", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "new": "-22.5mV", "old": "-18mV"}], "channel": "naChan", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/forwardRate[1]", "attribute": "scale", "old": "10mV", "new": "12.5mV", "action": "set", "note": "scale_gate_slope"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='naChan']/gateHHrates[@id='m']/reverseRate[1]", "attribute": "scale", "old": "-18mV", "new": "-22.5mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 254.777 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -23.00288783366684 | 12.6597 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 81.40997505163996 | 13.7295 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.5200000000155427 | 7.180000000017927 | 4.66 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 12.859999999988304 | 3.27 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-89ab37845776d6dde041` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 30.0 | 30 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -59.08461007939556 | 4.9985 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.0 | 0.022437 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-b805716222206afd104c` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | -1.1015156855833627e-05 |  | inf | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -16.907464818449988 | 6.20953 | 0.534897 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 90.01217651488619 | 2.71217 | 1.85449 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 4.119999999868412 | 0.58 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | last_isi | definedness | None | 14.179999999987103 |  | inf | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 35.0 | 34 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P05_long_step | adaptation_index | definedness | None | -2.558513110684687e-06 |  | inf | `r-940eedfaa66e3fa96c16` | `r-6fc1de645d5762cf8025` |
| h/1 | P05_long_step | ahp_depth | exceeds | -10.81385040282855 | -17.037027196378638 | 6.22318 | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-6fc1de645d5762cf8025` |
| h/1 | P05_long_step | last_isi | definedness | None | 14.800000000323053 |  | inf | `r-940eedfaa66e3fa96c16` | `r-6fc1de645d5762cf8025` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 135.0 | 134 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-6fc1de645d5762cf8025` |
| h/1 | P06_ramp | first_spike_latency | definedness | None | 8.50999999986442 |  | inf | `r-b32245eb811666b0240b` | `r-fef1b973a424c6c8bb0f` |
| h/1 | P06_ramp | spike_count | exceeds | 0.0 | 67.0 | 67 | 0.5 | `r-b32245eb811666b0240b` | `r-fef1b973a424c6c8bb0f` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -65.33900990142848 | 1.92361 | 0.5 | `r-66b1007575e04915ac55` | `r-6489506df8371ec997e1` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 3.5199999994142672 | 1.7 | 0.5 | `r-011ab0e03522b12f620c` | `r-0bf2ff10ef2fa6a2e66d` |
| h/1 | P08_rebound | spike_count | exceeds | 1.0 | 17.0 | 16 | 0.5 | `r-011ab0e03522b12f620c` | `r-0bf2ff10ef2fa6a2e66d` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -17.458368138766367 | 6.23179 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-86644dc4156effcfb1cf` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 4.0 | 3 | 0.5 | `r-efc8f2fd727ba1854c5f` | `r-86644dc4156effcfb1cf` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -22.35773269577186 | 12.03 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-23f1af5782ede052af8a` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 82.28215026837222 | 13.0149 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-23f1af5782ede052af8a` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.460000000015512 | 6.350000000017502 | 3.89 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-23f1af5782ede052af8a` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 12.789999999988368 | 3.27 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-23f1af5782ede052af8a` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-23f1af5782ede052af8a` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 30.0 | 30 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -59.030417102250226 | 5.05269 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.0 | 0.0224028 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-35bf6f3b0291a5120d07` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | -1.0711569566288549e-05 |  | inf | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -16.66397058286234 | 5.97232 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P04_step_2x | last_isi | definedness | None | 14.13999999998714 |  | inf | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 36.0 | 35 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P05_long_step | adaptation_index | definedness | None | -2.546155347125723e-06 |  | inf | `r-a455ac42295a97429d02` | `r-5a0a2ab1425c960b612e` |
| h/2 | P05_long_step | ahp_depth | exceeds | -10.808036804201677 | -16.79269372739848 | 5.98466 | 0.540693 | `r-a455ac42295a97429d02` | `r-5a0a2ab1425c960b612e` |
| h/2 | P05_long_step | last_isi | definedness | None | 14.76000000032218 |  | inf | `r-a455ac42295a97429d02` | `r-5a0a2ab1425c960b612e` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 136.0 | 135 | 0.5 | `r-a455ac42295a97429d02` | `r-5a0a2ab1425c960b612e` |
| h/2 | P06_ramp | first_spike_latency | definedness | None | 7.729999999865129 |  | inf | `r-4dc549d9b01b28a8eeb4` | `r-0bfc94e086428de431b7` |
| h/2 | P06_ramp | spike_count | exceeds | 0.0 | 67.0 | 67 | 0.5 | `r-4dc549d9b01b28a8eeb4` | `r-0bfc94e086428de431b7` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -65.33901102294948 | 1.92361 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-aba64c048d70f317aa9d` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 3.4899999994142945 | 1.7 | 0.5 | `r-a628bd90e08153ec217d` | `r-5b8744526baea71430ea` |
| h/2 | P08_rebound | spike_count | exceeds | 1.0 | 17.0 | 16 | 0.5 | `r-a628bd90e08153ec217d` | `r-5b8744526baea71430ea` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -17.21657525815896 | 5.99409 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-36ba36cc89db0e71ee2d` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 4.0 | 3 | 0.5 | `r-2c9f7eaf5c4d0d4f33d4` | `r-36ba36cc89db0e71ee2d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
