# m-scale_gate_slope-2aae0cf4be

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `traub2005_testseg_all`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / scale_gate_slope
- parameters: `{"changes": [{"attribute": "scale", "locator": "/neuroml[@id='cat']/ionChannel[@id='cat']/gate[@id='h']/steadyState[1]", "new": "-5mV", "old": "-4mV"}], "channel": "cat", "factor": 1.25, "gate": "h", "generator_seed": 20260917, "mechanism": "steady_state"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/cat.channel.nml", "locator": "/neuroml[@id='cat']/ionChannel[@id='cat']/gate[@id='h']/steadyState[1]", "attribute": "scale", "old": "-4mV", "new": "-5mV", "action": "set", "note": "scale_gate_slope"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 8060.731 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
