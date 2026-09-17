# m-scale_capacitance-ed0bebd0d7

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1177.658 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | -5.570929758721462 | 8.43212 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-08f6da33ee512f51ff87` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.85420990112726 | 92.17206192133324 | 3.31785 | 1.77708 | `r-3c4719e59bf2e9991e12` | `r-08f6da33ee512f51ff87` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 20.749999999853287 | 10.569999999862546 | 10.18 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-08f6da33ee512f51ff87` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 142.6599999998703 | 6.68 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-08f6da33ee512f51ff87` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-08f6da33ee512f51ff87` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | -5.095107182822687 | 8.29765 | 1.22099 | `r-d38646e1b306607cd46b` | `r-f3a9e13b176edb6b1f9b` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.49588775782593 | 93.0271301279322 | 3.53124 | 1.78992 | `r-d38646e1b306607cd46b` | `r-f3a9e13b176edb6b1f9b` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 10.689999999862437 | 5.5499999998671115 | 5.14 | 0.5 | `r-d38646e1b306607cd46b` | `r-f3a9e13b176edb6b1f9b` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 20.729999999981146 | 7.44 | 0.5634 | `r-d38646e1b306607cd46b` | `r-f3a9e13b176edb6b1f9b` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 29.0 | 7 | 0.5 | `r-d38646e1b306607cd46b` | `r-f3a9e13b176edb6b1f9b` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | -5.485129592895504 | 8.42454 | 0.5 | `r-d4ef4781c8007010e9af` | `r-27c37db5ab8f2dec46e7` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.78027725318925 | 92.11871337970322 | 3.33844 | 1.77708 | `r-d4ef4781c8007010e9af` | `r-27c37db5ab8f2dec46e7` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 20.739999999853296 | 10.559999999862555 | 10.18 | 0.5 | `r-d4ef4781c8007010e9af` | `r-27c37db5ab8f2dec46e7` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 142.61999999987034 | 6.83 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-27c37db5ab8f2dec46e7` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 6.0 | 1 | 0.5 | `r-d4ef4781c8007010e9af` | `r-27c37db5ab8f2dec46e7` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | -4.648146822617235 | 8.25769 | 1.22099 | `r-e63ab2df48d3a768b131` | `r-b8892cc78136da996120` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 92.98125457927522 | 3.5327 | 1.78992 | `r-e63ab2df48d3a768b131` | `r-b8892cc78136da996120` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 10.659999999862464 | 5.52999999986713 | 5.13 | 0.5 | `r-e63ab2df48d3a768b131` | `r-b8892cc78136da996120` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 20.719999999981155 | 7.35 | 0.5634 | `r-e63ab2df48d3a768b131` | `r-b8892cc78136da996120` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 30.0 | 8 | 0.5 | `r-e63ab2df48d3a768b131` | `r-b8892cc78136da996120` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
