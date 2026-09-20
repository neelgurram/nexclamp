# migliore2014_mt_soma__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "value", "file": "NeuroML2/Channels/kamt.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ComponentType[@name='kamt_h_tau_tau']/Constant[@name='VOLT_SCALE']", "n_sites": 437, "new": "1mV", "old": "1 mV", "site_index": 61, "style": "unit_spacing", "xsd_type": "Nml2Quantity"}`
- recorded edits: `[{"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml/ComponentType[@name='kamt_h_tau_tau']/Constant[@name='VOLT_SCALE']", "attribute": "value", "old": "1 mV", "new": "1mV", "action": "set", "note": "numerically identical literal (unit_spacing)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 591.567 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
