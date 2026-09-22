# m-scale_conductance-2956a62118

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "new": "3.087 mS_per_cm2", "old": "3.43 mS_per_cm2"}], "element": "channelDensityNernst", "element_id": "Ca_LVAst_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "attribute": "condDensity", "old": "3.43 mS_per_cm2", "new": "3.087 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 11953.381 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-5802429264cf80aefa9e` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-a1a90cfa3b6cff5a7b78` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
