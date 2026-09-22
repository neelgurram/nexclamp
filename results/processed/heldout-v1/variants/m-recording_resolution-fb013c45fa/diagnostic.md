# m-recording_resolution-fb013c45fa

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260917, "sample_every_ms": 0.05}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.05}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 10219.581 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 126.03113174260383 | 121.96924209524559 | 4.06189 | 2.52062 | `r-ad42eb643e1748725abb` | `r-68d701ef6ab50ed7dc2b` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 90.22942352330233 | 87.8749389505925 | 2.35448 | 1.81565 | `r-ebfd6e5f8d6b9e916dfe` | `r-c2ef215038bb19362778` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
