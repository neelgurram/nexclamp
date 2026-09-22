# m-wrong_compatible_component-fb7ebc795f

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "new": "K_Tst", "old": "SK_E2"}], "element_id": "SK_E2_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "attribute": "ionChannel", "old": "SK_E2", "new": "K_Tst", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5313.532 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.0296528898400037 | 0.005697176139461529 | 0.0239557 | 0.01 | `r-f821a906ac6ddfedc3f9` | `r-4463c30845a63d10d85f` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 12.81999999998834 | 10.77 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-4463c30845a63d10d85f` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 8.0 | 3 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-4463c30845a63d10d85f` |
| h/1 | P04_step_2x | last_isi | exceeds | 16.709999999984802 | 11.93999999998914 | 4.77 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-2510955f3f1d5998eb0e` |
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 42.0 | 12 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-2510955f3f1d5998eb0e` |
| h/1 | P05_long_step | last_isi | exceeds | 118.6600000025901 | 14.430000000314976 | 104.23 | 2.3732 | `r-a413bdc9ef17abaeb327` | `r-a435f812fe09b8172a78` |
| h/1 | P05_long_step | spike_count | exceeds | 16.0 | 137.0 | 121 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-a435f812fe09b8172a78` |
| h/1 | P06_ramp | spike_count | exceeds | 33.0 | 53.0 | 20 | 0.5 | `r-fc615de8a8cfe6dc7efe` | `r-27f8a92dbea318e99641` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.029665994195325708 | 0.005701748891649136 | 0.0239642 | 0.01 | `r-1175b1c4f005ecbea9cd` | `r-26e4ef3c926e03e1dc7b` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 12.80999999998835 | 10.77 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-26e4ef3c926e03e1dc7b` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 8.0 | 3 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-26e4ef3c926e03e1dc7b` |
| h/2 | P04_step_2x | last_isi | exceeds | 16.66999999998484 | 11.909999999989168 | 4.76 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-1ee5b965315abe1de1d7` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 42.0 | 12 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-1ee5b965315abe1de1d7` |
| h/2 | P05_long_step | last_isi | exceeds | 118.89000000259512 | 14.400000000314321 | 104.49 | 2.3732 | `r-019eab9c744398314e93` | `r-ce610f25e22687b971c5` |
| h/2 | P05_long_step | spike_count | exceeds | 16.0 | 137.0 | 121 | 0.5 | `r-019eab9c744398314e93` | `r-ce610f25e22687b971c5` |
| h/2 | P06_ramp | spike_count | exceeds | 33.0 | 53.0 | 20 | 0.5 | `r-bd5adb30d6c703f0c55d` | `r-c6697e7aaa1159b1e442` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
