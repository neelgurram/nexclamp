# nml2_hh_example__factor_file__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: control
- kind/family/operator: valid_transform / factoring / factor_file
- parameters: `{"element": "ionChannelHH", "file": "examples/NML2_SingleCompHHCell.nml", "generator_seed": 20260917, "ident": "passiveChan", "locator": "/neuroml/ionChannelHH[@id='passiveChan']", "n_sites": 4, "new_file": "examples/passiveChan.factored.nml", "site_index": 0}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml/ionChannelHH[@id='passiveChan']", "attribute": null, "old": "<ionChannelHH id=\"passiveChan\" conductance=\"10pS\">\n        <notes>Leak conductance</notes>\n    </ionChannelHH>", "new": null, "action": "remove", "note": "moved to examples/passiveChan.factored.nml"}, {"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml/include[@href='passiveChan.factored.nml']", "attribute": "href", "old": null, "new": "passiveChan.factored.nml", "action": "insert", "note": "include of the factored file"}, {"file": "examples/passiveChan.factored.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<neuroml xmlns=\"http://www.neuroml.org/schema/neuroml2\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.neuroml.org/schema/neuroml2 ../Schemas/NeuroML2/NeuroML_v2beta4.xsd\"\n         id=\"passiveChan_factored\">\n\n\n    <ionChannelHH id=\"passiveChan\" conductance=\"10pS\">\n        <notes>Leak conductance</notes>\n    </ionChannelHH>\n\n</neuroml>\n", "action": "insert", "note": "new file holding <ionChannelHH> 'passiveChan' plus copies of examples/NML2_SingleCompHHCell.nml's includes"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 210.174 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
