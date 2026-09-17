# pospischil2008_rs__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 4, "file": "NeuroML2/cells/RS/LEMS_RS.xml", "first": 4, "generator_seed": 20260917, "locator": "/Lems", "n_sites": 13, "permutation": "reverse", "site_index": 0, "tag": "Include"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/LEMS_RS.xml", "locator": "/Lems", "attribute": null, "old": "../../channels/Kd/Kd.channel.nml,../../channels/IM/IM.channel.nml,../../channels/Leak/Leak.channel.nml,../../channels/Na/Na.channel.nml", "new": "../../channels/Na/Na.channel.nml,../../channels/Leak/Leak.channel.nml,../../channels/IM/IM.channel.nml,../../channels/Kd/Kd.channel.nml", "action": "text", "note": "reorder 4 consecutive <Include> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 412.88 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
