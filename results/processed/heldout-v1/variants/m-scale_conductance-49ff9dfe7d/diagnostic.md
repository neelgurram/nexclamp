# m-scale_conductance-49ff9dfe7d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "new": "6.86 mS_per_cm2", "old": "3.43 mS_per_cm2"}], "element": "channelDensityNernst", "element_id": "Ca_LVAst_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityNernst[@id='Ca_LVAst_all']", "attribute": "condDensity", "old": "3.43 mS_per_cm2", "new": "6.86 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4739.706 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | 1.6149584744492103 | 2.07444 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-f0cf43f463543493052c` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 13.999999999987267 | 1.79 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-f0cf43f463543493052c` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-f0cf43f463543493052c` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | 3.2748915735888886 | 2.40086 | 0.5 | `r-49ced7acda977f37b12b` | `r-ec82a2ed66f41f9770c3` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 26.339999999976044 | 10.31 | 0.733 | `r-49ced7acda977f37b12b` | `r-ec82a2ed66f41f9770c3` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 20.0 | 5 | 0.5 | `r-49ced7acda977f37b12b` | `r-ec82a2ed66f41f9770c3` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | 2.7058608118684333 | 2.24531 | 0.5 | `r-b99907e8e6510bd22247` | `r-e4791ff18a6b55d65d97` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 156.45000000341497 | 13.48 | 3.03 | `r-b99907e8e6510bd22247` | `r-e4791ff18a6b55d65d97` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-e4791ff18a6b55d65d97` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 27.0 | 3 | 0.5 | `r-da1341cbf9665d4e7639` | `r-a0341b6a364ee5776c8a` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | 1.207081514996318 | 2.34774 | 0.5 | `r-ad42eb643e1748725abb` | `r-ca67ab81530b81d243de` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | 1.6113456093475946 | 2.07609 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-2afb8d8a468f56f49742` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 13.979999999987285 | 1.79 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-2afb8d8a468f56f49742` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-2afb8d8a468f56f49742` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | 3.3365207977311826 | 2.42642 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-4def91d4b9b8c5a20227` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 26.109999999976253 | 10.45 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-4def91d4b9b8c5a20227` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 20.0 | 5 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-4def91d4b9b8c5a20227` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | 2.850841171263781 | 2.29767 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-3904b831fa2199c2bf71` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 157.4500000034368 | 13.47 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-3904b831fa2199c2bf71` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-3904b831fa2199c2bf71` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 27.0 | 3 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-42373f69cb99e26449d0` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | 1.1636844940217799 | 2.33062 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-aa7031f66fe3643220d1` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
