# m-shift_forward_rate_midpoint-0fe6e40b23

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `bbp2015_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / kinetics / shift_forward_rate_midpoint
- parameters: `{"changes": [{"attribute": "midpoint", "locator": "/neuroml[@id='Im']/ionChannel[@id='Im']/gate[@id='m']/forwardRate[1]", "new": "-30mV", "old": "-35mV"}], "channel": "Im", "delta_mV": 5.0, "gate": "m", "generator_seed": 20260917, "mechanism": "forward_rate"}`
- recorded edits: `[{"file": "NMC/NeuroML2/Im.channel.nml", "locator": "/neuroml[@id='Im']/ionChannel[@id='Im']/gate[@id='m']/forwardRate[1]", "attribute": "midpoint", "old": "-35mV", "new": "-30mV", "action": "set", "note": "shift_forward_rate_midpoint"}]`
- execution overrides: `{}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 5126.178 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
