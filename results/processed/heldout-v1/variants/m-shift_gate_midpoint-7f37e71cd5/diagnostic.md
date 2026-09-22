# m-shift_gate_midpoint-7f37e71cd5

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='ka']/ionChannel[@id='ka']/gate[@id='m']/steadyState[1]", "new": "-65mV", "old": "-60mV"}], "channel": "ka", "delta_mV": -5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/ka.channel.nml", "locator": "/neuroml[@id='ka']/ionChannel[@id='ka']/gate[@id='m']/steadyState[1]", "attribute": "midpoint", "old": "-60mV", "new": "-65mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4631.836 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.017936897992228234 | None |  | 0.01 | `r-a309e30f4eac6329447d` | `r-921483c9535704a43eed` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -1.6654787585509752 | 6.31197 | 0.5 | `r-a309e30f4eac6329447d` | `r-921483c9535704a43eed` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 2.9100000000007817 | 38.04999999999702 | 35.14 | 0.5 | `r-a309e30f4eac6329447d` | `r-921483c9535704a43eed` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 8.740000000004471 | 1.15 | 0.5 | `r-a309e30f4eac6329447d` | `r-921483c9535704a43eed` |
| h/1 | P00_canonical | spike_count | exceeds | 9.0 | 3.0 | 6 | 0.5 | `r-a309e30f4eac6329447d` | `r-921483c9535704a43eed` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -67.64778379821769 | 4.53468 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.05132846117068506 | 0.034219 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-662698bd5a21a9d44e04` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.004861353302673796 | None |  | 0.01 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P04_step_2x | ahp_depth | definedness | -5.43348429870143 | None |  | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 76.68460655583269 | None |  | 1.89637 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 53.72999999982329 | None |  | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P04_step_2x | last_isi | definedness | 25.62999999997669 | None |  | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 0.0 | 18 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P05_long_step | adaptation_index | definedness | 0.0003686992675871277 | None |  | 0.01 | `r-c181d8dc3f2e9e1a86cf` | `r-13d8803b45a6b21de850` |
| h/1 | P05_long_step | ahp_depth | definedness | -5.300969345084837 | None |  | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-13d8803b45a6b21de850` |
| h/1 | P05_long_step | ap_amplitude | definedness | 77.26993942349823 | None |  | 1.98255 | `r-c181d8dc3f2e9e1a86cf` | `r-13d8803b45a6b21de850` |
| h/1 | P05_long_step | first_spike_latency | definedness | 86.49999999979349 | None |  | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-13d8803b45a6b21de850` |
| h/1 | P05_long_step | last_isi | definedness | 46.560000001016306 | None |  | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-13d8803b45a6b21de850` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 0.0 | 42 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-13d8803b45a6b21de850` |
| h/1 | P06_ramp | first_spike_latency | definedness | 435.03999999947655 | None |  | 8.7008 | `r-8c44150a9a017555d35c` | `r-7b2300283ad921fa6830` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 0.0 | 27 | 3 | `r-8c44150a9a017555d35c` | `r-7b2300283ad921fa6830` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.1199735717775 | -71.51051949615494 | 2.39055 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-c21353b2a994cd13cdf3` |
| h/1 | P09_short_pulse | ahp_depth | definedness | -8.488179428100779 | None |  | 1.08676 | `r-f411679bd6f2a1231337` | `r-26bdaf0314684c1b3aff` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 90.83680152686651 | None |  | 1.81674 | `r-f411679bd6f2a1231337` | `r-26bdaf0314684c1b3aff` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | 1.7799999998705403 | None |  | 0.5 | `r-f411679bd6f2a1231337` | `r-26bdaf0314684c1b3aff` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-f411679bd6f2a1231337` | `r-26bdaf0314684c1b3aff` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.018020148454594893 | None |  | 0.01 | `r-82914471c1c753634231` | `r-717b9f1ed14ff42ec1e9` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.911862463500448 | -1.5948204685796128 | 6.31704 | 0.5 | `r-82914471c1c753634231` | `r-717b9f1ed14ff42ec1e9` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 2.90000000000078 | 38.03999999999702 | 35.14 | 0.5 | `r-82914471c1c753634231` | `r-717b9f1ed14ff42ec1e9` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 8.820000000004512 | 1.21 | 0.5 | `r-82914471c1c753634231` | `r-717b9f1ed14ff42ec1e9` |
| h/2 | P00_canonical | spike_count | exceeds | 9.0 | 3.0 | 6 | 0.5 | `r-82914471c1c753634231` | `r-717b9f1ed14ff42ec1e9` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.11310686187736 | -67.64778346099845 | 4.53468 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.05132846117068506 | 0.034219 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-e993ee20da51ef6f1b8b` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.004952237915862522 | None |  | 0.01 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P04_step_2x | ahp_depth | definedness | -5.051723726911618 | None |  | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 76.05248450904598 | None |  | 1.89637 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 53.649999999823365 | None |  | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P04_step_2x | last_isi | definedness | 26.0599999999763 | None |  | 1.29 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 0.0 | 18 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P05_long_step | adaptation_index | definedness | 0.0003457083960339961 | None |  | 0.01 | `r-c41be102b8e8611b929c` | `r-ac791abdc808f7cb114d` |
| h/2 | P05_long_step | ahp_depth | definedness | -4.916790255219169 | None |  | 1.15254 | `r-c41be102b8e8611b929c` | `r-ac791abdc808f7cb114d` |
| h/2 | P05_long_step | ap_amplitude | definedness | 76.60908890083579 | None |  | 1.98255 | `r-c41be102b8e8611b929c` | `r-ac791abdc808f7cb114d` |
| h/2 | P05_long_step | first_spike_latency | definedness | 86.41999999979356 | None |  | 1.73 | `r-c41be102b8e8611b929c` | `r-ac791abdc808f7cb114d` |
| h/2 | P05_long_step | last_isi | definedness | 47.430000001035296 | None |  | 2.61 | `r-c41be102b8e8611b929c` | `r-ac791abdc808f7cb114d` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 0.0 | 41 | 3 | `r-c41be102b8e8611b929c` | `r-ac791abdc808f7cb114d` |
| h/2 | P06_ramp | first_spike_latency | definedness | 434.9599999994766 | None |  | 8.7008 | `r-11d8f8c83600b900cadc` | `r-83c5275ed4bf602ecfb0` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 0.0 | 26 | 3 | `r-11d8f8c83600b900cadc` | `r-83c5275ed4bf602ecfb0` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -69.11997425689714 | -71.51052015991228 | 2.39055 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-eb38664b0ec98ea0ab10` |
| h/2 | P09_short_pulse | ahp_depth | definedness | -8.125927218107364 | None |  | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-ce6d7b73aadff24c76f8` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 90.35200882226567 | None |  | 1.81674 | `r-4bcc4e2fdcca97c21eee` | `r-ce6d7b73aadff24c76f8` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | 1.7599999998705584 | None |  | 0.5 | `r-4bcc4e2fdcca97c21eee` | `r-ce6d7b73aadff24c76f8` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-4bcc4e2fdcca97c21eee` | `r-ce6d7b73aadff24c76f8` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
