# m-scale_conductance-5fc9665994

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pasCA1_all']", "new": "0.0714286 mS_per_cm2", "old": "0.0357143 mS_per_cm2"}], "element": "channelDensity", "element_id": "pasCA1_all", "factor": 2.0, "generator_seed": 20260917}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/SomaOnly_allCml.cell.nml", "locator": "/neuroml[@id='SomaOnly_allCml']/cell[@id='SomaOnly_allCml']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='pasCA1_all']", "attribute": "condDensity", "old": "0.0357143 mS_per_cm2", "new": "0.0714286 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3126.534 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 0.0002916302131315985 |  | inf | `r-1855c6a207dcec8ed210` | `r-4263f383788a27938e00` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -12.920240108053477 | 1.06541 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-4263f383788a27938e00` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 4.300000000000999 | 1.12 | 0.5 | `r-1855c6a207dcec8ed210` | `r-4263f383788a27938e00` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 17.150000000004873 | 1.18 | 0.5 | `r-1855c6a207dcec8ed210` | `r-4263f383788a27938e00` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-4263f383788a27938e00` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -62.94284074172971 | 2.07999 | 0.5 | `r-0925b86f96a976919154` | `r-49dfa8b5fa2efc7b9b44` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.00034150672768253537 | 0.000239055 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-4f10136befce99cf4091` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 16.069999999857544 | 11.2799999998619 | 4.79 | 0.5 | `r-0925b86f96a976919154` | `r-49dfa8b5fa2efc7b9b44` |
| h/1 | P04_step_2x | last_isi | exceeds | 40.059999999963566 | 32.429999999970505 | 7.63 | 0.8012 | `r-0925b86f96a976919154` | `r-49dfa8b5fa2efc7b9b44` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 16.0 | 3 | 0.5 | `r-0925b86f96a976919154` | `r-49dfa8b5fa2efc7b9b44` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 23.149999999851104 | 14.689999999858799 | 8.46 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-fe0d0914fb1f8f4ad578` |
| h/1 | P05_long_step | last_isi | exceeds | 51.510000001124354 | 38.47000000083972 | 13.04 | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-fe0d0914fb1f8f4ad578` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 52.0 | 13 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-fe0d0914fb1f8f4ad578` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 396.20999999951187 | 238.1799999996556 | 158.03 | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-52301fba45d663f75038` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 23.0 | 7 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-52301fba45d663f75038` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533750000003 | -66.37116208648685 | 1.76418 | 0.5 | `r-0925b86f96a976919154` | `r-49dfa8b5fa2efc7b9b44` |
| h/1 | P09_short_pulse | first_spike_latency | exceeds | 3.9799999998685394 | 3.2399999998692124 | 0.74 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-d511619b0a8c85df9aaf` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 2.409955221696444e-13 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-081d2283afd4d58bcec3` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -12.869281560034324 | 1.06521 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-081d2283afd4d58bcec3` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 4.2900000000009975 | 1.12 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-081d2283afd4d58bcec3` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 17.13000000000485 | 1.19 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-081d2283afd4d58bcec3` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-081d2283afd4d58bcec3` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -62.94284065780637 | 2.07999 | 0.5 | `r-6797defd923ff2562240` | `r-3714a8cce8aad48674fc` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.00034150672768253537 | 0.000239055 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-3db4c9cf0531797f0ea6` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 16.02999999985758 | 11.239999999861936 | 4.79 | 0.5 | `r-6797defd923ff2562240` | `r-3714a8cce8aad48674fc` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 32.39999999997053 | 7.65 | 0.8012 | `r-6797defd923ff2562240` | `r-3714a8cce8aad48674fc` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 16.0 | 3 | 0.5 | `r-6797defd923ff2562240` | `r-3714a8cce8aad48674fc` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 23.10999999985114 | 14.639999999858844 | 8.47 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-65425551ce7967c875a8` |
| h/2 | P05_long_step | last_isi | exceeds | 51.560000001125445 | 38.4600000008395 | 13.1 | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-65425551ce7967c875a8` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 52.0 | 13 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-65425551ce7967c875a8` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 396.1499999995119 | 238.10999999965566 | 158.04 | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-781eb44550cd60dd4cbb` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 23.0 | 7 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-781eb44550cd60dd4cbb` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -68.13533766326908 | -66.37116225128177 | 1.76418 | 0.5 | `r-6797defd923ff2562240` | `r-3714a8cce8aad48674fc` |
| h/2 | P09_short_pulse | first_spike_latency | exceeds | 3.9399999998685757 | 3.2099999998692397 | 0.73 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-67c9ed172bf8a0c2d156` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
