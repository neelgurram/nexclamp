# Decision log

Each decision records what was decided, why, the evidence, and whether it is **provisional**
(may change before preregistration), **fixed**, or **awaiting Neel**. Decisions about
scientific ground truth, thresholds, exclusions and splits belong to Neel. Where Claude Code
made a working choice so that building could proceed, it is marked *provisional* and listed
again under "Decisions Neel must make".

## Process

**D-001 Separate repository, local Git, one branch per milestone** (fixed)
NeuroSem lives in `C:\Users\gurra\NeuroSem` and is not part of Continuum. The work is on branch `m0-audit`. No GitHub remote exists yet; creating one is outward-facing (see N-01).

**D-002 The final specification supersedes the handoff** (fixed)
`docs/handoff/NEUROSEM_FINAL_SPEC.pdf` (SHA-256 `2d1f6e51…0c09`) takes precedence over `NEUROSEM_CLAUDE_HANDOFF.pdf` where they differ.

**D-003 Approval to proceed past the Milestone 0 stop, with the integrity gates kept** (fixed)
On 2026-09-13 Neel instructed: "keep going, and build out the entire thing". Claude Code took this as approval to implement and test Milestones 1-7 and to run the Milestone 6 pilot on discovery models. These gates were kept because they protect scientific validity:
- no held-out evaluation;
- no frozen full study without Neel's preregistration;
- no agent-study trials run by the assistant that built the evaluator;
- no public release or DOI without Neel.

## Toolchain

**D-004 Pinned toolchain** (provisional until the frozen study)
- Python 3.12.10 in `.venv`.
- pyNeuroML 1.3.22, which bundles jNeuroML 0.14.0 and jLEMS 0.12.0 (as reported by `jnml -v`).
- libNeuroML 0.6.7 and eFEL 5.7.34.
- Eclipse Temurin JDK 21.0.12.1+1, a portable copy in `.tools/`.

The Temurin archive's SHA-256 (`f9d6e191…8b4e`) was verified against the Adoptium API before extraction. The jNeuroML jar has SHA-256 `45ee565a…b931`.

Evidence: `docs/m0_evidence/tools/*.json` and `.tools/jdk_provenance.json`. Note that the audit inferred jLEMS 0.11.1; the jar itself reports 0.12.0.

**D-005 Call the jNeuroML jar directly, not pyNeuroML's runner helpers** (fixed)
The audit found three problems with those helpers:
- they return a bare `False` both for an invalid model and for a missing Java;
- some paths call `sys.exit`;
- they build shell commands with a colon-joined include path, which is fragile on Windows.

`simulators/jneuroml.py` instead passes argument lists to the jar and classifies results as ok, invalid, build error, runtime error, timeout, numerically unstable, or tool failure.

## Validation design

**D-006 Relative structural oracle over the whole include closure** (provisional)
Two facts were verified on 2026-09-13:
1. `jnml -validate <cell>` does not schema-check the files the cell includes; a corrupted included channel file passed.
2. The upstream LTS `IT.channel.nml` and `Ca.nml` fail standalone validation by design (custom LEMS ComponentTypes). OMV itself validates only the cell and network files.

Rule adopted:
- A **reference** is valid when its cell file and harness network files validate. Other failures are recorded as baseline errors.
- A **variant** is valid when it meets the same requirement and introduces no validation error its reference did not already have.

libNeuroML strict validation is recorded for information only. See `validation/structural.py`.

**D-007 Nominal time step h = 0.005 ms, refined to h/2 and h/4** (provisional)
Pilot probe results (`docs/pilot/dt_probe.md`):
- jLEMS spike times converge at first order, consistent with forward Euler.
- h = 0.005 ms runs at about 15-35 µs per simulated cell-step.
- Some features are highly step-sensitive; the LTS third spike moves about 50 ms across the tested range.

**D-008 Canonical protocol = the model's shipped harness** (provisional)
The conventional regression test for an Open Source Brain NeuroML model reruns its shipped LEMS simulation. That simulation is analysed with the same features and calibrated tolerances as every NeuroSem protocol, so canonical and battery results differ only in the stimulus. The analysis window always comes from the reference harness. An OMV-style spike-time check is not the primary canonical metric (see N-06).

**D-009 What each mutation family edits** (provisional)
- **Stimulus mutations** edit only the shipped harness (the canonical test). By construction, the NeuroSem battery cannot see them. They act as a sensitivity control for the canonical layer and are excluded from the pilot families.
- **Biophysical and reference mutations** edit model files and affect every protocol.
- **Numerical mutations** edit both the harness (step, `<Meta>`) and the execution configuration used by every protocol. `recording_resolution` is a configuration-only change (post-hoc output sampling), because LEMS OutputFile has no recording interval.

**D-010 Rheobase normalisation and search** (provisional)
Depolarising and hyperpolarising amplitudes are multiples of the reference model's rheobase, defined as the first spiking amplitude of a 500 ms step. The search uses a 12-point grid over 4 refinement rounds (`protocols/rheobase.py`), with the search resolution recorded. Every variant of a model receives the reference's concrete stimuli.

Pilot smoke run observations, which Neel should review (see N-07):
- For the LTS cell (rheobase about 0.039 nA), the 3 ms pulses at 10× rheobase and the 0→3× ramp evoke no spikes.
- The −2× rebound protocol shows no rebound depolarisation.

**D-011 Batched probe simulations** (fixed)
All protocols for one variant run as uncoupled single-cell populations in one jLEMS process, grouped by total duration. This is valid because the cells are unconnected; each keeps its own inputs and its own output column.

**D-012 Content-addressed, immutable raw results** (fixed)
- `run_id` is a hash of every file the simulator reads, the execution settings, and the jar.
- Identical inputs are never simulated twice; for example, stimulus-only mutants reuse the reference battery.
- `run.json` and `features.json` are write-once and tracked in Git.
- Traces are stored as float32 mV on a verified-uniform grid. They are ignored by Git, but their hash is tracked. A missing trace is re-simulated and must reproduce its recorded hash.
- Features are always extracted from the stored trace representation.
- Rheobase searches store per-amplitude spike counts only.

**D-013 Non-equivalence must reproduce under refinement** (provisional)
A variant is non-equivalent only if the same (protocol, feature) is detected at both h and h/2. SILENT means non-equivalent through a battery protocol with no canonical detection at the nominal level.

**D-014 Features whose state changes under refinement are excluded, not dropped** (provisional)
If a reference feature's defined/undefined state, or its firing-regime label, differs between h and h/2, that (model, protocol, feature) is excluded from detection. The exclusion is recorded in `tolerances.csv` and counted in the pilot report.

**D-015 Protocol cost = simulated cell-steps** (provisional)
Runtime-matched baselines use simulated cell-steps as the cost, averaged across models; for rheobase this is the whole search. Cell-steps are simulator- and machine-independent. The measured wall time is recorded alongside for validation.

**D-016 Frozen eFEL feature variants** (provisional)
One eFEL variant is used per concept (see `configs/features.yaml`), for example `steady_state_voltage_stimend` (not `steady_state_voltage`, which measures after the stimulus), `spike_count_stimint`, `adaptation_index2` and `strict_burst_number`. Settings are `interp_step = 0.01 ms` and `strict_stiminterval = true`. Settings are reset before every extraction, and unknown setting names are rejected.

**D-020 Runs that start and then diverge are "numerically unstable"; validator coverage gap recorded** (provisional)
Integration check, 2026-09-13:
- **Unstable runs.** A ×20 time-step mutant (battery step 0.1 ms) overflowed HH rate expressions mid-simulation. jLEMS printed "simulation started" together with a hint that the time step may be too large. Such runs are now classified as numerically unstable (spec class 3), not build errors. A mid-run error without that hint stays a runtime error (class 2).
- **Validator gap.** `jnml -validate` test 10025 ("Ion channel in channelDensity should exist") checks `channelDensity` but not `channelDensityVShift`. With `ionChannel="Nax"` on the RS cell's VShift Na density, the file still validates, while the same error on a plain `channelDensity` is caught.
- **Consequence for omitted includes.** Removing the Na include from RS.cell.nml leaves a structurally "valid" cell that fails to build when reused. The shipped harness still runs, because it includes the channel itself.

Such variants are class 2 (structurally valid, non-executable) and are flagged `canonical_runs_but_battery_failed`. Reporting the validator gap upstream to NeuroML is Neel's decision (N-11).

**D-021 Rule changes after the module build reviews** (provisional; each came from a builder note in `docs/build_notes/`)
- **One detection rule for every protocol, including the canonical one.** A protocol detects a mutant only if the same feature is detected at h and at h/2. SILENT (class 6) now uses the reproducible canonical rule, which is the same rule as the detection matrix and the primary endpoint. Previously class 6 used detection at h only, so `1 - DR_canonical` could exceed the silent-survival rate.
- **Canonical analysis window.** The window is the union of the pulses that target the population the harness records. It is no longer "the earliest pulse generator", which picked non-targeting or hyperpolarising pre-pulses in three curated candidates.
- **`scale_gate_time_constant` uses the q10Fixed mechanism.** In NeuroML2CoreTypes every core HH gate computes `tau = tau_base / rateScale`, with `rateScale = product(q10)`, and `inf = alpha/(alpha+beta)` is unchanged. Inserting `q10Fixed=k`, or scaling an existing one, therefore scales the time constant exactly.
  - Without this mechanism the operator has no sites in any Pospischil cell (custom rate ComponentTypes), so the specification's "scale a channel time constant" would never be tested in the pilot.
  - `q10ExpTemp` gates remain inapplicable.
- **`increase_dt` factor grid is x4, x10, x20.** A x2 mutant at the h/2 level reruns the reference at h and could never be admissible.
- **Numerical-blow-up bound raised from 250 mV to 10 V.** A harness recording a gate variable or a concentration is compared behaviourally, not called unstable. Genuine divergence in jLEMS appears as non-finite values or an aborted run (D-020).
- **`ahp_depth` needs at least 1 spike, not 2.** eFEL 5.7.34 defines it after a single spike, and P09 is designed to evoke one.
- **Depolarisation-block voltage is a config key.** It is now an explicit, frozen key: `depolarization_block_v_mV: -40.0`.
- **Validator warnings are not validity failures.** jnml exits 0 when a file passes with warnings. A jNeuroML crash while loading an existing file is a model defect (`valid=False`), not a tool failure.
- **Rheobase search retries a failing initial grid.** It retries with a smaller upper amplitude, up to three times, so small high-input-resistance cells can be included.
- **Core defects fixed.** Found by the core-tests builder, each with its reproduction:
  - schema-invalid element order when a ramp precedes a pulse;
  - inverted rheobase bracket on a non-reproducible response;
  - `K` accepted although NeuroML temperatures allow only `degC`;
  - missing molar unit `M`;
  - manifest duplicate and column checks.

**D-022 Hidden agent-study evaluators are kept out of Git** (provisional; see N-12)
- **What.** `agent_study/hidden/` (hidden checks and answer-key specs) and `results/agent_study/private/` (baselines) are Git-ignored. Only `agent_study/HIDDEN_MANIFEST.sha256` is committed.
- **Why.** Trials run on exported directories without Git history, but hidden files that enter history are hard to remove and would leak if the repository is pushed before the trials finish.
- **Conflict of interest.** The same assistant that built NeuroSem wrote these evaluator specs. Neel should review them, and ideally revise them independently, before any trial.

**D-023 A run is "dirty" only if simulation-relevant files differ from the commit** (fixed)
`provenance.git_state` checks `src`, `configs`, `data`, `models`, `scripts`, `workflows`, `pyproject.toml` and `requirements.lock`. Edits to documentation or audit evidence (for example, the prior-art sweep writing into `docs/m0_evidence` while the pilot ran) cannot change a simulation or a derived number, so they do not mark runs dirty.

**D-024 The pilot is larger than the specification's pilot table** (provisional; Neel to confirm)
The spec's pilot table lists 4 protocols, 3-5 features and 5-10 mutants per model. The pilot that ran on 2026-09-13 used:
- all 9 implemented battery protocols (P01, P02, P04-P10) plus rheobase (P03) and the canonical harness;
- the full feature set in `configs/features.yaml`;
- 2 sites per mutation operator across the biophysical, reference and numerical families, which gives about 26 mutants per model;
- 8 valid-transformation and no-change operators per model.

Why: the battery runs as one batched simulation per variant, so the extra protocols cost little. Running the full candidate battery also tests every protocol and feature for stability before anything is frozen. The larger scope makes the pilot's go/no-go criteria harder to pass by chance, not easier.

The primary protocol count and the frozen study scope remain decisions for the preregistration.

**D-025 The frozen study runs as a fresh campaign, with no cache reuse across commits** (provisional; Neel to confirm)
The pilot reused 75 cached simulations from earlier development commits; 38 were recorded with a dirty tree (`docs/pilot/pilot_interpretation.md` section 7).

Content addressing guarantees those traces match their inputs, but provenance is cleaner when every run of a confirmatory campaign comes from one clean commit. So the frozen study must:
- use a new campaign name;
- run on a committed, clean tree;
- check that every `run.json` records the same commit with `git_dirty = false`.

Now enforced in code: `evaluate_heldout` calls `registry.check_single_clean_commit` (D-026).

**D-026 Pilot data are exploratory and developmental; they never enter the confirmatory estimate** (Neel's direction, 2026-09-13; fixed)

*Role of the pilot.*
- It is the first publication-oriented experimental phase. It should produce rigorous exploratory results, candidate case studies, validated methods, runtime estimates, and evidence on whether silent behavioural drift exists.
- It is also the development set. It may be used to debug the pipeline, refine mutation operators, calibrate tolerances, select features and revise protocols.

*Pilot bounds.* 2-6 openly licensed NeuroML models; 4-8 stimulation protocols; 3-8 electrophysiological features; at least 3 mutation families; about 20-60 mutants; valid-transformation controls.

*Separation.* Pilot data are labelled exploratory/developmental and are never combined with the final held-out data for the primary confirmatory estimate.

*After the pilot, freeze all of the following, then run the held-out experiment once without changing them* (checklist in `PLAN.md`, "Post-pilot freeze sequence"):
- software version;
- model eligibility rules;
- mutation definitions;
- feature definitions;
- tolerances;
- canonical protocol;
- protocol-selection algorithm;
- hashed discovery/held-out splits;
- the preregistered primary hypothesis and analysis.

*In the manuscript.*
- The pilot may appear as method-development evidence, preliminary/exploratory findings, illustrative case studies, and motivation for the frozen design.
- The held-out study alone provides:
  - the primary detection-rate comparison;
  - the main confidence intervals and hypothesis test;
  - generalisation to unseen models;
  - generalisation to an unseen mutation family.

*Enforcement* (`src/neuraxis/experiments/registry.py`, tests in `tests/unit/test_campaign_registry.py`):
- every campaign has a permanent role (`exploratory_pilot`, `discovery`, `confirmatory_heldout`) in `results/campaign_registry.json`;
- `evaluate_heldout` refuses:
  - a campaign registered as exploratory or discovery;
  - a campaign name that already holds data;
  - a config-directory override;
  - models outside the held-out split;
  - runs from more than one commit or from a dirty tree;
- `assert_not_pooled` refuses to combine a confirmatory campaign with any other.

**D-027 Pilot data are preserved; finished campaigns are sealed; a revision is a new campaign** (Neel's direction, 2026-09-13; fixed)
Neel: "Do not discard pilot data. Preserve all pilot configurations, raw outputs, code versions, exclusions, revisions, and decision logs so the manuscript can report the development process transparently."
- **Code versions.** Git tag per iteration (`pilot-v1-code` at `d323afa`).
- **Configurations.** `make_context` copies the config files into `results/processed/<campaign>/config_snapshot/`, write-once and hash-checked. A campaign refuses a changed config or simulator, so a change needs a new campaign name.
- **Raw outputs.** Traces are too large for Git. `scripts/archive_campaign.py`:
  - writes `ARCHIVE_MANIFEST.sha256` (hash of every raw file, workspace and run scratch, including Git-ignored traces);
  - writes a write-once tar under `archive/` (Git-ignored) with its hash in `ARCHIVE.json`;
  - copies the run logs into the tracked results.
  Durable off-machine storage is Neel's choice (N-16); nothing has been uploaded.
- **Sealing.** `SEALED.json` makes the pipeline refuse to write into the campaign again. Derived analyses may still read it.
- **Exclusions, revisions and decisions.** `docs/pilot/PILOT_REGISTER.md` lists each iteration's exclusions and the commits that changed how its numbers were produced. Decisions stay in this file.

**D-028 Pilot iteration 1 exceeded the pilot bounds; it is kept as iteration 1, and a bounded iteration 2 is drafted** (provisional; N-14)
- **What exceeded the bounds.** Campaign `pilot` used 10 protocols (bound 4-8) and 18 features (bound 3-8). Its 2 models, 3 families, 52 mutants and 16 controls are within the bounds.
- **Relation to D-024.** This replaces D-024's rationale as the governing scope rule.
- **What happens to iteration 1.** It is not rerun, trimmed or discarded. It is reported as exploratory iteration 1, with the deviation stated.
- **Iteration 2.** `docs/pilot/pilot_v2_design.md` and `configs/pilot_protocol_v1/` propose:
  - 4 models from three sources;
  - 7 protocols;
  - 8 features;
  - 3 families, with about 44 mutants and about 32 controls.
  It has not been run.
- **Canonical features setting.** The canonical harness's compared features are now configurable (`canonical.features`; default unchanged), so iteration 2 can compare the canonical test and the battery like for like.

**D-029 Primary and secondary feature panels; the pilot limits are feasibility guidelines** (Neel, N-14; fixed)
- **Guidelines, not laws.** The 4-8 protocol and 3-8 feature limits are feasibility guidelines. They must not weaken the study or delete useful measurements.
- **Four kinds of element, kept distinct:**
  - primary prespecified measurements;
  - secondary exploratory measurements;
  - calibration procedures;
  - experimental detection protocols.
- **Primary panel for Pilot 2:** spike count, first-spike latency, last ISI, adaptation index, AP amplitude, AHP depth, steady-state voltage, rheobase. It alone decides classes, the detection matrix, the silent list and the pilot criteria (including the refinement-exclusion criterion).
- **Secondary panel:** the other 10 of Pilot 1's 18 features, per protocol exactly as in Pilot 1 (`secondary_features` in the config). They are extracted from the same traces and reported in `detections_secondary.csv` and `secondary_feature_report.csv`. They never change a primary result after the data are seen.
- **Report required.** Pilot 2 reports whether any secondary feature detects a mutant the primary panel misses.
- **No permanent removal.** No feature is removed for Pilot 1 unhelpfulness. The confirmatory panel is proposed after Pilot 2 and frozen before held-out evaluation.
- **Pilot 2's status.** It is a second development iteration informed by Pilot 1, not independent confirmation.
- **Code.** `ProtocolTemplate.secondary_features`, `Context.primary_panel`, `strata.split_primary`. Tests in `tests/unit/test_strata.py`.

**D-030 Numerical-setting mutations are a separate robustness experiment, never semantic drift** (Neel, N-15; fixed)
- **Primary corpus.** It is the semantic stratum only (biophysical, reference). Time-step, solver, spatial-discretization and recording-resolution changes form the "numerical robustness and convergence stress tests" stratum.
- **Enforcement.** `strata.primary_admissible` is used by aggregation, analysis and `evaluate_heldout`. Tests prove numerical mutants and controls cannot enter the primary denominator.
- **Identical settings.** Primary semantic mutants and controls must have no execution overrides and no change to step, solver method or discretisation (`check_identical_numerics`, run before simulation).
- **Convergence workflow.** Every numerical stress test runs at h, h/2 and h/4. Its deviation is compared with the reference's discretisation error and observed order (`numerical_robustness.csv`). Labels never say semantic drift.
- **Operator retained.** `increase_dt` stays, and Pilot 1's results stay.
- **Pilot 1 derived reanalysis** (`docs/pilot/numerical_reclassification.md`, `results/derived/pilot/`):
  - 0 silent semantic mutants;
  - all 3 silent mutants were numerical;
  - semantic paired counts: 19 both, 3 canonical only, 0 battery only;
  - the unequal-starting-step confound is documented.

**D-031 Pilot archives: redundant private storage now, DOI deposit at release** (Neel, N-16; in progress)
- **Done:**
  - archive SHA-256 re-verified;
  - test extraction with all 5,186 files checked against the manifest (`results/processed/pilot/ARCHIVE_VERIFICATION_local.json`, `scripts/verify_archive.py`);
  - format, software, command, size, count and dates recorded in `results/processed/pilot/ARCHIVE_README.md`, with restore steps;
  - full-history Git bundle created and verified, because the repository has no remote.
- **Not done: the second independent private copy.** The only cloud storage on this machine is a OneDrive signed in under an address not known to be Neel's. When asked where the copy should go, Neel dismissed the question, so nothing has been uploaded (N-16).
- **At release:**
  - review licences;
  - deposit only redistributable content on Zenodo or equivalent (otherwise manifests, hashes and scripts);
  - link the GitHub release;
  - keep Pilot 1 labelled exploratory.

**D-032 Pilot 2 protocol taxonomy and the family-count consequence** (provisional; N-17)
- **Taxonomy:**
  - the reference rheobase search is a calibration procedure;
  - variant rheobase (P03) is a detection measurement;
  - P00 canonical is an additional comparator.
- **Detection protocols:** 7 distinct (P03-P09; 6 stimulus waveforms plus 1 threshold measurement).
- **Redundancy in Pilot 1.** P03, P04, P06, P07, P08 and P09 detections were all subsets of P05's. They are kept for Pilot 2 on mechanistic grounds and reassessed before the freeze.
- **Consequence of D-030.** The primary semantic corpus now has 2 families. Held-out generalisation to an unseen semantic family needs a third family, or a revised aim.

**D-033 Project name Neuraxis; study labels on every record** (Neel, 2026-09-14; fixed)
- **Name.** The project is Neuraxis. Every data record of the development pilot carries `project_name = "Neuraxis"`, `study_phase = "development_pilot"`, `protocol_version = "PILOT_PROTOCOL_V1"` and a designation string ("development study informed by Pilot 1; exploratory").
- **Where the labels go:**
  - `run.json` and rheobase records (with `config_sha256`);
  - classification and all other campaign tables (leading columns);
  - `detections*.csv`;
  - cascade and generation JSON;
  - `STUDY_METADATA.json`;
  - reports and diagnostics;
  - every figure (footer);
  - every prespecified output table.
- **What still lacks inline labels.** Machine-format files with fixed parsers (`detection_matrix*.csv`, `tolerances.csv`, fingerprint JSON) carry the label through the campaign's `STUDY_METADATA.json`, not inline.
- **Package name.** The package is still `neurosem`; a rename is a separate mechanical change.
- **Not yet done.** No name-conflict search has been run for "Neuraxis" (N-10).

**D-034 Replacement archival plan; OSF is an optional later mirror** (Neel, 2026-09-14; fixed)
- **Pre-run steps, in order:**
  1. `docs/PILOT_PROTOCOL_V1.md` (written protocol) and `configs/pilot_protocol_v1/` (executable settings), with agreement enforced by `tests/unit/test_pilot_protocol_v1.py`;
  2. `manifests/pilot_pre_run_sha256.txt` (`scripts/pre_run_manifest.py`);
  3. a commit pushed to a private GitHub remote, with the push record in `manifests/pilot_pre_run_push_record.json`;
  4. a compressed pre-run package (`scripts/pre_run_package.py`; no model files or secrets; hash in `manifests/pilot_pre_run_package.json`).
- **Raw output.** Never overwritten (write-once, content-addressed run IDs, with timestamp, configuration hash, model tree hash and commit per run).
- **OSF.** OSF failure does not change the scientific design. An after-the-fact OSF upload is never presented as a preregistration completed before data collection.
- **At publication:**
  - public GitHub release and `CITATION.cff`;
  - licence verification;
  - Zenodo archive with the version DOI recorded;
  - raw data preserved separately if too large.

**D-035 Fixed pilot matrix, readiness gate, retry policy, stopping rule** (Neel, 2026-09-14; fixed)
- **What governs.** `docs/PILOT_PROTOCOL_V1.md` sections 8-10 govern Pilot 2.
- **No additions.** No protocols, mutants, models or repetitions are added because time remains.
- **Retries.** Only after infrastructure or toolchain aborts, at most 2, same commit and config. Model-attributable outcomes are never retried.
- **Frozen during a batch.** Thresholds, exclusions and definitions do not change during a batch. Proposals go to `docs/pilot/PILOT_PROTOCOL_V1_DEVIATIONS.md`.
- **Pre-run deviation.** The run commit is not `633482d`: labelling and scripts were added before the run, with no design change.

**D-036 Formal preregistration through AsPredicted before any held-out run** (Neel, 2026-09-14; fixed)
- **Draft.** After the pilot is reviewed, `docs/CONFIRMATORY_PREREGISTRATION_DRAFT.md` is prepared in AsPredicted format. It covers every item Neel listed, including disclosure of the pilot data already collected and confirmation that held-out outcomes were not inspected.
- **Hard stop.** No held-out data run until Neel writes exactly: "THE ASPREDICTED PREREGISTRATION HAS BEEN SUBMITTED AND VERIFIED. BEGIN THE FROZEN HELD-OUT EVALUATION."
- **Records.** Neel provides the time-stamped PDF and the verification URL.

**D-037 Third model-mutation family: ion-channel kinetics** (Neel, N-17; decided, not implemented)
- **Taxonomy, set prospectively:**
  1. static membrane/biophysical parameter mutations;
  2. ion-channel kinetics mutations (activation/inactivation midpoint shifts, gating-slope changes, gating time-constant scaling, voltage-dependence changes);
  3. reference or mechanism-composition mutations.
- **Operator requirements.** Every operator makes one documented change, preserves units and dimensions, yields schema-valid and executable models where intended, has immutable provenance, leaves stimulus, solver and time step unchanged, and is manually inspected on representative examples.
- **Correctness testing.** Allowed on sacrificial development fixtures.
- **Selection exclusion.** Its detection matrix is never used to select the final battery. It is labelled "excluded from protocol selection", not "completely unseen by the researchers".
- **Reclassification.** `scale_gate_time_constant` (currently biophysical) moves to family 2 when the taxonomy is implemented.
- **Timing.** Implemented after Pilot 2 and before the final freeze; not part of Pilot 2.

**D-038 Pilot 1 is reported only in its corrected form** (Neel, 2026-09-14; fixed)
- **The corrected facts:**
  - 22 real model edits;
  - canonical detected all 22;
  - battery detected 19;
  - no hidden semantic drift;
  - the three previously silent cases were numerical stress cases.
- **Where the original interpretation may not appear.** `docs/pilot/pilot_interpretation.md` (numerical-only silent cases counted as meeting criterion 1) is not used in any abstract, figure, introduction or publication claim. It stays in the repository only as a historical record, marked superseded.

**D-039 The Neuraxis execution plan is the controlling specification; the package is renamed** (Neel, 2026-09-16; fixed)
- **Controlling document.** `docs/handoff/NEURAXIS_EXECUTION_PLAN.pdf` (SHA-256 `2ae2a2ce…2ddd`) controls further work. Conflicts with earlier plans are resolved in `docs/DEVIATION_LOG.md` (X-01 to X-17).
- **Package.** `src/neurosem/` became `src/neuraxis/`. `neurosem` stays an import alias returning the same module objects, and the `neurosem` command and `NEUROSEM_*` environment variables still work.
- **Unchanged.** Feature-source labels and the `neurosem:` feature-config key stay, to keep hashed configs and recorded provenance.

**D-040 Run records follow the execution plan; tool failures never block retries** (fixed)
- **New fields:** `execution_id`, `model_hash`, `base_model_hash`, `mutation_id`, `transformation_id`, `protocol_id`, `time_step_ms`, `configuration_hash`, `start_time`, `end_time`, `runtime_seconds`, stdout and stderr paths with their hashes, `trace_hash`, `feature_hash`.
- **Run identity.** `run_id` stays the content address of the inputs; `execution_id` identifies each execution.
- **Cache verification.** Cached runs are reused only after their stored trace and output-stream hashes verify.
- **Tool failures.** They are kept in `_tool_failures/` and never become the run record.

**D-041 Mechanical model curation** (fixed)
- **Criteria.** `neuraxis curate-models` applies the plan's inclusion and exclusion criteria (C01-C13) using reference simulations only, before any split. Exclusions are logged and never depend on results.
- **Candidates.** Candidate snapshots live in `models/candidates/`.

**D-042 Ion-channel kinetics family implemented; excluded from protocol selection in code** (fixed, scope pending R-05)
- **Operators:** `shift_gate_midpoint`, `scale_gate_slope`, `shift_forward_rate_midpoint`, `shift_channel_vshift` (family `kinetics`, semantic stratum).
- **Selection exclusion.** `strata.SELECTION_EXCLUDED_FAMILIES` removes the family from `select-protocols`.
- **Correctness tests.** Run on development fixtures only; no detection data were made.
- **`scale_gate_time_constant`.** Recommended to stay in the biophysical development family because its Pilot 1 outcomes were inspected. This withdraws D-037's plan to move it, pending Neel.

**D-043 Code licence Apache-2.0, provisional** (plan directive; replaces D-018 provisionally)
- **Change.** `LICENSE` is the official Apache-2.0 text, and the previous BSD-3-Clause text is in `docs/licensing/`.
- **Pending.** Compatibility review L-01 and L-11.

**D-044 Internal study identifier; no final brand without approval** (Neel, 2026-09-17; fixed)
- **Identifier.** The study's internal identifier is `neuron_model_behavioral_validation` (`configs/study.yaml` `study_id`, `study_metadata.study_id`, `run.json` `study_id`), independent of branding.
- **Name.** Neuraxis is not publicly released or registered while the live NEURAXIS trademarks stand. The package rename stays on the current branch; no further large rename for now.
- **Brand rule.** No package publication, public repository, DOI, preregistration or manuscript title uses a final brand until Neel approves it. Options are in `docs/NAME_DECISION_PACKET.md`.

**D-045 Wang–Buzsáki undecided; decision packet** (Neel, 2026-09-17)
- **Status.** Neither included nor excluded yet.
- **Recommendation.** `docs/WANG_BUZSAKI_DECISION_PACKET.md` recommends exclusion from the primary analysis (validation exception needing a model-specific exception or manual repair), with an optional prespecified exploratory sensitivity analysis.
- **Pilot 2 default.** Pilot 2 leaves it out of the primary model set.

**D-046 Two-sided research question** (Neel, 2026-09-17; fixed)
- **Question.** "How much scientific protection does canonical regression provide for transformed neuronal models, and under what conditions do additional perturbation protocols provide unique information?"
- **No dependence on drift.** The study does not depend on finding silent drift.

**D-047 Canonical baseline audit and validation levels A-E** (Neel, 2026-09-17; fixed)
- **Audit.** `docs/CANONICAL_BASELINE_AUDIT.md` records that Pilot 1's canonical test was a feature-level regression: 11 features on the shipped stimulus, refinement-calibrated tolerances, exact firing regime, no full-trace or full spike-time comparison.
- **Levels.** From Pilot 2 on, results are reported at five levels:
  - A: basic validation;
  - B: canonical feature regression;
  - C: canonical full-trace regression (whole-trace RMSE, spike count, spike timing, thresholds from reference h versus h/2; `validation/trace_regression.py`);
  - D: multi-protocol perturbation testing;
  - E: full candidate battery.
- **B and C** are never merged.
- **Survivors.** Every apparent canonical survivor is re-checked at h/4.

**D-048 Pilot 2 redefined: PILOT_PROTOCOL_V2** (Neel, 2026-09-17)
- **Matrix:**
  - 4-6 models not used in Pilot 1;
  - 6-10 protocols;
  - 4-6 interpretable mutation families with two prespecified severity levels (`mutations/severity.py`);
  - about 15-25 variants per model;
  - at least 5 valid transformations per model;
  - refinement checks for survivors.
- **Fixed rules.** Branch rules A-D are fixed before data (`experiments/pilot_v2_outputs.py` `BRANCH_RULES`).
- **After Pilot 2, stop.** No expansion, no development campaign, no held-out access, no preregistration, no result claims, no threshold tuning.
- **Supersedes V1.** PILOT_PROTOCOL_V1 is superseded without having run.

**D-049 Kinetics mutations: gate before study use** (Neel, 2026-09-17)
- **Conditions.** Kinetics operators enter a study only after all of the following:
  - unit tests;
  - simulation integration tests;
  - documentation of the affected equations and elements;
  - confirmation that nothing else changed;
  - inspectable before/after outputs;
  - an atomic/compound classification.
- **Evidence.** `docs/KINETICS_OPERATOR_VALIDATION.md`, `results/audits/kinetics_validation/`.
- **Pilot 2 scope.** A limited prespecified subset may enter Pilot 2 once validated.

**D-050 Planned public name: PerturbPrint; one canonical namespace later** (Neel, 2026-09-17)
- **Public name.** PerturbPrint, subject to the completed name audit. Neuraxis is not used publicly.
- **Internal identifier.** `neuron_model_behavioral_validation`, permanent and independent of branding.
- **Rename timing.** No repository-wide rename while curation or tests run. The controlled plan is `docs/RENAME_PLAN.md`.
- **Namespace.** One canonical package namespace is recommended (`perturbprint`), with no permanent `neurosem`/`neuraxis` aliases. The only documented compatibility need is the Git-ignored hidden agent-study material, which can be updated in the same commit; Neel chooses whether to keep the `neurosem` alias until his evaluator review (N-12).
- **Preserved by the plan.** Git history, raw result paths, recorded metadata, prior names in the record, and every hash.

**D-051 Wang-Buzsáki excluded from the primary study; kept as a documented candidate** (Neel, 2026-09-17; fixed)
- **Excluded** because inclusion would need a model-specific schema exception or a manual repair (criterion C04).
- **Not repaired.** It is never hand-fixed and then used as an ordinary primary model.
- **Kept in the manifest** with the exclusion reason, the exact validator output, provenance, licence status and potential exploratory use (`data/model_manifest.csv`, `docs/WANG_BUZSAKI_DECISION_PACKET.md`).
- **Exploratory use** is allowed only as a prespecified, separately reported sensitivity analysis.

**D-052 Cache key for reusing a stored simulation** (Neel, 2026-09-17; fixed)
- **Key contents.** Model tree hash, the digest and version of the simulation-generation code, protocol configuration, the config-set hash, simulator and Java build, jar hash, time step and execution settings, recording variable, temperature, and the full input manifest.
- **Effect.** Any difference gives a different run id, so the run is repeated instead of reused. `cache_key_sha256`, `generation_version`, `generation_code_digest` and `java_version` are stored in every run record and re-checked before reuse.
- **Invalidation.** The temperature-field correction (X-19) changes generated inputs, so affected entries are invalid by construction. Curation restarted as `curation-v3`; curation v1 and the partial v2 are preserved.

## Models and licensing

**D-017 Pilot fixtures: Pospischil 2008 RS and LTS** (provisional)
Both are MIT-licensed (NeuroML2 directory), pinned to commit `049081c3`, hash-verified and OMV-tested. They behave differently (adapting vs T-current cell). They are correlated (same paper and shared channel files), which is acceptable for the pilot but not for held-out generalisation.

**D-018 Code license BSD-3-Clause** (provisional; see N-05)
Model files keep their own licenses: MIT, or LGPL-3.0 for the NeuroML2 HH example. Dependencies are used unmodified.

**D-019 Byte-exact storage of hashed files** (fixed)
`.gitattributes` disables line-ending conversion for `models/`, `results/raw/` and `data/splits/`.

## Decisions Neel must make

| id | decision | Claude's provisional choice / recommendation |
|---|---|---|
| N-01 | Create a GitHub repository (private now, public at release)? | **Decided 2026-09-14: private GitHub remote for the pre-run commit** (D-034); public only at release |
| N-02 | Discovery / held-out model split and held-out mutation family | pilot models listed as discovery only; no held-out assignment |
| N-03 | Final tolerance constants (`configs/tolerances.yaml`) after reviewing `tolerances.csv` from the pilot | starting floors, c = 3 |
| N-04 | Pilot decision thresholds (at most 25% of features excluded; at most 10% false positives) | provisional values in `experiments/pilot.py` |
| N-05 | Code license, and how to handle LGPL model files if mutants are redistributed | BSD-3-Clause; LGPL files keep their license |
| N-06 | Canonical metric: same features and tolerances (current), or OMV-style spike-time comparison, or both | same features; OMV check could be added as a secondary baseline |
| N-07 | Protocol amplitudes for models with very low rheobase (LTS short pulses, ramp, rebound) | keep as specified for the pilot; revisit only with discovery data, before freezing |
| N-08 | Whether to add NEURON as a cross-simulator (optional in the spec) | deferred |
| N-09 | Accept correlated Pospischil cells in the full study, and which curated candidates to add | see `docs/model_curation_candidates.md` when available |
| N-11 | Report the jNeuroML validator gap (`channelDensityVShift` references are not checked by test 10025) to the NeuroML maintainers? | not reported; outward-facing, needs Neel |
| N-13 | **Milestone 6 decision.** The pilot met all three formal criteria, but its only silent mutants are numerical-configuration changes (two explained largely by the harness/battery base-step asymmetry). The canonical harness caught every behaviour-changing biophysical and reference edit on the two correlated pilot models. Choose: a second design-frozen pilot on independent models; reframe as an evaluation of existing validation adequacy; or continue as specified | Recommend option 1 or 2 in `docs/pilot/pilot_interpretation.md`, not continuing on the numerical silent mutants. **Update:** Neel's direction (D-026) sets the path: bounded exploratory pilot iterations, then freeze, then one held-out study. Option 1 is taken up as iteration 2 (N-14). Whether the paper leads with silent drift or with validation adequacy stays open until the pilot phase ends. |
| N-14 | Pilot 2 design | **Decided 2026-09-13: approved with modifications** (D-029, D-032). Revised design in `docs/pilot/pilot_v2_design.md`. **Execution awaits Neel's go-ahead.** |
| N-15 | Time-step mutation | **Decided: removed from the primary semantic corpus; retained as a separate numerical robustness experiment** (D-030). Implemented and tested. |
| N-16 | Pilot archive storage | **Decided: private redundant storage now; Zenodo at public release** (D-031). Local copy verified. **Update 2026-09-14:** OSF unavailable; OSF is now an optional later mirror, and the pilot proceeds (D-034). An OSF upload package is staged in `archive/pilot/osf_upload/`. **Still open:** a second independent copy of the 1.92 GB Pilot 1 archive (not blocking). |
| N-17 | Third model-mutation family | **Decided: ion-channel kinetics** (D-037); to be implemented after Pilot 2 and before the freeze |
| N-12 | Where the hidden agent-study evaluators live permanently (separate private repository, encrypted archive, or offline), and whether Neel revises them independently, given they were written by the assistant that built NeuroSem | local only, Git-ignored, hashes committed |
| N-10 | Project name. The audit (`docs/m0_evidence/names/`, independently re-checked) found: no PyPI, conda-forge or GitHub-account conflict, but a 2025 CMAME article with an arXiv preprint and code named "NeuroSEM" (a computational simulation framework); an active GPL-3.0 GitHub project spelled "NeuroSem" in neuroscience and language models; the neuromarketing company NeuroSEM holding neurosem.com since 2013; and heavy overloading of "SEM" in neuroscience | **Update 2026-09-14: Neel named the project Neuraxis** (D-033). A name-conflict search for "Neuraxis" is still needed before any public release. Earlier recommendation: **PerturbPrint** (package/CLI `perturbprint`); it matches the defined term "perturbation fingerprint" and had zero hits in every source that answered (Zenodo, EUIPO and some rate-limited indexes could not be checked). `docs/NAME_CONFLICT_AUDIT.md` recommends deciding before preregistration and the frozen study, whose raw results are immutable. Runner-up: DriftClamp. Not legal clearance; re-check registries before release. Code keeps the working name `neurosem` until Neel decides (a rename is a mechanical refactor). |
