# acnet2_pyr_soma__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "condDensity", "file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_pyr_soma_group']", "n_sites": 83, "new": "1200 S_per_m2", "old": "120.0 mS_per_cm2", "site_index": 69, "to_unit": "S_per_m2", "xsd_type": "Nml2Quantity_conductanceDensity"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_pyr_soma_group']", "attribute": "condDensity", "old": "120.0 mS_per_cm2", "new": "1200 S_per_m2", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_conductanceDensity)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 478.203 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
