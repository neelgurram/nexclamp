# m-scale_gate_slope-2599d25adf

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='Ca_LVAst']/ionChannel[@id='Ca_LVAst']/gate[@id='h']/steadyState[1]", "new": "-5.12mV", "old": "-6.4mV"}], "channel": "Ca_LVAst", "factor": 0.8, "gate": "h", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Ca_LVAst.channel.nml", "locator": "/neuroml[@id='Ca_LVAst']/ionChannel[@id='Ca_LVAst']/gate[@id='h']/steadyState[1]", "attribute": "scale", "old": "-6.4mV", "new": "-5.12mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4730.864 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | -1.1430809257249877 | 0.683601 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-a52b5663a8ff68501800` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 16.529999999984966 | 0.74 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-a52b5663a8ff68501800` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-a52b5663a8ff68501800` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | 0.14120505523723637 | 0.732827 | 0.5 | `r-49ced7acda977f37b12b` | `r-391cd84a68f9ff2850b8` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 40.20999999996343 | 3.56 | 0.733 | `r-49ced7acda977f37b12b` | `r-391cd84a68f9ff2850b8` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 14.0 | 1 | 0.5 | `r-49ced7acda977f37b12b` | `r-391cd84a68f9ff2850b8` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -0.24597145843398494 | 0.70652 | 0.5 | `r-b99907e8e6510bd22247` | `r-ea1c753a3cddab7d5590` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 136.4200000027938 | 6.55 | 3.03 | `r-b99907e8e6510bd22247` | `r-ea1c753a3cddab7d5590` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 23.0 | 1 | 0.5 | `r-da1341cbf9665d4e7639` | `r-1331ef247c18cab034a1` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | -1.8523404769881324 | 0.711686 | 0.5 | `r-ad42eb643e1748725abb` | `r-c0219f93d20ab8c6ca08` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | -1.1488675890141025 | 0.684119 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-d8b5a70af5c1d0966a87` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 16.519999999984975 | 0.75 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-d8b5a70af5c1d0966a87` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-d8b5a70af5c1d0966a87` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | 0.1695777282727562 | 0.740525 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-45b5da7286e6d77c24ca` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 40.19999999996344 | 3.64 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-45b5da7286e6d77c24ca` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 14.0 | 1 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-45b5da7286e6d77c24ca` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | -0.16960989379838054 | 0.722779 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-b4de09944b713fdef699` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 137.39000000299893 | 6.59 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-b4de09944b713fdef699` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 23.0 | 1 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-1a3dc3dbc5456915dbd9` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | -1.8729942932136936 | 0.706063 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-6bbe7dbfe050c9535ad1` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
