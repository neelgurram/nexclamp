# hay2011_soma__add_comments__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: control
- kind/family/operator: no_change_control / formatting / add_comments
- parameters: `{"file": "neuroConstruct/generatedNeuroML2/L5bPyrCellHayEtAl2011.net.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 45, "position": "root_start", "site_index": 21}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/L5bPyrCellHayEtAl2011.net.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "1 comment(s)", "action": "insert", "note": "add_comments position=root_start"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1405.179 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
