# m-shift_reversal-ddf3b19e3e

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / shift_reversal
- parameters: `{"changes": [{"attribute": "erev", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_all']", "new": "40.0 mV", "old": "50.0 mV"}], "element": "channelDensity", "element_id": "nax_all", "generator_seed": 20260917, "shift_mV": -10.0}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='nax_all']", "attribute": "erev", "old": "50.0 mV", "new": "40.0 mV", "action": "set", "note": "shift_reversal"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3154.888 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 2.934501355031549e-13 |  | inf | `r-1855c6a207dcec8ed210` | `r-974a9020723c8ea2d64c` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -7.74336159169971 | 4.11147 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-974a9020723c8ea2d64c` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.14028549194009 | 92.09672927856468 | 8.04356 | 2.00281 | `r-1855c6a207dcec8ed210` | `r-974a9020723c8ea2d64c` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 17.700000000006867 | 0.63 | 0.5 | `r-1855c6a207dcec8ed210` | `r-974a9020723c8ea2d64c` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-974a9020723c8ea2d64c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006488627825968173 | 6.83013e-05 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-84811ebda5852e10d856` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -11.095191955566406 | 3.68056 | 0.738788 | `r-0925b86f96a976919154` | `r-e1c9beed717f52ec0808` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 100.46828841971717 | 92.19281005832961 | 8.27548 | 2.00937 | `r-0925b86f96a976919154` | `r-e1c9beed717f52ec0808` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 17.849999999855925 | 1.78 | 0.5 | `r-0925b86f96a976919154` | `r-e1c9beed717f52ec0808` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 42.55999999996129 | 2.5 | 0.8012 | `r-0925b86f96a976919154` | `r-e1c9beed717f52ec0808` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-0925b86f96a976919154` | `r-e1c9beed717f52ec0808` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -11.458969116211179 | 3.61426 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-ed249b9790903eef1198` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 100.41315077975412 | 92.06808471289084 | 8.34507 | 2.00826 | `r-4ab59c3e1336e488abd6` | `r-ed249b9790903eef1198` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 27.249999999847375 | 4.1 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-ed249b9790903eef1198` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 59.27000000129374 | 7.76 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-ed249b9790903eef1198` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 34.0 | 5 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-ed249b9790903eef1198` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 445.9599999994666 | 49.75 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-6517474d3e071c1cd3df` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 14.0 | 2 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-6517474d3e071c1cd3df` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -16.001159667968338 | -12.661247253417756 | 3.33991 | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-0a6a687d2bc775984fdc` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 100.17234039630091 | 92.02428817797458 | 8.14805 | 2.00345 | `r-86c7a89ca0bbba8e93d0` | `r-0a6a687d2bc775984fdc` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 0.0005652911252221865 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-032f0519dce6b5ca99c3` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -7.6895111994956835 | 4.11456 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-032f0519dce6b5ca99c3` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 100.07681274416072 | 91.97760391232106 | 8.09921 | 2.00281 | `r-1c8cea9109ae2bf6fdec` | `r-032f0519dce6b5ca99c3` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 17.700000000006845 | 0.62 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-032f0519dce6b5ca99c3` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-032f0519dce6b5ca99c3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.0006488627825968173 | 6.83013e-05 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-5b275350a8facb76bd15` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -10.861862182616278 | 3.69203 | 0.738788 | `r-6797defd923ff2562240` | `r-01e7d0b4d39d7df37994` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 100.0564460769101 | 91.90334701721575 | 8.1531 | 2.00937 | `r-6797defd923ff2562240` | `r-01e7d0b4d39d7df37994` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 17.80999999985596 | 1.78 | 0.5 | `r-6797defd923ff2562240` | `r-01e7d0b4d39d7df37994` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 42.56999999996128 | 2.52 | 0.8012 | `r-6797defd923ff2562240` | `r-01e7d0b4d39d7df37994` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 12.0 | 1 | 0.5 | `r-6797defd923ff2562240` | `r-01e7d0b4d39d7df37994` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -11.232734680175781 | 3.62406 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-279ad7cc70ba14747d95` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 100.03872680731578 | 91.87953186186289 | 8.15919 | 2.00826 | `r-a3b84bbc3dc843d0e573` | `r-279ad7cc70ba14747d95` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 27.209999999847412 | 4.1 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-279ad7cc70ba14747d95` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 59.38000000129614 | 7.82 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-279ad7cc70ba14747d95` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 34.0 | 5 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-279ad7cc70ba14747d95` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 445.8999999994667 | 49.75 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-a7d72173c81c6a402a1e` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 14.0 | 2 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-a7d72173c81c6a402a1e` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -15.791358947753906 | -12.443336486816406 | 3.34802 | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-118cc966eee4e5b23f70` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 99.86314392274174 | 91.77345275907561 | 8.08969 | 2.00345 | `r-2e410d8c71a4df0466e8` | `r-118cc966eee4e5b23f70` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
