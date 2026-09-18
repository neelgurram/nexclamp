# acnet2_pyr_soma__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 6, "file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 8, "permutation": "rotate", "site_index": 5, "tag": "include"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml", "attribute": null, "old": "Ca_conc.nml,Ca_pyr.channel.nml,Kahp_pyr.channel.nml,Kdr_pyr.channel.nml,LeakConductance_pyr.channel.nml,Na_pyr.channel.nml", "new": "Ca_pyr.channel.nml,Kahp_pyr.channel.nml,Kdr_pyr.channel.nml,LeakConductance_pyr.channel.nml,Na_pyr.channel.nml,Ca_conc.nml", "action": "text", "note": "reorder 6 consecutive <include> siblings (rotate)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 459.654 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
