# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions will follow Semantic
Versioning from the first tagged release. Decisions referenced as D-xxx are in `DECISIONS.md`.

## [Unreleased]

### Neuraxis execution-plan build (2026-09-16)

Controlling specification: `docs/handoff/NEURAXIS_EXECUTION_PLAN.pdf` (D-039). Conflicts and resolutions are recorded in `docs/DEVIATION_LOG.md`.

#### Changed
- Package renamed `neurosem` to `neuraxis` (`src/neuraxis/`); `neurosem` remains an alias module and command. Version is 0.2.0.dev0; `NEURAXIS_*` environment variables take precedence over `NEUROSEM_*`.
- Code licence is now Apache-2.0, provisionally (D-043); the BSD-3-Clause text is kept in `docs/licensing/`.
- Documents renamed to the plan's names; `DEPENDENCY_AUDIT.md` moved to `docs/`.
- Default `configs/study.yaml` gained `study_metadata` (Neuraxis, development).

#### Added
- Run records carry the plan's fields; output streams are stored and hash-verified; toolchain failures are kept in `_tool_failures/` and never block a retry (D-040).
- `neuraxis curate-models` (criteria C01-C13, reference simulations only; D-041) and candidate-snapshot lookup in `models/candidates/`.
- `neuraxis smoke-test` (the plan's nine infrastructure checks).
- Ion-channel kinetics mutation family: `shift_gate_midpoint`, `scale_gate_slope`, `shift_forward_rate_midpoint`, `shift_channel_vshift`; excluded from protocol selection in code (D-042).
- Workflows: `curate_models`, `run_references`, `generate_variants`, `run_development`, `freeze_study`, `run_heldout` (requires the exact AsPredicted authorisation sentence, URL and PDF), `lock_primary_results`, `run_robustness`, `run_agent_study`, `reproduce_manuscript`, `smoke_test`.
- `scripts/build_manifests.py`: `manifests/` (protocols, mutations with taxonomy class, transformations, splits, model sources, per-snapshot hashes) and `docs/LICENSING_MATRIX.md`.
- Documents: `CURRENT_REPOSITORY_STATE`, `SPECIFICATION_GAP_ANALYSIS`, `PRIOR_ART_MATRIX` (36 works, 5 verification packets), `NAME_AUDIT`, `PLAIN_LANGUAGE_OVERVIEW`, `DEVELOPMENT_PROTOCOL`, `FEATURE_CATALOG`, `DEVIATION_LOG`, `DECISIONS_REQUIRED`, `MODEL_CURATION_REPORT`; manuscript skeletons; D-039 to D-043.
- Tests: `test_kinetics_operators.py`, `test_run_record_fields.py`, `tests/regression/test_pilot1_corrected_facts.py`.

### Neuraxis PILOT_PROTOCOL_V1 pre-run preparation (2026-09-14/15)

#### Added
- `docs/PILOT_PROTOCOL_V1.md` (written protocol with an executable-settings block) and `tests/unit/test_pilot_protocol_v1.py` (protocol-config agreement).
- `docs/pilot/PILOT_PROTOCOL_V1_DEVIATIONS.md`.
- Study labels: `study_metadata` config block; `project_name`, `study_phase`, `protocol_version` and `config_sha256` in `run.json` and rheobase records; metadata columns in campaign tables and detections; `STUDY_METADATA.json`; labelled reports, diagnostics and figure footers.
- `experiments/pilot_outputs.py` and `scripts/pilot_outputs.py` (prespecified outputs 2-11), `scripts/reproducibility_check.py`, `scripts/pre_run_manifest.py`, `scripts/pre_run_package.py`; `tests/unit/test_pilot_outputs.py`.
- D-033 to D-038.

#### Changed
- `configs/pilot_v2_draft/` renamed to `configs/pilot_protocol_v1/`, with `study_metadata` and repeated/new model lists added. No design value changed.
- `docs/pilot/pilot_interpretation.md` marked superseded (D-038).

### Pilot 2 revision: feature panels, numerical stratum, archive verification (2026-09-13)

#### Added
- `experiments/strata.py`: semantic, numerical-robustness, harness and control strata; `primary_admissible`; `check_identical_numerics`; operator exclusion; primary/secondary detection split; convergence rows against the reference's h, h/2 and h/4 error (D-029, D-030).
- `secondary_features` for protocols and the canonical harness; `pilot.exclude_operators`.
- Campaign outputs: `detections_secondary.csv`, `secondary_feature_report.csv`, `numerical_robustness.csv`, `detection_matrix_numerical_robustness.csv`, `validation_cascade_numerical_robustness.json`, `generation.json`.
- `scripts/numerical_robustness_report.py` and `results/derived/pilot/`, a read-only reanalysis of sealed Pilot 1.
- `scripts/verify_archive.py`; `results/processed/pilot/ARCHIVE_README.md`, `ARCHIVE_VERIFICATION_local.json`; verified Git bundle (local, Git-ignored).
- `tests/unit/test_strata.py`.
- `docs/pilot/numerical_reclassification.md`; D-029 to D-032; N-17.

#### Changed
- The primary detection matrix, cascade, silent list, pilot criteria, analysis figures and held-out denominator use the semantic stratum and primary feature panel only.
- Numerical stress tests always run at h, h/2 and h/4.
- `docs/pilot/pilot_v2_design.md` revised per N-14; `configs/pilot_v2_draft/study.yaml` updated.

### Pilot role, preservation and bounded iteration 2 (2026-09-13)

#### Added
- `experiments/registry.py`: permanent campaign roles (`results/campaign_registry.json`), sealing, config snapshots, a one-configuration-per-campaign guard, a single-clean-commit check, SHA-256 archive manifests and write-once tar archives (D-026, D-027).
- `scripts/archive_campaign.py`; campaign `pilot` archived (5,186 files, 1.92 GB tar, Git-ignored) and sealed; tag `pilot-v1-code` at `d323afa`.
- `NEUROSEM_CONFIG_DIR` for development campaigns; `canonical.features` setting (default unchanged).
- `docs/pilot/PILOT_REGISTER.md`, `docs/pilot/pilot_v2_design.md`, `configs/pilot_v2_draft/` (draft, not run).
- `PLAN.md` post-pilot freeze sequence; D-026 to D-028; N-14 to N-16.

#### Changed
- `evaluate_heldout` refuses exploratory or discovery campaigns, reused campaign names, config overrides, non-held-out models, and mixed-commit or dirty runs.
- Pilot reports are labelled exploratory/developmental.
- Preregistration section 15 and the statistical plan state that pilot data are never pooled.

### Milestones 1-7 infrastructure and the Milestone 6 pilot (branch `m0-audit`, 2026-09-13)

Neel instructed Claude to build the whole project (D-003). The integrity gates stay in place:
- no held-out evaluation;
- no frozen study without preregistration;
- no agent trials by the assistant that built NeuroSem;
- no public release without Neel.

#### Added
- **Environment:**
  - Python 3.12 virtual environment with pinned pyNeuroML 1.3.22, libNeuroML 0.6.7 and eFEL 5.7.34, frozen in `requirements.lock`.
  - Portable Eclipse Temurin 21.0.12.1, checksum-verified (`scripts/bootstrap_java.py`, `.tools/jdk_provenance.json`).
  - `Dockerfile`, `environment.yml`, `Makefile` and GitHub Actions CI. None of these has been built or run yet, because this machine has no Docker and the repository has no GitHub remote.
  - `CITATION.cff` and `docs/REPRODUCING.md`.
- **Models:** commit-pinned, hash-verified snapshots with provenance, fetched by `scripts/fetch_models.py`:
  - Pospischil 2008 RS, LTS, FS and IB;
  - the NeuroML2 Hodgkin-Huxley example;
  - Wang-Buzsaki 1996.

  A curation sweep added 7 further licensed candidates (`data/model_candidates.csv`).
- **Core (`src/neurosem`):**
  - NeuroML quantity handling and provenance (content hashes, environment digest, write-once results).
  - jNeuroML adapter with an error taxonomy.
  - Protocol catalogue (P01-P10; P11 and P12 deferred), batched probe generation and rheobase grid search.
- **Validation:**
  - Relative structural oracle (D-006).
  - Content-addressed run recorder with feature keying (D-012).
  - Canonical harness protocol.
  - Tolerance calibration by refinement; fingerprints, detections and the six-way classification.
- **Mutations and transformations:**
  - 19 mutation operators in 4 families, with single-operator enforcement.
  - 8 valid-transformation and no-change operators with byte-preserving edits.
- **Selection and analysis:**
  - Detection matrix, greedy maximum coverage, count- and runtime-matched random baselines.
  - Split files with leakage barriers and the gated `HeldoutGate`.
  - Metrics, cluster bootstrap, exact McNemar, cluster sign-flip test, and all 8 figure functions.
- **Experiments and CLI:**
  - campaign, pilot, discovery (selection), gated held-out and analysis/reproduction stages;
  - the `neurosem` CLI with every command the specification lists.
- **Agent-study harness (Milestone 9):**
  - nine task definitions, public checks, clean trial export and scoring;
  - hidden evaluators kept out of Git (D-022).
- **Documentation:**
  - `docs/ARCHITECTURE.md`, glossary, model selection, protocol and mutation catalogues;
  - statistical plan, preregistration draft, AI disclosure, agent-study protocol;
  - Neel's learning guide, development notes (`docs/pilot/dt_probe.md`) and per-module build notes.
- **Tests:** 979 passing (1 skipped) on commit `3cdb957`, including real jNeuroML simulations.

#### Changed / fixed during integration
- Mid-run divergence is classified as numerically unstable. A validator coverage gap was recorded (D-020).
- One reproducible detection rule for every protocol, targeted canonical windows, the q10 time-constant mechanism, a new `increase_dt` grid, a 10 V blow-up bound, and several core defect fixes (D-021).
- jLEMS time labels are regularised to the exact fixed-step grid.
- The provenance dirty flag is scoped to simulation-relevant paths (D-023).

### Milestone 0 — Audit (branch `m0-audit`, started 2026-09-13)

#### Added
- `docs/handoff/`: the handoff and the final specification (PDFs archived unchanged, with text extractions).
- `docs/m0_evidence/`: raw evidence from the verification, critique, name, fixture and prior-art sweeps.
- `DECISIONS.md`, `CHANGELOG.md`, `AI_USE_LOG.md`, `.gitignore`, `.gitattributes`.
