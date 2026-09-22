# m-shift_reversal-5b6a87e0b4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "new": "-80.0 mV", "old": "-90.0 mV"}], "element": "channelDensity", "element_id": "pas_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "attribute": "erev", "old": "-90.0 mV", "new": "-80.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4566.106 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | -4.918664252006479 | 4.45918 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-5c7619f74bfa90a89b54` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 14.489999999986821 | 1.3 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-5c7619f74bfa90a89b54` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -70.1574205581664 | -67.57643458557118 | 2.58099 | 0.5 | `r-49ced7acda977f37b12b` | `r-cbfd1a44af7398e91f5f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.01707533638412677 | 0.00307356 | 0.000402978 | `s-606c2ee73d10b43bdee7` | `s-9ba45c79857972743793` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | -3.8231592458097623 | 4.69719 | 0.5 | `r-49ced7acda977f37b12b` | `r-cbfd1a44af7398e91f5f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.549999999864383 | 7.059999999865738 | 1.49 | 0.5 | `r-49ced7acda977f37b12b` | `r-cbfd1a44af7398e91f5f` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 21.08999999998082 | 15.56 | 0.733 | `r-49ced7acda977f37b12b` | `r-cbfd1a44af7398e91f5f` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 24.0 | 9 | 0.5 | `r-49ced7acda977f37b12b` | `r-cbfd1a44af7398e91f5f` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -4.037644414265955 | 4.49819 | 0.5 | `r-b99907e8e6510bd22247` | `r-5933293e47ef9512f63b` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.769999999860545 | 10.079999999862991 | 2.69 | 0.5 | `r-b99907e8e6510bd22247` | `r-5933293e47ef9512f63b` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 127.86000000279091 | 15.11 | 3.03 | `r-b99907e8e6510bd22247` | `r-5933293e47ef9512f63b` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-5933293e47ef9512f63b` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 368.589999999537 | 313.8199999995868 | 54.77 | 7.3718 | `r-da1341cbf9665d4e7639` | `r-1d3b8d81cc8e7f5817d9` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 28.0 | 4 | 0.5 | `r-da1341cbf9665d4e7639` | `r-1d3b8d81cc8e7f5817d9` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -94.93546852569605 | -93.31334480896021 | 1.62212 | 0.5 | `r-49ced7acda977f37b12b` | `r-cbfd1a44af7398e91f5f` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | -5.762085942584861 | 4.62143 | 0.5 | `r-ad42eb643e1748725abb` | `r-cef5720d40e10c3ee12f` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 126.03113174260383 | 122.14954756102131 | 3.88158 | 2.52062 | `r-ad42eb643e1748725abb` | `r-cef5720d40e10c3ee12f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | -4.9257877056406585 | 4.46104 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-9c1138c701764072c71e` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 14.47999999998683 | 1.29 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-9c1138c701764072c71e` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -70.15742004241932 | -67.57643407287586 | 2.58099 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-1b69e3c2ad86641925b6` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.01707533638412677 | 0.00307356 | 0.000402978 | `s-dcf9a3a6907c5d4ed514` | `s-b8e00f630c2f0286f66e` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | -3.8074679234797486 | 4.71757 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-1b69e3c2ad86641925b6` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 8.50999999986442 | 7.0199999998657745 | 1.49 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-1b69e3c2ad86641925b6` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 21.019999999980882 | 15.54 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-1b69e3c2ad86641925b6` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 24.0 | 9 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-1b69e3c2ad86641925b6` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | -3.982402310689295 | 4.53557 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-efe500a29c073eaf4193` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.729999999860581 | 10.049999999863019 | 2.68 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-efe500a29c073eaf4193` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 128.8400000028123 | 15.14 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-efe500a29c073eaf4193` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-efe500a29c073eaf4193` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 368.53999999953703 | 313.76999999958684 | 54.77 | 7.3718 | `r-1b54cfe9f9ae3444183f` | `r-f86de5b624f3b352d02d` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 29.0 | 5 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-f86de5b624f3b352d02d` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -94.93546955413842 | -93.3133458374026 | 1.62212 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-1b69e3c2ad86641925b6` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | -5.77973507436198 | 4.6128 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-e59b8e1c98a9c8416693` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 125.19136047490628 | 121.3194160353866 | 3.87194 | 2.52062 | `r-12a8ce0ecdd4bde4c832` | `r-e59b8e1c98a9c8416693` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
