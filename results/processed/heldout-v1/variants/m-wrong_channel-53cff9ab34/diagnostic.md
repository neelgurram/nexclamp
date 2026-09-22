# m-wrong_channel-53cff9ab34

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "new": "kca", "old": "pas"}], "element_id": "pas_all", "generator_seed": 20260917, "new_species": "k", "old_species": "non_specific"}`
- recorded edits: `[{"file": "NeuroML2/singleCompAllChans.cell.nml", "locator": "/neuroml[@id='cell']/cell[@id='cell']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "attribute": "ionChannel", "old": "pas", "new": "kca", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2569.779 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.768701139863538 | -9.268880114331381 | 3.49982 | 0.638435 | `r-cc06a5423671e115f063` | `r-16e9498e7fb382e440cc` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 108.20782089620715 | 110.76185226439286 | 2.55403 | 2.16416 | `r-cc06a5423671e115f063` | `r-16e9498e7fb382e440cc` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 205.8799999998668 | 223.73999999985057 | 17.86 | 4.1176 | `r-cc06a5423671e115f063` | `r-16e9498e7fb382e440cc` |
| h/1 | P00_canonical | last_isi | exceeds | 15.519999999985885 | 13.469999999987749 | 2.05 | 0.5 | `r-cc06a5423671e115f063` | `r-16e9498e7fb382e440cc` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-cc06a5423671e115f063` | `r-16e9498e7fb382e440cc` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 13.0 | 13 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -68.14186175689683 | -71.6636307137206 | 3.52177 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.0029028071853015504 | 0.0187487 | 0.000433031 | `s-d8858d31b993a1ff480b` | `s-e87fe430ec9adc4d7f45` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -12.946651097611621 | -4.614028442383159 | 8.33262 | 0.647333 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 108.29823684909732 | 110.63741302627746 | 2.33918 | 2.16596 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P04_step_2x | last_isi | exceeds | 17.279999999984284 | 14.879999999986467 | 2.4 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P04_step_2x | spike_count | exceeds | 29.0 | 34.0 | 5 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P05_long_step | ahp_depth | exceeds | -13.077251073198525 | -4.782706726072249 | 8.29454 | 0.653863 | `r-1b9872d61cd35dd7d644` | `r-c13dfde2a163751b6550` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 107.47266006221963 | 109.78025055023365 | 2.30759 | 2.14945 | `r-1b9872d61cd35dd7d644` | `r-c13dfde2a163751b6550` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 10.679999999862446 | 8.889999999864074 | 1.79 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-c13dfde2a163751b6550` |
| h/1 | P05_long_step | last_isi | exceeds | 22.42000000048938 | 17.37000000037915 | 5.05 | 0.5 | `r-1b9872d61cd35dd7d644` | `r-c13dfde2a163751b6550` |
| h/1 | P05_long_step | spike_count | exceeds | 89.0 | 115.0 | 26 | 3 | `r-1b9872d61cd35dd7d644` | `r-c13dfde2a163751b6550` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 403.0899999995056 | 98.97999999978214 | 304.11 | 8.0618 | `r-fb29aefdef0f8e35dca0` | `r-0a3a121c87914f483164` |
| h/1 | P06_ramp | spike_count | exceeds | 35.0 | 52.0 | 17 | 0.5 | `r-fb29aefdef0f8e35dca0` | `r-0a3a121c87914f483164` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -92.45854733276396 | -137.01773011460358 | 44.5592 | 0.5 | `r-d2cafd1fc897dbfd8130` | `r-98319e3fd8235b2ac3c9` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -13.72103464253783 | -5.510428894043102 | 8.21061 | 0.686052 | `r-83f9184aaeefc65499cb` | `r-25d2530061918d22c980` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 134.16434859879257 | 143.22354888608456 | 9.0592 | 2.68329 | `r-83f9184aaeefc65499cb` | `r-25d2530061918d22c980` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.767000547064455 | -9.253357634799087 | 3.51364 | 0.638435 | `r-731f49df5b3e5b386bce` | `r-81fc376c2a1ccb6eee84` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 108.25350570834362 | 110.69248962700003 | 2.43898 | 2.16416 | `r-731f49df5b3e5b386bce` | `r-81fc376c2a1ccb6eee84` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 205.86999999986682 | 225.07999999984935 | 19.21 | 4.1176 | `r-731f49df5b3e5b386bce` | `r-81fc376c2a1ccb6eee84` |
| h/2 | P00_canonical | last_isi | exceeds | 15.509999999985894 | 13.449999999987767 | 2.06 | 0.5 | `r-731f49df5b3e5b386bce` | `r-81fc376c2a1ccb6eee84` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-731f49df5b3e5b386bce` | `r-81fc376c2a1ccb6eee84` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 13.0 | 13 | 0.5 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -68.14186132202134 | -71.54935988681491 | 3.4075 | 0.5 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.02165152653507274 | 0.0029028071853015504 | 0.0187487 | 0.000433031 | `s-cfaadc06f539b47bcf96` | `s-4c9fe8b080f2b92bf87f` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -12.93722168223104 | -4.607999613445415 | 8.32922 | 0.647333 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 107.95729445905641 | 110.29925537167394 | 2.34196 | 2.16596 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P04_step_2x | last_isi | exceeds | 17.24999999998431 | 14.839999999986503 | 2.41 | 0.5 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P04_step_2x | spike_count | exceeds | 29.0 | 34.0 | 5 | 0.5 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P05_long_step | ahp_depth | exceeds | -13.06868377939648 | -4.778196146646877 | 8.29049 | 0.653863 | `r-a7eb0be940e544905260` | `r-72505ee6fe211d784ad2` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 107.05286025670158 | 109.39700699047931 | 2.34415 | 2.14945 | `r-a7eb0be940e544905260` | `r-72505ee6fe211d784ad2` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 10.639999999862482 | 8.859999999864101 | 1.78 | 0.5 | `r-a7eb0be940e544905260` | `r-72505ee6fe211d784ad2` |
| h/2 | P05_long_step | last_isi | exceeds | 22.380000000488508 | 17.340000000378495 | 5.04 | 0.5 | `r-a7eb0be940e544905260` | `r-72505ee6fe211d784ad2` |
| h/2 | P05_long_step | spike_count | exceeds | 90.0 | 115.0 | 25 | 3 | `r-a7eb0be940e544905260` | `r-72505ee6fe211d784ad2` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 403.0099999995057 | 98.92999999978218 | 304.08 | 8.0618 | `r-032d38f7b50aa7c6bdca` | `r-3714c036cabecf5010b6` |
| h/2 | P06_ramp | spike_count | exceeds | 35.0 | 52.0 | 17 | 0.5 | `r-032d38f7b50aa7c6bdca` | `r-3714c036cabecf5010b6` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -92.45854857788115 | -165.2319672699845 | 72.7734 | 0.5 | `r-935039983c3fcf534d52` | `r-7e63895610a916aa7ea8` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -13.710109865824776 | -5.510991861979335 | 8.19912 | 0.686052 | `r-dc583bb05cf4bf59d02c` | `r-ad42301f5a22bc942b8c` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 133.76337051196737 | 142.81951522580673 | 9.05614 | 2.68329 | `r-dc583bb05cf4bf59d02c` | `r-ad42301f5a22bc942b8c` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
