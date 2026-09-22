# m-shift_reversal-5d369845ce

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "new": "-90.0 mV", "old": "-85.0 mV"}], "element": "channelDensity", "element_id": "SK_E2_all", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='SK_E2_all']", "attribute": "erev", "old": "-85.0 mV", "new": "-90.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4679.14 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 18.22999999998342 | 2.44 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-eb69e8b4e53cf6f6d753` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-eb69e8b4e53cf6f6d753` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.01011398557861304 | -0.012700891939660718 | 0.0228149 | 0.01 | `r-49ced7acda977f37b12b` | `r-099a603fcdf7851c8134` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 120.09999999989077 | 83.45 | 0.733 | `r-49ced7acda977f37b12b` | `r-099a603fcdf7851c8134` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 4.0 | 11 | 0.5 | `r-49ced7acda977f37b12b` | `r-099a603fcdf7851c8134` |
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 151.46000000330605 | 8.49 | 3.03 | `r-b99907e8e6510bd22247` | `r-63a9f8f8ccf82bd0ff53` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-63a9f8f8ccf82bd0ff53` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 19.0 | 5 | 0.5 | `r-da1341cbf9665d4e7639` | `r-65a026566dd3822e12da` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 18.199999999983447 | 2.43 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-93e4b89bdb15601127a2` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-93e4b89bdb15601127a2` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.010272237117704504 | -0.012801696020874331 | 0.0230739 | 0.01 | `r-1e40b84a0cfdecc32574` | `r-44aae09f52648754236a` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 121.06999999988989 | 84.51 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-44aae09f52648754236a` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 4.0 | 11 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-44aae09f52648754236a` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 152.49000000332853 | 8.51 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-38ebc5a2a83e3b7eca71` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-38ebc5a2a83e3b7eca71` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 19.0 | 5 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-37ce34a29641812cb861` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
