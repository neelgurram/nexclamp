# m-scale_conductance-979dd75955

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "0.0521193150515 mS_per_cm2", "old": "0.104238630103 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml[@id='HH2_477127614']/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.104238630103 mS_per_cm2", "new": "0.0521193150515 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1460.433 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 28.91999999987314 | 24.779999999876907 | 4.14 | 0.5784 | `r-50990666ac8ec9a46823` | `r-b7a5ea119f2a571bf3c9` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.68582479858395 | -47.840478866596456 | 12.8453 | 0.5 | `r-d2b3788dfa4671532754` | `r-11ee70329835683b6f9b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.0323406871115361 | 0.0321358 | 0.00128953 | `s-bd435463250c35027583` | `s-e4a1d4699b4a1c4d6a4a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 41.14999999983473 | 32.89999999984224 | 8.25 | 0.823 | `r-d2b3788dfa4671532754` | `r-11ee70329835683b6f9b` |
| h/1 | P04_step_2x | last_isi | exceeds | 32.02999999997087 | 24.139999999978045 | 7.89 | 1.59 | `r-d2b3788dfa4671532754` | `r-11ee70329835683b6f9b` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 21.0 | 6 | 3 | `r-d2b3788dfa4671532754` | `r-11ee70329835683b6f9b` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 65.31999999981275 | 45.41999999983085 | 19.9 | 1.3064 | `r-5fe7a143f3c88a372d40` | `r-5fb5f16f1eb6cc1eb43d` |
| h/1 | P05_long_step | last_isi | exceeds | 56.07000000122389 | 34.58000000075481 | 21.49 | 2.61 | `r-5fe7a143f3c88a372d40` | `r-5fb5f16f1eb6cc1eb43d` |
| h/1 | P05_long_step | spike_count | exceeds | 36.0 | 58.0 | 22 | 0.5 | `r-5fe7a143f3c88a372d40` | `r-5fb5f16f1eb6cc1eb43d` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 415.89999999949396 | 273.49999999962347 | 142.4 | 8.318 | `r-0957e33747fc542d9104` | `r-b74bf277de7b0dd32c49` |
| h/1 | P06_ramp | spike_count | exceeds | 20.0 | 29.0 | 9 | 3 | `r-0957e33747fc542d9104` | `r-b74bf277de7b0dd32c49` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -93.17739953460699 | -114.91772292022708 | 21.7403 | 0.5 | `r-d2b3788dfa4671532754` | `r-11ee70329835683b6f9b` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 28.749999999873296 | 24.619999999877052 | 4.13 | 0.5784 | `r-cff06a8ac591df54f373` | `r-147fbb8cbf1d50707adf` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -60.68582508010861 | -47.839925601215484 | 12.8459 | 0.5 | `r-ae1b79422775c8a979b7` | `r-d09476efa4a03492a69e` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06447647018646267 | 0.0323406871115361 | 0.0321358 | 0.00128953 | `s-4d054cac6fc39c11b1f5` | `s-21f8e1edcf4420873af5` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 41.10999999983477 | 32.869999999842264 | 8.24 | 0.823 | `r-ae1b79422775c8a979b7` | `r-d09476efa4a03492a69e` |
| h/2 | P04_step_2x | last_isi | exceeds | 31.49999999997135 | 23.579999999978554 | 7.92 | 1.59 | `r-ae1b79422775c8a979b7` | `r-d09476efa4a03492a69e` |
| h/2 | P04_step_2x | spike_count | exceeds | 16.0 | 21.0 | 5 | 3 | `r-ae1b79422775c8a979b7` | `r-d09476efa4a03492a69e` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 65.27999999981279 | 45.38999999983088 | 19.89 | 1.3064 | `r-317893116e9cb0c903c3` | `r-0c4175e3965b5bdef5f2` |
| h/2 | P05_long_step | last_isi | exceeds | 55.2000000012049 | 33.88000000073953 | 21.32 | 2.61 | `r-317893116e9cb0c903c3` | `r-0c4175e3965b5bdef5f2` |
| h/2 | P05_long_step | spike_count | exceeds | 36.0 | 60.0 | 24 | 0.5 | `r-317893116e9cb0c903c3` | `r-0c4175e3965b5bdef5f2` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 415.849999999494 | 273.4599999996235 | 142.39 | 8.318 | `r-24b7e809e0450dd29615` | `r-c581b83ab85dcb99b9d3` |
| h/2 | P06_ramp | spike_count | exceeds | 21.0 | 30.0 | 9 | 3 | `r-24b7e809e0450dd29615` | `r-c581b83ab85dcb99b9d3` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -93.17739972381598 | -114.91771145477297 | 21.7403 | 0.5 | `r-ae1b79422775c8a979b7` | `r-d09476efa4a03492a69e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
