# m-shift_reversal-58a6710e4d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='napf_spinstell_all']", "new": "40.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "napf_spinstell_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='napf_spinstell_all']", "attribute": "erev", "old": "50.0 mV", "new": "40.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1548.264 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
