# pospischil2008_rs__explicit_default__000

- model: `pospischil2008_rs`
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260913, "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "n_sites": 8, "site_index": 5, "value": "all", "xsd_type": "SpecificCapacitance"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of SpecificCapacitance"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 525.781 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
