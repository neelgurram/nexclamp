# osb_hh2_477127614__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "conductance", "file": "cells/HH2/IM.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='IM']", "n_sites": 76, "new": "1e-11S", "old": "10pS", "site_index": 25, "to_unit": "S", "xsd_type": "Nml2Quantity_conductance"}`
- recorded edits: `[{"file": "cells/HH2/IM.channel.nml", "locator": "/neuroml/ionChannel[@id='IM']", "attribute": "conductance", "old": "10pS", "new": "1e-11S", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_conductance)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 490.924 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
