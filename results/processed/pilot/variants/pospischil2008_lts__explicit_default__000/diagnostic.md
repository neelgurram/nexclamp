# pospischil2008_lts__explicit_default__000

- model: `pospischil2008_lts`
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "NeuroML2/cells/LTS/LTS.cell.nml", "generator_seed": 20260913, "locator": "/neuroml/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "n_sites": 10, "site_index": 1, "value": "all", "xsd_type": "ChannelDensity"}`
- recorded edits: `[{"file": "NeuroML2/cells/LTS/LTS.cell.nml", "locator": "/neuroml/cell[@id='LTS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of ChannelDensity"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 501.884 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
