# m-increase_dt-445bb4bee3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / increase_dt
- parameters: `{"changes": [{"attribute": "step", "locator": "/Lems[1]/Component[@id='sim1']", "new": "0.1ms", "old": "0.025ms"}], "factor": 4, "generator_seed": 20260917}`
- recorded edits: `[{"file": "cells/HH2/LEMS_477127614.xml", "locator": "/Lems[1]/Component[@id='sim1']", "attribute": "step", "old": "0.025ms", "new": "0.1ms", "action": "set", "note": "increase_dt"}]`
- execution overrides: `{"dt_factor": 4}`
- class: **3_numerically_unstable**
- nominal-level status: numerically_unstable; runtime 146.022 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
