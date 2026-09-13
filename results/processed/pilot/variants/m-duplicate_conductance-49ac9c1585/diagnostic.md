# m-duplicate_conductance-49ac9c1585

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260913, "new_id": "Na_all_dup", "source_id": "Na_all"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"0.05 S_per_cm2\" id=\"Na_all_dup\" ionChannel=\"Na\" ion=\"na\" erev=\"50.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1669.626 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.45003406360930803 | 0.29127937336814597 | 0.158755 | 0.0450034 | `r-7fe8302f56856b53d535` | `r-312ca1d45e7ea9e1b7b7` |
| h/1 | P00_canonical | ahp_depth | exceeds | 16.573501743312846 | 15.536720422746654 | 1.03678 | 0.828675 | `r-7fe8302f56856b53d535` | `r-312ca1d45e7ea9e1b7b7` |
| h/1 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.8699999999992087 | 0.09 | 0.05 | `r-7fe8302f56856b53d535` | `r-312ca1d45e7ea9e1b7b7` |
| h/1 | P00_canonical | first_isi | exceeds | 14.159999999987122 | 16.189999999985275 | 2.03 | 0.6 | `r-7fe8302f56856b53d535` | `r-312ca1d45e7ea9e1b7b7` |
| h/1 | P00_canonical | last_isi | exceeds | 202.1999999998161 | 185.45999999983133 | 16.74 | 4.044 | `r-7fe8302f56856b53d535` | `r-312ca1d45e7ea9e1b7b7` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 92.73429489294529 | 95.57655716101759 | 2.84226 | 1.85469 | `r-c8dafa7919f8741d136a` | `r-95e19a10d6f31abf57b2` |
| h/1 | P04_step_2x | ap_half_width | exceeds | 0.7299999999993361 | 0.8299999999992451 | 0.1 | 0.05 | `r-c8dafa7919f8741d136a` | `r-95e19a10d6f31abf57b2` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 91.18347931093976 | 94.23575973720537 | 3.05228 | 1.82367 | `r-0e47469602e57d8257f5` | `r-b26c3113a085db4ad303` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.7199999999993452 | 0.8199999999992542 | 0.1 | 0.05 | `r-0e47469602e57d8257f5` | `r-b26c3113a085db4ad303` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.4630010462892806 | 0.29867773785018986 | 0.164323 | 0.0450034 | `r-055cc6b1739501cecd9d` | `r-441a00cf4a3c6a9bd771` |
| h/2 | P00_canonical | ahp_depth | exceeds | 16.673553569797534 | 15.623977748870885 | 1.04958 | 0.828675 | `r-055cc6b1739501cecd9d` | `r-441a00cf4a3c6a9bd771` |
| h/2 | P00_canonical | ap_half_width | exceeds | 0.7799999999992906 | 0.8699999999992087 | 0.09 | 0.05 | `r-055cc6b1739501cecd9d` | `r-441a00cf4a3c6a9bd771` |
| h/2 | P00_canonical | first_isi | exceeds | 13.959999999987303 | 15.989999999985457 | 2.03 | 0.6 | `r-055cc6b1739501cecd9d` | `r-441a00cf4a3c6a9bd771` |
| h/2 | P00_canonical | last_isi | exceeds | 202.7499999998156 | 186.11999999983072 | 16.63 | 4.044 | `r-055cc6b1739501cecd9d` | `r-441a00cf4a3c6a9bd771` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 92.6621055623362 | 95.59976577940549 | 2.93766 | 1.85469 | `r-13bd10976ea90e0f7248` | `r-685bac0d645417e1bb2d` |
| h/2 | P04_step_2x | ap_half_width | exceeds | 0.7299999999993361 | 0.8299999999992451 | 0.1 | 0.05 | `r-13bd10976ea90e0f7248` | `r-685bac0d645417e1bb2d` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 91.13381576739826 | 94.28588485926801 | 3.15207 | 1.82367 | `r-d6d2d7202a5745e9444f` | `r-980f0d77a7e44d43a4ee` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.7299999999993361 | 0.8199999999992542 | 0.09 | 0.05 | `r-d6d2d7202a5745e9444f` | `r-980f0d77a7e44d43a4ee` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
