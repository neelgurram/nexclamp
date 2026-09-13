# NeuroSem handoff (text extraction)

> Machine-extracted from `NEUROSEM_CLAUDE_HANDOFF.pdf` (SHA-256 `ba1db26a518038ce1d3b7c8837c7cc2b51c8386f3eb2369a28e52d0b9abd054d`) with pypdf. Math glyphs and the repository tree lost formatting; the PDF is authoritative.

NeuroSem: Claude Code Research and Implementation Handoff

## Mission

Build and evaluate NeuroSem , a reproducible framework for detecting silent behavioral changes in computational neuron models after editing, translation, refactoring, or repair. Research question: Can a neuron model remain structurally valid, execute successfully, and pass one conventional reference test while behaving differently under other scientifically relevant electrical stimuli? Primary hypothesis: A compact stimulation battery selected on discovery models will detect more behavior-changing transformations on held-out models than a single canonical protocol, and will outperform cost-matched random protocol sets. Claude Code is a development assistant. It may later be evaluated in a small isolated case study, but it is not the subject of the main paper.

## Plain-language concept

A published neuron model receives simulated electrical current and generates a voltage trace. An edit may leave the file legal and executable and may preserve its response to one standard stimulus, while changing its response to a weak current, long pulse, ramp, or rebound test. NeuroSem runs multiple stimuli, extracts interpretable electrophysiological features, and finds a small set of tests that best reveals those hidden differences. The intended contribution is not NeuroML validation, simulation, feature extraction, mutation testing, or metamorphic testing individually. Those already exist. The candidate novelty is their neuroscience-specific integration into a mutation-calibrated perturbation-fingerprint method with optimized stimulation protocols and held-out evaluation .

## IEEE pathway

A paper is submitted to a specific IEEE journal or conference, not to IEEE generally. The most plausible journal target is IEEE/ACM Transactions on Computational Biology and Bioinformatics (TCBB) if the finished work contains a substantial computational method, strong held-out evaluation, biological interpretation, and reproducible software. A future IEEE CIBCB conference may fit modeling, simulation, and optimization of biological systems, but its current call, deadlines, fees, presentation rules, and indexing must be checked before submission. Potential venue order:
1. IEEE/ACM TCBB — best IEEE journal fit.
2. A current IEEE CIBCB conference — good conference route if the call matches.
3. IEEE Journal of Biomedical and Health Informatics — only with a stronger biomedical-informatics or health connection.
4. IEEE TNSRE — only with direct neural-engineering, stimulation, or rehabilitation relevance.
5. IEEE Access — broad fallback, subject to current open-access fees. IEEE requires original work and does not allow simultaneous submission of substantially similar manuscripts. Substantive generative-AI use must be disclosed under the selected venue's current policy. Only humans can be authors and the human author remains responsible for the work.

## Existing field

Reuse rather than rebuild:
● NeuroML/LEMS: model representation and simulation descriptions.
● pyNeuroML/jNeuroML: parsing, validation, simulation, and translation.
● Open Source Brain Model Validation: model tests and continuous validation.
● SciUnit/NeuronUnit: scientific model testing.
● eFEL: standardized electrophysiological feature extraction. Do not claim novelty for schema validation, units, simulation, saved-trace comparison, feature extraction, multi-protocol characterization, metamorphic testing generally, mutation testing generally, or generic test-suite minimization. Before writing novelty claims, create docs/novelty_matrix.csv from Google Scholar, PubMed, IEEE Xplore, ACM DL, Semantic Scholar, arXiv, bioRxiv, GitHub, PyPI, and Zenodo. Search terms should include:
● conductance neuron model metamorphic testing
● NeuroML mutation testing
● neuron model semantic regression
● behavioral preservation neuronal model conversion
● perturbation fingerprint neuron model
● automatic stimulation protocol selection model validation
● mutation testing computational neuroscience
● AI coding agent neuron simulation Columns: citation, year, model type, controlled mutations, multiple stimuli, electrophysiology features, protocol optimization, held-out evaluation, AI transformations, software, and distinction from NeuroSem.

## Definitions

● Reference model: Validated, reproducibly executable source model with provenance.
● Transformation: Deliberate alteration to a model, protocol, repository, or execution configuration.
● Valid transformation: Representational change intended to preserve tested behavior.
● Mutant: Model produced by exactly one recorded mutation operator.
● Admissible non-equivalent mutant: Structurally valid and executable mutant with reproducible behavioral divergence somewhere in the predefined exhaustive battery.
● Canonical protocol: Single conventional stimulation used as the baseline regression test.
● Perturbation fingerprint: Electrophysiological feature vector across several stimulation protocols.
● Silent semantic drift: Behavioral divergence that passes structural checks, execution, and canonical regression but is exposed by additional perturbation testing.
● Empirical semantic certificate: Finite passing test set; evidence, not formal proof of equivalence. For model m , protocols P , and features E , define: 𝐹 ( 𝑚 ) = { 𝑓 ( 𝑚 , 𝑝 ) : 𝑝 ∈ 𝑃 , 𝑓 ∈ 𝐸 } .A transformation is detected when a prespecified protocol-feature difference exceeds its frozen calibrated tolerance.

## Research questions

1. How often do valid, executable mutations survive canonical testing but diverge elsewhere?
2. Does an optimized compact battery detect more admissible mutants than canonical testing?
3. Does it beat random protocol sets under the same protocol-count and runtime budgets?
4. Does it generalize to held-out neuron models?
5. Does it generalize to a held-out mutation family?
6. Which protocols and features reveal each fault family?
7. Do isolated AI-assisted transformations show related silent drift?

## Solo scope

Pilot
● 2 reference models.
● 4 protocols.
● 3–5 features.
● 3 mutation families.
● 5–10 mutants per model.
● 4–6 valid transformations.
● jNeuroML only. Pilot success requires at least one reproducible non-equivalent mutation that passes canonical testing and is detected elsewhere, stable feature extraction under numerical refinement, and acceptable false positives on valid transformations. Full study
● 12–16 reference models.
● 8–10 discovery models and 4–6 held-out models.
● 10–16 candidate protocols.
● 6–8 mutation families.
● 100–160 carefully curated admissible mutants.
● 24–40 valid transformations.
● 20–30 optional Claude Code tasks.
● 4–6 optional cross-simulator models. Reduce mutant count before sacrificing curation, provenance, controls, or held-out evaluation.

## Model selection

Include models only when they have:
● Traceable public source and usable license.
● Stable immutable snapshot and hashes.
● Current NeuroML validity.
● Deterministic execution in the frozen environment.
● Practical runtime.
● Interpretable voltage output and meaningful current response.
● Scientific provenance.
● No unavailable proprietary dependency. Seek diversity across tonic spiking, adaptation, bursting, rebound, sag, and excitability thresholds. Begin with simple/single-compartment models. Add few multicompartment models only after stability. Record model ID, source, citation, URL, download date, license, hashes, included files, simulator version, expected behavior, and inclusion decision.

## Protocols

Implement in stages:
1. Zero-current baseline.
2. Weak depolarizing step.
3. Rheobase search.
4. Step at a fixed multiple of model-specific rheobase.
5. Long suprathreshold step.
6. Depolarizing ramp.
7. Hyperpolarizing step.
8. Hyperpolarization-release rebound.
9. Short suprathreshold pulse.
10. Paired pulses.
11. Deterministic chirp only if stable.
12. Frozen pseudo-random waveform only as extension. Normalize principal depolarizing tests to model-specific rheobase so the tests are comparable across models.

## Features

Start with:
● Baseline and steady-state voltage.
● Voltage deflection and sag ratio.
● Rheobase.
● Spike count and firing frequency.
● First-spike latency.
● Action-potential amplitude and half-width.
● After-hyperpolarization depth.
● First and last interspike intervals.
● Adaptation index.
● Burst count.
● Qualitative firing regime. Use eFEL where supported. Freeze and record eFEL version, interpolation, thresholds, stimulation windows, and undefined-feature handling. Never replace missing features with zero.

## Transformations

Valid transformations Use these to estimate false positives:
● Equivalent unit conversion.
● XML formatting/comments.
● Equivalent numeric formatting.
● Identifier rename with all references updated.
● File factoring with preserved references.
● Reordering semantically independent elements.
● Explicitly writing an inherited default without changing its value. Verify each using structural inspection and a high-resolution exhaustive battery before inclusion.

## Mutations

Stimulus: amplitude, onset, duration, total time, or recorded variable. Biophysical: conductance, reversal potential, capacitance, gating time constant, initial voltage, or wrong segment group. Reference: wrong channel, missing include, duplicate assignment, or wrong compatible component. Numerical: integration step, solver configuration, spatial discretization, or output sampling. Use one fault per mutant in the primary study. Classify every mutant as structurally invalid, non-executable, numerically unstable, behaviorally equivalent, non-equivalent, or silent under canonical testing. Only admissible non-equivalent mutants belong in the main detection-rate denominator.

## Tolerances

For every reference model/protocol:
1. Run at h .
2. Repeat at h/2 .
3. Repeat at h/4 when practical.
4. Align traces on a common time grid.
5. Measure trace and feature differences.
6. Define feature-specific absolute and relative floors.
7. Freeze rules before held-out testing. Conceptual rule: τ 𝑚 , 𝑝 , 𝑓 = 𝑚𝑎𝑥 ( τ 𝑓 𝑎𝑏𝑠 , 𝑟 𝑓 | 𝑓 ( 𝑚 , 𝑝 ) | , 𝑐 | 𝑓 ℎ ( 𝑚 , 𝑝 ) − 𝑓 ℎ /2 ( 𝑚 , 𝑝 ) | ) . Constants must come from discovery/reference analyses and be subjected to sensitivity analysis. Never tune thresholds on held-out outcomes.

## Protocol selection

Build a binary detection matrix: rows are discovery mutants, columns are protocols, and cells show whether a protocol detects a mutant. Greedy maximum coverage:
1. Choose the protocol detecting the most currently undetected mutants.
2. Mark them covered.
3. Choose the protocol detecting the most remaining mutants.
4. Repeat to protocol budget k .
5. Freeze the selected set.
6. Test on held-out models and mutation families. Compare against canonical testing, random count-matched sets, random runtime-matched sets, and the exhaustive candidate battery. Keep the selection algorithm simple and interpretable unless complexity demonstrably improves held-out results.

## Leakage prevention

● Discovery data may guide development, tolerances, and protocol selection.
● Held-out models cannot influence protocol selection or thresholds.
● Hold out at least one entire mutation family.
● Store held-out manifests separately.
● Ensure selection code cannot read held-out labels.
● Hash split files and log held-out access.
● Do not repeatedly redesign after examining final failures.

## Statistics

Primary outcome: held-out detection rate of selected battery versus canonical regression. Report:
● Paired outcome counts.
● Difference in detection rates.
● Confidence interval resampling base models, not individual mutants alone.
● Exact paired test where appropriate.
● Random-baseline distribution.
● False-positive rate on valid transformations.
● Mutation-family breakdown.
● Detection-versus-cost curve.
● Sensitivity to tolerance choices. Mutants from one base model are correlated. Account for clustering. Preregister the hypothesis, endpoint, inclusion/exclusion rules, splits, protocols, tolerances, handling of crashes/equivalent mutants, and analysis before final evaluation.

## Claude Code case study

Place under Application to AI-assisted neuronal-model transformation . Do not include Claude in the paper title. Possible tasks:
● Repair seeded unit or reference errors.
● Restore a changed stimulus.
● Rename/refactor model components.
● Convert physical units correctly.
● Change one requested conductance without unauthorized edits.
● Improve runtime while preserving tested behavior.
● Diagnose a schema-valid behavioral change. Isolation:
● Freeze NeuroSem first.
● Expose only public tests.
● Hide selected protocols and answer keys.
● Start each trial from the same clean commit.
● Use fresh sessions with fixed permissions and budgets.
● Log model/version/date/prompts/transcripts/patches/costs.
● Do not manually intervene during autonomous trials.
● Score with deterministic hidden tests.
● Audit every output afterward. Keep claims restricted to the evaluated Claude configuration. Do not generalize to all coding agents.

## Repository

neurosem/ ├── README.md ├── LICENSE ├── CITATION.cff ├── pyproject.toml ├── environment.yml ├── Dockerfile ├── Makefile ├── .github/workflows/ci.yml ├── configs/ ├── data/ │ ├── model_manifest.csv │ ├── protocol_manifest.csv │ ├── mutation_manifest.csv │ ├── valid_transforms.csv │ └── splits/ ├── models/{raw,curated,snapshots}/ ├── src/neurosem/ │ ├── cli.py │ ├── provenance.py │ ├── simulators/ │ ├── protocols/ │ ├── features/ │ ├── mutations/ │ ├── transforms/ │ ├── validation/ │ ├── selection/ │ ├── experiments/ │ └── analysis/ ├── tests/{unit,integration,regression,fixtures}/ ├── workflows/ ├── results/{raw,processed,tables,figures}/ ├── docs/ └── manuscript/ Every run must record run ID, model and file hashes, source snapshot, protocol, mutation/transform, simulator and version, time step, duration, seed, environment digest, status, runtime, trace and feature paths/hashes, timestamp, and Git commit. Raw results are immutable. Target commands: neurosem validate-models neurosem run-reference neurosem calibrate-tolerances neurosem generate-mutants neurosem classify-mutants neurosem build-fingerprints neurosem select-protocols --budget 4 neurosem evaluate-heldout neurosem evaluate-agent neurosem analyze neurosem reproduce-paper

## Milestones

M0 — Audit Create dependency/version/license audit, name-conflict search, prior-art matrix, risk register, decisions log, changelog, and AI-use log. Stop for approval.
M1 — Environment Create package, frozen dependencies, jNeuroML/eFEL integration, Docker, CI, and two fixtures. One command must validate and simulate both models cleanly.
M2 — Reference pipeline Create immutable traces, provenance, feature extraction, rerun tests, and inspection plots.
M3 — Protocol engine Implement step, rheobase, long-step, ramp, hyperpolarization, and rebound protocols with independent timing/amplitude tests.
M4 — Mutation engine Implement three pilot families, one-change enforcement, provenance, and validity/execution classification. Manually audit at least 20 mutants.
M5 — Fingerprints Implement eFEL adapter, trace metrics, convergence calibration, diagnostics, and detection matrix. Every detection must identify protocol, feature, threshold, and evidence trace.
M6 — Pilot decision Run 2–6 models and 20–60 mutants. Continue only if canonical testing misses reproducible drift and added protocols detect it without unacceptable false positives.
M7 — Selection/holdouts Freeze splits; implement greedy and random cost-matched baselines; enforce leakage barriers.
M8 — Frozen study Preregister, freeze configs/hashes, run full study, and perform statistical/robustness/ablation analyses.
M9 — Agent study Run frozen isolated Claude tasks and save complete evaluation artifacts.
M10 — Release/manuscript Create public repository, versioned release, DOI archive, reproducibility guide, manuscript, supplement, disclosures, and venue-specific IEEE format.

## Controls

Required:
● No-change control.
● Valid-transformation false-positive control.
● Deterministic mutation sensitivity control.
● Canonical baseline.
● Random count- and runtime-matched baselines.
● Exhaustive empirical battery.
● Numerical refinement.
● Held-out models.
● Held-out mutation family.
● Agent isolation.

## Figures

1. Canonical-looking equivalence but divergence under another stimulus.
2. Validation cascade from all mutants to hidden detections.
3. Mutant-by-protocol detection heat map.
4. Detection versus number/cost of protocols.
5. Held-out model and mutation-family generalization.
6. False positives and tolerance sensitivity.
7. Interpretable neuroscience case studies.
8. Secondary Claude Code case study.

## Success criteria

A strong paper requires most of these:
● Reproducible silent drift in more than isolated contrived cases.
● Interpretable feature or firing-regime changes.
● Selected battery materially beats canonical testing.
● Selected battery beats cost-matched random batteries.
● Generalization to unseen models.
● Low, transparent false positives.
● Robustness to tolerance changes.
● Results independent of Claude failures.
● One-command reproduction of tables and figures. Pivot or stop if existing tests catch nearly everything, most faults merely crash, selection fails against random on holdout, false positives remain high, results depend on one unstable model, or conclusions vanish after numerical refinement.

## Mandatory Claude operating rules

● Never fabricate papers, APIs, versions, licenses, results, or citations.
● Verify current APIs and licenses from primary sources.
● Do not silently change scientific scope.
● Do not run held-out evaluation during development.
● Do not tune thresholds after held-out inspection.
● Do not call finite testing formal equivalence proof.
● Do not treat every parameter change as a defect.
● Do not write result claims before data exist.
● Add tests before or with implementation.
● Use a branch and milestone report for each stage.
● Stop for Neel's approval after every milestone.
● Explain all scientific decisions in plain English.

## Initial Claude prompt

You are the lead research-software engineer implementing the attached NEUROSEM_CLAUDE_HANDOFF.md. Read it completely before taking action. This is a rigorous computational-neuroscience research study, not a demonstration app. Reproducibility, scientific validity, provenance, and leakage prevention have priority over speed. Do not implement the full system yet. Perform Milestone 0 only and create: - PLAN.md - REQUIREMENTS.md - PRIOR_ART_AUDIT.md - docs/novelty_matrix.csv - DEPENDENCY_AUDIT.md - LICENSE_AUDIT.md - RISK_REGISTER.md - DECISIONS.md - CHANGELOG.md - AI_USE_LOG.md For Milestone 0:
1. Separate existing functionality to reuse from genuinely new NeuroSem functionality.
2. Verify current NeuroML, LEMS, pyNeuroML, jNeuroML, OMV, SciUnit/NeuronUnit, and eFEL documentation, APIs, versions, and licenses from primary sources.
3. Search for project/package/name conflicts; do not assume NeuroSem is available.
4. Conduct the specified prior-art sweep and populate the novelty matrix with citations and URLs.
5. Identify assumptions in the handoff that are outdated, uncertain, technically infeasible, or scientifically weak.
6. Recommend two minimal, openly usable NeuroML fixtures, but verify their provenance and license before downloading.
7. Propose exact environment setup commands.
8. Convert the milestones into an incremental implementation plan with exit tests.
9. List every decision requiring Neel's approval. Do not fabricate sources, APIs, package versions, licenses, benchmark numbers, or scientific outcomes. Do not generate final results or manuscript claims. Do not access or create a final held-out evaluation yet. After writing the Milestone 0 documents, stop and give a plain-English briefing containing: - what was verified; - what remains uncertain; - closest prior work and the proposed distinction; - recommended project-name change, if needed; - proposed fixture models; - setup commands; - risks that could invalidate the study; - decisions Neel must make. Wait for explicit approval before Milestone 1.

## Neel's required knowledge

Before the frozen study, Neel must be able to explain without Claude:
1. What a conductance-based neuron model represents.
2. What a current stimulus and voltage trace are.
3. What spike count, latency, rheobase, adaptation, and rebound mean.
4. Difference between schema validity, execution, numerical convergence, tested behavior preservation, and biological validity.
5. What a mutation and valid transformation are.
6. Why equivalent mutants must not count as missed errors.
7. What silent semantic drift means operationally.
8. What a perturbation fingerprint measures.
9. Why multiple protocols can reveal changes hidden by one protocol.
10. How greedy protocol selection works.
11. Why held-out models and mutation families matter.
12. How tolerances are calibrated.
13. What Claude built versus what Claude was experimentally evaluated on.
14. Limits of every final claim.

## Final decision rule

Do not commit to a journal before the pilot. If the pilot and held-out study support a substantial algorithmic contribution, TCBB is the leading IEEE target. If the result is narrower but complete, select a specialist computational-neuroscience or scientific-software venue. Venue prestige must not drive threshold tuning, selective reporting, inflated novelty, or unsupported biological claims.
 