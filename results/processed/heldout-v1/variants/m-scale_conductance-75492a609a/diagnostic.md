# m-scale_conductance-75492a609a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']", "new": "0.03375 mS_per_cm2", "old": "0.0675 mS_per_cm2"}], "element": "channelDensity", "element_id": "Im_all", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Im_all']", "attribute": "condDensity", "old": "0.0675 mS_per_cm2", "new": "0.03375 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 10866.323 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
