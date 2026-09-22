# m-scale_gate_time_constant-31e82d8467

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "fixedQ10", "locator": "/neuroml[@id='kad']/ionChannel[@id='kad']/gate[@id='l']/q10Settings[1]", "new": "0.8", "old": "1"}], "channel": "kad", "factor": 0.8, "gate": "l", "generator_seed": 20260917, "mechanism": "q10_scale"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/kad.channel.nml", "locator": "/neuroml[@id='kad']/ionChannel[@id='kad']/gate[@id='l']/q10Settings[1]", "attribute": "fixedQ10", "old": "1", "new": "0.8", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 6118.647 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
