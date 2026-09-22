# m-shift_reversal-2407231390

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ih_all']", "new": "-55.0 mV", "old": "-45.0 mV"}], "element": "channelDensity", "element_id": "Ih_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "NMC/NeuroML2/Soma_AllNML2.cell.nml", "locator": "/neuroml[@id='Soma_AllNML2']/cell[@id='Soma_AllNML2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ih_all']", "attribute": "erev", "old": "-45.0 mV", "new": "-55.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 5224.589 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.540112681203027 | 1.0746608356853358 | 1.61477 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-ade11e5b0be155aeb2d8` |
| h/1 | P00_canonical | last_isi | exceeds | 23.589999999978545 | 24.559999999977663 | 0.97 | 0.5 | `r-f821a906ac6ddfedc3f9` | `r-ade11e5b0be155aeb2d8` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8735102996834598 | 2.4128563919071553 | 1.53935 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-cbecc278129a8845e232` |
| h/1 | P04_step_2x | spike_count | exceeds | 30.0 | 29.0 | 1 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-cbecc278129a8845e232` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.5048961029071961 | 1.981284431457098 | 1.47639 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-a031b03b0d266bb502ab` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.129999999862946 | 10.759999999862373 | 0.63 | 0.5 | `r-a413bdc9ef17abaeb327` | `r-a031b03b0d266bb502ab` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501643676791 | -99.88697536010775 | 1.92196 | 0.5 | `r-57ea9af033cb1e2a1b46` | `r-cbecc278129a8845e232` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -0.9663868560786995 | 0.5780251541137744 | 1.54441 | 0.5 | `r-c4b56e49cd97e4a16650` | `r-022bc8751b5d4b5bbe75` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.5443046181071622 | 1.0705907633016665 | 1.6149 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-d90656ac749bdb5efa21` |
| h/2 | P00_canonical | last_isi | exceeds | 23.579999999978554 | 24.559999999977663 | 0.98 | 0.5 | `r-1175b1c4f005ecbea9cd` | `r-d90656ac749bdb5efa21` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.8550077082320229 | 2.3950932235721893 | 1.54009 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-ed37fc4302bb4457cb6a` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5178800226843094 | 1.9988453598048181 | 1.48097 | 0.5 | `r-019eab9c744398314e93` | `r-4cbf038332a72694ca6b` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.099999999862973 | 10.7299999998624 | 0.63 | 0.5 | `r-019eab9c744398314e93` | `r-4cbf038332a72694ca6b` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -97.96501782989534 | -99.88697675323519 | 1.92196 | 0.5 | `r-2cb2390f7c947ffeefc6` | `r-ed37fc4302bb4457cb6a` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -0.9949755071020263 | 0.5451939315811956 | 1.54017 | 0.5 | `r-c07f6c024edce4a536eb` | `r-9e452b62adf4cc481c70` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
