# m-scale_conductance-1f40a5f389

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "0.208477260206 mS_per_cm2", "old": "0.104238630103 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.104238630103 mS_per_cm2", "new": "0.208477260206 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1448.958 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 49.14999999985474 | 20.23 | 0.5784 | `r-50990666ac8ec9a46823` | `r-b6ef0b5d472dfb983baa` |
| h/1 | P00_canonical | last_isi | exceeds | 25.819999999976517 | 48.58999999995581 | 22.77 | 6.6 | `r-50990666ac8ec9a46823` | `r-b6ef0b5d472dfb983baa` |
| h/1 | P00_canonical | spike_count | exceeds | 28.0 | 15.0 | 13 | 9 | `r-50990666ac8ec9a46823` | `r-b6ef0b5d472dfb983baa` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.68582479858395 | -65.92117814178464 | 5.23535 | 0.5 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.13329007581449354 | 0.0688136 | 0.00128953 | `s-bd435463250c35027583` | `s-63632ed635d7aea18d4d` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.004400096639213388 | None |  | 0.01 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | ahp_depth | definedness | 11.031660542810322 | None |  | 1.26162 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 65.66345214961734 | None |  | 1.31327 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 41.14999999983473 | None |  | 0.823 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | last_isi | definedness | 32.02999999997087 | None |  | 1.59 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 0.0 | 15 | 3 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/1 | P05_long_step | adaptation_index | definedness | 0.0020482756593237653 | None |  | 0.01 | `r-5fe7a143f3c88a372d40` | `r-3aa6eb2ed9d4b91369fd` |
| h/1 | P05_long_step | ahp_depth | definedness | 10.79554604085748 | None |  | 1.25504 | `r-5fe7a143f3c88a372d40` | `r-3aa6eb2ed9d4b91369fd` |
| h/1 | P05_long_step | ap_amplitude | definedness | 65.26353454776816 | None |  | 1.30527 | `r-5fe7a143f3c88a372d40` | `r-3aa6eb2ed9d4b91369fd` |
| h/1 | P05_long_step | first_spike_latency | definedness | 65.31999999981275 | None |  | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-3aa6eb2ed9d4b91369fd` |
| h/1 | P05_long_step | last_isi | definedness | 56.07000000122389 | None |  | 2.61 | `r-5fe7a143f3c88a372d40` | `r-3aa6eb2ed9d4b91369fd` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 0.0 | 36 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-3aa6eb2ed9d4b91369fd` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 759.3799999991816 | 343.48 | 8.318 | `r-0957e33747fc542d9104` | `r-d930a826a3dd5b21a69b` |
| h/1 | P06_ramp | spike_count | exceeds | 20.0 | 6.0 | 14 | 3 | `r-0957e33747fc542d9104` | `r-d930a826a3dd5b21a69b` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -93.17739953460699 | -82.24693255767828 | 10.9305 | 0.5 | `r-d2b3788dfa4671532754` | `r-f70c65e5d87d4486323e` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 48.92999999985494 | 20.18 | 0.5784 | `r-cff06a8ac591df54f373` | `r-063e3bf69b9d836f50f3` |
| h/2 | P00_canonical | last_isi | exceeds | 23.619999999978518 | 45.96999999995819 | 22.35 | 6.6 | `r-cff06a8ac591df54f373` | `r-063e3bf69b9d836f50f3` |
| h/2 | P00_canonical | spike_count | exceeds | 31.0 | 16.0 | 15 | 9 | `r-cff06a8ac591df54f373` | `r-063e3bf69b9d836f50f3` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -60.68582508010861 | -65.92117803192136 | 5.23535 | 0.5 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.1332559251417253 | 0.0687795 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-ed9cc8c00bc6ca1c95b6` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.0043792695235912405 | None |  | 0.01 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P04_step_2x | ahp_depth | definedness | 11.452200846353144 | None |  | 1.26162 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 65.3342704782316 | None |  | 1.31327 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 41.10999999983477 | None |  | 0.823 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P04_step_2x | last_isi | definedness | 31.49999999997135 | None |  | 1.59 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P04_step_2x | spike_count | exceeds | 16.0 | 0.0 | 16 | 3 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |
| h/2 | P05_long_step | adaptation_index | definedness | 0.002149159038242536 | None |  | 0.01 | `r-317893116e9cb0c903c3` | `r-90e052e9853cf93b4fbd` |
| h/2 | P05_long_step | ahp_depth | definedness | 11.21389289347907 | None |  | 1.25504 | `r-317893116e9cb0c903c3` | `r-90e052e9853cf93b4fbd` |
| h/2 | P05_long_step | ap_amplitude | definedness | 64.9877738975208 | None |  | 1.30527 | `r-317893116e9cb0c903c3` | `r-90e052e9853cf93b4fbd` |
| h/2 | P05_long_step | first_spike_latency | definedness | 65.27999999981279 | None |  | 1.3064 | `r-317893116e9cb0c903c3` | `r-90e052e9853cf93b4fbd` |
| h/2 | P05_long_step | last_isi | definedness | 55.2000000012049 | None |  | 2.61 | `r-317893116e9cb0c903c3` | `r-90e052e9853cf93b4fbd` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 0.0 | 36 | 0.5 | `r-317893116e9cb0c903c3` | `r-90e052e9853cf93b4fbd` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 759.3299999991816 | 343.48 | 8.318 | `r-24b7e809e0450dd29615` | `r-9251dc6d192171c3e5d5` |
| h/2 | P06_ramp | spike_count | exceeds | 21.0 | 6.0 | 15 | 3 | `r-24b7e809e0450dd29615` | `r-9251dc6d192171c3e5d5` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -93.17739972381598 | -82.24693282928473 | 10.9305 | 0.5 | `r-ae1b79422775c8a979b7` | `r-357aae0bd0b90293648a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
