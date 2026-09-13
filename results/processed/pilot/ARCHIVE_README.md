# Pilot 1 archive: what it is, how to restore it, how to verify it

*Campaign `pilot` (exploratory iteration 1). DECISIONS D-027 and D-031. The archive itself is
not in Git; everything needed to check it is.*

## What is archived

| Item | Value |
|---|---|
| Archive file | `pilot_raw_and_workspaces.tar` |
| SHA-256 | `ad11661f4684c018f4cefb78a8f0faea4b396f745afdf2684ace6c2b24a19d3a` |
| Size | 1,922,519,040 bytes (1.92 GB) |
| Files | 5,186 data files, plus `ARCHIVE_MANIFEST.sha256` inside the tar (5,187 members) |
| Format | POSIX tar, PAX headers (Python `tarfile` default), **no compression** (traces are already compressed `.npz`) |
| Software | Python 3.12.10 standard-library `tarfile`, Windows 11 (10.0.22631) |
| Created | 2026-09-13 19:33:32 UTC, by `scripts/archive_campaign.py` (command below) |
| Last verified | 2026-09-13 19:54:34 UTC: full extraction, 5,186 of 5,186 files match, no extra files (`ARCHIVE_VERIFICATION_local.json`) |

Contents, by top-level folder inside the tar:

| Folder | Source on the original machine |
|---|---|
| `raw/` | `results/raw/pilot/`: every `run.json`, traces (`.npz`, Git-ignored), rheobase searches, environment records |
| `work_variants/` | `work/variants/pilot/`: materialised reference, mutant and control workspaces |
| `work_runs/` | `work/runs/pilot/`: simulator run scratch |
| `work_smoke/` | `work/smoke/`: development smoke runs |

## Tracked in Git alongside it

| What | Where |
|---|---|
| Per-file checksums | `results/processed/pilot/ARCHIVE_MANIFEST.sha256` |
| Archive hash and size | `results/processed/pilot/ARCHIVE.json` |
| Seal | `results/processed/pilot/SEALED.json` |
| Config files as used | `results/processed/pilot/config_snapshot/`; hashes in `campaign_configs.json` |
| Run logs | `results/processed/pilot/logs/` |
| Code version | tag `pilot-v1-code` (commit `d323afa`) |
| Environment | `results/raw/pilot/_environments/*.json`, `requirements.lock`, `.tools/jdk_provenance.json`; simulator versions in `campaign_configs.json` |

## Copies

| Copy | Location | Status |
|---|---|---|
| 1 (primary) | this machine, `archive/pilot/` (Git-ignored) | verified 2026-09-13 |
| 2 (independent, private) | **not yet created**: Neel has not yet chosen the storage location (N-16) | pending |
| Repository | `archive/pilot/neurosem_repo_d8bbb6b.bundle` (full Git history and tags; SHA-256 `e31588e0c84546abae8438e7b22bf167b3a00e3771d56ce639e7ece66fd77de6`; `git bundle verify` passed) | local only; travels with copy 2 |

The repository has no remote yet (N-01). The bundle is how the tag, logs and manifests survive if
this disk fails.

## How it was created

```bash
python scripts/archive_campaign.py --campaign pilot --role exploratory_pilot --code-commit d323afa --code-tag pilot-v1-code --note "..." --log work/logs/pilot_run.log --log work/logs/pilot_commit.txt --log work/logs/pilot_reference.log --log work/logs/pilot_analyze.log --log work/logs/integration_check.log --log work/logs/prov_test.log --extra work_smoke=work/smoke
```

## How to restore and verify

1. Get the repository. From the bundle, if there is no remote:

   ```bash
   git clone neurosem_repo_d8bbb6b.bundle NeuroSem
   ```

2. Set up the environment as in `docs/REPRODUCING.md` (Python venv from `requirements.lock`; `python scripts/bootstrap_java.py`).
3. Check the archive hash:

   ```bash
   sha256sum pilot_raw_and_workspaces.tar
   ```

   It must equal the SHA-256 above.
4. Extract and verify every file against the committed manifest. This check extracts into `--extract-to`, compares all 5,186 checksums and the embedded manifest, then deletes the extraction unless `--keep` is given:

   ```bash
   python scripts/verify_archive.py --campaign pilot --tar pilot_raw_and_workspaces.tar --extract-to restore_tmp --record verification.json --keep
   ```

5. To put the data back where the pipeline expects it, move `restore_tmp/raw/` to `results/raw/pilot/`, `work_variants/` to `work/variants/pilot/`, and `work_runs/` to `work/runs/pilot/`.
6. To inspect the code exactly as it ran:

   ```bash
   git checkout pilot-v1-code
   ```

## Publication rules

- Not public. Do not deposit until the public release.
- The archive holds copies of the model files (Pospischil 2008, MIT) inside the workspaces. At release, re-check every licence (`LICENSE_AUDIT.md`) and deposit only what may be redistributed. Otherwise deposit manifests, hashes and the fetch/reproduction scripts.
- At release: create a frozen Zenodo (or equivalent DOI) record and link it to the GitHub software release. Label this archive as exploratory Pilot 1, separate from the confirmatory data.
