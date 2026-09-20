# m-scale_conductance-8d921084f4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "new": "62.5 mS_per_cm2", "old": "50.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Na_all", "factor": 1.25, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "attribute": "condDensity", "old": "50.0 mS_per_cm2", "new": "62.5 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 925.981 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -5.515747070309203 | 0.683441 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 87.45660400498362 | 89.45839691326167 | 2.00179 | 1.74913 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 17.199999999856516 | 16.23999999985739 | 0.96 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | last_isi | exceeds | 20.21999999998161 | 19.43999999998232 | 0.78 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P00_canonical | spike_count | exceeds | 20.0 | 21.0 | 1 | 0.5 | `r-4cceac4cec0eb866659f` | `r-5567f02389795c6ec4b6` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.37497438699542385 | 0.00932313 | 0.00768595 | `s-208b51a847cba1e6aceb` | `s-a9264b3fc05cffce0044` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 88.51488494896842 | 90.39295959601024 | 1.87807 | 1.7703 | `r-54e05e4e4388308e9268` | `r-c0256a1d41eb91e6e4c9` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.90636062789724 | 89.86414337277284 | 1.95778 | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-73b02f2397ed958f46cb` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.669999999860636 | 12.129999999861127 | 0.54 | 0.5 | `r-d95212df9ca6b2b4efff` | `r-73b02f2397ed958f46cb` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 363.4899999995416 | 355.2899999995491 | 8.2 | 7.2698 | `r-5888f8cf54a64bb2eb2f` | `r-ab098fe004c83682311f` |
| h/1 | P06_ramp | spike_count | exceeds | 61.0 | 62.0 | 1 | 0.5 | `r-5888f8cf54a64bb2eb2f` | `r-ab098fe004c83682311f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -5.421684265149906 | 0.687004 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-694f1990031799d5c551` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 87.36877822947855 | 89.39162826669599 | 2.02285 | 1.74913 | `r-c9243a4c0b8a67de36a8` | `r-694f1990031799d5c551` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 17.189999999856525 | 16.229999999857398 | 0.96 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-694f1990031799d5c551` |
| h/2 | P00_canonical | last_isi | exceeds | 20.189999999981637 | 19.419999999982338 | 0.77 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-694f1990031799d5c551` |
| h/2 | P00_canonical | spike_count | exceeds | 20.0 | 21.0 | 1 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-694f1990031799d5c551` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.384297520661157 | 0.37497438699542385 | 0.00932313 | 0.00768595 | `s-a5d560731591d7405a9c` | `s-817dc903276aa0f814d1` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 88.43542480636255 | 90.2573776256644 | 1.82195 | 1.7703 | `r-e087238cb438e653e31d` | `r-7564123c270f5a1068c8` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 87.76913070748881 | 89.76739883594692 | 1.99827 | 1.75813 | `r-880359fc85650f897997` | `r-3575372fa0e201c029b3` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.629999999860672 | 12.099999999861154 | 0.53 | 0.5 | `r-880359fc85650f897997` | `r-3575372fa0e201c029b3` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 363.43999999954167 | 355.2399999995491 | 8.2 | 7.2698 | `r-b0adc3019253aae3e3e8` | `r-b9fc0dd0d6c2fd9d2994` |
| h/2 | P06_ramp | spike_count | exceeds | 61.0 | 62.0 | 1 | 0.5 | `r-b0adc3019253aae3e3e8` | `r-b9fc0dd0d6c2fd9d2994` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
