# m-shift_forward_rate_midpoint-484491b9f3

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `hay2011_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]", "new": "-149.9mV", "old": "-154.9mV"}], "channel": "Ih", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/Ih.channel.nml", "locator": "/neuroml[@id='Ih']/ionChannel[@id='Ih']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-154.9mV", "new": "-149.9mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 4799.617 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | ahp_depth | exceeds | -0.4594799502835798 | -2.0474120453495743 | 1.58793 | 0.5 | `r-a22266676a5c9c51fe6b` | `r-d065186b448911f50294` |
| h/1 | P04_step_2x | ahp_depth | exceeds | 0.8740316797887999 | -0.8581942265807356 | 1.73223 | 0.5 | `r-49ced7acda977f37b12b` | `r-9eab605c03e36a14b176` |
| h/1 | P04_step_2x | last_isi | exceeds | 36.64999999996667 | 34.50999999996861 | 2.14 | 0.733 | `r-49ced7acda977f37b12b` | `r-9eab605c03e36a14b176` |
| h/1 | P04_step_2x | spike_count | exceeds | 15.0 | 16.0 | 1 | 0.5 | `r-49ced7acda977f37b12b` | `r-9eab605c03e36a14b176` |
| h/1 | P05_long_step | ahp_depth | exceeds | 0.4605490137727344 | -1.1988009160333633 | 1.65935 | 0.5 | `r-b99907e8e6510bd22247` | `r-4237e85d232147b9b452` |
| h/1 | P05_long_step | first_spike_latency | exceeds | 12.769999999860545 | 12.0499999998612 | 0.72 | 0.5 | `r-b99907e8e6510bd22247` | `r-4237e85d232147b9b452` |
| h/1 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -94.93546852569605 | -92.61401161651636 | 2.32146 | 0.5 | `r-49ced7acda977f37b12b` | `r-9eab605c03e36a14b176` |
| h/1 | P09_short_pulse | ahp_depth | exceeds | -1.140654904681412 | -2.8589495366392157 | 1.71829 | 0.5 | `r-ad42eb643e1748725abb` | `r-c74ce0e644f1581590a9` |
| h/2 | P00_canonical | ahp_depth | exceeds | -0.46474839399847667 | -2.0529512906518335 | 1.5882 | 0.5 | `r-ebfd6e5f8d6b9e916dfe` | `r-0c601876939e16ec5644` |
| h/2 | P04_step_2x | ahp_depth | exceeds | 0.9101022720341234 | -0.8281198247252775 | 1.73822 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-343417736ad97213d250` |
| h/2 | P04_step_2x | last_isi | exceeds | 36.55999999996675 | 34.429999999968686 | 2.13 | 0.733 | `r-1e40b84a0cfdecc32574` | `r-343417736ad97213d250` |
| h/2 | P04_step_2x | spike_count | exceeds | 15.0 | 16.0 | 1 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-343417736ad97213d250` |
| h/2 | P05_long_step | ahp_depth | exceeds | 0.5531686782819634 | -1.117128918964795 | 1.6703 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-415e2d6061d6acda7d92` |
| h/2 | P05_long_step | first_spike_latency | exceeds | 12.729999999860581 | 12.019999999861227 | 0.71 | 0.5 | `r-cbc91d57fa8b8448b73b` | `r-415e2d6061d6acda7d92` |
| h/2 | P07_hyperpolarizing_step | steady_state_voltage | exceeds | -94.93546955413842 | -92.61401264495873 | 2.32146 | 0.5 | `r-1e40b84a0cfdecc32574` | `r-343417736ad97213d250` |
| h/2 | P09_short_pulse | ahp_depth | exceeds | -1.1669317245499542 | -2.88177735646606 | 1.71485 | 0.5 | `r-12a8ce0ecdd4bde4c832` | `r-1191dcd63ba93d73ba91` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
