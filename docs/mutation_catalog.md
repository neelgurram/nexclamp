# Mutation and transformation catalogue

*Status: draft, 2026-09-13. Binding operator names and targets are in
`docs/ARCHITECTURE.md` sections 3.4 and 3.5. This catalogue explains what each operator
changes, which validation layer **should** detect it, and known caveats. Pilot-site
statements come from reading the pinned model files. Statements about detection outcomes
are **expectations** derived from the contract, the configuration and the code, and none
of them is a measured result. The held-out mutation family is not named here; choosing it
is Neel's decision.*

## 1. Validation layers used in this catalogue

A variant passes through the layers in order and stops at the first failure.

| Layer | What it checks | Failure leads to |
|---|---|---|
| L1 structural | `jnml -validate` on every NeuroML file the model reads (cell include closure + harness NeuroML files); a variant fails if it adds any error its reference did not have (DECISIONS D-006) | class 1, structurally invalid |
| L2 execution | jLEMS builds and runs to completion and writes readable output | class 2, non-executable (build error, runtime error, timeout) |
| L2b stability | run not aborted by divergence (jLEMS time-step hint); output finite and within +-10 V | class 3, numerically unstable |
| L3 canonical | `P00_canonical` features versus reference, within tolerance, detection reproduced at h and h/2 (same rule as L4, DECISIONS D-021) | if L4 detects reproducibly and L3 does not: class 6 (silent) |
| L4 perturbation battery | P01-P10 (including P03 rheobase) versus reference, within tolerance | detection reproduced at h **and** h/2 makes the mutant non-equivalent (class 5 or 6) |
| none | nothing detected reproducibly | class 4, equivalent within the tested domain |

`TOOL_FAILURE` (for example Java missing) is never a property of the model. It must be
re-run, never classified.

## 2. General rules

- **Single fault.** Each mutant comes from exactly one operator applied at one site.
  `enforce_single_operator` rejects a variant if any changed element is not covered by its
  recorded `Edit`s, or if the edits span more than one target element (execution-override
  mutants excepted). Compound faults are for a secondary stress test only.
- **Workspaces.** Operators edit a materialised workspace copy, never `models/raw/`.
- **Sites.** `sites(ws)` lists every place an operator can act, in deterministic order.
  `generate_mutants(..., n_per_operator, seed)` samples from them reproducibly. An operator
  with no site for a model is **inapplicable**. Record it as inapplicable, not as an
  equivalent mutant.
- **Stimulus is fixed per model.** The battery's concrete protocols are instantiated once
  from the *reference* model's rheobase, and every variant receives exactly the same probe
  stimulus.
- **The canonical window comes from the reference harness**
  (`validation/canonical.py`). A variant whose harness stimulus was mutated is judged
  against the original test window.

## 3. Mutation operators (ARCHITECTURE 3.4)

### 3.1 Stimulus family

These operators edit **only the shipped harness** (the LEMS simulation or its network
file). NeuroSem's probe files are generated from the cell file and the reference-instantiated
protocols, so the battery's inputs are unchanged. The content-addressed run ID then reuses
the reference battery results. **This is by design.** It models the realistic error of
breaking a model's own test while the model itself is intact.

| Operator | What it changes | Pilot sites | Layer expected to detect | Caveats |
|---|---|---|---|---|
| `stim_amplitude` | harness `pulseGenerator/@amplitude` x factor | RS `Input_1` 7.5E-10 A; LTS `Input_1` 1.5E-10 A | L3 (spike count, frequency, latency) | Small factors may stay within tolerance and be class 4 |
| `stim_onset` | harness input `@delay` shifted by a number of ms | RS 0.3 s; LTS 400 ms | L3: a later onset raises first-spike latency relative to the reference window; an earlier onset moves stimulus into the baseline window | Keep shifts on whole ms so they fall on every refinement grid |
| `stim_duration` | harness input `@duration` x factor | RS 0.4 s; LTS 400 ms | L3 for shortening (spike count, last ISI) | **Lengthening is expected to be (near-)equivalent.** The simulation is deterministic and causal, so the trace is identical up to the original window end |
| `sim_length` | harness `Simulation/@length` x factor | RS 1000.0 ms; LTS 1000.0 ms | L3 via definedness mismatch when the run no longer covers the window | **Lengthening is expected to be equivalent.** The specification's metamorphic relation says extending a deterministic simulation preserves the overlapping interval |
| `record_wrong_variable` | the v column's `OutputColumn/@quantity` switched to another existing state path | RS/LTS harness `Display` lines name gate variables such as `.../Na_all/Na/m/q` | L3 | Earlier drafts expected class 3 because gate values exceed the old 250 mV bound; with the 10 V bound (D-021) the recorded non-voltage trace is compared behaviourally, so L3 is expected to detect it |

**Structural consequence: a stimulus mutant can never be class 6.** Only `P00_canonical`
can differ from the reference, so any reproducible detection is a canonical detection
(class 5). Including this family in the primary denominator would favour canonical
testing. How it is reported is a preregistration decision (`docs/statistical_plan.md`).

### 3.2 Biophysical family

These edit the model description, so they affect canonical and battery runs alike.

| Operator | What it changes | Pilot sites | Layer expected to detect | Caveats |
|---|---|---|---|---|
| `scale_conductance` | `channelDensity*/@condDensity` x factor (e.g. 0.5, 0.8, 1.25, 2) | RS: 4 densities (Leak, Kd, IM, Na); LTS: 5 (Leak, Na, Kd, IM, IT) | L3 or L4 | Some changes are expected to be class 4 or silent. IM x 0.8 in RS acts slowly, and a 400 ms canonical step may miss it while the 2 s `P05_long_step` catches it (**expectation**). Density strings must keep valid unit syntax |
| `shift_reversal` | `channelDensity*/@erev` by +-5 or +-10 mV | RS: 4 (including `channelDensityVShift` Na); LTS: 4 | L3 or L4; leak shifts move `baseline_voltage` | `channelDensityNernst` (LTS IT) has **no** `erev`: its reversal comes from the Ca pool, so there is no site |
| `scale_capacitance` | `specificCapacitance/@value` x factor | RS, LTS: 1 each (1.0 uF_per_cm2) | L3 or L4 (latency, frequency, AP shape) | |
| `scale_gate_time_constant` | both forward and reverse `rate` of one core HH gate x k (tau / k), or a `timeCourse` | Depends on how custom rate types are treated (see caveat) | L4 or L3 | Pospischil channels use custom rate ComponentTypes with no scalable parameter; the registered operator therefore uses the exact q10Fixed mechanism (insert or scale `q10Fixed` on a core gate; tau / k, steady state unchanged; DECISIONS D-021). `q10ExpTemp` gates (LTS IT `u`) stay inapplicable |
| `shift_initial_voltage` | `initMembPotential/@value` by +-5 mV | RS -70 mV; LTS -84 mV | usually none (class 4) | **Expected to be equivalent in the battery.** Every probe settles for 300 ms before any stimulus, which for RS is about 30 leak time constants (arithmetic, leak only: C/g = 10 ms). LTS may retain slower state (T-current inactivation, Ca pool), so equivalence there is less certain |
| `wrong_segment_group` | `channelDensity*/@segmentGroup` changed to another existing group | RS, LTS: groups `Soma`, `all`, `soma_group` | none (class 4) | **Expected exact no-op for single-compartment models.** All three groups contain the single segment 0. In RS and LTS the attribute is absent and defaults to `all` (NeuroML v2.3.1 XSD). Whether the operator inserts the attribute is an implementation choice that must be recorded in the `Edit`. The family only becomes meaningful for multicompartment models |

### 3.3 Reference family

| Operator | What it changes | Pilot sites | Layer expected to detect | Caveats |
|---|---|---|---|---|
| `wrong_channel` | `channelDensity*/@ionChannel` set to another channel id defined in the includes | RS: 4 densities x 3 alternatives; LTS: 5 x 4 | L2 (build error if the channel's species or type does not fit the density), otherwise L3 or L4 | Swapping Kd_all (5.0 mS/cm2) to IM gives an enormous M-current; strong silencing is **expected** |
| `omit_include` | remove one `<include>` from the cell file | RS: 4; LTS: 6 | L2 in the battery (the probe includes only the cell file, so a missing channel definition cannot resolve) | **The shipped harness may mask it.** `LEMS_RS.xml` and `LEMS_LTS.xml` include every channel file directly (and `RS.net.nml` repeats them), so the canonical run may still build while the probe fails. Whether this is class 2 or a behavioural detection is a scientific judgement for Neel. Whether `jnml -validate` on the cell file alone flags the unresolved reference is unverified. In FS, omitting the unused IM include is expected to be a no-op |
| `duplicate_conductance` | duplicate one `channelDensity*` element with a new unique id | RS: 4; LTS: 5 | L3 or L4 (behaves like doubling that density) | Structurally valid by construction (unique id); expected non-equivalent for most channels |
| `wrong_compatible_component` | `@ionChannel` swapped to another channel of the **same ion species** | RS: `k` Kd <-> IM; LTS: `k` Kd <-> IM | L3 or L4 | Few sites. LTS has only one Ca channel (IT) and one Na channel, so there is no same-species alternative for those. A "dimensionally compatible" error passes schema checks by design; LEMS-level semantic errors appear only at build or run time |

### 3.4 Numerical family

| Operator | What it changes | Pilot sites | Layer expected to detect | Caveats |
|---|---|---|---|---|
| `increase_dt` | harness `Simulation/@step` x factor **and** `exec_overrides.dt_factor` (probe dt x factor) | 1 per model | L4 or L3 for large factors; L2b if Euler becomes unstable | Default factors x4, x10, x20 (x2 removed: never admissible, section 5.2) |
| `solver_config` | harness `<Meta method>` **and** `exec_overrides.integrator_method` | 1 per model per method | none (class 4) | **Expected no-op for core types.** The M1 development probe showed first-order convergence, consistent with forward Euler. The M0 source reading found RK4 applies only to state flagged `simultaneous`, which no core type sets. The M0 evidence also notes `eulertree` switches to an unconsolidated state tree and **may not** be a no-op (evaluation order). Confirm empirically. A no-op solver mutant is class 4, not a missed error |
| `reduce_spatial_discretization` | multicompartment segment discretisation | **none** for all current models | not applicable | Returns no sites for single-compartment models and is recorded as inapplicable. It becomes usable only with multicompartment models, which jLEMS does not simulate (a NEURON path would be needed) |
| `recording_resolution` | `exec_overrides.sample_every_ms` (post-hoc output sampling; **no file edit**) | 1 per model per value | L4 and L3 on AP amplitude, half-width, AHP and latency | **A configuration mutation, not a model defect.** Dynamics are unchanged. Only the stored trace is thinned (`load_dat` stride) before eFEL resamples it to `interp_step` = 0.01 ms, and linear interpolation cannot recover a spike peak lost between samples. Because the run ID includes the execution config, these runs are not cached. Coarse sampling can also change `spike_count` if narrow peaks fall between samples |

## 4. Valid transformations and no-change controls (ARCHITECTURE 3.5)

All share the operator protocol, with `kind = valid_transform` or `no_change_control`.
**The layer expected to detect them is "none".** Any detection is a false positive and
counts toward the false-positive endpoint. Every transform must pass `jnml -validate` in its
unit tests.

| Registry name | Kind | What it changes | Pilot examples | Caveats |
|---|---|---|---|---|
| `unit_conversion` | valid transform | a quantity rewritten in another unit of the same dimension, with Decimal-exact value arithmetic | RS IM `0.07 mS_per_cm2` -> `0.7 S_per_m2`; LTS Leak `1e-5 S_per_cm2` -> `0.01 mS_per_cm2` | Only unit strings permitted by the NeuroML v2.3.1 XSD for that dimension are allowed (current: A, uA, nA, pA). jLEMS converts values to SI doubles, so the last bit can differ between representations. Over 10^5-10^6 Euler steps, fragile features (e.g. late LTS spikes) could move. Tolerances should absorb this, but a detection would be real and must be reported |
| `xml_formatting` | no-change control | whitespace and indentation only | any file | `IT.channel.nml`, `Ca.nml` and `IL.channel.nml` declare `ISO-8859-1` but contain only ASCII. A formatter must keep the declaration (or change it deliberately) and must not re-encode |
| `add_comments` | no-change control | insert XML comments | any file | Comments inside LEMS `ComponentType` bodies must remain well-formed |
| `numeric_literal_format` | valid transform | numerically equal literal, e.g. `50.0` -> `50` or `5e1` | RS `condDensity="50.0 mS_per_cm2"` | The XSD number pattern forbids `e+`; `units.format_number` never emits it |
| `rename_identifier` | valid transform | rename an id and update **all** references in all files | channel `IM` -> `IM_renamed`; cell `RS` -> `RS_renamed` | Must update harness LEMS paths (`CG_RS/0/RS/v` in `OutputColumn` and `Display` lines), network `population/@component`, LEMS `Include`s where relevant, and `model_overrides["cell_id"]` so generated probes target the renamed cell. Custom `ComponentType` names in LTS are referenced from gate `type` attributes |
| `factor_file` | valid transform | move one component to a new included file, with references preserved | move `LeakConductance` out of `Leak.channel.nml` | Every file that needs the component (cell file, harness LEMS, network) must still resolve it. The probe includes only the cell file |
| `reorder_independent` | valid transform | reorder semantically independent sibling elements | order of `channelDensity` elements | Summation order of channel currents may change floating-point rounding (same caveat as `unit_conversion`) |
| `explicit_default` | valid transform | write an inherited default explicitly with the same value | `channelDensity/@segmentGroup="all"` (the default is verified in the v2.3.1 XSD) | Each default must be verified from the XSD or core-type definition before use, never from memory |

**Verification before inclusion.** The specification requires each valid transformation to
be verified with structural inspection and the exhaustive high-resolution battery before
inclusion. If transformations that the battery flags are then *removed*, the false-positive
rate becomes zero by construction. The plan (`docs/statistical_plan.md`) therefore keeps
the two roles apart. Semantic equivalence is established by inspection and by the
transform's own tests, independently of the battery. Battery results on transforms are
reported, not used as a filter.

## 5. Cross-cutting caveats

### 5.1 Equivalent mutants are expected, and they are not misses

Several operators are expected to produce class 4 mutants in single-compartment models:
`wrong_segment_group`, `solver_config` (rk4), lengthening `sim_length` or `stim_duration`,
`shift_initial_voltage`, and `omit_include` of an unused file. These are excluded from the
detection-rate denominator. Counting them as missed errors would penalise every strategy
for changes that do not change behaviour in the tested domain. They are reported per
operator so readers can see where the mutation budget went.

### 5.2 `increase_dt` with factor 2 is never admissible (follows from the definitions)

This derivation uses the current tolerance and classification rules, not data.

1. Admissibility needs a detection at h **and** at h/2 (`classify`).
2. A mutant with `dt_factor = 2`, run at level h/2, actually runs at h. Its probe inputs are
   identical to the reference run at h, so it reuses that result, and its features equal
   the reference's features at h. The same holds for the canonical run, because refinement
   halves the doubled harness step back to the shipped step.
3. At level h/2 the comparison is therefore |f_ref(h) - f_ref(h/2)|.
4. The tolerance for the same (model, protocol, feature) is at least
   c x |f_ref(h) - f_ref(h/2)| with c = 3. A difference can never exceed a tolerance that is
   at least three times itself. Categorical and definedness changes under refinement are
   already excluded.
5. So a factor-2 mutant cannot be detected at h/2 and is never class 5 or 6.

Factors of 4 or more escape this (at h/2 the mutant runs at 2h, which calibration never
saw). Neel should choose factors knowing this.

**Resolved (2026-09-13, DECISIONS D-021):** x2 was removed from the default `increase_dt` grid, which is now x4, x10, x20.

### 5.3 Crashes are reported, not counted

Classes 1-3 are reported in the validation cascade (figure 2) and are never in the
detection-rate denominator. Operators expected to crash often (`omit_include` in the
battery, some `wrong_channel` swaps) inflate class 2 counts and say little about protocol
selection.

### 5.4 Pilot families

`configs/study.yaml` currently lists the pilot families `biophysical`, `reference` and
`numerical`, with `mutants_per_operator: 2` (sites sampled per operator per model) and
`transforms_per_operator: 1` (provisional). These are per-operator counts:
`experiments/pilot.py` passes them through `campaign.generate_stage` to
`mutations.generate_mutants` and `transforms.generate_transforms` for each model. The
per-model totals therefore depend on how many operators apply to each model. The specification's pilot targets are
5-10 mutants per model and 4-6 valid transformations (specification targets, not
configuration values). The stimulus family is absent from the pilot list, consistent with
section 3.1.
