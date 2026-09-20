# m-wrong_compatible_component-d99b9d3dab

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_compatible_component
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "new": "nax", "old": "nax__sh10"}], "element_id": "nax_ModelViewParmSubset_1", "generator_seed": 20260917, "new_species": "na", "old_species": "na"}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_ModelViewParmSubset_1']", "attribute": "ionChannel", "old": "nax__sh10", "new": "nax", "action": "set", "note": "wrong_compatible_component"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1871.049 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 84.54416275022575 | 89.92241668699194 | 5.37825 | 1.69088 | `r-fdc29d572ab8d33a1f37` | `r-31de2a169390a84a4681` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 11.400000000002109 | 4.18 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-31de2a169390a84a4681` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -57.202078374481154 | 1.2475 | 0.5 | `r-007bacc26e9c06940666` | `r-4e4219ec4fd90b90b97f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.013489515743460146 | 0.0112014 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-6fac38b2bc5276820ffa` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 84.44722366475656 | 89.72047805927653 | 5.27325 | 1.68894 | `r-007bacc26e9c06940666` | `r-4e4219ec4fd90b90b97f` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 13.429999999859945 | 5.77 | 0.5 | `r-007bacc26e9c06940666` | `r-4e4219ec4fd90b90b97f` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 61.29999999994425 | 18.23 | 1.5906 | `r-007bacc26e9c06940666` | `r-4e4219ec4fd90b90b97f` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-007bacc26e9c06940666` | `r-4e4219ec4fd90b90b97f` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 84.2643203750593 | 89.54698562761777 | 5.28267 | 1.68529 | `r-2e016fe90119b688bc84` | `r-5a55dd79161781d26e6c` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 17.55999999985619 | 10.25 | 0.5562 | `r-2e016fe90119b688bc84` | `r-5a55dd79161781d26e6c` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 73.50000000160435 | 39.14 | 2.2528 | `r-2e016fe90119b688bc84` | `r-5a55dd79161781d26e6c` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 28.0 | 9 | 0.5 | `r-2e016fe90119b688bc84` | `r-5a55dd79161781d26e6c` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 235.8699999996577 | 164.86 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-7c0b6e71ea0aa207d0d9` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 13.0 | 4 | 0.5 | `r-0cd5f319bb80295395e1` | `r-7c0b6e71ea0aa207d0d9` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 84.03120803962754 | 92.77827453740261 | 8.74707 | 1.68062 | `r-35777975476ff8854a8b` | `r-a81aed9aef927462bc1f` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 4.089999999868439 | 1.39 | 0.5 | `r-35777975476ff8854a8b` | `r-a81aed9aef927462bc1f` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 84.60015106199378 | 89.89284896848672 | 5.2927 | 1.69088 | `r-05c666388af07453703e` | `r-dd658465a5c4490cd939` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 11.3400000000021 | 4.18 | 0.5 | `r-05c666388af07453703e` | `r-dd658465a5c4490cd939` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -57.202077774810746 | 1.2475 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-9e1dfbfa03bbaf6993d0` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.013489515743460146 | 0.0112014 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-428bc565f22b40947599` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 84.47930145405832 | 89.76496124407562 | 5.28566 | 1.68894 | `r-0241c17b5ff2297d2a17` | `r-9e1dfbfa03bbaf6993d0` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 13.399999999859972 | 5.77 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-9e1dfbfa03bbaf6993d0` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 61.28999999994426 | 18.23 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-9e1dfbfa03bbaf6993d0` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 9.0 | 2 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-9e1dfbfa03bbaf6993d0` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.2574310317606 | 89.5643806471569 | 5.30695 | 1.68529 | `r-002bf860824963a1f621` | `r-0b5fae8b85e597cfbcbd` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 17.529999999856216 | 10.24 | 0.5562 | `r-002bf860824963a1f621` | `r-0b5fae8b85e597cfbcbd` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 73.49000000160413 | 39.13 | 2.2528 | `r-002bf860824963a1f621` | `r-0b5fae8b85e597cfbcbd` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 28.0 | 9 | 0.5 | `r-002bf860824963a1f621` | `r-0b5fae8b85e597cfbcbd` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 235.81999999965774 | 164.86 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-655d555d58041655d001` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 13.0 | 4 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-655d555d58041655d001` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 84.07723236217922 | 92.82892990239878 | 8.7517 | 1.68062 | `r-aac3ae71b1a6189ef4f4` | `r-c24e9bf3353597631906` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 4.0699999998684575 | 1.39 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-c24e9bf3353597631906` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
