# migliore2014_mt_soma__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "amplitude", "file": "NeuroML2/Channels/test/OlfactoryTest_12.net.nml", "generator_seed": 20260917, "locator": "/neuroml/pulseGenerator[@id='Input_13']", "n_sites": 88, "new": "0.00006uA", "old": "6.0E-11A", "site_index": 80, "to_unit": "uA", "xsd_type": "Nml2Quantity_current"}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/OlfactoryTest_12.net.nml", "locator": "/neuroml/pulseGenerator[@id='Input_13']", "attribute": "amplitude", "old": "6.0E-11A", "new": "0.00006uA", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_current)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 602.725 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
