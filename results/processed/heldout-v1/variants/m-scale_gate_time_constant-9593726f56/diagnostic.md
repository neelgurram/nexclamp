# m-scale_gate_time_constant-9593726f56

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"changes": [{"attribute": "rate", "locator": "/neuroml[@id='it']/ionChannel[@id='na']/gate[@id='m']/forwardRate[1]", "new": "1.3104per_ms", "old": "1.638per_ms"}, {"attribute": "rate", "locator": "/neuroml[@id='it']/ionChannel[@id='na']/gate[@id='m']/reverseRate[1]", "new": "0.8928per_ms", "old": "1.116per_ms"}], "channel": "na", "factor": 0.8, "gate": "m", "generator_seed": 20260917, "mechanism": "rate_parameters"}`
- recorded edits: `[{"file": "NeuroML2/na.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='na']/gate[@id='m']/forwardRate[1]", "attribute": "rate", "old": "1.638per_ms", "new": "1.3104per_ms", "action": "set", "note": "scale_gate_time_constant"}, {"file": "NeuroML2/na.channel.nml", "locator": "/neuroml[@id='it']/ionChannel[@id='na']/gate[@id='m']/reverseRate[1]", "attribute": "rate", "old": "1.116per_ms", "new": "0.8928per_ms", "action": "set", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 5250.583 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
