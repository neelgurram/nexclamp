# m-scale_capacitance-068b4305c4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Soma_AllCML.cell.nml", "locator": "/neuroml[@id='Soma_AllCML']/cell[@id='Soma_AllCML']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4639.572 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 90.78240967397937 | 94.81769560420798 | 4.03529 | 1.81565 | `r-a22266676a5c9c51fe6b` | `r-4efa4b89ac8eef0b7e2d` |
| h/1 | P00_canonical | last_isi | exceeds | 15.789999999985639 | 13.909999999987349 | 1.88 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-4efa4b89ac8eef0b7e2d` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-4efa4b89ac8eef0b7e2d` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.04202652392433 | 93.5670890773784 | 4.52506 | 3.5976 | `r-49ced7acda977f37b12b` | `r-aa10c4033d703cb49933` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.549999999864383 | 6.789999999865984 | 1.76 | 0.5 | `r-49ced7acda977f37b12b` | `r-aa10c4033d703cb49933` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 26.84999999997558 | 9.8 | 0.733 | `r-49ced7acda977f37b12b` | `r-aa10c4033d703cb49933` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 20.0 | 5 | 0.5 | `r-49ced7acda977f37b12b` | `r-aa10c4033d703cb49933` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 85.6294059753018 | 89.95713042096878 | 4.32772 | 3.92393 | `r-b99907e8e6510bd22247` | `r-7aff9c88b6241bfe227c` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.769999999860545 | 10.05999999986301 | 2.71 | 0.5 | `r-b99907e8e6510bd22247` | `r-7aff9c88b6241bfe227c` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 27.0 | 3 | 0.5 | `r-da1341cbf9665d4e7639` | `r-dc49609ae742a69caa61` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 90.22942352330233 | 94.4670944240575 | 4.23767 | 1.81565 | `r-ebfd6e5f8d6b9e916dfe` | `r-a7353a06a84d22f6de1e` |
| h/2 | P00_canonical | last_isi | exceeds | 15.769999999985657 | 13.889999999987367 | 1.88 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-a7353a06a84d22f6de1e` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-a7353a06a84d22f6de1e` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 87.8428268328099 | 92.44927978498805 | 4.60645 | 3.5976 | `r-1e40b84a0cfdecc32574` | `r-624f468d9eb4b00a78bd` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 8.50999999986442 | 6.759999999866011 | 1.75 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-624f468d9eb4b00a78bd` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 26.73999999997568 | 9.82 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-624f468d9eb4b00a78bd` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 20.0 | 5 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-624f468d9eb4b00a78bd` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.32143019785677 | 88.67007446180125 | 4.34864 | 3.92393 | `r-cbc91d57fa8b8448b73b` | `r-a4145d96b399576cb221` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.729999999860581 | 10.029999999863037 | 2.7 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-a4145d96b399576cb221` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 27.0 | 3 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-8421b92b177ef9d45f0b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
