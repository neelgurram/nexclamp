# m-shift_reversal-71f7c0a79f

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kap_all']", "new": "-85.0 mV", "old": "-90.0 mV"}], "element": "channelDensity", "element_id": "kap_all", "generator_seed": 20260917, "shift_mV": 5.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='kap_all']", "attribute": "erev", "old": "-90.0 mV", "new": "-85.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3120.188 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 0.0002781641171205756 |  | inf | `r-1855c6a207dcec8ed210` | `r-b995f2f0b2a8597ae082` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 4.900000000001093 | 0.52 | 0.5 | `r-1855c6a207dcec8ed210` | `r-b995f2f0b2a8597ae082` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-b995f2f0b2a8597ae082` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -64.21164719696043 | 0.81118 | 0.5 | `r-0925b86f96a976919154` | `r-7cc38a968fbe51922a1b` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.00040980807321904243 | 0.000170753 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-8288d097c546630a56ba` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 13.219999999860136 | 2.85 | 0.5 | `r-0925b86f96a976919154` | `r-7cc38a968fbe51922a1b` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 36.309999999966976 | 3.75 | 0.8012 | `r-0925b86f96a976919154` | `r-7cc38a968fbe51922a1b` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 14.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-7cc38a968fbe51922a1b` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 17.639999999856116 | 5.51 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-08e7b035cec388749fe6` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 43.81000000095628 | 7.7 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-08e7b035cec388749fe6` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 46.0 | 7 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-08e7b035cec388749fe6` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 292.2499999996064 | 103.96 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-d0cde39fb7a783f8d138` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 19.0 | 3 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-d0cde39fb7a783f8d138` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.0002783189538117528 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-379cf78d2aca3acc9179` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 4.890000000001091 | 0.52 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-379cf78d2aca3acc9179` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-379cf78d2aca3acc9179` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -64.21164711456296 | 0.81118 | 0.5 | `r-6797defd923ff2562240` | `r-b73cdfba06761da00c5b` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.00040980807321904243 | 0.000170753 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-9329e93dced56e62b48d` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 13.169999999860181 | 2.86 | 0.5 | `r-6797defd923ff2562240` | `r-b73cdfba06761da00c5b` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 36.289999999966994 | 3.76 | 0.8012 | `r-6797defd923ff2562240` | `r-b73cdfba06761da00c5b` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 14.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-b73cdfba06761da00c5b` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 17.599999999856152 | 5.51 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-1d285d0ac91da16d93ab` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 43.8200000009565 | 7.74 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-1d285d0ac91da16d93ab` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 46.0 | 7 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-1d285d0ac91da16d93ab` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 292.18999999960647 | 103.96 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-f58547650496ca68c98d` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 19.0 | 3 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-f58547650496ca68c98d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
