# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions will follow Semantic
Versioning from the first tagged release. Decisions referenced as D-xxx are in `DECISIONS.md`.

## [Unreleased]

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
