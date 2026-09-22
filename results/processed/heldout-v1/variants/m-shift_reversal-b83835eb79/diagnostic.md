# m-shift_reversal-b83835eb79

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg2`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "new": "-85.0 mV", "old": "-95.0 mV"}], "element": "channelDensity", "element_id": "ka_all", "generator_seed": 20260917, "shift_mV": 10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_test2.cell.nml", "locator": "/neuroml[@id='TestSeg_test2']/cell[@id='TestSeg_test2']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='ka_all']", "attribute": "erev", "old": "-95.0 mV", "new": "-85.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4633.565 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -7.977452861728821 | -7.04652755889137 | 0.930925 | 0.5 | `r-a309e30f4eac6329447d` | `r-7ff5955eded069648ff5` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 76.03836822509587 | 77.95250511167974 | 1.91414 | 1.52077 | `r-a309e30f4eac6329447d` | `r-7ff5955eded069648ff5` |
| h/1 | P00_canonical | last_isi | exceeds | 7.590000000003883 | 7.020000000003591 | 0.57 | 0.5 | `r-a309e30f4eac6329447d` | `r-7ff5955eded069648ff5` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.11310723342887 | -61.672331110382 | 1.44078 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-ea0cec336fe0c961f09c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.011338023359060175 | 0.00577146 | 0.00034219 | `s-b9450aacc8ce67e5b927` | `s-71373c7f0160a528eee2` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 53.72999999982329 | 34.23999999984102 | 19.49 | 1.0746 | `r-531ed8bf9e8ec22d7778` | `r-ea0cec336fe0c961f09c` |
| h/1 | P04_step_2x | last_isi | exceeds | 25.62999999997669 | 19.309999999982438 | 6.32 | 1.29 | `r-531ed8bf9e8ec22d7778` | `r-ea0cec336fe0c961f09c` |
| h/1 | P04_step_2x | spike_count | exceeds | 18.0 | 25.0 | 7 | 0.5 | `r-531ed8bf9e8ec22d7778` | `r-ea0cec336fe0c961f09c` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 86.49999999979349 | 49.579999999827066 | 36.92 | 1.73 | `r-c181d8dc3f2e9e1a86cf` | `r-5c2608371a6ba05fb69b` |
| h/1 | P05_long_step | last_isi | exceeds | 46.560000001016306 | 29.300000000639557 | 17.26 | 2.61 | `r-c181d8dc3f2e9e1a86cf` | `r-5c2608371a6ba05fb69b` |
| h/1 | P05_long_step | spike_count | exceeds | 42.0 | 67.0 | 25 | 3 | `r-c181d8dc3f2e9e1a86cf` | `r-5c2608371a6ba05fb69b` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 435.03999999947655 | 320.5399999995807 | 114.5 | 8.7008 | `r-8c44150a9a017555d35c` | `r-fbb8f3a37287dabb404c` |
| h/1 | P06_ramp | spike_count | exceeds | 27.0 | 37.0 | 10 | 3 | `r-8c44150a9a017555d35c` | `r-fbb8f3a37287dabb404c` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -8.488179428100779 | -6.811621096247393 | 1.67656 | 1.08676 | `r-f411679bd6f2a1231337` | `r-f9566d8d57f6d821966b` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.911862463500448 | -6.979610462093852 | 0.932252 | 0.5 | `r-82914471c1c753634231` | `r-0ef27e24a22a83690a75` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 75.97283554077825 | 77.81970214843251 | 1.84687 | 1.52077 | `r-82914471c1c753634231` | `r-0ef27e24a22a83690a75` |
| h/2 | P00_canonical | last_isi | exceeds | 7.610000000003893 | 7.0300000000035965 | 0.58 | 0.5 | `r-82914471c1c753634231` | `r-0ef27e24a22a83690a75` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.11310686187736 | -61.67233046722404 | 1.44078 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-77f4ccc4f69d4a615a46` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.01710948705689502 | 0.011338023359060175 | 0.00577146 | 0.00034219 | `s-7aa0e6becefba73a0572` | `s-f167f95c82b1c19f8c5e` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 53.649999999823365 | 34.17999999984107 | 19.47 | 1.0746 | `r-c4e93fb668595b0fb26c` | `r-77f4ccc4f69d4a615a46` |
| h/2 | P04_step_2x | last_isi | exceeds | 26.0599999999763 | 19.699999999982083 | 6.36 | 1.29 | `r-c4e93fb668595b0fb26c` | `r-77f4ccc4f69d4a615a46` |
| h/2 | P04_step_2x | spike_count | exceeds | 18.0 | 25.0 | 7 | 0.5 | `r-c4e93fb668595b0fb26c` | `r-77f4ccc4f69d4a615a46` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 86.41999999979356 | 49.50999999982713 | 36.91 | 1.73 | `r-c41be102b8e8611b929c` | `r-7a8e6ef10cf24d5b165b` |
| h/2 | P05_long_step | last_isi | exceeds | 47.430000001035296 | 29.830000000651125 | 17.6 | 2.61 | `r-c41be102b8e8611b929c` | `r-7a8e6ef10cf24d5b165b` |
| h/2 | P05_long_step | spike_count | exceeds | 41.0 | 66.0 | 25 | 3 | `r-c41be102b8e8611b929c` | `r-7a8e6ef10cf24d5b165b` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 434.9599999994766 | 320.44999999958077 | 114.51 | 8.7008 | `r-11d8f8c83600b900cadc` | `r-5529e03a0eb5cdc956ea` |
| h/2 | P06_ramp | spike_count | exceeds | 26.0 | 37.0 | 11 | 3 | `r-11d8f8c83600b900cadc` | `r-5529e03a0eb5cdc956ea` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -8.125927218107364 | -6.440526000955472 | 1.6854 | 1.08676 | `r-4bcc4e2fdcca97c21eee` | `r-68fcf85f32214dc99a72` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
