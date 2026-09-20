# m-shift_reversal-3d387f89f7

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `pospischil2008_fs`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "new": "45.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "Na_all", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/cells/FS/FS.cell.nml", "locator": "/neuroml[@id='FS']/cell[@id='FS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Na_all']", "attribute": "erev", "old": "50.0 mV", "new": "45.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 928.939 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -4.832305908199814 | -3.9496078491177684 | 0.882698 | 0.5 | `r-4cceac4cec0eb866659f` | `r-4cfe249288630565b363` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 87.45660400498362 | 82.58050918742542 | 4.87609 | 1.74913 | `r-4cceac4cec0eb866659f` | `r-4cfe249288630565b363` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 88.51488494896842 | 83.6892929090031 | 4.82559 | 1.7703 | `r-54e05e4e4388308e9268` | `r-05d97ff7c858925955e1` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 87.90636062789724 | 82.99207687477374 | 4.91428 | 1.75813 | `r-d95212df9ca6b2b4efff` | `r-69599d2e668bc3d6c39d` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 118.24569702145673 | 113.46432113640651 | 4.78138 | 2.36491 | `r-534f36c941e5711ea7a5` | `r-5cac9f7068750cce1ffb` |
| h/2 | P00_canonical | ahp_depth | exceeds | -4.734680175792306 | -3.852378845228131 | 0.882301 | 0.5 | `r-c9243a4c0b8a67de36a8` | `r-e932685659cf01582b19` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 87.36877822947855 | 82.5058631910268 | 4.86292 | 1.74913 | `r-c9243a4c0b8a67de36a8` | `r-e932685659cf01582b19` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 88.43542480636255 | 83.5235939037554 | 4.91183 | 1.7703 | `r-e087238cb438e653e31d` | `r-7e129123336ffddb1637` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 87.76913070748881 | 82.86491012731764 | 4.90422 | 1.75813 | `r-880359fc85650f897997` | `r-2bbd3cf7b0842ca06a2a` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 118.07249069170416 | 113.30671310379064 | 4.76578 | 2.36491 | `r-84e85309a66928a29934` | `r-10d1ba77371906d27fa9` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
