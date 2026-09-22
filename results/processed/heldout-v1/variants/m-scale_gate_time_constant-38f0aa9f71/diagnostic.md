# m-scale_gate_time_constant-38f0aa9f71

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "napf", "factor": 0.5, "gate": "m", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/napf.channel.nml", "locator": "/neuroml[@id='napf']/ionChannel[@id='napf']/gate[@id='m']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"0.5\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8090.952 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.5216693418942094 | 0.4297707458832944 | 0.0918986 | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-b366ab5450c56e28be21` |
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -5.322500542028692 | 2.92591 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-b366ab5450c56e28be21` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 74.70865440368996 | 68.73390388489332 | 5.97475 | 1.49417 | `r-068a1eafd4afbbd6d23e` | `r-b366ab5450c56e28be21` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 22.140000000005465 | 1.56 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-b366ab5450c56e28be21` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | 1.6244473673464341 | 4.6888 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-deaebd16ea8af2bb49ac` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 71.33246612267223 | 66.03326797629298 | 5.2992 | 1.42665 | `r-96e71f2e3b8549494d50` | `r-deaebd16ea8af2bb49ac` |
| h/1 | P04_step_2x | spike_count | exceeds | 51.0 | 45.0 | 6 | 3 | `r-96e71f2e3b8549494d50` | `r-deaebd16ea8af2bb49ac` |
| h/1 | P05_long_step | ahp_depth | exceeds | -2.799466059340233 | 2.116901896173033 | 4.91637 | 1.17341 | `r-74af15e68cf19cbae102` | `r-0f778d41fabbd0f52db2` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 72.98996734843095 | 67.82105636667586 | 5.16891 | 1.4598 | `r-74af15e68cf19cbae102` | `r-0f778d41fabbd0f52db2` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 26.040000000568398 | 1.57 | 1.11 | `r-74af15e68cf19cbae102` | `r-0f778d41fabbd0f52db2` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 78.0 | 5 | 3 | `r-74af15e68cf19cbae102` | `r-0f778d41fabbd0f52db2` |
| h/1 | P06_ramp | spike_count | exceeds | 70.0 | 61.0 | 9 | 3 | `r-6afcc4c87334b55f282e` | `r-6500586beb1e2c000a22` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -2.697613642280899 | 0.5429959513706848 | 3.24061 | 1.32669 | `r-289063c903c8c366c952` | `r-7662f559770f5698431e` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 96.16110801631415 | 91.14291381709126 | 5.01819 | 1.92322 | `r-289063c903c8c366c952` | `r-7662f559770f5698431e` |
| h/1 | P09_short_pulse | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-289063c903c8c366c952` | `r-7662f559770f5698431e` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.5214881334190068 | 0.43004513217297363 | 0.091443 | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-5cac884001eb79e602ab` |
| h/2 | P00_canonical | ahp_depth | exceeds | -8.213585962703469 | -5.30887260247227 | 2.90471 | 0.5 | `r-87bcc3cd30685deaf603` | `r-5cac884001eb79e602ab` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 74.66815185545984 | 68.82012557982928 | 5.84803 | 1.49417 | `r-87bcc3cd30685deaf603` | `r-5cac884001eb79e602ab` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 22.180000000005485 | 1.54 | 0.5 | `r-87bcc3cd30685deaf603` | `r-5cac884001eb79e602ab` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -2.68242419940799 | 1.7465851669488046 | 4.42901 | 1.14578 | `r-6290d36f97e6ddeb2b58` | `r-cb783621eeea7336c997` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 71.00378608656828 | 65.75673675514271 | 5.24705 | 1.42665 | `r-6290d36f97e6ddeb2b58` | `r-cb783621eeea7336c997` |
| h/2 | P04_step_2x | spike_count | exceeds | 50.0 | 44.0 | 6 | 3 | `r-6290d36f97e6ddeb2b58` | `r-cb783621eeea7336c997` |
| h/2 | P05_long_step | ahp_depth | exceeds | -2.408330571497629 | 2.23357704925796 | 4.64191 | 1.17341 | `r-f1a8b6a7a66c54d9b827` | `r-62c8088424e092aafa2c` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 72.5536842363497 | 67.47036552261777 | 5.08332 | 1.4598 | `r-f1a8b6a7a66c54d9b827` | `r-62c8088424e092aafa2c` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 26.44000000057713 | 1.6 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-62c8088424e092aafa2c` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 77.0 | 5 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-62c8088424e092aafa2c` |
| h/2 | P06_ramp | spike_count | exceeds | 69.0 | 61.0 | 8 | 3 | `r-ce6273bb85e534e50ecc` | `r-21f8f18e5983bb809e1b` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -2.255384099392458 | 0.7360794907464197 | 2.99146 | 1.32669 | `r-5eb7b54961cd58341dac` | `r-fe06efa83905d98573bd` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 95.5725460033362 | 90.63871764860632 | 4.93383 | 1.92322 | `r-5eb7b54961cd58341dac` | `r-fe06efa83905d98573bd` |
| h/2 | P09_short_pulse | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-5eb7b54961cd58341dac` | `r-fe06efa83905d98573bd` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
