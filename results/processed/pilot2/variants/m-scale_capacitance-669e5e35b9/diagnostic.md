# m-scale_capacitance-669e5e35b9

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "1.44 uF_per_cm2", "old": "1.8 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "1.8 uF_per_cm2", "new": "1.44 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1749.056 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | first_spike_latency | exceeds | 15.58000000000149 | 12.730000000002057 | 2.85 | 0.5 | `r-fdc29d572ab8d33a1f37` | `r-120f8530adfa8a922fd5` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.023973772283313984 | 0.000717164 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-daa6be540226794ce7e0` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 19.199999999854697 | 15.609999999857962 | 3.59 | 0.5 | `r-007bacc26e9c06940666` | `r-f72145e1e9fec511aa6e` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 75.87999999993099 | 3.65 | 1.5906 | `r-007bacc26e9c06940666` | `r-f72145e1e9fec511aa6e` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 22.369999999851814 | 5.44 | 0.5562 | `r-2e016fe90119b688bc84` | `r-7e8725242f6c94d11736` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 108.72000000237313 | 3.92 | 2.2528 | `r-2e016fe90119b688bc84` | `r-7e8725242f6c94d11736` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 20.0 | 1 | 0.5 | `r-2e016fe90119b688bc84` | `r-7e8725242f6c94d11736` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 392.17999999951553 | 8.55 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-39ef3d49f08008ad894e` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 84.03120803962754 | 92.8362655652318 | 8.80506 | 1.68062 | `r-35777975476ff8854a8b` | `r-98ec10723ea69b73f411` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 5.479999999867175 | 4.019999999868503 | 1.46 | 0.5 | `r-35777975476ff8854a8b` | `r-98ec10723ea69b73f411` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 15.520000000001502 | 12.680000000002067 | 2.84 | 0.5 | `r-05c666388af07453703e` | `r-ca08b7944a573cbc965d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.023973772283313984 | 0.000717164 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-590129342b9ff8052586` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 19.169999999854724 | 15.57999999985799 | 3.59 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-b43223f7eed3639400ce` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 75.869999999931 | 3.65 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-b43223f7eed3639400ce` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 22.33999999985184 | 5.43 | 0.5562 | `r-002bf860824963a1f621` | `r-4b286348234c85dc9d07` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 108.69000000237247 | 3.93 | 2.2528 | `r-002bf860824963a1f621` | `r-4b286348234c85dc9d07` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 20.0 | 1 | 0.5 | `r-002bf860824963a1f621` | `r-4b286348234c85dc9d07` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 392.1299999995156 | 8.55 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-485606d8417ca2824ce3` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 84.07723236217922 | 92.90596771367652 | 8.82874 | 1.68062 | `r-aac3ae71b1a6189ef4f4` | `r-8259c9fd67ed0cbccdea` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 5.459999999867193 | 3.999999999868521 | 1.46 | 0.5 | `r-aac3ae71b1a6189ef4f4` | `r-8259c9fd67ed0cbccdea` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
