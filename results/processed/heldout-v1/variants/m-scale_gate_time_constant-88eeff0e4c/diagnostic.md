# m-scale_gate_time_constant-88eeff0e4c

*study_id: neuron_model_behavioral_validation | project_name: Neuraxis | study_phase: confirmatory_heldout | protocol_version: HELDOUT_PROTOCOL_V1 | designation: Confirmatory held-out evaluation; preregistered at AsPredicted before any held-out observation; never pooled with development data*

- model: `migliore2005_ca1_soma`
- stratum: primary_semantic
- kind/family/operator: mutant / biophysical / scale_gate_time_constant
- parameters: `{"channel": "kdr", "factor": 2.0, "gate": "n", "generator_seed": 20260917, "mechanism": "q10_insert"}`
- recorded edits: `[{"file": "neuroConstruct/generatedNeuroML2/kdr.channel.nml", "locator": "/neuroml[@id='kdr']/ionChannel[@id='kdr']/gate[@id='n']/q10Settings[1]", "attribute": null, "old": null, "new": "<q10Settings xmlns=\"http://www.neuroml.org/schema/neuroml2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" type=\"q10Fixed\" fixedQ10=\"2\"/>", "action": "insert", "note": "scale_gate_time_constant"}]`
- execution overrides: `{}`
- class: **5_non_equivalent**
- nominal-level status: ok; runtime 3149.834 s

| level | protocol | feature | reason | reference | variant | |diff| | tau | reference run | variant run |
|---|---|---|---|---|---|---|---|---|---|
| h/1 | P00_canonical | adaptation_index | definedness | None | 0.00031104199088017974 |  | inf | `r-1855c6a207dcec8ed210` | `r-7ac8e6c92899d2841bac` |
| h/1 | P00_canonical | ahp_depth | exceeds | -11.854831069263057 | -13.561551298075031 | 1.70672 | 0.592742 | `r-1855c6a207dcec8ed210` | `r-7ac8e6c92899d2841bac` |
| h/1 | P00_canonical | last_isi | exceeds | 18.329999999996353 | 16.0800000000036 | 2.25 | 0.5 | `r-1855c6a207dcec8ed210` | `r-7ac8e6c92899d2841bac` |
| h/1 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1855c6a207dcec8ed210` | `r-7ac8e6c92899d2841bac` |
| h/1 | P04_step_2x | ahp_depth | exceeds | -14.775756835937727 | -15.738685607909929 | 0.962929 | 0.738788 | `r-0925b86f96a976919154` | `r-c9d5935e6b8b8ca16c13` |
| h/1 | P05_long_step | ahp_depth | exceeds | -15.073226928710938 | -15.938896179198295 | 0.865669 | 0.753661 | `r-4ab59c3e1336e488abd6` | `r-06238aebda895420aa0c` |
| h/2 | P00_canonical | adaptation_index | definedness | None | 2.105967261655067e-13 |  | inf | `r-1c8cea9109ae2bf6fdec` | `r-b244abf41fb3c479a46f` |
| h/2 | P00_canonical | ahp_depth | exceeds | -11.804068418284558 | -13.508126064319484 | 1.70406 | 0.592742 | `r-1c8cea9109ae2bf6fdec` | `r-b244abf41fb3c479a46f` |
| h/2 | P00_canonical | last_isi | exceeds | 18.319999999996355 | 16.06000000000357 | 2.26 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-b244abf41fb3c479a46f` |
| h/2 | P00_canonical | spike_count | exceeds | 3.0 | 4.0 | 1 | 0.5 | `r-1c8cea9109ae2bf6fdec` | `r-b244abf41fb3c479a46f` |
| h/2 | P04_step_2x | ahp_depth | exceeds | -14.55389404296919 | -15.492660522460938 | 0.938766 | 0.738788 | `r-6797defd923ff2562240` | `r-de5feb9e0e3997452793` |
| h/2 | P04_step_2x | last_isi | exceeds | 40.049999999963575 | 39.23999999996431 | 0.81 | 0.8012 | `r-6797defd923ff2562240` | `r-de5feb9e0e3997452793` |
| h/2 | P05_long_step | ahp_depth | exceeds | -14.856796264648438 | -15.69654083252 | 0.839745 | 0.753661 | `r-a3b84bbc3dc843d0e573` | `r-fc2ee7cd81a79c24a640` |

Evidence traces: `results/raw/<campaign>/<run_id>/traces.npz` for the run ids above; features in the matching `features.json`. A detection counts toward non-equivalence only if the same protocol and feature are detected at h/1 and h/2.
