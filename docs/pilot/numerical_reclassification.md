# Pilot 1: time-step and other numerical mutants reclassified

*Neel's decision N-15, recorded as D-030. Exploratory. Pilot 1 is sealed and unchanged. This
reanalysis only reads it and writes to `results/derived/pilot/`, built by
`python scripts/numerical_robustness_report.py --campaign pilot`.*

## In plain English

- Changing the simulator's step size or recording rate is not the same as changing the model.
  Such changes now have their own category: **numerical robustness and convergence stress
  tests**.
- In Pilot 1, the three "hidden" changes were all numerical. With them moved out, Pilot 1 has
  **no hidden semantic drift at all**. The standard test caught every behaviour-changing edit to
  the model itself.
- The time-step results are kept, but they come with a warning: the standard test and the battery
  started from different step sizes, so they were not a fair comparison.

## The confound

`increase_dt` multiplies the step of every run by the same factor. But the starting steps differed:
- the canonical harness started at 0.001 ms (0.004 ms at factor 4);
- the battery started at the nominal 0.005 ms (0.02 ms at factor 4).

Forward Euler error grows with the step. So the battery saw a large numerical error while the
canonical run stayed accurate, and "missed by canonical" mostly reflects that asymmetry, not a
difference in what the tests probe.

## Reclassified counts (from `results/derived/pilot/primary_semantic_summary.json`)

| Stratum | Class counts |
|---|---|
| Primary semantic (biophysical, reference): 40 mutants | 22 non-equivalent, 0 silent, 7 equivalent, 1 unstable, 8 non-executable, 2 invalid |
| Numerical robustness (time step, recording resolution, solver): 12 mutants | 3 missed by canonical, 3 detected by canonical, 6 no reproducible sensitivity |

In-sample paired counts on the 22 admissible semantic mutants:
- detected by both the battery and the canonical harness: 19;
- canonical only: 3;
- battery only: 0;
- neither: 0.

The three numerical mutants missed by canonical are `m-increase_dt-b7cdfa6b5c` (RS, x4),
`m-increase_dt-12296e231e` (LTS, x4) and `m-recording_resolution-7d6e4357af` (RS, 0.25 ms). They
are labelled "numerical_sensitivity_missed_by_canonical (not semantic drift)".

## Convergence view (`results/derived/pilot/numerical_robustness.csv`)

For each numerical mutant, every (protocol, feature) deviation from the reference is compared
with the reference's own discretisation error, |f(h) − f(h/2)|, and the observed order from h, h/2
and h/4. Across 768 entries:
- 390 within 3 times the reference error;
- 177 beyond it;
- 198 unchanged;
- 3 changed definedness.

Pilot 1 ran numerical variants only at h (and h/2 when detected), so variant h/4 values are
absent. Pilot 2 runs every numerical stress test at h, h/2 and h/4.

## What changed in the code

- `src/neurosem/experiments/strata.py` assigns each variant to a stratum: primary semantic,
  numerical robustness, harness stimulus, or control.
- The primary detection matrix, cascade, silent list, pilot criteria, analysis figures and the
  held-out denominator use the semantic stratum only (`primary_admissible`). Numerical mutants get
  `detection_matrix_numerical_robustness.csv`, `validation_cascade_numerical_robustness.json` and
  `numerical_robustness.csv`.
- Primary semantic mutants and controls must carry no execution overrides and no change to step,
  solver method or discretisation (`check_identical_numerics`, called before any simulation).
- Tests: `tests/unit/test_strata.py`.
- The `increase_dt` operator and its Pilot 1 results are kept.
