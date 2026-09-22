# bbp2015_soma__add_comments__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: control
- kind/family/operator: no_change_control / formatting / add_comments
- parameters: `{"file": "NMC/NeuroML2/Im.channel.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 54, "position": "before_root_end", "site_index": 17}`
- recorded edits: `[{"file": "NMC/NeuroML2/Im.channel.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "1 comment(s)", "action": "insert", "note": "add_comments position=before_root_end"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1701.781 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
