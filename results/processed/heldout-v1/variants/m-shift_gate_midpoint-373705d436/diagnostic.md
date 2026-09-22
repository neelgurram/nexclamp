# m-shift_gate_midpoint-373705d436

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Ca_LVAst']/ionChannel[@id='Ca_LVAst']/gate[@id='h']/steadyState[1]", "new": "-95mV", "old": "-90mV"}], "channel": "Ca_LVAst", "delta_mV": -5.0, "gate": "h", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Ca_LVAst.channel.nml", "locator": "/neuroml[@id='Ca_LVAst']/ionChannel[@id='Ca_LVAst']/gate[@id='h']/steadyState[1]", "attribute": "midpoint", "old": "-90mV", "new": "-95mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4863.844 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | -1.571850962452615 | 1.11237 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-78bef5a8f5bc5ad426f2` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 16.869999999984657 | 1.08 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-78bef5a8f5bc5ad426f2` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-78bef5a8f5bc5ad426f2` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | -0.40967830149416784 | 1.28371 | 0.5 | `r-49ced7acda977f37b12b` | `r-828fc2b8750bd008dd40` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 40.91999999996278 | 4.27 | 0.733 | `r-49ced7acda977f37b12b` | `r-828fc2b8750bd008dd40` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 13.0 | 2 | 0.5 | `r-49ced7acda977f37b12b` | `r-828fc2b8750bd008dd40` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -0.7453640314740113 | 1.20591 | 0.5 | `r-b99907e8e6510bd22247` | `r-170b41ab9b153583682b` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 134.4700000029352 | 8.5 | 3.03 | `r-b99907e8e6510bd22247` | `r-170b41ab9b153583682b` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-170b41ab9b153583682b` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 23.0 | 1 | 0.5 | `r-da1341cbf9665d4e7639` | `r-da0104178e3030955ea8` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | -2.476588091532193 | 1.33593 | 0.5 | `r-ad42eb643e1748725abb` | `r-4da9251b7a6baa2ce019` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | -1.5781262728351635 | 1.11338 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-7c9faf6b367653a94318` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 16.849999999984675 | 1.08 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-7c9faf6b367653a94318` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-7c9faf6b367653a94318` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | -0.3871804097493481 | 1.29728 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-afcced03ea1804366aaa` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 40.90999999996279 | 4.35 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-afcced03ea1804366aaa` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 13.0 | 2 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-afcced03ea1804366aaa` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | -0.6801186421725305 | 1.23329 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-4fd902be256430e49b7d` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 135.4600000029568 | 8.52 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-4fd902be256430e49b7d` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 15.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-4fd902be256430e49b7d` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 23.0 | 1 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-ba4abcc5c3d9f839ef3f` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | -2.492740712483325 | 1.32581 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-9f86435a48234a60ed65` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
