# bbp2015_soma__explicit_default__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: control
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']", "n_sites": 18, "site_index": 12, "value": "all", "xsd_type": "ChannelDensityNernst"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_HVA_all']", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of ChannelDensityNernst"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1756.968 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
