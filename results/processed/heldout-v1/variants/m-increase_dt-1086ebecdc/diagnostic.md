# m-increase_dt-1086ebecdc

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/LEMS_SomaTest.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 4244.191 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | -5.43348429870143 | -9.857047598513958 | 4.42356 | 1.14528 | `r-531ed8bf9e8ec22d7778` | `r-b802b6afee05fcd2508a` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 76.68460655583269 | 79.81501006754402 | 3.1304 | 1.89637 | `r-531ed8bf9e8ec22d7778` | `r-b802b6afee05fcd2508a` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.300969345084837 | -9.8301013971748 | 4.52913 | 1.15254 | `r-c181d8dc3f2e9e1a86cf` | `r-b7c4314662117788e8bc` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 77.26993942349823 | 80.348255157643 | 3.07832 | 1.98255 | `r-c181d8dc3f2e9e1a86cf` | `r-b7c4314662117788e8bc` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -11.637315512319745 | 3.14914 | 1.08676 | `r-f411679bd6f2a1231337` | `r-124b6807b6d36e9968cf` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 90.83680152686651 | None |  | 1.81674 | `r-f411679bd6f2a1231337` | `r-124b6807b6d36e9968cf` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -5.051723726911618 | -6.419106249471852 | 1.36738 | 1.14528 | `r-c4e93fb668595b0fb26c` | `r-f4bd187382e6295b1b4a` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 19.0 | 1 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-f4bd187382e6295b1b4a` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.916790255219169 | -6.3045333658653675 | 1.38774 | 1.15254 | `r-c41be102b8e8611b929c` | `r-4254824c006ae8f03b98` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -9.304373578344212 | 1.17845 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-93d23ba8256ca3e63fc7` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
