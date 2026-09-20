# m-wrong_channel-105026e445

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "IL", "old": "Na"}], "element_id": "Na_all", "generator_seed": 20260917, "new_species": "ca", "old_species": "na"}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "ionChannel", "old": "Na", "new": "IL", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1401.363 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.0017557204659683922 | None |  | 0.01 | `r-50990666ac8ec9a46823` | `r-83500d9fdd06efa9953f` |
| h/1 | P00_canonical | ahp_depth | definedness | 7.666865774086709 | None |  | 6.89996 | `r-50990666ac8ec9a46823` | `r-83500d9fdd06efa9953f` |
| h/1 | P00_canonical | ap_amplitude | definedness | 68.17416534535639 | None |  | 3.91218 | `r-50990666ac8ec9a46823` | `r-83500d9fdd06efa9953f` |
| h/1 | P00_canonical | first_spike_latency | definedness | 28.91999999987314 | None |  | 0.5784 | `r-50990666ac8ec9a46823` | `r-83500d9fdd06efa9953f` |
| h/1 | P00_canonical | last_isi | definedness | 25.819999999976517 | None |  | 6.6 | `r-50990666ac8ec9a46823` | `r-83500d9fdd06efa9953f` |
| h/1 | P00_canonical | spike_count | exceeds | 28.0 | 0.0 | 28 | 9 | `r-50990666ac8ec9a46823` | `r-83500d9fdd06efa9953f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.0545386244109009 | 0.00993785 | 0.00128953 | `s-bd435463250c35027583` | `s-73ec573267d93109d799` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.004400096639213388 | None |  | 0.01 | `r-d2b3788dfa4671532754` | `r-0f69334f7fe9b2435640` |
| h/1 | P04_step_2x | ahp_depth | definedness | 11.031660542810322 | None |  | 1.26162 | `r-d2b3788dfa4671532754` | `r-0f69334f7fe9b2435640` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 65.66345214961734 | None |  | 1.31327 | `r-d2b3788dfa4671532754` | `r-0f69334f7fe9b2435640` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 41.14999999983473 | None |  | 0.823 | `r-d2b3788dfa4671532754` | `r-0f69334f7fe9b2435640` |
| h/1 | P04_step_2x | last_isi | definedness | 32.02999999997087 | None |  | 1.59 | `r-d2b3788dfa4671532754` | `r-0f69334f7fe9b2435640` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 0.0 | 15 | 3 | `r-d2b3788dfa4671532754` | `r-0f69334f7fe9b2435640` |
| h/1 | P05_long_step | adaptation_index | definedness | 0.0020482756593237653 | None |  | 0.01 | `r-5fe7a143f3c88a372d40` | `r-c967d4adfff16ea26680` |
| h/1 | P05_long_step | ahp_depth | definedness | 10.79554604085748 | None |  | 1.25504 | `r-5fe7a143f3c88a372d40` | `r-c967d4adfff16ea26680` |
| h/1 | P05_long_step | ap_amplitude | definedness | 65.26353454776816 | None |  | 1.30527 | `r-5fe7a143f3c88a372d40` | `r-c967d4adfff16ea26680` |
| h/1 | P05_long_step | first_spike_latency | definedness | 65.31999999981275 | None |  | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-c967d4adfff16ea26680` |
| h/1 | P05_long_step | last_isi | definedness | 56.07000000122389 | None |  | 2.61 | `r-5fe7a143f3c88a372d40` | `r-c967d4adfff16ea26680` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 0.0 | 36 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-c967d4adfff16ea26680` |
| h/1 | P06_ramp | first_spike_latency | definedness | 415.89999999949396 | None |  | 8.318 | `r-0957e33747fc542d9104` | `r-899528a77fbac50b1522` |
| h/1 | P06_ramp | spike_count | exceeds | 20.0 | 0.0 | 20 | 3 | `r-0957e33747fc542d9104` | `r-899528a77fbac50b1522` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.001963943238299798 | None |  | 0.01 | `r-cff06a8ac591df54f373` | `r-0116f017713fea5e535e` |
| h/2 | P00_canonical | ahp_depth | definedness | 9.966850862869194 | None |  | 6.89996 | `r-cff06a8ac591df54f373` | `r-0116f017713fea5e535e` |
| h/2 | P00_canonical | ap_amplitude | definedness | 66.87010574454787 | None |  | 3.91218 | `r-cff06a8ac591df54f373` | `r-0116f017713fea5e535e` |
| h/2 | P00_canonical | first_spike_latency | definedness | 28.749999999873296 | None |  | 0.5784 | `r-cff06a8ac591df54f373` | `r-0116f017713fea5e535e` |
| h/2 | P00_canonical | last_isi | definedness | 23.619999999978518 | None |  | 6.6 | `r-cff06a8ac591df54f373` | `r-0116f017713fea5e535e` |
| h/2 | P00_canonical | spike_count | exceeds | 31.0 | 0.0 | 31 | 9 | `r-cff06a8ac591df54f373` | `r-0116f017713fea5e535e` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.0545386244109009 | 0.00993785 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-281fdd69ce1be66462b7` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.0043792695235912405 | None |  | 0.01 | `r-ae1b79422775c8a979b7` | `r-30d17c54ac2eae6167d0` |
| h/2 | P04_step_2x | ahp_depth | definedness | 11.452200846353144 | None |  | 1.26162 | `r-ae1b79422775c8a979b7` | `r-30d17c54ac2eae6167d0` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 65.3342704782316 | None |  | 1.31327 | `r-ae1b79422775c8a979b7` | `r-30d17c54ac2eae6167d0` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 41.10999999983477 | None |  | 0.823 | `r-ae1b79422775c8a979b7` | `r-30d17c54ac2eae6167d0` |
| h/2 | P04_step_2x | last_isi | definedness | 31.49999999997135 | None |  | 1.59 | `r-ae1b79422775c8a979b7` | `r-30d17c54ac2eae6167d0` |
| h/2 | P04_step_2x | spike_count | exceeds | 16.0 | 0.0 | 16 | 3 | `r-ae1b79422775c8a979b7` | `r-30d17c54ac2eae6167d0` |
| h/2 | P05_long_step | adaptation_index | definedness | 0.002149159038242536 | None |  | 0.01 | `r-317893116e9cb0c903c3` | `r-0764fc815d36e1fc8119` |
| h/2 | P05_long_step | ahp_depth | definedness | 11.21389289347907 | None |  | 1.25504 | `r-317893116e9cb0c903c3` | `r-0764fc815d36e1fc8119` |
| h/2 | P05_long_step | ap_amplitude | definedness | 64.9877738975208 | None |  | 1.30527 | `r-317893116e9cb0c903c3` | `r-0764fc815d36e1fc8119` |
| h/2 | P05_long_step | first_spike_latency | definedness | 65.27999999981279 | None |  | 1.3064 | `r-317893116e9cb0c903c3` | `r-0764fc815d36e1fc8119` |
| h/2 | P05_long_step | last_isi | definedness | 55.2000000012049 | None |  | 2.61 | `r-317893116e9cb0c903c3` | `r-0764fc815d36e1fc8119` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 0.0 | 36 | 0.5 | `r-317893116e9cb0c903c3` | `r-0764fc815d36e1fc8119` |
| h/2 | P06_ramp | first_spike_latency | definedness | 415.849999999494 | None |  | 8.318 | `r-24b7e809e0450dd29615` | `r-8a6f2ae9249af8fcc2f7` |
| h/2 | P06_ramp | spike_count | exceeds | 21.0 | 0.0 | 21 | 3 | `r-24b7e809e0450dd29615` | `r-8a6f2ae9249af8fcc2f7` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
