# m-shift_reversal-d2ca2a5c38

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "-61.3013913493 mV", "old": "-71.3013913493 mV"}], "element": "channelDensity", "element_id": "LeakConductance_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "erev", "old": "-71.3013913493 mV", "new": "-61.3013913493 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1500.607 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 7.666865774086709 | -2.168809911369891 | 9.83568 | 6.89996 | `r-50990666ac8ec9a46823` | `r-108cfe45576b45ef9266` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 17.61999999988342 | 11.3 | 0.5784 | `r-50990666ac8ec9a46823` | `r-108cfe45576b45ef9266` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.68582479858395 | -50.72648142547603 | 9.95934 | 0.5 | `r-d2b3788dfa4671532754` | `r-bc2b68196d93ebb698ac` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.035243494296837645 | 0.029233 | 0.00128953 | `s-bd435463250c35027583` | `s-2d3d545b7afe4f28b595` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 11.031660542810322 | 1.2016627222719904 | 9.83 | 1.26162 | `r-d2b3788dfa4671532754` | `r-bc2b68196d93ebb698ac` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 41.14999999983473 | 23.169999999851086 | 17.98 | 0.823 | `r-d2b3788dfa4671532754` | `r-bc2b68196d93ebb698ac` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 24.219999999977972 | 7.81 | 1.59 | `r-d2b3788dfa4671532754` | `r-bc2b68196d93ebb698ac` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 21.0 | 6 | 3 | `r-d2b3788dfa4671532754` | `r-bc2b68196d93ebb698ac` |
| h/1 | P05_long_step | ahp_depth | exceeds | 10.79554604085748 | 0.9881388575256622 | 9.80741 | 1.25504 | `r-5fe7a143f3c88a372d40` | `r-90f9f02c7a62a5c51d2c` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 65.31999999981275 | 32.059999999843 | 33.26 | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-90f9f02c7a62a5c51d2c` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 34.34000000074957 | 21.73 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-90f9f02c7a62a5c51d2c` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 59.0 | 23 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-90f9f02c7a62a5c51d2c` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 265.04999999963115 | 150.85 | 8.318 | `r-0957e33747fc542d9104` | `r-db21f3f338696d949ec7` |
| h/1 | P06_ramp | spike_count | exceeds | 20.0 | 29.0 | 9 | 3 | `r-0957e33747fc542d9104` | `r-db21f3f338696d949ec7` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -93.17739953460699 | -83.19072219543463 | 9.98668 | 0.5 | `r-d2b3788dfa4671532754` | `r-bc2b68196d93ebb698ac` |
| h/2 | P00_canonical | ahp_depth | exceeds | 9.966850862869194 | 0.14437779151814567 | 9.82247 | 6.89996 | `r-cff06a8ac591df54f373` | `r-56b7df41b6189a5f0a39` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 17.459999999883564 | 11.29 | 0.5784 | `r-cff06a8ac591df54f373` | `r-56b7df41b6189a5f0a39` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -60.68582508010861 | -50.726486526489204 | 9.95934 | 0.5 | `r-ae1b79422775c8a979b7` | `r-f8576e12b5077564c723` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.035243494296837645 | 0.029233 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-bead382cb90c3c44c034` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 11.452200846353144 | 1.6247844734189627 | 9.82742 | 1.26162 | `r-ae1b79422775c8a979b7` | `r-f8576e12b5077564c723` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 41.10999999983477 | 23.129999999851123 | 17.98 | 0.823 | `r-ae1b79422775c8a979b7` | `r-f8576e12b5077564c723` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 23.719999999978427 | 7.78 | 1.59 | `r-ae1b79422775c8a979b7` | `r-f8576e12b5077564c723` |
| h/2 | P04_step_2x | spike_count | exceeds | 16.0 | 21.0 | 5 | 3 | `r-ae1b79422775c8a979b7` | `r-f8576e12b5077564c723` |
| h/2 | P05_long_step | ahp_depth | exceeds | 11.21389289347907 | 1.4090862312283008 | 9.80481 | 1.25504 | `r-317893116e9cb0c903c3` | `r-e64cc0274805a94afba4` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 65.27999999981279 | 32.01999999984304 | 33.26 | 1.3064 | `r-317893116e9cb0c903c3` | `r-e64cc0274805a94afba4` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 33.730000000736254 | 21.47 | 2.61 | `r-317893116e9cb0c903c3` | `r-e64cc0274805a94afba4` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 60.0 | 24 | 0.5 | `r-317893116e9cb0c903c3` | `r-e64cc0274805a94afba4` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 264.9999999996312 | 150.85 | 8.318 | `r-24b7e809e0450dd29615` | `r-37eb5e96950ea9096364` |
| h/2 | P06_ramp | spike_count | exceeds | 21.0 | 30.0 | 9 | 3 | `r-24b7e809e0450dd29615` | `r-37eb5e96950ea9096364` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -93.17739972381598 | -83.19072241516119 | 9.98668 | 0.5 | `r-ae1b79422775c8a979b7` | `r-f8576e12b5077564c723` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
