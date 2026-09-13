# m-increase_dt-26c6d170d7

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.01ms", "old": "0.001ms"}], "factor": 10, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LEMS_LTS.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.01ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 10}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 271.13 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.28530394121576463 | 0.16473 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-0afb677bd4b2534f69c4` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 14.782995923996182 | 1.79051 | 0.828675 | `r-7fe8302f56856b53d535` | `r-0afb677bd4b2534f69c4` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 18.21999999998343 | 4.06 | 0.6 | `r-7fe8302f56856b53d535` | `r-0afb677bd4b2534f69c4` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 192.409999999825 | 9.79 | 4.044 | `r-7fe8302f56856b53d535` | `r-0afb677bd4b2534f69c4` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 11.448196909004414 | 0.871626 | 0.615991 | `r-7fe8302f56856b53d535` | `r-0afb677bd4b2534f69c4` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 6.00885324351097 | 8.58855 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-fa17cbccc14ffe8f5019` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 5.668818758647518 | 8.40919 | 1.31907 | `r-0e47469602e57d8257f5` | `r-7e24939d256bece3d40f` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.3594142115576332 | 0.103587 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-98d8748d39d466c9f144` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 15.7756577835125 | 0.897896 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-98d8748d39d466c9f144` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 15.839999999985594 | 1.88 | 0.6 | `r-055cc6b1739501cecd9d` | `r-98d8748d39d466c9f144` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 197.71999999982017 | 5.03 | 4.044 | `r-055cc6b1739501cecd9d` | `r-98d8748d39d466c9f144` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 15.055308659871415 | 10.869624452209848 | 4.18568 | 1.3737 | `r-13bd10976ea90e0f7248` | `r-5a24bccdcc4f1f4bd507` |
| h/2 | P05_long_step | ahp_depth | exceeds | 14.517703374227494 | 10.458438233948286 | 4.05927 | 1.31907 | `r-d6d2d7202a5745e9444f` | `r-5e4d4f2cbf2d1d6d8143` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
