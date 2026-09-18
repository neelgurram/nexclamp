# m-scale_gate_slope-d122bda225

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "new": "0.0173625V", "old": "0.01389V"}, {"attribute": "scale", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "new": "-0.00625V", "old": "-0.005V"}], "channel": "Ca_pyr", "factor": 1.25, "gate": "m", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "attribute": "scale", "old": "0.01389V", "new": "0.0173625V", "action": "set", "note": "scale_gate_slope"}, {"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "attribute": "scale", "old": "-0.005V", "new": "-0.00625V", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1396.851 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.01961323435065521 | 0.103221 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-3de6dd5309f1024f5822` |
| h/1 | P00_canonical | ahp_depth | exceeds | -7.047089353288882 | 0.6459193529401404 | 7.69301 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-3de6dd5309f1024f5822` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 100.04901504481984 | 96.76613235466795 | 3.28288 | 2.00098 | `r-7ce2d1a0f19cc5d24572` | `r-3de6dd5309f1024f5822` |
| h/1 | P00_canonical | first_spike_latency | exceeds | 32.640000000015604 | 36.38000000001752 | 3.74 | 0.6528 | `r-7ce2d1a0f19cc5d24572` | `r-3de6dd5309f1024f5822` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 102.68999999990666 | 25.8 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-3de6dd5309f1024f5822` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 6.0 | 2 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-3de6dd5309f1024f5822` |
| h/1 | P02_weak_step | steady_state_voltage | exceeds | -66.2136446029663 | -69.78645777130126 | 3.57281 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.03582405573389796 | 0.0282085 | 0.000152312 | `s-f72e8dc74d5f026206e4` | `s-13c6307a34e69f26428a` |
| h/1 | P04_step_2x | ahp_depth | definedness | -7.019535802205411 | None |  | 0.5 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/1 | P04_step_2x | ap_amplitude | definedness | 98.06893539575677 | None |  | 1.96138 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/1 | P04_step_2x | first_spike_latency | definedness | 25.40999999984905 | None |  | 0.5082 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/1 | P04_step_2x | last_isi | definedness | 451.11999999958977 | None |  | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/1 | P04_step_2x | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/1 | P05_long_step | adaptation_index | definedness | -8.519410542851502e-06 | None |  | 0.01 | `r-f6700284baa99a5ef41f` | `r-2bdd2847d592c61bdf4e` |
| h/1 | P05_long_step | ahp_depth | definedness | -7.059071324666348 | None |  | 0.5 | `r-f6700284baa99a5ef41f` | `r-2bdd2847d592c61bdf4e` |
| h/1 | P05_long_step | ap_amplitude | definedness | 98.06814575218911 | None |  | 1.96136 | `r-f6700284baa99a5ef41f` | `r-2bdd2847d592c61bdf4e` |
| h/1 | P05_long_step | first_spike_latency | definedness | 37.16999999983835 | None |  | 0.7434 | `r-f6700284baa99a5ef41f` | `r-2bdd2847d592c61bdf4e` |
| h/1 | P05_long_step | last_isi | definedness | 586.8900000005651 | None |  | 11.7378 | `r-f6700284baa99a5ef41f` | `r-2bdd2847d592c61bdf4e` |
| h/1 | P05_long_step | spike_count | exceeds | 4.0 | 0.0 | 4 | 0.5 | `r-f6700284baa99a5ef41f` | `r-2bdd2847d592c61bdf4e` |
| h/1 | P06_ramp | first_spike_latency | definedness | 501.13999999941643 | None |  | 10.0228 | `r-ee8bcdd517fb72ba8d0c` | `r-631592fbdc43329e3cc1` |
| h/1 | P06_ramp | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-ee8bcdd517fb72ba8d0c` | `r-631592fbdc43329e3cc1` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424023132327 | -71.82436180114749 | 1.01012 | 0.5 | `r-85c49aecb0e07f4c5069` | `r-1d655b957b54a26bf16c` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.019481725326317447 | 0.103424 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-a4a2b5d29483817331f1` |
| h/2 | P00_canonical | ahp_depth | exceeds | -7.040942077636629 | 0.6481986781528946 | 7.68914 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-a4a2b5d29483817331f1` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 99.87902450527808 | 96.6165084837971 | 3.26252 | 2.00098 | `r-2526a9bbad7e1faa361e` | `r-a4a2b5d29483817331f1` |
| h/2 | P00_canonical | first_spike_latency | exceeds | 32.6300000000156 | 36.3500000000175 | 3.72 | 0.6528 | `r-2526a9bbad7e1faa361e` | `r-a4a2b5d29483817331f1` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 102.37999999990694 | 25.79 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-a4a2b5d29483817331f1` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 6.0 | 2 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-a4a2b5d29483817331f1` |
| h/2 | P02_weak_step | steady_state_voltage | exceeds | -66.2136438430786 | -69.78647587585448 | 3.57283 | 0.5 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.007615600027320539 | 0.035687453042824946 | 0.0280719 | 0.000152312 | `s-4f52e2b97721efbbe2d2` | `s-dbdeb11965351a8c8047` |
| h/2 | P04_step_2x | ahp_depth | definedness | -7.016957875569673 | None |  | 0.5 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |
| h/2 | P04_step_2x | ap_amplitude | definedness | 97.6356582663006 | None |  | 1.96138 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |
| h/2 | P04_step_2x | first_spike_latency | definedness | 25.359999999849094 | None |  | 0.5082 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |
| h/2 | P04_step_2x | last_isi | definedness | 450.1799999995906 | None |  | 9.0224 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |
| h/2 | P04_step_2x | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |
| h/2 | P05_long_step | adaptation_index | definedness | -8.532786352377084e-06 | None |  | 0.01 | `r-493fa57e11933a720397` | `r-8dd7401064025a5f2008` |
| h/2 | P05_long_step | ahp_depth | definedness | -7.056752797444673 | None |  | 0.5 | `r-493fa57e11933a720397` | `r-8dd7401064025a5f2008` |
| h/2 | P05_long_step | ap_amplitude | definedness | 97.55448913585151 | None |  | 1.96136 | `r-493fa57e11933a720397` | `r-8dd7401064025a5f2008` |
| h/2 | P05_long_step | first_spike_latency | definedness | 37.10999999983841 | None |  | 0.7434 | `r-493fa57e11933a720397` | `r-8dd7401064025a5f2008` |
| h/2 | P05_long_step | last_isi | definedness | 585.9700000005014 | None |  | 11.7378 | `r-493fa57e11933a720397` | `r-8dd7401064025a5f2008` |
| h/2 | P05_long_step | spike_count | exceeds | 4.0 | 0.0 | 4 | 0.5 | `r-493fa57e11933a720397` | `r-8dd7401064025a5f2008` |
| h/2 | P06_ramp | first_spike_latency | definedness | 501.0599999994165 | None |  | 10.0228 | `r-2e3e935d6ecd1df4b94b` | `r-077aa1d31e703c05d28c` |
| h/2 | P06_ramp | spike_count | exceeds | 2.0 | 0.0 | 2 | 0.5 | `r-2e3e935d6ecd1df4b94b` | `r-077aa1d31e703c05d28c` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -70.81424049987795 | -71.82436251983646 | 1.01012 | 0.5 | `r-16be743cbc8f0485fd82` | `r-c108fbd02faa41f1324a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
