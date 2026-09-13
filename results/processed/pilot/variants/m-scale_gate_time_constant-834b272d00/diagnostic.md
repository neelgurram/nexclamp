# m-scale_gate_time_constant-834b272d00

- model: `pospischil2008_lts`
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Na", "factor": 2.0, "gate": "m", "generator_seed": 20260913, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='m']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2132.2 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.34741584772601103 | 0.102618 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 15.382126010896684 | 1.19138 | 0.828675 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 16.14999999998531 | 1.99 | 0.6 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 206.34999999981233 | 4.15 | 4.044 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/1 | P00_canonical | mean_frequency | exceeds | 12.319822594574143 | 11.301350511403374 | 1.01847 | 0.615991 | `r-7fe8302f56856b53d535` | `r-61fd46efb75fd0f9275c` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.35755270664611927 | 0.105448 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 15.482879741672534 | 1.19067 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 15.91999999998552 | 1.96 | 0.6 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 207.01999999981172 | 4.27 | 4.044 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |
| h/2 | P00_canonical | mean_frequency | exceeds | 12.393493415976295 | 11.350737797974237 | 1.04276 | 0.615991 | `r-055cc6b1739501cecd9d` | `r-4f5e5b4eae4a0f451328` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
