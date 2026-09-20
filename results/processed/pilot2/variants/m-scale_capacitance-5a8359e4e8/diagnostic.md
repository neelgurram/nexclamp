# m-scale_capacitance-5a8359e4e8

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1310.562 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -12.204025268533783 | 7.37172 | 0.5 | `r-4cceac4cec0eb866659f` | `r-dafe43d5a2d0478d6f0a` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 87.45660400498362 | 91.30285263137543 | 3.84625 | 1.74913 | `r-4cceac4cec0eb866659f` | `r-dafe43d5a2d0478d6f0a` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 8.819999999864137 | 8.38 | 0.5 | `r-4cceac4cec0eb866659f` | `r-dafe43d5a2d0478d6f0a` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 11.679999999989377 | 8.54 | 0.5 | `r-4cceac4cec0eb866659f` | `r-dafe43d5a2d0478d6f0a` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 35.0 | 15 | 0.5 | `r-4cceac4cec0eb866659f` | `r-dafe43d5a2d0478d6f0a` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -11.788536071736814 | 7.17563 | 1.51774 | `r-54e05e4e4388308e9268` | `r-09e167a8d306a6eb4f6b` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 88.51488494896842 | 92.76014328132842 | 4.24526 | 1.7703 | `r-54e05e4e4388308e9268` | `r-09e167a8d306a6eb4f6b` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.009999999864874 | 4.20999999986833 | 3.8 | 0.5 | `r-54e05e4e4388308e9268` | `r-09e167a8d306a6eb4f6b` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 6.589999999994006 | 3.95 | 0.5 | `r-54e05e4e4388308e9268` | `r-09e167a8d306a6eb4f6b` |
| h/1 | P04_step_2x | spike_count | exceeds | 47.0 | 76.0 | 29 | 3 | `r-54e05e4e4388308e9268` | `r-09e167a8d306a6eb4f6b` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -12.637336730974127 | 7.3132 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-dcc19b43bd0cd09f0270` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.90636062789724 | 91.80000686682544 | 3.89365 | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-dcc19b43bd0cd09f0270` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 6.559999999866193 | 6.11 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-dcc19b43bd0cd09f0270` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 9.290000000202781 | 6.32 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-dcc19b43bd0cd09f0270` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 215.0 | 87 | 3 | `r-d95212df9ca6b2b4efff` | `r-dcc19b43bd0cd09f0270` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 363.4899999995416 | 352.7199999995514 | 10.77 | 7.2698 | `r-5888f8cf54a64bb2eb2f` | `r-7fb48de644d0afbf82cc` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 96.0 | 35 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-7fb48de644d0afbf82cc` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | -2.319023132308189 | 5.79285 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-331a6663db403e62face` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.6599999998706494 | 0.9399999998713042 | 0.72 | 0.5 | `r-534f36c941e5711ea7a5` | `r-331a6663db403e62face` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-534f36c941e5711ea7a5` | `r-331a6663db403e62face` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -12.104644775415707 | 7.36996 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-2dfc8aa8ce2f766944a5` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 87.36877822947855 | 91.34519958700596 | 3.97642 | 1.74913 | `r-c9243a4c0b8a67de36a8` | `r-2dfc8aa8ce2f766944a5` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 17.189999999856525 | 8.819999999864137 | 8.37 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-2dfc8aa8ce2f766944a5` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 11.679999999989377 | 8.51 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-2dfc8aa8ce2f766944a5` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 35.0 | 15 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-2dfc8aa8ce2f766944a5` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | -11.273757934544392 | 7.16676 | 1.51774 | `r-e087238cb438e653e31d` | `r-dbd73eda7d07789986f2` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 88.43542480636255 | 92.70101165822479 | 4.26559 | 1.7703 | `r-e087238cb438e653e31d` | `r-dbd73eda7d07789986f2` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.989999999864892 | 4.1799999998683575 | 3.81 | 0.5 | `r-e087238cb438e653e31d` | `r-dbd73eda7d07789986f2` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 6.539999999994052 | 3.9 | 0.5 | `r-e087238cb438e653e31d` | `r-dbd73eda7d07789986f2` |
| h/2 | P04_step_2x | spike_count | exceeds | 48.0 | 76.0 | 28 | 3 | `r-e087238cb438e653e31d` | `r-dbd73eda7d07789986f2` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -12.135429382304054 | 7.30819 | 1.49068 | `r-880359fc85650f897997` | `r-d245f6c89bcc16c80a63` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 87.76913070748881 | 91.78482818646623 | 4.0157 | 1.75813 | `r-880359fc85650f897997` | `r-d245f6c89bcc16c80a63` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.629999999860672 | 6.52999999986622 | 6.1 | 0.5 | `r-880359fc85650f897997` | `r-d245f6c89bcc16c80a63` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 9.230000000201471 | 6.25 | 0.5 | `r-880359fc85650f897997` | `r-d245f6c89bcc16c80a63` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 216.0 | 87 | 3 | `r-880359fc85650f897997` | `r-d245f6c89bcc16c80a63` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 363.43999999954167 | 352.66999999955146 | 10.77 | 7.2698 | `r-b0adc3019253aae3e3e8` | `r-90d57c02f08d91be81ff` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 97.0 | 36 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-90d57c02f08d91be81ff` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | -1.7216949463492028 | 5.76404 | 1.70556 | `r-84e85309a66928a29934` | `r-31fc17cfdf4b95f497e0` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.6399999998706676 | 0.9299999998713133 | 0.71 | 0.5 | `r-84e85309a66928a29934` | `r-31fc17cfdf4b95f497e0` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 2.0 | 1 | 0.5 | `r-84e85309a66928a29934` | `r-31fc17cfdf4b95f497e0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
