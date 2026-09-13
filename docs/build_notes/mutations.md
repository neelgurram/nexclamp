# Build note: `neurosem.mutations`

Author: mutations sub-agent, 2026-09-13. Scope: ARCHITECTURE.md section 3.4. Nothing here is
a study result; observations are from short smoke runs on this machine (jNeuroML 0.14.0 /
jLEMS 0.12.0, Temurin 21).

## 1. Requested contract / core changes

### 1.1 `VariantRecord` has no generator seed field
`data/mutation_manifest.csv` has a `generator_seed` column but `schemas.VariantRecord` has
no seed field. **Workaround:** `generate_mutants` stores the seed as
`params["generator_seed"]`; `write_manifest` moves it into the `generator_seed` column and
leaves it out of `params_json`. **Request:** add `generator_seed: int | None = None` to
`VariantRecord` (then drop the params key).

### 1.2 `scale_gate_time_constant` yields no sites for any Pospischil model (open coverage gap)
The contract limits the operator to core HH gate `rate`/`timeCourse` parameters. Every
Pospischil channel (Na, Kd, IM, IT) uses core gate types (`gateHHrates`, `gateHHtauInf`)
but custom LEMS rate/time-course ComponentTypes that have **no parameter** to scale. So
under the contract the operator has 0 sites for all four Pospischil models (RS, LTS, FS,
IB), including both pilot models. The spec's biophysical item "scale a channel time
constant" is therefore never exercised in the pilot. Site counts with the registered
operator / with the q10 fallback: RS 0/16, LTS 0/16, FS 0/12, IB 0/24,
`nml2_hh_example` 12/12, `wangbuzsaki1996_wb` 8/8
(`work/tmp/mutations/site_counts.py`, 2026-09-13).

**Implemented, off by default:** `ScaleGateTimeConstant(allow_q10_fallback=True)` adds
`<q10Settings type="q10Fixed" fixedQ10="k"/>` to a core gate that has none, or scales an
existing `q10Fixed`. Why this is exact: in the bundled NeuroML2CoreTypes/Channels.xml,
every core HH gate computes `rateScale` as the product over `q10Settings[*]/q10` and uses
`tau = .../rateScale`. For rate gates, `inf = alpha/(alpha+beta)` does not depend on
`rateScale`, so the steady state is unchanged. The insert is placed after `notes`, which
is the XSD sequence order. Gates with `q10ExpTemp` (LTS IT `u`) stay inapplicable because
that q10 is not linear in any one parameter. Observed under jLEMS (RS harness, 400 ms,
dt 0.025 ms): inserting q10Fixed on IM `p` (x0.5) or Na `h` (x2) changed the voltage trace
(max |dv| about 116 mV). So jLEMS applies the inserted element.
**Request (integrator / contract owner):** decide, and record the decision in
ARCHITECTURE.md section 3.4, either (a) approve the q10Fixed mechanism and register
`ScaleGateTimeConstant(allow_q10_fallback=True)`, or (b) choose pilot models with core rate
gates (e.g. `wangbuzsaki1996_wb`). Enforcement already accepts q10 records structurally
(`check_record` verifies a single q10Fixed insert or fixedQ10 scaling by k), so (a) needs
only the registration change.

### 1.3 API additions and single-fault rules (backward compatible except as noted)
- `enforce_single_operator(ref, var, record, *, ignore_patterns=())`. It is strict by
  default: any added or removed file fails, including simulator outputs and probe files
  written into a variant workspace. `ignore_patterns` (fnmatch on relative paths) exempts
  only files **absent from the reference**; every reference file is still hash-compared
  (a pre-existing snapshot `.dat` may not change), and `tree_sha256`/`parent_tree_sha256`
  are compared over the reference file set, so ignored outputs never break the hash check.
  Either run enforcement before simulating, or pass e.g.
  `ignore_patterns=["*.dat", "*/LEMS_ns_*", "*/ns_*"]`.
- **Mutant records may not carry `model_overrides`** (no operator produces them), and their
  `exec_overrides` keys must equal the operator's declared `exec_override_keys` exactly:
  `increase_dt` = {dt_factor}, `solver_config` = {integrator_method},
  `recording_resolution` = {sample_every_ms}, empty for every other operator. Before this
  fix a conductance mutant plus `dt_factor`, or an override-only record, passed enforcement.
- **`OperatorBase.check_record(record, ref)` is abstract** (signature changed from
  `check_record(record)`): each operator verifies that the edits are *its* kind of fault,
  i.e. the element, attribute and file; the magnitude against `params` (Decimal-exact
  `factor`/`shift`); and relations such as the species partition for channel swaps, a
  top-level `<include>` for `omit_include`, an exact copy except id for
  `duplicate_conductance`, a state path already referenced by the harness for
  `record_wrong_variable`, and the same k on both rates for `scale_gate_time_constant`.
  When `params.changes` is present it must equal the recorded edits. Tamper tests cover
  each family.
- `load_variant(path, models=None)`: `models` defaults to `load_models()`. It refuses a
  mutant record with `model_overrides` and any override key that is not a `ModelRecord`
  field (previously unknown keys were silently dropped); otherwise overrides are applied.
- `generate_mutants` generates repeated operator names once (order preserved) and raises
  on a duplicate variant id, so a manifest can never double-count a mutant.
- `OperatorBase` adds `inapplicable(ws)`, `describe(site)`, `check_record(record, ref)`,
  `container_children` and `exec_override_keys`. There is also
  `inapplicable_sites(ws, operators)`.
- "All edits lie inside ONE target element": each record must address a single element.
  The one exception is an operator that declares `container_children`, and only
  `scale_gate_time_constant` does, for `forwardRate` + `reverseRate` of one gate. Its edits
  may address distinct declared direct children of one common parent, one per child role.
  Two edits in two channel densities are rejected (there is a tamper test for this).

### 1.4 Integration hazards noticed in other modules (not edited)
- **Path mismatch (campaign owner must fix; confirmed by review).**
  `experiments/campaign.py:191` calls
  `generate_mutants(model, ops, n, seed, ctx.variants_root / mid / "mutants")`. Per the
  contract, `generate_mutants` writes `root/<model_id>/<variant_id>/`, so variants land in
  `variants_root/<mid>/mutants/<mid>/<variant_id>/`, while `campaign.py:202` reads
  `variants_root/<model_id>/mutants/<variant_id>`. The campaign will not find generated
  mutants. Fix in campaign: either keep `root` and add `model_id` to `variant_dir`, or
  pass a root such that `root/<model_id>/<variant_id>` equals what `variant_dir` returns.
  Add an integration check that `load_variant(variant_dir(ctx, rec))` succeeds for every
  generated record. The mutations module keeps the contract layout.
- `docs/build_notes/core.md` notes that probe generation writes `ns_*`/`LEMS_ns_*` files
  into a workspace. Enforcement is strict about added files, so run it before probing or
  pass `ignore_patterns` (see 1.3).
- `quantity_si` raises `MutationError` (not `KeyError`) for units missing from
  `neurosem.units` (core.md item 5: e.g. `M`). Operators only read Nml2Quantity-typed
  attributes, whose units in the current models are all supported.

## 2. Interpretation choices (please confirm)
- **`wrong_channel` vs `wrong_compatible_component`.** Alternatives are split by ion
  species: `wrong_channel` swaps to a channel of a different species (or non-specific),
  and `wrong_compatible_component` to one of the same species. With the table's literal
  wording ("another channel id"), the same mutant could be generated under both names,
  which would double-count it per family. Only channels reachable through the cell file's
  includes are candidates.
- **`scale_gate_time_constant` scope.** Only channels referenced by the cell's channel
  densities are considered. Mutating an unused channel is equivalent by construction.
- **Stimulus targets.** These are generators in the files included directly by the harness
  LEMS file. For `nml2_hh_example` that is the cell file itself. So HH stimulus mutants
  change bytes of the cell file that probe batteries include; probe `inputs_sha256`
  changes, and the reference-battery cache will not be reused, although the probe network
  never references `pulseGen1`.
- **`record_wrong_variable`.** Substitutes are only state paths the shipped harness itself
  references (Display `Line` and other `OutputColumn` quantities). For RS these are gating
  variables (dimensionless). After `load_dat`'s x1000 they exceed
  `PHYSICAL_V_BOUND_MV`, so these runs will be classified `UNSTABLE`, not `OK`.
- **`reduce_spatial_discretization`.** Coarsens `numberInternalDivisions` properties on
  segment groups of multicompartment cells. jLEMS uses one compartment per segment and is
  expected to ignore the property (unverified); it matters for NEURON export. All current
  manifest models are single-compartment, so there are no sites (reported as inapplicable).
- **`solver_config`.** Methods are `rk4` and `eulertree`. If a jlems `Meta` already exists,
  its `method` is set instead of inserting a second one.
- **`wrong_segment_group` on single-compartment cells.** Every group holds the same
  segment, so these mutants are expected to be equivalent (negative controls).

## 3. Default parameter grids (why)
Factors are log-symmetric pairs (0.9/1.1, 0.8/1.25, 0.5/2). "Too small" and "too large"
faults of the same size are both present, from a plausible 10 % slip to a gross factor-2
error. A detection rate is only informative if hard-to-detect small faults are included.

| operator | grid |
|---|---|
| stim_amplitude | x -1, 0.5, 0.9, 1.1, 2 |
| stim_onset | -50, -10, -2, +2, +10, +50 ms (negative delays skipped) |
| stim_duration, sim_length | x 0.5, 0.9, 1.1, 2 |
| scale_conductance, scale_capacitance | x 0.5, 0.8, 0.9, 1.1, 1.25, 2 |
| shift_reversal | -10, -5, -2, +2, +5, +10 mV |
| shift_initial_voltage | -20, -5, -2, +2, +5, +20 mV |
| scale_gate_time_constant | rates x 0.5, 0.8, 1.25, 2 (tau / k) |
| increase_dt | x 2, 5, 10, 20 (x20 approaches forward-Euler instability for fast Na) |
| recording_resolution | 0.05, 0.25, 1, 2 ms (2 ms is longer than an AP half-width) |
| reduce_spatial_discretization | divisions // 2, // 4 |

Quantity arithmetic uses `Decimal` and keeps each literal's style and unit, e.g.
`7.5E-10A x 0.9 -> 6.75E-10A` and `0.3s + 10 ms -> 0.31s`.

## 4. Observations (smoke runs, not results)
- **Site counts with all sites generated and enforced** (all passed enforcement): RS 121,
  LTS 144, HH example 109, WB 99.
- **`solver_config` under jnml.** The RS harness (400 ms, dt 0.025 ms, 3 spikes) with
  `Meta method="rk4"` or `"eulertree"` gave voltage traces bit-identical to the reference;
  the same held for LTS in an exploratory run. The M0 source reading
  (`neuroml-lems.verify.json`) supports this only for `rk4`: under jnml's `Sim.run()` it is
  a documented no-op. `eulertree` *does* change the jLEMS code path (no consolidation, raw
  state tree, still forward Euler). Its identical trace is an empirical observation for
  this model, window and version, consistent with both paths being Euler, not an
  equivalence by construction. The check is repeated in
  `tests/integration/test_mutants_validate.py`.
- **jnml -validate misses some removed includes.** Validator test 10025 checks the ion
  channel of `channelDensity` elements. Removing the include on the cell file failed
  validation for every channel referenced by a plain `channelDensity` or
  `channelDensityNernst`. It did **not** fail for:
  - RS without `Na.channel.nml`: `Na` is used by a `channelDensityVShift`;
  - LTS without `Ca.nml`: the `CaPoolModel` concentration model.

  Those mutants are "structurally valid" and must be classified at execution time. Note
  also that the RS/LTS harness LEMS files include the channel files directly, so the
  canonical run may still build.
- **Integration run** (n_per_operator=2, seed 20260913, RS and LTS): `omit_include` was the
  only operator that produced cell files jnml -validate rejects (1 of 2 per model).
- **XML serialisation (corrected).** Re-serialising through lxml is *semantically*
  identical (`xml_changes == []` for every harness, cell, include and channel file of RS,
  LTS, HH example and WB) and keeps the XML declaration, including ISO-8859-1, byte-for-byte.
  It is **not byte-minimal**. A no-op read/write changed bytes in 11 of 21 files checked
  (`work/tmp/mutations/noop_rewrite.py`), for example 19 changed diff lines in
  `IT.channel.nml`, 16 in the HH example harness and 13 in `WangBuzsaki.cell.nml`.
  lxml joins multi-line start tags, drops the space before `/>` and removes trailing
  blank lines. So a mutant's textual diff also shows reformatting, and the earlier
  "one-line diff" claim was wrong. Use `xml_changes` (or `variant.json` edits), not `git
  diff`, to audit a mutant. If byte-minimal diffs are needed for the 20-mutant manual
  audit, attribute edits would have to be spliced into the original text at the
  attribute's byte span instead of re-serialising the tree (not implemented).
