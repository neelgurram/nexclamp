# pospischil2008_lts__numeric_literal_format__000

- model: `pospischil2008_lts`
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "value", "file": "NeuroML2/cells/LTS/LTS.cell.nml", "generator_seed": 20260913, "locator": "/neuroml/cell[@id='LTS']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "n_sites": 153, "new": "100.0 ohm_cm", "old": "100 ohm_cm", "site_index": 65, "style": "padded", "xsd_type": "Nml2Quantity_resistivity"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml/cell[@id='LTS']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "attribute": "value", "old": "100 ohm_cm", "new": "100.0 ohm_cm", "action": "set", "note": "numerically identical literal (padded)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 671.752 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
