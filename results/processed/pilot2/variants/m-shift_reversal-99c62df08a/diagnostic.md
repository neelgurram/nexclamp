# m-shift_reversal-99c62df08a

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "-110.0 mV", "old": "-100.0 mV"}], "element": "channelDensity", "element_id": "Kd_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "erev", "old": "-100.0 mV", "new": "-110.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1213.029 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -8.821830749495149 | 3.98952 | 0.5 | `r-4cceac4cec0eb866659f` | `r-35a0cbe112823007caac` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 21.00999999998089 | 0.79 | 0.5 | `r-4cceac4cec0eb866659f` | `r-35a0cbe112823007caac` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 19.0 | 1 | 0.5 | `r-4cceac4cec0eb866659f` | `r-35a0cbe112823007caac` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -8.797592163078448 | 4.18468 | 1.51774 | `r-54e05e4e4388308e9268` | `r-90ddea7b40297109325f` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 11.079999999989923 | 0.54 | 0.5 | `r-54e05e4e4388308e9268` | `r-90ddea7b40297109325f` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -9.481994628900878 | 4.15786 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-a1395ec490b9fc56d6f7` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 16.310000000356013 | 0.7 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-a1395ec490b9fc56d6f7` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 122.0 | 6 | 3 | `r-d95212df9ca6b2b4efff` | `r-a1395ec490b9fc56d6f7` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 58.0 | 3 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-8806091f2c2303ada31c` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | -0.8878555297742139 | 4.36168 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-ecddf75d70cce527c6ce` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -8.705619812016138 | 3.97094 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-8b6448acf598cc41cd2e` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 20.97999999998092 | 0.79 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-8b6448acf598cc41cd2e` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 19.0 | 1 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-8b6448acf598cc41cd2e` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | -8.194213867181261 | 4.08722 | 1.51774 | `r-e087238cb438e653e31d` | `r-54aaf41bc28073beaa78` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 10.969999999990023 | 0.53 | 0.5 | `r-e087238cb438e653e31d` | `r-54aaf41bc28073beaa78` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -8.887451171884436 | 4.06021 | 1.49068 | `r-880359fc85650f897997` | `r-c54c8c86e7983bea2b58` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 16.180000000353175 | 0.7 | 0.5 | `r-880359fc85650f897997` | `r-c54c8c86e7983bea2b58` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 123.0 | 6 | 3 | `r-880359fc85650f897997` | `r-c54c8c86e7983bea2b58` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 58.0 | 3 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-e42bbf72d7d6f00a7104` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | -0.22061920167887195 | 4.26296 | 1.70556 | `r-84e85309a66928a29934` | `r-d12aa3d0f66af8fdb4b5` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
