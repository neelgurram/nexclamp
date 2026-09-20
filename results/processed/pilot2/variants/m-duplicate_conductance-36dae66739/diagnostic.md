# m-duplicate_conductance-36dae66739

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "nax_ModelViewParmSubset_1_dup", "source_id": "nax_ModelViewParmSubset_1"}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"40.0 mS_per_cm2\" id=\"nax_ModelViewParmSubset_1_dup\" ionChannel=\"nax__sh10\" segmentGroup=\"soma_group\" ion=\"na\" erev=\"50.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 2533.914 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -13.736048114833551 | 1.34536 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-418ad48da46838bbcd90` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 84.54416275022575 | 87.55979919431411 | 3.01564 | 1.69088 | `r-fdc29d572ab8d33a1f37` | `r-418ad48da46838bbcd90` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 13.680000000001868 | 1.9 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-418ad48da46838bbcd90` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.020592855679256884 | 0.00409808 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-6f276661dfaaa0d62735` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -14.497451782226562 | 1.2883 | 0.660458 | `r-007bacc26e9c06940666` | `r-a5b03fd8abf7a881c393` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 84.44722366475656 | 87.55795669696364 | 3.11073 | 1.68894 | `r-007bacc26e9c06940666` | `r-a5b03fd8abf7a881c393` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 16.609999999857052 | 2.59 | 0.5 | `r-007bacc26e9c06940666` | `r-a5b03fd8abf7a881c393` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 72.68999999993389 | 6.84 | 1.5906 | `r-007bacc26e9c06940666` | `r-a5b03fd8abf7a881c393` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -15.435829162597415 | 1.21966 | 0.710809 | `r-2e016fe90119b688bc84` | `r-4fb2f519e8cf74cd98ad` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 84.2643203750593 | 87.43571853784275 | 3.1714 | 1.68529 | `r-2e016fe90119b688bc84` | `r-4fb2f519e8cf74cd98ad` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 23.09999999985115 | 4.71 | 0.5562 | `r-2e016fe90119b688bc84` | `r-4fb2f519e8cf74cd98ad` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 96.73000000211141 | 15.91 | 2.2528 | `r-2e016fe90119b688bc84` | `r-4fb2f519e8cf74cd98ad` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 22.0 | 3 | 0.5 | `r-2e016fe90119b688bc84` | `r-4fb2f519e8cf74cd98ad` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 337.9099999995649 | 62.82 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-ceca322b05cd7c82934c` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-0cd5f319bb80295395e1` | `r-ceca322b05cd7c82934c` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 84.03120803962754 | 86.36170959602038 | 2.3305 | 1.68062 | `r-35777975476ff8854a8b` | `r-190722a89232c47e009c` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 4.549999999868021 | 0.93 | 0.5 | `r-35777975476ff8854a8b` | `r-190722a89232c47e009c` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -13.70719993173779 | 1.35223 | 0.619534 | `r-05c666388af07453703e` | `r-25e5a2bf07079c8ba848` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 84.60015106199378 | 87.66034698484188 | 3.0602 | 1.69088 | `r-05c666388af07453703e` | `r-25e5a2bf07079c8ba848` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 13.62000000000188 | 1.9 | 0.5 | `r-05c666388af07453703e` | `r-25e5a2bf07079c8ba848` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.020592855679256884 | 0.00409808 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-00aca18203ba3efd23f8` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -14.483688354492188 | 1.29157 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-8fdcb27ab90ba3a3622b` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 84.47930145405832 | 87.61468887469422 | 3.13539 | 1.68894 | `r-0241c17b5ff2297d2a17` | `r-8fdcb27ab90ba3a3622b` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 16.57999999985708 | 2.59 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-8fdcb27ab90ba3a3622b` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 72.6699999999339 | 6.85 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-8fdcb27ab90ba3a3622b` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -15.422569274901846 | 1.22272 | 0.710809 | `r-002bf860824963a1f621` | `r-22d39ecdfcc9d5a00a37` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.2574310317606 | 87.46005630641965 | 3.20263 | 1.68529 | `r-002bf860824963a1f621` | `r-22d39ecdfcc9d5a00a37` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 23.069999999851177 | 4.7 | 0.5562 | `r-002bf860824963a1f621` | `r-22d39ecdfcc9d5a00a37` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 96.72000000211119 | 15.9 | 2.2528 | `r-002bf860824963a1f621` | `r-22d39ecdfcc9d5a00a37` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 22.0 | 3 | 0.5 | `r-002bf860824963a1f621` | `r-22d39ecdfcc9d5a00a37` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 337.85999999956493 | 62.82 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-69dc5830065511fa612e` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-69dc5830065511fa612e` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 84.07723236217922 | 86.34989547862781 | 2.27266 | 1.68062 | `r-aac3ae71b1a6189ef4f4` | `r-162ff6a311f33b811ac8` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 4.529999999868039 | 0.93 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-162ff6a311f33b811ac8` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
