# m-shift_forward_rate_midpoint-8400d317d9

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='it']/ionChannel[@id='kv']/gate[@id='n']/forwardRate[1]", "new": "20mV", "old": "25mV"}], "channel": "kv", "delta_mV": -5.0, "gate": "n", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "NeuroML2/kv.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='kv']/gate[@id='n']/forwardRate[1]", "attribute": "midpoint", "old": "25mV", "new": "20mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2332.816 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-cc06a5423671e115f063` | `r-75d3afde2654fafeefba` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -68.14186175689683 | -68.76599568328842 | 0.624134 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-adc3fcd42ce05ed9e8b5` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.025817908612799673 | 0.00416638 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-e9cbbc414a487f45f020` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 17.979999999983647 | 0.7 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-adc3fcd42ce05ed9e8b5` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-adc3fcd42ce05ed9e8b5` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 12.27999999986099 | 1.6 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-e654a4b4e43b77942622` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 25.200000000550062 | 2.78 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-e654a4b4e43b77942622` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 80.0 | 9 | 3 | `r-1b9872d61cd35dd7d644` | `r-e654a4b4e43b77942622` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 530.5299999993897 | 127.44 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-7bcc845b8fbf9935f049` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 29.0 | 6 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-7bcc845b8fbf9935f049` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | -10.590716924034965 | 3.13032 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-c9f508eb99331fdf1b1d` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-731f49df5b3e5b386bce` | `r-092e7322ea5407e3a541` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -68.14186132202134 | -68.76599522399889 | 0.624134 | 0.5 | `r-935039983c3fcf534d52` | `r-63972aaaf4abdb7db2d4` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.025817908612799673 | 0.00416638 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-79832579ac1c83542f69` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 17.939999999983684 | 0.69 | 0.5 | `r-935039983c3fcf534d52` | `r-63972aaaf4abdb7db2d4` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 28.0 | 1 | 0.5 | `r-935039983c3fcf534d52` | `r-63972aaaf4abdb7db2d4` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 12.239999999861027 | 1.6 | 0.5 | `r-a7eb0be940e544905260` | `r-f036e012d5b23790f5ed` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 25.16000000054919 | 2.78 | 0.5 | `r-a7eb0be940e544905260` | `r-f036e012d5b23790f5ed` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 80.0 | 10 | 3 | `r-a7eb0be940e544905260` | `r-f036e012d5b23790f5ed` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 530.4399999993898 | 127.43 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-f29daacab95b2041bedf` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 29.0 | 6 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-f29daacab95b2041bedf` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -10.568485275267363 | 3.14162 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-9b9e1513a1e3e3a7b3f6` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
