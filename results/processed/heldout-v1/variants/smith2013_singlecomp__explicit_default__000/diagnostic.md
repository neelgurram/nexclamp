# smith2013_singlecomp__explicit_default__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: control
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "NeuroML2/singleCompAllChans.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "n_sites": 10, "site_index": 9, "value": "all", "xsd_type": "InitMembPotential"}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/initMembPotential[1]", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of InitMembPotential"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 749.467 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
