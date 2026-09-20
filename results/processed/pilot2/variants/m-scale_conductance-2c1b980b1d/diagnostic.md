# m-scale_conductance-2c1b980b1d

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "new": "20.0 mS_per_cm2", "old": "10.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Kd_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Kd_all']", "attribute": "condDensity", "old": "10.0 mS_per_cm2", "new": "20.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 944.021 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -11.33185577391474 | 6.49955 | 0.5 | `r-4cceac4cec0eb866659f` | `r-ce687e1d6a22a76e95ae` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 21.41999999998052 | 1.2 | 0.5 | `r-4cceac4cec0eb866659f` | `r-ce687e1d6a22a76e95ae` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 19.0 | 1 | 0.5 | `r-4cceac4cec0eb866659f` | `r-ce687e1d6a22a76e95ae` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -4.612907409655477 | -11.421661376965176 | 6.80875 | 1.51774 | `r-54e05e4e4388308e9268` | `r-54c3c635f8e2178649f9` |
| h/1 | P04_step_2x | last_isi | exceeds | 10.539999999990414 | 11.249999999989768 | 0.71 | 0.5 | `r-54e05e4e4388308e9268` | `r-54c3c635f8e2178649f9` |
| h/1 | P05_long_step | ahp_depth | exceeds | -5.324134826653506 | -12.002944946290356 | 6.67881 | 1.49068 | `r-d95212df9ca6b2b4efff` | `r-352f32332874fb3c49cf` |
| h/1 | P05_long_step | last_isi | exceeds | 15.610000000340733 | 16.570000000361688 | 0.96 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-352f32332874fb3c49cf` |
| h/1 | P05_long_step | spike_count | exceeds | 128.0 | 120.0 | 8 | 3 | `r-d95212df9ca6b2b4efff` | `r-352f32332874fb3c49cf` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 57.0 | 4 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-726b158b101765b23e1d` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | 3.4738235474345487 | -4.817665100096264 | 8.29149 | 1.70556 | `r-534f36c941e5711ea7a5` | `r-8f937920749f958302e7` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -11.218475341810134 | 6.4838 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-3d4e7a161fe2d065b50b` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 21.389999999980546 | 1.2 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-3d4e7a161fe2d065b50b` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 19.0 | 1 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-3d4e7a161fe2d065b50b` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -4.106994628894597 | -10.837409973159495 | 6.73042 | 1.51774 | `r-e087238cb438e653e31d` | `r-465849d912b50d6fd681` |
| h/2 | P04_step_2x | last_isi | exceeds | 10.439999999990505 | 11.14999999998986 | 0.71 | 0.5 | `r-e087238cb438e653e31d` | `r-465849d912b50d6fd681` |
| h/2 | P05_long_step | ahp_depth | exceeds | -4.827239990238667 | -11.429115295390432 | 6.60188 | 1.49068 | `r-880359fc85650f897997` | `r-24073d45d20c0d58a710` |
| h/2 | P05_long_step | last_isi | exceeds | 15.480000000337895 | 16.45000000035907 | 0.97 | 0.5 | `r-880359fc85650f897997` | `r-24073d45d20c0d58a710` |
| h/2 | P05_long_step | spike_count | exceeds | 129.0 | 121.0 | 8 | 3 | `r-880359fc85650f897997` | `r-24073d45d20c0d58a710` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 57.0 | 4 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-f46a1d45d068c2e9eb47` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | 4.042343139694225 | -4.147621154817756 | 8.18996 | 1.70556 | `r-84e85309a66928a29934` | `r-0d3af3fa55e3df6c23cb` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
