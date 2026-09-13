# Discovery / held-out splits

Status: **PROVISIONAL (pilot)**. Nothing in this directory is frozen yet: there is no
`SPLITS.sha256`, and no held-out models or families have been assigned.

| File | Content | Read by |
|---|---|---|
| `discovery_models.txt` | discovery model ids, one per line (LF, UTF-8, no BOM) | `neurosem.selection.splits.discovery_view` |
| `discovery_families.txt` | mutation families usable for protocol selection, one per line | `discovery_view` |
| `heldout/heldout_models.txt` | held-out model ids (not yet created; see `heldout/README.md`) | only `splits.HeldoutGate` |
| `heldout/heldout_families.txt` | held-out mutation families (not yet created) | only `splits.HeldoutGate` |
| `SPLITS.sha256` | `sha256  relative/path` for every `*.txt` file under `data/splits/` | `verify_split_hashes`, `HeldoutGate` |

## Current provisional discovery split

- Models: `pospischil2008_rs`, `pospischil2008_lts`, the two pilot fixtures
  (`inclusion=include` in `data/model_manifest.csv`).
- Families: `biophysical`, `reference`, `numerical`, the pilot mutation families in
  `configs/study.yaml`. `stimulus` is therefore outside the discovery split. That does
  **not** make it a held-out family; held-out families are assigned only in
  `heldout/heldout_families.txt`.

The pilot is used to develop operators, calibrate tolerances and debug selection. The
study specification asks for 8-10 discovery models and 4-6 held-out models in the full
study, so this list is expected to change before the freeze.

## Rules

1. Discovery-side code (`selection.matrix`, `selection.greedy`, experiments, CLI commands
   other than `evaluate-heldout`) gets the split only through `discovery_view(root)`,
   which reads the two discovery files and never opens `heldout/`. Tests make every open,
   stat or listing of `heldout/` fail while discovery selection runs.
2. `DiscoveryView.filter_matrix` raises `LeakageError` if a detection matrix contains any
   row whose model or family is not in the discovery lists.
3. Freezing: `python scripts/freeze_splits.py` validates the split (all four files present
   and non-empty, known families, discovery and held-out lists disjoint, model ids in the
   manifest) and writes `SPLITS.sha256`. An existing, different freeze is overwritten only
   with `--force-with-reason "..."`. Freezes and forced re-freezes are appended to
   `results/heldout_access.log`.
4. Once frozen, `discovery_view` verifies the discovery files against `SPLITS.sha256`;
   the frozen study calls it with `require_frozen=True`.
5. Held-out labels are read only by `HeldoutGate(root, "configs/FROZEN.lock", reason)`,
   which requires the frozen configuration lock at exactly `configs/FROZEN.lock` (a lock
   file anywhere else is refused) to record `SPLITS.sha256`, `configs/study.yaml` and every
   other `configs/*.yaml` with matching hashes, and logs every access (timestamp, reason,
   git commit).

Files here are stored byte-exact (`.gitattributes`: `data/splits/** -text`) because they
are identified by SHA-256. Keep LF line endings.
