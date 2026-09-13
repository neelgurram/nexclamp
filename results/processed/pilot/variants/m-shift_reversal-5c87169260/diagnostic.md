# m-shift_reversal-5c87169260

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-95.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260913, "shift_mV": 5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-95.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2076.718 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.7172279644532592 | 0.267194 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 19.1799317970314 | 2.60643 | 0.828675 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 10.399999999990541 | 3.76 | 0.6 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 225.1199999997953 | 22.92 | 4.044 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 13.148379462252691 | 0.828557 | 0.615991 | `r-7fe8302f56856b53d535` | `r-e4e026235ff465541cad` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 16.920031870525193 | 2.32262 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | firing_regime | categorical | single_spike | tonic |  |  | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | first_isi | definedness | None | 57.09999999994807 |  | inf | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | last_isi | definedness | None | 57.09999999994807 |  | inf | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | mean_frequency | definedness | None | 17.44439598782424 |  | inf | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P04_step_2x | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-c8dafa7919f8741d136a` | `r-dde03969c4b9f75a0ff2` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 16.27267011515299 | 2.19466 | 1.31907 | `r-0e47469602e57d8257f5` | `r-0021a0beebd16a20cb27` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.7255621844882975 | 0.262561 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 19.279411418918627 | 2.60586 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 10.26999999999066 | 3.69 | 0.6 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 225.59999999979487 | 22.85 | 4.044 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 13.185219369108752 | 0.791726 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-64e03728e18c6cfafbc8` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 15.055308659871415 | 17.36131604512532 | 2.30601 | 1.3737 | `r-13bd10976ea90e0f7248` | `r-020bb83ef6d7daf89db8` |
| h/2 | P04_step_2x | firing_regime | categorical | single_spike | tonic |  |  | `r-13bd10976ea90e0f7248` | `r-020bb83ef6d7daf89db8` |
| h/2 | P04_step_2x | first_isi | definedness | None | 39.86999999996374 |  | inf | `r-13bd10976ea90e0f7248` | `r-020bb83ef6d7daf89db8` |
| h/2 | P04_step_2x | last_isi | definedness | None | 39.86999999996374 |  | inf | `r-13bd10976ea90e0f7248` | `r-020bb83ef6d7daf89db8` |
| h/2 | P04_step_2x | mean_frequency | definedness | None | 20.540207456140955 |  | inf | `r-13bd10976ea90e0f7248` | `r-020bb83ef6d7daf89db8` |
| h/2 | P04_step_2x | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-13bd10976ea90e0f7248` | `r-020bb83ef6d7daf89db8` |
| h/2 | P05_long_step | ahp_depth | exceeds | 14.517703374227494 | 16.68980725606282 | 2.1721 | 1.31907 | `r-d6d2d7202a5745e9444f` | `r-085bf44d59da5cb72a41` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
