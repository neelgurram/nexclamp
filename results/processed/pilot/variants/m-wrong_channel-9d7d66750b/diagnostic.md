# m-wrong_channel-9d7d66750b

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "Kd", "old": "LeakConductance"}], "element_id": "LeakConductance_all", "generator_seed": 20260913, "new_species": "k", "old_species": "non_specific"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "ionChannel", "old": "LeakConductance", "new": "Kd", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **3_numerically_unstable**
- nominal-level status: numerically_unstable; runtime 493.619 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
