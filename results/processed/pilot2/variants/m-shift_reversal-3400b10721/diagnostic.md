# m-shift_reversal-3400b10721

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kahp_pyr_soma_group']", "new": "-70.0 mV", "old": "-75.0 mV"}], "element": "channelDensity", "element_id": "Kahp_pyr_soma_group", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kahp_pyr_soma_group']", "attribute": "erev", "old": "-75.0 mV", "new": "-70.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1506.13 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | 0.024795690162097123 | 0.058812 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-2da37e0e72678eff37b7` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 36.839999999966494 | 40.05 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-2da37e0e72678eff37b7` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 15.0 | 7 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-2da37e0e72678eff37b7` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -64.96725969085692 | 1.24638 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-66cca1fd06302306e115` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.005395806297384059 | 0.00221979 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-1c7fa5f2c22b842929b8` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -7.940022852579531 | 0.920487 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-66cca1fd06302306e115` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 20.319999999853678 | 5.09 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-66cca1fd06302306e115` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 368.55999999966485 | 82.56 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-66cca1fd06302306e115` |
| h/1 | P05_long_step | ahp_depth | exceeds | -7.059071324666348 | -7.97701778666179 | 0.917946 | 0.5 | `r-f6700284baa99a5ef41f` | `r-0a1178edf3f7cd297371` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 27.569999999847084 | 9.6 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-0a1178edf3f7cd297371` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 431.90999999972655 | 154.98 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-0a1178edf3f7cd297371` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-f6700284baa99a5ef41f` | `r-0a1178edf3f7cd297371` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 325.1499999995765 | 175.99 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-e5447bd45f73717a8249` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-e5447bd45f73717a8249` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424023132327 | -70.15805413055422 | 0.656186 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-66cca1fd06302306e115` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | -8.093106653849077 |  | inf | `r-195ba3020e76bc4e3add` | `r-b87c611d902701375e8f` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 98.0150260935946 |  | inf | `r-195ba3020e76bc4e3add` | `r-b87c611d902701375e8f` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 8.579999999864356 |  | inf | `r-195ba3020e76bc4e3add` | `r-b87c611d902701375e8f` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-195ba3020e76bc4e3add` | `r-b87c611d902701375e8f` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | 0.024784922001199444 | 0.059157 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-67c697e8dc958075dda0` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 36.7199999999666 | 39.87 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-67c697e8dc958075dda0` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 15.0 | 7 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-67c697e8dc958075dda0` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -64.96725820465086 | 1.24639 | 0.5 | `r-16be743cbc8f0485fd82` | `r-c03ae52a5f573ff2f740` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.005395806297384059 | 0.00221979 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-adfaf805a618cebeff31` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -7.016957875569673 | -7.937255373636887 | 0.920297 | 0.5 | `r-16be743cbc8f0485fd82` | `r-c03ae52a5f573ff2f740` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 20.269999999853724 | 5.09 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-c03ae52a5f573ff2f740` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 367.6099999996657 | 82.57 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-c03ae52a5f573ff2f740` |
| h/2 | P05_long_step | ahp_depth | exceeds | -7.056752797444673 | -7.974509707132981 | 0.917757 | 0.5 | `r-493fa57e11933a720397` | `r-77ba738752aa90a420db` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 27.51999999984713 | 9.59 | 0.7434 | `r-493fa57e11933a720397` | `r-77ba738752aa90a420db` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 430.97999999964054 | 154.99 | 11.7378 | `r-493fa57e11933a720397` | `r-77ba738752aa90a420db` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-493fa57e11933a720397` | `r-77ba738752aa90a420db` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 325.0599999995766 | 176 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-220c6e8b818ce9049e9e` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-220c6e8b818ce9049e9e` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424049987795 | -70.15805426177981 | 0.656186 | 0.5 | `r-16be743cbc8f0485fd82` | `r-c03ae52a5f573ff2f740` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | -8.091376772562242 |  | inf | `r-eb52f398ba2e116da449` | `r-05a9522147cc646e5857` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 97.48746872108046 |  | inf | `r-eb52f398ba2e116da449` | `r-05a9522147cc646e5857` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 8.51999999986441 |  | inf | `r-eb52f398ba2e116da449` | `r-05a9522147cc646e5857` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-eb52f398ba2e116da449` | `r-05a9522147cc646e5857` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
