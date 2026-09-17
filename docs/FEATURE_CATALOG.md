# Feature catalog

*Source of truth: `configs/features.yaml` (eFEL 5.7.34 variants and settings) and
`configs/tolerances.yaml`. Status: provisional until frozen for the confirmatory study.*

## Extraction rules

- **Settings.** Applied with `efel.reset()` and `efel.set_setting()` before every extraction:
  threshold −20 mV, derivative thresholds +10 / −12 mV/ms, `interp_step` 0.01 ms,
  `strict_stiminterval` true. Unknown setting names are rejected.
- **Traces.** Features are extracted from the stored trace representation (float32 mV on a verified
  uniform grid), so every number reproduces from raw files.
- **Undefined values.** An undefined feature stays undefined and is never replaced by zero. If fewer
  than `min_spikes` spikes occur in the analysis window, the feature is recorded as "not applicable".
- **Detection rule.** A feature detects a difference when |variant − reference| > τ, with
  τ = max(abs floor, rel·|f_ref|, 3·|f(h) − f(h/2)|). A change in definedness also counts.
  - A detection counts only if it reproduces at h and h/2.
  - Reference entries whose state changes under refinement are excluded.

## Features

| Feature | eFEL variant (aggregation) | Unit | Minimum spikes | Meaning | Tolerance floor / relative | PILOT_PROTOCOL_V1 role |
|---|---|---|---|---|---|---|
| `spike_count` | `spike_count_stimint` | 1 | 0 | spikes in the analysis window | 0.5 / 0 | primary |
| `first_spike_latency` | `time_to_first_spike` | ms | 1 | stimulus onset to first spike | 0.5 ms / 2% | primary |
| `last_isi` | `all_ISI_values` (last) | ms | 2 | final interspike interval | 0.5 ms / 2% | primary |
| `adaptation_index` | `adaptation_index2` | 1 | 4 | spike-frequency adaptation | 0.01 / 10% | primary |
| `ap_amplitude` | `AP_amplitude` (first) | mV | 1 | height of the first spike | 1 mV / 2% | primary |
| `ahp_depth` | `AHP_depth` (first) | mV | 1 | depth of the after-hyperpolarisation | 0.5 mV / 5% | primary |
| `steady_state_voltage` | `steady_state_voltage_stimend` | mV | 0 | voltage at the end of the stimulus | 0.5 mV / 0 | primary |
| `rheobase` | Neuraxis bracketing search | nA | – | smallest 500 ms step that evokes a spike | 2× search resolution / 2% | primary |
| `mean_frequency` | `mean_frequency` | Hz | 2 | mean firing rate | 0.5 Hz / 5% | secondary |
| `ap_half_width` | `AP_duration_half_width` (first) | ms | 1 | spike width at half height | 0.05 ms / 5% | secondary |
| `first_isi` | `all_ISI_values` (first) | ms | 2 | first interspike interval | 0.5 ms / 2% | secondary |
| `burst_count` | `strict_burst_number` | 1 | 4 | number of bursts | 0.5 / 0 | secondary |
| `firing_regime` | Neuraxis rule on eFEL outputs | label | – | silent, single spike, depolarisation block, bursting, adapting or tonic | exact match | secondary |
| `baseline_voltage` | `voltage_base` | mV | 0 | resting voltage before the stimulus | 0.5 mV / 0 | secondary |
| `voltage_deflection` | `voltage_deflection_vb_ssse` | mV | 0 | steady-state change from baseline | 0.5 mV / 5% | secondary |
| `sag_ratio` | `sag_ratio1` (hyperpolarising only) | 1 | 0 | Ih sag during a hyperpolarising step | 0.02 / 5% | secondary |
| `minimum_voltage` | `minimum_voltage` | mV | 0 | lowest voltage in the window | 0.5 mV / 0 | secondary |
| `maximum_voltage` | `maximum_voltage` | mV | 0 | highest voltage in the window | 1 mV / 0 | secondary |

**Roles.**
- **Primary** features decide every classification in PILOT_PROTOCOL_V1.
- **Secondary** features are extracted and reported but never change a primary result (D-029).
- The confirmatory panel is proposed only after the development pilots and frozen before held-out
  evaluation.
- Per-protocol assignment is in `configs/pilot_protocol_v1/study.yaml` and `docs/PROTOCOL_CATALOG.md`.

## Firing-regime rule

Evaluated in order:
1. **Silent:** no spikes.
2. **Single spike:** one spike.
3. **Depolarisation block:** the last spike falls before half the window and the voltage then stays
   above −40 mV.
4. **Bursting:** at least 2 bursts.
5. **Adapting:** adaptation index above 0.1.
6. **Tonic:** otherwise.
