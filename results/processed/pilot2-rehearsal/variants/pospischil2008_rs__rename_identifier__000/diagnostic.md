# pospischil2008_rs__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "NeuroML2/cells/RS/RS.cell.nml", "generator_seed": 20260917, "kind": "morphology", "locator": "/neuroml/cell[@id='RS']/morphology[@id='morphology_RS']", "n_sites": 20, "new": "morphology_RS_renamed", "old": "morphology_RS", "site_index": 1}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml/cell[@id='RS']/morphology[@id='morphology_RS']", "attribute": "id", "old": "morphology_RS", "new": "morphology_RS_renamed", "action": "set", "note": "rename morphology morphology_RS -> morphology_RS_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 438.576 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
