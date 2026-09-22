# traub2005_testseg2__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "scale", "file": "neuroConstruct/generatedNeuroML2/nap.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='nap']/gate[@id='m']/steadyState[1]", "n_sites": 455, "new": "10 mV", "old": "10mV", "site_index": 381, "style": "unit_spacing", "xsd_type": "Nml2Quantity_voltage"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/nap.channel.nml", "locator": "/neuroml/ionChannel[@id='nap']/gate[@id='m']/steadyState[1]", "attribute": "scale", "old": "10mV", "new": "10 mV", "action": "set", "note": "numerically identical literal (unit_spacing)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1572.933 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
