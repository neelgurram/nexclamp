# m-shift_reversal-f753277a7b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na_all']", "new": "70 mV", "old": "60 mV"}], "element": "channelDensity", "element_id": "na_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na_all']", "attribute": "erev", "old": "60 mV", "new": "70 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2312.764 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 108.20782089620715 | 118.0491676370368 | 9.84135 | 2.16416 | `r-cc06a5423671e115f063` | `r-73ee1fd09165a5cac37b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.021002663752475923 | 0.000648863 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-699e0d4c115420fa78b8` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 108.29823684909732 | 118.33782577661356 | 10.0396 | 2.16596 | `r-d2cafd1fc897dbfd8130` | `r-8555382b9b74a429538d` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 107.47266006221963 | 117.35036468604868 | 9.8777 | 2.14945 | `r-1b9872d61cd35dd7d644` | `r-b4a7fdf21b18d5ac5b94` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 384.2699999995227 | 18.82 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-d4e54bad833223955736` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-d4e54bad833223955736` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | -10.882960128784774 | 2.83807 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-efeace36964ef4a3a785` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 134.16434859879257 | 143.82170104296807 | 9.65735 | 2.68329 | `r-83f9184aaeefc65499cb` | `r-efeace36964ef4a3a785` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 108.25350570834362 | 117.95969009462395 | 9.70618 | 2.16416 | `r-731f49df5b3e5b386bce` | `r-2a657e4af32b627737ae` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.021002663752475923 | 0.000648863 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-d131dc4a20943b9457c5` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 107.95729445905641 | 117.71419142818229 | 9.7569 | 2.16596 | `r-935039983c3fcf534d52` | `r-d2ca72f02162bc21dc6e` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 107.05286025670158 | 116.85311126681437 | 9.80025 | 2.14945 | `r-a7eb0be940e544905260` | `r-9b3e1c949c3fd031fcb6` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 384.1999999995228 | 18.81 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-e2d8040811eb4580a890` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 36.0 | 1 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-e2d8040811eb4580a890` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -10.859378196710736 | 2.85073 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-33ea674f3251ef44e84c` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 133.76337051196737 | 143.29953765533668 | 9.53617 | 2.68329 | `r-dc583bb05cf4bf59d02c` | `r-33ea674f3251ef44e84c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
