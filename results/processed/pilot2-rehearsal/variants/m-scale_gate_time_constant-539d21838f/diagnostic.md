# m-scale_gate_time_constant-539d21838f

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Kd", "factor": 0.8, "gate": "n", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Kd/Kd.channel.nml", "locator": "/neuroml[@id='Kd']/ionChannel[@id='Kd']/gate[@id='n']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"0.8\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1197.942 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 0.9585610809292007 | 1.90263 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-d5c044f951fbb35a69ab` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 164.74999999985022 | 28.77 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-d5c044f951fbb35a69ab` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 1.453510520931431 | 1.74903 | 1.22099 | `r-d38646e1b306607cd46b` | `r-b135bceb066175728c44` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 30.109999999972615 | 1.94 | 0.5634 | `r-d38646e1b306607cd46b` | `r-b135bceb066175728c44` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 20.0 | 2 | 0.5 | `r-d38646e1b306607cd46b` | `r-b135bceb066175728c44` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 1.0299264119488925 | 1.90948 | 0.5 | `r-d4ef4781c8007010e9af` | `r-79327e2c094241b37f09` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 164.6499999998503 | 28.86 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-79327e2c094241b37f09` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 1.825367139179221 | 1.78417 | 1.22099 | `r-e63ab2df48d3a768b131` | `r-aa5cf77e8a9f282043d5` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 30.029999999972688 | 1.96 | 0.5634 | `r-e63ab2df48d3a768b131` | `r-aa5cf77e8a9f282043d5` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 20.0 | 2 | 0.5 | `r-e63ab2df48d3a768b131` | `r-aa5cf77e8a9f282043d5` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
