# Kinetics operator validation (D-037, D-049)

*The gate Neel set before any kinetics mutation enters a study. Evidence:
- `results/audits/kinetics_validation/kinetics_validation.json`, with before/after plots in `plots/`;
- `scripts/kinetics_validation.py` (run 2026-09-17; all 24 sites passed);
- tests `tests/unit/test_kinetics_operators.py` and `tests/integration/test_kinetics_validation.py`.

These are operator-correctness data on development fixtures, not study data.*

## In plain English

- **What the operators change.** Each kinetics operator changes how one ion-channel gate responds to
  voltage: where it switches on (midpoint), how steeply (slope), only its opening rate, or the whole
  channel's voltage shift.
- **What was checked.** Every generated change was checked to touch only what it claims. The shipped
  simulation file stayed identical, no solver or time-step setting changed, the file stayed valid,
  and the model still ran.
- **Before and after.** Every case has a before/after voltage plot a person can inspect.
- **Main limit.** Most published models in our pool write their channels as custom equations, which
  these operators cannot edit. The operators apply mainly to models that use NeuroML's standard gate
  equations.

## 1. Fixtures

| Fixture | Why | Sites exercised |
|---|---|---|
| `tests/fixtures/kinetics_fixture/` (written for testing; Apache-2.0; never a study model) | standard HH-type gates: rate gates `m`, `h` and a time-course gate `n` with a core steady state | midpoint, slope, forward-rate operators |
| `pospischil2008_rs` (Pilot 1 development model) | the only model here with a `channelDensityVShift` | `shift_channel_vshift` |

## 2. Operators, affected equations and elements

| Operator | Elements edited | Equations affected (NeuroML core types) | Atomic or compound |
|---|---|---|---|
| `shift_gate_midpoint`, rate gates | `forwardRate@midpoint` and `reverseRate@midpoint` of one gate (plus a core `steadyState@midpoint` if present) | HHExpRate r = rate·exp((V−midpoint)/scale); HHSigmoidRate r = rate/(1+exp((midpoint−V)/scale)); HHExpLinearRate r = rate·x/(1−exp(−x)), x = (V−midpoint)/scale | **compound**: 2 (or 3) attributes of one gate, one documented change (a rigid shift of the gate's voltage dependence) |
| `shift_gate_midpoint`, time-course gates | `steadyState@midpoint` of one gate | HHSigmoidVariable x∞ = rate/(1+exp((midpoint−V)/scale)) (and the Exp and ExpLinear variants) | **atomic** |
| `scale_gate_slope`, rate gates | `forwardRate@scale` and `reverseRate@scale` of one gate | as above; the steepness factor `scale` is multiplied by k, keeping its sign and unit | **compound** |
| `scale_gate_slope`, time-course gates | `steadyState@scale` | as above | **atomic** |
| `shift_forward_rate_midpoint` | `forwardRate@midpoint` of a pure rate gate (no steady-state element) | forward (opening) rate only; this changes both x∞ = α/(α+β) and τ = 1/(α+β) | **atomic** |
| `shift_channel_vshift` | `channelDensityVShift@vShift` | passed to the channel. Per the NeuroML core definition, how vShift is used "is determined by the individual gates". It affects only gates whose own definitions read `vShift` (for example the Pospischil custom rate types); core HH rate types do not read it | **atomic** |

## 3. What was confirmed for every site (24 of 24 passed)

1. **Single documented change.** `enforce_single_operator` confirmed that only the recorded
   attributes of the target element changed: no other file, element or attribute.
2. **Nothing else touched.**
   - No execution override (solver, step and recording unchanged).
   - The shipped simulation file was byte-identical to the reference.
   - The operator's `check_record` confirmed the exact magnitude (shift in mV, or scale factor).
3. **Valid and runnable.** The mutant was schema-valid under the relative oracle and simulated
   successfully (status ok).
4. **Inspectable output.** A before/after voltage plot and the spike counts before and after were
   recorded.

| Operator (fixture) | Sites | Spike count before → after (range) | Status |
|---|---|---|---|
| `shift_gate_midpoint` | 12 (m, h rate gates; n steady state; ±5, ±10 mV) | 38 → 0 to 50 | all ok |
| `scale_gate_slope` | 6 (×0.8, ×1.25) | 38 → 33 to 42 | all ok |
| `shift_forward_rate_midpoint` | 4 (m, h; ±5 mV) | 38 → 30 to 42 | all ok |
| `shift_channel_vshift` (RS) | 2 (±5 mV on `Na_all`) | 5 → 13 (−5 mV), 0 (+5 mV) | all ok |

## 4. Applicability

- **No sites on Pospischil.** The Pospischil cells' gates are custom LEMS types (for example
  `Kd_n_alpha_rate`), so the midpoint, slope and forward-rate operators report them as inapplicable,
  with reasons.
- **Core-gate models.** Most sweep-2 candidates also use custom component types. Kinetics sites
  therefore exist mainly in models built on core HH gates, and `shift_channel_vshift` only where a
  channel reads `vShift`. Pilot 2 records the applicable sites per model.

## 5. Pilot 2 use (PILOT_PROTOCOL_V2)

- **Included subset:** `shift_gate_midpoint` (mild ±5 mV, strong ±10 mV) and `shift_channel_vshift`
  (±5 mV, mild).
- **Held back:** `scale_gate_slope` and `shift_forward_rate_midpoint` are validated but excluded from
  Pilot 2, to keep the kinetics family limited and prespecified.
- **Status:** the family stays "excluded from protocol selection".
