# m-scale_conductance-fd3b7c7dcc

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kamt_ModelViewParmSubset_1']", "new": "2.0 mS_per_cm2", "old": "4.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "kamt_ModelViewParmSubset_1", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kamt_ModelViewParmSubset_1']", "attribute": "condDensity", "old": "4.0 mS_per_cm2", "new": "2.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1738.367 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -7.4147806879299765 | 4.97591 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-78f35603703ed1cdb27d` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 14.300000000001745 | 1.28 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-78f35603703ed1cdb27d` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -55.82597444839473 | 2.6236 | 0.5 | `r-007bacc26e9c06940666` | `r-807ba17d1088a751ff39` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.017758349839491837 | 0.00693259 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-034fe36b5241d66b9630` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -9.061417867024495 | 4.14773 | 0.660458 | `r-007bacc26e9c06940666` | `r-807ba17d1088a751ff39` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 17.059999999856643 | 2.14 | 0.5 | `r-007bacc26e9c06940666` | `r-807ba17d1088a751ff39` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -10.549073506672919 | 3.6671 | 0.710809 | `r-2e016fe90119b688bc84` | `r-049c14f528c6b9ceb85e` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 23.369999999850904 | 4.44 | 0.5562 | `r-2e016fe90119b688bc84` | `r-049c14f528c6b9ceb85e` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 101.00000000220462 | 11.64 | 2.2528 | `r-2e016fe90119b688bc84` | `r-049c14f528c6b9ceb85e` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 21.0 | 2 | 0.5 | `r-2e016fe90119b688bc84` | `r-049c14f528c6b9ceb85e` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 297.9899999996012 | 102.74 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-bc281f106b232b7c6101` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-0cd5f319bb80295395e1` | `r-bc281f106b232b7c6101` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -15.785363484700518 | 2.12064 | 0.8953 | `r-35777975476ff8854a8b` | `r-02a68088e2c77a582ac8` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 4.969999999867639 | 0.51 | 0.5 | `r-35777975476ff8854a8b` | `r-02a68088e2c77a582ac8` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -7.382559401478929 | 4.97241 | 0.619534 | `r-05c666388af07453703e` | `r-9f1dd678f3153592f443` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 14.250000000001755 | 1.27 | 0.5 | `r-05c666388af07453703e` | `r-9f1dd678f3153592f443` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -55.8259742370605 | 2.6236 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-baac4e962fc3f5f953e3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.017758349839491837 | 0.00693259 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-6b6e4faf1e26ddea5fac` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -9.04613621266683 | 4.14598 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-baac4e962fc3f5f953e3` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 17.03999999985666 | 2.13 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-baac4e962fc3f5f953e3` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -10.534432721455893 | 3.66542 | 0.710809 | `r-002bf860824963a1f621` | `r-b129dcba110297f5ae07` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 23.33999999985093 | 4.43 | 0.5562 | `r-002bf860824963a1f621` | `r-b129dcba110297f5ae07` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 100.98000000220418 | 11.64 | 2.2528 | `r-002bf860824963a1f621` | `r-b129dcba110297f5ae07` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 21.0 | 2 | 0.5 | `r-002bf860824963a1f621` | `r-b129dcba110297f5ae07` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 297.93999999960124 | 102.74 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-92d926c581e6f3d0dce7` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-92d926c581e6f3d0dce7` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -15.773347211201987 | 2.11947 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-9c863d4a77bd83f78546` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 4.949999999867657 | 0.51 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-9c863d4a77bd83f78546` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
