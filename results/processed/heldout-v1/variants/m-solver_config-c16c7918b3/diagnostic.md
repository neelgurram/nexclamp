# m-solver_config-c16c7918b3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / solver_config
- parameters: `{"generator_seed": 20260917, "mechanism": "insert_meta", "method": "eulertree"}`
- recorded edits: `[{"file": "NMC/NeuroML2/LEMS_Soma_AllNML2.xml", "locator": "/Lems[1]/Component[@id='sim1']/Meta[1]", "attribute": null, "old": null, "new": "<Meta xmlns=\"http://www.neuroml.org/lems/0.7.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" for=\"jlems\" method=\"eulertree\"/>", "action": "insert", "note": "solver_config"}]`
- execution overrides: `{"integrator_method": "eulertree"}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 12210.975 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
