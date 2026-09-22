# m-scale_gate_time_constant-52af1c4a01

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "SK_E2", "factor": 2.0, "gate": "z", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SK_E2.channel.nml", "locator": "/neuroml[@id='SK_E2']/ionChannel[@id='SK_E2']/gate[@id='z']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1467.025 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
