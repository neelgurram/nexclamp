# m-duplicate_conductance-328cf062a2

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "Na_all_dup", "source_id": "Na_all"}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"50.0 mS_per_cm2\" id=\"Na_all_dup\" ionChannel=\"Na\" ion=\"na\" erev=\"50.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1043.898 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -6.857032775887603 | 2.02473 | 0.5 | `r-4cceac4cec0eb866659f` | `r-f07d0448402c3c165e38` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 87.45660400498362 | 92.25548935063989 | 4.79889 | 1.74913 | `r-4cceac4cec0eb866659f` | `r-f07d0448402c3c165e38` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 14.529999999858944 | 2.67 | 0.5 | `r-4cceac4cec0eb866659f` | `r-f07d0448402c3c165e38` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 18.10999999998353 | 2.11 | 0.5 | `r-4cceac4cec0eb866659f` | `r-f07d0448402c3c165e38` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 22.0 | 2 | 0.5 | `r-4cceac4cec0eb866659f` | `r-f07d0448402c3c165e38` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.35612321562734783 | 0.0281743 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-7aa60f0ca34ea3b1ccf1` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -6.603492736805833 | 1.99059 | 1.51774 | `r-54e05e4e4388308e9268` | `r-0528428126c4a6be3352` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 88.51488494896842 | 92.85311508331876 | 4.33823 | 1.7703 | `r-54e05e4e4388308e9268` | `r-0528428126c4a6be3352` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 7.259999999865556 | 0.75 | 0.5 | `r-54e05e4e4388308e9268` | `r-0528428126c4a6be3352` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -7.2779235839769285 | 1.95379 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-c89c6f3f4ab154089142` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.90636062789724 | 92.48564529508985 | 4.57928 | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-c89c6f3f4ab154089142` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 11.119999999862046 | 1.55 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-c89c6f3f4ab154089142` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 14.560000000317814 | 1.05 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-c89c6f3f4ab154089142` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 137.0 | 9 | 3 | `r-d95212df9ca6b2b4efff` | `r-c89c6f3f4ab154089142` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 363.4899999995416 | 338.6899999995642 | 24.8 | 7.2698 | `r-5888f8cf54a64bb2eb2f` | `r-4b0180f56f21cbb75ab2` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 63.0 | 2 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-4b0180f56f21cbb75ab2` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | 1.2291259765387963 | 2.2447 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-70e51ce26fc57bd4fbba` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -6.770141601555977 | 2.03546 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-a2a3f6e0698693710f3b` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 87.36877822947855 | 92.20054626562556 | 4.83177 | 1.74913 | `r-c9243a4c0b8a67de36a8` | `r-a2a3f6e0698693710f3b` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 17.189999999856525 | 14.519999999858953 | 2.67 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-a2a3f6e0698693710f3b` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 18.089999999983547 | 2.1 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-a2a3f6e0698693710f3b` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 22.0 | 2 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-a2a3f6e0698693710f3b` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.35612321562734783 | 0.0281743 | 0.00768595 | `s-a5d560731591d7405a9c` | `s-2bf8323f074b7de33a19` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | -6.153953552244431 | 2.04696 | 1.51774 | `r-e087238cb438e653e31d` | `r-260d77eb653ab7ec597a` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 88.43542480636255 | 92.7989768995833 | 4.36355 | 1.7703 | `r-e087238cb438e653e31d` | `r-260d77eb653ab7ec597a` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.989999999864892 | 7.2299999998655835 | 0.76 | 0.5 | `r-e087238cb438e653e31d` | `r-260d77eb653ab7ec597a` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -6.835319519054039 | 2.00808 | 1.49068 | `r-880359fc85650f897997` | `r-3c80656cb141cc2f7403` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 87.76913070748881 | 92.37847137578348 | 4.60934 | 1.75813 | `r-880359fc85650f897997` | `r-3c80656cb141cc2f7403` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.629999999860672 | 11.089999999862073 | 1.54 | 0.5 | `r-880359fc85650f897997` | `r-3c80656cb141cc2f7403` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 14.450000000315413 | 1.03 | 0.5 | `r-880359fc85650f897997` | `r-3c80656cb141cc2f7403` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 138.0 | 9 | 3 | `r-880359fc85650f897997` | `r-3c80656cb141cc2f7403` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 363.43999999954167 | 338.6399999995642 | 24.8 | 7.2698 | `r-b0adc3019253aae3e3e8` | `r-4cef8d43b2aa0c41d727` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 64.0 | 3 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-4cef8d43b2aa0c41d727` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | 1.727462768608433 | 2.31488 | 1.70556 | `r-84e85309a66928a29934` | `r-2db63ee1c7dc9ce29c79` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
