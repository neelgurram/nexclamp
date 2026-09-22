# migliore2005_ca1_soma__numeric_literal_format__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: control
- kind/family/operator: valid_transform / literal_format / numeric_literal_format
- parameters: `{"attribute": "z", "file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='SomaOnly_allCml']/morphology[@id='morphology_SomaOnly_allCml']/segment[@id='0']/distal[1]", "n_sites": 379, "new": "0", "old": "0.0", "site_index": 32, "style": "plain", "xsd_type": "xs:double"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml/cell[@id='SomaOnly_allCml']/morphology[@id='morphology_SomaOnly_allCml']/segment[@id='0']/distal[1]", "attribute": "z", "old": "0.0", "new": "0", "action": "set", "note": "numerically identical literal (plain)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 1022.028 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
