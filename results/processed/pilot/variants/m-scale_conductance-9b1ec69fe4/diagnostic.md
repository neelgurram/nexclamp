# m-scale_conductance-9b1ec69fe4

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "2.7e-5 S_per_cm2", "old": "3e-5 S_per_cm2"}], "element": "channelDensity", "element_id": "IM_all", "factor": 0.9, "generator_seed": 20260913}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "condDensity", "old": "3e-5 S_per_cm2", "new": "2.7e-5 S_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1937.372 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 167.7299999998475 | 34.47 | 4.044 | `r-7fe8302f56856b53d535` | `r-50fdfa3fd704e3ab44ac` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 14.392630972966272 | 2.07281 | 0.615991 | `r-7fe8302f56856b53d535` | `r-50fdfa3fd704e3ab44ac` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 168.0699999998472 | 34.68 | 4.044 | `r-055cc6b1739501cecd9d` | `r-eb4438836dade2e41895` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 14.470732942648155 | 2.07724 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-eb4438836dade2e41895` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
