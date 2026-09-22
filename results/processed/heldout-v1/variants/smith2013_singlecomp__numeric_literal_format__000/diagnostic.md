# smith2013_singlecomp__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "conductance", "file": "NeuroML2/kca.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='kca']", "n_sites": 322, "new": "10 pS", "old": "10pS", "site_index": 98, "style": "unit_spacing", "xsd_type": "Nml2Quantity_conductance"}`
- recorded edits: `[{"file": "NeuroML2/kca.channel.nml", "locator": "/neuroml/ionChannel[@id='kca']", "attribute": "conductance", "old": "10pS", "new": "10 pS", "action": "set", "note": "numerically identical literal (unit_spacing)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 774.325 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
