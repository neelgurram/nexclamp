# m-shift_reversal-36bce9b069

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='leak']", "new": "-64.3mV", "old": "-54.3mV"}], "element": "channelDensity", "element_id": "leak", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml[@id='NML2_SingleCompHHCell']/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='leak']", "attribute": "erev", "old": "-54.3mV", "new": "-64.3mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 603.323 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | -7.74713208133793e-05 | None |  | 0.01 | `r-5f0a94c66ff17cd98a0a` | `r-4e9c67fde5bf9998fb0e` |
| h/1 | P00_canonical | ahp_depth | exceeds | -10.343139648437372 | -7.427619934081264 | 2.91552 | 0.517157 | `r-5f0a94c66ff17cd98a0a` | `r-4e9c67fde5bf9998fb0e` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 95.13947677592056 | 99.3143615720661 | 4.17488 | 1.90279 | `r-5f0a94c66ff17cd98a0a` | `r-4e9c67fde5bf9998fb0e` |
| h/1 | P00_canonical | last_isi | definedness | 16.12999999998533 | None |  | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-4e9c67fde5bf9998fb0e` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-5f0a94c66ff17cd98a0a` | `r-4e9c67fde5bf9998fb0e` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -64.08310811767565 | -66.82824819335924 | 2.74514 | 0.5 | `r-66b1007575e04915ac55` | `r-98d84e3da6430a96d8ec` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.022436992008742575 | 0.028379209070418687 | 0.00594222 | 0.00044874 | `s-6485b8f0d5e0c45b0b4d` | `s-138a647b77a69f69ee5b` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -10.697937011716306 | -7.778518676755965 | 2.91942 | 0.534897 | `r-66b1007575e04915ac55` | `r-98d84e3da6430a96d8ec` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.72434234740876 | 96.4078598033359 | 3.68352 | 1.85449 | `r-66b1007575e04915ac55` | `r-98d84e3da6430a96d8ec` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 3.5399999998689395 | 4.329999999868221 | 0.79 | 0.5 | `r-66b1007575e04915ac55` | `r-98d84e3da6430a96d8ec` |
| h/1 | P05_long_step | ahp_depth | exceeds | -10.81385040282855 | -7.890449523924119 | 2.9234 | 0.540693 | `r-940eedfaa66e3fa96c16` | `r-441626d7a85e1f4aa4d5` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.2126808181487 | 94.21921920873737 | 3.00654 | 1.82425 | `r-940eedfaa66e3fa96c16` | `r-441626d7a85e1f4aa4d5` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 4.42999999986813 | 5.959999999866739 | 1.53 | 0.5 | `r-940eedfaa66e3fa96c16` | `r-441626d7a85e1f4aa4d5` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261677551295 | -72.48515858306911 | 5.22254 | 0.5 | `r-66b1007575e04915ac55` | `r-98d84e3da6430a96d8ec` |
| h/1 | P08_rebound | first_spike_latency | definedness | 5.219999999412721 | None |  | 0.5 | `r-011ab0e03522b12f620c` | `r-9b8b87b42b9fd34d7aec` |
| h/1 | P08_rebound | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-011ab0e03522b12f620c` | `r-9b8b87b42b9fd34d7aec` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -11.226577758789873 | -8.288925170897627 | 2.93765 | 0.561329 | `r-efc8f2fd727ba1854c5f` | `r-09bb541c7691ad01dddb` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 106.45812988261622 | 112.647174834953 | 6.18904 | 2.12916 | `r-efc8f2fd727ba1854c5f` | `r-09bb541c7691ad01dddb` |
| h/2 | P00_canonical | adaptation_index | definedness | -1.02201355559918e-13 | None |  | 0.01 | `r-d4235ef154cdc2eeb44c` | `r-9f16acbd58788b72626f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -10.327699567887592 | -7.415529165353618 | 2.91217 | 0.517157 | `r-d4235ef154cdc2eeb44c` | `r-9f16acbd58788b72626f` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 95.29706954941832 | 99.36120986924539 | 4.06414 | 1.90279 | `r-d4235ef154cdc2eeb44c` | `r-9f16acbd58788b72626f` |
| h/2 | P00_canonical | last_isi | definedness | 16.059999999985394 | None |  | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-9f16acbd58788b72626f` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-d4235ef154cdc2eeb44c` | `r-9f16acbd58788b72626f` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -64.08310755462634 | -66.82824763030993 | 2.74514 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-76c7cd37560be932511a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02240284133597432 | 0.028345058397650436 | 0.00594222 | 0.00044874 | `s-b96e12fd1e882cb18a94` | `s-f5ab2a74825a9d577efd` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -10.691650390625 | -7.7738800048828125 | 2.91777 | 0.534897 | `r-8d6f46142acd4ec898a7` | `r-76c7cd37560be932511a` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.82558822777118 | 96.49916458264678 | 3.67358 | 1.85449 | `r-8d6f46142acd4ec898a7` | `r-76c7cd37560be932511a` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 3.509999999868967 | 4.299999999868248 | 0.79 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-76c7cd37560be932511a` |
| h/2 | P05_long_step | ahp_depth | exceeds | -10.808036804201677 | -7.886329650878082 | 2.92171 | 0.540693 | `r-a455ac42295a97429d02` | `r-0c50209f437c533def8e` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.37988662862392 | 94.34526825068687 | 2.96538 | 1.82425 | `r-a455ac42295a97429d02` | `r-0c50209f437c533def8e` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 4.3899999998681665 | 5.919999999866775 | 1.53 | 0.5 | `r-a455ac42295a97429d02` | `r-0c50209f437c533def8e` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -67.26261789703395 | -72.4851597045901 | 5.22254 | 0.5 | `r-8d6f46142acd4ec898a7` | `r-76c7cd37560be932511a` |
| h/2 | P08_rebound | first_spike_latency | definedness | 5.189999999412748 | None |  | 0.5 | `r-a628bd90e08153ec217d` | `r-5b7db53d4195d047e90f` |
| h/2 | P08_rebound | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-a628bd90e08153ec217d` | `r-5b7db53d4195d047e90f` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -11.22248840332071 | -8.28646850585777 | 2.93602 | 0.561329 | `r-2c9f7eaf5c4d0d4f33d4` | `r-8ab46f83d8e434af8e2a` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 106.43966293307548 | 112.62408447229862 | 6.18442 | 2.12916 | `r-2c9f7eaf5c4d0d4f33d4` | `r-8ab46f83d8e434af8e2a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
