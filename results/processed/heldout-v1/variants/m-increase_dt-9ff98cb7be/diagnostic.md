# m-increase_dt-9ff98cb7be

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004 ms", "old": "0.001 ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/LEMS_singleCompAllChans.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001 ms", "new": "0.004 ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 2192.279 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | -12.946651097611621 | 134.4641600018608 | 147.411 | 0.647333 | `r-d2cafd1fc897dbfd8130` | `r-50d0636dd5bd16e9d578` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | 123.24873889333371 | 136.97 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-0cc45cec00e9cb3f994f` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 134.16434859879257 | None |  | 2.68329 | `r-83f9184aaeefc65499cb` | `r-0cc45cec00e9cb3f994f` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 133.76337051196737 | None |  | 2.68329 | `r-dc583bb05cf4bf59d02c` | `r-1a321840c45f7404e51c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
