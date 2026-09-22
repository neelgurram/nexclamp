# m-shift_gate_midpoint-484712e890

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_gate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='cat']/ionChannel[@id='cat']/gate[@id='h']/steadyState[1]", "new": "-75mV", "old": "-80mV"}], "channel": "cat", "delta_mV": 5.0, "gate": "h", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/cat.channel.nml", "locator": "/neuroml[@id='cat']/ionChannel[@id='cat']/gate[@id='h']/steadyState[1]", "attribute": "midpoint", "old": "-80mV", "new": "-75mV", "action": "set", "note": "shift_gate_midpoint"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 8019.871 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | last_isi | exceeds | 23.700000000004948 | 23.000000000004178 | 0.7 | 0.5 | `r-068a1eafd4afbbd6d23e` | `r-2d522a3d8ebb05fb632a` |
| h/2 | P00_canonical | last_isi | exceeds | 23.72000000000496 | 23.020000000004188 | 0.7 | 0.5 | `r-87bcc3cd30685deaf603` | `r-f8f2968a98c3c1381ad8` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
