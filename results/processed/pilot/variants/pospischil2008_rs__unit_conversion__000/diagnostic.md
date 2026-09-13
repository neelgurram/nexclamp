# pospischil2008_rs__unit_conversion__000

- model: `pospischil2008_rs`
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "value", "file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260913, "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "n_sites": 39, "new": "-0.07 V", "old": "-70.0 mV", "site_index": 15, "to_unit": "V", "xsd_type": "Nml2Quantity_voltage"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "attribute": "value", "old": "-70.0 mV", "new": "-0.07 V", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_voltage)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 297.621 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
