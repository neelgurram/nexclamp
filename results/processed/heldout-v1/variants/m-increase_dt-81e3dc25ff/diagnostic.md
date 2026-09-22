# m-increase_dt-81e3dc25ff

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.01ms", "old": "0.0025ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/LEMS_L5bPyrCellHayEtAl2011_LowDt.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.0025ms", "new": "0.01ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 4708.866 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 90.78240967397937 | 94.13262174829055 | 3.35021 | 1.81565 | `r-a22266676a5c9c51fe6b` | `r-61c2e6ce2c952f5ae4e7` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | 61.9661014074081 | 61.0921 | 0.5 | `r-49ced7acda977f37b12b` | `r-945415988cdd3fbdb74b` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.04202652392433 | 95.32083890364632 | 6.27881 | 3.5976 | `r-49ced7acda977f37b12b` | `r-945415988cdd3fbdb74b` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 37.939999999965494 | 1.29 | 0.733 | `r-49ced7acda977f37b12b` | `r-945415988cdd3fbdb74b` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 14.0 | 1 | 0.5 | `r-49ced7acda977f37b12b` | `r-945415988cdd3fbdb74b` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -0.8050923194816306 | 1.26564 | 0.5 | `r-b99907e8e6510bd22247` | `r-7afbaa21d1a293ed1ba2` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 85.6294059753018 | 92.10211179483636 | 6.47271 | 3.92393 | `r-b99907e8e6510bd22247` | `r-7afbaa21d1a293ed1ba2` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 130.96000000285858 | 12.01 | 3.03 | `r-b99907e8e6510bd22247` | `r-7afbaa21d1a293ed1ba2` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-7afbaa21d1a293ed1ba2` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 126.03113174260383 | None |  | 2.52062 | `r-ad42eb643e1748725abb` | `r-95e0d8514ca5bf6bb32c` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 87.8428268328099 | 91.49146270469772 | 3.64864 | 3.5976 | `r-1e40b84a0cfdecc32574` | `r-783a851e4813b0a2abe2` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 140.18000000305983 | 3.8 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-0783341c6cef84f00511` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 125.19136047490628 | None |  | 2.52062 | `r-12a8ce0ecdd4bde4c832` | `r-6488a7841be4a27bfa90` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
