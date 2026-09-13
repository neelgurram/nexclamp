# m-omit_include-7207b139f8

- model: `pospischil2008_lts`
- kind/family/operator: mutant / reference / omit_include
- parameters: `{"generator_seed": 20260913, "href": "../../channels/Ca/Ca.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Ca/Ca.nml\"/>"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml[@id='LTS']/include[6]", "attribute": null, "old": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Ca/Ca.nml\"/>", "new": null, "action": "remove", "note": "omit_include"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 63.738 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
