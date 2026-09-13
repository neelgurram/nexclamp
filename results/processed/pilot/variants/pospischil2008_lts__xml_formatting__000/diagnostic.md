# pospischil2008_lts__xml_formatting__000

- model: `pospischil2008_lts`
- kind/family/operator: no_change_control / formatting / xml_formatting
- parameters: `{"file": "NeuroML2/channels/Ca/Ca.nml", "generator_seed": 20260913, "locator": "/neuroml", "n_sites": 18, "site_index": 7, "style": "attribute_order"}`
- recorded edits: `[{"file": "NeuroML2/channels/Ca/Ca.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": null, "action": "text", "note": "xml_formatting style=attribute_order (whitespace/attribute order only)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 657.169 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
