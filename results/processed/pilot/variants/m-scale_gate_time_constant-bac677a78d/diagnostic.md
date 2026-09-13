# m-scale_gate_time_constant-bac677a78d

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "IM", "factor": 1.25, "gate": "p", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/IM/IM.channel.nml", "locator": "/neuroml[@id='IM']/ionChannel[@id='IM']/gate[@id='p']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"1.25\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2145.869 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.2448155292982877 | 0.205219 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-20eb30c924c2c50fc1f1` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 206.4899999998122 | 4.29 | 4.044 | `r-7fe8302f56856b53d535` | `r-20eb30c924c2c50fc1f1` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 10.586491636687365 | 1.73333 | 0.615991 | `r-7fe8302f56856b53d535` | `r-20eb30c924c2c50fc1f1` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.25765754837144395 | 0.205343 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-ee20c7a950056f089a81` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 207.34999999981142 | 4.6 | 4.044 | `r-055cc6b1739501cecd9d` | `r-ee20c7a950056f089a81` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 10.649343734208268 | 1.74415 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-ee20c7a950056f089a81` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
