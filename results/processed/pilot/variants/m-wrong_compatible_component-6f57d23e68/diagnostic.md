# m-wrong_compatible_component-6f57d23e68

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "IM", "old": "Kd"}], "element_id": "Kd_all", "generator_seed": 20260913, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "ionChannel", "old": "Kd", "new": "IM", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 444.412 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
