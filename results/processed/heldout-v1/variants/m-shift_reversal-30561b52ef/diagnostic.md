# m-shift_reversal-30561b52ef

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "new": "40.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "nap_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "attribute": "erev", "old": "50.0 mV", "new": "40.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8001.26 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.5216693418942094 | None |  | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-8bda1e276eb2f7b6b6fd` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 7.78999999999845 | 15.91 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-8bda1e276eb2f7b6b6fd` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-8bda1e276eb2f7b6b6fd` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.06314459394850079 | 0.00170753 | 0.00122874 | `s-fa4d0c2502716e8c3739` | `s-58739cadc00b994ae8fd` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 30.199999999844692 | 1.1 | 0.582 | `r-96e71f2e3b8549494d50` | `r-c81d52890d74838d2d97` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 44.78999999983142 | 1.9 | 0.8578 | `r-74af15e68cf19cbae102` | `r-648e80c2ad1c5b9aaec5` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 26.590000000580403 | 2.12 | 1.11 | `r-74af15e68cf19cbae102` | `r-648e80c2ad1c5b9aaec5` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 77.0 | 6 | 3 | `r-74af15e68cf19cbae102` | `r-648e80c2ad1c5b9aaec5` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 382.869999999524 | 392.90999999951487 | 10.04 | 7.6574 | `r-6afcc4c87334b55f282e` | `r-56cb7b318b9aedb3f1db` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.5214881334190068 | None |  | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-234111c237f28ef84942` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 7.78999999999845 | 15.93 | 0.5 | `r-87bcc3cd30685deaf603` | `r-234111c237f28ef84942` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-87bcc3cd30685deaf603` | `r-234111c237f28ef84942` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.06314459394850079 | 0.00170753 | 0.00122874 | `s-54b0d60082a59a1582ae` | `s-ea6fdc46f4cdffd9e25d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 29.029999999845757 | 30.119999999844765 | 1.09 | 0.582 | `r-6290d36f97e6ddeb2b58` | `r-937c37df574bca0f6e94` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 44.71999999983149 | 1.9 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-440d80906c8d2f58cecd` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 27.000000000589353 | 2.16 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-440d80906c8d2f58cecd` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 76.0 | 6 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-440d80906c8d2f58cecd` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 382.78999999952407 | 392.82999999951494 | 10.04 | 7.6574 | `r-ce6273bb85e534e50ecc` | `r-9e4bb7c72170219e0d49` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
