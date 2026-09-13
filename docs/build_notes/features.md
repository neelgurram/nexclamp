# Build note: `features/` (efel_adapter, regimes, trace_metrics)

Owner module: `src/neurosem/features/`. No core module was edited. This note lists
places where the implementation adds to or interprets ARCHITECTURE.md sections 3.1 to
3.3, and requests for core/config owners.

## Contract additions (backward compatible)

| Function | Addition | Why |
|---|---|---|
| `extract(trace, protocol, cfg, warnings=None)` | `warnings: list[str] \| None` side channel (the contract text left this open: "`|warn`? No: ... side channel") | If a list is given, eFEL `RuntimeWarning`s and adapter notes are appended as `"<protocol_id>: <Category>: <message>"`. If not, they propagate through Python's `warnings`. |
| `extract_all(..., warnings=None)` | same side channel | symmetry |
| `pack_traces(traces, compress=False, finite_only=False)` | optional deflate; optional strict finiteness | Default is ZIP_STORED, so the bytes do not depend on the zlib version. Entries have a fixed timestamp (1980-01-01) and `create_system=3`, so identical traces give identical bytes and SHA-256 on any OS. `np.savez` stamps the current time and is not byte-deterministic. `compress=True` is for disk space. Long h/4 batteries are about 1.6 MB per trace-second uncompressed. `finite_only` is described under interpretation 11. |
| `trace_metrics.grid_params(t)` | new | `(t0, dt, n)` of a verified uniform grid. `dt` is the mean step. |
| `trace_metrics.stored_representation(trace, finite_only=False)` | new | Exactly `unpack_traces(pack_traces({k: trace}))[k]`, for extracting features before a trace is written without changing any number. |
| `efel_adapter.feature_specs(cfg)`, `FeatureSpec` | new | validated view of `features.yaml` |
| `efel_adapter.effective_settings(cfg)` | new | eFEL version plus every eFEL setting as applied, for provenance records (dependency file reduced to its base name) |
| `efel_adapter.is_hyperpolarizing(protocol)`, `stimulus_amplitude_sum_nA` | new | the `requires: hyperpolarizing` rule |
| `FeatureConfigError(ValueError)` | new | config and protocol-feature inconsistencies |
| `regimes.regime_config(cfg)`, `regimes.depolarization_block(...)`, `regimes.LABELS` | new | testable pieces of the regime logic |

`cfg` may be a plain dict or a `neurosem.config.LoadedConfig`. For `LoadedConfig` its `.data` is used.

## Interpretations the integrator should know

1. **Stored representation is the caller's job.** `extract` works on whatever `Trace` it
   is given. To satisfy "features are always extracted from the stored representation",
   `validation.execution` should extract from `unpack_traces(bytes)` or from
   `stored_representation(trace)`. The two are bit-identical. The integration test
   shows that the float64 trace read from jLEMS text gives the same states, counts and
   regime, with voltage and time features within small bounds.
2. **Unpacked voltages are float64** holding exactly the stored float32 values. Every float32 is exactly
   representable in float64, and eFEL converts to double anyway.
3. **Spike-count gating uses the config's `spike_count` entry** (`spike_count_stimint` with
   `strict_stiminterval: true`), so it counts spikes inside the analysis window. For P08
   (rebound) that is the post-release window.
4. **eFEL is called twice per trace.** The first call gets the spike count. The second
   gets only the applicable features. Not-applicable features are never computed, so the
   warnings list holds only warnings for features that were applicable but undefined.
   Settings are `efel.reset()` plus re-applied before each call.
5. **`agg: scalar` with more than one value raises `FeatureConfigError`**, a configuration bug. An empty or
   `None` result is `undefined`. A non-finite eFEL value is `undefined`, with a note in the warnings list.
6. **`requires: hyperpolarizing`**: the protocol is hyperpolarising when the signed sum of its
   pulse amplitudes is negative. A ramp contributes its mean current `(start + finish) / 2`,
   because the contract does not define a ramp's "amplitude".
7. **Trace and window checks in `extract` raise `ValueError`.** A trace with non-finite
   samples raises, because features are not extracted from `UNSTABLE` runs. A window
   entirely outside the trace raises. A window that overruns *either* end of the trace by
   more than one recorded sample step (the trace's mean step, plus 1e-6 of a step for
   rounding) also raises: eFEL would otherwise report `defined` spike counts, frequencies
   or baselines computed over time that was never recorded. An overrun of up to one step
   is accepted with a note in the warnings list ("... by less than one sample step"). That
   covers output sampling (`sample_every_ms`) dropping the final sample. Protocol windows
   from `protocols.definitions` end at or before `total_ms`, and jLEMS output includes
   the sample at `total_ms` (checked in the integration test), so real batteries do not
   trigger the note. `validation.execution` should catch the `ValueError`.
8. **Thread safety.** All eFEL reset/set/extract sequences hold a module-level `RLock`, so
   `run_parallel` threads cannot contaminate each other's settings (tested). Capturing
   warnings uses `warnings.catch_warnings`, which is process-global. Warnings raised by
   unrelated code in other threads during an eFEL call could be captured into that call's
   list. Extraction itself is serialised.
9. **Regime depolarisation block**: "last spike before `gap_fraction` of the window, and the
   *minimum* voltage over [start + fraction x duration, end] stays above the block
   voltage". It needs at least one spike. **A single spike followed by block is labelled
   `single_spike`**, because the contract's label order puts `single_spike` before
   `depolarization_block` and the first match wins (tested in `test_regimes.py`). Tolerance
   and classification analyses should not expect `depolarization_block` for one-spike
   responses. Spike times for this check are upward crossings of `settings.Threshold`
   (`trace_metrics.spike_times`), not eFEL peak times. Label order is taken from
   `firing_regime.labels` in the config, and must be a permutation of the six contract
   labels. If the spike count is not defined, the regime counts window crossings instead.
   It never raises for short or odd traces.
10. `trace_metrics.decimate` refuses an `every_ms` that is not a whole multiple of the step.
    `simulators.jneuroml.load_dat` rounds the stride silently instead. `resample` and
    `align` refuse to extrapolate.
11. **Non-finite voltages in storage.** `validation.execution._finish` packs the traces of
    `UNSTABLE` runs as well as `OK` runs, and re-raises any exception from packing. The
    simulator adapter marks a run `UNSTABLE` for any non-finite sample or |V| above
    `PHYSICAL_V_BOUND_MV` (250 mV), so `OK` traces are always finite and far inside the
    float32 range. `pack_traces` therefore does not refuse non-finite data by default:
    NaN and +/-inf are stored as-is (float32 holds them exactly). A finite sample beyond
    the float32 range (about 3.4e38 mV, reachable only by a diverging run) becomes an
    infinity of the same sign, detected explicitly rather than through a numpy cast
    warning. That is the only case in which stored samples differ from their input, and
    the stored trace stays non-finite, so `extract` refuses it and it can never yield
    features. `finite_only=True` raises `ValueError` for any non-finite or out-of-range
    sample instead. Refusing by default would turn every diverging `UNSTABLE` run into an
    exception in `_finish` and lose its `UNSTABLE` record.
12. **Uniform grid check bounds positions as well as steps.** `is_uniform` and `grid_params`
    require both the largest step deviation and the largest position deviation
    `|t[k] - (t0 + k*dt)|` to be within 1e-6 of a step. Bounding only the steps let small
    same-sign step errors add up. A synthetic 480001-sample grid at dt 0.005 ms passed the
    step check while samples sat 22% of a step off the stored grid. `simulators.jneuroml`
    already replaces jLEMS time labels with the exact grid `t0 + i*dt` (`regularize_time`),
    so real output passes with no margin issue.
13. `unpack_traces` raises `ValueError` (not `OverflowError`) for a non-finite, negative or
    fractional stored sample count.

## Requests for other owners (not edited: not my files)

- **`configs/features.yaml` (config / preregistration owner): make the depolarisation-block
  voltage an explicit, preregistered key.** The -40 mV value appears only in a comment on
  `depolarization_block_min_gap_fraction`. The code reads an optional
  `firing_regime.depolarization_block_v_mV` (default -40.0). It should be added to the YAML
  so it is hashed and frozen with the other parameters. One fixed voltage for all models is
  fragile. In the code review's real-simulation probe (not re-run for this note), the HH
  cell at 2.0 nA fired one spike and then sat on a steady plateau at -40.8 mV, 0.8 mV below
  the -40 mV cut-off. It was labelled `single_spike` (see interpretation 9), and would not
  have counted as block under the -40 mV rule even with a different label order. RS at
  30 nA gave 5 spikes and a plateau near -16.5 mV, correctly labelled
  `depolarization_block`. Consider setting the block voltage per model, or relative to the
  spike `Threshold` or the resting voltage, before the preregistration is frozen. No change
  to the features code is needed for either choice: the key is already read from config.
- `features.yaml` lists `rheobase` with `unit: nA` but no `kind`. `extract` skips it by design.
- `validation/execution.py` (optional hardening): pass `finite_only=(status is RunStatus.OK)`
  to `pack_traces`. For `OK` runs this turns any future simulator that skips the physical-bound
  check into a loud error instead of a stored infinity. `UNSTABLE` runs keep the default.

## Observed facts (this machine, 2026-09-13; no result claims)

- jLEMS OutputFile time grid for the RS probe at dt 0.025 ms: maximum relative step jitter 3.6e-12, far
  inside the 1e-6 uniformity rule. `.dat` voltages carry 8 significant digits (1e-5 mV), about
  the same resolution as float32 at these magnitudes.
- eFEL 5.7.34 on synthetic trains: `strict_burst_number` is 1 (not 0) for a single regular or adapting train,
  2 for two 4-spike bursts, and 3 for three 3-spike bursts. `bursting_min_bursts: 2` is therefore the meaningful
  cut. `adaptation_index2` is 0.0 for perfectly regular trains. `sag_ratio1` returns `None` for a flat
  trace (a real `undefined` case). `mean_frequency` returns a rate for a single spike, which the
  `min_spikes: 2` gate turns into `not_applicable`.
- RS cell, 0.75 nA / 300 ms step, dt 0.025 ms: 4 spikes, AP amplitude about 89.7 mV, half-width about 0.7 ms,
  `adaptation_index2` about 0.29. At -0.25 nA, `sag_ratio1` is about 0.015 although the RS model has no
  h-current. That is a small undershoot, and tolerance calibration should expect such non-zero sag values.
