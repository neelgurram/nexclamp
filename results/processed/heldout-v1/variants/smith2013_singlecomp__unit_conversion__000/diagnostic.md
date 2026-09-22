# smith2013_singlecomp__unit_conversion__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: control
- kind/family/operator: valid_transform / unit_conversion / unit_conversion
- parameters: `{"attribute": "delay", "file": "NeuroML2/singleCompAllChans.net.nml", "generator_seed": 20260917, "locator": "/neuroml/pulseGenerator[@id='iclamp1']", "n_sites": 114, "new": "0.3 s", "old": "300 ms", "site_index": 109, "to_unit": "s", "xsd_type": "Nml2Quantity_time"}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.net.nml", "locator": "/neuroml/pulseGenerator[@id='iclamp1']", "attribute": "delay", "old": "300 ms", "new": "0.3 s", "action": "set", "note": "exact decimal unit conversion (Nml2Quantity_time)"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 738.986 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
