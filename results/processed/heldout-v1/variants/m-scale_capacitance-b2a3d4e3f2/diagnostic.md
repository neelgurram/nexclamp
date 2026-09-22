# m-scale_capacitance-b2a3d4e3f2

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5134.733 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.0880088878417 | 92.15071487223572 | 4.06271 | 1.76176 | `r-f821a906ac6ddfedc3f9` | `r-26dee452c65d9938ca0f` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 19.619999999982156 | 3.97 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-26dee452c65d9938ca0f` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-26dee452c65d9938ca0f` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 90.98012542725024 | 94.67940139905 | 3.69928 | 3.13776 | `r-57ea9af033cb1e2a1b46` | `r-dafc19963b363a58341d` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 6.8099999998659655 | 5.41999999986723 | 1.39 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-dafc19963b363a58341d` |
| h/1 | P04_step_2x | last_isi | exceeds | 16.709999999984802 | 14.68999999998664 | 2.02 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-dafc19963b363a58341d` |
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 34.0 | 4 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-dafc19963b363a58341d` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.42731093900892 | 91.27099608420062 | 3.84369 | 3.45091 | `r-a413bdc9ef17abaeb327` | `r-292a2465e501d52b7508` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 7.989999999864892 | 2.14 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-292a2465e501d52b7508` |
| h/1 | P06_ramp | spike_count | exceeds | 33.0 | 37.0 | 4 | 0.5 | `r-fc615de8a8cfe6dc7efe` | `r-145638c75b36ad0cdce9` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.05227279779325 | 91.75904084247271 | 3.70677 | 1.76176 | `r-1175b1c4f005ecbea9cd` | `r-6e9bcd68b703d653062c` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 19.619999999982156 | 3.96 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-6e9bcd68b703d653062c` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-6e9bcd68b703d653062c` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.93420410215381 | 93.73220825108498 | 3.798 | 3.13776 | `r-2cb2390f7c947ffeefc6` | `r-4baa3f68e0f3aa7f6da3` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 6.779999999865993 | 5.389999999867257 | 1.39 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-4baa3f68e0f3aa7f6da3` |
| h/2 | P04_step_2x | last_isi | exceeds | 16.66999999998484 | 14.649999999986676 | 2.02 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-4baa3f68e0f3aa7f6da3` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 34.0 | 4 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-4baa3f68e0f3aa7f6da3` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 86.27700805705253 | 90.14051818282219 | 3.86351 | 3.45091 | `r-019eab9c744398314e93` | `r-b4f54f204315c7ee2c74` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 7.95999999986492 | 2.14 | 0.5 | `r-019eab9c744398314e93` | `r-b4f54f204315c7ee2c74` |
| h/2 | P06_ramp | spike_count | exceeds | 33.0 | 37.0 | 4 | 0.5 | `r-bd5adb30d6c703f0c55d` | `r-6e11c103ac72c30db437` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
