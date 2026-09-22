# m-duplicate_conductance-bbcb98adea

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "kc_fast_all_dup", "source_id": "kc_fast_all"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/TestSeg_all.cell.nml", "locator": "/neuroml[@id='TestSeg_all']/cell[@id='TestSeg_all']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kc_fast_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"2.0 mS_per_cm2\" id=\"kc_fast_all_dup\" ionChannel=\"kc_fast\" ion=\"k\" erev=\"-95.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8324.571 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.5216693418942094 | None |  | 0.0521669 | `r-068a1eafd4afbbd6d23e` | `r-1e8d22cd5663b437302b` |
| h/1 | P00_canonical | ahp_depth | exceeds | -8.248406196708032 | -8.936921855110413 | 0.688516 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-1e8d22cd5663b437302b` |
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 47.85999999999859 | 24.16 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-1e8d22cd5663b437302b` |
| h/1 | P00_canonical | spike_count | exceeds | 4.0 | 2.0 | 2 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-1e8d22cd5663b437302b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.07478997336247524 | 0.0133529 | 0.00122874 | `s-fa4d0c2502716e8c3739` | `s-ff4d7a293c572eb5930a` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 29.099999999845693 | 36.21999999983922 | 7.12 | 0.582 | `r-96e71f2e3b8549494d50` | `r-f526c22ca8239c807b57` |
| h/1 | P04_step_2x | spike_count | exceeds | 51.0 | 36.0 | 15 | 3 | `r-96e71f2e3b8549494d50` | `r-f526c22ca8239c807b57` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 42.88999999983315 | 58.57999999981888 | 15.69 | 0.8578 | `r-74af15e68cf19cbae102` | `r-c03fa8c4561c600f5263` |
| h/1 | P05_long_step | last_isi | exceeds | 24.470000000534128 | 60.100000001311855 | 35.63 | 1.11 | `r-74af15e68cf19cbae102` | `r-c03fa8c4561c600f5263` |
| h/1 | P05_long_step | spike_count | exceeds | 83.0 | 35.0 | 48 | 3 | `r-74af15e68cf19cbae102` | `r-c03fa8c4561c600f5263` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 382.869999999524 | 462.4599999994516 | 79.59 | 7.6574 | `r-6afcc4c87334b55f282e` | `r-10b9c18d70d501f979d5` |
| h/1 | P06_ramp | spike_count | exceeds | 70.0 | 56.0 | 14 | 3 | `r-6afcc4c87334b55f282e` | `r-10b9c18d70d501f979d5` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.5214881334190068 | None |  | 0.0521669 | `r-87bcc3cd30685deaf603` | `r-1077a35de8c60b09fbe2` |
| h/2 | P00_canonical | ahp_depth | exceeds | -8.213585962703469 | -8.901322246190816 | 0.687736 | 0.5 | `r-87bcc3cd30685deaf603` | `r-1077a35de8c60b09fbe2` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 47.8699999999986 | 24.15 | 0.5 | `r-87bcc3cd30685deaf603` | `r-1077a35de8c60b09fbe2` |
| h/2 | P00_canonical | spike_count | exceeds | 4.0 | 2.0 | 2 | 0.5 | `r-87bcc3cd30685deaf603` | `r-1077a35de8c60b09fbe2` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.06143706031008811 | 0.07478997336247524 | 0.0133529 | 0.00122874 | `s-54b0d60082a59a1582ae` | `s-240b66ffe0a007d95420` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 29.029999999845757 | 36.13999999983929 | 7.11 | 0.582 | `r-6290d36f97e6ddeb2b58` | `r-6a8fad7604d284a7c09b` |
| h/2 | P04_step_2x | spike_count | exceeds | 50.0 | 36.0 | 14 | 3 | `r-6290d36f97e6ddeb2b58` | `r-6a8fad7604d284a7c09b` |
| h/2 | P05_long_step | adaptation_index | exceeds | 0.0019247942670489696 | 0.012759895196898902 | 0.0108351 | 0.01 | `r-f1a8b6a7a66c54d9b827` | `r-b781055351df6846ded0` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 42.819999999833215 | 58.499999999818954 | 15.68 | 0.8578 | `r-f1a8b6a7a66c54d9b827` | `r-b781055351df6846ded0` |
| h/2 | P05_long_step | last_isi | exceeds | 24.840000000542204 | 60.71000000132517 | 35.87 | 1.11 | `r-f1a8b6a7a66c54d9b827` | `r-b781055351df6846ded0` |
| h/2 | P05_long_step | spike_count | exceeds | 82.0 | 35.0 | 47 | 3 | `r-f1a8b6a7a66c54d9b827` | `r-b781055351df6846ded0` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 382.78999999952407 | 462.3799999994517 | 79.59 | 7.6574 | `r-ce6273bb85e534e50ecc` | `r-e8907fa7f7d80db55da5` |
| h/2 | P06_ramp | spike_count | exceeds | 69.0 | 55.0 | 14 | 3 | `r-ce6273bb85e534e50ecc` | `r-e8907fa7f7d80db55da5` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
