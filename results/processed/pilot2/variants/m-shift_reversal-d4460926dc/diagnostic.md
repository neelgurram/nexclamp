# m-shift_reversal-d4460926dc

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "new": "-66.7723 mV", "old": "-61.7723 mV"}], "element": "channelDensity", "element_id": "pas_ModelViewParmSubset_1", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "attribute": "erev", "old": "-61.7723 mV", "new": "-66.7723 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1808.169 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -10.19408803911351 | 2.1966 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-2d029fb712efca3d53bd` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 18.880000000000834 | 3.3 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-2d029fb712efca3d53bd` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -61.81903840026851 | 3.36946 | 0.5 | `r-007bacc26e9c06940666` | `r-16326c684c79063fc073` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.030974660200805956 | 0.00628372 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-06bb165a756257c949aa` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -9.921412284850575 | 3.28774 | 0.660458 | `r-007bacc26e9c06940666` | `r-16326c684c79063fc073` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 24.54999999984983 | 5.35 | 0.5 | `r-007bacc26e9c06940666` | `r-16326c684c79063fc073` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 88.15999999991982 | 8.63 | 1.5906 | `r-007bacc26e9c06940666` | `r-16326c684c79063fc073` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-007bacc26e9c06940666` | `r-16326c684c79063fc073` |
| h/1 | P05_long_step | adaptation_index | exceeds | 0.005414466597953451 | 0.01879707597977295 | 0.0133826 | 0.01 | `r-2e016fe90119b688bc84` | `r-8a3c52709748f6f99932` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -10.915011222839354 | 3.30116 | 0.710809 | `r-2e016fe90119b688bc84` | `r-8a3c52709748f6f99932` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 40.34999999983546 | 12.54 | 0.5562 | `r-2e016fe90119b688bc84` | `r-8a3c52709748f6f99932` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 187.40000000319856 | 74.76 | 2.2528 | `r-2e016fe90119b688bc84` | `r-8a3c52709748f6f99932` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 12.0 | 7 | 0.5 | `r-2e016fe90119b688bc84` | `r-8a3c52709748f6f99932` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 489.2999999994272 | 88.57 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-f6f0a3b8bea37b0295fa` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 7.0 | 2 | 0.5 | `r-0cd5f319bb80295395e1` | `r-f6f0a3b8bea37b0295fa` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -81.01395223693858 | -85.7623091217042 | 4.74836 | 0.5 | `r-007bacc26e9c06940666` | `r-16326c684c79063fc073` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -14.703028495788345 | 3.20298 | 0.8953 | `r-35777975476ff8854a8b` | `r-2553659b2d821225a176` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 10.869999999862273 | 5.39 | 0.5 | `r-35777975476ff8854a8b` | `r-2553659b2d821225a176` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -10.159371485164513 | 2.1956 | 0.619534 | `r-05c666388af07453703e` | `r-58c8b489cb368136ec4a` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 18.830000000000844 | 3.31 | 0.5 | `r-05c666388af07453703e` | `r-58c8b489cb368136ec4a` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -61.819038212585404 | 3.36946 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-c330ffa8c154ca96d7f3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.030974660200805956 | 0.00628372 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-f52d61d25f3e694f539c` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -9.904703905741371 | 3.28741 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-c330ffa8c154ca96d7f3` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 24.51999999984986 | 5.35 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-c330ffa8c154ca96d7f3` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 88.14999999991983 | 8.63 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-c330ffa8c154ca96d7f3` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-c330ffa8c154ca96d7f3` |
| h/2 | P05_long_step | adaptation_index | exceeds | 0.0054122174080685195 | 0.018771070279217424 | 0.0133589 | 0.01 | `r-002bf860824963a1f621` | `r-e141525c85c137773298` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -10.899073412577309 | 3.30078 | 0.710809 | `r-002bf860824963a1f621` | `r-e141525c85c137773298` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 40.3099999998355 | 12.54 | 0.5562 | `r-002bf860824963a1f621` | `r-e141525c85c137773298` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 187.27000000317253 | 74.65 | 2.2528 | `r-002bf860824963a1f621` | `r-e141525c85c137773298` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 12.0 | 7 | 0.5 | `r-002bf860824963a1f621` | `r-e141525c85c137773298` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 489.24999999942725 | 88.57 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-4bb0ce1d9a10a02d7b25` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 7.0 | 2 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-4bb0ce1d9a10a02d7b25` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -81.01395266571055 | -85.7623095565797 | 4.74836 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-c330ffa8c154ca96d7f3` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -14.690966417948403 | 3.20185 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-2da110c9cdd719a85497` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 10.809999999862328 | 5.35 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-2da110c9cdd719a85497` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
