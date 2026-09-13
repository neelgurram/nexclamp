# m-shift_initial_voltage-fa992f061c

- model: `pospischil2008_rs`
- kind/family/operator: mutant / biophysical / shift_initial_voltage
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "new": "-75.0 mV", "old": "-70.0 mV"}], "element": "initMembPotential", "element_id": null, "generator_seed": 20260913, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "attribute": "value", "old": "-70.0 mV", "new": "-75.0 mV", "action": "set", "note": "shift_initial_voltage"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 630.416 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
