# nml2_hh_example__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "rate", "file": "examples/NML2_SingleCompHHCell.nml", "generator_seed": 20260917, "locator": "/neuroml/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "n_sites": 55, "new": "125per_s", "old": "0.125per_ms", "site_index": 32, "to_unit": "per_s", "xsd_type": "Nml2Quantity_pertime"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml/ionChannelHH[@id='kChan']/gateHHrates[@id='n']/reverseRate[1]", "attribute": "rate", "old": "0.125per_ms", "new": "125per_s", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_pertime)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 208.484 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
