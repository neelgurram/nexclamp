# nml2_hh_example__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "diameter", "file": "examples/NML2_SingleCompHHCell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='hhcell']/morphology[@id='morph1']/segment[@id='0']/proximal[1]", "n_sites": 111, "new": "17.8412420", "old": "17.841242", "site_index": 64, "style": "padded", "xsd_type": "DoubleGreaterThanZero"}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml/cell[@id='hhcell']/morphology[@id='morph1']/segment[@id='0']/proximal[1]", "attribute": "diameter", "old": "17.841242", "new": "17.8412420", "action": "set", "note": "numerically identical literal (padded)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 213.297 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
