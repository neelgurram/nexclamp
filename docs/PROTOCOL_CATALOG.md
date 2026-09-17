# Protocol catalogue

*Status: draft, 2026-09-13. The source of truth is `DEFAULT_TEMPLATES` in
`src/neuraxis/protocols/definitions.py`, as overridden by the `protocols:` list in
`configs/study.yaml`, which currently names all twelve templates with no parameter
overrides. `data/protocol_manifest.csv` is generated from them by
`scripts/build_protocol_manifest.py`, and a unit test fails if the CSV is stale. All
parameters are **provisional** until preregistration. Statements marked **expected** are
not results.*

## 1. Rules shared by every protocol

**Rheobase normalisation.** R is the reference model's rheobase in nA, found by
`P03_rheobase`. Depolarising and hyperpolarising amplitudes are multiples of R, so "2 x
rheobase" means the same test in every model. Each template is instantiated **once per
reference model**, and every variant of that model gets exactly the same concrete stimulus.
If the reference is spontaneously active, the search status is `spontaneous` and protocols
use `fallback_rheobase_nA` = 0.1 nA. The rule for a `not_found` or `error` search on a
reference is not yet fixed; it is listed in the preregistration draft.

**Settling period.** Every probe cell starts with s = `settle_ms` = 300 ms of zero
current, and every stimulus starts at s. This lets initial-condition transients die away,
and eFEL's baseline window (the last 10 % before the analysis window starts) falls inside
this quiet period for most protocols.

**Timing on the grid.** All delays and durations are whole milliseconds. With
h = 0.005 ms, h/2 = 0.0025 ms and h/4 = 0.00125 ms, every stimulus edge falls exactly on a
time step at every refinement level, so refinement never moves the stimulus.

**One battery, one JVM per length.** `protocols/generate.py` writes a NeuroML network in
which each protocol is its own uncoupled single-cell population with its own inputs, plus a
LEMS file that records `v` of every population. Protocols with the same total length share
one simulation (`group_by_length`). The network uses the model's temperature
(`networkWithTemperature`) and a fixed seed (12345). The fixtures contain no stochastic
elements.

**Stimulus components.** `pulseGenerator` (delay, duration, amplitude) and `rampGenerator`
(delay, duration, start amplitude 0, finish amplitude, baseline 0). These are NeuroML
v2.3.1 core inputs.

**Feature extraction (eFEL 5.7.34, `configs/features.yaml`).** Before every trace eFEL is
`reset()` and then given `Threshold` -20 mV, `DerivativeThreshold` 10 mV/ms,
`DownDerivativeThreshold` -12 mV/ms, `interp_step` 0.01 ms, `strict_stiminterval` true,
`ignore_first_ISI` false and `strict_burst_factor` 2.0. The protocol's analysis window is
passed as `stim_start` / `stim_end`. Window conventions that matter, verified from eFEL
documentation or by a synthetic check:

| eFEL feature | Window it uses |
|---|---|
| `voltage_base` | mean V over [0.9 x stim_start, stim_start] |
| `steady_state_voltage_stimend` | mean V over the last 10 % of the window |
| `minimum_voltage`, `maximum_voltage` | inside [stim_start, stim_end] (synthetic check: excursions outside the window were ignored) |
| `spike_count_stimint` | peaks with stim_start <= t <= stim_end |
| `mean_frequency` | spikes strictly inside the window / (last spike time - stim_start) |
| `time_to_first_spike` | first spike **peak** time - stim_start |

**Feature states.** A feature is `not_applicable` when fewer spikes occur than its
`min_spikes`. It is also `not_applicable` when it `requires: hyperpolarizing` and the
protocol's summed stimulus amplitude is not negative. eFEL returning `None` means
`undefined`. Nothing is replaced by zero.

## 2. Timing table (settle = 300 ms, R = rheobase)

Components are written as "kind delay/duration amplitude". Cell-steps are for the protocol
run alone at h = 0.005 ms (total ms / h).

| protocol_id | stimulus components | analysis window (ms) | total simulated (ms) | cell-steps at h |
|---|---|---|---|---|
| P01_baseline | pulse 300/700 ms, 0 nA | 300-1000 | 1000 | 200,000 |
| P02_weak_step | pulse 300/500 ms, +0.5 x R | 300-800 | 1000 | 200,000 |
| P04_step_2x | pulse 300/500 ms, +2 x R | 300-800 | 1000 | 200,000 |
| P05_long_step | pulse 300/2000 ms, +1.5 x R | 300-2300 | 2500 | 500,000 |
| P06_ramp | ramp 300/1000 ms, 0 to +3 x R | 300-1300 | 1500 | 300,000 |
| P07_hyperpolarizing_step | pulse 300/500 ms, -1 x R | 300-800 | 1000 | 200,000 |
| P08_rebound | pulse 300/500 ms, -2 x R | 800-1100 | 1100 | 220,000 |
| P09_short_pulse | pulse 300/3 ms, +10 x R | 300-360 | 500 | 100,000 |
| P10_paired_pulses | pulses 300/3 ms and 323/3 ms, +10 x R each | 300-380 | 500 | 100,000 |

`P03_rheobase` is a search, not a single stimulus (section 3). `P11_chirp` and
`P12_frozen_noise` are not implemented (section 7).

## 3. Protocol entries

Each entry lists its purpose (the specification's protocol number), exact rule, window,
features, and caveats.

### P01_baseline: zero-current baseline (spec 1)

- **Rule.** Pulse of 0 nA from s for `duration_ms` = 700. Total s + 700.
- **Window.** [s, s + 700] = [300, 1000].
- **Features.** `baseline_voltage`, `steady_state_voltage`, `spike_count`,
  `firing_regime`.
- **Why.** Detects changes in resting potential (e.g. a leak `erev` shift) and spontaneous
  firing that should not be there.
- **Note.** The zero-amplitude pulse keeps every protocol's population structure identical.
  `baseline_voltage` averages [270, 300] ms, and `steady_state_voltage` averages the last
  70 ms of the window.

### P02_weak_step: weak depolarising step (spec 2)

- **Rule.** Pulse of +`multiple` x R = +0.5 R from s for 500 ms, then 200 ms without
  current. Total s + 700.
- **Window.** [s, s + 500].
- **Features.** `baseline_voltage`, `steady_state_voltage`, `voltage_deflection`,
  `spike_count`.
- **Why.** A subthreshold probe of passive properties. The deflection is roughly current x
  input resistance, so conductance or capacitance changes show up here without spikes.
- **Expected.** Silent, because R is defined with the same 500 ms step duration. A spike
  here would itself be informative (non-monotonic excitability).

### P03_rheobase: rheobase search (spec 3)

- **Rule (`protocols/rheobase.py`, `configs/study.yaml` `rheobase:`).** Each simulation is
  one batched probe of `grid` = 12 cells. Each cell gets s = 300 ms settling, then a 500 ms
  step at one amplitude. Spikes are counted as upward crossings of -20 mV inside the step.
  1. **Bracketing.** The grid spans [0, 0.5] nA. If no amplitude spikes, the grid moves
     up: [0.5, 2], [2, 8], [8, 32] (expand x 4, cap 32 nA). If 0 nA already spikes, the
     status is `spontaneous`. If nothing spikes up to 32 nA, it is `not_found`.
  2. **Refinement.** Up to `rounds` - 1 = 3 more grids of 12 across [last silent, first
     spiking]. The search keeps the previous bracket if the response inside it is
     non-monotonic.
  3. **Result.** The first spiking amplitude, with resolution = final bracket width.
- **Feature.** `rheobase` (nA), computed **on each variant itself**.
- **Tolerance.** `abs_floor` 0 and `rel` 0.02, with the floor raised to at least 2 x the
  search resolution (`resolution_multiple`).
- **Arithmetic example.** If the first grid brackets the rheobase, its spacing is
  0.5 / 11 = 0.0455 nA. Three refinements divide it by 11 each, giving
  0.0455 / 1331 = 3.4e-5 nA. The resolution floor (about 7e-5 nA) is then far below the
  2 % relative term for any rheobase above about 0.004 nA.
- **Cost.** One simulation = 12 cells x (800 ms / 0.005 ms) = 1,920,000 cell-steps at h.
  The number of simulations depends on the outcome (`search` in `protocols/rheobase.py`):
  - 1 if 0 nA already spikes (`spontaneous`), or the first run fails (`error`);
  - exactly 4 if nothing spikes up to 32 nA (`not_found`);
  - 2-7 for status `ok` (1-4 bracketing + 1-3 refinement);
  - between 1 and 7 for an `error` in a later run.

  So a search costs up to 7 simulations, or 13,440,000 cell-steps. **That is several times
  the rest of the battery** (section 6).

### P04_step_2x: step at a fixed multiple of rheobase (spec 4)

- **Rule.** Pulse of +2 R from s for 500 ms, then 200 ms without current. Window
  [s, s + 500].
- **Features.** The 11 spiking features: `spike_count`, `mean_frequency`,
  `first_spike_latency`, `ap_amplitude`, `ap_half_width`, `ahp_depth`, `first_isi`,
  `last_isi`, `adaptation_index`, `burst_count`, `firing_regime`.
- **Why.** A standard suprathreshold response, comparable across models because it is
  rheobase-scaled.

### P05_long_step: long suprathreshold step (spec 5)

- **Rule.** Pulse of +1.5 R from s for 2000 ms, then 200 ms without current. Window
  [s, s + 2000].
- **Features.** The same 11 spiking features.
- **Why.** Slow processes (e.g. IM activation over hundreds of milliseconds, adaptation)
  need time to show. A 400 ms canonical step may end before they matter (**expected**,
  unverified).

### P06_ramp: depolarising ramp (spec 6)

- **Rule.** Ramp from 0 to +3 R over 1000 ms starting at s, then 200 ms at baseline 0.
  Window [s, s + 1000].
- **Features.** `spike_count`, `first_spike_latency`, `mean_frequency`, `firing_regime`.
- **Why.** The first-spike latency on a ramp encodes the *current* at which firing starts:
  a latency of L ms means the current was 3 R x L / 1000 nA (arithmetic). This probes
  dynamic threshold and accommodation rather than a fixed step.

### P07_hyperpolarizing_step: hyperpolarising step (spec 7)

- **Rule.** Pulse of -1 R from s for 500 ms, then 200 ms without current. Window
  [s, s + 500].
- **Features.** `baseline_voltage`, `steady_state_voltage`, `voltage_deflection`,
  `sag_ratio` (applicable because the summed amplitude is negative), `minimum_voltage`.
- **Why.** Passive properties below rest, plus sag if an Ih-like current exists.
- **Caveats.** No current manifest model contains Ih, so `sag_ratio` is **expected** to be
  uninformative (`docs/model_selection.md` section 7). eFEL's `sag_ratio1` is undefined
  when baseline equals minimum voltage. The hyperpolarising amplitude scales with R, so
  high-rheobase models are pushed harder.

### P08_rebound: hyperpolarisation-release rebound (spec 8)

- **Rule.** Pulse of -|`multiple`| x R = -2 R from s for 500 ms. The window starts at
  release (s + 500) and lasts `post_window_ms` = 300. Total s + 800.
- **Window.** [800, 1100].
- **Features.** `spike_count`, `first_spike_latency` (measured from release),
  `maximum_voltage` (within the post-release window), `firing_regime`.
- **Why.** T-type Ca currents are de-inactivated by hyperpolarisation and can fire the cell
  on release. LTS contains IT, so a rebound response is **expected but unverified**. RS
  has no T-current, so none is expected.
- **Caveat.** eFEL's baseline window here is [720, 800] ms, *inside* the hyperpolarisation.
  None of P08's features uses `voltage_base`. Adding a baseline-relative feature (e.g.
  `ahp_depth`) to P08 would silently measure relative to the hyperpolarised level.

### P09_short_pulse: short suprathreshold pulse (spec 9)

- **Rule.** Pulse of +10 R for `pulse_ms` = 3 from s. Window [s, s + `window_ms`] =
  [300, 360]. Total s + 60 + 140.
- **Features.** `spike_count`, `first_spike_latency`, `ap_amplitude`, `ap_half_width`,
  `ahp_depth`.
- **Why.** Isolates the shape of a single action potential with little ongoing current.
- **Caveats.**
  1. Whether 10 R for 3 ms evokes a spike depends on the membrane time constant; this is
     **expected**, not guaranteed.
  2. `ahp_depth` now has `min_spikes: 1` (DECISIONS D-021), because eFEL computes
     `AHP_depth` for a single spike (section 5; `docs/build_notes/science-docs.md` item 5).
  3. eFEL measures `AP_amplitude` from a derivative-threshold onset, and the fast charging
     by a large brief pulse may shift that onset.

### P10_paired_pulses: paired pulses (spec 10)

- **Rule.** Two pulses of +10 R, each 3 ms. The first starts at s. The second starts at
  s + `pulse_ms` + `interval_ms` = s + 23 (the 20 ms interval is from the end of the first
  pulse to the start of the second). Window [s, s + 80]. Total s + 200.
- **Features.** `spike_count`, `first_spike_latency`, `first_isi`, `ap_amplitude` (first
  spike).
- **Why.** Recovery from the first spike: refractoriness, and whether a second spike
  occurs and when.

### P00_canonical: the shipped harness (conventional regression baseline)

- **Rule.** Run the model's own LEMS harness unchanged (`harness_lems` in the manifest).
  At refinement level k the harness `step` is divided by k.
- **Window (`validation/canonical.py`).** The union of the pulses in the **reference** harness
  that target the recorded population (the population named in the harness `OutputColumn` used
  as the voltage column): [earliest onset, min(latest offset, simulation length)]. If no
  targeting input can be identified, all pulse generators are used; with no pulse it is
  [0.1 x length, length]. The rule applied is recorded in the protocol description, and the
  window is reused for every variant (DECISIONS D-021).
- **Features.** `CANONICAL_FEATURES` (11): `baseline_voltage`, `spike_count`,
  `mean_frequency`, `first_spike_latency`, `ap_amplitude`, `ap_half_width`, `ahp_depth`,
  `first_isi`, `last_isi`, `adaptation_index`, `firing_regime`.
- **Pilot harnesses.**
  - RS: 0.75 nA, window [300, 700] ms, 1000 ms at step 0.001 ms.
  - LTS: 0.15 nA, window [400, 800] ms, 1000 ms at step 0.001 ms.
  - The canonical stimulus is **not** rheobase-scaled. It is whatever the model's authors
    shipped.
- **Why analysed with the same features and tolerances.** Canonical and battery then differ
  only in the stimulus, not in the metric. This is stricter than OMV's usual spike-time
  comparison, which is a deliberate choice so the baseline is not a straw man.

## 4. Fingerprint size

The implemented templates list 53 (protocol, feature) entries (P01 4, P02 4, P03 1,
P04 11, P05 11, P06 4, P07 5, P08 4, P09 5, P10 4). Adding the 11 canonical features gives
**64 entries per model per time step**. Some entries will be `not_applicable` for a given
model, for example spiking features in a protocol where the cell stays silent.

## 5. Feature definitions

| NeuroSem feature | Source | Aggregation | Unit | min_spikes | Definition |
|---|---|---|---|---|---|
| baseline_voltage | eFEL `voltage_base` | scalar | mV | 0 | mean V over [0.9 x start, start] |
| steady_state_voltage | eFEL `steady_state_voltage_stimend` | scalar | mV | 0 | mean V over the last 10 % of the window |
| voltage_deflection | eFEL `voltage_deflection_vb_ssse` | scalar | mV | 0 | steady_state_voltage - baseline_voltage |
| sag_ratio | eFEL `sag_ratio1` | scalar | 1 | 0 (+ hyperpolarising only) | (ssv_stimend - min V) / (voltage_base - min V) |
| minimum_voltage | eFEL `minimum_voltage` | scalar | mV | 0 | minimum V in the window |
| maximum_voltage | eFEL `maximum_voltage` | scalar | mV | 0 | maximum V in the window |
| spike_count | eFEL `spike_count_stimint` | scalar (count) | 1 | 0 | peaks inside [start, end] |
| mean_frequency | eFEL `mean_frequency` | scalar | Hz | 2 | in-window spikes / (last spike - start) |
| first_spike_latency | eFEL `time_to_first_spike` | scalar | ms | 1 | first peak - start |
| ap_amplitude | eFEL `AP_amplitude` | first | mV | 1 | peak minus derivative-threshold onset, first spike |
| ap_half_width | eFEL `AP_duration_half_width` | first | ms | 1 | width at half amplitude, first spike |
| ahp_depth | eFEL `AHP_depth` | first | mV | 2 | minimum AHP voltage - voltage_base (negative for a dip) |
| first_isi | eFEL `all_ISI_values` | first | ms | 2 | first interspike interval |
| last_isi | eFEL `all_ISI_values` | last | ms | 2 | last interspike interval |
| adaptation_index | eFEL `adaptation_index2` | scalar | 1 | 4 | mean normalised ISI change (see note) |
| burst_count | eFEL `strict_burst_number` | scalar (count) | 1 | 4 | number of bursts (`strict_burst_factor` 2.0) |
| firing_regime | NeuroSem `features/regimes.py` | categorical | - | - | silent, single_spike, depolarization_block, bursting (>= 2 bursts), adapting (index > 0.1), tonic |
| rheobase | NeuroSem `protocols/rheobase.py` | scalar | nA | - | first spiking amplitude of the search |

**Synthetic check (eFEL 5.7.34, frozen settings, artificial traces; not a model
simulation).**

- **Spike train at the RS reference spike times.** Spikes were placed at the upstream RS
  reference times (320.554 ... 592.105 ms), with window [300, 700] ms. The results were:
  - `time_to_first_spike` = 20.55 ms and `mean_frequency` = 17.12 Hz, which equals
    5 / (592.105 - 300) s.
  - `all_ISI_values` = 27.97, 39.42, 68.75, 135.42 ms, quantised by `interp_step`.
  - `adaptation_index2` = 0.2988. This equals the mean of (ISI(i+1) - ISI(i)) /
    (ISI(i+1) + ISI(i)) over the last two ISI pairs, so the first pair is skipped.
  - `strict_burst_number` = 1, for a train that is adapting rather than bursting. So
    `burst_count` = 1 alone should not be read as bursting, and the firing-regime rule
    rightly requires >= 2 bursts.
- **One synthetic spike.** eFEL returned `AHP_depth` of about -9.8 mV and `mean_frequency`
  = 100 Hz (1 spike, 10 ms after start). The second value shows why `mean_frequency` needs
  `min_spikes` 2.
- **Excursions outside the window.** A dip and a bump placed outside the window did not
  affect `minimum_voltage` or `maximum_voltage`.

## 6. Cost measure

**Definition.** The cost of a protocol is the number of **cell-steps** it needs: simulated
cells x time steps. It depends only on protocol length, time step and batch size, not on
the machine. That makes it suitable for runtime-matched baselines and for "comparable
computational cost" (RQ2). Wall-clock runtime is recorded per run as well.

| Item | Cell-steps at h = 0.005 ms | Notes |
|---|---|---|
| P01, P02, P04, P07 | 200,000 each | 1000 ms |
| P05 | 500,000 | 2500 ms |
| P06 | 300,000 | 1500 ms |
| P08 | 220,000 | 1100 ms |
| P09, P10 | 100,000 each | 500 ms |
| **Batched battery P01-P10 without P03** | **2,020,000** | 5 simulations (lengths 500, 1000, 1100, 1500, 2500 ms) |
| P03 rheobase search | 1,920,000 per simulation; 1-7 simulations | up to 13,440,000 (1 if spontaneous, 2-7 if ok, 4 if not found) |
| P00 canonical, RS or LTS | 1,000,000 | shipped 1000 ms at 0.001 ms (level 1) |
| P00 canonical, HH example | 30,000 | 300 ms at 0.01 ms |
| P00 canonical, Wang-Buzsaki | 100,000 | 100 ms at 0.001 ms |

Each refinement level doubles the cost (h/2 is 2x, h/4 is 4x).

**Planning conversion.** `docs/pilot/dt_probe.md` measured roughly 15-35 microseconds per
cell-step plus about 1 s of JVM start-up per simulation on the development machine. The
batched battery at h is therefore roughly 30-70 s of CPU plus 5 JVM starts per variant
(arithmetic, not a benchmark).

**How cost enters selection (proposal, to be frozen).**

- A protocol's cost is its own cell-steps, as if run alone.
- `P03_rheobase` is charged the actual search cell-steps for each variant, or a
  preregistered typical value.
- The canonical protocol is charged its harness cell-steps.
- Savings from batching several protocols into one JVM are not credited, so cost stays
  additive.
- The reference's own rheobase search is paid once per model and is not charged per
  mutant.

## 7. Deferred protocols: P11 and P12

| protocol | Specification wording | Why deferred |
|---|---|---|
| P11_chirp | "Deterministic chirp, only if implementation is stable" | NeuroML v2.3.1 core inputs are `pulseGenerator`, `rampGenerator`, `sineGenerator` (fixed period), `compoundInput` and their DL variants, voltage clamps, and spike-driven inputs. **There is no chirp** (M0 evidence, `neuroml-lems`). A chirp needs a new custom LEMS `ComponentType`: new NeuroSem code whose stability, dt-alignment and exporter support (e.g. NEURON) are unverified. The specification allows deferral |
| P12_frozen_noise | "Frozen pseudo-random waveform, only as a later extension" | There is no core arbitrary-waveform or noise-current input. Two open NeuroML2 feature requests (#97, #99) ask for noisy current sources. The specification itself labels it a later extension |

Consequences:

- The candidate pool is the ten implemented protocols, P01-P10 including P03. It meets the
  lower bound of the specification's 10-16 range only if all ten are candidates.
- The templates stay in the catalogue with `implemented = false` and their reason, so the
  manifest shows they were considered and not silently dropped.
- Instantiating them raises `NotImplementedError`.

## 8. Open issues

1. `ahp_depth` in P09 is `not_applicable` by configuration (section 3, P09).
2. The reference-rheobase rule for `not_found` / `error` is not yet specified.
3. There is no Ih model, so `sag_ratio` (P07) is likely uninformative.
4. The spike threshold is -20 mV for all models. A per-model threshold is an open decision,
   since eFEL misses spikes peaking below -20 mV.
5. Whether `P00_canonical` itself is a selection candidate, and how P03 is charged, must be
   preregistered.
