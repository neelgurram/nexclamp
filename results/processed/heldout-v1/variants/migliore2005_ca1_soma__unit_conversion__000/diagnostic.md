# migliore2005_ca1_soma__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "erev", "file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "n_sites": 95, "new": "-0.03 V", "old": "-30.0 mV", "site_index": 7, "to_unit": "V", "xsd_type": "Nml2Quantity_voltage"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='hd_all']", "attribute": "erev", "old": "-30.0 mV", "new": "-0.03 V", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_voltage)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 997.789 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
