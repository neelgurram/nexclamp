# Pilot report: campaign `pilot`

*Generated automatically from `results/processed/pilot/`. Development-stage pilot on discovery models; not a confirmatory result. Thresholds used below for the pilot decision are provisional and must be reviewed by Neel.*

## Setup

- models: pospischil2008_rs, pospischil2008_lts
- nominal dt: 0.005 ms; refinement factors [1, 2, 4]
- mutation families: biophysical, reference, numerical; seed 20260913
- variants: 68 (52 mutants, 16 valid transformations / no-change controls)
- `pospischil2008_rs` rheobase (ok): 0.560652 nA; libNeuroML strict valid: True; 1 of 64 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P01_baseline, P02_weak_step, P08_rebound
- `pospischil2008_lts` rheobase (ok): 0.0386586 nA; libNeuroML strict valid: False; 20 of 64 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P01_baseline, P02_weak_step, P06_ramp, P08_rebound, P09_short_pulse, P10_paired_pulses

## Validation cascade (mutants)

```
{
  "total_mutants": 52,
  "schema_valid": 50,
  "executable": 42,
  "numerically_stable": 41,
  "non_equivalent": 28,
  "canonical_survivors_detected_elsewhere": 3,
  "equivalent_within_tested_domain": 13
}
```

## Classes (all variants)

| class | count |
|---|---|
| 1_structurally_invalid | 2 |
| 2_non_executable | 8 |
| 3_numerically_unstable | 1 |
| 4_equivalent_within_tested_domain | 29 |
| 5_non_equivalent | 25 |
| 6_silent_under_canonical | 3 |

## Pilot success criteria (specification)

1. **At least one admissible mutation passes the canonical protocol and is reproducibly detected by another protocol:** MET (3 silent mutant(s): m-increase_dt-b7cdfa6b5c, m-recording_resolution-7d6e4357af, m-increase_dt-12296e231e).
2. **Feature extraction stable under numerical refinement:** MET -- deterministic re-execution {'pospischil2008_rs': True, 'pospischil2008_lts': True}; 0 of 128 reference (protocol, feature) tolerance entries excluded because their state or category changed between h and h/2; tolerance limited by: {'relative': 29, 'abs_floor': 60, 'exact': 12, 'refinement': 6, 'both_undefined': 21}. (Provisional pilot threshold: fewer than 25% excluded.)
3. **Valid transformations do not trigger widespread false positives:** MET -- 0 of 16 valid transformations/no-change controls were classified non-equivalent. (Provisional pilot threshold: at most 10%.)

## Decision guidance

All three pilot criteria are met on these data. Per Milestone 6 the study may continue to Milestone 7 after Neel reviews the audit sheet, the diagnostics of the silent mutants and the tolerance table.

## Files

- `classification.csv`, `detections.csv`, `detection_matrix.csv`, `protocol_costs.csv`
- `tolerances.csv`, `convergence.csv`, `validation_cascade.json`, `false_positives.csv`
- `mutant_audit_sheet.csv` (Milestone 4 exit criterion: a human must audit at least 20 mutants)
- `variants/<variant_id>/diagnostic.md` (Milestone 5 exit criterion: evidence for every detection)
- `references/<model>/` (protocols, canonical window, rheobase search, fingerprints, determinism)
