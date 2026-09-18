# m-omit_include-b072277531

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / omit_include
- parameters: `{"generator_seed": 20260917, "href": "Ca_conc.nml", "removed": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"Ca_conc.nml\"/>"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/include[1]", "attribute": null, "old": "<include xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" href=\"Ca_conc.nml\"/>", "new": null, "action": "remove", "note": "omit_include"}]`
- execution overrides: `{}`
- class: **2_non_executable**
- nominal-level status: build_error; runtime 26.761 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
