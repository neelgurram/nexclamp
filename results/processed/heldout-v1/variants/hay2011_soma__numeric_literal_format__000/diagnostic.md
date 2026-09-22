# hay2011_soma__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "delay", "file": "neuroConstruct/generatedNeuroML2/L5bPyrCellHayEtAl2011.net.nml", "generator_seed": 20260917, "locator": "/neuroml/pulseGenerator[@id='Input_3']", "n_sites": 420, "new": "100.00ms", "old": "100.0ms", "site_index": 176, "style": "padded", "xsd_type": "Nml2Quantity_time"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/L5bPyrCellHayEtAl2011.net.nml", "locator": "/neuroml/pulseGenerator[@id='Input_3']", "attribute": "delay", "old": "100.0ms", "new": "100.00ms", "action": "set", "note": "numerically identical literal (padded)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1393.474 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
