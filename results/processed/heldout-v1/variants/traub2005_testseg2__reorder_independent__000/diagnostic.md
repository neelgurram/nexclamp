# traub2005_testseg2__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 14, "file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 26, "permutation": "reverse", "site_index": 4, "tag": "include"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml", "attribute": null, "old": "k2.channel.nml,ka.channel.nml,ka_ib.channel.nml,kdr.channel.nml,kdr_fs.channel.nml,km.channel.nml,naf.channel.nml,naf2.channel.nml,naf_tcr.channel.nml,nap.channel.nml,napf.channel.nml,napf_spinstell.channel.nml,napf_tcr.channel.nml,pas.channel.nml", "new": "pas.channel.nml,napf_tcr.channel.nml,napf_spinstell.channel.nml,napf.channel.nml,nap.channel.nml,naf_tcr.channel.nml,naf2.channel.nml,naf.channel.nml,km.channel.nml,kdr_fs.channel.nml,kdr.channel.nml,ka_ib.channel.nml,ka.channel.nml,k2.channel.nml", "action": "text", "note": "reorder 14 consecutive <include> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1537.278 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
