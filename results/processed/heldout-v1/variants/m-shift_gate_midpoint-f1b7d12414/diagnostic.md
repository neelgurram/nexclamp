# m-shift_gate_midpoint-f1b7d12414

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/forwardRate[1]", "new": "-20mV", "old": "-30mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/reverseRate[1]", "new": "-20mV", "old": "-30mV"}], "channel": "nax", "delta_mV": 10.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/nax.channel.nml", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-20mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/nax.channel.nml", "locator": "/neuroml[@id='nax']/ionChannel[@id='nax']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-30mV", "new": "-20mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3088.009 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.14028549194009 | 93.24039840693817 | 6.89989 | 2.00281 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 5.420000000001174 | 15.440000000001518 | 10.02 | 0.5 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 30.159999999995136 | 11.83 | 0.5 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 2.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-16e89293d0d6edc7c678` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -65.0228273132324 | -65.98750321502683 | 0.964676 | 0.5 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.002732053821460283 | 0.00215149 | 6.83013e-05 | `s-b1b4baffdde7651e5212` | `s-cd80646e6e55af2bd523` |
| h/1 | P04_step_2x | adaptation_index | definedness | 1.2482836100362002e-05 | None |  | 0.01 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | ahp_depth | definedness | -14.775756835937727 | None |  | 0.738788 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 100.46828841971717 | None |  | 2.00937 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 16.069999999857544 | None |  | 0.5 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | last_isi | definedness | 40.059999999963566 | None |  | 0.8012 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P04_step_2x | spike_count | exceeds | 13.0 | 0.0 | 13 | 0.5 | `r-0925b86f96a976919154` | `r-1d3b15547e02626f091f` |
| h/1 | P05_long_step | adaptation_index | definedness | 3.1579676843726073e-13 | None |  | 0.01 | `r-4ab59c3e1336e488abd6` | `r-88312cb77382b5746291` |
| h/1 | P05_long_step | ahp_depth | definedness | -15.073226928710938 | None |  | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-88312cb77382b5746291` |
| h/1 | P05_long_step | ap_amplitude | definedness | 100.41315077975412 | None |  | 2.00826 | `r-4ab59c3e1336e488abd6` | `r-88312cb77382b5746291` |
| h/1 | P05_long_step | first_spike_latency | definedness | 23.149999999851104 | None |  | 0.5 | `r-4ab59c3e1336e488abd6` | `r-88312cb77382b5746291` |
| h/1 | P05_long_step | last_isi | definedness | 51.510000001124354 | None |  | 1.0302 | `r-4ab59c3e1336e488abd6` | `r-88312cb77382b5746291` |
| h/1 | P05_long_step | spike_count | exceeds | 39.0 | 0.0 | 39 | 0.5 | `r-4ab59c3e1336e488abd6` | `r-88312cb77382b5746291` |
| h/1 | P06_ramp | first_spike_latency | definedness | 396.20999999951187 | None |  | 7.9242 | `r-7e89f1dc706a0ef0fd1a` | `r-d054b69aa049879c60c8` |
| h/1 | P06_ramp | spike_count | exceeds | 16.0 | 0.0 | 16 | 0.5 | `r-7e89f1dc706a0ef0fd1a` | `r-d054b69aa049879c60c8` |
| h/1 | P09_short_pulse | ahp_depth | definedness | -16.001159667968338 | None |  | 0.800058 | `r-86c7a89ca0bbba8e93d0` | `r-1d45a69ea13d5aa20a52` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | 100.17234039630091 | None |  | 2.00345 | `r-86c7a89ca0bbba8e93d0` | `r-1d45a69ea13d5aa20a52` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | 3.9799999998685394 | None |  | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-1d45a69ea13d5aa20a52` |
| h/1 | P09_short_pulse | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-86c7a89ca0bbba8e93d0` | `r-1d45a69ea13d5aa20a52` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 100.07681274416072 | 93.18840026852445 | 6.88841 | 2.00281 | `r-1c8cea9109ae2bf6fdec` | `r-fcb026eca11ab27613ef` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 5.4100000000011725 | 15.43000000000152 | 10.02 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-fcb026eca11ab27613ef` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 30.15999999999513 | 11.84 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-fcb026eca11ab27613ef` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 2.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-fcb026eca11ab27613ef` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -65.02282723083493 | -65.98750313262937 | 0.964676 | 0.5 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.0005805614370603101 | 0.002732053821460283 | 0.00215149 | 6.83013e-05 | `s-5b5b3fcb49666d218518` | `s-ffac8b4ea8e3063c93ca` |
| h/2 | P04_step_2x | adaptation_index | definedness | 1.248595330253465e-05 | None |  | 0.01 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P04_step_2x | ahp_depth | definedness | -14.55389404296919 | None |  | 0.738788 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 100.0564460769101 | None |  | 2.00937 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 16.02999999985758 | None |  | 0.5 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P04_step_2x | last_isi | definedness | 40.049999999963575 | None |  | 0.8012 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P04_step_2x | spike_count | exceeds | 13.0 | 0.0 | 13 | 0.5 | `r-6797defd923ff2562240` | `r-e5d7ef93df6ddd288da3` |
| h/2 | P05_long_step | adaptation_index | definedness | 3.1579676994309704e-13 | None |  | 0.01 | `r-a3b84bbc3dc843d0e573` | `r-15326f1934b2c4397e14` |
| h/2 | P05_long_step | ahp_depth | definedness | -14.856796264648438 | None |  | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-15326f1934b2c4397e14` |
| h/2 | P05_long_step | ap_amplitude | definedness | 100.03872680731578 | None |  | 2.00826 | `r-a3b84bbc3dc843d0e573` | `r-15326f1934b2c4397e14` |
| h/2 | P05_long_step | first_spike_latency | definedness | 23.10999999985114 | None |  | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-15326f1934b2c4397e14` |
| h/2 | P05_long_step | last_isi | definedness | 51.560000001125445 | None |  | 1.0302 | `r-a3b84bbc3dc843d0e573` | `r-15326f1934b2c4397e14` |
| h/2 | P05_long_step | spike_count | exceeds | 39.0 | 0.0 | 39 | 0.5 | `r-a3b84bbc3dc843d0e573` | `r-15326f1934b2c4397e14` |
| h/2 | P06_ramp | first_spike_latency | definedness | 396.1499999995119 | None |  | 7.9242 | `r-8a56ade2f92e09dafdaf` | `r-bdc507ca197a3281b678` |
| h/2 | P06_ramp | spike_count | exceeds | 16.0 | 0.0 | 16 | 0.5 | `r-8a56ade2f92e09dafdaf` | `r-bdc507ca197a3281b678` |
| h/2 | P09_short_pulse | ahp_depth | definedness | -15.791358947753906 | None |  | 0.800058 | `r-2e410d8c71a4df0466e8` | `r-3092c94e03a3dd009838` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | 99.86314392274174 | None |  | 2.00345 | `r-2e410d8c71a4df0466e8` | `r-3092c94e03a3dd009838` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | 3.9399999998685757 | None |  | 0.5 | `r-2e410d8c71a4df0466e8` | `r-3092c94e03a3dd009838` |
| h/2 | P09_short_pulse | spike_count | exceeds | 1.0 | 0.0 | 1 | 0.5 | `r-2e410d8c71a4df0466e8` | `r-3092c94e03a3dd009838` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
