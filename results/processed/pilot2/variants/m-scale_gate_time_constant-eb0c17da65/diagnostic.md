# m-scale_gate_time_constant-eb0c17da65

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/forwardRate[1]", "new": "6.4e1per_s", "old": "1.28e2per_s"}, {"attribute": "rate", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/reverseRate[1]", "new": "2e3per_s", "old": "4e3per_s"}], "channel": "Na_pyr", "factor": 0.5, "gate": "h", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Na_pyr.channel.nml", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/forwardRate[1]", "attribute": "rate", "old": "1.28e2per_s", "new": "6.4e1per_s", "action": "set", "note": "scale_gate_time_constant"}, {"file": "LEMSexamples/morphologies/Na_pyr.channel.nml", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/reverseRate[1]", "attribute": "rate", "old": "4e3per_s", "new": "2e3per_s", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1459.184 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.04671932739912799 | 0.130327 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-992f6d2676616d2b1b47` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | -7.568164269583633 | 0.521075 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-992f6d2676616d2b1b47` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 102.63596725449597 | 2.58695 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-992f6d2676616d2b1b47` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 120.59999999989037 | 43.71 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-992f6d2676616d2b1b47` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 5.0 | 3 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-992f6d2676616d2b1b47` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 98.06893539575677 | 100.60270309325779 | 2.53377 | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-554d9ad1f1b1ad0f907e` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-554d9ad1f1b1ad0f907e` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-554d9ad1f1b1ad0f907e` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 98.06814575218911 | 100.56618499677191 | 2.49804 | 1.96136 | `r-f6700284baa99a5ef41f` | `r-6d6cddcfd246a560b827` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 647.6000000046679 | 60.71 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-6d6cddcfd246a560b827` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.04667826472914667 | 0.13062 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-7be27abc7573e88ede15` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | -7.564954267229368 | 0.524012 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-7be27abc7573e88ede15` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 102.53409576402812 | 2.65507 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-7be27abc7573e88ede15` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 120.27999999989066 | 43.69 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-7be27abc7573e88ede15` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 5.0 | 3 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-7be27abc7573e88ede15` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 97.6356582663006 | 100.29986572216364 | 2.66421 | 1.96138 | `r-16be743cbc8f0485fd82` | `r-2e5528ccb8009523ca79` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-2e5528ccb8009523ca79` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 1.0 | 1 | 0.5 | `r-16be743cbc8f0485fd82` | `r-2e5528ccb8009523ca79` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 97.55448913585151 | 100.17643738059338 | 2.62195 | 1.96136 | `r-493fa57e11933a720397` | `r-cf92c96d7f9950f320c2` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 646.7400000046082 | 60.77 | 11.7378 | `r-493fa57e11933a720397` | `r-cf92c96d7f9950f320c2` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
