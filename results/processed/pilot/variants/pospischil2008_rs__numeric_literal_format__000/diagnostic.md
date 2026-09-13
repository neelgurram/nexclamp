# pospischil2008_rs__numeric_literal_format__000

- model: `pospischil2008_rs`
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "condDensity", "file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260913, "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "n_sites": 126, "new": "0.10 mS_per_cm2", "old": "0.1 mS_per_cm2", "site_index": 18, "style": "padded", "xsd_type": "Nml2Quantity_conductanceDensity"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.1 mS_per_cm2", "new": "0.10 mS_per_cm2", "action": "set", "note": "numerically identical literal (padded)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 545.505 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
