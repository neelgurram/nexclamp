# Pilot report: campaign `pilot2`

- project: **Neuraxis**; study phase: **development_pilot**; protocol version: **PILOT2_PROTOCOL**
- designation: Exploratory development data; second development iteration informed by Pilot 1; not independent confirmation; never pooled with the confirmatory held-out estimate
- findings in this report: **all exploratory; none confirmatory**
- analyses specified before the data were generated: yes, in `docs/PILOT2_PROTOCOL.md`
- software commit at report time: `bce1100971479505c70a4d5030a16dcd29695991` (tree dirty: False); per-run commits are in each `run.json`
- deviations: see `docs/pilot/PILOT2_PROTOCOL_DEVIATIONS.md`
- config set SHA-256: `1265b57e7500d39876bcf0a8cff1e4eabfabcfdfeee9b60c818bbade162ce9b9`

**EXPLORATORY / DEVELOPMENTAL DATA.** Never pooled with the held-out data for the primary confirmatory estimate (DECISIONS D-026).

*Generated automatically from `results/processed/pilot2/`. Development-stage pilot; not a confirmatory result. Thresholds used below for the pilot decision are provisional and must be reviewed by Neel.*

## Setup

- models: acnet2_pyr_soma, migliore2014_mt_soma, nml2_hh_example, osb_hh2_477127614, pospischil2008_fs
- nominal dt: 0.005 ms; refinement factors [1, 2, 4]
- mutation families: biophysical, reference, kinetics, numerical; seed 20260917
- variants: 143 (88 primary semantic mutants, 15 numerical robustness stress tests, 40 valid transformations / no-change controls)
- excluded operators: wrong_segment_group, shift_initial_voltage
- primary feature panel: ['adaptation_index', 'ahp_depth', 'ap_amplitude', 'first_spike_latency', 'last_isi', 'rheobase', 'spike_count', 'steady_state_voltage']
- `acnet2_pyr_soma` rheobase (ok): 0.0076156 nA; libNeuroML strict valid: True; 5 of 31 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P02_weak_step, P07_hyperpolarizing_step, P08_rebound, P09_short_pulse
- `migliore2014_mt_soma` rheobase (ok): 0.0246909 nA; libNeuroML strict valid: True; 3 of 31 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P02_weak_step, P07_hyperpolarizing_step, P08_rebound
- `nml2_hh_example` rheobase (ok): 0.022437 nA; libNeuroML strict valid: True; 5 of 31 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P02_weak_step, P06_ramp, P07_hyperpolarizing_step
- `osb_hh2_477127614` rheobase (ok): 0.0644765 nA; libNeuroML strict valid: True; 4 of 31 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P02_weak_step, P07_hyperpolarizing_step, P08_rebound, P09_short_pulse
- `pospischil2008_fs` rheobase (ok): 0.384298 nA; libNeuroML strict valid: True; 1 of 31 reference (protocol, feature) entries undefined at h and h/2 (detectable only by becoming defined); protocols with zero reference spikes: P02_weak_step, P07_hyperpolarizing_step, P08_rebound

## Validation cascade (primary semantic mutants)

```
{
  "total_mutants": 88,
  "schema_valid": 85,
  "executable": 81,
  "numerically_stable": 80,
  "non_equivalent": 75,
  "canonical_survivors_detected_elsewhere": 8,
  "equivalent_within_tested_domain": 5
}
```

## Classes by stratum

| stratum | class | count |
|---|---|---|
| control | 4_equivalent_within_tested_domain | 40 |
| numerical_robustness | 3_numerically_unstable | 1 |
| numerical_robustness | 4_equivalent_within_tested_domain | 12 |
| numerical_robustness | 5_non_equivalent | 1 |
| numerical_robustness | 6_silent_under_canonical | 1 |
| primary_semantic | 1_structurally_invalid | 3 |
| primary_semantic | 2_non_executable | 4 |
| primary_semantic | 3_numerically_unstable | 1 |
| primary_semantic | 4_equivalent_within_tested_domain | 5 |
| primary_semantic | 5_non_equivalent | 67 |
| primary_semantic | 6_silent_under_canonical | 8 |

## Pilot success criteria (specification; primary semantic stratum and primary feature panel)

1. **At least one admissible semantic mutation passes the canonical protocol and is reproducibly detected by another protocol:** MET (8 silent mutant(s): m-scale_conductance-44150b501c, m-scale_conductance-0fd04dc708, m-scale_conductance-a9d05675ab, m-shift_gate_midpoint-c36e1e57f0, m-scale_conductance-d67ea70a4a, m-shift_reversal-c7e1f18cfe, m-duplicate_conductance-06ea96d790, m-wrong_compatible_component-a12a6658b4).
2. **Feature extraction stable under numerical refinement:** MET -- deterministic re-execution {'acnet2_pyr_soma': True, 'migliore2014_mt_soma': True, 'nml2_hh_example': True, 'osb_hh2_477127614': True, 'pospischil2008_fs': True}; 0 of 155 reference (protocol, feature) tolerance entries excluded because their state or category changed between h and h/2; tolerance limited by: {'abs_floor': 76, 'relative': 46, 'both_undefined': 18, 'refinement': 15}. (Provisional pilot threshold: fewer than 25% excluded.)
3. **Valid transformations do not trigger widespread false positives:** MET -- 0 of 40 valid transformations/no-change controls were classified non-equivalent. (Provisional pilot threshold: at most 10%.)

## Decision guidance

All three pilot criteria are met on these data. Per Milestone 6 the study may continue to Milestone 7 after Neel reviews the audit sheet, the diagnostics of the silent mutants and the tolerance table.

## Validation levels (model mutants; B and C kept separate)

| level | count |
|---|---|
| A_basic_pass | 80 of 85 |
| B_canonical_feature | 67 of 85 |
| C_canonical_trace | 60 of 85 |
| D_multi_protocol | 75 of 85 |
| E_full_battery | 76 of 85 |
| feature_level_canonical_survivor | 9 of 85 |
| full_trace_canonical_survivor | 6 of 85 |

Branch classification and all prespecified outputs: `pilot_v2_outputs/` (`scripts/pilot_v2_outputs.py`).

## Numerical robustness and convergence stress tests (separate analysis; never semantic drift)

- 15 numerical mutants; cascade: `{"total_mutants": 15, "schema_valid": 15, "executable": 15, "numerically_stable": 14, "non_equivalent": 2, "canonical_survivors_detected_elsewhere": 1, "equivalent_within_tested_domain": 12}`
- missed by canonical but detected elsewhere: 1 (m-increase_dt-2391bb7a93). These are numerical sensitivities, not hidden semantic drift.
- per-feature deviation versus the reference's own h / h/2 / h/4 discretisation error: `numerical_robustness.csv` (855 rows)

## Secondary exploratory features (reported only; do not change the result above)

- mutants the primary panel classed as equivalent but a secondary feature detected reproducibly: 0
- details: `secondary_feature_report.csv`, `detections_secondary.csv`

## Files

- `classification.csv` (with `stratum` and `interpretation`), `detections.csv`, `detection_matrix.csv` (primary semantic only), `protocol_costs.csv`, `generation.json`
- `tolerances.csv`, `convergence.csv`, `validation_cascade.json`, `false_positives.csv`
- `mutant_audit_sheet.csv` (Milestone 4 exit criterion: a human must audit at least 20 mutants)
- `variants/<variant_id>/diagnostic.md` (Milestone 5 exit criterion: evidence for every detection)
- `references/<model>/` (protocols, canonical window, rheobase search, fingerprints, determinism)
