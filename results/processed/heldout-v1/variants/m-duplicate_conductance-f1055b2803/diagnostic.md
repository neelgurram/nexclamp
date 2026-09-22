# m-duplicate_conductance-f1055b2803

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / reference / duplicate_conductance
- parameters: `{"generator_seed": 20260917, "new_id": "kdr_all_dup", "source_id": "kdr_all"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kdr_all_dup']", "attribute": null, "old": null, "new": "<channelDensity xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" condDensity=\"10.0 mS_per_cm2\" id=\"kdr_all_dup\" ionChannel=\"kdr\" ion=\"k\" erev=\"-90.0 mV\"/>", "action": "insert", "note": "duplicate_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3432.248 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -16.481418173111507 | 4.62659 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-1e3a3480776f1a2c3ba4` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 19.40999999999641 | 1.08 | 0.5 | `r-1855c6a207dcec8ed210` | `r-1e3a3480776f1a2c3ba4` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006830134553650707 | 0.000102452 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-6666d6cd966cfa7696d4` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -18.76663208007767 | 3.99088 | 0.738788 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 17.57999999985617 | 1.51 | 0.5 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 41.39999999996235 | 1.34 | 0.8012 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-a8785fab935981a65bea` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -18.987228393554688 | 3.914 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 26.929999999847666 | 3.78 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 54.380000001187 | 2.87 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 37.0 | 2 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-1cb566d9fda5525060ab` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 450.2699999994627 | 54.06 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-2cffddf3dfc3582ebea9` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-2cffddf3dfc3582ebea9` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -19.589523315429474 | 3.58836 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-c42761bb1d9a1131e940` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -16.445875594865058 | 4.64181 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-59672825c4f64188d4d8` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 19.39999999999639 | 1.08 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-59672825c4f64188d4d8` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006830134553650707 | 0.000102452 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-11cf4a3784dc54f535fa` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -18.613143920897542 | 4.05925 | 0.738788 | `r-6797defd923ff2562240` | `r-3256d68c8a1e920295ba` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 17.529999999856216 | 1.5 | 0.5 | `r-6797defd923ff2562240` | `r-3256d68c8a1e920295ba` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 41.379999999962365 | 1.33 | 0.8012 | `r-6797defd923ff2562240` | `r-3256d68c8a1e920295ba` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-3256d68c8a1e920295ba` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -18.838096618652344 | 3.9813 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-f4ecdd0bf1d32003b82b` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 26.889999999847703 | 3.78 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-f4ecdd0bf1d32003b82b` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 54.400000001187436 | 2.84 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-f4ecdd0bf1d32003b82b` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 37.0 | 2 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-f4ecdd0bf1d32003b82b` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 450.20999999946275 | 54.06 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-cf31a11da43b7c52f19d` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 15.0 | 1 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-cf31a11da43b7c52f19d` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -15.791358947753906 | -19.44612121581949 | 3.65476 | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-33bf872b4fa1f5c4b77f` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
