# m-shift_reversal-218fcb2b5b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kahp_slower_all']", "new": "-93.0 mV", "old": "-95.0 mV"}], "element": "channelDensity", "element_id": "kahp_slower_all", "generator_seed": 20260917, "shift_mV": 2.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kahp_slower_all']", "attribute": "erev", "old": "-95.0 mV", "new": "-93.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 7991.491 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 23.200000000004593 | 0.5 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-e837774c9cc8ca1d2746` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 23.220000000004603 | 0.5 | 0.5 | `r-87bcc3cd30685deaf603` | `r-cebdc37457095800c495` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
