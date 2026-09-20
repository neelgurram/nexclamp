# m-shift_reversal-3bffbb8e9b

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kamt_ModelViewParmSubset_1']", "new": "-80.0 mV", "old": "-90.0 mV"}], "element": "channelDensity", "element_id": "kamt_ModelViewParmSubset_1", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kamt_ModelViewParmSubset_1']", "attribute": "erev", "old": "-90.0 mV", "new": "-80.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1713.305 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -6.255697601470189 | 6.13499 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-4d3bb920707eb3a1c1ca` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 14.760000000001654 | 0.82 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-4d3bb920707eb3a1c1ca` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -57.02379573059078 | 1.42578 | 0.5 | `r-007bacc26e9c06940666` | `r-e4e2c4901b51c89f2ea1` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.02137832115292671 | 0.00331262 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-755fc9d607e83098095b` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -7.408246832529706 | 5.80091 | 0.660458 | `r-007bacc26e9c06940666` | `r-e4e2c4901b51c89f2ea1` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 17.879999999855897 | 1.32 | 0.5 | `r-007bacc26e9c06940666` | `r-e4e2c4901b51c89f2ea1` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 85.47999999992226 | 5.95 | 1.5906 | `r-007bacc26e9c06940666` | `r-e4e2c4901b51c89f2ea1` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-007bacc26e9c06940666` | `r-e4e2c4901b51c89f2ea1` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -8.459379034678143 | 5.75679 | 0.710809 | `r-2e016fe90119b688bc84` | `r-dc35659bc9eac37d804f` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 25.10999999984932 | 2.7 | 0.5562 | `r-2e016fe90119b688bc84` | `r-dc35659bc9eac37d804f` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 347.62999999955605 | 53.1 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-0731784e4b10c841e855` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-0cd5f319bb80295395e1` | `r-0731784e4b10c841e855` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -12.219075995127362 | 5.68693 | 0.8953 | `r-35777975476ff8854a8b` | `r-38490f6c6090a4259d3f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -6.232287392687439 | 6.12268 | 0.619534 | `r-05c666388af07453703e` | `r-0e2b0cd0155838e7681a` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 14.710000000001664 | 0.81 | 0.5 | `r-05c666388af07453703e` | `r-0e2b0cd0155838e7681a` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -57.02379557800288 | 1.42578 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-06a6da25013236dab6d2` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.02137832115292671 | 0.00331262 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-0cc6644df81348e5a141` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -7.397413107554115 | 5.7947 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-06a6da25013236dab6d2` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 17.849999999855925 | 1.32 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-06a6da25013236dab6d2` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 85.45999999992227 | 5.94 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-06a6da25013236dab6d2` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 6.0 | 1 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-06a6da25013236dab6d2` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -8.449369284311928 | 5.75048 | 0.710809 | `r-002bf860824963a1f621` | `r-d03a814b0e2ddea28657` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 25.07999999984935 | 2.69 | 0.5562 | `r-002bf860824963a1f621` | `r-d03a814b0e2ddea28657` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 347.5799999995561 | 53.1 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-8de0a4e1f23e3df50202` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 8.0 | 1 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-8de0a4e1f23e3df50202` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -12.212606283823646 | 5.68021 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-bb0c96e3b61b120920e0` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
