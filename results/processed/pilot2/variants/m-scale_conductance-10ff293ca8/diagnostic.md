# m-scale_conductance-10ff293ca8

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "0.075 mS_per_cm2", "old": "0.15 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.15 mS_per_cm2", "new": "0.075 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 896.915 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 10.069999999863 | 7.13 | 0.5 | `r-4cceac4cec0eb866659f` | `r-3eb3dae08757c4be7ae7` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 13.209999999987986 | 7.01 | 0.5 | `r-4cceac4cec0eb866659f` | `r-3eb3dae08757c4be7ae7` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 31.0 | 11 | 0.5 | `r-4cceac4cec0eb866659f` | `r-3eb3dae08757c4be7ae7` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 6.0 | 6 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -60.91402953033431 | -55.51094929559746 | 5.40308 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.17894952530564853 | 0.205348 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-e452bf28638b0a2e122d` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 6.349999999866384 | 1.66 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 8.919999999991887 | 1.62 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P04_step_2x | spike_count | exceeds | 47.0 | 56.0 | 9 | 3 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 8.609999999864328 | 4.06 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-259e7b6f88afc8ca662d` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 11.640000000254076 | 3.97 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-259e7b6f88afc8ca662d` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 172.0 | 44 | 3 | `r-d95212df9ca6b2b4efff` | `r-259e7b6f88afc8ca662d` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 363.4899999995416 | 191.8099999996977 | 171.68 | 7.2698 | `r-5888f8cf54a64bb2eb2f` | `r-62d46e7eef3d889ea01b` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 80.0 | 19 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-62d46e7eef3d889ea01b` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -88.16673006286652 | -106.33346285247835 | 18.1667 | 0.5 | `r-54e05e4e4388308e9268` | `r-021307729cf1e7122622` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 17.189999999856525 | 10.069999999863 | 7.12 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-f4d2edcbbc391b595f77` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 13.169999999988022 | 7.02 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-f4d2edcbbc391b595f77` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 31.0 | 11 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-f4d2edcbbc391b595f77` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 6.0 | 6 | 0.5 | `r-e087238cb438e653e31d` | `r-7e2d21dcd75a0540434c` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -60.91402884902938 | -55.547475948367165 | 5.36655 | 0.5 | `r-e087238cb438e653e31d` | `r-7e2d21dcd75a0540434c` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.17894952530564853 | 0.205348 | 0.00768595 | `s-a5d560731591d7405a9c` | `s-955ef95c9de9ff3080f7` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.989999999864892 | 6.329999999866402 | 1.66 | 0.5 | `r-e087238cb438e653e31d` | `r-7e2d21dcd75a0540434c` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 8.819999999991978 | 1.62 | 0.5 | `r-e087238cb438e653e31d` | `r-7e2d21dcd75a0540434c` |
| h/2 | P04_step_2x | spike_count | exceeds | 48.0 | 56.0 | 8 | 3 | `r-e087238cb438e653e31d` | `r-7e2d21dcd75a0540434c` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.629999999860672 | 8.579999999864356 | 4.05 | 0.5 | `r-880359fc85650f897997` | `r-f379af994425be2cf52f` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 11.510000000251239 | 3.97 | 0.5 | `r-880359fc85650f897997` | `r-f379af994425be2cf52f` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 173.0 | 44 | 3 | `r-880359fc85650f897997` | `r-f379af994425be2cf52f` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 363.43999999954167 | 191.75999999969775 | 171.68 | 7.2698 | `r-b0adc3019253aae3e3e8` | `r-738aa3935bedd5fc9ce9` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 81.0 | 20 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-738aa3935bedd5fc9ce9` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -88.16673142547639 | -106.33346421356234 | 18.1667 | 0.5 | `r-e087238cb438e653e31d` | `r-7e2d21dcd75a0540434c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
