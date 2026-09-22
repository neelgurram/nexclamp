# m-shift_gate_midpoint-831ea54a80

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='NaTa_t']/ionChannel[@id='NaTa_t']/gate[@id='h']/forwardRate[1]", "new": "-76mV", "old": "-66mV"}, {"attribute": "midpoint", "locator": "/neuroml[@id='NaTa_t']/ionChannel[@id='NaTa_t']/gate[@id='h']/reverseRate[1]", "new": "-76mV", "old": "-66mV"}], "channel": "NaTa_t", "delta_mV": -10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/NaTa_t.channel.nml", "locator": "/neuroml[@id='NaTa_t']/ionChannel[@id='NaTa_t']/gate[@id='h']/forwardRate[1]", "attribute": "midpoint", "old": "-66mV", "new": "-76mV", "action": "set", "note": "shift_gate_midpoint"}, {"file": "neuroConstruct/generatedNeuroML2/NaTa_t.channel.nml", "locator": "/neuroml[@id='NaTa_t']/ionChannel[@id='NaTa_t']/gate[@id='h']/reverseRate[1]", "attribute": "midpoint", "old": "-66mV", "new": "-76mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4920.887 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | 0.009793123149720978 | None |  | 0.01 | `r-a22266676a5c9c51fe6b` | `r-fe9a99db76ffff27c4e3` |
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | 48.559451923496454 | 49.0189 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-fe9a99db76ffff27c4e3` |
| h/1 | P00_canonical | ap_amplitude | exceeds | 90.78240967397937 | 54.182939052869756 | 36.5995 | 1.81565 | `r-a22266676a5c9c51fe6b` | `r-fe9a99db76ffff27c4e3` |
| h/1 | P00_canonical | last_isi | definedness | 15.789999999985639 | None |  | 0.5 | `r-a22266676a5c9c51fe6b` | `r-fe9a99db76ffff27c4e3` |
| h/1 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-fe9a99db76ffff27c4e3` |
| h/1 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.02212963595382829 | 0.00198074 | 0.000402978 | `s-606c2ee73d10b43bdee7` | `s-7c67f8d93bb77988719e` |
| h/1 | P04_step_2x | adaptation_index | definedness | 0.01011398557861304 | None |  | 0.01 | `r-49ced7acda977f37b12b` | `r-0ff48759418334cf35ea` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | 51.32756254323671 | 50.4535 | 0.5 | `r-49ced7acda977f37b12b` | `r-0ff48759418334cf35ea` |
| h/1 | P04_step_2x | ap_amplitude | exceeds | 89.04202652392433 | 49.75434136556797 | 39.2877 | 3.5976 | `r-49ced7acda977f37b12b` | `r-0ff48759418334cf35ea` |
| h/1 | P04_step_2x | first_spike_latency | exceeds | 8.549999999864383 | 9.899999999863155 | 1.35 | 0.5 | `r-49ced7acda977f37b12b` | `r-0ff48759418334cf35ea` |
| h/1 | P04_step_2x | last_isi | definedness | 36.64999999996667 | None |  | 0.733 | `r-49ced7acda977f37b12b` | `r-0ff48759418334cf35ea` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 1.0 | 14 | 0.5 | `r-49ced7acda977f37b12b` | `r-0ff48759418334cf35ea` |
| h/1 | P05_long_step | adaptation_index | definedness | -0.0038302951745234274 | None |  | 0.01 | `r-b99907e8e6510bd22247` | `r-cd95880c2e1886cbc7dc` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | 51.88954946644933 | 51.429 | 0.5 | `r-b99907e8e6510bd22247` | `r-cd95880c2e1886cbc7dc` |
| h/1 | P05_long_step | ap_amplitude | exceeds | 85.6294059753018 | 46.92559027759219 | 38.7038 | 3.92393 | `r-b99907e8e6510bd22247` | `r-cd95880c2e1886cbc7dc` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.769999999860545 | 15.059999999858462 | 2.29 | 0.5 | `r-b99907e8e6510bd22247` | `r-cd95880c2e1886cbc7dc` |
| h/1 | P05_long_step | last_isi | definedness | 142.97000000312073 | None |  | 3.03 | `r-b99907e8e6510bd22247` | `r-cd95880c2e1886cbc7dc` |
| h/1 | P05_long_step | spike_count | exceeds | 14.0 | 1.0 | 13 | 0.5 | `r-b99907e8e6510bd22247` | `r-cd95880c2e1886cbc7dc` |
| h/1 | P06_ramp | first_spike_latency | exceeds | 368.589999999537 | 403.67999999950507 | 35.09 | 7.3718 | `r-da1341cbf9665d4e7639` | `r-bc4a7f4e5b239b74a56c` |
| h/1 | P06_ramp | spike_count | exceeds | 24.0 | 1.0 | 23 | 0.5 | `r-da1341cbf9665d4e7639` | `r-bc4a7f4e5b239b74a56c` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | -0.4749124323520846 | 0.665742 | 0.5 | `r-ad42eb643e1748725abb` | `r-43478b16a37cbdf7235e` |
| h/1 | P09_short_pulse | ap_amplitude | exceeds | 126.03113174260383 | 117.74725341942366 | 8.28388 | 2.52062 | `r-ad42eb643e1748725abb` | `r-43478b16a37cbdf7235e` |
| h/2 | P00_canonical | adaptation_index | definedness | 0.009806079948801606 | None |  | 0.01 | `r-ebfd6e5f8d6b9e916dfe` | `r-3bebffb0afb479ccde10` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | 48.74267538492013 | 49.2074 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-3bebffb0afb479ccde10` |
| h/2 | P00_canonical | ap_amplitude | exceeds | 90.22942352330233 | 53.92231989116531 | 36.3071 | 1.81565 | `r-ebfd6e5f8d6b9e916dfe` | `r-3bebffb0afb479ccde10` |
| h/2 | P00_canonical | last_isi | definedness | 15.769999999985657 | None |  | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-3bebffb0afb479ccde10` |
| h/2 | P00_canonical | spike_count | exceeds | 7.0 | 1.0 | 6 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-3bebffb0afb479ccde10` |
| h/2 | P03_rheobase | rheobase | exceeds | 0.020148896933269586 | 0.02212963595382829 | 0.00198074 | 0.000402978 | `s-dcf9a3a6907c5d4ed514` | `s-669527d3f1c534a093fc` |
| h/2 | P04_step_2x | adaptation_index | definedness | 0.010272237117704504 | None |  | 0.01 | `r-1e40b84a0cfdecc32574` | `r-cc26c6efc559d382234b` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | 51.660620694476464 | 50.7505 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-cc26c6efc559d382234b` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 87.8428268328099 | 49.45390117278648 | 38.3889 | 3.5976 | `r-1e40b84a0cfdecc32574` | `r-cc26c6efc559d382234b` |
| h/2 | P04_step_2x | first_spike_latency | exceeds | 8.50999999986442 | 9.869999999863182 | 1.36 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-cc26c6efc559d382234b` |
| h/2 | P04_step_2x | last_isi | definedness | 36.55999999996675 | None |  | 0.733 | `r-1e40b84a0cfdecc32574` | `r-cc26c6efc559d382234b` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 1.0 | 14 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-cc26c6efc559d382234b` |
| h/2 | P05_long_step | adaptation_index | definedness | -0.003813229079145206 | None |  | 0.01 | `r-cbc91d57fa8b8448b73b` | `r-38f1bad100722c8d09ba` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | 52.16904926810021 | 51.6159 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-38f1bad100722c8d09ba` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 84.32143019785677 | 46.619891644259106 | 37.7015 | 3.92393 | `r-cbc91d57fa8b8448b73b` | `r-38f1bad100722c8d09ba` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.729999999860581 | 15.02999999985849 | 2.3 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-38f1bad100722c8d09ba` |
| h/2 | P05_long_step | last_isi | definedness | 143.98000000314278 | None |  | 3.03 | `r-cbc91d57fa8b8448b73b` | `r-38f1bad100722c8d09ba` |
| h/2 | P05_long_step | spike_count | exceeds | 14.0 | 1.0 | 13 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-38f1bad100722c8d09ba` |
| h/2 | P06_ramp | first_spike_latency | exceeds | 368.53999999953703 | 403.6299999995051 | 35.09 | 7.3718 | `r-1b54cfe9f9ae3444183f` | `r-3972359ce75eaa3cc981` |
| h/2 | P06_ramp | spike_count | exceeds | 24.0 | 1.0 | 23 | 0.5 | `r-1b54cfe9f9ae3444183f` | `r-3972359ce75eaa3cc981` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | -0.44164180246907847 | 0.72529 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-768ec9426710da29556e` |
| h/2 | P09_short_pulse | ap_amplitude | exceeds | 125.19136047490628 | 116.43338776202557 | 8.75797 | 2.52062 | `r-12a8ce0ecdd4bde4c832` | `r-768ec9426710da29556e` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
