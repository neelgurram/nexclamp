# pospischil2008_fs__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "value", "file": "NeuroML2/channels/Na/Na.channel.nml", "generator_seed": 20260917, "locator": "/neuroml/ComponentType[@name='Na_m_alpha_rate']/Constant[@name='TIME_SCALE']", "n_sites": 118, "new": "1ms", "old": "1 ms", "site_index": 103, "style": "unit_spacing", "xsd_type": "Nml2Quantity"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml/ComponentType[@name='Na_m_alpha_rate']/Constant[@name='TIME_SCALE']", "attribute": "value", "old": "1 ms", "new": "1ms", "action": "set", "note": "numerically identical literal (unit_spacing)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 381.944 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
