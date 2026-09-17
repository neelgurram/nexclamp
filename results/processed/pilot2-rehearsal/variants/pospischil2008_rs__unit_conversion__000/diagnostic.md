# pospischil2008_rs__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "condDensity", "file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "n_sites": 39, "new": "0.0001 S_per_cm2", "old": "0.1 mS_per_cm2", "site_index": 1, "to_unit": "S_per_cm2", "xsd_type": "Nml2Quantity_conductanceDensity"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.1 mS_per_cm2", "new": "0.0001 S_per_cm2", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_conductanceDensity)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 428.677 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
