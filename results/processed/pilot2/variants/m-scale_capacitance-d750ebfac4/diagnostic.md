# m-scale_capacitance-d750ebfac4

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_capacitance
- parameters: `{"changes": [{"attribute": "value", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "new": "2.272 uF_per_cm2", "old": "2.84 uF_per_cm2"}], "element": "specificCapacitance", "element_id": null, "factor": 0.8, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/specificCapacitance[1]", "attribute": "value", "old": "2.84 uF_per_cm2", "new": "2.272 uF_per_cm2", "action": "set", "note": "scale_capacitance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1445.361 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 102.79596328704014 | 2.74695 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-67a5c3751c604230c884` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 73.35999999993334 | 3.53 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-67a5c3751c604230c884` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.007308243972406257 | 0.000307356 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-4400dd7a3347c33dcf73` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 98.06893539575677 | 100.07933044643937 | 2.0104 | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-6b2f3c148115ff170d06` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 20.069999999853906 | 5.34 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-6b2f3c148115ff170d06` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 437.50999999960214 | 13.61 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-6b2f3c148115ff170d06` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 29.019999999845766 | 8.15 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-3e5ccfa7f4c15e1fe161` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 561.5199999994893 | 25.37 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-3e5ccfa7f4c15e1fe161` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 486.80999999942946 | 14.33 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-8e362fe6f5e68125dcea` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | -7.188040217081706 |  | inf | `r-195ba3020e76bc4e3add` | `r-b7dd7e19019e683a13f5` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 99.93616485789168 |  | inf | `r-195ba3020e76bc4e3add` | `r-b7dd7e19019e683a13f5` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 6.459999999866284 |  | inf | `r-195ba3020e76bc4e3add` | `r-b7dd7e19019e683a13f5` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-195ba3020e76bc4e3add` | `r-b7dd7e19019e683a13f5` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 102.64216232271141 | 2.76314 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-f875db77652018a7100d` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 73.05999999993361 | 3.53 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-f875db77652018a7100d` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.007308243972406257 | 0.000307356 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-83a3f4a59f1ebe6b2a2e` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 20.01999999985395 | 5.34 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-acbfefaeb7c75685c6a7` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 436.539999999603 | 13.64 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-acbfefaeb7c75685c6a7` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 97.55448913585151 | 99.51774597461298 | 1.96326 | 1.96136 | `r-493fa57e11933a720397` | `r-be52af83c0580834b5be` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 28.96999999984581 | 8.14 | 0.7434 | `r-493fa57e11933a720397` | `r-be52af83c0580834b5be` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 560.5599999994902 | 25.41 | 11.7378 | `r-493fa57e11933a720397` | `r-be52af83c0580834b5be` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 486.71999999942955 | 14.34 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-548f939e558b28586424` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | -7.1866583124792385 |  | inf | `r-eb52f398ba2e116da449` | `r-575bfbc07ace8bda7f0e` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 99.50751495331957 |  | inf | `r-eb52f398ba2e116da449` | `r-575bfbc07ace8bda7f0e` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 6.399999999866338 |  | inf | `r-eb52f398ba2e116da449` | `r-575bfbc07ace8bda7f0e` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-eb52f398ba2e116da449` | `r-575bfbc07ace8bda7f0e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
