# m-shift_channel_vshift-8dac96bdae

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_channel_vshift
- parameters: `{"changes": [{"attribute": "vShift", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "-3.20080138951 mV", "old": "1.79919861049 mV"}], "channel": "Na", "delta_mV": -5.0, "element_id": "Na_all", "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "vShift", "old": "1.79919861049 mV", "new": "-3.20080138951 mV", "action": "set", "note": "shift_channel_vshift"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1462.617 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 68.17416534535639 | 76.53405380306441 | 8.35989 | 3.91218 | `r-50990666ac8ec9a46823` | `r-f6737678091aa9298f62` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 22.349999999879117 | 6.57 | 0.5784 | `r-50990666ac8ec9a46823` | `r-f6737678091aa9298f62` |
| h/1 | P00_canonical | last_isi | exceeds | 25.819999999976517 | 18.299999999983356 | 7.52 | 6.6 | `r-50990666ac8ec9a46823` | `r-f6737678091aa9298f62` |
| h/1 | P00_canonical | spike_count | exceeds | 28.0 | 41.0 | 13 | 9 | `r-50990666ac8ec9a46823` | `r-f6737678091aa9298f62` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.04675227101973909 | 0.0177242 | 0.00128953 | `s-bd435463250c35027583` | `s-4a0ad2d50e622f265340` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 65.66345214961734 | 73.89179611359035 | 8.22834 | 1.31327 | `r-d2b3788dfa4671532754` | `r-0d2d6ef6f0015891c293` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 41.14999999983473 | 30.239999999844656 | 10.91 | 0.823 | `r-d2b3788dfa4671532754` | `r-0d2d6ef6f0015891c293` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 19.289999999982456 | 12.74 | 1.59 | `r-d2b3788dfa4671532754` | `r-0d2d6ef6f0015891c293` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 27.0 | 12 | 3 | `r-d2b3788dfa4671532754` | `r-0d2d6ef6f0015891c293` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 65.26353454776816 | 73.55947876145397 | 8.29594 | 1.30527 | `r-5fe7a143f3c88a372d40` | `r-5f1094062e67aadae165` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 65.31999999981275 | 43.66999999983244 | 21.65 | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-5f1094062e67aadae165` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 29.350000000640648 | 26.72 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-5f1094062e67aadae165` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 70.0 | 34 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-5f1094062e67aadae165` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 326.97999999957483 | 88.92 | 8.318 | `r-0957e33747fc542d9104` | `r-1886eb91f47b6b9fc786` |
| h/1 | P06_ramp | spike_count | exceeds | 20.0 | 35.0 | 15 | 3 | `r-0957e33747fc542d9104` | `r-1886eb91f47b6b9fc786` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 66.87010574454787 | 75.01953354001529 | 8.14943 | 3.91218 | `r-cff06a8ac591df54f373` | `r-07800e0250bd7487ac6c` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 22.17999999987927 | 6.57 | 0.5784 | `r-cff06a8ac591df54f373` | `r-07800e0250bd7487ac6c` |
| h/2 | P00_canonical | last_isi | exceeds | 23.619999999978518 | 15.989999999985457 | 7.63 | 6.6 | `r-cff06a8ac591df54f373` | `r-07800e0250bd7487ac6c` |
| h/2 | P00_canonical | spike_count | exceeds | 31.0 | 47.0 | 16 | 9 | `r-cff06a8ac591df54f373` | `r-07800e0250bd7487ac6c` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.04675227101973909 | 0.0177242 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-69367493ba4058c1e220` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 65.3342704782316 | 73.56506157035216 | 8.23079 | 1.31327 | `r-ae1b79422775c8a979b7` | `r-82347bc8acd43b5c9563` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 41.10999999983477 | 30.199999999844692 | 10.91 | 0.823 | `r-ae1b79422775c8a979b7` | `r-82347bc8acd43b5c9563` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 18.639999999983047 | 12.86 | 1.59 | `r-ae1b79422775c8a979b7` | `r-82347bc8acd43b5c9563` |
| h/2 | P04_step_2x | spike_count | exceeds | 16.0 | 28.0 | 12 | 3 | `r-ae1b79422775c8a979b7` | `r-82347bc8acd43b5c9563` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 64.9877738975208 | 73.30197525184647 | 8.3142 | 1.30527 | `r-317893116e9cb0c903c3` | `r-2c7db128bf932d6bc84e` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 65.27999999981279 | 43.62999999983248 | 21.65 | 1.3064 | `r-317893116e9cb0c903c3` | `r-2c7db128bf932d6bc84e` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 28.40000000061991 | 26.8 | 2.61 | `r-317893116e9cb0c903c3` | `r-2c7db128bf932d6bc84e` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 72.0 | 36 | 0.5 | `r-317893116e9cb0c903c3` | `r-2c7db128bf932d6bc84e` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 326.9299999995749 | 88.92 | 8.318 | `r-24b7e809e0450dd29615` | `r-fa641e4e1bd4c7413b11` |
| h/2 | P06_ramp | spike_count | exceeds | 21.0 | 37.0 | 16 | 3 | `r-24b7e809e0450dd29615` | `r-fa641e4e1bd4c7413b11` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
