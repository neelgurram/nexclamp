# m-increase_dt-22bc5325eb

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.01ms", "old": "0.0025ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/LEMS_m_in_b_in.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.0025ms", "new": "0.01ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1288.167 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 78.69999999992848 | 1.81 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-20a16cb40220e73395e1` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 98.06893539575677 | 100.72551345542473 | 2.65658 | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-904f5821acba17dd80b1` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 98.06814575218911 | 100.58672331923695 | 2.51858 | 1.96136 | `r-f6700284baa99a5ef41f` | `r-14d14df1f2952958973c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
