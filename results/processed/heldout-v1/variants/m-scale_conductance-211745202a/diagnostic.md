# m-scale_conductance-211745202a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']", "new": "1.0912 mS_per_cm2", "old": "0.992 mS_per_cm2"}], "element": "channelDensityNernst", "element_id": "Ca_HVA_all", "factor": 1.1, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']", "attribute": "condDensity", "old": "0.992 mS_per_cm2", "new": "1.0912 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 10777.708 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 148.30000000288578 | 5.33 | 3.03 | `r-b99907e8e6510bd22247` | `r-366bafc2c9bd474d5ba3` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-366bafc2c9bd474d5ba3` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 149.34000000316496 | 5.36 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-7aff52af6d554a0a23b3` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-7aff52af6d554a0a23b3` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
