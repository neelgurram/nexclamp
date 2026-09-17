# m-shift_reversal-93e4e5a5cc

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "new": "40.0 mV", "old": "50.0 mV"}], "element": "channelDensityVShift", "element_id": "Na_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensityVShift[@id='Na_all']", "attribute": "erev", "old": "50.0 mV", "new": "40.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1192.137 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.18879883718470647 | 0.110023 | 0.0298822 | `r-3c4719e59bf2e9991e12` | `r-b9dd612d7b60a05aa643` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 4.537426577251296 | 1.67623 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-b9dd612d7b60a05aa643` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.85420990112726 | 78.9657630936381 | 9.88845 | 1.77708 | `r-3c4719e59bf2e9991e12` | `r-b9dd612d7b60a05aa643` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 20.749999999853287 | 21.259999999852823 | 0.51 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-b9dd612d7b60a05aa643` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 102.38999999990693 | 33.59 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-b9dd612d7b60a05aa643` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-b9dd612d7b60a05aa643` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 4.944561709096746 | 1.74202 | 1.22099 | `r-d38646e1b306607cd46b` | `r-f266dab3e100966aa63b` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.49588775782593 | 79.56398391831263 | 9.9319 | 1.78992 | `r-d38646e1b306607cd46b` | `r-f266dab3e100966aa63b` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 24.359999999977845 | 3.81 | 0.5634 | `r-d38646e1b306607cd46b` | `r-f266dab3e100966aa63b` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 25.0 | 3 | 0.5 | `r-d38646e1b306607cd46b` | `r-f266dab3e100966aa63b` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.18892169869334188 | 0.110036 | 0.0298822 | `r-d4ef4781c8007010e9af` | `r-ec722549464b8120bca2` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 4.613735771174646 | 1.67432 | 0.5 | `r-d4ef4781c8007010e9af` | `r-ec722549464b8120bca2` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.78027725318925 | 78.90426635884708 | 9.87601 | 1.77708 | `r-d4ef4781c8007010e9af` | `r-ec722549464b8120bca2` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 20.739999999853296 | 21.249999999852832 | 0.51 | 0.5 | `r-d4ef4781c8007010e9af` | `r-ec722549464b8120bca2` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 102.27999999990703 | 33.51 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-ec722549464b8120bca2` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-d4ef4781c8007010e9af` | `r-ec722549464b8120bca2` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 5.341885253904124 | 1.73235 | 1.22099 | `r-e63ab2df48d3a768b131` | `r-78c92db6a5bc61ba00b4` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 79.5375709544143 | 9.91099 | 1.78992 | `r-e63ab2df48d3a768b131` | `r-78c92db6a5bc61ba00b4` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 24.259999999977936 | 3.81 | 0.5634 | `r-e63ab2df48d3a768b131` | `r-78c92db6a5bc61ba00b4` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 25.0 | 3 | 0.5 | `r-e63ab2df48d3a768b131` | `r-78c92db6a5bc61ba00b4` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
