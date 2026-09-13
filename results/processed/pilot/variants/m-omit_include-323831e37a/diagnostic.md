# m-omit_include-323831e37a

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / omit_include
- parameters: `{"generator_seed": 20260913, "href": "../../channels/Na/Na.channel.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Na/Na.channel.nml\"/>"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/include[4]", "attribute": null, "old": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"../../channels/Na/Na.channel.nml\"/>", "new": null, "action": "remove", "note": "omit_include"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 48.259 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
