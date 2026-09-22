# m-wrong_channel-9f2bfc0fc0

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / wrong_channel
- parameters: `{"changes": [{"attribute": "ionChannel", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "new": "kc", "old": "pas"}], "element_id": "pas_all", "generator_seed": 20260917, "new_species": "k", "old_species": "non_specific"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pas_all']", "attribute": "ionChannel", "old": "pas", "new": "kc", "action": "set", "note": "wrong_channel"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8327.831 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.5216693418942094 | 0.04045318200486847 | 0.481216 | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-f1392278ff4e775f8634` |
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -6.552830330767989 | 1.69558 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-f1392278ff4e775f8634` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 74.70865440368996 | 73.09142112730957 | 1.61723 | 1.49417 | `r-068a1eafd4afbbd6d23e` | `r-f1392278ff4e775f8634` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 9.290000000002237 | 14.41 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-f1392278ff4e775f8634` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 7.0 | 3 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-f1392278ff4e775f8634` |
| h/1 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-96e71f2e3b8549494d50` | `r-390026cf8d1262b5a658` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -63.19053124313325 | -60.06039347457852 | 3.13014 | 0.5 | `r-96e71f2e3b8549494d50` | `r-390026cf8d1262b5a658` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.029096373198552013 | 0.0323407 | 0.00122874 | `s-fa4d0c2502716e8c3739` | `s-7596c79c036591637597` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -3.06435100805065 | -10.44649996692614 | 7.38215 | 1.14578 | `r-96e71f2e3b8549494d50` | `r-390026cf8d1262b5a658` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 2.8099999998696035 | 26.29 | 0.582 | `r-96e71f2e3b8549494d50` | `r-390026cf8d1262b5a658` |
| h/1 | P04_step_2x | spike_count | exceeds | 51.0 | 75.0 | 24 | 3 | `r-96e71f2e3b8549494d50` | `r-390026cf8d1262b5a658` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 31.539999999843474 | 11.35 | 0.8578 | `r-74af15e68cf19cbae102` | `r-9ebd87a185e72725501e` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 9.800000000213913 | 14.67 | 1.11 | `r-74af15e68cf19cbae102` | `r-9ebd87a185e72725501e` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 204.0 | 121 | 3 | `r-74af15e68cf19cbae102` | `r-9ebd87a185e72725501e` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 382.869999999524 | 192.52999999969705 | 190.34 | 7.6574 | `r-6afcc4c87334b55f282e` | `r-8e2fb92a831d51f7b835` |
| h/1 | P06_ramp | spike_count | exceeds | 70.0 | 104.0 | 34 | 3 | `r-6afcc4c87334b55f282e` | `r-8e2fb92a831d51f7b835` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -74.16547203826991 | -76.56372692108327 | 2.39825 | 0.5 | `r-96e71f2e3b8549494d50` | `r-390026cf8d1262b5a658` |
| h/1 | P08_rebound | first_spike_latency | definedness | None | 145.1099999992855 |  | inf | `r-ed128acffbbbc221d4ab` | `r-a770aad45497472caa3a` |
| h/1 | P08_rebound | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-ed128acffbbbc221d4ab` | `r-a770aad45497472caa3a` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.5214881334190068 | 0.04045270689571032 | 0.481035 | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-b77b2619cd51fbb11e3e` |
| h/2 | P00_canonical | ahp_depth | exceeds | -8.213585962703469 | -6.5205452382862745 | 1.69304 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b77b2619cd51fbb11e3e` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 74.66815185545984 | 73.10600471497332 | 1.56215 | 1.49417 | `r-87bcc3cd30685deaf603` | `r-b77b2619cd51fbb11e3e` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 9.29000000000223 | 14.43 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b77b2619cd51fbb11e3e` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 7.0 | 3 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b77b2619cd51fbb11e3e` |
| h/2 | P02_weak_step | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-6290d36f97e6ddeb2b58` | `r-ae6261fe9c5b6d6ff256` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -63.19052997512787 | -60.05570283966032 | 3.13483 | 0.5 | `r-6290d36f97e6ddeb2b58` | `r-ae6261fe9c5b6d6ff256` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.029130523871320264 | 0.0323065 | 0.00122874 | `s-54b0d60082a59a1582ae` | `s-cf0278dca5935255e5dc` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -2.68242419940799 | -10.098895871428084 | 7.41647 | 1.14578 | `r-6290d36f97e6ddeb2b58` | `r-ae6261fe9c5b6d6ff256` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 29.029999999845757 | 2.7799999998696308 | 26.25 | 0.582 | `r-6290d36f97e6ddeb2b58` | `r-ae6261fe9c5b6d6ff256` |
| h/2 | P04_step_2x | spike_count | exceeds | 50.0 | 75.0 | 25 | 3 | `r-6290d36f97e6ddeb2b58` | `r-ae6261fe9c5b6d6ff256` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 31.5099999998435 | 11.31 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-3b1b8d42c9879300949b` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 9.840000000214786 | 15 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-3b1b8d42c9879300949b` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 202.0 | 120 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-3b1b8d42c9879300949b` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 382.78999999952407 | 192.54999999969704 | 190.24 | 7.6574 | `r-ce6273bb85e534e50ecc` | `r-10925f78f8c5f629ab53` |
| h/2 | P06_ramp | spike_count | exceeds | 69.0 | 104.0 | 35 | 3 | `r-ce6273bb85e534e50ecc` | `r-10925f78f8c5f629ab53` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -74.16546953735444 | -76.56798876953293 | 2.40252 | 0.5 | `r-6290d36f97e6ddeb2b58` | `r-ae6261fe9c5b6d6ff256` |
| h/2 | P08_rebound | first_spike_latency | definedness | None | 145.15999999928545 |  | inf | `r-aab2bd4eb57eabce6551` | `r-5d023191ba36ea3f8875` |
| h/2 | P08_rebound | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-aab2bd4eb57eabce6551` | `r-5d023191ba36ea3f8875` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
