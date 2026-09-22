# hay2011_soma__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 2, "file": "neuroConstruct/generatedNeuroML2/NaTa_t.channel.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='NaTa_t']", "n_sites": 18, "permutation": "reverse", "site_index": 11, "tag": "gate"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/NaTa_t.channel.nml", "locator": "/neuroml/ionChannel[@id='NaTa_t']", "attribute": null, "old": "m,h", "new": "h,m", "action": "text", "note": "reorder 2 consecutive <gate> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1398.341 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
