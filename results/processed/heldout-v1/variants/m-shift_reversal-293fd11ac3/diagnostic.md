# m-shift_reversal-293fd11ac3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "new": "45.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "nap_all", "generator_seed": 20260917, "shift_mV": -5.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nap_all']", "attribute": "erev", "old": "50.0 mV", "new": "45.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8012.079 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.5216693418942094 | None |  | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-36051761fd8522397121` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 7.609999999998486 | 16.09 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-36051761fd8522397121` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-36051761fd8522397121` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 43.829999999832296 | 0.94 | 0.8578 | `r-74af15e68cf19cbae102` | `r-362a3084e57b5edd6775` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.5214881334190068 | None |  | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-b6398ef2ed6c77615e09` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 7.609999999998486 | 16.11 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b6398ef2ed6c77615e09` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 3.0 | 1 | 0.5 | `r-87bcc3cd30685deaf603` | `r-b6398ef2ed6c77615e09` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 43.75999999983236 | 0.94 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-752a498a9b92ab039a0b` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
