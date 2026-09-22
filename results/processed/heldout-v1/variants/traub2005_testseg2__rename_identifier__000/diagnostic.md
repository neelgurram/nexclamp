# traub2005_testseg2__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "neuroConstruct/generatedNeuroML2/Test.net.nml", "generator_seed": 20260917, "kind": "network", "locator": "/neuroml/network[@id='network_Thalamocortical']", "n_sites": 55, "new": "network_Thalamocortical_renamed", "old": "network_Thalamocortical", "site_index": 1}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/LEMS_SomaTest.xml", "locator": "/Lems/Component[@id='sim1']", "attribute": "target", "old": "network_Thalamocortical", "new": "network_Thalamocortical_renamed", "action": "set", "note": "rename network network_Thalamocortical -> network_Thalamocortical_renamed (locators refer to the pre-edit file)"}, {"file": "neuroConstruct/generatedNeuroML2/Test.net.nml", "locator": "/neuroml/network[@id='network_Thalamocortical']", "attribute": "id", "old": "network_Thalamocortical", "new": "network_Thalamocortical_renamed", "action": "set", "note": "rename network network_Thalamocortical -> network_Thalamocortical_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1558.383 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
