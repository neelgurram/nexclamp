# m-shift_gate_midpoint-7f017f2908

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/forwardRate[1]", "new": "-25mV", "old": "-30mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/reverseRate[1]", "new": "-25mV", "old": "-30mV"}], "channel": "km", "delta_mV": 5.0, "gate": "n", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "NeuroML2/km.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/forwardRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-25mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NeuroML2/km.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/reverseRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-25mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 5259.225 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.019739088860050543 | 0.00191244 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-ed1f93252959628f94a9` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-3240c6fd094cb04a2388` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 21.360000000466243 | 1.06 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-4d7f2cfb585179b27094` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 94.0 | 5 | 3 | `r-1b9872d61cd35dd7d644` | `r-4d7f2cfb585179b27094` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 351.13999999955286 | 51.95 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-235f695ba9ecd22362fc` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 38.0 | 3 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-235f695ba9ecd22362fc` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.019739088860050543 | 0.00191244 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-159b64990e3dd7a1c134` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-935039983c3fcf534d52` | `r-a53663df0017321b35f7` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 21.32000000046537 | 1.06 | 0.5 | `r-a7eb0be940e544905260` | `r-a85f1a983e06f91729fb` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 94.0 | 4 | 3 | `r-a7eb0be940e544905260` | `r-a85f1a983e06f91729fb` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 351.0699999995529 | 51.94 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-4b79b9872fea0867ee41` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 38.0 | 3 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-4b79b9872fea0867ee41` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
