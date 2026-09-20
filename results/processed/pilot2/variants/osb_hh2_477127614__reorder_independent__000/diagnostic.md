# osb_hh2_477127614__reorder_independent__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: control
- kind/family/operator: valid_transform / reordering / reorder_independent
- parameters: `{"count": 2, "file": "cells/HH2/IL.channel.nml", "first": 1, "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='IL']", "n_sites": 16, "permutation": "reverse", "site_index": 6, "tag": "gate"}`
- recorded edits: `[{"file": "cells/HH2/IL.channel.nml", "locator": "/neuroml/ionChannel[@id='IL']", "attribute": null, "old": "q,r", "new": "r,q", "action": "text", "note": "reorder 2 consecutive <gate> siblings (reverse)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 491.742 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
