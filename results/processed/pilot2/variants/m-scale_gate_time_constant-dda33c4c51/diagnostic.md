# m-scale_gate_time_constant-dda33c4c51

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Kd", "factor": 0.8, "gate": "n", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Kd/Kd.channel.nml", "locator": "/neuroml[@id='Kd']/ionChannel[@id='Kd']/gate[@id='n']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"0.8\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1348.685 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -6.100250244136205 | 1.26794 | 0.5 | `r-4cceac4cec0eb866659f` | `r-a116dc3d73e13b2a52fc` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 20.729999999981146 | 0.51 | 0.5 | `r-4cceac4cec0eb866659f` | `r-a116dc3d73e13b2a52fc` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 19.0 | 1 | 0.5 | `r-4cceac4cec0eb866659f` | `r-a116dc3d73e13b2a52fc` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 124.0 | 4 | 3 | `r-d95212df9ca6b2b4efff` | `r-8b9541ca34ee6103c12b` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 58.0 | 3 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-24c392824b26e1eeefc5` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | -4.687477111816406 | 8.1613 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-49d9fdb7537e2dd265cb` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -6.0126113891712265 | 1.27793 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-7d3a2902d2f69dae8864` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 20.709999999981164 | 0.52 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-7d3a2902d2f69dae8864` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 19.0 | 1 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-7d3a2902d2f69dae8864` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 125.0 | 4 | 3 | `r-880359fc85650f897997` | `r-94e280f7a428324812f0` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 59.0 | 2 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-84f4eefb06503949ef7f` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | -4.14154052734294 | 8.18388 | 1.70556 | `r-84e85309a66928a29934` | `r-5502d129997dd0a6829a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
