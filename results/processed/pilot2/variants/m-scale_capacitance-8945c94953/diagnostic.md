# m-scale_capacitance-8945c94953

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1297.965 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -7.317955017071469 | 2.48565 | 0.5 | `r-4cceac4cec0eb866659f` | `r-0ca42dcce955133708ba` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 13.849999999859563 | 3.35 | 0.5 | `r-4cceac4cec0eb866659f` | `r-0ca42dcce955133708ba` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 16.959999999984575 | 3.26 | 0.5 | `r-4cceac4cec0eb866659f` | `r-0ca42dcce955133708ba` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 24.0 | 4 | 0.5 | `r-4cceac4cec0eb866659f` | `r-0ca42dcce955133708ba` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -7.034240722637293 | 2.42133 | 1.51774 | `r-54e05e4e4388308e9268` | `r-b0e3ae581690fc39ad94` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 6.499999999866247 | 1.51 | 0.5 | `r-54e05e4e4388308e9268` | `r-b0e3ae581690fc39ad94` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 9.06999999999175 | 1.47 | 0.5 | `r-54e05e4e4388308e9268` | `r-b0e3ae581690fc39ad94` |
| h/1 | P04_step_2x | spike_count | exceeds | 47.0 | 55.0 | 8 | 3 | `r-54e05e4e4388308e9268` | `r-b0e3ae581690fc39ad94` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -7.79663085935303 | 2.4725 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-83f849aa5ef2ee5e705b` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 10.229999999862855 | 2.44 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-83f849aa5ef2ee5e705b` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 13.210000000288346 | 2.4 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-83f849aa5ef2ee5e705b` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 151.0 | 23 | 3 | `r-d95212df9ca6b2b4efff` | `r-83f849aa5ef2ee5e705b` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 70.0 | 9 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-e64cc5208301f7be46ee` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | 1.5595855713901585 | 1.91424 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-789b64ac4dd0dff4651d` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -7.219413757326379 | 2.48473 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-d845b7667b3a92a94248` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 17.189999999856525 | 13.849999999859563 | 3.34 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-d845b7667b3a92a94248` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 16.929999999984602 | 3.26 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-d845b7667b3a92a94248` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 24.0 | 4 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-d845b7667b3a92a94248` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | -6.521369934066371 | 2.41438 | 1.51774 | `r-e087238cb438e653e31d` | `r-c96011421f1cd572b194` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.989999999864892 | 6.469999999866275 | 1.52 | 0.5 | `r-e087238cb438e653e31d` | `r-c96011421f1cd572b194` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 8.979999999991833 | 1.46 | 0.5 | `r-e087238cb438e653e31d` | `r-c96011421f1cd572b194` |
| h/2 | P04_step_2x | spike_count | exceeds | 48.0 | 55.0 | 7 | 3 | `r-e087238cb438e653e31d` | `r-c96011421f1cd572b194` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -7.293930053707555 | 2.46669 | 1.49068 | `r-880359fc85650f897997` | `r-e1a346ceb65bf61324c0` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.629999999860672 | 10.199999999862882 | 2.43 | 0.5 | `r-880359fc85650f897997` | `r-e1a346ceb65bf61324c0` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 13.110000000286163 | 2.37 | 0.5 | `r-880359fc85650f897997` | `r-e1a346ceb65bf61324c0` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 152.0 | 23 | 3 | `r-880359fc85650f897997` | `r-e1a346ceb65bf61324c0` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 71.0 | 10 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-747989071062048c0813` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | 2.140342712465909 | 1.902 | 1.70556 | `r-84e85309a66928a29934` | `r-c3d85d58feca31dad456` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
