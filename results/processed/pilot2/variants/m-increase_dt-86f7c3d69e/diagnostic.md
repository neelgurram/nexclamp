# m-increase_dt-86f7c3d69e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.04ms", "old": "0.01ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/LEMS_OlfactoryTest_12.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.01ms", "new": "0.04ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1076.259 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
