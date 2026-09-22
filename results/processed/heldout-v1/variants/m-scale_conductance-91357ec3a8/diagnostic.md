# m-scale_conductance-91357ec3a8

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "new": "0.064 mS_per_cm2", "old": "0.08 mS_per_cm2"}], "element": "channelDensity", "element_id": "SK_E2_all", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "attribute": "condDensity", "old": "0.08 mS_per_cm2", "new": "0.064 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4673.377 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 14.449999999986858 | 1.34 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-5ff182756ed7cd3b672a` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 20.689999999981183 | 15.96 | 0.733 | `r-49ced7acda977f37b12b` | `r-07f1415ae5ca9fcc5042` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 25.0 | 10 | 0.5 | `r-49ced7acda977f37b12b` | `r-07f1415ae5ca9fcc5042` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 133.26000000290878 | 9.71 | 3.03 | `r-b99907e8e6510bd22247` | `r-8f058171ac786ec8f550` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-8f058171ac786ec8f550` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 28.0 | 4 | 0.5 | `r-da1341cbf9665d4e7639` | `r-ebf71f0b7000bcf2e715` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 14.439999999986867 | 1.33 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-ba18c95fc6ba2b3010b6` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 20.629999999981237 | 15.93 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-3a08dee48cde33c66869` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 25.0 | 10 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-3a08dee48cde33c66869` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 134.2500000029304 | 9.73 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-c31840f29d6f7f38e5a8` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-c31840f29d6f7f38e5a8` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 28.0 | 4 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-125b127a3a8859c704d9` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
