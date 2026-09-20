# m-scale_capacitance-d886e6ca3e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "2.13391305762 uF_per_cm2", "old": "4.26782611524 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "4.26782611524 uF_per_cm2", "new": "2.13391305762 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1496.38 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 7.666865774086709 | -0.11416398275899553 | 7.78103 | 6.89996 | `r-50990666ac8ec9a46823` | `r-400a1d4568fe9464917d` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 68.17416534535639 | 80.57992172373817 | 12.4058 | 3.91218 | `r-50990666ac8ec9a46823` | `r-400a1d4568fe9464917d` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 14.729999999886047 | 14.19 | 0.5784 | `r-50990666ac8ec9a46823` | `r-400a1d4568fe9464917d` |
| h/1 | P00_canonical | last_isi | exceeds | 25.819999999976517 | 16.979999999984557 | 8.84 | 6.6 | `r-50990666ac8ec9a46823` | `r-400a1d4568fe9464917d` |
| h/1 | P00_canonical | spike_count | exceeds | 28.0 | 44.0 | 16 | 9 | `r-50990666ac8ec9a46823` | `r-400a1d4568fe9464917d` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 11.031660542810322 | 3.5592859217379953 | 7.47237 | 1.26162 | `r-d2b3788dfa4671532754` | `r-9ea5c7be3fe8a2572624` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 65.66345214961734 | 78.13383865419655 | 12.4704 | 1.31327 | `r-d2b3788dfa4671532754` | `r-9ea5c7be3fe8a2572624` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 41.14999999983473 | 20.699999999853333 | 20.45 | 0.823 | `r-d2b3788dfa4671532754` | `r-9ea5c7be3fe8a2572624` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 21.5499999999804 | 10.48 | 1.59 | `r-d2b3788dfa4671532754` | `r-9ea5c7be3fe8a2572624` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 24.0 | 9 | 3 | `r-d2b3788dfa4671532754` | `r-9ea5c7be3fe8a2572624` |
| h/1 | P05_long_step | ahp_depth | exceeds | 10.79554604085748 | 3.2340295740855396 | 7.56152 | 1.25504 | `r-5fe7a143f3c88a372d40` | `r-14eb3141ea0a48f04ea6` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 65.26353454776816 | 77.58669662570807 | 12.3232 | 1.30527 | `r-5fe7a143f3c88a372d40` | `r-14eb3141ea0a48f04ea6` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 65.31999999981275 | 32.63999999984247 | 32.68 | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-14eb3141ea0a48f04ea6` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 35.74000000078013 | 20.33 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-14eb3141ea0a48f04ea6` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 57.0 | 21 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-14eb3141ea0a48f04ea6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 381.72999999952503 | 34.17 | 8.318 | `r-0957e33747fc542d9104` | `r-dfa0e143b1af7aac60b7` |
| h/1 | P06_ramp | spike_count | exceeds | 20.0 | 31.0 | 11 | 3 | `r-0957e33747fc542d9104` | `r-dfa0e143b1af7aac60b7` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | 2.605092806495975 |  | inf | `r-00f5b9389bbdd9e19b1d` | `r-b016a693e9b97b73b7ce` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 78.73919296349928 |  | inf | `r-00f5b9389bbdd9e19b1d` | `r-b016a693e9b97b73b7ce` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 4.309999999868239 |  | inf | `r-00f5b9389bbdd9e19b1d` | `r-b016a693e9b97b73b7ce` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-00f5b9389bbdd9e19b1d` | `r-b016a693e9b97b73b7ce` |
| h/2 | P00_canonical | ahp_depth | exceeds | 9.966850862869194 | 2.4334314756279554 | 7.53342 | 6.89996 | `r-cff06a8ac591df54f373` | `r-eeda5c726f29c30d9e53` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 66.87010574454787 | 79.43167419653376 | 12.5616 | 3.91218 | `r-cff06a8ac591df54f373` | `r-eeda5c726f29c30d9e53` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 14.589999999886174 | 14.16 | 0.5784 | `r-cff06a8ac591df54f373` | `r-eeda5c726f29c30d9e53` |
| h/2 | P00_canonical | last_isi | exceeds | 23.619999999978518 | 15.859999999985575 | 7.76 | 6.6 | `r-cff06a8ac591df54f373` | `r-eeda5c726f29c30d9e53` |
| h/2 | P00_canonical | spike_count | exceeds | 31.0 | 47.0 | 16 | 9 | `r-cff06a8ac591df54f373` | `r-eeda5c726f29c30d9e53` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 11.452200846353144 | 4.043370485935242 | 7.40883 | 1.26162 | `r-ae1b79422775c8a979b7` | `r-434c83cd187e37f12397` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 65.3342704782316 | 77.87233734277805 | 12.5381 | 1.31327 | `r-ae1b79422775c8a979b7` | `r-434c83cd187e37f12397` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 41.10999999983477 | 20.66999999985336 | 20.44 | 0.823 | `r-ae1b79422775c8a979b7` | `r-434c83cd187e37f12397` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 21.22999999998069 | 10.27 | 1.59 | `r-ae1b79422775c8a979b7` | `r-434c83cd187e37f12397` |
| h/2 | P04_step_2x | spike_count | exceeds | 16.0 | 24.0 | 8 | 3 | `r-ae1b79422775c8a979b7` | `r-434c83cd187e37f12397` |
| h/2 | P05_long_step | ahp_depth | exceeds | 11.21389289347907 | 3.714062929800363 | 7.49983 | 1.25504 | `r-317893116e9cb0c903c3` | `r-988c649dc3928724e77b` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 64.9877738975208 | 77.26649475179445 | 12.2787 | 1.30527 | `r-317893116e9cb0c903c3` | `r-988c649dc3928724e77b` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 65.27999999981279 | 32.59999999984251 | 32.68 | 1.3064 | `r-317893116e9cb0c903c3` | `r-988c649dc3928724e77b` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 35.350000000771615 | 19.85 | 2.61 | `r-317893116e9cb0c903c3` | `r-988c649dc3928724e77b` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 57.0 | 21 | 0.5 | `r-317893116e9cb0c903c3` | `r-988c649dc3928724e77b` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 381.6799999995251 | 34.17 | 8.318 | `r-24b7e809e0450dd29615` | `r-ff50d639c9d02f719e7d` |
| h/2 | P06_ramp | spike_count | exceeds | 21.0 | 31.0 | 10 | 3 | `r-24b7e809e0450dd29615` | `r-ff50d639c9d02f719e7d` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | 3.086980105088685 |  | inf | `r-34e1187a894445f911cf` | `r-2a18dcfe964cc19a16c3` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 78.49634170696295 |  | inf | `r-34e1187a894445f911cf` | `r-2a18dcfe964cc19a16c3` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 4.2799999998682665 |  | inf | `r-34e1187a894445f911cf` | `r-2a18dcfe964cc19a16c3` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-34e1187a894445f911cf` | `r-2a18dcfe964cc19a16c3` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
