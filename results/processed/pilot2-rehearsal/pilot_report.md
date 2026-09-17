# Pilot report: campaign `pilot2-rehearsal`

- project: **Neuraxis**; study phase: **development_pilot**; protocol version: **PILOT2_PROTOCOL_REHEARSAL**
- designation: Infrastructure rehearsal of the analysis pipeline on a Pilot 1 model; not study data; never reported as a result and never pooled with anything
- findings in this report: **all exploratory; none confirmatory**
- analyses specified before the data were generated: yes, in `docs/PILOT2_PROTOCOL_REHEARSAL.md`
- software commit at report time: `49c86785cba7031b2dbda9a0b5a5c2e5fe60772c` (tree dirty: True); per-run commits are in each `run.json`
- deviations: see `docs/pilot/PILOT2_PROTOCOL_REHEARSAL_DEVIATIONS.md`
- config set SHA-256: `977dea6a424c8dfa91e8fa2482e0c60da7323a4230274f8186a14129901684b1`

**EXPLORATORY / DEVELOPMENTAL DATA.** Never pooled with the held-out data for the primary confirmatory estimate (DECISIONS D-026).

*Generated automatically from `results/processed/pilot2-rehearsal/`. Development-stage pilot; not a confirmatory result. Thresholds used below for the pilot decision are provisional and must be reviewed by Neel.*

## Setup

- models: pospischil2008_rs
- nominal dt: 0.005 ms; refinement factors [1, 2, 4]
- mutation families: biophysical; seed 20260917
- variants: 16 (8 primary semantic mutants, 0 numerical robustness stress tests, 8 valid transformations / no-change controls)
- excluded operators: wrong_segment_group, shift_initial_voltage
- primary feature panel: ['adaptation_index', 'ahp_depth', 'ap_amplitude', 'first_spike_latency', 'last_isi', 'spike_count', 'steady_state_voltage']
- `pospischil2008_rs` rheobase (ok): 0.560652 nA; libNeuroML strict valid: True; 0 of 15 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P07_hyperpolarizing_step

## Validation cascade (primary semantic mutants)

```
{
  "total_mutants": 8,
  "schema_valid": 8,
  "executable": 8,
  "numerically_stable": 8,
  "non_equivalent": 8,
  "canonical_survivors_detected_elsewhere": 0,
  "equivalent_within_tested_domain": 0
}
```

## Classes by stratum

| stratum | class | count |
|---|---|---|
| control | 4_equivalent_within_tested_domain | 8 |
| primary_semantic | 5_non_equivalent | 8 |

## Pilot success criteria (specification; primary semantic stratum and primary feature panel)

1. **At least one admissible semantic mutation passes the canonical protocol and is reproducibly detected by another protocol:** NOT MET (0 silent mutant(s)).
2. **Feature extraction stable under numerical refinement:** MET -- deterministic re-execution {'pospischil2008_rs': True}; 0 of 15 reference (protocol, feature) tolerance entries excluded because their state or category changed between h and h/2; tolerance limited by: {'relative': 6, 'abs_floor': 8, 'refinement': 1}. (Provisional pilot threshold: fewer than 25% excluded.)
3. **Valid transformations do not trigger widespread false positives:** MET -- 0 of 8 valid transformations/no-change controls were classified non-equivalent. (Provisional pilot threshold: at most 10%.)

## Decision guidance

Not all pilot criteria are met. Per the specification: do not manufacture drift. Review the failing criterion; if hidden drift does not exist, reframe as an empirical evaluation of existing validation adequacy or stop.

## Validation levels (model mutants; B and C kept separate)

| level | count |
|---|---|
| A_basic_pass | 8 of 8 |
| B_canonical_feature | 8 of 8 |
| C_canonical_trace | 8 of 8 |
| D_multi_protocol | 6 of 8 |
| E_full_battery | 8 of 8 |
| feature_level_canonical_survivor | 0 of 8 |
| full_trace_canonical_survivor | 0 of 8 |

Branch classification and all prespecified outputs: `pilot_v2_outputs/` (`scripts/pilot_v2_outputs.py`).

## Numerical robustness and convergence stress tests (separate analysis; never semantic drift)

- 0 numerical mutants; cascade: `{"total_mutants": 0, "schema_valid": 0, "executable": 0, "numerically_stable": 0, "non_equivalent": 0, "canonical_survivors_detected_elsewhere": 0, "equivalent_within_tested_domain": 0}`
- missed by canonical but detected elsewhere: 0. These are numerical sensitivities, not hidden semantic drift.
- per-feature deviation versus the reference's own h / h/2 / h/4 discretisation error: `numerical_robustness.csv` (0 rows)

## Secondary exploratory features (reported only; do not change the result above)

- mutants the primary panel classed as equivalent but a secondary feature detected reproducibly: 0
- details: `secondary_feature_report.csv`, `detections_secondary.csv`

## Files

- `classification.csv` (with `stratum` and `interpretation`), `detections.csv`, `detection_matrix.csv` (primary semantic only), `protocol_costs.csv`, `generation.json`
- `tolerances.csv`, `convergence.csv`, `validation_cascade.json`, `false_positives.csv`
- `mutant_audit_sheet.csv` (Milestone 4 exit criterion: a human must audit at least 20 mutants)
- `variants/<variant_id>/diagnostic.md` (Milestone 5 exit criterion: evidence for every detection)
- `references/<model>/` (protocols, canonical window, rheobase search, fingerprints, determinism)
