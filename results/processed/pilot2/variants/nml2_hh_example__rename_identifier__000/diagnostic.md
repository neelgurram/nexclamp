# nml2_hh_example__rename_identifier__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `nml2_hh_example`
- stratum: control
- kind/family/operator: valid_transform / renaming / rename_identifier
- parameters: `{"file": "examples/NML2_SingleCompHHCell.nml", "generator_seed": 20260917, "kind": "channelDensity", "locator": "/neuroml/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='leak']", "n_sites": 16, "new": "leak_renamed", "old": "leak", "site_index": 10}`
- recorded edits: `[{"file": "examples/NML2_SingleCompHHCell.nml", "locator": "/neuroml/cell[@id='hhcell']/biophysicalProperties[@id='bioPhys1']/membraneProperties[1]/channelDensity[@id='leak']", "attribute": "id", "old": "leak", "new": "leak_renamed", "action": "set", "note": "rename channelDensity leak -> leak_renamed (locators refer to the pre-edit file)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 206.952 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
