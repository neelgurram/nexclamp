# m-wrong_segment_group-01dc7ba1d7

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / wrong_segment_group
- parameters: `{"changes": [{"attribute": "segmentGroup", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "new": "Soma", "old": null}], "element": "channelDensity", "element_id": "IM_all", "generator_seed": 20260913, "new_group": "Soma"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all']", "attribute": "segmentGroup", "old": null, "new": "Soma", "action": "set", "note": "wrong_segment_group"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 595.407 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
