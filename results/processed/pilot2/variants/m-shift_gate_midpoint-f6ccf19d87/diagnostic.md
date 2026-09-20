# m-shift_gate_midpoint-f6ccf19d87

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/forwardRate[1]", "new": "-50mV", "old": "-45mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/reverseRate[1]", "new": "-50mV", "old": "-45mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/steadyState[1]", "new": "12.5mV", "old": "17.5mV"}], "channel": "kamt", "delta_mV": -5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates_and_steady_state"}`
- recorded edits: `[{"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-45mV", "new": "-50mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-45mV", "new": "-50mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "NeuroML2/Channels/kamt.channel.nml", "locator": "/neuroml[@id='kamt']/ionChannel[@id='kamt']/gate[@id='m']/steadyState[1]", "attribute": "midpoint", "old": "17.5mV", "new": "12.5mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1746.76 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -12.39068603515625 | -13.895318899581682 | 1.50463 | 0.619534 | `r-fdc29d572ab8d33a1f37` | `r-50c19291728e4b370388` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 16.710000000001266 | 1.13 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-50c19291728e4b370388` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -58.44957622985835 | -59.98505079269405 | 1.53547 | 0.5 | `r-007bacc26e9c06940666` | `r-9ba7db60b19ad4bf7643` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.028925619834710745 | 0.00423468 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-6cac837bba73b915bafa` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -13.209152221679446 | -14.454392143249748 | 1.24524 | 0.660458 | `r-007bacc26e9c06940666` | `r-9ba7db60b19ad4bf7643` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 20.939999999853114 | 1.74 | 0.5 | `r-007bacc26e9c06940666` | `r-9ba7db60b19ad4bf7643` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 103.84999999990555 | 24.32 | 1.5906 | `r-007bacc26e9c06940666` | `r-9ba7db60b19ad4bf7643` |
| h/1 | P04_step_2x | spike_count | exceeds | 7.0 | 5.0 | 2 | 0.5 | `r-007bacc26e9c06940666` | `r-9ba7db60b19ad4bf7643` |
| h/1 | P05_long_step | adaptation_index | exceeds | 0.005414466597953451 | 0.019986322789762364 | 0.0145719 | 0.01 | `r-2e016fe90119b688bc84` | `r-bdd5649b3372528d4d68` |
| h/1 | P05_long_step | ahp_depth | exceeds | -14.216171264648949 | -15.360558219909663 | 1.14439 | 0.710809 | `r-2e016fe90119b688bc84` | `r-bdd5649b3372528d4d68` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 32.08999999984297 | 4.28 | 0.5562 | `r-2e016fe90119b688bc84` | `r-bdd5649b3372528d4d68` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 218.3500000012384 | 105.71 | 2.2528 | `r-2e016fe90119b688bc84` | `r-bdd5649b3372528d4d68` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 10.0 | 9 | 0.5 | `r-2e016fe90119b688bc84` | `r-bdd5649b3372528d4d68` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 489.0499999994274 | 88.32 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-f866b88db477f6fa4cc0` |
| h/1 | P06_ramp | spike_count | exceeds | 9.0 | 6.0 | 3 | 0.5 | `r-0cd5f319bb80295395e1` | `r-f866b88db477f6fa4cc0` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 6.039999999866666 | 0.56 | 0.5 | `r-35777975476ff8854a8b` | `r-75d1f697a3a20066761c` |
| h/2 | P00_canonical | ahp_depth | exceeds | -12.354972194083288 | -13.866768452658576 | 1.5118 | 0.619534 | `r-05c666388af07453703e` | `r-22f4dbb7c9fb2aed5007` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 16.650000000001278 | 1.13 | 0.5 | `r-05c666388af07453703e` | `r-22f4dbb7c9fb2aed5007` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -58.449576139068554 | -59.98505069808955 | 1.53547 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d90068ee1e8efd7a3b2b` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.028925619834710745 | 0.00423468 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-d08d27900c471e162eb5` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -13.192115783691406 | -14.440849973042802 | 1.24873 | 0.660458 | `r-0241c17b5ff2297d2a17` | `r-d90068ee1e8efd7a3b2b` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 20.919999999853133 | 1.75 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d90068ee1e8efd7a3b2b` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 103.82999999990557 | 24.31 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-d90068ee1e8efd7a3b2b` |
| h/2 | P04_step_2x | spike_count | exceeds | 7.0 | 5.0 | 2 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-d90068ee1e8efd7a3b2b` |
| h/2 | P05_long_step | adaptation_index | exceeds | 0.0054122174080685195 | 0.01995127481345323 | 0.0145391 | 0.01 | `r-002bf860824963a1f621` | `r-de708f2b5201608c9df8` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.199851989746094 | -15.347733212787858 | 1.14788 | 0.710809 | `r-002bf860824963a1f621` | `r-de708f2b5201608c9df8` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 32.04999999984301 | 4.28 | 0.5562 | `r-002bf860824963a1f621` | `r-de708f2b5201608c9df8` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 218.1500000012045 | 105.53 | 2.2528 | `r-002bf860824963a1f621` | `r-de708f2b5201608c9df8` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 10.0 | 9 | 0.5 | `r-002bf860824963a1f621` | `r-de708f2b5201608c9df8` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 488.9999999994275 | 88.32 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-db62125758a3e3b0c13c` |
| h/2 | P06_ramp | spike_count | exceeds | 9.0 | 6.0 | 3 | 0.5 | `r-046a6f9c0b3cbbc75058` | `r-db62125758a3e3b0c13c` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 6.009999999866693 | 0.55 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-9f3be86f1ad8f7c56eee` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
