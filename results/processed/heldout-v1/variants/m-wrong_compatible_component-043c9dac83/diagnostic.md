# m-wrong_compatible_component-043c9dac83

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kca_all']", "new": "km", "old": "kca"}], "element_id": "kca_all", "generator_seed": 20260917, "new_species": "k", "old_species": "k"}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kca_all']", "attribute": "ionChannel", "old": "kca", "new": "km", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2301.609 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 17.279999999984284 | 1.76 | 0.5 | `r-cc06a5423671e115f063` | `r-e4c8a49ac70a6915878b` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-cc06a5423671e115f063` | `r-e4c8a49ac70a6915878b` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -68.14186175689683 | -69.32391605529772 | 1.18205 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-05edaa1d8fdf1772d832` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.027218086196298067 | 0.00556656 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-ef38206742d09964d201` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 7.069999999865729 | 7.579999999865265 | 0.51 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-05edaa1d8fdf1772d832` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 19.829999999981965 | 2.55 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-05edaa1d8fdf1772d832` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 25.0 | 4 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-05edaa1d8fdf1772d832` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 12.459999999860827 | 1.78 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-fedf42211200108eeca4` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 34.75000000075852 | 12.33 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-fedf42211200108eeca4` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 59.0 | 30 | 3 | `r-1b9872d61cd35dd7d644` | `r-fedf42211200108eeca4` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 675.4099999992579 | 272.32 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-3f7af33cf319c021dde0` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 20.0 | 15 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-3f7af33cf319c021dde0` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 17.269999999984293 | 1.76 | 0.5 | `r-731f49df5b3e5b386bce` | `r-72f644b4f3b4e5252949` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-731f49df5b3e5b386bce` | `r-72f644b4f3b4e5252949` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -68.14186132202134 | -69.32391554412828 | 1.18205 | 0.5 | `r-935039983c3fcf534d52` | `r-991245b18589590f9a5e` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.027218086196298067 | 0.00556656 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-fe439946dd2f2029123f` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 7.029999999865765 | 7.539999999865302 | 0.51 | 0.5 | `r-935039983c3fcf534d52` | `r-991245b18589590f9a5e` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 19.789999999982 | 2.54 | 0.5 | `r-935039983c3fcf534d52` | `r-991245b18589590f9a5e` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 25.0 | 4 | 0.5 | `r-935039983c3fcf534d52` | `r-991245b18589590f9a5e` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 12.419999999860863 | 1.78 | 0.5 | `r-a7eb0be940e544905260` | `r-6432e3546f73a99aaa89` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 34.650000000756336 | 12.27 | 0.5 | `r-a7eb0be940e544905260` | `r-6432e3546f73a99aaa89` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 60.0 | 30 | 3 | `r-a7eb0be940e544905260` | `r-6432e3546f73a99aaa89` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 675.2599999992581 | 272.25 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-5a278478f89f7d72953f` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 20.0 | 15 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-5a278478f89f7d72953f` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
