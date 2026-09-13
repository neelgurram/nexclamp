# Held-out split (not yet assigned)

This directory will hold the evaluation-only split. **No held-out models or mutation
families have been assigned.** Choosing them is Neel's decision and is made once, before
the frozen study, not by the software and not during development.

Once created, the files here are read only by `neurosem.selection.splits.HeldoutGate`,
which refuses unless the study configuration is frozen and logs every access to
`results/heldout_access.log`.

## How the held-out split will be added and frozen

1. **Choose** the held-out models and at least one held-out mutation family. The
   specification targets 4-6 held-out base models and at least one mutation family that
   is excluded from protocol selection. Prefer held-out models that do not share
   `source_family` with any discovery model in `data/model_manifest.csv`: models from the
   same paper or repository share channel files and behave in correlated ways (for
   example, the FS and IB candidates share `pospischil2008` with both pilot models).
   `freeze_splits.py` prints a warning for such pairs; it does not decide for you.
2. **Write** two files in this directory, one identifier per line, UTF-8, LF line endings:
   - `heldout_models.txt`: model ids from `data/model_manifest.csv`;
   - `heldout_families.txt`: values of `neurosem.schemas.MutationFamily`
     (`stimulus`, `biophysical`, `reference`, `numerical`).
3. **Update** `../discovery_models.txt` and `../discovery_families.txt` so they are
   disjoint from the held-out lists (the freeze refuses overlapping lists).
4. **Freeze**: `python scripts/freeze_splits.py`. This writes `../SPLITS.sha256` and logs
   the freeze. Commit the split files and `SPLITS.sha256` together, and record the split
   in the preregistration.
5. **Lock the study** (Milestone 8): write `configs/FROZEN.lock` in the same
   `sha256  relative/path` format, recording `data/splits/SPLITS.sha256`,
   `configs/study.yaml` and every other `configs/*.yaml`. Until that lock exists at exactly
   that path and matches, `HeldoutGate` stays closed; a lock file written anywhere else
   does not open it.
6. **Evaluate** only through `HeldoutGate` (`neurosem evaluate-heldout`). Do not inspect
   held-out failures and redesign around them. If a split must change after freezing,
   run `freeze_splits.py --force-with-reason "..."`; the reason, the previous hash and any
   earlier held-out accesses are logged and must be disclosed.
