# m-scale_conductance-61ece641cf

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "47.7398593036 mS_per_cm2", "old": "59.6748241295 mS_per_cm2"}], "element": "channelDensityVShift", "element_id": "Na_all", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "condDensity", "old": "59.6748241295 mS_per_cm2", "new": "47.7398593036 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1510.197 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 68.17416534535639 | 61.841576385003336 | 6.33259 | 3.91218 | `r-50990666ac8ec9a46823` | `r-7d00a1f313bba9b58d9c` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 29.749999999872387 | 0.83 | 0.5784 | `r-50990666ac8ec9a46823` | `r-7d00a1f313bba9b58d9c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.06642305853425312 | 0.00194659 | 0.00128953 | `s-bd435463250c35027583` | `s-81c843d3e7af018ccde0` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 65.66345214961734 | 59.25761032288638 | 6.40584 | 1.31327 | `r-d2b3788dfa4671532754` | `r-acd61a39c28e648eaca3` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 41.14999999983473 | 42.6199999998334 | 1.47 | 0.823 | `r-d2b3788dfa4671532754` | `r-acd61a39c28e648eaca3` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 65.26353454776816 | 58.76797866952984 | 6.49556 | 1.30527 | `r-5fe7a143f3c88a372d40` | `r-ff93dc1815bf917e07bf` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 65.31999999981275 | 68.60999999980976 | 3.29 | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-ff93dc1815bf917e07bf` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 35.0 | 1 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-ff93dc1815bf917e07bf` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 425.9899999994848 | 10.09 | 8.318 | `r-0957e33747fc542d9104` | `r-efda558dd1c411503edf` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 66.87010574454787 | 60.632741929882414 | 6.23736 | 3.91218 | `r-cff06a8ac591df54f373` | `r-ebd670bdceba90e5aacd` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 29.589999999872532 | 0.84 | 0.5784 | `r-cff06a8ac591df54f373` | `r-ebd670bdceba90e5aacd` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.06642305853425312 | 0.00194659 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-73939aaddbd357110d36` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 65.3342704782316 | 58.94656944439143 | 6.3877 | 1.31327 | `r-ae1b79422775c8a979b7` | `r-c1e541cbc07a77074ed3` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 41.10999999983477 | 42.57999999983343 | 1.47 | 0.823 | `r-ae1b79422775c8a979b7` | `r-c1e541cbc07a77074ed3` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 64.9877738975208 | 58.49903679069902 | 6.48874 | 1.30527 | `r-317893116e9cb0c903c3` | `r-5905cee7e854a482129f` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 65.27999999981279 | 68.5699999998098 | 3.29 | 1.3064 | `r-317893116e9cb0c903c3` | `r-5905cee7e854a482129f` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 35.0 | 1 | 0.5 | `r-317893116e9cb0c903c3` | `r-5905cee7e854a482129f` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 425.9399999994848 | 10.09 | 8.318 | `r-24b7e809e0450dd29615` | `r-452853b9d7070f25d35d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
