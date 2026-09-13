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
| N-01 | Create a GitHub repository (private now, public at release)? | none created |
| N-02 | Discovery / held-out model split and held-out mutation family | pilot models listed as discovery only; no held-out assignment |
| N-03 | Final tolerance constants (`configs/tolerances.yaml`) after reviewing `tolerances.csv` from the pilot | starting floors, c = 3 |
| N-04 | Pilot decision thresholds (at most 25% of features excluded; at most 10% false positives) | provisional values in `experiments/pilot.py` |
| N-05 | Code license, and how to handle LGPL model files if mutants are redistributed | BSD-3-Clause; LGPL files keep their license |
| N-06 | Canonical metric: same features and tolerances (current), or OMV-style spike-time comparison, or both | same features; OMV check could be added as a secondary baseline |
| N-07 | Protocol amplitudes for models with very low rheobase (LTS short pulses, ramp, rebound) | keep as specified for the pilot; revisit only with discovery data, before freezing |
| N-08 | Whether to add NEURON as a cross-simulator (optional in the spec) | deferred |
| N-09 | Accept correlated Pospischil cells in the full study, and which curated candidates to add | see `docs/model_curation_candidates.md` when available |
| N-11 | Report the jNeuroML validator gap (`channelDensityVShift` references are not checked by test 10025) to the NeuroML maintainers? | not reported; outward-facing, needs Neel |
| N-13 | **Milestone 6 decision.** The pilot met all three formal criteria, but its only silent mutants are numerical-configuration changes (two explained largely by the harness/battery base-step asymmetry). The canonical harness caught every behaviour-changing biophysical and reference edit on the two correlated pilot models. Choose: a second design-frozen pilot on independent models; reframe as an evaluation of existing validation adequacy; or continue as specified | Recommend option 1 or 2 in `docs/pilot/pilot_interpretation.md`, not continuing on the numerical silent mutants |
| N-12 | Where the hidden agent-study evaluators live permanently (separate private repository, encrypted archive, or offline), and whether Neel revises them independently, given they were written by the assistant that built NeuroSem | local only, Git-ignored, hashes committed |
| N-10 | Project name. The audit (`docs/m0_evidence/names/`, independently re-checked) found: no PyPI, conda-forge or GitHub-account conflict, but a 2025 CMAME article with an arXiv preprint and code named "NeuroSEM" (a computational simulation framework); an active GPL-3.0 GitHub project spelled "NeuroSem" in neuroscience and language models; the neuromarketing company NeuroSEM holding neurosem.com since 2013; and heavy overloading of "SEM" in neuroscience | **Recommend renaming before any public release.** Preferred: **PerturbPrint** (package/CLI `perturbprint`); it matches the defined term "perturbation fingerprint" and had zero hits in every source that answered (Zenodo, EUIPO and some rate-limited indexes could not be checked). `docs/NAME_CONFLICT_AUDIT.md` recommends deciding before preregistration and the frozen study, whose raw results are immutable. Runner-up: DriftClamp. Not legal clearance; re-check registries before release. Code keeps the working name `neurosem` until Neel decides (a rename is a mechanical refactor). |
