# m-recording_resolution-46bcb819ee

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260913, "sample_every_ms": 0.25}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.25}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1598.175 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.01163101444587 | 97.15863402358048 | 2.853 | 2.00023 | `r-7fe8302f56856b53d535` | `r-0553a9c85faf2a4d3b3a` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.8499999999992269 | 0.07 | 0.05 | `r-7fe8302f56856b53d535` | `r-0553a9c85faf2a4d3b3a` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.9338417077712 | 96.62106215859443 | 3.31278 | 2.00023 | `r-055cc6b1739501cecd9d` | `r-30419fb2699d680a303a` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.8599999999992178 | 0.08 | 0.05 | `r-055cc6b1739501cecd9d` | `r-30419fb2699d680a303a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
