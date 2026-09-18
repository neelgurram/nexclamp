# m-shift_gate_midpoint-e68b2bd3be

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "new": "1e-2V", "old": "5e-03V"}, {"attribute": "midpoint", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "new": "-3.9e-3V", "old": "-8.9e-3V"}], "channel": "Ca_pyr", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "5e-03V", "new": "1e-2V", "action": "set", "note": "shift_gate_midpoint"}, {"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "attribute": "midpoint", "old": "-8.9e-3V", "new": "-3.9e-3V", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1403.901 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | 0.061764830800615726 | 0.0218428 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-ae50ba04ee5dab210d0b` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 58.86999999994646 | 18.02 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-ae50ba04ee5dab210d0b` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 10.0 | 2 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-ae50ba04ee5dab210d0b` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -65.1290979156494 | 1.08455 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-cc41cdfc9df9ab25629c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0053275049518475516 | 0.0022881 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-7695f9e82a96728e2793` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -7.019535802205411 | -7.717420936584475 | 0.697885 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-cc41cdfc9df9ab25629c` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 25.40999999984905 | 21.169999999852905 | 4.24 | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-cc41cdfc9df9ab25629c` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 392.21999999964333 | 58.9 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-cc41cdfc9df9ab25629c` |
| h/1 | P05_long_step | ahp_depth | exceeds | -7.059071324666348 | -7.754324317932131 | 0.695253 | 0.5 | `r-f6700284baa99a5ef41f` | `r-33238cda2c1b83752548` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 37.16999999983835 | 28.85999999984591 | 8.31 | 0.7434 | `r-f6700284baa99a5ef41f` | `r-33238cda2c1b83752548` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 450.83000000147763 | 136.06 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-33238cda2c1b83752548` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-f6700284baa99a5ef41f` | `r-33238cda2c1b83752548` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 501.13999999941643 | 313.8999999995867 | 187.24 | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-41d69f1458942ea64080` |
| h/1 | P09_short_pulse | ahp_depth | definedness | None | -7.869337440490725 |  | inf | `r-195ba3020e76bc4e3add` | `r-478f258ebbf7bed1c18b` |
| h/1 | P09_short_pulse | ap_amplitude | definedness | None | 97.99366378937756 |  | inf | `r-195ba3020e76bc4e3add` | `r-478f258ebbf7bed1c18b` |
| h/1 | P09_short_pulse | first_spike_latency | definedness | None | 9.829999999863219 |  | inf | `r-195ba3020e76bc4e3add` | `r-478f258ebbf7bed1c18b` |
| h/1 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-195ba3020e76bc4e3add` | `r-478f258ebbf7bed1c18b` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | 0.061873888334997365 | 0.0220681 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-4504727cb83fe33e5ee7` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 58.549999999946806 | 18.04 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-4504727cb83fe33e5ee7` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 10.0 | 2 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-4504727cb83fe33e5ee7` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -65.12909624786376 | 1.08455 | 0.5 | `r-16be743cbc8f0485fd82` | `r-4591cdf9cdfe42720d61` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.0053275049518475516 | 0.0022881 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-8176e26b8896bc9608ac` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -7.016957875569673 | -7.7149512736002634 | 0.697993 | 0.5 | `r-16be743cbc8f0485fd82` | `r-4591cdf9cdfe42720d61` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 25.359999999849094 | 21.12999999985294 | 4.23 | 0.5082 | `r-16be743cbc8f0485fd82` | `r-4591cdf9cdfe42720d61` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 391.0399999996444 | 59.14 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-4591cdf9cdfe42720d61` |
| h/2 | P05_long_step | ahp_depth | exceeds | -7.056752797444673 | -7.75209879557292 | 0.695346 | 0.5 | `r-493fa57e11933a720397` | `r-f8506e07aedd87a7aaa0` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 37.10999999983841 | 28.809999999845957 | 8.3 | 0.7434 | `r-493fa57e11933a720397` | `r-f8506e07aedd87a7aaa0` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 449.68000000137204 | 136.29 | 11.7378 | `r-493fa57e11933a720397` | `r-f8506e07aedd87a7aaa0` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 5.0 | 1 | 0.5 | `r-493fa57e11933a720397` | `r-f8506e07aedd87a7aaa0` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 501.0599999994165 | 313.8199999995868 | 187.24 | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-ab9887f881518fa6302a` |
| h/2 | P09_short_pulse | ahp_depth | definedness | None | -7.867913004557295 |  | inf | `r-eb52f398ba2e116da449` | `r-0b46428d12ee1e11eab2` |
| h/2 | P09_short_pulse | ap_amplitude | definedness | None | 97.52399826085654 |  | inf | `r-eb52f398ba2e116da449` | `r-0b46428d12ee1e11eab2` |
| h/2 | P09_short_pulse | first_spike_latency | definedness | None | 9.759999999863282 |  | inf | `r-eb52f398ba2e116da449` | `r-0b46428d12ee1e11eab2` |
| h/2 | P09_short_pulse | spike_count | exceeds | 0.0 | 1.0 | 1 | 0.5 | `r-eb52f398ba2e116da449` | `r-0b46428d12ee1e11eab2` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
