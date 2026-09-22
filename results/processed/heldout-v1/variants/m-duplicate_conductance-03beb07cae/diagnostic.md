# m-duplicate_conductance-03beb07cae

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "naf2_all_dup", "source_id": "naf2_all"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='naf2_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"0.033 mS_per_cm2\" id=\"naf2_all_dup\" ionChannel=\"naf2\" ion=\"na\" erev=\"50.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1692.758 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
