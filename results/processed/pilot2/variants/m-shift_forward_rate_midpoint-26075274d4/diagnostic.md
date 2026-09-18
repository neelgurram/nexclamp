# m-shift_forward_rate_midpoint-26075274d4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Kdr_pyr']/ionChannel[@id='Kdr_pyr']/gate[@id='n']/forwardRate[1]", "new": "-1.99e-2V", "old": "-2.49e-2V"}], "channel": "Kdr_pyr", "delta_mV": 5.0, "gate": "n", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Kdr_pyr.channel.nml", "locator": "/neuroml[@id='Kdr_pyr']/ionChannel[@id='Kdr_pyr']/gate[@id='n']/forwardRate[1]", "attribute": "midpoint", "old": "-2.49e-2V", "new": "-1.99e-2V", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1381.356 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.026568783862177505 | 0.110176 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | 0.40819819859105166 | 7.45529 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 97.74502563455034 | 2.30399 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 36.29000000001747 | 3.65 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-096dc4273f8b10fd509b` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -65.30295373992912 | 0.910691 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.00560071033399358 | 0.00201489 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-e926c540e77a67af6004` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -2.6654319458002504 | 4.3541 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 140.82999999974408 | 115.42 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-75bc8d3abd4d2f78f95f` |
| h/1 | P05_long_step | ahp_depth | exceeds | -7.059071324666348 | -2.7075843505858046 | 4.35149 | 0.5 | `r-f6700284baa99a5ef41f` | `r-604fcd4eb71b0c69defe` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 187.43999999970168 | 150.27 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-604fcd4eb71b0c69defe` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 447.87000000484295 | 139.02 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-604fcd4eb71b0c69defe` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-f6700284baa99a5ef41f` | `r-604fcd4eb71b0c69defe` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 310.26999999959 | 190.87 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-b43f8e84d9ace69d8408` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.0265029040532634 | 0.110445 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-68815197f2b7b516dd6d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | 0.4095996747699644 | 7.45054 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-68815197f2b7b516dd6d` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 97.50362777694752 | 2.3754 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-68815197f2b7b516dd6d` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 32.6300000000156 | 36.260000000017456 | 3.63 | 0.6528 | `r-2526a9bbad7e1faa361e` | `r-68815197f2b7b516dd6d` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-68815197f2b7b516dd6d` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -65.30432235107413 | 0.909321 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2944d4c33a00e7af9181` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.00560071033399358 | 0.00201489 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-8c62d2ea78723a609a6b` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -7.016957875569673 | -2.675203399658045 | 4.34175 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2944d4c33a00e7af9181` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 139.88999999974493 | 114.53 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-2944d4c33a00e7af9181` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-2944d4c33a00e7af9181` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2944d4c33a00e7af9181` |
| h/2 | P05_long_step | ahp_depth | exceeds | -7.056752797444673 | -2.7176380920408576 | 4.33911 | 0.5 | `r-493fa57e11933a720397` | `r-1ff2b706e63d1424c176` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 186.50999999970253 | 149.4 | 0.7434 | `r-493fa57e11933a720397` | `r-1ff2b706e63d1424c176` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 447.0900000047516 | 138.88 | 11.7378 | `r-493fa57e11933a720397` | `r-1ff2b706e63d1424c176` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-493fa57e11933a720397` | `r-1ff2b706e63d1424c176` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 309.8299999995904 | 191.23 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-620f433a146cc1326b72` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
