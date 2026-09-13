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
| N-10 | Project name (see `PRIOR_ART_AUDIT.md` name-conflict section) | pending audit |
