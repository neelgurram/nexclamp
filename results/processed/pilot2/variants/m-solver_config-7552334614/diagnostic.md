# m-solver_config-7552334614

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / solver_config
- parameters: `{"generator_seed": 20260917, "mechanism": "insert_meta", "method": "eulertree"}`
- recorded edits: `[{"file": "LEMSexamples/LEMS_NML2_Ex5_DetCell.xml", "locator": "/Lems[1]/Simulation[@id='sim1']/Meta[1]", "attribute": null, "old": null, "new": "<Meta for=\"jlems\" method=\"eulertree\"/>", "action": "insert", "note": "solver_config"}]`
- execution overrides: `{"integrator_method": "eulertree"}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1266.917 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
