# m-scale_conductance-44150b501c

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "new": "0.11360408 mS_per_cm2", "old": "0.1420051 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_pyr_all", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_pyr_all']", "attribute": "condDensity", "old": "0.1420051 mS_per_cm2", "new": "0.11360408 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3157.344 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.006522778498736425 | 0.00109282 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-e3cc3fb5381901f1cd1e` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 24.359999999850004 | 1.05 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-fb5a54a6f1afdd735a28` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 430.33999999960866 | 20.78 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-fb5a54a6f1afdd735a28` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 34.1499999998411 | 3.02 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-ffd228d54d4607adfcbf` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 506.879999999539 | 80.01 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-ffd228d54d4607adfcbf` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 428.54999999948245 | 72.59 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-71719fbf3aad64f53526` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424023132327 | -71.75014665069583 | 0.935906 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-fb5a54a6f1afdd735a28` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | -6.935772814432781 |  | inf | `r-195ba3020e76bc4e3add` | `r-658adbba6cdd718372f7` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 97.94194030767557 |  | inf | `r-195ba3020e76bc4e3add` | `r-658adbba6cdd718372f7` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 27.879999999846802 |  | inf | `r-195ba3020e76bc4e3add` | `r-658adbba6cdd718372f7` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-195ba3020e76bc4e3add` | `r-658adbba6cdd718372f7` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.006522778498736425 | 0.00109282 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-42a217796a22f3298f96` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 24.30999999985005 | 1.05 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-dca38405d926c3c97741` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 429.4099999996095 | 20.77 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-dca38405d926c3c97741` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 34.089999999841154 | 3.02 | 0.7434 | `r-493fa57e11933a720397` | `r-a157bdf928b79f971150` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 505.9699999995398 | 80 | 11.7378 | `r-493fa57e11933a720397` | `r-a157bdf928b79f971150` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 428.4699999994825 | 72.59 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-df34936cb4955fa9cc9c` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424049987795 | -71.75014685974124 | 0.935906 | 0.5 | `r-16be743cbc8f0485fd82` | `r-dca38405d926c3c97741` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | -6.934515932718909 |  | inf | `r-eb52f398ba2e116da449` | `r-64e64946029e26bf0935` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 97.52888107244742 |  | inf | `r-eb52f398ba2e116da449` | `r-64e64946029e26bf0935` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 27.42999999984721 |  | inf | `r-eb52f398ba2e116da449` | `r-64e64946029e26bf0935` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-eb52f398ba2e116da449` | `r-64e64946029e26bf0935` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
