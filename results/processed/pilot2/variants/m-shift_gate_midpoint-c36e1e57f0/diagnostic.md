# m-shift_gate_midpoint-c36e1e57f0

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/forwardRate[1]", "new": "-60mV", "old": "-70mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/reverseRate[1]", "new": "-60mV", "old": "-70mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/steadyState[1]", "new": "-31.7mV", "old": "-41.7mV"}], "channel": "kamt", "delta_mV": 10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"}`
- recorded edits: `[{"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/forwardRate[1]", "attribute": "midpoint", "old": "-70mV", "new": "-60mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/reverseRate[1]", "attribute": "midpoint", "old": "-70mV", "new": "-60mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='h']/steadyState[1]", "attribute": "midpoint", "old": "-41.7mV", "new": "-31.7mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3882.735 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 117.75000000257023 | 5.11 | 2.2528 | `r-2e016fe90119b688bc84` | `r-47b8f00f69bd51377150` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 18.0 | 1 | 0.5 | `r-2e016fe90119b688bc84` | `r-47b8f00f69bd51377150` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 417.53999999949247 | 16.81 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-8a94a4fa829c0c2d73e3` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-0cd5f319bb80295395e1` | `r-8a94a4fa829c0c2d73e3` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 117.72000000256958 | 5.1 | 2.2528 | `r-002bf860824963a1f621` | `r-f696d0ba42341e534afb` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 18.0 | 1 | 0.5 | `r-002bf860824963a1f621` | `r-f696d0ba42341e534afb` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 417.4899999994925 | 16.81 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-d00c373d4196fab32999` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-d00c373d4196fab32999` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
