# osb_hh2_477127614__add_comments__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: control
- kind/family/operator: no_change_control / formatting / add_comments
- parameters: `{"file": "cells/HH2/Kd.channel.nml", "generator_seed": 20260917, "locator": "/neuroml", "n_sites": 24, "position": "before_root_end", "site_index": 11}`
- recorded edits: `[{"file": "cells/HH2/Kd.channel.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "1 comment(s)", "action": "insert", "note": "add_comments position=before_root_end"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 492.907 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
