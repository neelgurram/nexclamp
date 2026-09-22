# hay2011_soma__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "neuroConstruct/generatedNeuroML2/NaTa_t.channel.nml", "generator_seed": 20260917, "kind": "gate", "locator": "/neuroml/ionChannel[@id='NaTa_t']/gate[@id='m']", "n_sites": 48, "new": "m_renamed", "old": "m", "site_index": 22}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/NaTa_t.channel.nml", "locator": "/neuroml/ionChannel[@id='NaTa_t']/gate[@id='m']", "attribute": "id", "old": "m", "new": "m_renamed", "action": "set", "note": "rename gate m -> m_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1394.973 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
