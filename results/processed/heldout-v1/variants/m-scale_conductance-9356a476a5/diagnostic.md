# m-scale_conductance-9356a476a5

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='km_all']", "new": "1.65 mS_per_cm2", "old": "1.5 mS_per_cm2"}], "element": "channelDensity", "element_id": "km_all", "factor": 1.1, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='km_all']", "attribute": "condDensity", "old": "1.5 mS_per_cm2", "new": "1.65 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 7930.106 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.5216693418942094 | None |  | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-2dca9115421f4337d46b` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 7.719999999998464 | 15.98 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-2dca9115421f4337d46b` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-2dca9115421f4337d46b` |
| h/1 | P04_step_2x | spike_count | exceeds | 51.0 | 47.0 | 4 | 3 | `r-96e71f2e3b8549494d50` | `r-1f2652881fb271274fb2` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 26.190000000571672 | 1.72 | 1.11 | `r-74af15e68cf19cbae102` | `r-81d9e8a82da1f7678e59` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 78.0 | 5 | 3 | `r-74af15e68cf19cbae102` | `r-81d9e8a82da1f7678e59` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.5214881334190068 | None |  | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-c49a507faa1fbbb95289` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 7.719999999998464 | 16 | 0.5 | `r-87bcc3cd30685deaf603` | `r-c49a507faa1fbbb95289` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-87bcc3cd30685deaf603` | `r-c49a507faa1fbbb95289` |
| h/2 | P04_step_2x | spike_count | exceeds | 50.0 | 46.0 | 4 | 3 | `r-6290d36f97e6ddeb2b58` | `r-1438caca9cac8e4f6b51` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 26.60000000058062 | 1.76 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-c50e0725580124b3677a` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 77.0 | 5 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-c50e0725580124b3677a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
