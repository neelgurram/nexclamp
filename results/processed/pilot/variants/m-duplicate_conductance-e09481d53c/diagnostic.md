# m-duplicate_conductance-e09481d53c

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260913, "new_id": "Kd_all_dup", "source_id": "Kd_all"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"0.005 S_per_cm2\" id=\"Kd_all_dup\" ionChannel=\"Kd\" ion=\"k\" erev=\"-100.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1614.421 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.10673969458726523 | 0.343294 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 7.096504367830278 | 9.477 | 0.828675 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.629999999999427 | 0.15 | 0.05 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 36.059999999967204 | 21.9 | 0.6 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 120.09999999989077 | 82.1 | 4.044 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 13.337601365790292 | 1.01778 | 0.615991 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-7fe8302f56856b53d535` | `r-a51c908837fe9f2a76ef` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 5.78886731974255 | 8.80854 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-5cc710c096466537cd1f` |
| h/1 | P04_step_2x | ap_half_width | exceeds | 0.7299999999993361 | 0.5899999999994634 | 0.14 | 0.05 | `r-c8dafa7919f8741d136a` | `r-5cc710c096466537cd1f` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 5.581637705485022 | 8.49638 | 1.31907 | `r-0e47469602e57d8257f5` | `r-351b3f0b3a3884d6b072` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.7199999999993452 | 0.5799999999994725 | 0.14 | 0.05 | `r-0e47469602e57d8257f5` | `r-351b3f0b3a3884d6b072` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.10773920221562774 | 0.355262 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 7.198928936004663 | 9.47462 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.629999999999427 | 0.15 | 0.05 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 35.80999999996743 | 21.85 | 0.6 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 120.8399999998901 | 81.91 | 4.044 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 13.293276260887074 | 0.899783 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-055cc6b1739501cecd9d` | `r-ca85caa3c394414f4151` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 15.055308659871415 | 6.296824773153219 | 8.75848 | 1.3737 | `r-13bd10976ea90e0f7248` | `r-7ce037de71724faae834` |
| h/2 | P04_step_2x | ap_half_width | exceeds | 0.7299999999993361 | 0.5899999999994634 | 0.14 | 0.05 | `r-13bd10976ea90e0f7248` | `r-7ce037de71724faae834` |
| h/2 | P05_long_step | ahp_depth | exceeds | 14.517703374227494 | 6.085788091023758 | 8.43192 | 1.31907 | `r-d6d2d7202a5745e9444f` | `r-2269ecc8f6e7fdc8763e` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.7299999999993361 | 0.5899999999994634 | 0.14 | 0.05 | `r-d6d2d7202a5745e9444f` | `r-2269ecc8f6e7fdc8763e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
