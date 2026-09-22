# bbp2015_soma__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "NMC/NeuroML2/Ca_LVAst.channel.nml", "generator_seed": 20260917, "kind": "gate", "locator": "/neuroml/ionChannel[@id='Ca_LVAst']/gate[@id='h']", "n_sites": 59, "new": "h_renamed", "old": "h", "site_index": 9}`
- recorded edits: `[{"file": "NMC/NeuroML2/Ca_LVAst.channel.nml", "locator": "/neuroml/ionChannel[@id='Ca_LVAst']/gate[@id='h']", "attribute": "id", "old": "h", "new": "h_renamed", "action": "set", "note": "rename gate h -> h_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1772.077 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
