# m-shift_gate_midpoint-5b359c9cfa

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='it']/ionChannel[@id='it']/gate[@id='h']/steadyState[1]", "new": "-88mV", "old": "-78mV"}], "channel": "it", "delta_mV": -10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "NeuroML2/it.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='it']/gate[@id='h']/steadyState[1]", "attribute": "midpoint", "old": "-78mV", "new": "-88mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2264.676 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-cc06a5423671e115f063` | `r-eedb70c949b1f1a39c93` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.02421282699269176 | 0.0025613 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-11476ba1165f6e42446d` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 441.6699999994705 | 38.58 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-2ece4000419b8931de86` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 34.0 | 1 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-2ece4000419b8931de86` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-731f49df5b3e5b386bce` | `r-c2f7951cdcee606bf712` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.02421282699269176 | 0.0025613 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-7e969955755bbf594de9` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 441.5899999994706 | 38.58 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-59fa017f271bf4131cba` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 34.0 | 1 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-59fa017f271bf4131cba` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
