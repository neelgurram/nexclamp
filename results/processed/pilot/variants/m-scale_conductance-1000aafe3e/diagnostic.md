# m-scale_conductance-1000aafe3e

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='IT_all']", "new": "3.6e-4 S_per_cm2", "old": "4e-4 S_per_cm2"}], "element": "channelDensityNernst", "element_id": "IT_all", "factor": 0.9, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='IT_all']", "attribute": "condDensity", "old": "4e-4 S_per_cm2", "new": "3.6e-4 S_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2078.622 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.2671563219115466 | 0.182878 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-1bb8a8898e7993b6a2e8` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 97.23264313024089 | 2.77899 | 2.00023 | `r-7fe8302f56856b53d535` | `r-1bb8a8898e7993b6a2e8` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 16.79999999998472 | 2.64 | 0.6 | `r-7fe8302f56856b53d535` | `r-1bb8a8898e7993b6a2e8` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 31.629999999752442 | 33.18999999975102 | 1.56 | 0.6326 | `r-7fe8302f56856b53d535` | `r-1bb8a8898e7993b6a2e8` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 10.892652905631557 | 1.42717 | 0.615991 | `r-7fe8302f56856b53d535` | `r-1bb8a8898e7993b6a2e8` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -74.93620969696036 | -75.47193822784418 | 0.535729 | 0.5 | `r-c8dafa7919f8741d136a` | `r-c8ebe72a3f2cc23957cd` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.0439519158527423 | 0.00529335 | 0.000773171 | `s-3999769ed965342ea63b` | `s-d45ec80e3c505a76da35` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 57.54999999981982 | 61.729999999816016 | 4.18 | 1.151 | `r-c8dafa7919f8741d136a` | `r-c8ebe72a3f2cc23957cd` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 77.49999999980167 | 85.29999999979458 | 7.8 | 1.55 | `r-0e47469602e57d8257f5` | `r-75124fb529339a015d2a` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.27341676147136873 | 0.189584 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-83929c916fc90401bcfe` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 97.25429153717681 | 2.67955 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-83929c916fc90401bcfe` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 16.56999999998493 | 2.61 | 0.6 | `r-055cc6b1739501cecd9d` | `r-83929c916fc90401bcfe` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 31.61999999975245 | 33.17999999975103 | 1.56 | 0.6326 | `r-055cc6b1739501cecd9d` | `r-83929c916fc90401bcfe` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 10.923291187651294 | 1.4702 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-83929c916fc90401bcfe` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -74.93623204345693 | -75.47195529632562 | 0.535723 | 0.5 | `r-13bd10976ea90e0f7248` | `r-d018e264ffd1c080cd5f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.038658561573663 | 0.0439519158527423 | 0.00529335 | 0.000773171 | `s-372d4e42bc81ae6ab2b8` | `s-447f50f067102c05703e` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 57.49999999981986 | 61.67999999981606 | 4.18 | 1.151 | `r-13bd10976ea90e0f7248` | `r-d018e264ffd1c080cd5f` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 77.43999999980173 | 85.22999999979464 | 7.79 | 1.55 | `r-d6d2d7202a5745e9444f` | `r-86449a9c2078e309b450` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
