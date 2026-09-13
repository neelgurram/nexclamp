# Build note: `selection/` (ARCHITECTURE.md section 3.7)

Implemented: `src/neurosem/selection/{__init__,matrix,greedy,splits}.py`, `scripts/freeze_splits.py`,
`data/splits/{README.md,discovery_models.txt,discovery_families.txt}`, `data/splits/heldout/README.md`,
tests `tests/unit/test_{selection_matrix,greedy_selection,splits_leakage}.py`.

No core module needed changing. ARCHITECTURE.md does not define several formats and a few
signatures that this module had to fix; they are listed here so the contract file can be
updated to match (section 2 table and section 3.7).

## 1. File formats defined by this module

| Path | Format |
|---|---|
| detection matrix CSV (`DetectionMatrix.to_csv`) | header `mutant_id,model_id,family,<protocol_id>...`; first data row `__cost__,,,<repr(float) cost>...`; then one row per mutant with `0`/`1`. LF, UTF-8. `repr` round-trips costs exactly. |
| `data/splits/SPLITS.sha256` | `sha256sum` text format `<64 hex>  <repo-relative posix path>`, sorted; covers every `*.txt` under `data/splits/` (README `*.md` files are not frozen). |
| `configs/FROZEN.lock` | same `sha256sum` format. `HeldoutGate` accepts only `<root>/configs/FROZEN.lock` (any other path is refused, even with matching hashes) and requires it to record `data/splits/SPLITS.sha256`, `configs/study.yaml` (which must exist) and every other `configs/*.yaml`/`*.yml` present, all matching. Milestone 8 should write it with `neurosem.selection.splits.format_hash_manifest(root, [...])`. Adding a config after the lock closes the gate until the lock is regenerated (intended). |
| `results/heldout_access.log` | JSON lines, append-only, keys sorted. Events: `heldout_gate_opened` (`timestamp_utc, reason, git_commit, git_dirty, frozen_lock, frozen_lock_sha256, splits_sha256`), `splits_frozen` / `splits_refrozen` (`timestamp_utc, reason, git_commit, git_dirty, splits_sha256, previous_splits_sha256, files`). |

## 2. Signature additions (backward compatible with section 3.7)

- `Selection` gains defaulted fields `gains, objective, stop_reason, n_mutants, k, cost_budget, candidates,
  shortfall`. **`costs` is cumulative** (parallel to `coverage_curve`), not per protocol. `shortfall`
  (maximum coverage only) is `k - len(protocols)`.
- `k`, `draws`, `seed` (and `budget_k`, `random_draws`, `seed` in `selection_settings`) must be integers
  (`int` or NumPy integer, not `bool`); anything else raises `TypeError` instead of being truncated.
- `greedy.count_matched_sets(...)`, `greedy.runtime_matched_sets(...)` return the drawn sets; the
  `random_*` functions return the rates of exactly those sets. `greedy.selection_settings(study_cfg)`
  reads `configs/study.yaml: selection` and rejects any `tie_break` other than `[cost, protocol_id]`.
- `DetectionMatrix` gains `from_detected_sets`, `take_rows`, `covered`, `total_cost`,
  `column_indices`, `row_indices`; `matrix.cell_step_costs(protocols, dt_ms, n_cells=1, measured=None)`
  (equals `ProbeBundle.cell_steps` per batch; the rheobase search cost must be passed as `measured`).
- `verify_split_hashes(root, scope="all" | "discovery")`; `discovery_view(root, require_frozen=False)`.
- `DiscoveryView` gains `families, frozen, file_sha256` and `is_discovery`, `discovery_mask`.
  `excluded_families` = known `MutationFamily` values not listed in `discovery_families.txt`
  (derived without reading held-out files; "excluded from discovery" is not "held out").
  Built from the contract fields only (`DiscoveryView(models, excluded_families)`), `families` is
  derived as known families minus `excluded_families`; unknown or overlapping families raise `ValueError`.
- `Split` gains a defaulted `discovery_families`.
- `HeldoutGate(root, frozen_lock, reason)`: a relative `frozen_lock` is resolved against `root`, and
  the resolved path must be `<root>/configs/FROZEN.lock` (the parameter stays for contract
  compatibility and for test roots). An empty reason is refused. `split()` re-verifies all hashes before reading.
- `read_id_list` rejects a UTF-8 byte-order mark (`ValueError`) instead of making it part of the first id.
- Exceptions: `LeakageError(RuntimeError)` > `SplitIntegrityError` > `FrozenSplitError`.
- `splits.freeze_splits(root, force_reason=None) -> FreezeResult` holds the freeze logic used by
  `scripts/freeze_splits.py` (exit 0 frozen/unchanged, 1 invalid split, 2 refused).
- `neurosem.selection` re-exports only discovery-side names; `HeldoutGate` must be imported from
  `neurosem.selection.splits` (keeps the static "no heldout outside splits.py" test meaningful).

## 3. Interpretations that downstream code must know

1. **Greedy early stop (decision; ARCHITECTURE.md section 3.7 should record it).** The spec's
   procedure says "continue until reaching budget k"; the assignment allows an early stop "only
   when nothing remains to cover". `greedy_max_coverage` stops before `k` when every mutant is
   covered (`all_mutants_covered`) *or* when no remaining candidate detects any still-undetected
   mutant (`no_remaining_gain`). For the greedy rule these are the same situation: every remaining
   candidate has zero marginal gain, and a zero-gain protocol would be picked only by the
   cost/id tie-break, i.e. by an arbitrary rule with no discovery evidence, yet it would still
   change the frozen battery that goes to held-out evaluation. Filling to `k` was therefore
   rejected (review option (a)); the stop is kept and the empty slots are stored in
   `Selection.shortfall` (review option (b)). Consequence for analysis: when `shortfall > 0`,
   the count-matched baseline must use `len(selection.protocols)` (report `k` and the shortfall
   alongside), otherwise the random battery gets more protocols than the selected one; figures
   must not assume the battery size equals `--budget K`.
2. **Runtime-matched rule.** Random-order first fit: permute candidates (sorted by id, then
   `default_rng(seed).permutation`), add each protocol whose cost still fits the budget, skip the
   rest; sets are maximal. Budget comparisons allow a relative slack of `1e-9` so that the greedy
   battery's own total (an `fsum`) is always feasible regardless of summation order.
3. **Cost-sensitive greedy** is ratio greedy plus the Khuller-Moss-Naor (1999) best-single-protocol
   comparison. It is the specification's *optional* objective; the primary battery is
   `greedy_max_coverage`. Gain/cost ratios are ranked exactly (`fractions.Fraction` of the stored
   costs), not by float division: IEEE division is correctly rounded, so exactly equal ratios
   always compared equal, but *unequal* ratios could round to the same double (e.g. gains 1 and 3
   at stored costs 0.1 and 0.3 both give 10.0, although 3/0.3 is exactly larger) and be sent to the
   cost/id tie-break. Zero-cost protocols with positive gain rank above all paid ones and, among
   themselves, by gain (they previously all tied at `inf`).
4. **Reproducibility of random baselines** holds for a fixed seed and NumPy version (2.5.3 in the
   current venv); NumPy does not guarantee identical `Generator` streams across versions.
5. `DiscoveryView.filter_matrix` raises on any non-discovery row instead of dropping it. Matrix
   builders that start from all mutants must restrict rows explicitly
   (`m.take_rows(view.discovery_mask(m))`) so the restriction is visible in code.

## 4. Open decisions (not taken here)

- Held-out models and families: unassigned (Neel). `data/splits/heldout/` contains only a README.
- `discovery_families.txt` lists the pilot families (`biophysical, reference, numerical`), which
  leaves `stimulus` outside discovery; whether a family is held out is decided in the held-out files.
- Whether `HeldoutGate` should additionally require `configs/study.yaml: status: frozen` (currently
  the lock alone is the freeze marker).
