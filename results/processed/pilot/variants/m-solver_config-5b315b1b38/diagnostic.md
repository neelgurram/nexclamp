# m-solver_config-5b315b1b38

- model: `pospischil2008_rs`
- kind/family/operator: mutant / numerical / solver_config
- parameters: `{"generator_seed": 20260913, "mechanism": "insert_meta", "method": "rk4"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/LEMS_RS.xml", "locator": "/Lems[1]/Component[@id='sim1']/Meta[1]", "attribute": null, "old": null, "new": "<Meta xmlns=\"http://www.neuroml.org/lems/0.7.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" for=\"jlems\" method=\"rk4\"/>", "action": "insert", "note": "solver_config"}]`
- execution overrides: `{"integrator_method": "rk4"}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 555.229 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
