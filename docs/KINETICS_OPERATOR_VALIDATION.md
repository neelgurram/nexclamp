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

## 5. Pilot 2 use (PILOT2_PROTOCOL)

*Revised 2026-09-17, before any Pilot 2 data existed (D-054).* All four validated operators enter
Pilot 2. The earlier plan held `scale_gate_slope` and `shift_forward_rate_midpoint` back; that would
have removed the only **atomic** operator, and with it the atomic-versus-compound report Neel
requires. The family is still a limited, prespecified subset: 4 of 23 operators and 12 of the 88
primary semantic mutants, and it remains "excluded from protocol selection".

- **Included:** `shift_gate_midpoint` (mild ±5 mV, strong ±10 mV), `scale_gate_slope` (×0.8, ×1.25),
  `shift_forward_rate_midpoint` (±5 mV), `shift_channel_vshift` (±5 mV). Only `shift_gate_midpoint`
  has strong-severity sites; the magnitude sets of the other three are mild by construction, which is
  recorded rather than adjusted after the fact.
- **Atomicity, as recorded:** atomic = one attribute of one element (`shift_forward_rate_midpoint`,
  `shift_channel_vshift`); compound = several attributes forming one documented change of one gate
  (`shift_gate_midpoint`, `scale_gate_slope`). `shift_channel_vshift` is atomic as an edit but
  channel-wide in effect; scope is reported beside atomicity.

### Per-model applicability on the Pilot 2 models

*Run 2026-09-17, `scripts/kinetics_validation.py --only-models --models … --max-sites 6`; evidence in
`results/audits/kinetics_pilot2/` (48 sites, plots per site). Eligible sites first, validated sites in
brackets. **All 48 sites passed.***

| model | shift_gate_midpoint | scale_gate_slope | shift_forward_rate_midpoint | shift_channel_vshift | max abs dV from reference |
|---|---|---|---|---|---|
| `acnet2_pyr_soma` | 16 (6) | 8 (6) | 8 (6) | no `channelDensityVShift` | 118 mV |
| `migliore2014_mt_soma` | 8 (6) | 4 (4) | gate has a steady-state element; a forward-only shift would be overridden | no `channelDensityVShift` | 109 mV |
| `nml2_hh_example` | 12 (6) | 6 (6) | 6 (6) | no `channelDensityVShift` | 112 mV |
| `osb_hh2_477127614` | `gateHHtauInf` has no core midpoint | no core `scale` | not a rate gate | 2 (2) | 99 mV |
| `pospischil2008_fs` | Kd rates are custom LEMS types | same | same | no `channelDensityVShift` | not applicable |

**Inapplicability is not a model failure.** It is a property of how the model encodes its channels:
a custom LEMS rate type simply has no core midpoint or slope parameter to change. The reason is
recorded per gate, and `pospischil2008_fs` stays a full Pilot 2 model through the other five
analysis families.

- **Status:** the family stays "excluded from protocol selection".
