# m-scale_conductance-3136c4d394

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "new": "0.0002857 S_per_cm2", "old": "0.00014285 S_per_cm2"}], "element": "channelDensity", "element_id": "pas_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "attribute": "condDensity", "old": "0.00014285 S_per_cm2", "new": "0.0002857 S_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2301.673 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 108.20782089620715 | 105.89248657436934 | 2.31533 | 2.16416 | `r-cc06a5423671e115f063` | `r-56931e0513d7d58ff529` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 205.8799999998668 | 210.2799999998628 | 4.4 | 4.1176 | `r-cc06a5423671e115f063` | `r-56931e0513d7d58ff529` |
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 22.579999999979464 | 7.06 | 0.5 | `r-cc06a5423671e115f063` | `r-56931e0513d7d58ff529` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 5.0 | 2 | 0.5 | `r-cc06a5423671e115f063` | `r-56931e0513d7d58ff529` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -68.14186175689683 | -71.23184580230699 | 3.08998 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.042551738269243904 | 0.0209002 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-7bed3045388d7d04f926` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.00011161243381631631 | None |  | 0.01 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 108.29823684909732 | 104.63276672281748 | 3.66547 | 2.16596 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 7.069999999865729 | 21.519999999852587 | 14.45 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/1 | P04_step_2x | last_isi | definedness | 17.279999999984284 | None |  | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 1.0 | 28 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/1 | P05_long_step | adaptation_index | definedness | 8.6211619823114e-05 | None |  | 0.01 | `r-1b9872d61cd35dd7d644` | `r-40ca128526166b3a63c0` |
| h/1 | P05_long_step | ahp_depth | definedness | -13.077251073198525 | None |  | 0.653863 | `r-1b9872d61cd35dd7d644` | `r-40ca128526166b3a63c0` |
| h/1 | P05_long_step | ap_amplitude | definedness | 107.47266006221963 | None |  | 2.14945 | `r-1b9872d61cd35dd7d644` | `r-40ca128526166b3a63c0` |
| h/1 | P05_long_step | first_spike_latency | definedness | 10.679999999862446 | None |  | 0.5 | `r-1b9872d61cd35dd7d644` | `r-40ca128526166b3a63c0` |
| h/1 | P05_long_step | last_isi | definedness | 22.42000000048938 | None |  | 0.5 | `r-1b9872d61cd35dd7d644` | `r-40ca128526166b3a63c0` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 0.0 | 89 | 3 | `r-1b9872d61cd35dd7d644` | `r-40ca128526166b3a63c0` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 826.9899999991201 | 423.9 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-c6e861db0de0a0c0f136` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 10.0 | 25 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-c6e861db0de0a0c0f136` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -92.45854733276396 | -83.79374032592803 | 8.66481 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-530ffe7b12a97f8512aa` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 108.25350570834362 | 105.86882400637025 | 2.38468 | 2.16416 | `r-731f49df5b3e5b386bce` | `r-ecdc96252c96c5025cf1` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 205.86999999986682 | 210.26999999986282 | 4.4 | 4.1176 | `r-731f49df5b3e5b386bce` | `r-ecdc96252c96c5025cf1` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 22.569999999979473 | 7.06 | 0.5 | `r-731f49df5b3e5b386bce` | `r-ecdc96252c96c5025cf1` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 5.0 | 2 | 0.5 | `r-731f49df5b3e5b386bce` | `r-ecdc96252c96c5025cf1` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -68.14186132202134 | -71.23184519195543 | 3.08998 | 0.5 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.042551738269243904 | 0.0209002 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-3c76a8d52de040ab9baa` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.0001230236486784441 | None |  | 0.01 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 107.95729445905641 | 104.05185318418799 | 3.90544 | 2.16596 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.029999999865765 | 21.44999999985265 | 14.42 | 0.5 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |
| h/2 | P04_step_2x | last_isi | definedness | 17.24999999998431 | None |  | 0.5 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 1.0 | 28 | 0.5 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |
| h/2 | P05_long_step | adaptation_index | definedness | 8.798113045873893e-05 | None |  | 0.01 | `r-a7eb0be940e544905260` | `r-72e5a6992762676d7704` |
| h/2 | P05_long_step | ahp_depth | definedness | -13.06868377939648 | None |  | 0.653863 | `r-a7eb0be940e544905260` | `r-72e5a6992762676d7704` |
| h/2 | P05_long_step | ap_amplitude | definedness | 107.05286025670158 | None |  | 2.14945 | `r-a7eb0be940e544905260` | `r-72e5a6992762676d7704` |
| h/2 | P05_long_step | first_spike_latency | definedness | 10.639999999862482 | None |  | 0.5 | `r-a7eb0be940e544905260` | `r-72e5a6992762676d7704` |
| h/2 | P05_long_step | last_isi | definedness | 22.380000000488508 | None |  | 0.5 | `r-a7eb0be940e544905260` | `r-72e5a6992762676d7704` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 0.0 | 90 | 3 | `r-a7eb0be940e544905260` | `r-72e5a6992762676d7704` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 826.8799999991202 | 423.87 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-82e76341c1113422aade` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 10.0 | 25 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-82e76341c1113422aade` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -92.45854857788115 | -83.79374153289824 | 8.66481 | 0.5 | `r-935039983c3fcf534d52` | `r-faf7dc37f1ea87bcf10f` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
