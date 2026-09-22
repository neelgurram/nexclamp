# m-shift_reversal-192b2f0278

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Nap_Et2_all']", "new": "60.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "Nap_Et2_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Nap_Et2_all']", "attribute": "erev", "old": "50.0 mV", "new": "60.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5231.877 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 22.069999999979927 | 1.52 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-d7592a3538705a276ea7` |
| h/1 | P06_ramp | spike_count | exceeds | 33.0 | 34.0 | 1 | 0.5 | `r-fc615de8a8cfe6dc7efe` | `r-b4492cd79f74be5e9173` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 22.059999999979937 | 1.52 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-a775e9886b75bdd06828` |
| h/2 | P06_ramp | spike_count | exceeds | 33.0 | 34.0 | 1 | 0.5 | `r-bd5adb30d6c703f0c55d` | `r-7b99e33620bdaad24931` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
