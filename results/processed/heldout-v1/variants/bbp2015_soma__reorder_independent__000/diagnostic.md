# bbp2015_soma__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 14, "file": "NMC/NeuroML2/Soma_AllNML2.net.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 26, "permutation": "reverse", "site_index": 22, "tag": "include"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.net.nml", "locator": "/neuroml", "attribute": null, "old": "Ca.channel.nml,Ca_LVAst.channel.nml,CaDynamics_E2_NML2.nml,Ih.channel.nml,Im.channel.nml,K_Pst.channel.nml,K_Tst.channel.nml,KdShu2007.channel.nml,Nap_Et2.channel.nml,NaTa_t.channel.nml,pas.channel.nml,SK_E2.channel.nml,SKv3_1.channel.nml,Soma_AllNML2.cell.nml", "new": "Soma_AllNML2.cell.nml,SKv3_1.channel.nml,SK_E2.channel.nml,pas.channel.nml,NaTa_t.channel.nml,Nap_Et2.channel.nml,KdShu2007.channel.nml,K_Tst.channel.nml,K_Pst.channel.nml,Im.channel.nml,Ih.channel.nml,CaDynamics_E2_NML2.nml,Ca_LVAst.channel.nml,Ca.channel.nml", "action": "text", "note": "reorder 14 consecutive <include> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1796.205 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
