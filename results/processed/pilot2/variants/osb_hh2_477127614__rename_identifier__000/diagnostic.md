# osb_hh2_477127614__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "cells/HH2/Leak.channel.nml", "generator_seed": 20260917, "kind": "ionChannel", "locator": "/neuroml/ionChannel[@id='LeakConductance']", "n_sites": 30, "new": "LeakConductance_renamed", "old": "LeakConductance", "site_index": 17}`
- recorded edits: `[{"file": "cells/HH2/HH2_477127614.cell.nml", "locator": "/neuroml/cell[@id='HH2_477127614']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "ionChannel", "old": "LeakConductance", "new": "LeakConductance_renamed", "action": "set", "note": "rename ionChannel LeakConductance -> LeakConductance_renamed (locators refer to the pre-edit file)"}, {"file": "cells/HH2/Leak.channel.nml", "locator": "/neuroml/ionChannel[@id='LeakConductance']", "attribute": "id", "old": "LeakConductance", "new": "LeakConductance_renamed", "action": "set", "note": "rename ionChannel LeakConductance -> LeakConductance_renamed (locators refer to the pre-edit file)"}, {"file": "cells/HH2/Leak.channel.nml", "locator": "/neuroml/ionChannel[@id='LeakConductance']/annotation[1]/RDF[1]/Description[1]", "attribute": "rdf:about", "old": "LeakConductance", "new": "LeakConductance_renamed", "action": "set", "note": "rename ionChannel LeakConductance -> LeakConductance_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 477.879 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
