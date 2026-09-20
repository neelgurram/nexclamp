# osb_hh2_477127614__factor_file__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `osb_hh2_477127614`
- stratum: control
- kind/family/operator: valid_transform / factoring / factor_file
- parameters: `{"element": "pulseGenerator", "file": "cells/HH2/network_477127614_HH2.net.nml", "generator_seed": 20260917, "ident": "input_29", "locator": "/neuroml/pulseGenerator[@id='input_29']", "n_sites": 21, "new_file": "cells/HH2/input_29.factored.nml", "site_index": 18}`
- recorded edits: `[{"file": "cells/HH2/network_477127614_HH2.net.nml", "locator": "/neuroml/pulseGenerator[@id='input_29']", "attribute": null, "old": "<pulseGenerator id=\"input_29\" delay=\"270ms\" duration=\"1000ms\" amplitude=\"50.0 pA\"/>", "new": null, "action": "remove", "note": "moved to cells/HH2/input_29.factored.nml"}, {"file": "cells/HH2/network_477127614_HH2.net.nml", "locator": "/neuroml/include[@href='input_29.factored.nml']", "attribute": "href", "old": null, "new": "input_29.factored.nml", "action": "insert", "note": "include of the factored file"}, {"file": "cells/HH2/input_29.factored.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "<neuroml xmlns=\"http://www.neuroml.org/schema/neuroml2\"  xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta5.xsd\" id=\"input_29_factored\">\n\n    <include href=\"HH2_477127614.cell.nml\"></include>\n\n    <pulseGenerator id=\"input_29\" delay=\"270ms\" duration=\"1000ms\" amplitude=\"50.0 pA\"/>\n\n</neuroml>\n", "action": "insert", "note": "new file holding <pulseGenerator> 'input_29' plus copies of cells/HH2/network_477127614_HH2.net.nml's includes"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 485.992 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
