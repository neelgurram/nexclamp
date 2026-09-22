# m-scale_gate_time_constant-97ff619aea

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "it", "factor": 0.5, "gate": "h", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/it.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='it']/gate[@id='h']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"0.5\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 5516.653 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.022368690663206067 | 0.000717164 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-24c5eae5e37ce68ba598` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 389.19999999951824 | 13.89 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-38fa85c0261a860b13a2` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-38fa85c0261a860b13a2` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.022368690663206067 | 0.000717164 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-aa66a7f31b3ce9cfb57e` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 389.1299999995183 | 13.88 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-945f80b69f62599872e0` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-945f80b69f62599872e0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
