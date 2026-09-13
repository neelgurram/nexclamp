# pospischil2008_lts__rename_identifier__000

- model: `pospischil2008_lts`
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "generator_seed": 20260913, "kind": "segmentGroup", "locator": "/neuroml/cell[@id='LTS']/morphology[@id='morphology_LTS']/segmentGroup[@id='soma_group']", "n_sites": 25, "new": "soma_group_renamed", "old": "soma_group", "site_index": 3}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml/cell[@id='LTS']/morphology[@id='morphology_LTS']/segmentGroup[@id='soma_group']", "attribute": "id", "old": "soma_group", "new": "soma_group_renamed", "action": "set", "note": "rename segmentGroup soma_group -> soma_group_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 654.87 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
