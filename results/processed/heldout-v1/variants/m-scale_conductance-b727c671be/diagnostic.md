# m-scale_conductance-b727c671be

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na_all']", "new": "2e-1 S_per_cm2", "old": "1000.0e-4 S_per_cm2"}], "element": "channelDensity", "element_id": "na_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='na_all']", "attribute": "condDensity", "old": "1000.0e-4 S_per_cm2", "new": "2e-1 S_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2346.979 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 108.20782089620715 | 112.4864120515385 | 4.27859 | 2.16416 | `r-cc06a5423671e115f063` | `r-9f71c9325eb0cf0bd009` |
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 14.849999999986494 | 0.67 | 0.5 | `r-cc06a5423671e115f063` | `r-9f71c9325eb0cf0bd009` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.016563076292602966 | 0.00508845 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-09286d7deb9688d6c81f` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 108.29823684909732 | 112.29425430444428 | 3.99602 | 2.16596 | `r-d2cafd1fc897dbfd8130` | `r-dd1446eee81871e812ca` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 7.069999999865729 | 5.889999999866802 | 1.18 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-dd1446eee81871e812ca` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 16.22999999998524 | 1.05 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-dd1446eee81871e812ca` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 31.0 | 2 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-dd1446eee81871e812ca` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 107.47266006221963 | 111.7528915341699 | 4.28023 | 2.14945 | `r-1b9872d61cd35dd7d644` | `r-d24ccb847e35f5584672` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 8.319999999864592 | 2.36 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-d24ccb847e35f5584672` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 19.7500000004311 | 2.67 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-d24ccb847e35f5584672` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 101.0 | 12 | 3 | `r-1b9872d61cd35dd7d644` | `r-d24ccb847e35f5584672` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 285.9799999996121 | 117.11 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-6e2ce4fc777bb63278f2` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 42.0 | 7 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-6e2ce4fc777bb63278f2` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | -11.108151367184519 | 2.61288 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-0ddd9583795aa2b6acf0` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 108.25350570834362 | 112.46677017388804 | 4.21326 | 2.16416 | `r-731f49df5b3e5b386bce` | `r-630787723e6f8af5bb6d` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 14.839999999986503 | 0.67 | 0.5 | `r-731f49df5b3e5b386bce` | `r-630787723e6f8af5bb6d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.016563076292602966 | 0.00508845 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-1b6ffcffd6cac04d102d` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 107.95729445905641 | 112.16939544963321 | 4.2121 | 2.16596 | `r-935039983c3fcf534d52` | `r-388b8bb3a5b2c29a1df3` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.029999999865765 | 5.8599999998668295 | 1.17 | 0.5 | `r-935039983c3fcf534d52` | `r-388b8bb3a5b2c29a1df3` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 16.189999999985275 | 1.06 | 0.5 | `r-935039983c3fcf534d52` | `r-388b8bb3a5b2c29a1df3` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 31.0 | 2 | 0.5 | `r-935039983c3fcf534d52` | `r-388b8bb3a5b2c29a1df3` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 107.05286025670158 | 111.45710754687973 | 4.40425 | 2.14945 | `r-a7eb0be940e544905260` | `r-c4bef9df1bc8ac877031` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 8.28999999986462 | 2.35 | 0.5 | `r-a7eb0be940e544905260` | `r-c4bef9df1bc8ac877031` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 19.720000000430446 | 2.66 | 0.5 | `r-a7eb0be940e544905260` | `r-c4bef9df1bc8ac877031` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 102.0 | 12 | 3 | `r-a7eb0be940e544905260` | `r-c4bef9df1bc8ac877031` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 285.9099999996122 | 117.1 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-bfaddf68458c4b4d1751` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 42.0 | 7 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-bfaddf68458c4b4d1751` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -11.094213022863457 | 2.6159 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-334971452b4bb8a98e57` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
