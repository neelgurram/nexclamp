# m-duplicate_conductance-4e2ab48a04

- model: `pospischil2008_rs`
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260913, "new_id": "IM_all_dup", "source_id": "IM_all"}`
- recorded edits: `[{"file": "NeuroML2/cells/RS/RS.cell.nml", "locator": "/neuroml[@id='RS']/cell[@id='RS']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='IM_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"0.07 mS_per_cm2\" id=\"IM_all_dup\" ionChannel=\"IM\" ion=\"k\" erev=\"-100.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1911.872 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.2988218828985024 | None |  | 0.0298822 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | baseline_voltage | exceeds | -70.57644285583496 | -71.08610289764404 | 0.50966 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | firing_regime | categorical | adapting | tonic |  |  | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | first_isi | exceeds | 28.06999999997447 | 77.88999999992916 | 49.82 | 0.5614 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 20.749999999853287 | 22.75999999985146 | 2.01 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | last_isi | exceeds | 135.97999999987638 | 77.88999999992916 | 58.09 | 2.7196 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | mean_frequency | exceeds | 17.03113291098414 | 19.870839543014004 | 2.83971 | 0.851557 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P00_canonical | spike_count | exceeds | 5.0 | 2.0 | 3 | 0.5 | `r-5171ec6a0414fa8c47f8` | `r-49b2ad28ca42aa3097ef` |
| h/1 | P01_baseline | baseline_voltage | exceeds | -70.57644295501709 | -71.08610312652588 | 0.50966 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P02_weak_step | baseline_voltage | exceeds | -70.57644295501709 | -71.08610312652588 | 0.50966 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -61.915689658355596 | -63.125348459625116 | 1.20966 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P02_weak_step | voltage_deflection | exceeds | 8.66075329666149 | 7.960754666900769 | 0.699999 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.6040912505976367 | 0.0434397 | 0.011213 | `s-e75f45f43aa09d678807` | `s-8d2c264b5d8945ec4e81` |
| h/1 | P04_step_2x | adaptation_index | exceeds | 0.018020491828063687 | 0.12800947404320187 | 0.109989 | 0.01 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P04_step_2x | firing_regime | categorical | tonic | adapting |  |  | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P04_step_2x | first_isi | exceeds | 13.069999999988113 | 14.949999999986403 | 1.88 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P04_step_2x | last_isi | exceeds | 28.16999999997438 | 89.87999999991825 | 61.71 | 0.5634 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P04_step_2x | mean_frequency | exceeds | 44.11292909854356 | 20.048115477169087 | 24.0648 | 2.20565 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P04_step_2x | spike_count | exceeds | 22.0 | 9.0 | 13 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P05_long_step | adaptation_index | definedness | 0.02130270892949869 | None |  | 0.01 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P05_long_step | burst_count | definedness | 1.0 | None |  | 0.5 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P05_long_step | first_isi | exceeds | 21.2199999999807 | 30.109999999972615 | 8.89 | 0.6 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 16.619999999857043 | 17.77999999985599 | 1.16 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P05_long_step | last_isi | exceeds | 78.13000000170541 | 30.109999999972615 | 48.02 | 1.5626 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P05_long_step | mean_frequency | exceeds | 14.694109182274286 | 41.7623721028849 | 27.0683 | 0.734705 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P05_long_step | spike_count | exceeds | 29.0 | 2.0 | 27 | 0.5 | `r-6299bd8dadd5e9592d63` | `r-af0d1618ec98250bbca5` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 381.69999999952506 | 434.4199999994771 | 52.72 | 7.634 | `r-7054f91d1e6b5f4b29f8` | `r-8353565c8131aa86a5a6` |
| h/1 | P06_ramp | mean_frequency | exceeds | 30.288956646438177 | 16.019543843505677 | 14.2694 | 1.51445 | `r-7054f91d1e6b5f4b29f8` | `r-8353565c8131aa86a5a6` |
| h/1 | P06_ramp | spike_count | exceeds | 30.0 | 16.0 | 14 | 0.5 | `r-7054f91d1e6b5f4b29f8` | `r-8353565c8131aa86a5a6` |
| h/1 | P07_hyperpolarizing_step | baseline_voltage | exceeds | -70.57644295501709 | -71.08610312652588 | 0.50966 | 0.5 | `r-0c0f3a761516cf334965` | `r-4cc6b84ec4a94fe06e02` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.4308354873657265 | -2.587038352966303 | 1.1562 | 0.5 | `r-4a031cb8037cbebd46bc` | `r-3f6c504aff407fe58b27` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.2989579287624928 | None |  | 0.0298822 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | baseline_voltage | exceeds | -70.57644283040365 | -71.08610286712647 | 0.50966 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | firing_regime | categorical | adapting | tonic |  |  | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | first_isi | exceeds | 28.029999999974507 | 77.4099999999296 | 49.38 | 0.5614 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 20.739999999853296 | 22.749999999851468 | 2.01 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | last_isi | exceeds | 135.78999999987656 | 77.4099999999296 | 58.38 | 2.7196 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | mean_frequency | exceeds | 17.059606264310375 | 19.96805111825451 | 2.90844 | 0.851557 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P00_canonical | spike_count | exceeds | 5.0 | 2.0 | 3 | 0.5 | `r-35d4f8d415fe0d06a895` | `r-1e4ab09cd531ecff4a83` |
| h/2 | P01_baseline | baseline_voltage | exceeds | -70.5764428838094 | -71.08610297648111 | 0.50966 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P02_weak_step | baseline_voltage | exceeds | -70.5764428838094 | -71.08610297648111 | 0.50966 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -61.91568922958361 | -63.12534712142929 | 1.20966 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P02_weak_step | voltage_deflection | exceeds | 8.660753654225793 | 7.960755855051822 | 0.699998 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.5606515948364182 | 0.6040912505976367 | 0.0434397 | 0.011213 | `s-3f9a22347a7b118b5e38` | `s-8ddaf91e831a3aeac86b` |
| h/2 | P04_step_2x | adaptation_index | exceeds | 0.018206269147133136 | 0.1287328723591699 | 0.110527 | 0.01 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P04_step_2x | firing_regime | categorical | tonic | adapting |  |  | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P04_step_2x | first_isi | exceeds | 12.92999999998824 | 14.789999999986549 | 1.86 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P04_step_2x | last_isi | exceeds | 28.06999999997447 | 89.66999999991845 | 61.6 | 0.5634 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P04_step_2x | mean_frequency | exceeds | 44.38974193423394 | 20.173944230276078 | 24.2158 | 2.20565 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P04_step_2x | spike_count | exceeds | 22.0 | 9.0 | 13 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P05_long_step | adaptation_index | definedness | 0.021450084876352596 | None |  | 0.01 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P05_long_step | burst_count | definedness | 1.0 | None |  | 0.5 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P05_long_step | first_isi | exceeds | 21.019999999980882 | 29.809999999972888 | 8.79 | 0.6 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 16.58999999985707 | 17.739999999856025 | 1.15 | 0.5 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P05_long_step | last_isi | exceeds | 77.97000000170192 | 29.809999999972888 | 48.16 | 1.5626 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P05_long_step | mean_frequency | exceeds | 14.734349834088421 | 42.06098843337952 | 27.3266 | 0.734705 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P05_long_step | spike_count | exceeds | 29.0 | 2.0 | 27 | 0.5 | `r-a71c890435a70aeaf61b` | `r-7cf6aeec272788ae6bde` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 381.6399999995251 | 434.36999999947716 | 52.73 | 7.634 | `r-2c42dd73d53f21fe7690` | `r-881eb79a8f6ce80c72ad` |
| h/2 | P06_ramp | mean_frequency | exceeds | 30.358227079570092 | 16.03929627589254 | 14.3189 | 1.51445 | `r-2c42dd73d53f21fe7690` | `r-881eb79a8f6ce80c72ad` |
| h/2 | P06_ramp | spike_count | exceeds | 30.0 | 16.0 | 14 | 0.5 | `r-2c42dd73d53f21fe7690` | `r-881eb79a8f6ce80c72ad` |
| h/2 | P07_hyperpolarizing_step | baseline_voltage | exceeds | -70.5764428838094 | -71.08610297648111 | 0.50966 | 0.5 | `r-13ae588754662eb409bf` | `r-30cee6eaed6d659d2047` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.3990133539835625 | -2.5561241963704475 | 1.15711 | 0.5 | `r-fa41d650658e23c878d5` | `r-dbcab50abd13b5146278` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
