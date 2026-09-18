# m-shift_gate_midpoint-3c7134e6ec

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/forwardRate[1]", "new": "-3.3e-2V", "old": "-4.3e-2V"}, {"attribute": "midpoint", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/reverseRate[1]", "new": "-1e-2V", "old": "-2e-2V"}], "channel": "Na_pyr", "delta_mV": 10.0, "gate": "h", "generator_seed": 20260917, "mechanism": "rates"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Na_pyr.channel.nml", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/forwardRate[1]", "attribute": "midpoint", "old": "-4.3e-2V", "new": "-3.3e-2V", "action": "set", "note": "shift_gate_midpoint"}, {"file": "LEMSexamples/morphologies/Na_pyr.channel.nml", "locator": "/neuroml[@id='Na_pyr']/ionChannel[@id='Na_pyr']/gate[@id='h']/reverseRate[1]", "attribute": "midpoint", "old": "-2e-2V", "new": "-1e-2V", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1369.539 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | -0.01664867476962522 | 0.100256 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-840105f58a8e56d9450f` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 91.83999999991653 | 14.95 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-840105f58a8e56d9450f` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-840105f58a8e56d9450f` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 473.02999999956984 | 21.91 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-790f5508d9e7a51b61b6` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 604.3600000017468 | 17.47 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-ab49aaeecb1fe56235f7` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | -0.01679938253401503 | 0.100741 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-16e123e3ee5f1ee35449` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 91.85999999991651 | 15.27 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-16e123e3ee5f1ee35449` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 7.0 | 1 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-16e123e3ee5f1ee35449` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 473.1699999995697 | 22.99 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-a5bccc7c66a919ba6d6d` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 604.4600000017526 | 18.49 | 11.7378 | `r-493fa57e11933a720397` | `r-99a34bbfaf1bb4a35a2d` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
