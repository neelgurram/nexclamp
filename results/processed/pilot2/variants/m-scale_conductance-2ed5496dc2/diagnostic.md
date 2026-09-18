# m-scale_conductance-2ed5496dc2

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_conductance
- parameters: `{"changes": [{"attribute": "condDensity", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ca_pyr_soma_group']", "new": "5.0 mS_per_cm2", "old": "10.0 mS_per_cm2"}], "element": "channelDensity", "element_id": "Ca_pyr_soma_group", "factor": 0.5, "generator_seed": 20260917}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/pyr_soma_m_in_b_in.cell.nml", "locator": "/neuroml[@id='pyr_4_sym_soma']/cell[@id='pyr_soma_m_in_b_in']/biophysicalProperties[@id='biophys']/membraneProperties[1]/channelDensity[@id='Ca_pyr_soma_group']", "attribute": "condDensity", "old": "10.0 mS_per_cm2", "new": "5.0 mS_per_cm2", "action": "set", "note": "scale_conductance"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1420.98 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | 0.029502934321434044 | 0.0541047 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-0e1e94a9d1ff6d8b600b` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 37.629999999965776 | 39.26 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-0e1e94a9d1ff6d8b600b` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 15.0 | 7 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-0e1e94a9d1ff6d8b600b` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -65.34640342559813 | 0.867241 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-c1122fde757e302f00b2` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.005703162352298341 | 0.00191244 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-c12a1fcaf2aee84dd1d2` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -7.59371910095237 | 0.574183 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-c1122fde757e302f00b2` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 21.799999999852332 | 3.61 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-c1122fde757e302f00b2` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 343.9899999996872 | 107.13 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-c1122fde757e302f00b2` |
| h/1 | P05_long_step | ahp_depth | exceeds | -7.059071324666348 | -7.63142356872558 | 0.572352 | 0.5 | `r-f6700284baa99a5ef41f` | `r-5416aa0622f314b55b7a` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 29.999999999844874 | 7.17 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-5416aa0622f314b55b7a` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 407.5699999996293 | 179.32 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-5416aa0622f314b55b7a` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-f6700284baa99a5ef41f` | `r-5416aa0622f314b55b7a` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 336.699999999566 | 164.44 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-89ba659b087e26fe7720` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-89ba659b087e26fe7720` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | -7.749213790893549 |  | inf | `r-195ba3020e76bc4e3add` | `r-b3a2414391cd3e8bb790` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 97.97423172106667 |  | inf | `r-195ba3020e76bc4e3add` | `r-b3a2414391cd3e8bb790` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 10.679999999862446 |  | inf | `r-195ba3020e76bc4e3add` | `r-b3a2414391cd3e8bb790` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-195ba3020e76bc4e3add` | `r-b3a2414391cd3e8bb790` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | 0.029446628825684513 | 0.0544953 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-87692c27cfd95028290c` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 37.46999999996592 | 39.12 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-87692c27cfd95028290c` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 15.0 | 7 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-87692c27cfd95028290c` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -65.34640200195311 | 0.867242 | 0.5 | `r-16be743cbc8f0485fd82` | `r-fe15ac2e2967476edf28` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.005703162352298341 | 0.00191244 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-f981e03d73b97a1fa183` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -7.016957875569673 | -7.591152524312335 | 0.574195 | 0.5 | `r-16be743cbc8f0485fd82` | `r-fe15ac2e2967476edf28` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 21.749999999852378 | 3.61 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-fe15ac2e2967476edf28` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 342.94999999968815 | 107.23 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-fe15ac2e2967476edf28` |
| h/2 | P05_long_step | ahp_depth | exceeds | -7.056752797444673 | -7.6291011327107725 | 0.572348 | 0.5 | `r-493fa57e11933a720397` | `r-f5628dd410e727fcdd3c` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 29.93999999984493 | 7.17 | 0.7434 | `r-493fa57e11933a720397` | `r-f5628dd410e727fcdd3c` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 406.55999999963024 | 179.41 | 11.7378 | `r-493fa57e11933a720397` | `r-f5628dd410e727fcdd3c` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-493fa57e11933a720397` | `r-f5628dd410e727fcdd3c` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 336.61999999956606 | 164.44 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-3195a146caa5b6670ac5` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 3.0 | 1 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-3195a146caa5b6670ac5` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | -7.7477229588826475 |  | inf | `r-eb52f398ba2e116da449` | `r-4e776fb480844a40f9c2` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 97.4406662003909 |  | inf | `r-eb52f398ba2e116da449` | `r-4e776fb480844a40f9c2` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 10.60999999986251 |  | inf | `r-eb52f398ba2e116da449` | `r-4e776fb480844a40f9c2` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-eb52f398ba2e116da449` | `r-4e776fb480844a40f9c2` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
