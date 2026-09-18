# acnet2_pyr_soma__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "scale", "file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "n_sites": 194, "new": "-5e-3V", "old": "-0.005V", "site_index": 25, "style": "scientific", "xsd_type": "Nml2Quantity_voltage"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "attribute": "scale", "old": "-0.005V", "new": "-5e-3V", "action": "set", "note": "numerically identical literal (scientific)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 462.641 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
