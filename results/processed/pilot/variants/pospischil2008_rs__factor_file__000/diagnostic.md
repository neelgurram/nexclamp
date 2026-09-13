# pospischil2008_rs__factor_file__000

- model: `pospischil2008_rs`
- kind/family/operator: valid_transform / factoring / factor_file
- parameters: `{"element": "pulseGenerator", "file": "NeuroML2/cells/RS/RS.net.nml", "generator_seed": 20260913, "ident": "Input_1", "locator": "/neuroml/pulseGenerator[@id='Input_1']", "n_sites": 11, "new_file": "NeuroML2/cells/RS/Input_1.factored.nml", "site_index": 1}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.net.nml", "locator": "/neuroml/pulseGenerator[@id='Input_1']", "attribute": null, "old": "<pulseGenerator id=\"Input_1\" delay=\"0.3s\" duration=\"0.4s\" amplitude=\"7.5E-10A\"/>", "new": null, "action": "remove", "note": "moved to NeuroML2/cells/RS/Input_1.factored.nml"}, {"file": "NeuroML2/cells/RS/RS.net.nml", "locator": "/neuroml/include[@href='Input_1.factored.nml']", "attribute": "href", "old": null, "new": "Input_1.factored.nml", "action": "insert", "note": "include of the factored file"}, {"file": "NeuroML2/cells/RS/Input_1.factored.nml", "locator": "/neuroml", "attribute": null, "old": null, "new": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<neuroml xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.neuroml.org/schema/neuroml2  https://raw.githubusercontent.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta4.xsd\" id=\"Input_1_factored\">\n\n    <include href=\"../../channels/Kd/Kd.channel.nml\"/>\n    <include href=\"../../channels/IM/IM.channel.nml\"/>\n    <include href=\"../../channels/Leak/Leak.channel.nml\"/>\n    <include href=\"../../channels/Na/Na.channel.nml\"/>\n    <include href=\"RS.cell.nml\"/>\n\n    <pulseGenerator id=\"Input_1\" delay=\"0.3s\" duration=\"0.4s\" amplitude=\"7.5E-10A\"/>\n\n</neuroml>\n", "action": "insert", "note": "new file holding <pulseGenerator> 'Input_1' plus copies of NeuroML2/cells/RS/RS.net.nml's includes"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 318.325 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
