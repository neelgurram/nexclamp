# m-scale_gate_time_constant-25d2ef79c1

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: development_pilot | protocol_version: PILOT2_PROTOCOL | designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate*

- model: `acnet2_pyr_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "new": "1.28e3per_s", "old": "1.6e3per_s"}, {"attribute": "rate", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "new": "8e1per_s", "old": "1e2per_s"}], "channel": "Ca_pyr", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/forwardRate[1]", "attribute": "rate", "old": "1.6e3per_s", "new": "1.28e3per_s", "action": "set", "note": "scale_gate_time_constant"}, {"file": "LEMSexamples/morphologies/Ca_pyr.channel.nml", "locator": "/neuroml[@id='Ca_pyr']/ionChannel[@id='Ca_pyr']/gate[@id='m']/reverseRate[1]", "attribute": "rate", "old": "1e2per_s", "new": "8e1per_s", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 1498.367 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | exceeds | 0.08360766405035329 | 0.07314791643162374 | 0.0104597 | 0.01 | `r-7ce2d1a0f19cc5d24572` | `r-be89725a6908c658c10b` |
| h/1 | P00_canonical | last_isi | exceeds | 76.88999999993013 | 64.75999999994116 | 12.13 | 1.5378 | `r-7ce2d1a0f19cc5d24572` | `r-be89725a6908c658c10b` |
| h/1 | P00_canonical | spike_count | exceeds | 8.0 | 9.0 | 1 | 0.5 | `r-7ce2d1a0f19cc5d24572` | `r-be89725a6908c658c10b` |
| h/1 | P04_step_2x | last_isi | exceeds | 451.11999999958977 | 431.00999999960806 | 20.11 | 9.0224 | `r-85c49aecb0e07f4c5069` | `r-c154a272fb0a30c33b8a` |
| h/1 | P05_long_step | last_isi | exceeds | 586.8900000005651 | 566.9399999994844 | 19.95 | 11.7378 | `r-f6700284baa99a5ef41f` | `r-f93bfa9eb75d2b2d8f19` |
| h/2 | P00_canonical | adaptation_index | exceeds | 0.08394194146984126 | 0.07318947423665083 | 0.0107525 | 0.01 | `r-2526a9bbad7e1faa361e` | `r-d43b5541167d0f9500a4` |
| h/2 | P00_canonical | last_isi | exceeds | 76.5899999999304 | 64.46999999994142 | 12.12 | 1.5378 | `r-2526a9bbad7e1faa361e` | `r-d43b5541167d0f9500a4` |
| h/2 | P00_canonical | spike_count | exceeds | 8.0 | 9.0 | 1 | 0.5 | `r-2526a9bbad7e1faa361e` | `r-d43b5541167d0f9500a4` |
| h/2 | P04_step_2x | last_isi | exceeds | 450.1799999995906 | 430.03999999960894 | 20.14 | 9.0224 | `r-16be743cbc8f0485fd82` | `r-153c541f2831524df490` |
| h/2 | P05_long_step | last_isi | exceeds | 585.9700000005014 | 566.0099999994852 | 19.96 | 11.7378 | `r-493fa57e11933a720397` | `r-77abcb8366cde978e39a` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
