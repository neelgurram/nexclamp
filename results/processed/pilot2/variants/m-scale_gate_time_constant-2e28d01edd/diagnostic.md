# m-scale_gate_time_constant-2e28d01edd

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "Na", "factor": 2.0, "gate": "h", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "NeuroML2/channels/Na/Na.channel.nml", "locator": "/neuroml[@id='Na']/ionChannel[@id='Na']/gate[@id='h']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1325.102 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -0.3263854980490919 | 4.50592 | 0.5 | `r-4cceac4cec0eb866659f` | `r-054689ba190025196741` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 87.45660400498362 | 81.5754051223939 | 5.8812 | 1.74913 | `r-4cceac4cec0eb866659f` | `r-054689ba190025196741` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 19.079999999982647 | 1.14 | 0.5 | `r-4cceac4cec0eb866659f` | `r-054689ba190025196741` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 21.0 | 1 | 0.5 | `r-4cceac4cec0eb866659f` | `r-054689ba190025196741` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -0.20871734617371374 | 4.40419 | 1.51774 | `r-54e05e4e4388308e9268` | `r-60e7d84d440bdad95212` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 88.51488494896842 | 83.24060058714329 | 5.27428 | 1.7703 | `r-54e05e4e4388308e9268` | `r-60e7d84d440bdad95212` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 9.72999999999115 | 0.81 | 0.5 | `r-54e05e4e4388308e9268` | `r-60e7d84d440bdad95212` |
| h/1 | P04_step_2x | spike_count | exceeds | 47.0 | 51.0 | 4 | 3 | `r-54e05e4e4388308e9268` | `r-60e7d84d440bdad95212` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -0.9855880737233775 | 4.33855 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-f8f8d2005c014c7bdf1e` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.90636062789724 | 82.40787124799868 | 5.49849 | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-f8f8d2005c014c7bdf1e` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 14.630000000319342 | 0.98 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-f8f8d2005c014c7bdf1e` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 136.0 | 8 | 3 | `r-d95212df9ca6b2b4efff` | `r-f8f8d2005c014c7bdf1e` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 65.0 | 4 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-beeccdc9f5c5f5f645c9` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | 8.191490173388573 | 4.71767 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-2b3d9ab826ebf5187332` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 118.24569702145673 | 114.33942413290694 | 3.90627 | 2.36491 | `r-534f36c941e5711ea7a5` | `r-2b3d9ab826ebf5187332` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -0.20559692383476147 | 4.52908 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-409029e3be134b1e0feb` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 87.36877822947855 | 81.45985794181396 | 5.90892 | 1.74913 | `r-c9243a4c0b8a67de36a8` | `r-409029e3be134b1e0feb` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 19.049999999982674 | 1.14 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-409029e3be134b1e0feb` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 21.0 | 1 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-409029e3be134b1e0feb` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | 0.43156433106508985 | 4.53856 | 1.51774 | `r-e087238cb438e653e31d` | `r-195b63a49cb2255438d8` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 88.43542480636255 | 82.8834075938895 | 5.55202 | 1.7703 | `r-e087238cb438e653e31d` | `r-195b63a49cb2255438d8` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 9.60999999999126 | 0.83 | 0.5 | `r-e087238cb438e653e31d` | `r-195b63a49cb2255438d8` |
| h/2 | P04_step_2x | spike_count | exceeds | 48.0 | 52.0 | 4 | 3 | `r-e087238cb438e653e31d` | `r-195b63a49cb2255438d8` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -0.3587570190485536 | 4.46848 | 1.49068 | `r-880359fc85650f897997` | `r-1a8a2f158c1ed1beca34` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 87.76913070748881 | 82.09594345149503 | 5.67319 | 1.75813 | `r-880359fc85650f897997` | `r-1a8a2f158c1ed1beca34` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 14.460000000315631 | 1.02 | 0.5 | `r-880359fc85650f897997` | `r-1a8a2f158c1ed1beca34` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 138.0 | 9 | 3 | `r-880359fc85650f897997` | `r-1a8a2f158c1ed1beca34` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 66.0 | 5 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-6754727158967cdcfdef` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | 8.932647705054457 | 4.8903 | 1.70556 | `r-84e85309a66928a29934` | `r-fa163cb353f72a8a2e5c` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 118.07249069170416 | 113.97922134317093 | 4.09327 | 2.36491 | `r-84e85309a66928a29934` | `r-fa163cb353f72a8a2e5c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
