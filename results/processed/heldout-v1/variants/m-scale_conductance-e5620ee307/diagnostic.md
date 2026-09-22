# m-scale_conductance-e5620ee307

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Nap_Et2_all']", "new": "1.548 mS_per_cm2", "old": "1.72 mS_per_cm2"}], "element": "channelDensity", "element_id": "Nap_Et2_all", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Nap_Et2_all']", "attribute": "condDensity", "old": "1.72 mS_per_cm2", "new": "1.548 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5165.79 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.0296528898400037 | 0.0586073105983255 | 0.0289544 | 0.01 | `r-f821a906ac6ddfedc3f9` | `r-dd5831a02ed542c48f2c` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 25.919999999976426 | 2.33 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-dd5831a02ed542c48f2c` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-dd5831a02ed542c48f2c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02735468888737108 | 0.027969400997199648 | 0.000614712 | 0.000547094 | `s-02f79883d677a19ab9ec` | `s-122f1e69c77759a784f8` |
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-0596b743a8c685ab9e8b` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 361.82999999954313 | 369.40999999953624 | 7.58 | 7.2366 | `r-fc615de8a8cfe6dc7efe` | `r-5e22aa4f4c3d5a35f11b` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.029665994195325708 | 0.05884756845116469 | 0.0291816 | 0.01 | `r-1175b1c4f005ecbea9cd` | `r-539ec0dff8e36cd84aa1` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 25.909999999976435 | 2.33 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-539ec0dff8e36cd84aa1` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 4.0 | 1 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-539ec0dff8e36cd84aa1` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02735468888737108 | 0.027969400997199648 | 0.000614712 | 0.000547094 | `s-220825f25b753f7de32f` | `s-b87925537835b68f9cee` |
| h/2 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-b9c32680fe6fb25bd57a` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 361.7799999995432 | 369.3499999995363 | 7.57 | 7.2366 | `r-bd5adb30d6c703f0c55d` | `r-eca1e21ac6a98e561846` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
