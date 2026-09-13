# pospischil2008_lts__reorder_independent__000

- model: `pospischil2008_lts`
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 4, "file": "NeuroML2/channels/IT/IT.channel.nml", "first": 1, "generator_seed": 20260913, "locator": "/neuroml", "n_sites": 14, "permutation": "reverse", "site_index": 7, "tag": "ComponentType"}`
- recorded edits: `[{"file": "NeuroML2/channels/IT/IT.channel.nml", "locator": "/neuroml", "attribute": null, "old": "IT_s_gate,IT_s_inf_inf,IT_u_tau_tau,IT_u_inf_inf", "new": "IT_u_inf_inf,IT_u_tau_tau,IT_s_inf_inf,IT_s_gate", "action": "text", "note": "reorder 4 consecutive <ComponentType> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 541.902 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
