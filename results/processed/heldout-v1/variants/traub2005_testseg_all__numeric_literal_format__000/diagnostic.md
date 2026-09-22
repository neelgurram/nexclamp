# traub2005_testseg_all__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "midpoint", "file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "n_sites": 692, "new": "-4.3e1mV", "old": "-43mV", "site_index": 500, "style": "scientific", "xsd_type": "Nml2Quantity_voltage"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/km.channel.nml", "locator": "/neuroml/ionChannel[@id='km']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-43mV", "new": "-4.3e1mV", "action": "set", "note": "numerically identical literal (scientific)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 2660.245 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
