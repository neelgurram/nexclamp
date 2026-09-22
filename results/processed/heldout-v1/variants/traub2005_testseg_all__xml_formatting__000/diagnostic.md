# traub2005_testseg_all__xml_formatting__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: control
- kind/family/operator: no_change_control / formatting / xml_formatting
- parameters: `{"file": "neuroConstruct/generatedNeuroML2/cad__beta0_03__phi300000.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 58, "site_index": 13, "style": "attribute_order"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/cad__beta0_03__phi300000.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": null, "action": "text", "note": "xml_formatting style=attribute_order (whitespace/attribute order only)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 2695.586 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
