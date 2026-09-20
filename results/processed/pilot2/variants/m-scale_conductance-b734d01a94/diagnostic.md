# m-scale_conductance-b734d01a94

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "9.0 mS_per_cm2", "old": "10.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Kd_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "condDensity", "old": "10.0 mS_per_cm2", "new": "9.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 922.89 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -3.721069335935283 | 1.11124 | 0.5 | `r-4cceac4cec0eb866659f` | `r-eccb47c4413d2dfe2a8d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -3.6263351440319127 | 1.10835 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-03c15fddc7ec6c1b8735` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 62.0 | 1 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-48c4870c4c955f26e0e9` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
