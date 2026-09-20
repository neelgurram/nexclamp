# Results draft: campaign `pilot2-rehearsal`

*Generated 2026-09-18T22:28:48+00:00 from recorded outputs at commit `292b7d877089eb8739cf062dc5199c1ba5e00b5d` (tree dirty: False). Numbers are copied, never computed here. Bracketed lines are prompts for the researcher.*

> **development_pilot** - Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything

Protocol version `PILOT2_PROTOCOL_REHEARSAL`, study `neuron_model_behavioral_validation`.

## 1. Attrition

Exact counts at every stage; no percentage appears in this section without its counts.

| stage | n |
|---|---|
| variants generated (all strata) | 16 |
| primary semantic mutants | 8 |
| structurally valid and executable | 8 |
| numerically stable | 8 |
| admissible (non-equivalent or silent) | 8 |
| equivalent within the tested domain | 0 |

## 2. Per-model results (the generalization units)

Five models is a small number of clusters, so per-model values are reported beside any pooled figure and never replaced by it (amendment S-01, section 11.1). The right-hand columns repeat the same quantity over the mutants that carry **no prior outcome exposure** (section 11.3).

| model | mutants | admissible | canonical detected | rate | admissible (unexposed) | canonical detected (unexposed) | rate (unexposed) |
|---|---|---|---|---|---|---|---|
| pospischil2008_rs | 8 | 8 | 8 | 1.000 | 8 | 8 | 1.000 |

*No exposure manifest found at `manifests/PILOT2_EXPOSED_VARIANTS.csv`; the unexposed columns repeat the full set.*

## 3. Validation levels A-E

Levels B (canonical features) and C (canonical full trace) are never merged.

| group | n_generated | A_basic_pass | B_canonical_feature | C_canonical_trace | D_multi_protocol | E_full_battery | feature_level_canonical_survivors | full_trace_canonical_survivors |
|---|---|---|---|---|---|---|---|---|
| model_mutants__all_models | 8 | 8 | 8 | 8 | 6 | 8 | 0 | 0 |
| harmless_controls__all_models | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| model_mutants__model__pospischil2008_rs | 8 | 8 | 8 | 8 | 6 | 8 | 0 | 0 |
| harmless_controls__model__pospischil2008_rs | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |

## 4. Unique protocol contribution

Variants that **only** this protocol detected. A protocol that contributes nothing unique is reported as contributing nothing, and cost-matched comparison is required before any battery is called useful (S-01, section 11.2).

| protocol_id | is_canonical | n_detected_only_by_this_protocol | models | analysis_families | variant_ids |
|---|---|---|---|---|---|
| P00_canonical | True | 2 | pospischil2008_rs | maximal_conductance;reversal_potential | m-scale_conductance-a5d53b94c4;m-shift_reversal-80b6724096 |
| P04_step_2x | False | 0 |  |  |  |
| P07_hyperpolarizing_step | False | 0 |  |  |  |
| P03_rheobase | False | 0 |  |  |  |

## 5. Canonical survivors

Each apparent survivor carries its h/4 confirmation status; unconfirmed survivors are never counted as hidden drift.

| rows |
|---|
| 0 |

## 6. Valid-transformation controls (own table, never pooled)

A control classified non-equivalent is a false positive of the method.

| rows |
|---|
| 0 |

## 7. Kinetics: atomic versus compound

Reported separately and never pooled into one kinetics number.

| rows |
|---|
| 0 |

## 8. Uncertain cases

Listed explicitly rather than forced into a class.

| rows |
|---|
| 0 |

## 9. Numerical robustness stratum (separate analysis)

These are convergence stress tests. They never enter the semantic denominator and are never described as hidden semantic drift.

*No numerical stratum rows.*

## 10. Branch classification

- primary branch: **C_canonical_adequacy**
- precedence: D_pipeline_uncertainty > A_hidden_drift_supported > B_feature_level_insufficiency > C_canonical_adequacy > indeterminate

```json
{
  "n_semantic_mutants": 8,
  "n_E_admissible": 8,
  "n_controls": 8,
  "control_false_positives": 0,
  "control_false_positive_rate": 0.0,
  "controls_not_passing_basic_validation": 0,
  "feature_level_survivors": 0,
  "feature_survivors_unconfirmed_h4": 0,
  "confirmed_full_trace_survivors": 0,
  "confirmed_full_trace_survivor_models": [],
  "feature_survivors_detected_by_canonical_trace": 0,
  "refinement_excluded_fraction": 0.0,
  "canonical_B_or_C_detection_rate": 1.0
}
```

Rules were fixed before the data existed and are not re-tuned. Branch A is never forced.

## 11. Claims this dataset does not support

- no claim of universal behavioural equivalence: an undetected difference is evidence about the tested protocols and features, not proof that two models behave identically;
- no claim of broad biological validation: these are single-compartment or somatic cells from a handful of papers;
- every coverage figure is conditional on the empirical reference battery, the frozen tolerance table and the models tested;
- nothing here is confirmatory.

## 12. For the researcher to write

- [ ] [One sentence: what the canonical-versus-battery comparison shows, in plain language.]
- [ ] [One sentence: whether any protocol earned its compute, citing section 4.]
- [ ] [One sentence: what the controls and the numerical stratum say about method noise.]
- [ ] [Limitations paragraph: model count, single simulator unless the cross-simulator check ran, RMSE insensitivity on spiking protocols, and the exposed variants.]

