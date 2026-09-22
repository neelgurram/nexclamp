# m-scale_gate_time_constant-02eb4e0b90

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "new": "0.26125per_ms", "old": "0.209per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "new": "1.175per_ms", "old": "0.94per_ms"}], "channel": "Ca_HVA", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "attribute": "rate", "old": "0.209per_ms", "new": "0.26125per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "neuroConstruct/generatedNeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "attribute": "rate", "old": "0.94per_ms", "new": "1.175per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 10787.712 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 142.97000000312073 | 153.4100000033486 | 10.44 | 3.03 | `r-b99907e8e6510bd22247` | `r-fa9e902cc0d05131563a` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-b99907e8e6510bd22247` | `r-fa9e902cc0d05131563a` |
| h/2 | P05_long_step | last_isi | exceeds | 143.98000000314278 | 154.36000000336935 | 10.38 | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-1c8c55be264e3d964924` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 13.0 | 1 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-1c8c55be264e3d964924` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
