# Canonical baseline audit (Pilot 1)

*What Pilot 1 called the "standard" or canonical test, exactly, and whether it represents
existing model-testing practice. Sources:
- `results/processed/pilot/references/*/canonical_protocol.json`;
- `results/processed/pilot/tolerances.csv`;
- `src/neuraxis/validation/canonical.py`;
- `src/neuraxis/validation/fingerprint.py` (at Pilot 1's code tag `pilot-v1-code`, the same logic);
- the prior-art verification packets in `docs/prior_art/packets/`.

Written 2026-09-17, before Pilot 2.*

## In plain English

- **What the test was.** Pilot 1's "standard test" reran the simulation file shipped with each model:
  one current step. It then compared 11 measurements (spike count, firing rate, spike shape,
  adaptation, firing type and others) against the unedited model, with tolerances set from
  numerical accuracy.
- **What it did not do.** It did not compare the whole voltage trace point by point. Nor did it
  compare exact spike times, which is what the OpenSourceBrain tests (OMV) do.
- **Stronger than common practice.** It was stronger than "does it run?" and richer than a single
  spike count.
- **But a different kind of check.** Common practice (OMV) is a hand-set tolerance on expected spike
  times. So Pilot 1's baseline was a feature-level canonical regression, not an OMV-style
  spike-time regression and not a full-trace regression. Pilot 2 keeps these as separate levels.

## 1. Stimulus, amplitude, duration and time step

| Model | Stimulus (shipped harness) | Amplitude | Onset, duration | Simulation length | Time step | Analysis window |
|---|---|---|---|---|---|---|
| `pospischil2008_rs` | one `pulseGenerator` in `RS.net.nml` | 0.75 nA | 300 ms, 400 ms | 1000 ms | 0.001 ms (shipped) | 300-700 ms |
| `pospischil2008_lts` | one `pulseGenerator` in `LTS.net.nml` | 0.15 nA | 400 ms, 400 ms | 1000 ms | 0.001 ms (shipped) | 400-800 ms |

- **Harness files.** The harness ran unchanged. Its stimulus was **not** rheobase-scaled; it used the
  model author's own amplitude.
- **Refinement.** For refinement, the harness step was divided by 2 (h/2) and 4 (h/4). The battery
  protocols instead ran at 0.005 ms, so the two step sizes differed.
- **Window.** The analysis window was the union of the pulses that target the recorded population.

## 2. What was compared

| Aspect | Pilot 1 canonical test |
|---|---|
| Execution only | Part of it: a variant whose harness failed to run was class 2 (non-executable), before any comparison |
| Spike count | Yes (`spike_count_stimint`; any change of at least 1 spike is detected) |
| Electrophysiological features | **Yes, 11 features:** baseline voltage, spike count, mean frequency, first-spike latency, AP amplitude, AP half-width, AHP depth, first ISI, last ISI, adaptation index, firing regime |
| Full voltage trace | **No.** No point-wise or RMSE comparison of traces |
| Spike timing | Only through latency and first/last ISI; not the full spike-time list |
| Discrete firing rules | Firing regime (silent / single spike / depolarisation block / bursting / adapting / tonic), exact match required; spike count as a count; a change in definedness (a feature appearing or disappearing) counts as a detection |
| Trace metrics | None used for detection. RMSE and max-difference helpers exist in `features/trace_metrics.py` but were not part of classification |

## 3. Tolerances and detection logic

- **Tolerance formula.** For each (model, feature): τ = max(abs floor, rel × |f_ref(h)|,
  3 × |f_ref(h) − f_ref(h/2)|).
  - Floors and relative terms come from `configs/tolerances.yaml`.
  - The refinement term is measured on the unedited model's harness at h and h/2.
- **Values used in Pilot 1.**

  | Model | Spike count | Latency | Mean frequency | First ISI | Adaptation index |
  |---|---|---|---|---|---|
  | RS | 5 ± 0.5 | 20.75 ± 0.5 ms | 17.03 ± 0.85 Hz | 28.07 ± 0.56 ms | 0.299 ± 0.030 |
  | LTS | 4 ± 0.5 | 31.63 ± 0.63 ms | 12.32 ± 0.62 Hz | 14.16 ± 0.60 ms (refinement-limited) | 0.450 ± 0.045 |

  Firing regime: exact.
- **Detection rule.** A feature detects when |variant − reference| > τ at the nominal step and
  again at h/2 (same protocol, same feature).
- **Canonical detection.** The canonical test "detects" a mutant if any of its features does so
  reproducibly.
- **Silent mutant.** A mutant was "silent" (class 6) when the canonical test did not detect it but a
  battery protocol did.

## 4. Is this baseline representative of existing practice?

**Evidence from the verified prior-art packets** (researcher inspection of the packets is still
pending):

- **OMV** (`docs/prior_art/packets/omv-osb-model-validation.md`) is the conventional regression check
  for Open Source Brain NeuroML models.
  - Checks run in order: schema and LEMS checks, then a comparison of simulation outputs such as
    **spike times** with expected values in a MEP file.
  - Comparison uses `numpy.allclose` with a relative tolerance **set by hand** per observable
    (default 0.1 when none is given).
  - Pospischil's own MEP file lists the RS spike times (320.554, 348.522, 387.944, 456.69,
    592.105 ms).
- **NeuroML-DB** (`docs/prior_art/packets/neuroml-db-birgiolas-2023.md`) characterises models under
  standard stimulus protocols but sets **no** numerical tolerances. It reports no detection or
  false-alarm rates.
- **Other packets.** The workflow papers (Reva et al. 2023) and the effective-stimuli work (Druckmann
  et al. 2011) use multi-feature, multi-stimulus comparisons for *fitting and validation against
  data*, not as regression tests of transformed models.

**Assessment:**

1. **Relative to OMV, the baseline differs in kind.**
   - More features (11 versus spike times only).
   - Tolerances set from numerical refinement rather than by hand; often tighter for timing features
     (±0.5 ms latency, versus OMV's default 10% relative), sometimes looser.
   - No full spike-time list and no trace comparison.
   - So it is not a faithful replica of OMV, and neither "stronger" nor "weaker" everywhere. A
     mutant that shifts, say, the third spike time without changing count, latency, first/last ISI
     or adaptation beyond tolerance would pass Pilot 1's canonical test but could fail an OMV
     spike-time check.
2. **Relative to "does it run?", it is much stronger.** A study that uses only execution as the
   baseline would overstate the value of extra protocols.
3. **Pilot 1's conclusion must be read as feature-level.** "The canonical feature regression caught
   all 22 real model edits". That is not the same as full-trace or spike-time regression, and not
   the same as execution-only checking.

## 5. Consequences for Pilot 2 (PILOT_PROTOCOL_V2)

Pilot 2 reports five validation levels separately:

| Level | Content |
|---|---|
| A. Basic | structure, dimensions, references, execution |
| B. Canonical feature regression | the Pilot 1 kind of check: the primary feature panel on the shipped stimulus |
| C. Canonical full-trace regression | the same stimulus, compared on the full voltage trace, the full spike-time list and discrete firing outcomes, with thresholds calibrated from h versus h/2 |
| D. Multi-protocol perturbation testing | additional protocols, with feature, trace and qualitative comparisons |
| E. Full candidate battery | the empirical reference battery (not a proof of equivalence) |

Levels B and C are never merged. Level C's spike-time comparison is the closest Neuraxis analogue to
an OMV spike-time check with a calibrated rather than hand-set tolerance.
