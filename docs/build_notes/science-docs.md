# Build note: science-docs

*Author: science-docs module (Claude Code subagent), 2026-09-13.*

**This module needs no core or contract change.** The observations below came up while
documenting the protocols, mutations and statistics. Each one affects another module's
design or needs a decision from Neel. They are derived from reading code, configuration
and model files, not from simulation results.

## 1. `increase_dt` with `dt_factor = 2` can never be admissible

- Owner affected: mutations (numerical), validation.fingerprint / convergence.
- A factor-2 mutant run at level h/2 reproduces the reference run at h exactly (identical
  probe inputs, so the run is cached; the canonical harness step is also halved back).
- The h/2 comparison is therefore |f_ref(h) - f_ref(h/2)|. That is at most tau / c, with
  c = 3, so it is never detected at h/2 and never class 5 or 6.
- Suggestion: use factors of 4 or more, or document the family as numerical-sensitivity
  only. See `docs/mutation_catalog.md` section 5.2.

## 2. `record_wrong_variable` may be classified as numerically unstable

- Owner affected: mutations (stimulus), simulators / validation.execution.
- `load_dat` multiplies every column by 1000. A gating variable in [0, 1] becomes 0-1000,
  and `run_lems` flags |v| > 250 as `UNSTABLE` (class 3).
- The mutant then never reaches behavioural comparison. If it should count as a canonical
  detection, the classification needs a rule for it; otherwise report it as class 3 with an
  explanation.

## 3. Stimulus-family mutants can never be class 6

- Owner affected: analysis / preregistration.
- They change only the harness, so only `P00_canonical` can differ.
- Recommend reporting this family separately, or excluding it from the primary comparison
  by a preregistered rule.

## 4. `omit_include` can be masked in the shipped harness

- Owner affected: mutations (reference), classify.
- `LEMS_RS.xml` and `LEMS_LTS.xml` include all channel files directly, so the canonical run
  may still build.
- The generated probe includes only the cell file, so the battery fails to build and the
  mutant becomes class 2.
- Whether that is intended needs Neel's decision.

## 5. `ahp_depth` in `P09_short_pulse` is probably always not applicable

- Owner affected: protocols / features config.
- `configs/features.yaml` gives `ahp_depth` `min_spikes: 2`. A 3 ms pulse is designed to
  evoke one spike, so the feature will almost always be `not_applicable` there.
- A synthetic check with eFEL 5.7.34 and the frozen settings shows that `AHP_depth` *is*
  defined for a single spike: it returned about -9.8 mV on an artificial one-spike trace.
  So `min_spikes: 2` removes the feature, not eFEL.
- Options: set `min_spikes: 1` for `ahp_depth`, or remove it from P09.
- See `docs/protocol_catalog.md` section 5.

## 6. Canonical windows with no baseline

- Owner affected: validation.canonical.
- The Wang-Buzsaki harness stimulus starts at 0 ms, so eFEL's `voltage_base` window
  [0.9 x 0, 0] is empty.
- The IB harness step outlasts the simulation, and its window is clipped.
- Both are candidates only, but the canonical feature state for them should be checked
  before inclusion.

## 7. Valid-transformation verification must not filter on battery results

- Owner affected: transforms, analysis.
- If transforms that the exhaustive battery flags are dropped, the false-positive rate is
  zero by construction.
- Keep semantic verification (inspection and transform tests) separate from battery
  outcomes, and report the battery outcomes.

## 8. Wrong segment group is a no-op in single-compartment models

- Owner affected: mutations (biophysical).
- All groups contain segment 0, and the attribute is absent (XSD default `all`).
- Expected class 4. Consider marking the operator inapplicable for single-compartment
  models so the mutation budget is not wasted.

## 9. Spike detection rules differ slightly between rheobase and eFEL

- Owner affected: protocols.rheobase, features.
- The rheobase counter uses raw upward crossings of -20 mV in the step window. eFEL counts
  peaks after linear interpolation with `Threshold` -20 mV.
- A marginal spike near threshold could be counted by one and not the other. Low risk,
  but worth a unit test on a near-threshold trace.

## 10. Class 6 and DR_canonical use different canonical-detection rules

*Added after review, 2026-09-13.*

- Owners affected: validation.fingerprint (`classify`), experiments.heldout, analysis.
- `classify` calls a mutant silent (class 6) when there is **no canonical detection at h**:
  `canonical_detects` uses `det_h` only.
- The detection matrix (`campaign.py`, `detecting_protocols`) and `evaluate_heldout` use
  **reproducible** detection, meaning the same (protocol, feature) is detected at h and at
  h/2. This applies to every strategy, the canonical protocol included.
- So take a mutant whose canonical detection at h does not reproduce at h/2, and which some
  battery protocol detects reproducibly. It is class 5, yet it counts as a canonical miss
  in the primary endpoint. 1 - DR_canonical can therefore exceed the silent-survival rate.
- No code change is requested here. `docs/statistical_plan.md` section 2 and
  `docs/preregistration_draft.md` sections 2 and 10 now document the implemented rule and
  this gap. Analysis should report the number of such mutants, using the
  `canonical_detected_h` matrix column.
- If Neel wants the two to agree, one of them has to change. Either `classify` switches to
  reproducible canonical detection, or the matrix and `heldout.py` switch to detection at h
  only. Selection and evaluation must keep using one rule.
- `experiments/heldout.py` also hard-codes the bootstrap at B = 10000 and uses
  `selection.seed` as its seed. The preregistration must freeze these values, or the code
  must change before the freeze.
