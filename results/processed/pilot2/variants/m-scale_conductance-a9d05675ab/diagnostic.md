# m-scale_conductance-a9d05675ab

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `migliore2014_mt_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "new": "0.07499997 mS_per_cm2", "old": "0.0833333 mS_per_cm2"}], "element": "channelDensity", "element_id": "pas_ModelViewParmSubset_1", "factor": 0.9, "generator_seed": 20260917}`
- recorded edits: `[{"file": "NeuroML2/Channels/test/MT_soma.cell.nml", "locator": "/neuroml[@id='MT_soma']/cell[@id='MT_soma']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_ModelViewParmSubset_1']", "attribute": "condDensity", "old": "0.0833333 mS_per_cm2", "new": "0.07499997 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 3988.199 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.023222457482412404 | 0.00146848 | 0.000493819 | `s-41b22c8fa120e2b12315` | `s-8f9915357200910cd610` |
| h/1 | P04_step_2x | last_isi | exceeds | 79.52999999992767 | 76.46999999993045 | 3.06 | 1.5906 | `r-007bacc26e9c06940666` | `r-a57600213a0c33d371cd` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 27.809999999846866 | 26.779999999847803 | 1.03 | 0.5562 | `r-2e016fe90119b688bc84` | `r-a2e2a0961c627f676847` |
| h/1 | P05_long_step | last_isi | exceeds | 112.64000000245869 | 104.30000000227665 | 8.34 | 2.2528 | `r-2e016fe90119b688bc84` | `r-a2e2a0961c627f676847` |
| h/1 | P05_long_step | spike_count | exceeds | 19.0 | 20.0 | 1 | 0.5 | `r-2e016fe90119b688bc84` | `r-a2e2a0961c627f676847` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 400.72999999950775 | 380.1099999995265 | 20.62 | 8.0146 | `r-0cd5f319bb80295395e1` | `r-8b8b64a9718ec383a1be` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -81.01395223693858 | -83.01469571838389 | 2.00074 | 0.5 | `r-007bacc26e9c06940666` | `r-a57600213a0c33d371cd` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.024690936411447307 | 0.023222457482412404 | 0.00146848 | 0.000493819 | `s-2231bc09093d4c365d9c` | `s-d8ac7e19d98ab3e2db34` |
| h/2 | P04_step_2x | last_isi | exceeds | 79.51999999992768 | 76.45999999993046 | 3.06 | 1.5906 | `r-0241c17b5ff2297d2a17` | `r-bf97f08b1ee66e7453d7` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 27.769999999846902 | 26.74999999984783 | 1.02 | 0.5562 | `r-002bf860824963a1f621` | `r-b1bcd74f42bbeaf05dd0` |
| h/2 | P05_long_step | last_isi | exceeds | 112.62000000245826 | 104.27000000227599 | 8.35 | 2.2528 | `r-002bf860824963a1f621` | `r-b1bcd74f42bbeaf05dd0` |
| h/2 | P05_long_step | spike_count | exceeds | 19.0 | 20.0 | 1 | 0.5 | `r-002bf860824963a1f621` | `r-b1bcd74f42bbeaf05dd0` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 400.6799999995078 | 380.06999999952654 | 20.61 | 8.0146 | `r-046a6f9c0b3cbbc75058` | `r-5aca9b23a841b9e88fc8` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -81.01395266571055 | -83.01469614868175 | 2.00074 | 0.5 | `r-0241c17b5ff2297d2a17` | `r-bf97f08b1ee66e7453d7` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
