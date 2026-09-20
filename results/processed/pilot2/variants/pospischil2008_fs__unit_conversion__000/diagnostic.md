# pospischil2008_fs__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "value", "file": "NeuroML2/cells/FS/FS.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='FS']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "n_sites": 35, "new": "0.1 kohm_cm", "old": "100 ohm_cm", "site_index": 12, "to_unit": "kohm_cm", "xsd_type": "Nml2Quantity_resistivity"}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml/cell[@id='FS']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "attribute": "value", "old": "100 ohm_cm", "new": "0.1 kohm_cm", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_resistivity)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 407.975 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
