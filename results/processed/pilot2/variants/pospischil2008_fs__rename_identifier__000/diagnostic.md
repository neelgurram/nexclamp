# pospischil2008_fs__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "NeuroML2/cells/FS/FS.net.nml", "generator_seed": 20260917, "kind": "network", "locator": "/neuroml/network[@id='network_PospischilEtAl2008']", "n_sites": 19, "new": "network_PospischilEtAl2008_renamed", "old": "network_PospischilEtAl2008", "site_index": 9}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.net.nml", "locator": "/neuroml/network[@id='network_PospischilEtAl2008']", "attribute": "id", "old": "network_PospischilEtAl2008", "new": "network_PospischilEtAl2008_renamed", "action": "set", "note": "rename network network_PospischilEtAl2008 -> network_PospischilEtAl2008_renamed (locators refer to the pre-edit file)"}, {"file": "NeuroML2/cells/FS/LEMS_FS.xml", "locator": "/Lems/Component[@id='sim1']", "attribute": "target", "old": "network_PospischilEtAl2008", "new": "network_PospischilEtAl2008_renamed", "action": "set", "note": "rename network network_PospischilEtAl2008 -> network_PospischilEtAl2008_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 355.465 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
