# m-recording_resolution-b8ebc2dd19

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `smith2013_singlecomp`
- stratum: numerical_robustness
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260917, "sample_every_ms": 0.05}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.05}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 5148.393 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
