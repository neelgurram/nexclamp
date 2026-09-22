# m-scale_capacitance-8e96c2f6e1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.8 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.8 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2333.063 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 14.289999999987003 | 1.23 | 0.5 | `r-cc06a5423671e115f063` | `r-70342a694840764a96ec` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 7.069999999865729 | 5.669999999867002 | 1.4 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-56aa1a1a90fc5b8d9d2c` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 15.759999999985666 | 1.52 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-56aa1a1a90fc5b8d9d2c` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 32.0 | 3 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-56aa1a1a90fc5b8d9d2c` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 8.469999999864456 | 2.21 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-fb195b447603536f8460` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 19.940000000435248 | 2.48 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-fb195b447603536f8460` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 101.0 | 12 | 3 | `r-1b9872d61cd35dd7d644` | `r-fb195b447603536f8460` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 39.0 | 4 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-18aecf7d548ec2e2f3d1` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | -10.53778418731848 | 3.18325 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-a14e76516673d20db281` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 14.279999999987012 | 1.23 | 0.5 | `r-731f49df5b3e5b386bce` | `r-3d920b1131646115da8a` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.029999999865765 | 5.63999999986703 | 1.39 | 0.5 | `r-935039983c3fcf534d52` | `r-8ae191b9176799608feb` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 15.729999999985694 | 1.52 | 0.5 | `r-935039983c3fcf534d52` | `r-8ae191b9176799608feb` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 32.0 | 3 | 0.5 | `r-935039983c3fcf534d52` | `r-8ae191b9176799608feb` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 8.439999999864483 | 2.2 | 0.5 | `r-a7eb0be940e544905260` | `r-1a6c155538d1d994777e` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 19.900000000434375 | 2.48 | 0.5 | `r-a7eb0be940e544905260` | `r-1a6c155538d1d994777e` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 101.0 | 11 | 3 | `r-a7eb0be940e544905260` | `r-1a6c155538d1d994777e` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 39.0 | 4 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-14a1af840cb9229ce2bd` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -10.516689325966041 | 3.19342 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-04243b2f59e0e1721f74` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
