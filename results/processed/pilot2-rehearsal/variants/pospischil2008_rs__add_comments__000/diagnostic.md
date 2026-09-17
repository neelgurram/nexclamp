# pospischil2008_rs__add_comments__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: control
- kind/family/operator: no_change_control / formatting / add_comments
- parameters: `{"file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 21, "position": "before_each_child", "site_index": 4}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "5 comment(s)", "action": "insert", "note": "add_comments position=before_each_child"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 440.73 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
