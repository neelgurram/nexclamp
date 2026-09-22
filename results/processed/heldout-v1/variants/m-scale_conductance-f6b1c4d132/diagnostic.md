# m-scale_conductance-f6b1c4d132

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "new": "0.00011428 S_per_cm2", "old": "0.00014285 S_per_cm2"}], "element": "channelDensity", "element_id": "pas_all", "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "attribute": "condDensity", "old": "0.00014285 S_per_cm2", "new": "0.00011428 S_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 5368.714 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -68.14186175689683 | -66.87114409027086 | 1.27072 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-533082787175337c14ec` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.01769004849395533 | 0.00396148 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-d37051d1e6f67a4c79b5` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 7.069999999865729 | 6.549999999866202 | 0.52 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-533082787175337c14ec` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 16.539999999984957 | 0.74 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-533082787175337c14ec` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-533082787175337c14ec` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 9.329999999863674 | 1.35 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-e901e7fbe0a4696d0a3b` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 20.490000000447253 | 1.93 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-e901e7fbe0a4696d0a3b` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 98.0 | 9 | 3 | `r-1b9872d61cd35dd7d644` | `r-e901e7fbe0a4696d0a3b` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 324.29999999957727 | 78.79 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-4607efedc8c0b7e192ef` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 40.0 | 5 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-4607efedc8c0b7e192ef` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -92.45854733276396 | -96.80814167480497 | 4.34959 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-533082787175337c14ec` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -68.14186132202134 | -66.87114354248033 | 1.27072 | 0.5 | `r-935039983c3fcf534d52` | `r-af12dee4c3cb133589e2` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.01769004849395533 | 0.00396148 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-ee5b792760e0b5c91d6b` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.029999999865765 | 6.519999999866229 | 0.51 | 0.5 | `r-935039983c3fcf534d52` | `r-af12dee4c3cb133589e2` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 16.509999999984984 | 0.74 | 0.5 | `r-935039983c3fcf534d52` | `r-af12dee4c3cb133589e2` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-935039983c3fcf534d52` | `r-af12dee4c3cb133589e2` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 9.2999999998637 | 1.34 | 0.5 | `r-a7eb0be940e544905260` | `r-fe27ee0eb4aac58c7bdf` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 20.4600000004466 | 1.92 | 0.5 | `r-a7eb0be940e544905260` | `r-fe27ee0eb4aac58c7bdf` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 98.0 | 8 | 3 | `r-a7eb0be940e544905260` | `r-fe27ee0eb4aac58c7bdf` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 324.22999999957733 | 78.78 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-b33322b224cd5364e4ff` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 40.0 | 5 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-b33322b224cd5364e4ff` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -92.45854857788115 | -96.80814291839629 | 4.34959 | 0.5 | `r-935039983c3fcf534d52` | `r-af12dee4c3cb133589e2` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -10.22533586374081 | 3.48477 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-3f65292f6059b2d49382` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
