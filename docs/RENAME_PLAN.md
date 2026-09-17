# Rename plan: `neuraxis` → `perturbprint`

*Prepared 2026-09-17 on Neel's decision that the planned public name is **PerturbPrint**
(`docs/NAME_DECISION_PACKET.md`). **Not executed yet.** It runs only after the current readiness work
and Pilot 2, and only on Neel's go-ahead. The permanent internal study identifier,
`neuron_model_behavioral_validation`, does not change and is independent of branding.*

## In plain English

- The code folder gets renamed once, from `neuraxis` to `perturbprint`.
- Old results, old file paths, old names in the history and every hash stay exactly as they are.
- We do **not** keep three names working forever. One name, one import.

## 1. Recommendation: one canonical namespace, no permanent aliases

**Recommended: `perturbprint` only.** Reasons:
- nothing is published (no PyPI release, no DOI, no public repository, no downstream user), so no
  external code imports `neurosem` or `neuraxis`;
- three import paths for one package invite mismatched module objects, duplicated registries and
  confusing provenance;
- the alias shim exists only to spare an in-repository refactor, which this plan does anyway.

**The one concrete compatibility need** is the hidden agent-study material
(`agent_study/hidden/*/hidden_checks.yaml`, Git-ignored, hashes committed in
`agent_study/HIDDEN_MANIFEST.sha256`). Those files mention `neurosem`. The plan updates them and
re-records their hashes in the same commit; if Neel would rather not touch them before his own
review (N-12), the `neurosem` alias can stay until that review, and only until then.

**Decision requested:** drop both aliases at rename time (recommended), or keep `neurosem` until the
hidden-evaluator review.

## 2. What must not change

| Preserved | How |
|---|---|
| Git history | A rename commit, never a rewrite; `git log --follow` keeps file history. Tag `pilot-v1-code` stays. |
| Raw result paths | `results/raw/pilot/…`, `results/raw/curation-*/…` untouched; sealed campaigns stay sealed. |
| Recorded metadata | `project_name`, `study_id`, feature-source labels such as `neurosem:firing_regime`, and the `neurosem:` key in `features.yaml` stay as recorded. Renaming them would change hashed configuration and break recorded provenance. |
| Hashes | No file that any manifest hashes is edited: model snapshots, `ARCHIVE_MANIFEST.sha256`, `SPLITS.sha256`, pre-run manifests, archive tars. Verified before and after. |
| Earlier names in the record | `DECISIONS.md`, `docs/DEVIATION_LOG.md`, `CHANGELOG.md`, `AI_USE_LOG.md`, `docs/NAME_*`, `docs/build_notes/`, `docs/m0_evidence/`, `docs/handoff/` keep NeuroSem and Neuraxis as written. |

## 3. Steps (one commit, on a branch)

1. **Freeze.** No campaign running; working tree clean; full suite green.
2. `git mv src/neuraxis src/perturbprint`.
3. Rewrite imports and module paths in `src/`, `tests/`, `scripts/`, `workflows/`, `pyproject.toml`,
   `Makefile`, `Dockerfile`, `.github/workflows/` — `from neuraxis`, `import neuraxis`,
   `neuraxis.<module>`, `src/neuraxis`.
4. Environment variables: `PERTURBPRINT_*` preferred, `NEURAXIS_*` and `NEUROSEM_*` accepted for one
   release, all documented in `provenance.env_var`.
5. `pyproject.toml`: `name = "perturbprint"`, console script `perturbprint`; keep `neuraxis` and
   `neurosem` console scripts only if Neel chooses the compatibility option.
6. Alias modules: delete `src/neurosem/` (and do not create `src/neuraxis/`) under the recommended
   option; otherwise keep the existing shim pattern.
7. Update the living documents (README, PLAN, protocol documents, catalogues) but not the historical
   record listed above.
8. **Verification, all in the rename commit's log:**
   - `python -m pytest` full suite green;
   - `python scripts/verify_archive.py --campaign pilot …` still verifies (5,186 files);
   - `python scripts/pre_run_manifest.py … --verify` for every pre-run manifest;
   - `neuraxis`/`perturbprint` CLI `--help` and `import perturbprint` work;
   - `git status` clean; every previously tracked hash file unchanged (`git diff --stat` shows no
     manifest edits).
9. Record it: `docs/DEVIATION_LOG.md` (new row), `CHANGELOG.md`, `DECISIONS.md`, and a note in
   `docs/NAME_DECISION_PACKET.md` that the name is adopted.

## 4. What the rename does not decide

- Public release, DOI, repository visibility and manuscript title still wait for Neel (D-044).
- The name audit is not legal clearance; EU, WIPO and UK registers were not searched.
