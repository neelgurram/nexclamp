# traub2005_testseg_all__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "conductance", "file": "neuroConstruct/generatedNeuroML2/cal.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='cal']", "n_sites": 227, "new": "1e-11S", "old": "10pS", "site_index": 97, "to_unit": "S", "xsd_type": "Nml2Quantity_conductance"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/cal.channel.nml", "locator": "/neuroml/ionChannel[@id='cal']", "attribute": "conductance", "old": "10pS", "new": "1e-11S", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_conductance)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 2701.109 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
