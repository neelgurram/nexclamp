# m-shift_reversal-9acb9774d9

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "new": "60.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "nax_ModelViewParmSubset_1", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "attribute": "erev", "old": "50.0 mV", "new": "60.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1730.243 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -13.908838414434172 | 1.51815 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-7f84302635c971e4718f` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 84.54416275022575 | 94.6511955261036 | 10.107 | 1.69088 | `r-fdc29d572ab8d33a1f37` | `r-7f84302635c971e4718f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.024110374974386995 | 0.000580561 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-feb18bc6b3b01dede9ee` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -14.635002136229986 | 1.42585 | 0.660458 | `r-007bacc26e9c06940666` | `r-b56fc25c3a2362deef6e` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 84.44722366475656 | 94.53992462302645 | 10.0927 | 1.68894 | `r-007bacc26e9c06940666` | `r-b56fc25c3a2362deef6e` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -15.537178039550781 | 1.32101 | 0.710809 | `r-2e016fe90119b688bc84` | `r-46ece7203e1efd7f00a8` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 84.2643203750593 | 94.22221756134981 | 9.9579 | 1.68529 | `r-2e016fe90119b688bc84` | `r-46ece7203e1efd7f00a8` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 27.049999999847557 | 0.76 | 0.5562 | `r-2e016fe90119b688bc84` | `r-46ece7203e1efd7f00a8` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 115.06000000251152 | 2.42 | 2.2528 | `r-2e016fe90119b688bc84` | `r-46ece7203e1efd7f00a8` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 391.72999999951594 | 9 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-547b5b99f09f4f70fa05` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -18.833297729492188 | 0.927292 | 0.8953 | `r-35777975476ff8854a8b` | `r-74ed2645b230beea69ce` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 84.03120803962754 | 94.1106147779056 | 10.0794 | 1.68062 | `r-35777975476ff8854a8b` | `r-74ed2645b230beea69ce` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -13.870637428701215 | 1.51567 | 0.619534 | `r-05c666388af07453703e` | `r-c23cde969b7bac669056` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 84.60015106199378 | 94.68136596677796 | 10.0812 | 1.69088 | `r-05c666388af07453703e` | `r-c23cde969b7bac669056` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.024110374974386995 | 0.000580561 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-57df9e5a412c7ac88416` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -14.616828918457031 | 1.42471 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-7be16f39864c12444dc7` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 84.47930145405832 | 94.45828628686849 | 9.97898 | 1.68894 | `r-0241c17b5ff2297d2a17` | `r-7be16f39864c12444dc7` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -15.519821166992188 | 1.31997 | 0.710809 | `r-002bf860824963a1f621` | `r-eaa820f779912834ec1b` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.2574310317606 | 94.30352020409165 | 10.0461 | 1.68529 | `r-002bf860824963a1f621` | `r-eaa820f779912834ec1b` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 27.009999999847594 | 0.76 | 0.5562 | `r-002bf860824963a1f621` | `r-eaa820f779912834ec1b` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 115.02000000251064 | 2.4 | 2.2528 | `r-002bf860824963a1f621` | `r-eaa820f779912834ec1b` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 391.679999999516 | 9 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-492d487e6aa4bbf163c0` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -18.81951141357422 | 0.926697 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-1f87a5b65b51e15fcdbc` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 84.07723236217922 | 94.04696273933021 | 9.96973 | 1.68062 | `r-aac3ae71b1a6189ef4f4` | `r-1f87a5b65b51e15fcdbc` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
