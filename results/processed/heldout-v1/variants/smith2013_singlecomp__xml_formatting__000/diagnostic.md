# smith2013_singlecomp__xml_formatting__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: control
- kind/family/operator: no_change_control / formatting / xml_formatting
- parameters: `{"file": "NeuroML2/kca.channel.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 20, "site_index": 7, "style": "attribute_order"}`
- recorded edits: `[{"file": "NeuroML2/kca.channel.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": null, "action": "text", "note": "xml_formatting style=attribute_order (whitespace/attribute order only)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 761.968 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
