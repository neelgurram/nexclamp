# m-scale_gate_slope-15951a0f18

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/forwardRate[1]", "new": "8mV", "old": "10mV"}, {"attribute": "scale", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/reverseRate[1]", "new": "10.666666664mV", "old": "13.33333333mV"}, {"attribute": "scale", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/steadyState[1]", "new": "11.2mV", "old": "14mV"}], "channel": "kamt", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"}`
- recorded edits: `[{"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/forwardRate[1]", "attribute": "scale", "old": "10mV", "new": "8mV", "action": "set", "note": "scale_gate_slope"}, {"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/reverseRate[1]", "attribute": "scale", "old": "13.33333333mV", "new": "10.666666664mV", "action": "set", "note": "scale_gate_slope"}, {"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/steadyState[1]", "attribute": "scale", "old": "14mV", "new": "11.2mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1801.392 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -14.85734673874888 | 2.46666 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-d753db1fa81a34a26e56` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 13.590000000001886 | 1.99 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-d753db1fa81a34a26e56` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -53.899869396209674 | 4.54971 | 0.5 | `r-007bacc26e9c06940666` | `r-e2ba43885ec4c6587c7f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.014548186599276007 | 0.0101427 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-3e7660799f0de222f461` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -16.252468477884925 | 3.04332 | 0.660458 | `r-007bacc26e9c06940666` | `r-e2ba43885ec4c6587c7f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 15.859999999857735 | 3.34 | 0.5 | `r-007bacc26e9c06940666` | `r-e2ba43885ec4c6587c7f` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 55.93999999994912 | 23.59 | 1.5906 | `r-007bacc26e9c06940666` | `r-e2ba43885ec4c6587c7f` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-007bacc26e9c06940666` | `r-e2ba43885ec4c6587c7f` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -17.02508200327555 | 2.80891 | 0.710809 | `r-2e016fe90119b688bc84` | `r-5c028e4f655d8e01210d` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 21.299999999852787 | 6.51 | 0.5562 | `r-2e016fe90119b688bc84` | `r-5c028e4f655d8e01210d` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 70.0300000015286 | 42.61 | 2.2528 | `r-2e016fe90119b688bc84` | `r-5c028e4f655d8e01210d` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 30.0 | 11 | 0.5 | `r-2e016fe90119b688bc84` | `r-5c028e4f655d8e01210d` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 257.22999999963827 | 143.5 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-c3b97c161c04af1057dc` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 13.0 | 4 | 0.5 | `r-0cd5f319bb80295395e1` | `r-c3b97c161c04af1057dc` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -19.89507712046305 | 1.98907 | 0.8953 | `r-35777975476ff8854a8b` | `r-701792a60f6a35d31686` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 4.639999999867939 | 0.84 | 0.5 | `r-35777975476ff8854a8b` | `r-701792a60f6a35d31686` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -14.804755158685332 | 2.44978 | 0.619534 | `r-05c666388af07453703e` | `r-834ca6db2c73a0f02cf2` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 13.540000000001896 | 1.98 | 0.5 | `r-05c666388af07453703e` | `r-834ca6db2c73a0f02cf2` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -53.899868836212114 | 4.54971 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-50b6946c7d8d279e502e` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.014548186599276007 | 0.0101427 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-f588578522aee6f29551` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -16.227123645781532 | 3.03501 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-50b6946c7d8d279e502e` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 15.829999999857762 | 3.34 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-50b6946c7d8d279e502e` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 55.949999999949114 | 23.57 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-50b6946c7d8d279e502e` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-50b6946c7d8d279e502e` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -17.0004467048645 | 2.80059 | 0.710809 | `r-002bf860824963a1f621` | `r-315b5b9079d2bd0844ee` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 21.269999999852814 | 6.5 | 0.5562 | `r-002bf860824963a1f621` | `r-315b5b9079d2bd0844ee` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 70.04000000152882 | 42.58 | 2.2528 | `r-002bf860824963a1f621` | `r-315b5b9079d2bd0844ee` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 30.0 | 11 | 0.5 | `r-002bf860824963a1f621` | `r-315b5b9079d2bd0844ee` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 257.1799999996383 | 143.5 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-ee6da22f37612b8f5fba` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 13.0 | 4 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-ee6da22f37612b8f5fba` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -19.87360802078247 | 1.98079 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-2c0e997c6d2b47527736` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 4.619999999867957 | 0.84 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-2c0e997c6d2b47527736` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
