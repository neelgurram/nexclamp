# m-wrong_compatible_component-51b1ad6cb5

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "new": "SKv3_1", "old": "SK_E2"}], "element_id": "SK_E2_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "attribute": "ionChannel", "old": "SK_E2", "new": "SKv3_1", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4515.88 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 11.809999999989259 | 3.98 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-b0e8dbdd3cca72d18178` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-b0e8dbdd3cca72d18178` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 13.349999999987858 | 23.3 | 0.733 | `r-49ced7acda977f37b12b` | `r-8777602e590dad83a7a6` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 37.0 | 22 | 0.5 | `r-49ced7acda977f37b12b` | `r-8777602e590dad83a7a6` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 17.25000000037653 | 125.72 | 3.03 | `r-b99907e8e6510bd22247` | `r-fd3f12384f7935c2386d` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 116.0 | 102 | 0.5 | `r-b99907e8e6510bd22247` | `r-fd3f12384f7935c2386d` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 46.0 | 22 | 0.5 | `r-da1341cbf9665d4e7639` | `r-533ba524cd7bd6938df2` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 11.779999999989286 | 3.99 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-66bf97374cf915b2dc3c` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-66bf97374cf915b2dc3c` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 13.319999999987886 | 23.24 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-2624909d11d0cd7d802b` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 37.0 | 22 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-2624909d11d0cd7d802b` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 17.19000000037522 | 126.79 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-5f3be65a92c05a8b4eac` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 116.0 | 102 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-5f3be65a92c05a8b4eac` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 47.0 | 23 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-7107af89f2c09b95cdc8` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
