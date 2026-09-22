# m-shift_reversal-018c346f67

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='km_all']", "new": "-85 mV", "old": "-90 mV"}], "element": "channelDensity", "element_id": "km_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='km_all']", "attribute": "erev", "old": "-90 mV", "new": "-85 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 5434.181 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.020900211734171163 | 0.000751315 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-0463889f13ded522fa40` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-c5136b17a5e6ae4afa2a` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 21.79000000047563 | 0.63 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-e4df2cafa77b2033cdbf` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 383.14999999952374 | 19.94 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-267f8fedff6aefb964a6` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-267f8fedff6aefb964a6` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.020900211734171163 | 0.000751315 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-3141f07d83066bdab517` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 30.0 | 1 | 0.5 | `r-935039983c3fcf534d52` | `r-54e3364f622708b20417` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 21.750000000474756 | 0.63 | 0.5 | `r-a7eb0be940e544905260` | `r-feea36e286c694fa0c1b` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 383.0699999995238 | 19.94 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-c2e68203ad9d18aad6d5` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 37.0 | 2 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-c2e68203ad9d18aad6d5` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
