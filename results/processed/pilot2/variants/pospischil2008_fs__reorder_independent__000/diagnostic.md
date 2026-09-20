# pospischil2008_fs__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 4, "file": "NeuroML2/channels/Na/Na.channel.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 13, "permutation": "reverse", "site_index": 10, "tag": "ComponentType"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml", "attribute": null, "old": "Na_m_alpha_rate,Na_m_beta_rate,Na_h_alpha_rate,Na_h_beta_rate", "new": "Na_h_beta_rate,Na_h_alpha_rate,Na_m_beta_rate,Na_m_alpha_rate", "action": "text", "note": "reorder 4 consecutive <ComponentType> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 268.906 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
