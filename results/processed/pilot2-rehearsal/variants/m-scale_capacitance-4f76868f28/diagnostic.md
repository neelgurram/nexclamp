# m-scale_capacitance-4f76868f28

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1158.162 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.330285848157983 | 0.031464 | 0.0298822 | `r-3c4719e59bf2e9991e12` | `r-7171ccc8c27078707c24` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 0.08477917225935983 | 2.77642 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-7171ccc8c27078707c24` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 20.749999999853287 | 16.67999999985699 | 4.07 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-7171ccc8c27078707c24` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 130.10999999988172 | 5.87 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-7171ccc8c27078707c24` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 0.464685005186098 | 2.73786 | 1.22099 | `r-d38646e1b306607cd46b` | `r-877a13d441a68de28971` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 10.689999999862437 | 8.639999999864301 | 2.05 | 0.5 | `r-d38646e1b306607cd46b` | `r-877a13d441a68de28971` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 25.379999999976917 | 2.79 | 0.5634 | `r-d38646e1b306607cd46b` | `r-877a13d441a68de28971` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 24.0 | 2 | 0.5 | `r-d38646e1b306607cd46b` | `r-877a13d441a68de28971` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.33035668697612197 | 0.0313988 | 0.0298822 | `r-d4ef4781c8007010e9af` | `r-34dd11f1f6610f1bae45` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 0.16628396606887463 | 2.77313 | 0.5 | `r-d4ef4781c8007010e9af` | `r-34dd11f1f6610f1bae45` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 20.739999999853296 | 16.669999999856998 | 4.07 | 0.5 | `r-d4ef4781c8007010e9af` | `r-34dd11f1f6610f1bae45` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 129.9199999998819 | 5.87 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-34dd11f1f6610f1bae45` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 0.8881239369697767 | 2.72142 | 1.22099 | `r-e63ab2df48d3a768b131` | `r-57024df742a9cf9e383d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 10.659999999862464 | 8.609999999864328 | 2.05 | 0.5 | `r-e63ab2df48d3a768b131` | `r-57024df742a9cf9e383d` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 25.30999999997698 | 2.76 | 0.5634 | `r-e63ab2df48d3a768b131` | `r-57024df742a9cf9e383d` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 24.0 | 2 | 0.5 | `r-e63ab2df48d3a768b131` | `r-57024df742a9cf9e383d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
