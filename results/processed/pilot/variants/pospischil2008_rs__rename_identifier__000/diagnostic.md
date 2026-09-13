# pospischil2008_rs__rename_identifier__000

- model: `pospischil2008_rs`
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260913, "kind": "channelDensity", "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "n_sites": 20, "new": "Kd_all_renamed", "old": "Kd_all", "site_index": 6}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/LEMS_RS.xml", "locator": "/Lems/Component[@id='sim1']/Display[@id='rates']/Line[@id='Kd n']", "attribute": "quantity", "old": "CG_RS/0/RS/biophys/membraneProperties/Kd_all/Kd/n/q", "new": "CG_RS/0/RS/biophys/membraneProperties/Kd_all_renamed/Kd/n/q", "action": "set", "note": "rename channelDensity Kd_all -> Kd_all_renamed (locators refer to the pre-edit file)"}, {"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "id", "old": "Kd_all", "new": "Kd_all_renamed", "action": "set", "note": "rename channelDensity Kd_all -> Kd_all_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 502.426 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
