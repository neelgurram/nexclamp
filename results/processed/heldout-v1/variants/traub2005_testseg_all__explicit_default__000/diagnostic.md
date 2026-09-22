# traub2005_testseg_all__explicit_default__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: control
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "n_sites": 28, "site_index": 27, "value": "all", "xsd_type": "Resistivity"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/intracellularProperties[1]/resistivity[1]", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of Resistivity"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 2673.716 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
