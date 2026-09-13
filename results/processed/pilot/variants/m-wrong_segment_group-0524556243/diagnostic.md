# m-wrong_segment_group-0524556243

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / wrong_segment_group
- parameters: `{"changes": [{"attribute": "segmentGroup", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "soma_group", "old": null}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260913, "new_group": "soma_group"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "segmentGroup", "old": null, "new": "soma_group", "action": "set", "note": "wrong_segment_group"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 613.75 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
