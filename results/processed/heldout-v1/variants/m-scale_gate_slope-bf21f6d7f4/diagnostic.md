# m-scale_gate_slope-bf21f6d7f4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/forwardRate[1]", "new": "11.25mV", "old": "9mV"}, {"attribute": "scale", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/reverseRate[1]", "new": "-11.25mV", "old": "-9mV"}], "channel": "km", "factor": 1.25, "gate": "n", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "NeuroML2/km.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/forwardRate[1]", "attribute": "scale", "old": "9mV", "new": "11.25mV", "action": "set", "note": "scale_gate_slope"}, {"file": "NeuroML2/km.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='km']/gate[@id='n']/reverseRate[1]", "attribute": "scale", "old": "-9mV", "new": "-11.25mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2224.997 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 16.059999999985394 | 0.54 | 0.5 | `r-cc06a5423671e115f063` | `r-7549894552a74bda75d8` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-cc06a5423671e115f063` | `r-7549894552a74bda75d8` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -68.14186175689683 | -69.31676047973617 | 1.1749 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-9c8b55c547f24a6bfded` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.025169045830202855 | 0.00351752 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-f34d7ac20ccabc164bd8` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 18.149999999983493 | 0.87 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-9c8b55c547f24a6bfded` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-9c8b55c547f24a6bfded` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 12.069999999861182 | 1.39 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-7eb680ffe482461c5d6c` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 25.700000000560976 | 3.28 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-7eb680ffe482461c5d6c` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 78.0 | 11 | 3 | `r-1b9872d61cd35dd7d644` | `r-7eb680ffe482461c5d6c` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 513.649999999405 | 110.56 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-8d51ca8a7658e26888a5` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 29.0 | 6 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-8d51ca8a7658e26888a5` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 16.049999999985403 | 0.54 | 0.5 | `r-731f49df5b3e5b386bce` | `r-6a45e19c63de34ba6efd` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-731f49df5b3e5b386bce` | `r-6a45e19c63de34ba6efd` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -68.14186132202134 | -69.31675994720445 | 1.1749 | 0.5 | `r-935039983c3fcf534d52` | `r-38965d212e3bb1e25751` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.025169045830202855 | 0.00351752 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-c82e135be70d34c271c0` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 18.10999999998353 | 0.86 | 0.5 | `r-935039983c3fcf534d52` | `r-38965d212e3bb1e25751` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-935039983c3fcf534d52` | `r-38965d212e3bb1e25751` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 12.029999999861218 | 1.39 | 0.5 | `r-a7eb0be940e544905260` | `r-d465e830351df9c1c3a9` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 25.650000000559885 | 3.27 | 0.5 | `r-a7eb0be940e544905260` | `r-d465e830351df9c1c3a9` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 78.0 | 12 | 3 | `r-a7eb0be940e544905260` | `r-d465e830351df9c1c3a9` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 513.5599999994051 | 110.55 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-42dda063de5dd539d393` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 30.0 | 5 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-42dda063de5dd539d393` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
