# m-increase_dt-2391bb7a93

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/LEMS_FS.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 1406.803 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -5.420849756874816 | 0.588544 | 0.5 | `r-4cceac4cec0eb866659f` | `r-fbe9a349d90bb056b4bc` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -7.746064327219727 | 3.13316 | 1.51774 | `r-54e05e4e4388308e9268` | `r-0bc143b1d915402a39ef` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 11.119999999989886 | 0.58 | 0.5 | `r-54e05e4e4388308e9268` | `r-0bc143b1d915402a39ef` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -8.401469097076074 | 3.07733 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-9be687f5262174060bce` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 16.300000000355794 | 0.69 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-9be687f5262174060bce` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 122.0 | 6 | 3 | `r-d95212df9ca6b2b4efff` | `r-9be687f5262174060bce` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 57.0 | 4 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-5da6357040f183df548c` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | -0.07298063276228106 | 3.5468 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-85934e64d8708b5f04f4` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 118.24569702145673 | None |  | 2.36491 | `r-534f36c941e5711ea7a5` | `r-85934e64d8708b5f04f4` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | -5.639048624666742 | 1.53205 | 1.51774 | `r-e087238cb438e653e31d` | `r-3c690e2ddc983c97ed5e` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -6.331968579582849 | 1.50473 | 1.49068 | `r-880359fc85650f897997` | `r-b946ee175f2f2b3dadc5` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 59.0 | 2 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-847a791ea26aec45eb00` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | 2.316239123138928 | 1.7261 | 1.70556 | `r-84e85309a66928a29934` | `r-c06db54116f8e371e764` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 118.07249069170416 | None |  | 2.36491 | `r-84e85309a66928a29934` | `r-c06db54116f8e371e764` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
