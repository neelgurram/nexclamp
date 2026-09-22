# m-scale_capacitance-35f5f6af53

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.5 uF_per_cm2", "old": "1.0 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.0 uF_per_cm2", "new": "0.5 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2264.603 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 108.20782089620715 | 113.00677108317737 | 4.79895 | 2.16416 | `r-cc06a5423671e115f063` | `r-4254a3d71bc66372c59a` |
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 12.509999999988622 | 3.01 | 0.5 | `r-cc06a5423671e115f063` | `r-4254a3d71bc66372c59a` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-cc06a5423671e115f063` | `r-4254a3d71bc66372c59a` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.02049040366095212 | 0.00116112 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-936c03b377b0f7960be8` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 108.29823684909732 | 112.42393111451781 | 4.12569 | 2.16596 | `r-d2cafd1fc897dbfd8130` | `r-81a40b30d22b226ca33f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 7.069999999865729 | 3.609999999868876 | 3.46 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-81a40b30d22b226ca33f` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 13.59999999998763 | 3.68 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-81a40b30d22b226ca33f` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 37.0 | 8 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-81a40b30d22b226ca33f` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 107.47266006221963 | 111.01063537836099 | 3.53798 | 2.14945 | `r-1b9872d61cd35dd7d644` | `r-ef73e77cefdb5e60dc41` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 5.269999999867366 | 5.41 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-ef73e77cefdb5e60dc41` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 16.520000000360596 | 5.9 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-ef73e77cefdb5e60dc41` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 121.0 | 32 | 3 | `r-1b9872d61cd35dd7d644` | `r-ef73e77cefdb5e60dc41` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 387.5799999995197 | 15.51 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-28969693365f24326371` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 45.0 | 10 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-28969693365f24326371` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | -10.776792882278585 | 2.94424 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-4553928a402be5014ef2` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 1.5299999998707676 | 0.859999999871377 | 0.67 | 0.5 | `r-83f9184aaeefc65499cb` | `r-4553928a402be5014ef2` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 108.25350570834362 | 112.93950271966924 | 4.686 | 2.16416 | `r-731f49df5b3e5b386bce` | `r-7ea9ad8b86dbb996af85` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 12.509999999988622 | 3 | 0.5 | `r-731f49df5b3e5b386bce` | `r-7ea9ad8b86dbb996af85` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-731f49df5b3e5b386bce` | `r-7ea9ad8b86dbb996af85` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.02049040366095212 | 0.00116112 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-a1de48de6f3a8040a021` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 107.95729445905641 | 112.04814147446089 | 4.09085 | 2.16596 | `r-935039983c3fcf534d52` | `r-178da7fdacada2815a09` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.029999999865765 | 3.579999999868903 | 3.45 | 0.5 | `r-935039983c3fcf534d52` | `r-178da7fdacada2815a09` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 13.569999999987658 | 3.68 | 0.5 | `r-935039983c3fcf534d52` | `r-178da7fdacada2815a09` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 37.0 | 8 | 0.5 | `r-935039983c3fcf534d52` | `r-178da7fdacada2815a09` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 107.05286025670158 | 110.54543303173241 | 3.49257 | 2.14945 | `r-a7eb0be940e544905260` | `r-6957bdf66e53b0b8c9e2` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 5.2299999998674025 | 5.41 | 0.5 | `r-a7eb0be940e544905260` | `r-6957bdf66e53b0b8c9e2` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 16.470000000359505 | 5.91 | 0.5 | `r-a7eb0be940e544905260` | `r-6957bdf66e53b0b8c9e2` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 122.0 | 32 | 3 | `r-a7eb0be940e544905260` | `r-6957bdf66e53b0b8c9e2` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 387.4899999995198 | 15.52 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-fbed701014e46f090ebd` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 45.0 | 10 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-fbed701014e46f090ebd` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -10.765669769284344 | 2.94444 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-55a7a72b6c09903eca5c` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 1.5099999998707858 | 0.8399999998713952 | 0.67 | 0.5 | `r-dc583bb05cf4bf59d02c` | `r-55a7a72b6c09903eca5c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
