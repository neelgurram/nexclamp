# m-scale_capacitance-f459583f48

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "0.9 uF_per_cm2", "old": "1.8 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.8 uF_per_cm2", "new": "0.9 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1694.141 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -14.10739135742189 | 1.71671 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-981bdd0cf4c38ac5950d` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 84.54416275022575 | 87.31504440306045 | 2.77088 | 1.69088 | `r-fdc29d572ab8d33a1f37` | `r-981bdd0cf4c38ac5950d` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 8.440000000001646 | 7.14 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-981bdd0cf4c38ac5950d` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.022539444027047335 | 0.00215149 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-c4a462f6fab43872920d` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -14.952186584471761 | 1.74303 | 0.660458 | `r-007bacc26e9c06940666` | `r-c7352738bee39186b940` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 84.44722366475656 | 87.17129135269684 | 2.72407 | 1.68894 | `r-007bacc26e9c06940666` | `r-c7352738bee39186b940` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 10.239999999862846 | 8.96 | 0.5 | `r-007bacc26e9c06940666` | `r-c7352738bee39186b940` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 71.91999999993459 | 7.61 | 1.5906 | `r-007bacc26e9c06940666` | `r-c7352738bee39186b940` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-007bacc26e9c06940666` | `r-c7352738bee39186b940` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -15.992164611815952 | 1.77599 | 0.710809 | `r-2e016fe90119b688bc84` | `r-5fd1abd1635b12189555` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 84.2643203750593 | 86.99682998798497 | 2.73251 | 1.68529 | `r-2e016fe90119b688bc84` | `r-5fd1abd1635b12189555` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 14.389999999859072 | 13.42 | 0.5562 | `r-2e016fe90119b688bc84` | `r-5fd1abd1635b12189555` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 103.46000000225831 | 9.18 | 2.2528 | `r-2e016fe90119b688bc84` | `r-5fd1abd1635b12189555` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 21.0 | 2 | 0.5 | `r-2e016fe90119b688bc84` | `r-5fd1abd1635b12189555` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 377.6199999995288 | 23.11 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-4377e518a02c35c5fea5` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-0cd5f319bb80295395e1` | `r-4377e518a02c35c5fea5` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -17.906005859375 | -19.575790405273438 | 1.66978 | 0.8953 | `r-35777975476ff8854a8b` | `r-be0967ee585ff9a4a794` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 84.03120803962754 | 114.55339050510173 | 30.5222 | 1.68062 | `r-35777975476ff8854a8b` | `r-be0967ee585ff9a4a794` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 2.7199999998696853 | 2.76 | 0.5 | `r-35777975476ff8854a8b` | `r-be0967ee585ff9a4a794` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -14.07454556137769 | 1.71957 | 0.619534 | `r-05c666388af07453703e` | `r-db3a334ecdd89c1a95e5` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 84.60015106199378 | 87.363605499252 | 2.76345 | 1.69088 | `r-05c666388af07453703e` | `r-db3a334ecdd89c1a95e5` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 8.390000000001638 | 7.13 | 0.5 | `r-05c666388af07453703e` | `r-db3a334ecdd89c1a95e5` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.022539444027047335 | 0.00215149 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-6d679209076eaf56e145` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -14.936599731445312 | 1.74448 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-a9a321dfa35c35e0dbdc` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 84.47930145405832 | 87.2525596632073 | 2.77326 | 1.68894 | `r-0241c17b5ff2297d2a17` | `r-a9a321dfa35c35e0dbdc` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 10.209999999862873 | 8.96 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-a9a321dfa35c35e0dbdc` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 71.9099999999346 | 7.61 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-a9a321dfa35c35e0dbdc` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 8.0 | 1 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-a9a321dfa35c35e0dbdc` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -15.977272033691406 | 1.77742 | 0.710809 | `r-002bf860824963a1f621` | `r-8082c98631d7760454cc` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.2574310317606 | 86.94264984275091 | 2.68522 | 1.68529 | `r-002bf860824963a1f621` | `r-8082c98631d7760454cc` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 14.359999999859099 | 13.41 | 0.5562 | `r-002bf860824963a1f621` | `r-8082c98631d7760454cc` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 103.43000000225766 | 9.19 | 2.2528 | `r-002bf860824963a1f621` | `r-8082c98631d7760454cc` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 21.0 | 2 | 0.5 | `r-002bf860824963a1f621` | `r-8082c98631d7760454cc` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 377.5699999995288 | 23.11 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-541c810cb87fd09efd11` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 10.0 | 1 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-541c810cb87fd09efd11` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -17.89281463623047 | -19.564239501953125 | 1.67142 | 0.8953 | `r-aac3ae71b1a6189ef4f4` | `r-83d0b2be9022b6315894` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 84.07723236217922 | 114.53056717141888 | 30.4533 | 1.68062 | `r-aac3ae71b1a6189ef4f4` | `r-83d0b2be9022b6315894` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 2.7099999998696944 | 2.75 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-83d0b2be9022b6315894` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
