# pospischil2008_lts__unit_conversion__000

- model: `pospischil2008_lts`
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "conductance", "file": "NeuroML2/channels/Kd/Kd.channel.nml", "generator_seed": 20260913, "locator": "/neuroml/ionChannel[@id='Kd']", "n_sites": 51, "new": "1e-11S", "old": "10pS", "site_index": 39, "to_unit": "S", "xsd_type": "Nml2Quantity_conductance"}`
- recorded edits: `[{"file": "NeuroML2/channels/Kd/Kd.channel.nml", "locator": "/neuroml/ionChannel[@id='Kd']", "attribute": "conductance", "old": "10pS", "new": "1e-11S", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_conductance)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 706.602 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
