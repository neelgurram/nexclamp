# m-scale_gate_time_constant-de97b02e71

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "new": "0.26125per_ms", "old": "0.209per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "new": "1.175per_ms", "old": "0.94per_ms"}], "channel": "Ca_HVA", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/forwardRate[1]", "attribute": "rate", "old": "0.209per_ms", "new": "0.26125per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "NMC/NeuroML2/Ca_HVA.channel.nml", "locator": "/neuroml[@id='Ca_HVA']/ionChannel[@id='Ca_HVA']/gate[@id='m']/reverseRate[1]", "attribute": "rate", "old": "0.94per_ms", "new": "1.175per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 12139.369 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 118.6600000025901 | 127.2500000027776 | 8.59 | 2.3732 | `r-a413bdc9ef17abaeb327` | `r-08ea8f23288a8448e79d` |
| h/1 | P05_long_step | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-08ea8f23288a8448e79d` |
| h/2 | P05_long_step | last_isi | exceeds | 118.89000000259512 | 127.41000000278109 | 8.52 | 2.3732 | `r-019eab9c744398314e93` | `r-1546b6c6ba113e2022d0` |
| h/2 | P05_long_step | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-019eab9c744398314e93` | `r-1546b6c6ba113e2022d0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
