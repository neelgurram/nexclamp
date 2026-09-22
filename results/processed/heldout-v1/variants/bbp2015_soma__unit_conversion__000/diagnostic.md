# bbp2015_soma__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "tau", "file": "NMC/NeuroML2/KdShu2007.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='KdShu2007']/gate[@id='m']/timeCourse[1]", "n_sites": 234, "new": "0.0006s", "old": "0.6ms", "site_index": 92, "to_unit": "s", "xsd_type": "Nml2Quantity_time"}`
- recorded edits: `[{"file": "NMC/NeuroML2/KdShu2007.channel.nml", "locator": "/neuroml/ionChannel[@id='KdShu2007']/gate[@id='m']/timeCourse[1]", "attribute": "tau", "old": "0.6ms", "new": "0.0006s", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_time)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1698.144 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
