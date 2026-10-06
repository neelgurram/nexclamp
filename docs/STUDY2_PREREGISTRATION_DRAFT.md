# Study 2 preregistration draft: does the result survive a change of integrator?

*Draft for AsPredicted. Nothing in this document has been run. Written 2026-10-05, before any
NEURON detection has been computed on any held-out variant. Study 1 (AsPredicted #312455) is
sealed and its result is fixed; this is a separate, additive study that reuses Study 1's frozen
variant set but recomputes every detection in a second simulator.*

## Why this study

Study 1 measured detection with one integrator: jLEMS's fixed-step forward Euler. A reviewer can
ask whether the 0.134 gap between canonical regression and the preregistered battery is a property
of the models or of that integrator. The only honest answer is to recompute the endpoint from traces
produced by an independently written simulator. NEURON is the reference implementation in the field,
and jNeuroML translates the same NeuroML sources into NEURON mechanisms, so the comparison uses the
identical model files rather than a hand-ported re-implementation.

`docs/CROSS_SIMULATOR_VALIDATION.md` already records that all seven curated models export and that
the six held-out base models reproduce their published reference traces in NEURON (identical spike
counts; 0.009-0.182 ms worst-case spike-time difference). That establishes the toolchain. It says
nothing about detection, which is what this study measures.

## 1. Data collection

No new models, no new edits, no new protocols. The 186 variants of the sealed `heldout-v1`
campaign are re-exported to NEURON and re-simulated. Nothing about the variant set, the class
assignments or the battery composition may change; all three were fixed before Study 1 ran and are
hash-locked in `configs/FROZEN.lock`.

## 2. Hypothesis

The canonical-versus-battery difference replicates under a second integrator:
`delta_NEURON = p_battery_NEURON - p_canonical_NEURON > 0`, with a 95% interval excluding zero.

A secondary, pre-committed outcome of equal publication value: the difference does **not** replicate,
which would show that the Study 1 gap is partly an artefact of forward-Euler discretisation. Both
outcomes will be reported in full, as in Study 1.

## 3. Dependent variable

For each of the two strategies, the proportion of behaviour-changing faults detected:

- **fault set**: exactly the faults Study 1 classified as class 5 or 6 (admissible,
  behaviour-changing). The classification is an edit-level property established in Study 1 and is
  **not** recomputed here; recomputing it would make the two studies incomparable.
- **detection**: the Study 1 rule, unchanged in form. A feature difference counts when it exceeds
  `tau = max(abs_floor, rel * |f_h|, 3 * |f_h - f_h/2|)` and reproduces at the halved step.
- **tolerances**: recalibrated inside NEURON. The `3 * |f_h - f_h/2|` term is a discretisation-error
  term and must come from NEURON's own refinement (`dt` versus `dt/2`), not from jLEMS's. The
  `abs_floor` and `rel` constants stay at their frozen values.
- **canonical strategy**: the one simulation shipped with the model, as in Study 1.
- **battery strategy**: the same three protocols selected in advance on the development models.

Full-trace quantities (spike count, spike timing, RMSE) are reported separately and never merged
with feature detections, as in Study 1.

## 4. Conditions

Two within-fault conditions, canonical and battery, applied to the same faults. Fixed step
integration with the same `dt` as Study 1's h where the model's shipped simulation permits it;
CVode is not used, because an adaptive solver has no single step to halve and so cannot supply the
calibration term.

## 5. Analyses

Identical to Study 1, with the same code paths:

- primary: paired difference in detection proportion, 95% cluster bootstrap by base model,
  B = 10,000, seed 20260917;
- exact McNemar on discordant faults;
- exact cluster permutation test as a seed-independent check;
- **replication concordance** (new): per-fault agreement between the Study 1 and NEURON detection
  decisions, reported as a 2x2 table with exact McNemar, and the per-fault list of disagreements.

## 6. Outliers and exclusions

Pre-specified and recorded with reasons, not discretionary:

1. A variant whose NeuroML fails to export to NEURON, or whose mechanisms fail to compile, is
   excluded from the NEURON endpoint and listed with its exact error. The same variant stays in the
   Study 1 numbers, which are unchanged.
2. A variant whose NEURON run does not complete, or whose base model's NEURON trace does not
   reproduce its own published reference, is excluded with its diagnostic.
3. No variant is excluded on the basis of its detection outcome, in either simulator.

If more than 20% of faults are excluded for reasons 1-2, the primary endpoint is reported as
exploratory rather than confirmatory, and the exclusion pattern is reported per model.

## 7. Sample size

Fixed by Study 1: 82 behaviour-changing faults across six held-out base models, less any
pre-specified exclusions above. No stopping rule, because the set is enumerated in advance.

## 8. Anything else

- Study 1 is complete, sealed and will be reported whatever this study shows. This study cannot
  change Study 1's numbers; it adds a column.
- Software: NEURON 9.0.2, jNeuroML 0.14.0 / jLEMS 0.12.0, Python 3.12.10, eFEL 5.7.34.
- The NEURON campaign is sealed on completion by the same mechanism as Study 1, and run records are
  content-addressed and write-once.
- A feasibility probe (export, compile and run one variant per base model, to measure wall-clock
  cost and catch toolchain failures) is run **before** this preregistration is submitted. Its only
  output is timing and pass/fail of the toolchain. No detection is computed in the probe, and the
  probe's variants are re-run from scratch in the registered campaign.
