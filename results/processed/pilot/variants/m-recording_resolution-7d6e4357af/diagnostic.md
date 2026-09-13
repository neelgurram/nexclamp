# m-recording_resolution-7d6e4357af

- model: `pospischil2008_rs`
- kind/family/operator: mutant / numerical / recording_resolution
- parameters: `{"generator_seed": 20260913, "sample_every_ms": 0.25}`
- recorded edits: `[]`
- execution overrides: `{"sample_every_ms": 0.25}`
- class: **6_silent_under_canonical**
- nominal-level status: ok; runtime 1449.85 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P05_long_step | ap_amplitude | exceeds | 89.18265915023935 | 84.4117355294313 | 4.77092 | 1.78365 | `r-6299bd8dadd5e9592d63` | `r-23a42b89179af0150565` |
| h/1 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.7799999999992906 | 0.08 | 0.05 | `r-6299bd8dadd5e9592d63` | `r-23a42b89179af0150565` |
| h/1 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.9699999999991178 | 0.09 | 0.05 | `r-4a031cb8037cbebd46bc` | `r-69682a360336c0b1303a` |
| h/2 | P04_step_2x | ap_amplitude | exceeds | 89.44855880885186 | 86.93050001503505 | 2.51806 | 1.78992 | `r-13ae588754662eb409bf` | `r-996e9431f4326b1dbc4c` |
| h/2 | P05_long_step | ap_amplitude | exceeds | 89.08078384555085 | 82.36533351582165 | 6.71545 | 1.78365 | `r-a71c890435a70aeaf61b` | `r-db007c32dac81a51cd9e` |
| h/2 | P05_long_step | ap_half_width | exceeds | 0.6999999999993634 | 0.7699999999992997 | 0.07 | 0.05 | `r-a71c890435a70aeaf61b` | `r-db007c32dac81a51cd9e` |
| h/2 | P09_short_pulse | ap_half_width | exceeds | 0.8799999999991996 | 0.9799999999991087 | 0.1 | 0.05 | `r-fa41d650658e23c878d5` | `r-7be5f11eae92d24f09ae` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
