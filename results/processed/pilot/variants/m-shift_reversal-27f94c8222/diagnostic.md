# m-shift_reversal-27f94c8222

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "new": "45.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "Na_all", "generator_seed": 20260913, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "attribute": "erev", "old": "50.0 mV", "new": "45.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2122.562 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.5659605091530608 | 0.115926 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-8c77e84bf8c03c36d7ad` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 17.673607028964994 | 1.10011 | 0.828675 | `r-7fe8302f56856b53d535` | `r-8c77e84bf8c03c36d7ad` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 95.19048309617733 | 4.82115 | 2.00023 | `r-7fe8302f56856b53d535` | `r-8c77e84bf8c03c36d7ad` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 12.289999999988822 | 1.87 | 0.6 | `r-7fe8302f56856b53d535` | `r-8c77e84bf8c03c36d7ad` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 174.07999999984173 | 28.12 | 4.044 | `r-7fe8302f56856b53d535` | `r-8c77e84bf8c03c36d7ad` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 15.022345739313193 | 2.70252 | 0.615991 | `r-7fe8302f56856b53d535` | `r-8c77e84bf8c03c36d7ad` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.73429489294529 | 87.73717117430411 | 4.99712 | 1.85469 | `r-c8dafa7919f8741d136a` | `r-49ed9b4a1c4dd5d90560` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.18347931093976 | 86.18749618663429 | 4.99598 | 1.82367 | `r-0e47469602e57d8257f5` | `r-c4ba9a491fca14262798` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.5763961112367173 | 0.113395 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-0d455653bc8351adba77` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 17.776290996551538 | 1.10274 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-0d455653bc8351adba77` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 95.11647033979364 | 4.81737 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-0d455653bc8351adba77` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 12.129999999988968 | 1.83 | 0.6 | `r-055cc6b1739501cecd9d` | `r-0d455653bc8351adba77` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 174.30999999984152 | 28.44 | 4.044 | `r-055cc6b1739501cecd9d` | `r-0d455653bc8351adba77` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 15.098897780488226 | 2.7054 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-0d455653bc8351adba77` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.6621055623362 | 87.68401336830414 | 4.97809 | 1.85469 | `r-13bd10976ea90e0f7248` | `r-9427fe340e7f4751d6aa` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.13381576739826 | 86.15034485009397 | 4.98347 | 1.82367 | `r-d6d2d7202a5745e9444f` | `r-244fa27cfdf4cf9aa497` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
