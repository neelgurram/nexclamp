# pospischil2008_rs__reorder_independent__000

- model: `pospischil2008_rs`
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 2, "file": "NeuroML2/channels/Kd/Kd.channel.nml", "first": 1, "generator_seed": 20260913, "locator": "/neuroml", "n_sites": 13, "permutation": "reverse", "site_index": 9, "tag": "ComponentType"}`
- recorded edits: `[{"file": "NeuroML2/channels/Kd/Kd.channel.nml", "locator": "/neuroml", "attribute": null, "old": "Kd_n_alpha_rate,Kd_n_beta_rate", "new": "Kd_n_beta_rate,Kd_n_alpha_rate", "action": "text", "note": "reorder 2 consecutive <ComponentType> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 519.059 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
