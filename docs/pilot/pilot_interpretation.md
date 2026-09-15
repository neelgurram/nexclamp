# Pilot (Milestone 6): what the data do and do not show

> **SUPERSEDED (D-038). Historical record only.** Do not use this interpretation in any abstract,
> figure, introduction or publication claim. Corrected Pilot 1 facts: 22 real model edits; the
> canonical test detected all 22; the battery detected 19; no hidden semantic drift; the three
> previously silent cases were numerical stress cases.
>
> **Update (2026-09-13, D-030).** Numerical-setting mutations are now a separate robustness
> experiment. Recounted over model-semantic edits only, Pilot 1 has **0 silent mutants**: the
> canonical harness detected all 22 behaviour-changing semantic mutants, and the battery detected
> 19 of them. The three "silent" mutants below are reclassified as numerical sensitivities, not
> semantic drift. See `docs/pilot/numerical_reclassification.md`. The text below is kept as
> originally written.

*Campaign `pilot`, run 2026-09-13 17:11–18:55 UTC on commit `d323afa`. Two discovery models
(Pospischil 2008 RS and LTS). Development-stage pilot, in-sample, **not a confirmatory result**.
Automatic report: `results/processed/pilot/pilot_report.md`. Figures: `results/figures/pilot/`.
Tables: `results/tables/pilot/`. This note is Claude's interpretation for Neel; the decision is Neel's.*

## In plain English

- We broke two model neurons in 52 controlled ways and made 16 harmless edits.
- The harmless edits never set off an alarm: 0 of 16.
- Every change to the model's *biology* that altered behaviour (conductances, reversal potentials, capacitance, channel speeds, duplicated or swapped channels) was already caught by the model's own standard test. The extra stimuli added nothing there.
- The three "hidden" changes all came from *simulator settings* (a bigger time step or coarser recording). Two of them look hidden partly because the standard test and our battery started from different time steps.
- So the pilot's formal pass criteria are met, but it has **not** yet shown the effect NeuroSem is about: hidden behaviour changes from edits to the model itself. On these two closely related models, the standard test was strong.
- This is exactly the situation where the specification asks you to decide carefully whether to continue, change the plan, or stop. It warns: do not manufacture drift.

## 1. Numbers (from `classification.csv`, `validation_cascade.json`, `analysis_summary.json`)

| | count |
|---|---|
| Mutants generated | 52 (26 per model; biophysical, reference and numerical families) |
| Structurally invalid (class 1) | 2 |
| Non-executable (class 2) | 8 (3 of them: the shipped harness still runs, the reused model does not) |
| Numerically unstable (class 3) | 1 |
| Equivalent within tested domain (class 4) | 13 |
| Non-equivalent, canonical detects (class 5) | 25 |
| Silent under canonical, detected elsewhere (class 6) | 3 |
| Valid transformations / no-change controls flagged | **0 of 16** (Clopper-Pearson 95 % interval 0 to 0.21, units treated as independent) |

**In-sample paired comparison** on the 28 admissible mutants (discovery data; 2 correlated models; `reliable = false`):

| | canonical detects | canonical misses |
|---|---|---|
| battery (P01–P10 without canonical) detects | 21 | 3 |
| battery misses | 4 | 0 |

The battery detected 24 of 28 (0.86); the canonical protocol detected 25 of 28 (0.89).

**Tolerance sensitivity** (`tolerance_sensitivity.csv`): the false-positive rate is 0 at multipliers 0.5, 1, 2 and 4. The silent fraction of mutants is 3.9 %, 5.8 %, 5.8 % and 1.9 %. The admissible fraction falls from 55 % to 35 % as tolerances loosen. One variant is not evaluable at multiplier 0.5.

## 2. Pilot criteria versus substance

| Criterion (spec) | Formal result | What it rests on |
|---|---|---|
| 1. ≥ 1 admissible mutation passes canonical and is reproducibly detected elsewhere | Met (3) | Only numerical-configuration mutants (see section 3) |
| 2. Feature extraction stable under refinement | Met | 0 of 128 reference entries changed state between h and h/2; bitwise-identical reruns. LTS has 20 of 64 reference entries undefined, a weak battery for that cell (N-07). |
| 3. No widespread false positives | Met | 0 of 16; the interval is wide with n = 16 |

## 3. The three silent mutants

1. **`m-increase_dt-b7cdfa6b5c` (RS) and `m-increase_dt-12296e231e` (LTS), x4 time step.**
   - What changed: the shipped harness step went from 0.001 ms to 0.004 ms. The battery step went from 0.005 ms to 0.02 ms.
   - What detected it: forward-Euler error at 0.02 ms shifts AHP depth by about 2.5 mV, first ISI by about 1 ms, and spike count by 1 (in P04 and P05).
   - Why canonical stayed quiet: at 0.004 ms the canonical run stays accurate. For LTS, the canonical detection seen at h did not reproduce at h/2, and under the single reproducible rule (D-021) that counts as not detected.
   - Interpretation: the silence is largely an artefact of the harness and the battery using different base steps. It is not evidence that other stimuli reveal hidden behaviour. It is the circularity between the numerical family and tolerance calibration raised in the NUM critique (`RISK_REGISTER.md`).
2. **`m-recording_resolution-7d6e4357af` (RS), output sampled every 0.25 ms.**
   - Action-potential amplitude and half-width change in P05 and P09. This is expected when a 0.7 ms spike is sampled at 0.25 ms.
   - It is a genuine configuration fault that passed the canonical test, but a scientifically trivial one.

## 4. What the biophysical and reference families show

- **Every behaviour-changing biophysical mutant was class 5.** The canonical harness detected each one reproducibly. This includes conductance x0.9 on a single channel, capacitance x1.1, reversal shifts of ±5 mV, and gate time constants x1.25.
- **Equivalent mutants were the expected no-ops plus small, transient changes:**
  - `wrong_segment_group` (4) in single-compartment cells;
  - `solver_config` (4), because jLEMS ignores `Meta`;
  - `shift_initial_voltage` of +2 or -5 mV (3), which relaxes away before the stimulus;
  - output sampling at 0.05 ms (2).
- **Reference mutants mostly crashed or failed validation.** `wrong_compatible_component` gave 4 build errors, `omit_include` 2 invalid and 2 non-executable, `wrong_channel` 2 non-executable and 1 unstable. This touches the pivot criterion "most mutations only crash or violate schema" for that family.

## 5. Why this may be specific to the pilot (not yet a conclusion)

- **Strong canonical harnesses.** Both are 1000 ms steps at 0.001 ms with 11 features, including adaptation and ISIs. Many published models ship weaker tests.
- **Correlated models.** Both come from one paper and share channel files. Other cell classes and sources may behave differently.
- **Coarse mutation grid.** The sampled magnitudes were all at least 10 % or 2 mV. Smaller faults, and faults in rarely exercised mechanisms (for example T-type rebound, which the LTS battery barely drives, N-07), were not sampled.
- **Weak LTS battery.** Several protocols evoked no spikes in LTS, so its fingerprint is thin.

## 6. Options for Neel (the specification's Milestone 6 decision)

The spec's rule: "Continue only if canonical testing misses at least some reproducible non-equivalent mutants and additional protocols detect them without unacceptable false positives. If no hidden drift exists, do not manufacture it. Reframe the project as an empirical evaluation of the adequacy of existing validation or stop."

1. **Treat criterion 1 as not substantively met for model edits.** Before any further scaling, run a second pilot with protocols and design frozen *before* looking at it, on independent models: the curated candidates (N-09), including small-soma and Ih/rebound cells, and ideally models whose shipped tests are weaker. Align the canonical and battery base steps, or drop `increase_dt` from the primary families, so numerical artefacts cannot create silent mutants.
2. **Reframe now** as an empirical evaluation of how adequate existing (canonical) validation is across NeuroML models. The current pilot is itself a first data point: canonical tests caught every behaviour-changing biophysical edit here.
3. **Continue to Milestone 7 as specified**, counting the numerical silent mutants. This is not recommended, because the result would rest on the time-step asymmetry.

Whatever the choice, it must be recorded before any held-out work, and the protocol amplitudes for low-rheobase cells (N-07) must be settled on discovery data only.

## 7. Provenance note

The pilot reused 75 cached simulations from earlier development runs:
- the reference warm-up and the integration check, on commits `5184ce9`, `0317355` and `751ee99`;
- 38 of those were recorded with a dirty working tree.

Runs are content-addressed on every file the simulator reads, plus the settings and jar, so the cached traces are exactly what the same inputs produce. Features were re-extracted under the current feature code. Even so, the frozen study should run as a fresh campaign on a clean, committed tree with no cross-commit reuse (DECISIONS D-025).
