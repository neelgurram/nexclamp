# acnet2_pyr_soma__explicit_default__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: control
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "n_sites": 6, "site_index": 5, "value": "all", "xsd_type": "Resistivity"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of Resistivity"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 515.899 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
