# traub2005_testseg_all__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "generator_seed": 20260917, "kind": "channelDensity", "locator": "/neuroml/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kc_fast_all']", "n_sites": 87, "new": "kc_fast_all_renamed", "old": "kc_fast_all", "site_index": 16}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kc_fast_all']", "attribute": "id", "old": "kc_fast_all", "new": "kc_fast_all_renamed", "action": "set", "note": "rename channelDensity kc_fast_all -> kc_fast_all_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 2680.757 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
