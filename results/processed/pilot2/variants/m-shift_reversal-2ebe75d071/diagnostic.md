# m-shift_reversal-2ebe75d071

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-102.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260917, "shift_mV": -2.0}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-102.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 943.725 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -5.663406372074732 | 0.8311 | 0.5 | `r-4cceac4cec0eb866659f` | `r-de3c292bb6f4ac8f995f` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 60.0 | 1 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-fca84687f54423d7430d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -5.562149047842723 | 0.827469 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-19692e77773ce19a20d2` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 60.0 | 1 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-d06b569c258ff266d83c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
