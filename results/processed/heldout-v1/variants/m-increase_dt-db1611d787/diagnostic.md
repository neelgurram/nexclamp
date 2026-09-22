# m-increase_dt-db1611d787

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "2E-3ms", "old": "5.0E-4ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/LEMS_Thalamocortical.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "5.0E-4ms", "new": "2E-3ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 7548.24 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | -6.372028923032289 | 3.30768 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-31a291134718c3775d21` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 71.33246612267223 | 73.25463675649888 | 1.92217 | 1.42665 | `r-96e71f2e3b8549494d50` | `r-31a291134718c3775d21` |
| h/1 | P05_long_step | ahp_depth | exceeds | -2.799466059340233 | -6.374155963839414 | 3.57469 | 1.17341 | `r-74af15e68cf19cbae102` | `r-52e1513024ff397cdfad` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 72.98996734843095 | 75.25086783716023 | 2.2609 | 1.4598 | `r-74af15e68cf19cbae102` | `r-52e1513024ff397cdfad` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -2.697613642280899 | -6.486715995699811 | 3.7891 | 1.32669 | `r-289063c903c8c366c952` | `r-f5c762dd122df5da6370` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 96.16110801631415 | None |  | 1.92322 | `r-289063c903c8c366c952` | `r-f5c762dd122df5da6370` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -2.68242419940799 | -3.9156844914748916 | 1.23326 | 1.14578 | `r-6290d36f97e6ddeb2b58` | `r-af0287078c9234cdc24d` |
| h/2 | P05_long_step | ahp_depth | exceeds | -2.408330571497629 | -3.689686047859311 | 1.28136 | 1.17341 | `r-f1a8b6a7a66c54d9b827` | `r-2767537945c8f851b878` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 86.0 | 4 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-2767537945c8f851b878` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -2.255384099392458 | -3.6910147575484444 | 1.43563 | 1.32669 | `r-5eb7b54961cd58341dac` | `r-0b03ef08bad6620f67d3` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 95.5725460033362 | None |  | 1.92322 | `r-5eb7b54961cd58341dac` | `r-0b03ef08bad6620f67d3` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
