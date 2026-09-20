# nml2_hh_example__explicit_default__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: control
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "examples/NML2_SingleCompHHCell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "n_sites": 7, "site_index": 4, "value": "all", "xsd_type": "SpecificCapacitance"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/specificCapacitance[1]", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of SpecificCapacitance"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 206.426 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
