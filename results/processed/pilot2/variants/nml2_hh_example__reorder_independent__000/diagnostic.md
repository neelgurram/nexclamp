# nml2_hh_example__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 3, "file": "examples/NML2_SingleCompHHCell.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 5, "permutation": "reverse", "site_index": 0, "tag": "ionChannelHH"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml", "attribute": null, "old": "passiveChan,naChan,kChan", "new": "kChan,naChan,passiveChan", "action": "text", "note": "reorder 3 consecutive <ionChannelHH> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 208.178 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
