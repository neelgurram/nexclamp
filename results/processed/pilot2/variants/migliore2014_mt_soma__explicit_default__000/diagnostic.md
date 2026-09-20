# migliore2014_mt_soma__explicit_default__000

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: control
- kind/family/operator: valid_transform / explicit_default / explicit_default
- parameters: `{"attribute": "segmentGroup", "file": "NeuroML2/Channels/test/MT_soma.cell.nml", "generator_seed": 20260917, "locator": "/neuroml/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/spikeThresh[1]", "n_sites": 8, "site_index": 4, "value": "all", "xsd_type": "SpikeThresh"}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/spikeThresh[1]", "attribute": "segmentGroup", "old": null, "new": "all", "action": "insert", "note": "explicit XSD default of SpikeThresh"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 610.931 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
