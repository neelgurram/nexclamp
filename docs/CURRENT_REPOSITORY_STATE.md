# Current repository state

*Required first document of the Neuraxis execution plan (`docs/handoff/NEURAXIS_EXECUTION_PLAN.pdf`,
SHA-256 `2ae2a2ce…2ddd`). Inventory taken on 2026-09-16 at commit `c46e10a` (branch `m0-audit`,
20 commits, tag `pilot-v1-code`, no remote), before this build. Section 7 lists what the build
changed.*

## In plain English

- Most of the testing machine already exists and is tested: over 1,000 automated tests pass.
- One small practice run (Pilot 1) was done on two related model cells. Its data are locked and
  unchanged. It showed no hidden behaviour change from real model edits.
- A second practice run (Pilot 2) is designed but has not run. It stopped at a readiness check
  because one model file (Wang–Buzsáki) breaks the NeuroML schema.
- No held-out ("exam") data have been created or looked at.
- The project was called NeuroSem; it is now Neuraxis. Old names stay where changing them would
  damage the record of what was done.

## 1. What exists

| Area | Location | Status |
|---|---|---|
| Python package | `src/neuraxis/` (renamed from `src/neurosem/` in this build; `neurosem` remains an import alias) | verified by the test suite |
| Simulation adapter | `simulators/jneuroml.py` (jNeuroML 0.14.0 jar, Temurin 21) | verified; real jLEMS runs in integration tests |
| Structural validation | `validation/structural.py` (relative oracle over the include closure, D-006) | verified |
| Protocols and rheobase calibration | `protocols/` (P01-P10 implemented; P11 and P12 not implementable with NeuroML core inputs) | verified |
| Features | `features/` (eFEL 5.7.34 adapter, trace metrics, firing regimes) | verified |
| Mutations, valid transformations | `mutations/`, `transforms/` (13 mutation operators in 4 families, 8 transformation operators) | verified; human audit of ≥20 mutants pending |
| Fingerprints, tolerances, classification | `validation/fingerprint.py`, `validation/convergence.py` | verified |
| Campaign orchestration | `experiments/campaign.py`, `registry.py` (roles, sealing), `strata.py` (semantic vs numerical) | verified |
| Selection and leakage barriers | `selection/` (greedy, random baselines, `HeldoutGate`) | verified; split not assigned |
| Analysis and figures | `analysis/`, `experiments/analyze.py`, `experiments/pilot_outputs.py` | verified on synthetic data; figures drawn for Pilot 1 |
| Agent-study harness | `experiments/agent.py`, `agent_study/` (hidden checks Git-ignored) | built; no trials run; hidden checks need independent review (N-12) |
| Configuration | `configs/study.yaml`, `features.yaml`, `tolerances.yaml`, `agent_policy.yaml`; `configs/pilot_protocol_v1/` | provisional; not frozen |
| Models | `models/raw/` (Pospischil 2008, NeuroML2 HH, Wang–Buzsáki), `models/candidates/` (Prinz, Maex, Smith, Migliore, Solinas, Pinsky–Rinzel); `data/model_manifest.csv`, `data/model_candidates.csv` | commit-pinned, hash-verified; licences audited (`LICENSE_AUDIT.md`) |
| Environment | `requirements.lock`, `pyproject.toml`, `environment.yml`, `.tools/` JDK, `Dockerfile`, `Makefile`, `.github/workflows` | lock and venv verified; Docker never built (no Docker on this machine); CI never run (no remote) |
| Audits and plans | `DEPENDENCY_AUDIT.md`, `LICENSE_AUDIT.md`, `PRIOR_ART_AUDIT.md`, `docs/novelty_matrix.csv` (335 works), `docs/NAME_CONFLICT_AUDIT.md`, `RISK_REGISTER.md`, `REQUIREMENTS.md`, `PLAN.md`, `DECISIONS.md` (D-001 to D-038) | written and fact-checked; Neel's review pending |

## 2. Data and their status

| Data | Status | Inspected? | Integrity |
|---|---|---|---|
| Pilot 1 (campaign `pilot`, 2026-09-13, commit `d323afa`) | **exploratory**, sealed | yes, fully | 2026-09-16 check: every raw, workspace and run-scratch file matches `ARCHIVE_MANIFEST.sha256`; no new files. Local archive verified by full extraction on 2026-09-13. |
| Pilot 1 derived reanalysis (`results/derived/pilot/`) | exploratory | yes | derived from sealed data only |
| Smoke and validation checks of RS, LTS, WB, HH (2026-09-15) | infrastructure checks, not study data | reference-level output only | scratch (`work/smoke/`) |
| Earlier curation of candidate models (Prinz, Smith, Migliore, Solinas, Pinsky–Rinzel) | infrastructure checks | **reference-level** harness runs and plots only; no mutant was run | `docs/m0_evidence/model_curation/` |
| Pilot 2 (`pilot-v2`) | not run | no | – |
| Held-out split | **not assigned** (`data/splits/heldout/` has only a README) | **no held-out outcome has ever been generated or accessed**; `HeldoutGate` has never been opened; no `results/heldout_access.log` exists | – |

**Overwrites.** Raw results are write-once (`provenance.write_immutable`). The integrity check
above found no overwritten file.

**Leakage.** None: no held-out assignment exists. The candidate models whose *reference*
behaviour was inspected during curation have had no mutation outcomes generated, so they remain
eligible for an untouched evaluation split. This is disclosed as "reference behaviour inspected
during curation", not as "unseen".

## 3. Status of existing results

- **Exploratory:** Pilot 1 and its reanalysis; any Pilot 2 data when generated.
- **Confirmatory:** none.
- **Status-uncertain:** none.
- **Pilot 1 reporting.** Only in corrected form (D-038): 22 real model edits, all detected by the
  canonical test, 19 by the battery, no hidden semantic drift. The three earlier "silent" cases
  were numerical stress tests.

## 4. Reusable, needing repair, obsolete, conflicting

| Item | Assessment |
|---|---|
| Core pipeline, validation, features, mutations, selection, analysis | reuse |
| `docs/pilot/pilot_interpretation.md` | obsolete interpretation; kept as a record, marked superseded |
| Run record | extended in this build to the plan's field list (section 7) |
| Tool-failure runs | repaired in this build: an infrastructure failure no longer blocks a legitimate retry |
| Wang–Buzsáki model | fails NeuroML schema validation of its own cell file; excluded under the plan's inclusion criterion "passes appropriate NeuroML validation" unless Neel chooses otherwise (`docs/DECISIONS_REQUIRED.md`) |
| Code licence | `LICENSE` is BSD-3-Clause (D-018); the plan asks for Apache-2.0 provisionally. Recorded in `docs/DEVIATION_LOG.md`. |
| Repository layout | differs from the plan's recommended tree; equivalences in `docs/SPECIFICATION_GAP_ANALYSIS.md` |
| Model count | 6 manifest models, 7+ candidates; the plan and spec need 12-16 models from distinct sources. More curation is needed (`docs/MODEL_CURATION_REPORT.md`). |

## 5. Names

- **NeuroSem.** Appears about 4,300 times: historical documents, evidence, result records,
  feature-source labels such as `neurosem:firing_regime`, and environment variables `NEUROSEM_*`.
  - Kept where changing it would alter recorded provenance or hashed configs.
  - `NEURAXIS_*` environment variables now take precedence.
- **PerturbPrint.** 6 files; it was an earlier naming recommendation.
- **Neuraxis.** The current, provisional name, pending `docs/NAME_AUDIT.md`.

## 6. Decisions requiring human approval

See `docs/DECISIONS_REQUIRED.md`.

## 7. Changes made by this build (2026-09-16)

See `CHANGELOG.md` ("Neuraxis execution-plan build") and `docs/SPECIFICATION_GAP_ANALYSIS.md`.
