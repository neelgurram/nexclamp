# hay2011_soma__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "amplitude", "file": "neuroConstruct/generatedNeuroML2/L5bPyrCellHayEtAl2011.net.nml", "generator_seed": 20260917, "locator": "/neuroml/pulseGenerator[@id='Input_4']", "n_sites": 178, "new": "50pA", "old": "5.0E-5uA", "site_index": 72, "to_unit": "pA", "xsd_type": "Nml2Quantity_current"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/L5bPyrCellHayEtAl2011.net.nml", "locator": "/neuroml/pulseGenerator[@id='Input_4']", "attribute": "amplitude", "old": "5.0E-5uA", "new": "50pA", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_current)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1686.204 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
