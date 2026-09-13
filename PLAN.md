# NeuroSem implementation plan (Milestones 0-10)

| | |
|---|---|
| Document | Milestone 0 deliverable `PLAN.md` (handoff "Initial Claude prompt", item 8: "Convert the milestones into an incremental implementation plan with exit tests"; item 9: decisions list) |
| Date | 2026-09-13 |
| Authority | `docs/handoff/NEUROSEM_FINAL_SPEC.pdf` (text in `NEUROSEM_FINAL_SPEC.extracted.md`) supersedes the handoff (D-002) |
| Repository state | Branch `m0-audit`, HEAD `d323afa`. No Git remote. Uncommitted at the time of writing: `DECISIONS.md` (D-023) and `CHANGELOG.md` are modified; `DEPENDENCY_AUDIT.md`, `LICENSE_AUDIT.md`, `docs/NAME_CONFLICT_AUDIT.md` and four round-2 prior-art evidence files are untracked. Nothing under `results/` is tracked. |
| Roles | Neel Gurram is the author and makes every scientific and outward-facing decision. Claude Code built the software and wrote this plan. |
| Running now | The Milestone 6 pilot, `neurosem pilot --campaign pilot`, started 2026-09-13T17:11:01Z at `d323afa` (`work/logs/pilot_run.log`). **Running; results pending.** Nothing in this plan interprets its partial output. |
| Results | No study results exist. Nothing here is a finding or a novelty claim. |

## In plain English

- NeuroSem asks one question: does an edited neuron model still behave like the original?
- Most of the machinery is built and tested on this laptop.
- The first real test run, the pilot, is running now. We do not know its outcome yet.
- The pilot decides whether the project continues. If edits never hide behaviour changes, we do not invent them.
- Some checks only a human can do. Example: reading at least 20 generated mutants and confirming each label.
- Some steps are locked on purpose. The final study, the held-out test and the AI-agent trials wait for Neel.
- Think of an exam. The answer key (held-out data) stays sealed until the rules are written down and signed (preregistration and `configs/FROZEN.lock`).
- The project name "NeuroSem" clashes with other projects. Neel should choose a name before anything goes public.
- The list of decisions for Neel is near the end of this file.

## Status labels

| Label | Meaning |
|---|---|
| done | All deliverables exist and the exit test passed. |
| done except human step | Everything automatic is in place; the exit test needs a human check. |
| in progress | Some deliverables or checks are still missing. |
| blocked on decision | Work cannot finish until Neel decides something. |
| gated by design | Deliberately not started until an earlier gate is passed (D-003). |
| not started | No work yet. |

## Summary

| Milestone | Status (verified 2026-09-13) | Main thing missing |
|---|---|---|
| M0 Audit | in progress | `PRIOR_ART_AUDIT.md`, `docs/novelty_matrix.csv`, `RISK_REGISTER.md`, `REQUIREMENTS.md`; audits uncommitted; Neel's review |
| M1 Environment | in progress (CI part blocked on N-01) | Docker never built, CI never run, clean-install exit command never run and logged |
| M2 Reference pipeline | in progress | inspection plots of reference traces |
| M3 Protocol engine | in progress | visual verification plots |
| M4 Mutation engine | done except human step | manual audit of >= 20 mutants (sheet written when the pilot ends) |
| M5 Fingerprints | in progress | exit check needs pilot outputs; tolerance constants provisional (N-03) |
| M6 Pilot decision | done except human step | pilot completed 2026-09-13 18:55 UTC (`results/processed/pilot/pilot_report.md`); formal criteria met, but silent mutants are numerical-only (`docs/pilot/pilot_interpretation.md`); Neel's go/no-go pending (DECISIONS N-13) |
| M7 Selection and holdouts | blocked on decision | held-out split (N-02), model set (N-09); splits provisional and unfrozen |
| M8 Frozen full study | gated by design | preregistration, `configs/FROZEN.lock`, 12-16 models |
| M9 Agent study | gated by design | harness built; no trials; hidden-evaluator review (N-12) |
| M10 Release and manuscript | not started | public repository, name, licensing, manuscript |

---

## Milestone 0: Audit

**Deliverables (spec).** Dependency and version audit; license audit; name-conflict search; prior-art matrix; risk register; decision log. Stop and request approval.
The handoff's initial prompt also asks for `PLAN.md`, `REQUIREMENTS.md`, `PRIOR_ART_AUDIT.md`, `docs/novelty_matrix.csv`, `RISK_REGISTER.md`, `CHANGELOG.md` and `AI_USE_LOG.md`, and lists nine M0 items:

| Handoff M0 item | Where it stands |
|---|---|
| 1. Separate reused from new functionality | `DEPENDENCY_AUDIT.md` section 5 (see "Separation" below) |
| 2. Verify NeuroML, LEMS, pyNeuroML, jNeuroML, OMV, SciUnit/NeuronUnit, eFEL from primary sources | `DEPENDENCY_AUDIT.md`; `docs/m0_evidence/tools/*.research.json` with `*.verify.json` |
| 3. Name conflicts | `docs/NAME_CONFLICT_AUDIT.md`; `docs/m0_evidence/names/` |
| 4. Prior-art sweep and novelty matrix | Evidence only: `docs/m0_evidence/prior_art/` (11 finder files, 46 round-1 and 6 round-2 deep-read files, `critic_r2.json`). **`PRIOR_ART_AUDIT.md` and `docs/novelty_matrix.csv` do not exist.** |
| 5. Outdated, uncertain, infeasible or weak assumptions | Evidence only: `docs/m0_evidence/critique/` (five lenses, each with a skeptic verdict). Cited in the audits, **not compiled into one document**. |
| 6. Two fixtures, provenance and license verified before download | `docs/m0_evidence/fixtures/`, `docs/model_selection.md`; "Fixture models" below |
| 7. Exact environment setup commands | `docs/REPRODUCING.md`, `DEPENDENCY_AUDIT.md` section 6 |
| 8. Milestones as a plan with exit tests | this file |
| 9. Every decision needing Neel's approval | `DECISIONS.md` and "Decisions requiring Neel's approval" below |

**Exit tests.**
1. Every file named above exists: `ls PLAN.md REQUIREMENTS.md PRIOR_ART_AUDIT.md docs/novelty_matrix.csv DEPENDENCY_AUDIT.md LICENSE_AUDIT.md RISK_REGISTER.md DECISIONS.md CHANGELOG.md AI_USE_LOG.md docs/NAME_CONFLICT_AUDIT.md`.
2. `docs/novelty_matrix.csv` has the spec's columns (citation, year, model type, mutations, multiple stimuli, electrophysiology features, protocol optimisation, held-out evaluation, AI transformations, software availability, distinction from NeuroSem), with a URL per row.
3. Neel spot-checks the closest-prior-work citations (required by `AI_USE_LOG.md` Entry 001).
4. The audits are committed, and Neel's approval is recorded in `DECISIONS.md`.

**Status: in progress.**
- Done: `DECISIONS.md`, `CHANGELOG.md`, `AI_USE_LOG.md` (commits `4e1acd5`, `4b9b7bd`, later edits).
- Written but uncommitted: `DEPENDENCY_AUDIT.md`, `LICENSE_AUDIT.md`, `docs/NAME_CONFLICT_AUDIT.md`.
- Missing: `PRIOR_ART_AUDIT.md`, `docs/novelty_matrix.csv`, `RISK_REGISTER.md`, `REQUIREMENTS.md`.
- The M0 approval stop: Neel's instruction "keep going, and build out the entire thing" was taken as approval to build M1-M7, with integrity gates kept (D-003). The M0 documents themselves have not been reviewed.
- Two documents already point to files that do not exist yet: `AI_USE_LOG.md` refers to `PRIOR_ART_AUDIT.md` and `docs/novelty_matrix.csv`.

**Evidence.** `docs/m0_evidence/{tools,environment,fixtures,names,prior_art,critique,model_curation}/`; `docs/handoff/`; the files above.

**Next actions.**
1. Write `PRIOR_ART_AUDIT.md` and `docs/novelty_matrix.csv` from the saved prior-art evidence. Do not claim novelty; "absence from a search is not proof" (spec).
2. Write `RISK_REGISTER.md` from the upheld or softened critique issues (`docs/m0_evidence/critique/*.skeptic.json`), plus the risks in the spec's "Failure and pivot criteria".
3. Write `REQUIREMENTS.md` (spec requirements traced to code and tests).
4. Commit the audits and this plan. Neel reviews and records approval.

## Milestone 1: Environment

**Deliverables (spec).** Python package; frozen dependencies; jNeuroML execution; eFEL installation; Docker environment; continuous integration; two tiny fixture models.

**Exit test (spec).** One command validates and simulates both fixture models on a clean installation. Concretely:
1. Fresh CPython 3.12 venv, then install from the lock (`docs/REPRODUCING.md`); `python -m pip check` and the lock comparison exit 0.
2. `neurosem smoke --models pospischil2008_rs pospischil2008_lts` exits 0. It validates each model, runs its shipped harness, finds rheobase and runs the batched battery (`scripts/smoke_jnml.py`). Save the output log.
3. The same test inside the Docker image, and in CI on `ubuntu-latest`.

**Status: in progress; the CI part is blocked on decision N-01.**

| Deliverable | State | Evidence |
|---|---|---|
| Python package | built | `pyproject.toml`, `src/neurosem/`, editable install `neurosem 0.1.0.dev0` |
| Frozen dependencies | built; fresh Windows install verified | `requirements.lock` (75 pins); `docs/REPRODUCING.md` verification table |
| jNeuroML execution | works on this machine | `src/neurosem/simulators/jneuroml.py`; jNeuroML 0.14.0 / jLEMS 0.12.0, Temurin 21.0.12.1+1 in `.tools/` (D-004, D-005); `tests/integration/test_jneuroml_adapter.py` |
| eFEL | installed and version-guarded | eFEL 5.7.34; `configs/features.yaml` pins it |
| Docker | **written, never built** (Docker is not installed; this is Windows 11 Home) | `Dockerfile`; build context only emulated |
| CI | **written, never run** (no GitHub remote) | `.github/workflows/ci.yml` |
| Two fixtures | fetched, commit-pinned, hash-verified | `models/raw/PospischilEtAl2008@049081c3/`, `data/model_manifest.csv` |

- The clean-install exit command has **not** been run and logged. `neurosem validate-models --models pospischil2008_rs` ran once in the emulated Docker context (`docs/REPRODUCING.md`). `work/smoke/` holds RS and LTS scratch folders from a smoke run, but no log was saved.
- `Makefile` and `environment.yml` were never executed (make and conda are not installed).
- Stale text: the Dockerfile "PROVENANCE GAP" comment and the matching `docs/REPRODUCING.md` warning predate `d323afa`, which added the `NEUROSEM_GIT_COMMIT` fallback (`DEPENDENCY_AUDIT.md` section 6.4).

**Next actions.**
1. Run exit steps 1-2 in a fresh venv and keep the log (after the pilot finishes, so the two runs do not compete for the CPU).
2. Neel decides N-01 (GitHub repository) and the Linux reference platform (P-10 below). Then run CI and the Docker build there.
3. Correct the stale provenance-gap text.

## Milestone 2: Reference pipeline

**Deliverables (spec).** Trace format; provenance records; feature extraction; deterministic rerun test; basic plots for manual inspection.

**Exit test (spec).** Repeated runs give the same conclusions within a predeclared numerical tolerance. Concretely:
1. `neurosem run-reference --campaign <c>` writes `results/processed/<c>/references/<model>/determinism.json` with `bitwise_identical_battery_traces: true` for every reference model.
2. Unit tests for the storage format and provenance pass: `.venv/Scripts/python -m pytest -q tests/unit/test_trace_metrics.py tests/unit/test_provenance.py tests/integration/test_run_recorder.py`.
3. A reference-trace plot for every (model, protocol) exists, and Neel has looked at it.

**Status: in progress.**
- Trace format: float32 mV on a verified uniform grid, byte-deterministic packing (D-012; `features/trace_metrics.py`).
- Provenance: content-addressed `run_id`, write-once `run.json` and feature JSON, environment digest, Git state with the D-023 dirty rule (`provenance.py`, `validation/execution.py`).
- Features: `features/efel_adapter.py` (D-016).
- Determinism: `results/processed/pilot/references/pospischil2008_rs/determinism.json` and `.../pospischil2008_lts/determinism.json` both record `bitwise_identical_battery_traces: true`, with five replicate and five base run ids each. `work/logs/pilot_reference.log` lists the same run ids. Scope: same machine, same JRE. Bitwise identity across JVMs or CPUs is not expected ([C:NUM-08]).
- **Inspection plots: none found.** `analysis/figures.py` has the eight manuscript figures (fig1 and fig7 draw trace pairs), but no command produces per-protocol reference-trace plots, and no such plot exists in `results/` or `docs/`. The PNGs in `docs/m0_evidence/model_curation/figures/` are candidate-screening plots; those in `work/tmp/analysis/` are development artefacts.
- Records: D-012 says `run.json` and feature files are tracked in Git, but no file under `results/` is tracked yet (`git ls-files results` returns 0).

**Next actions.**
1. Add a small plotting step for reference traces per protocol and level (h, h/2, h/4), and have Neel inspect it.
2. Commit the reference run records after the pilot, as D-012 intends.

## Milestone 3: Protocol engine

**Deliverables (spec).** Weak and strong steps; rheobase search; long step; ramp; hyperpolarisation and rebound.

**Exit test (spec).** Protocol timing and current amplitudes are independently tested and visually verified. Concretely:
1. `.venv/Scripts/python -m pytest -q tests/unit/test_protocol_definitions.py tests/unit/test_generate_xml.py tests/unit/test_rheobase_search.py tests/integration/test_probe_battery.py` passes.
2. For each pilot model, one plot per protocol shows the injected current and the voltage response on a shared time axis, and Neel signs it off.

**Status: in progress.**
- Implemented: P01-P10 (baseline, weak step, rheobase, 2x step, long step, ramp, hyperpolarising step, rebound, short pulse, paired pulses). P11 chirp and P12 frozen noise raise "not implemented" by design (spec: only if stable, or later). Code: `protocols/definitions.py`, `protocols/generate.py`, `protocols/rheobase.py`.
- Independent tests exist: integer-millisecond edges on every refinement grid, windows, linear amplitude scaling with rheobase, schema-valid generated XML, and on real jLEMS runs the exact pulse onset, ramp onset, paired-pulse timing, deflection sign and release repolarisation (`tests/integration/test_probe_battery.py`). The battery test uses an assumed 0.1 nA rheobase at dt 0.025 ms, so it checks timing, not firing (`docs/build_notes/core.md`).
- **Visual verification: not done.** No plotting code exists in `src/neurosem/protocols`, `src/neurosem/validation`, `scripts/` or `tests/`.
- Known open issue (N-07): on LTS (rheobase about 0.039 nA) the short pulses and the ramp evoke no spikes, and the rebound protocol showed no rebound depolarisation in a smoke run (D-010).

**Next actions.** Produce the plots in exit test 2. Neel reviews them together with N-07, using discovery data only.

## Milestone 4: Mutation engine

**Deliverables (spec).** Three pilot mutation families; one-change-per-mutant enforcement; machine-readable provenance; structural-validity and execution classification.

**Exit test (spec).** At least 20 manually audited mutants match their labels. Concretely:
1. `.venv/Scripts/python -m pytest -q tests/unit/test_mutation_operators.py tests/unit/test_mutations_base.py tests/integration/test_mutants_validate.py` passes.
2. When the pilot finishes, `results/processed/pilot/mutant_audit_sheet.csv` exists. Its columns `human_auditor`, `edit_matches_label (yes/no)`, `class_plausible (yes/no)` and `notes` are blank until a human fills them.
3. Neel fills at least 20 rows (sampled across operators and both models, sampling rule recorded), every audited row says `yes` or has a note, and the completed sheet is committed.

**Status: done except human step.**
- 19 operators in 4 families (stimulus, biophysical, reference, numerical). The pilot uses biophysical, reference and numerical (`configs/study.yaml`; stimulus is excluded from the pilot, D-009).
- One-change enforcement: `enforce_single_operator` plus per-operator `check_record`, with tamper tests (`docs/build_notes/mutations.md` section 1.3).
- Provenance: `variant.json` per variant and `mutation_manifest.csv` per campaign.
- Classification: six classes in `validation/fingerprint.py`; relative structural oracle (D-006); instability rule (D-020).
- The audit sheet is written by `experiments/campaign.py` at the end of the pilot. It does not exist yet.
- Audit tip: check the `edits` column or `variant.json`, not `git diff`. lxml re-serialisation is not byte-minimal (`docs/build_notes/mutations.md` section 4).

**Next actions.** Wait for the pilot. Neel audits at least 20 mutants and records the result.

## Milestone 5: Fingerprints

**Deliverables (spec).** eFEL adapter; trace metrics; convergence calibration; per-mutant diagnostic reports; detection matrix.

**Exit test (spec).** Every detected mutant is linked to the protocol, feature, threshold and evidence trace that caused detection. Concretely:
1. `.venv/Scripts/python -m pytest -q tests/unit/test_efel_adapter.py tests/unit/test_trace_metrics.py tests/unit/test_regimes.py tests/unit/test_convergence_fingerprint.py tests/unit/test_selection_matrix.py tests/integration/test_features_real_trace.py` passes.
2. After the pilot, every mutant with a detection has `results/processed/pilot/variants/<variant_id>/diagnostic.md` naming protocol, feature, tolerance and evidence run ids, and `detection_matrix.csv` agrees with `detections.csv`.
3. Neel hand-checks a random sample of detections against the evidence trace and the recorded tolerance ([C:INTEG-08]).

**Status: in progress.**
- Built: `features/efel_adapter.py`, `features/trace_metrics.py`, `features/regimes.py`, `validation/convergence.py` (h, h/2, h/4; D-013, D-014), `validation/fingerprint.py`, `selection/matrix.py`, and the diagnostic writer `experiments/campaign.py::_write_diagnostic`.
- Exit checks 2-3 depend on the running pilot.
- Tolerance constants (starting floors, c = 3) are provisional (N-03).

**Next actions.** After the pilot: run exit check 2, then Neel's sample check. Neel decides N-03 from `tolerances.csv` before anything is frozen.

## Milestone 6: Pilot decision

**Deliverables (spec).** Run 2-6 models and 20-60 mutants. Continue only if canonical testing misses some reproducible non-equivalent mutants and additional protocols detect them without unacceptable false positives. If no hidden drift exists, do not manufacture it: reframe as an evaluation of existing validation, or stop.

**Exit test.**
1. `neurosem pilot --campaign pilot` exits 0 and writes `results/processed/pilot/pilot_report.md`. The report checks the spec's three pilot criteria: (1) at least one silent mutant, detected reproducibly by a non-canonical protocol; (2) deterministic reruns and fewer than 25% of tolerance entries excluded under refinement; (3) at most 10% false positives on valid transformations. The two thresholds are provisional (N-04; `experiments/pilot.py`).
2. The report states a mutant count within 20-60, or the deviation is recorded.
3. Neel reviews the report, the audit sheet (M4), the diagnostics of any silent mutants (M5) and `tolerances.csv`, then records a continue / reframe / stop decision in `DECISIONS.md`.

**Status: in progress. The pilot is running; results pending.**
- Started 2026-09-13T17:11:01Z at `d323afa`; a `neurosem` Python process and jLEMS Java processes were active at 18:44Z.
- Configuration: models `pospischil2008_rs` and `pospischil2008_lts`; families biophysical, reference, numerical; 2 sites per operator; 1 site per transform operator; seed 20260913; nominal dt 0.005 ms (`configs/study.yaml`).
- Scope note for Neel: the spec's pilot table names 4 protocols and 3-5 features. The pilot runs the full implemented battery (P01-P10 plus the canonical harness and rheobase) with the configured feature set. That is a larger pilot than the table, and it should be stated in the preregistration's "data already seen" section.
- Evidence so far: `work/logs/pilot_run.log`, `work/logs/pilot_commit.txt`. No partial output is interpreted here.

**Next actions.**
1. Do not edit simulation-relevant paths (`src`, `configs`, `data`, `models`, `scripts`, `workflows`, `pyproject.toml`, `requirements.lock`) while it runs. Otherwise later runs are marked dirty (D-023). Documentation edits are safe.
2. When it ends, run exit steps 2-3.
3. Neel decides N-03, N-04 and N-07 with the pilot evidence, before any freeze.
4. Keep valid transformations in the false-positive denominator whatever the battery says about them (P-06).

## Milestone 7: Selection and holdouts

**Deliverables (spec).** Frozen discovery and held-out splits; greedy coverage selection; random cost-matched baselines; leakage tests.

**Exit test (spec).** Selection code cannot access held-out labels. Concretely:
1. `.venv/Scripts/python -m pytest -q tests/unit/test_splits_leakage.py tests/unit/test_greedy_selection.py tests/unit/test_selection_matrix.py` passes. It includes a dynamic test that fails on any open, stat or listing of `data/splits/heldout/` during discovery selection, static confinement tests, `filter_matrix` refusal of non-discovery rows, and `HeldoutGate` refusal without a matching lock.
2. `data/splits/heldout/heldout_models.txt` and `heldout_families.txt` exist, and `python scripts/freeze_splits.py` exits 0 and writes `data/splits/SPLITS.sha256`. The split files and hash file are committed together.
3. `neurosem select-protocols --campaign <c> --budget <k>` runs on the discovery split only.

**Status: blocked on decision (N-02, N-09). Code is built; splits are provisional and unfrozen.**
- Built: `selection/greedy.py` (greedy maximum coverage with a recorded `shortfall`, count- and runtime-matched random baselines, optional cost-sensitive variant), `selection/matrix.py`, `selection/splits.py` (`discovery_view`, `HeldoutGate`), `scripts/freeze_splits.py`.
- Splits: `data/splits/discovery_models.txt` lists the two pilot models; `discovery_families.txt` lists biophysical, reference, numerical. `data/splits/heldout/` contains only a README. There is no `SPLITS.sha256`.
- The spec asks for 8-10 discovery and 4-6 held-out models. The manifest has 6 rows (2 included) in 3 source families. `data/model_candidates.csv` adds 7 candidates from 4 further families (`docs/model_curation_candidates.md`), none included.

**Next actions.**
1. Wait for the M6 decision.
2. Neel chooses the model set (N-09) and the held-out models and at least one held-out family (N-02). Held-out models should not share a source family with discovery models.
3. Write the held-out files, freeze with `scripts/freeze_splits.py`, commit.

## Milestone 8: Frozen full study

**Deliverables (spec).** Preregistration; frozen configurations and hashes; full execution logs; statistical analysis; robustness and ablation analyses.

**Exit tests.**
1. The preregistration is registered with a timestamp in the registry Neel chooses. Every `[NEEL DECISION REQUIRED]` field in `docs/preregistration_draft.md` (on 85 lines today, counted with `grep -c`) is filled by Neel.
2. `configs/FROZEN.lock` exists at exactly that path, in `sha256  path` format, covering `data/splits/SPLITS.sha256`, `configs/study.yaml` and every other `configs/*.yaml`. All hashes match. `configs/study.yaml` says `status: frozen`, if P-09 adds that rule.
3. `neurosem evaluate-heldout --campaign <c> --selection <frozen selection JSON> --reason "<reason>"` opens the gate once and appends to `results/heldout_access.log`.
4. `neurosem analyze --campaign <c>` and `neurosem reproduce-paper --campaign <c>` rebuild every table and figure from raw and processed results.

**Status: gated by design (D-003).**
- Exists: `docs/preregistration_draft.md` (draft), `docs/statistical_plan.md` (draft), `analysis/metrics.py`, `analysis/bootstrap.py` (cluster bootstrap, exact McNemar, cluster sign-flip), `experiments/heldout.py`, `experiments/analyze.py` (tolerance sensitivity).
- Absent: `configs/FROZEN.lock`, a registered preregistration, full-study runs. `configs/study.yaml` says `status: provisional`.

**Next actions.** Only after M6 "continue" and M7's frozen split: curate 12-16 models, fill the preregistration, freeze, then run once.

## Milestone 9: Agent study

**Deliverables (spec).** Frozen prompts; isolated Claude Code trials; raw transcripts and patches where redistribution is permitted; hidden evaluation results; manual patch audit.

**Exit tests.**
1. Neel's review (and ideally independent revision) of every hidden evaluator spec is recorded (N-12). `sha256sum -c agent_study/HIDDEN_MANIFEST.sha256` passes.
2. A frozen agent configuration with `provisional: false` exists, recording policy, task, prompt, public-test and hidden-spec hashes (`experiments/agent.py::freeze_hashes`).
3. Each trial runs in an isolated environment started from the same clean commit, and `neurosem evaluate-agent --task <task> --trial-dir <dir> --frozen-config <file>` scores it.
4. Every patch is audited by hand after scoring. Transcripts, patches, costs and versions are logged under `results/agent_study/`.

**Status: gated by design. The harness is built; no trials exist.**
- Built: nine task definitions `agent_study/tasks/t01-t09`, the shared public runner, hidden evaluator specs in `agent_study/hidden/` (Git-ignored; hashes committed, D-022), `configs/agent_policy.yaml` (provisional), `docs/agent_study_protocol.md`, `src/neurosem/experiments/agent.py`, `tests/unit/test_agent_harness.py`.
- `results/agent_study/` does not exist.
- D-003: the assistant that built the evaluators does not run the trials.
- Nine tasks are one per task type, not a sample. The spec plans 20-30 tasks.

**Next actions.** After M8 is frozen: Neel reviews the hidden specs (N-12) and the provisional agent values (P-01), and decides whether M9 runs at all.

## Milestone 10: Release and manuscript

**Deliverables (spec).** Public repository; versioned release; DOI-minting archive; reproduction guide; manuscript and supplement; data, code and AI-use statements; IEEE formatting only after choosing a venue.

**Exit tests.** The public repository exists under the chosen name; a tagged release has a DOI; `neurosem reproduce-paper` regenerates every table and figure from the archive on the reference platform; the manuscript and supplement exist; the licensing checklist (L-01 to L-11) is closed.

**Status: not started.**
- Groundwork only: `CITATION.cff` (validated against CFF 1.2.0), `docs/REPRODUCING.md` (environment only), `docs/ai_disclosure.md`.
- No `manuscript/` directory, no remote, no release.
- The spec's repository tree also lists `tests/regression/`, `tests/fixtures/`, `results/tables/` and `results/figures/`; these do not exist yet.

**Next actions.** None before M8. Settle the name (N-10) and licensing (N-05, L-01 to L-11) well before release.

---

## Separation of reused and new functionality

The full table is in `DEPENDENCY_AUDIT.md` section 5. In short:
- **Reused, not claimed as new:** NeuroML v2 and LEMS; `jnml -validate` and jLEMS simulation in the jNeuroML jar; libNeuroML validation; eFEL feature algorithms; mutation testing, metamorphic testing, greedy set cover and standard statistics as general methods; GitHub Actions and Docker.
- **Code written for NeuroSem:** the relative structural oracle, the direct-jar adapter and status taxonomy, protocol generation and rheobase normalisation, the eFEL adapter with three feature states, tolerance calibration by refinement, single-fault NeuroML/LEMS mutation operators and valid transformations, fingerprints and the detection matrix, split and leakage barriers, and clustered statistics.
- "Written for NeuroSem" is not a novelty claim. Novelty is judged only by the prior-art audit, which is not written yet (M0).

## Fixture models

Spec M0 item 6. Details: `docs/model_selection.md`, `docs/m0_evidence/fixtures/fixture_candidates.json`, `fixture_verify.json`, D-017.

**Recommended pair (in use for the pilot).**

| | Pospischil 2008 RS | Pospischil 2008 LTS |
|---|---|---|
| Source | `OpenSourceBrain/PospischilEtAl2008` at commit `049081c39357d9e7c478b63ef7b10f374d1c50f4`, `NeuroML2/cells/RS/` | same commit, `NeuroML2/cells/LTS/` |
| Model | single compartment; Leak, Na, Kd, IM | single compartment; adds IT (T-type Ca) and a Ca pool |
| Expected behaviour (upstream, not NeuroSem) | adapting spike train | early spike pair; rebound expected but unverified |
| License | MIT for the `NeuroML2/` files. The OMV `.mep` files in `NEURON_MODIFIED/` fall under a citation-only carve-out with no redistribution grant (L-05). | same |
| Citation | Pospischil et al. (2008), Biol Cybern 99:427-441; ModelDB 123623 (DOI checked in Crossref) | same |
| Verification | 38/38 SHA-256 values recomputed; upstream OMV CI run 30447139603 passed its jNeuroML jobs at the pinned commit | same |
| Caveats | none specific | libNeuroML 0.6.7 strict validation rejects the custom `IT_s_gate` while `jnml -validate` accepts the cell, so jnml is the structural oracle (D-006). PyLEMS 0.6.9 cannot run it, so there is no Java-free path. |

**Backups.**
- Pospischil 2008 FS (same commit; tonic; includes IM without an IM density).
- NeuroML2 `NML2_SingleCompHHCell` with `LEMS_NML2_Ex5_DetCell.xml` (`NeuroML/NeuroML2` at `a5f5dadc`; LGPL-3.0; independent source). This is also the alternative to LTS if strict pure-Python validity is required; it loses the T-current behaviour.
- Wang-Buzsaki 1996 `wb1` (`OpenSourceBrain/WangBuzsaki1996` at `c5322844`; MIT for the NeuroML2 directory). Its shipped stimulus starts at 0 ms, so the canonical window has no baseline.
- Pospischil 2008 IB (same commit). Its shipped step outlasts the 1000 ms run.

**Correlation caveat.** RS and LTS come from one paper, one repository and one commit, and share byte-identical Na, Kd, IM and Leak channel files. They are one independent source. That is acceptable for a pipeline pilot, not for held-out generalisation: a Pospischil cell in the held-out set is not an unseen model while another Pospischil cell is in discovery (`docs/model_selection.md` section 5). No current manifest model contains an Ih channel, so sag is expected to carry little information (`docs/model_selection.md` section 7).

## Environment setup

- Exact commands, and what was and was not verified on each route: `docs/REPRODUCING.md`.
- Versions, pitfalls, lock regeneration and evidence: `DEPENDENCY_AUDIT.md` sections 2, 6 and 7.
- The verified route is Windows 11 with CPython 3.12.10 and a portable Temurin JDK. Linux, Docker, CI, make and conda are written down but not run.

Windows sequence (from `docs/REPRODUCING.md`):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install pip==26.2.1
.\.venv\Scripts\python -m pip install -r requirements.lock
.\.venv\Scripts\python -m pip install --no-deps -e .
.\.venv\Scripts\python -m pip check
.\.venv\Scripts\python scripts\bootstrap_java.py --release jdk-21.0.12.1+1 --expect-sha256 f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e
.\.venv\Scripts\python -m pytest -q -m "not jnml"
.\.venv\Scripts\python -m pytest -q
```

Latest recorded full suite: `work/logs/full_suite_3.log`, "979 passed, 1 skipped". `CHANGELOG.md` ties that count to commit `3cdb957`. After `d323afa`, `work/logs/prov_test.log` shows 26 passed (provenance tests only). The full suite has not been re-run at `d323afa`. `work/` is Git-ignored, so these logs are local.

## How to run

Every subcommand below was checked with `C:/Users/gurra/NeuroSem/.venv/Scripts/neurosem --help` and `<subcommand> --help` on 2026-09-13. Most take `--campaign <name>` (results go to `results/processed/<name>/`) and `--workers <n>`. `--models` defaults to the pilot models in `configs/study.yaml`.

| Step | Command | Notes |
|---|---|---|
| Fetch pinned models | `neurosem fetch-models [--dest models/raw]` | commit-pinned, hash-checked |
| Validate | `neurosem validate-models [--models ...]` | with no `--models`, validates manifest rows marked include or candidate |
| Smoke check (M1 exit) | `neurosem smoke [--models ...]` | validate, harness run, rheobase, battery |
| References | `neurosem run-reference --campaign <c> [--models ...]` | h, h/2, h/4 and determinism |
| Tolerances | `neurosem calibrate-tolerances --campaign <c> [--models ...]` | |
| Mutants and transforms | `neurosem generate-mutants --campaign <c> [--models ...] [--families ...] [--n-mutants N] [--n-transforms N] [--seed S]` | `--n-mutants` is sites per operator |
| Classify | `neurosem classify-mutants --campaign <c> [--models ...]` | `build-fingerprints` has identical help text ("fingerprint, compare and classify generated variants") and the same options |
| Pilot (M6) | `neurosem pilot --campaign pilot [--models ...] [--seed S] [--n-mutants N] [--n-transforms N]` | end to end; writes `pilot_report.md` |
| Select protocols | `neurosem select-protocols --campaign <c> [--budget K] [--draws D] [--seed S]` | discovery split only |
| Held-out (gated) | `neurosem evaluate-heldout --campaign <c> --selection <frozen selection JSON> --reason "<text>"` | refuses without a matching `configs/FROZEN.lock`; logs every access |
| Agent scoring (gated) | `neurosem evaluate-agent --task <id> --trial-dir <dir> --frozen-config <file>` | all three arguments required |
| Analysis | `neurosem analyze --campaign <c>` | reads processed results; do not run on a campaign that is still running |
| Reproduction | `neurosem reproduce-paper --campaign <c>` | |
| Freeze splits | `.venv/Scripts/python scripts/freeze_splits.py [--force-with-reason "..."]` | M7 |
| Tests | `.venv/Scripts/python -m pytest -q` (or `-m "not jnml"` for the fast subset) | |

`workflows/*.py` are thin wrappers around the same CLI commands. `Makefile` targets (`setup`, `java`, `test`, `test-fast`, `validate-models`, `pilot`, `reproduce-paper`, `docker-build`, `docker-test`, `lint`) exist but have never been executed.

## Order constraints

1. **Pilot decision before expansion.** No full-study curation, split freeze or selection freeze until Neel records the M6 decision.
2. **Preregistration and `configs/FROZEN.lock` before any held-out access.** Assign and freeze the split (`SPLITS.sha256`), register the preregistration, then write the lock. `HeldoutGate` enforces the lock in code; the preregistration step is procedural, and Neel must do it first. No held-out evaluation during development (D-003).
3. **Thresholds before held-out.** Tolerance constants, pilot-derived protocol amplitudes and analysis settings (N-03, N-07, P-07) are fixed before the lock and never tuned after held-out inspection. A forced re-freeze is logged and must be disclosed.
4. **Hidden-evaluator review before agent trials.** Neel reviews, and ideally revises independently, every hidden evaluator spec (N-12). NeuroSem and the protocol selection are frozen first. The assistant that built the evaluators does not run the trials (D-003).
5. **Rename decision before public release.** Decide N-10 before any public repository, package, DOI or manuscript. Deciding before the frozen study is cheaper still, because raw results record the `neurosem` name in provenance and feature labels and must stay immutable (`docs/NAME_CONFLICT_AUDIT.md` section 7).
6. **Licensing before the first public push.** Settle N-01, N-05 and L-01, L-05, L-06 first. Fix licensing before any Zenodo deposit, because a withdrawn record keeps a tombstone.
7. **No simulation-relevant edits while a campaign runs** (D-023). Otherwise its later runs are marked dirty.

## Decisions requiring Neel's approval

### A. Open decisions in `DECISIONS.md`

| id | decision | current provisional choice |
|---|---|---|
| N-01 | Create a GitHub repository (private now, public at release)? | none created |
| N-02 | Discovery / held-out model split and held-out mutation family | pilot models are discovery only; no held-out assignment |
| N-03 | Final tolerance constants (`configs/tolerances.yaml`) after reviewing the pilot's `tolerances.csv` | starting floors, c = 3 |
| N-04 | Pilot decision thresholds | at most 25% of features excluded; at most 10% false positives (`experiments/pilot.py`) |
| N-05 | Code license; handling of LGPL model files if mutants are redistributed | BSD-3-Clause; LGPL files keep their license |
| N-06 | Canonical metric: shared features and tolerances, an OMV-style spike-time check, or both | shared features |
| N-07 | Protocol amplitudes for very-low-rheobase models (LTS short pulses, ramp, rebound) | keep for the pilot; revisit with discovery data before freezing |
| N-08 | Add NEURON as a cross-simulator? | deferred |
| N-09 | Accept correlated Pospischil cells in the full study; which curated candidates to add | see `docs/model_curation_candidates.md` |
| N-10 | Project name | rename before any public release; preferred PerturbPrint, runner-up DriftClamp |
| N-11 | Report the jNeuroML `channelDensityVShift` validator gap upstream? | not reported (outward-facing) |
| N-12 | Permanent home of the hidden agent-study evaluators, and whether Neel revises them independently | local only, Git-ignored, hashes committed |

### B. Raised in `LICENSE_AUDIT.md` section 11 (refinements of N-05; not yet separate entries in `DECISIONS.md`)

| id | decision | audit's recommendation (provisional) |
|---|---|---|
| L-01 | Code license | keep BSD-3-Clause |
| L-02 | Documentation license | CC-BY-4.0 for `docs/` |
| L-03 | License for generated data | state one explicitly (CC-BY-4.0 or CC0-1.0) |
| L-04 | LGPL mutants of `nml2_hh_example` | publish regeneration scripts and hashes, not files |
| L-05 | Five tracked carve-out `.mep` files (4 Pospischil, 1 Solinas) | remove from the public tree; reference by URL plus SHA-256 |
| L-06 | Add the GPL v3 text next to the NeuroML2 snapshot's `LICENSE.lesser` | add before any redistribution |
| L-07 | Publish a Docker image? | publish the Dockerfile only |
| L-08 | Per-file license metadata (REUSE, manifest column, CI lint) | adopt before public release |
| L-09 | Ask upstream maintainers about license discrepancies (outward-facing) | optional |
| L-10 | Prinz 2003 citation mismatch | cite both until checked |
| L-11 | Human licensing review before release | yes, before M10 |
| L-12 | OMV as a secondary baseline (links to N-06) | if added, record pyrx's GPLv2 license first |

### C. Raised in `docs/NAME_CONFLICT_AUDIT.md` (N-10 detail)

- Choose one: A. rename to PerturbPrint now (recommended); B. DriftClamp now; C. decide later, before public release; D. keep NeuroSem and accept conflicts C1-C3.
- Whatever the choice, re-check registries, GitHub, USPTO and the sources that failed (Semantic Scholar, Zenodo, OpenAlex, EUIPO, WIPO) just before release. The audit is not legal clearance.
- The audit's claim that a rename is "mechanical" is unverified. A trial rename in a scratch copy followed by the test suite would confirm it.

### D. Raised in build notes, `DEPENDENCY_AUDIT.md` and `docs/model_selection.md`, not yet in `DECISIONS.md`

The P-xx labels are local to this plan.

| id | decision | source |
|---|---|---|
| P-01 | Agent-study provisional values: budgets (80 turns, 60 min, 15 USD per trial), permissions, public spike-time tolerance 1.0 ms, t08 success threshold (at least 2x fewer integration steps), trials per task (9 definitions against 20-30 planned), and whether M9 runs at all | `docs/build_notes/agent-study.md`; preregistration S7 |
| P-02 | Whether the stimulus family enters the primary population or is reported separately; it can never be class 6 by construction | `docs/build_notes/science-docs.md` item 3; D-009 covers the pilot only |
| P-03 | Confirm the class for mutants whose shipped harness runs but whose battery fails to build (for example `omit_include` masked by the harness); currently class 2, flagged | `science-docs.md` item 4; D-020; preregistration draft |
| P-04 | `wrong_segment_group` on single-compartment cells: keep as a negative control or mark inapplicable | `science-docs.md` item 8; `mutations.md` section 2 |
| P-05 | Confirm the species split between `wrong_channel` (different ion species) and `wrong_compatible_component` (same species) | `mutations.md` section 2 |
| P-06 | Confirm the rule that valid transformations are never filtered on battery outcomes; otherwise the false-positive rate is zero by construction | `science-docs.md` item 7 |
| P-07 | Held-out bootstrap B, permutations and seed now come from `configs/study.yaml` `analysis` (10000 / 10000 / 20260913; read by `experiments/heldout.py`). Confirm the values and freeze them with the preregistration | `science-docs.md` item 10; DECISIONS D-021 |
| P-08 | Depolarisation-block voltage: one fixed -40 mV for all models, or per model / relative to threshold or rest | `docs/build_notes/features.md` |
| P-09 | Should `HeldoutGate` also require `status: frozen` in `configs/study.yaml`? | `docs/build_notes/selection.md` section 4 |
| P-10 | Reference platform for frozen-study data (WSL 2 Ubuntu, Docker on Linux, GitHub Linux runners, other). Docker Desktop's documented WSL 2 backend requirements do not list Windows 11 Home. | `DEPENDENCY_AUDIT.md` section 8; [C:NUM-07] |
| P-11 | Hashed universal lock file vs plain `pip freeze`; exact Temurin build in CI; Python 3.14 as a secondary CI job | `DEPENDENCY_AUDIT.md` section 8 |
| P-12 | Confirm greedy early stop with a recorded `shortfall` (rather than filling to k with zero-gain protocols) | `selection.md` section 3.1 |
| P-13 | Models without a shipped single-cell harness (Maex 1998 granule and Golgi): author a canonical harness as a preregistered deviation, or exclude them from the canonical comparison | `docs/build_notes/model-curation.md` section 5 |
| P-14 | Sag gap: keep searching for a licensed single-compartment Ih model, report sag as uninformative, or drop sag from the diversity goals | `docs/model_selection.md` section 7 |
| P-15 | Confirm `jnml -validate` (jNeuroML 0.14.0) as the structural oracle for the frozen study; add model-level simulator version and required-includes columns to the manifest, or rely on per-run records | `docs/model_selection.md` section 10 |

### E. Preregistration fields

`docs/preregistration_draft.md` has `[NEEL DECISION REQUIRED]` markers on 85 lines (`grep -c`): registry, frozen commit and hashes, budget k, effect size, inclusion rules, splits, protocol parameters, tolerance constants, statistical decision rule, handling of undefined features and crashes, sample-size rules, and others. Many overlap with the rows above. All must be filled by Neel before M8.
