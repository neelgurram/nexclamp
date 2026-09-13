# m-increase_dt-12296e231e

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LEMS_LTS.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 557.565 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.379353406410434 | 0.0706807 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-c1391b812261ee915934` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 15.399999999985994 | 1.24 | 0.6 | `r-7fe8302f56856b53d535` | `r-c1391b812261ee915934` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 14.597407663981116 | 11.814285765330297 | 2.78312 | 1.3737 | `r-c8dafa7919f8741d136a` | `r-79e0e3270f61c1e6d7d8` |
| h/1 | P05_long_step | ahp_depth | exceeds | 14.078013743082678 | 11.38144800059041 | 2.69657 | 1.31907 | `r-0e47469602e57d8257f5` | `r-298607f946860b898c62` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 15.055308659871415 | 13.677202611287584 | 1.37811 | 1.3737 | `r-13bd10976ea90e0f7248` | `r-9a7ec723e15e2c92547c` |
| h/2 | P05_long_step | ahp_depth | exceeds | 14.517703374227494 | 13.190706858317384 | 1.327 | 1.31907 | `r-d6d2d7202a5745e9444f` | `r-5b9b4ad39a239dc8318d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
