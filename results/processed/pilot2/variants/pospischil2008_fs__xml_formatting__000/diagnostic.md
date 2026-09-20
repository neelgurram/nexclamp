# pospischil2008_fs__xml_formatting__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: control
- kind/family/operator: no_change_control / formatting / xml_formatting
- parameters: `{"file": "NeuroML2/cells/FS/FS.cell.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 14, "site_index": 1, "style": "attribute_order"}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": null, "action": "text", "note": "xml_formatting style=attribute_order (whitespace/attribute order only)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 402.984 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
