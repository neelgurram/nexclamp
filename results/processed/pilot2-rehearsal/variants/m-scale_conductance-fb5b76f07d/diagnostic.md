# m-scale_conductance-fb5b76f07d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "new": "0.2 mS_per_cm2", "old": "0.1 mS_per_cm2"}], "element": "channelDensity", "element_id": "LeakConductance_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='LeakConductance_all']", "attribute": "condDensity", "old": "0.1 mS_per_cm2", "new": "0.2 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1159.893 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.2988218828985024 | None |  | 0.0298822 | `r-3c4719e59bf2e9991e12` | `r-ed9386bb70440ebe36c2` |
| h/1 | P00_canonical | ahp_depth | definedness | 2.861194747922525 | None |  | 0.5 | `r-3c4719e59bf2e9991e12` | `r-ed9386bb70440ebe36c2` |
| h/1 | P00_canonical | ap_amplitude | definedness | 88.85420990112726 | None |  | 1.77708 | `r-3c4719e59bf2e9991e12` | `r-ed9386bb70440ebe36c2` |
| h/1 | P00_canonical | first_spike_latency | definedness | 20.749999999853287 | None |  | 0.5 | `r-3c4719e59bf2e9991e12` | `r-ed9386bb70440ebe36c2` |
| h/1 | P00_canonical | last_isi | definedness | 135.97999999987638 | None |  | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-ed9386bb70440ebe36c2` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 0.0 | 5 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-ed9386bb70440ebe36c2` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 1.1359196776176488 | 0.575268 | 0.011213 | `s-5f55d8b80c82db215fd9` | `s-f7c6c06bb7c80551d8cc` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.018020491828063687 | None |  | 0.01 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/1 | P04_step_2x | ahp_depth | definedness | 3.2025415878387236 | None |  | 1.22099 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 89.49588775782593 | None |  | 1.78992 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 10.689999999862437 | None |  | 0.5 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/1 | P04_step_2x | last_isi | definedness | 28.16999999997438 | None |  | 0.5634 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 0.0 | 22 | 0.5 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -89.3964946701052 | -79.76309131774924 | 9.6334 | 0.5 | `r-d38646e1b306607cd46b` | `r-c8c3caf949217231b9fa` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.2989579287624928 | None |  | 0.0298822 | `r-d4ef4781c8007010e9af` | `r-cde70cf4f08685578de9` |
| h/2 | P00_canonical | ahp_depth | definedness | 2.9394112752346615 | None |  | 0.5 | `r-d4ef4781c8007010e9af` | `r-cde70cf4f08685578de9` |
| h/2 | P00_canonical | ap_amplitude | definedness | 88.78027725318925 | None |  | 1.77708 | `r-d4ef4781c8007010e9af` | `r-cde70cf4f08685578de9` |
| h/2 | P00_canonical | first_spike_latency | definedness | 20.739999999853296 | None |  | 0.5 | `r-d4ef4781c8007010e9af` | `r-cde70cf4f08685578de9` |
| h/2 | P00_canonical | last_isi | definedness | 135.78999999987656 | None |  | 2.7196 | `r-d4ef4781c8007010e9af` | `r-cde70cf4f08685578de9` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 0.0 | 5 | 0.5 | `r-d4ef4781c8007010e9af` | `r-cde70cf4f08685578de9` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 1.1359196776176488 | 0.575268 | 0.011213 | `s-cb9ed586448108518164` | `s-89821edc17012c251234` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.018206269147133136 | None |  | 0.01 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |
| h/2 | P04_step_2x | ahp_depth | definedness | 3.6095391972804407 | None |  | 1.22099 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 89.44855880885186 | None |  | 1.78992 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 10.659999999862464 | None |  | 0.5 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |
| h/2 | P04_step_2x | last_isi | definedness | 28.06999999997447 | None |  | 0.5634 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 0.0 | 22 | 0.5 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -89.39649565734885 | -79.7630922973635 | 9.6334 | 0.5 | `r-e63ab2df48d3a768b131` | `r-ecc3c0800347ba3b8a3e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
