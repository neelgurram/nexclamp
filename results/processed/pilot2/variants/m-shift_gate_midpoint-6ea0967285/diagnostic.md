# m-shift_gate_midpoint-6ea0967285

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/forwardRate[1]", "new": "-45mV", "old": "-55mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "new": "-55mV", "old": "-65mV"}], "channel": "kChan", "delta_mV": 10.0, "gate": "n", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/forwardRate[1]", "attribute": "midpoint", "old": "-55mV", "new": "-45mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "attribute": "midpoint", "old": "-65mV", "new": "-55mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 260.248 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -22.956324866081466 | 12.6132 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-99658c1594885c6768c9` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 99.84794235209554 | 4.70847 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-99658c1594885c6768c9` |
| h/1 | P00_canonical | last_isi | exceeds | 16.12999999998533 | 10.429999999990514 | 5.7 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-99658c1594885c6768c9` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 10.0 | 3 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-99658c1594885c6768c9` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 37.0 | 37 | 0.5 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -52.88318946504382 | 11.1999 | 0.5 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.0 | 0.022437 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-22a21dd072ac47e90614` |
| h/1 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -19.148983077245525 | 8.45105 | 0.534897 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 95.24115371826987 | 2.51681 | 1.85449 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 6.979999999865811 | 3.44 | 0.5 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P04_step_2x | last_isi | definedness | None | 11.549999999989495 |  | inf | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 43.0 | 42 | 0.5 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P05_long_step | adaptation_index | definedness | None | 6.97465262088509e-14 |  | inf | `r-940eedfaa66e3fa96c16` | `r-e7438007ea16e95fbd07` |
| h/1 | P05_long_step | ahp_depth | exceeds | -10.81385040282855 | -19.35107047958781 | 8.53722 | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-e7438007ea16e95fbd07` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 96.08660507338506 | 4.87392 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-e7438007ea16e95fbd07` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 7.489999999865347 | 3.06 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-e7438007ea16e95fbd07` |
| h/1 | P05_long_step | last_isi | definedness | None | 12.070000000263462 |  | inf | `r-940eedfaa66e3fa96c16` | `r-e7438007ea16e95fbd07` |
| h/1 | P05_long_step | spike_count | exceeds | 1.0 | 166.0 | 165 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-e7438007ea16e95fbd07` |
| h/1 | P06_ramp | first_spike_latency | definedness | None | 9.919999999863137 |  | inf | `r-b32245eb811666b0240b` | `r-4d88a66016f4bbec5ec3` |
| h/1 | P06_ramp | spike_count | exceeds | 0.0 | 82.0 | 82 | 0.5 | `r-b32245eb811666b0240b` | `r-4d88a66016f4bbec5ec3` |
| h/1 | P07_hyperpolarizing_step | spike_count | exceeds | 0.0 | 26.0 | 26 | 0.5 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -59.05637645453308 | 8.20624 | 0.5 | `r-66b1007575e04915ac55` | `r-a9260c80a3ea561938d7` |
| h/1 | P08_rebound | first_spike_latency | exceeds | 5.219999999412721 | 3.429999999414349 | 1.79 | 0.5 | `r-011ab0e03522b12f620c` | `r-989ec9b28fe5b630c618` |
| h/1 | P08_rebound | spike_count | exceeds | 1.0 | 21.0 | 20 | 0.5 | `r-011ab0e03522b12f620c` | `r-989ec9b28fe5b630c618` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -19.8076363365198 | 8.58106 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-c244096bb01f34850b8d` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 84.55143737907663 | 21.9067 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-c244096bb01f34850b8d` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.4599999998708313 | 3.579999999868903 | 2.12 | 0.5 | `r-efc8f2fd727ba1854c5f` | `r-c244096bb01f34850b8d` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 4.0 | 3 | 0.5 | `r-efc8f2fd727ba1854c5f` | `r-c244096bb01f34850b8d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -22.24252000905492 | 11.9148 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-8dfccef1a04fc0517d93` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 100.72179031356858 | 5.42472 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-8dfccef1a04fc0517d93` |
| h/2 | P00_canonical | last_isi | exceeds | 16.059999999985394 | 10.369999999990569 | 5.69 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-8dfccef1a04fc0517d93` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 10.0 | 3 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-8dfccef1a04fc0517d93` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 37.0 | 37 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -53.21713025822892 | 10.866 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.0 | 0.0224028 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-c56ef2c2197dd0f2fcfe` |
| h/2 | P04_step_2x | adaptation_index | definedness | None | 0.0 |  | inf | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -19.116911486191597 | 8.42526 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 95.40279388578469 | 2.57721 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 6.1799999998665385 | 2.67 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P04_step_2x | last_isi | definedness | None | 11.519999999989523 |  | inf | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 43.0 | 42 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P05_long_step | adaptation_index | definedness | None | 6.974651856030126e-14 |  | inf | `r-a455ac42295a97429d02` | `r-acd91c98dfa8e07c5118` |
| h/2 | P05_long_step | ahp_depth | exceeds | -10.808036804201677 | -19.31693895200857 | 8.5089 | 0.540693 | `r-a455ac42295a97429d02` | `r-acd91c98dfa8e07c5118` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 96.1334381117388 | 4.75355 | 1.82425 | `r-a455ac42295a97429d02` | `r-acd91c98dfa8e07c5118` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 6.6999999998660655 | 2.31 | 0.5 | `r-a455ac42295a97429d02` | `r-acd91c98dfa8e07c5118` |
| h/2 | P05_long_step | last_isi | definedness | None | 12.040000000262808 |  | inf | `r-a455ac42295a97429d02` | `r-acd91c98dfa8e07c5118` |
| h/2 | P05_long_step | spike_count | exceeds | 1.0 | 166.0 | 165 | 0.5 | `r-a455ac42295a97429d02` | `r-acd91c98dfa8e07c5118` |
| h/2 | P06_ramp | first_spike_latency | definedness | None | 9.189999999863801 |  | inf | `r-4dc549d9b01b28a8eeb4` | `r-c133339ef1838860670d` |
| h/2 | P06_ramp | spike_count | exceeds | 0.0 | 82.0 | 82 | 0.5 | `r-4dc549d9b01b28a8eeb4` | `r-c133339ef1838860670d` |
| h/2 | P07_hyperpolarizing_step | spike_count | exceeds | 0.0 | 26.0 | 26 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -61.09148872070422 | 6.17113 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-5a9c11ca1e72a48e071d` |
| h/2 | P08_rebound | first_spike_latency | exceeds | 5.189999999412748 | 3.4099999994143673 | 1.78 | 0.5 | `r-a628bd90e08153ec217d` | `r-354b9f73c22d59fe698d` |
| h/2 | P08_rebound | spike_count | exceeds | 1.0 | 21.0 | 20 | 0.5 | `r-a628bd90e08153ec217d` | `r-354b9f73c22d59fe698d` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -19.829603746934197 | 8.60712 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-3418711358fc96db9086` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 90.72190475618928 | 15.7178 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-3418711358fc96db9086` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.4399999998708495 | 2.7899999998696217 | 1.35 | 0.5 | `r-2c9f7eaf5c4d0d4f33d4` | `r-3418711358fc96db9086` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 4.0 | 3 | 0.5 | `r-2c9f7eaf5c4d0d4f33d4` | `r-3418711358fc96db9086` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
