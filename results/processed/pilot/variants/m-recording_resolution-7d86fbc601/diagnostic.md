# m-recording_resolution-7d86fbc601

- model: `pospischil2008_lts`
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260913, "sample_every_ms": 0.05}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.05}`
- class: **4_equivalent_within_tested_domain**
- nominal-level status: ok; runtime 704.892 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
