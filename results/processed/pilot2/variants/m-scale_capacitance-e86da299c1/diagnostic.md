# m-scale_capacitance-e86da299c1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "1.42 uF_per_cm2", "old": "2.84 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "2.84 uF_per_cm2", "new": "1.42 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1479.886 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 115.19244766190107 | 15.1434 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 31.470000000015006 | 1.17 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 67.94999999993826 | 8.94 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 9.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-d3372013b99a41353508` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.006795983880882453 | 0.000819616 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-8125cdf65ae78e98b10e` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 98.06893539575677 | 103.36754607915228 | 5.29861 | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-59d2b4f3b4022be4c6a8` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 12.319999999860954 | 13.09 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-59d2b4f3b4022be4c6a8` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 415.5399999996221 | 35.58 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-59d2b4f3b4022be4c6a8` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 98.06814575218911 | 103.21031951683564 | 5.14217 | 1.96136 | `r-f6700284baa99a5ef41f` | `r-9398cf72774d89fd5cde` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 17.36999999985636 | 19.8 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-9398cf72774d89fd5cde` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 524.0399999995234 | 62.85 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-9398cf72774d89fd5cde` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 461.73999999945227 | 39.4 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-75e043cdd124250e6375` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | -7.193619267781571 |  | inf | `r-195ba3020e76bc4e3add` | `r-39a89ee09fbed42e1e6d` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 104.44334792741344 |  | inf | `r-195ba3020e76bc4e3add` | `r-39a89ee09fbed42e1e6d` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 3.0999999998693397 |  | inf | `r-195ba3020e76bc4e3add` | `r-39a89ee09fbed42e1e6d` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-195ba3020e76bc4e3add` | `r-39a89ee09fbed42e1e6d` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 114.97919845543966 | 15.1002 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-7e9645d1aa4bf656b45a` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 32.6300000000156 | 31.460000000015 | 1.17 | 0.6528 | `r-2526a9bbad7e1faa361e` | `r-7e9645d1aa4bf656b45a` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 67.64999999993853 | 8.94 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-7e9645d1aa4bf656b45a` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 9.0 | 1 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-7e9645d1aa4bf656b45a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.006795983880882453 | 0.000819616 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-69c3d31678837278312b` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 97.6356582663006 | 102.93304825067867 | 5.29739 | 1.96138 | `r-16be743cbc8f0485fd82` | `r-3d077d017184bc9457ad` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 12.27999999986099 | 13.08 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-3d077d017184bc9457ad` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 414.4899999996231 | 35.69 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-3d077d017184bc9457ad` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 97.55448913585151 | 102.82633972222817 | 5.27185 | 1.96136 | `r-493fa57e11933a720397` | `r-c9f21a5c1e6afdc1e19c` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 17.319999999856407 | 19.79 | 0.7434 | `r-493fa57e11933a720397` | `r-c9f21a5c1e6afdc1e19c` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 523.0199999995243 | 62.95 | 11.7378 | `r-493fa57e11933a720397` | `r-c9f21a5c1e6afdc1e19c` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 461.64999999945235 | 39.41 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-64fe8a9c38655fd97373` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | -7.192380088806161 |  | inf | `r-eb52f398ba2e116da449` | `r-565d6cbdafbd72cb47b2` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 104.0886230498906 |  | inf | `r-eb52f398ba2e116da449` | `r-565d6cbdafbd72cb47b2` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 3.079999999869358 |  | inf | `r-eb52f398ba2e116da449` | `r-565d6cbdafbd72cb47b2` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-eb52f398ba2e116da449` | `r-565d6cbdafbd72cb47b2` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
