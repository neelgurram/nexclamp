# m-increase_dt-3ec3095c52

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.004ms", "old": "0.001ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/LEMS_CA1PyramidalCell.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.001ms", "new": "0.004ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 2957.715 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | 113.80796156145718 | 128.584 | 0.738788 | `r-0925b86f96a976919154` | `r-56a90ab481ea2549f5d7` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | 113.82708628287568 | 128.9 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-031dd55f520bb8769020` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -17.36525204849154 | 1.36409 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-1577dd969da3378b2b1d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
