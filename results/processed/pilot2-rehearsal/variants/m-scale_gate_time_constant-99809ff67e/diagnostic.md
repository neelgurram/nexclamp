# m-scale_gate_time_constant-99809ff67e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL_REHEARSAL | designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything*

- model: `pospischil2008_rs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Na", "factor": 2.0, "gate": "h", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='h']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1175.499 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.2988218828985024 | 0.16385878423910816 | 0.134963 | 0.0298822 | `r-3c4719e59bf2e9991e12` | `r-de57eb8114fc15fa1bb2` |
| h/1 | P00_canonical | ahp_depth | exceeds | 2.861194747922525 | 6.563221115114558 | 3.70203 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-de57eb8114fc15fa1bb2` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 88.85420990112726 | 83.63755035514475 | 5.21666 | 1.77708 | `r-3c4719e59bf2e9991e12` | `r-de57eb8114fc15fa1bb2` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 112.09999999989805 | 23.88 | 2.7196 | `r-3c4719e59bf2e9991e12` | `r-de57eb8114fc15fa1bb2` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-3c4719e59bf2e9991e12` | `r-de57eb8114fc15fa1bb2` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 3.2025415878387236 | 6.8499262313850195 | 3.64738 | 1.22099 | `r-d38646e1b306607cd46b` | `r-740a10fcf6c9903ec8a6` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.49588775782593 | 84.71452331685443 | 4.78136 | 1.78992 | `r-d38646e1b306607cd46b` | `r-740a10fcf6c9903ec8a6` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 23.489999999978636 | 4.68 | 0.5634 | `r-d38646e1b306607cd46b` | `r-740a10fcf6c9903ec8a6` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 26.0 | 4 | 0.5 | `r-d38646e1b306607cd46b` | `r-740a10fcf6c9903ec8a6` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.2989579287624928 | 0.163881624295786 | 0.135076 | 0.0298822 | `r-d4ef4781c8007010e9af` | `r-633e0ea2e73afd62d957` |
| h/2 | P00_canonical | ahp_depth | exceeds | 2.9394112752346615 | 6.657032124837244 | 3.71762 | 0.5 | `r-d4ef4781c8007010e9af` | `r-633e0ea2e73afd62d957` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 88.78027725318925 | 83.62856292805839 | 5.15171 | 1.77708 | `r-d4ef4781c8007010e9af` | `r-633e0ea2e73afd62d957` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 111.77999999989834 | 24.01 | 2.7196 | `r-d4ef4781c8007010e9af` | `r-633e0ea2e73afd62d957` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 7.0 | 2 | 0.5 | `r-d4ef4781c8007010e9af` | `r-633e0ea2e73afd62d957` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 3.6095391972804407 | 7.34644334157138 | 3.7369 | 1.22099 | `r-e63ab2df48d3a768b131` | `r-d0386948b14197fd4879` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 84.49725341944621 | 4.95131 | 1.78992 | `r-e63ab2df48d3a768b131` | `r-d0386948b14197fd4879` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 23.279999999978827 | 4.79 | 0.5634 | `r-e63ab2df48d3a768b131` | `r-d0386948b14197fd4879` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 26.0 | 4 | 0.5 | `r-e63ab2df48d3a768b131` | `r-d0386948b14197fd4879` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
