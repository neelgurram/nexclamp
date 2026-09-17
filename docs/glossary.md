# NeuroSem glossary

*Status: living document, drafted 2026-09-13. Definitions in section 1 follow the final
specification (`docs/handoff/NEUROSEM_FINAL_SPEC.pdf`, which is authoritative). Where a
definition names a NeuroSem file or setting, that is the current, provisional
implementation. It becomes binding only when frozen by preregistration.*

Each entry is one or two plain sentences. Terms in *italics* are defined elsewhere in
this glossary.

---

## 1. Operational definitions from the specification

**Reference model.** An unmodified, validated, reproducibly executable neuron model with
recorded provenance. In NeuroSem this is a `data/model_manifest.csv` row with
`inclusion = include`, run from its pinned snapshot under `models/raw/`.

**Transformation.** Any deliberate alteration to the model repository, the model
description, the simulation protocol or the execution configuration. *Mutants*, *valid
transformations* and *no-change controls* are all transformations.

**Valid transformation.** A representational or engineering change intended to preserve
tested scientific behaviour, such as converting to an equivalent unit or renaming an
identifier consistently. A detection on a valid transformation is a *false positive*.

**Mutant.** A transformed model created by exactly one recorded *mutation operator*.
NeuroSem rejects a variant if any file change is not covered by its recorded edits
(`enforce_single_operator`).

**Admissible non-equivalent mutant.** A structurally valid, executable mutant whose
behaviour diverges reproducibly from its reference somewhere in the predefined
*exhaustive battery*. Operationally it is *mutant class* 5 or 6: at least one
(protocol, feature) difference exceeds *tolerance* at both *h* and *h/2*.

**Canonical protocol.** The single standard stimulation test used as the conventional
behavioural-regression baseline. In NeuroSem it is the simulation shipped with the model
(its *harness*), analysed as `P00_canonical`.

**Perturbation fingerprint.** The collection of electrophysiological measurements a model
produces across several stimulation protocols: F(m) = { f(m, p) : p in P, f in E }. With the
current templates it holds 64 (protocol, feature) entries per model at one time step.

**Silent semantic drift.** Reproducible behavioural divergence that passes structural
validation, executes successfully and passes the canonical regression test, but is
exposed by another perturbation test. Operationally this is *mutant class* 6.

**Empirical semantic certificate.** A finite set of passing protocol-feature tests. It is
evidence that behaviour was preserved *for the tests run*, never a proof of equivalence
under every possible input.

**Detection.** A transformation is detected when at least one prespecified
protocol-feature difference exceeds its calibrated *tolerance*. A feature that is
defined in one model and undefined in the other also counts (*definedness mismatch*).

**Mutant classes (1-6).** Every generated mutant gets exactly one class:
(1) structurally invalid; (2) structurally valid but non-executable; (3) executable but
numerically unstable; (4) executable and behaviourally equivalent within the tested
domain; (5) executable and non-equivalent; (6) silent under canonical testing but detected
by another protocol. Only classes 5 and 6 enter the main detection-rate *denominator*.

**Equivalent mutant.** A class 4 mutant: it runs, and no reproducible difference is found
in the tested domain. It does not count as a missed error, because the change may
genuinely not matter for these stimuli.

**No-change control.** A transformation that only changes formatting or comments. Any
detection on it reveals noise or a bug in the pipeline itself.

**Discovery set.** The models (and mutation families) that may be used to develop
operators, calibrate tolerances, select protocols, debug features and choose the analysis.

**Held-out model set.** Models kept apart from every development decision and used only
in the final evaluation. They must not influence protocol selection or thresholds.

**Held-out mutation family.** At least one whole *mutation family* excluded from protocol
selection and used only in the final evaluation. It tests whether the battery catches
kinds of fault it was never tuned on.

**Leakage.** Any path by which held-out information influences a development decision.
Controls include separate manifests, hashed split files, code that cannot read held-out
labels, and a log of every held-out access.

**Lockbox.** A second, final held-out set that is opened only once, and only if enough
models remain to form one.

**Preregistration.** A time-stamped, frozen statement of hypotheses, endpoints, rules and
analyses written before the final data are seen. NeuroSem's draft is
`docs/PREREGISTRATION_DRAFT.md`.

**`configs/FROZEN.lock`.** The planned file of hashes that fixes configuration and split
files at preregistration. The held-out gate refuses to open held-out data unless the
hashes match.

## 2. Neuroscience terms

**Conductance-based neuron model.** A set of differential equations in which membrane
voltage changes because ion channels pass currents through conductances. Each channel's
current is its conductance times the distance of the voltage from the channel's
*reversal potential*.

**Single-compartment model.** A neuron model with one electrical compartment (here, one
soma segment), so voltage is the same everywhere in the cell. All current pilot models are
single-compartment.

**Membrane potential.** The voltage across the cell membrane, in millivolts (mV).
A *voltage trace* is the membrane potential recorded over time.

**Current clamp.** An experiment in which a chosen current is injected into the cell and
the voltage response is recorded. Every NeuroSem protocol is a current-clamp protocol.

**Ion channel.** A membrane protein, modelled as a conductance that opens and closes
according to *gating variables*. Examples in the fixtures: Na, Kd (delayed-rectifier K),
IM (slow M-type K), IT (T-type Ca) and a leak conductance.

**Maximal conductance density (`condDensity`).** A channel's conductance per unit membrane
area when fully open, for example `5.0 mS_per_cm2`. Scaling it is the
`scale_conductance` mutation.

**Reversal potential (`erev`).** The voltage at which a channel's current is zero.
Shifting it is the `shift_reversal` mutation.

**Specific capacitance.** The membrane's charge-storage capacity per unit area (fixtures:
`1.0 uF_per_cm2`). A larger capacitance makes voltage change more slowly for the same
current.

**Gating variable.** A number between 0 and 1 giving the fraction of a channel's gates in
the open state. It relaxes towards a voltage-dependent steady state with a time constant.

**Gate time constant.** How quickly a gating variable approaches its steady state. For
rate-based gates it equals 1 / (forward rate + reverse rate), so multiplying both rates by k
divides the time constant by k.

**Initial membrane potential (`initMembPotential`).** The voltage at time zero. Its effect
normally fades during the settling period before any stimulus.

**Segment group.** A named set of morphology segments to which a channel density applies.
In a single-compartment model every group contains the same single segment.

**Action potential (spike).** A brief, large, all-or-none voltage excursion. NeuroSem
detects spikes where voltage crosses -20 mV (the eFEL `Threshold` setting).

**Rheobase.** The smallest amplitude of a long current step (here 500 ms) that makes the
cell fire at least one spike. NeuroSem finds it by a bracketing search and scales most
depolarising protocols to it.

**Spike count.** The number of spikes inside the analysis window.

**Firing frequency.** How often a cell fires. eFEL's `mean_frequency` divides the number of
in-window spikes by the time from window start to the last spike, not by the window
length.

**First-spike latency.** The time from stimulus onset to the first spike. eFEL's
`time_to_first_spike` measures to the spike's *peak*.

**Interspike interval (ISI).** The time between two consecutive spikes. NeuroSem records
the first and the last ISI in the window.

**Spike-frequency adaptation.** Firing that slows during a constant stimulus, so ISIs
lengthen. It is often caused by slow potassium currents such as IM.

**Adaptation index.** A single number summarising how much ISIs lengthen. It is near 0
for regular firing and positive for adapting firing. NeuroSem uses eFEL's
`adaptation_index2`.

**Action-potential amplitude.** The height of a spike. eFEL's `AP_amplitude` measures it
from the spike's onset (where the voltage slope crosses a derivative threshold) to its
peak.

**Action-potential half-width.** The duration of a spike measured at half its amplitude.
It reflects how fast sodium and potassium currents act.

**AHP (afterhyperpolarization).** The dip of voltage below baseline just after a spike.
*AHP depth* (eFEL `AHP_depth`) is the minimum voltage between spikes minus the baseline
voltage.

**Burst.** A tight group of spikes separated from other groups by longer silences.
*Burst count* is the number of such groups (eFEL `strict_burst_number`).

**Rebound (post-inhibitory rebound).** Firing or depolarisation that occurs right after a
hyperpolarising current is switched off. T-type calcium currents are a classic cause.

**Sag.** During a long hyperpolarising step, voltage first drops and then partly recovers
("sags back") while current is still applied. It is typically caused by the Ih (HCN)
current. None of the current manifest models contains Ih.

**Sag ratio.** A number that summarises sag. NeuroSem uses eFEL's `sag_ratio1` =
(steady-state voltage - minimum voltage) / (baseline voltage - minimum voltage).

**Depolarization block.** Strong depolarisation makes a cell stop firing while it is held
at a raised voltage.

**Firing regime.** A qualitative label for a response: `silent`, `single_spike`,
`depolarization_block`, `bursting`, `adapting` or `tonic`. The first matching label wins
(`configs/features.yaml`).

**Tonic firing.** Regular, sustained firing with roughly constant ISIs.

**Baseline voltage.** Mean voltage just before stimulus onset. eFEL's `voltage_base` uses
the last 10 % of the time before the window start.

**Steady-state voltage.** Mean voltage near the end of the stimulus. NeuroSem uses eFEL's
`steady_state_voltage_stimend` (last 10 % of the window), not `steady_state_voltage`, which
eFEL measures after the stimulus ends.

**Voltage deflection.** Steady-state voltage minus baseline voltage: how far a step
current pushes the cell (eFEL `voltage_deflection_vb_ssse`).

**T-type calcium current (IT).** A low-threshold calcium current that is de-inactivated by
hyperpolarisation and can produce rebound spikes. It is present in the LTS fixture.

**M-current (IM).** A slowly activating potassium current that reduces firing over
hundreds of milliseconds. It is present in RS, LTS and IB.

## 3. Models, tools and files

**NeuroML (v2).** An XML standard for describing neuron and network models. NeuroSem pins
validity to the NeuroML v2.3.1 schema.

**LEMS.** A companion XML language that defines component behaviour (`ComponentType`s) and
simulations: what to run, for how long, at what time step and what to record.

**Custom `ComponentType`.** A model-specific LEMS definition that extends the core NeuroML
types. The LTS channel IT uses one (`IT_s_gate`), which is why strict libNeuroML checking
rejects the file.

**jNeuroML / jLEMS.** The Java reference tools. `jnml -validate` checks NeuroML files, and
jLEMS runs LEMS simulations. The pilot uses jNeuroML 0.14.0, whose jar contains jLEMS
0.12.0.

**pyNeuroML / libNeuroML.** Python front ends. pyNeuroML ships the jNeuroML jar, and
libNeuroML is the Python object model with its own (informational) validity check.

**eFEL.** The Electrophys Feature Extraction Library (version 5.7.34 here). It computes
spike and voltage features from a trace and a stimulus window.

**OMV (Open Source Brain Model Validation).** A tool that reruns a model and compares a few
observables, such as spike times, against stored expected values with a relative
tolerance. It is the conventional regression test that NeuroSem's canonical protocol
mirrors.

**SciUnit / NeuronUnit.** Frameworks for testing models against experimental
observations. They are prior art and optional adapters, not dependencies.

**Harness.** The LEMS simulation file shipped with a model (for example
`LEMS_RS.xml`). It defines the canonical protocol.

**Probe.** A LEMS and NeuroML network pair generated by NeuroSem to run a protocol battery.
Each protocol gets its own uncoupled single-cell population.

**Snapshot.** A pinned, byte-exact copy of upstream model files under
`models/raw/<snapshot>/`, with `PROVENANCE.json` recording URLs and SHA-256 hashes.

**Workspace.** A private, writable copy of a snapshot in which a reference, mutant or
transformation lives. Snapshots are never edited in place.

**Variant.** Any workspace plus its `variant.json` record: a reference, mutant, valid
transformation or no-change control.

**Run ID (content addressing).** A run's identifier is a hash of everything the simulation
reads plus its settings. Identical inputs reuse stored results, and raw results are
written once and never overwritten.

**Provenance record.** The metadata stored with every run: model and file hashes,
protocol, variant, simulator version, time step, seed, environment digest, status,
runtime, trace and feature hashes, timestamp and Git commit.

## 4. Numerics

**Time step (dt, h).** The fixed interval by which the simulator advances time. The
provisional nominal step is h = 0.005 ms (`configs/study.yaml`).

**Refinement levels (h, h/2, h/4).** The same simulation repeated with the time step halved
and quartered. Differences between levels estimate the solver's own error.

**Forward Euler.** The simplest integration method: next value = current value + dt x
current rate of change. It is first-order, so halving dt roughly halves the error, and a
development probe on the fixtures showed exactly this behaviour (`docs/pilot/dt_probe.md`).

**Numerical convergence.** Results stop changing meaningfully as the time step shrinks.
The *observed order* is estimated from how much the difference shrinks between h to h/2
and h/2 to h/4.

**Numerical instability.** The simulation diverges: jLEMS aborts after the run has started
with its "time step may be too large" hint, or the output contains non-finite values or
values beyond +-10 V (a deliberately loose bound, so a harness that records a non-voltage
state is judged by its behaviour instead). NeuroSem treats this as a solver blow-up, not
physiology (class 3). See DECISIONS D-020 and D-021.

**Settling period.** Stimulus-free time at the start of every probe (300 ms) that lets the
model reach rest. The eFEL baseline is taken from its last 10 %.

**Interpolation step (`interp_step`).** eFEL resamples every trace to this uniform step
(0.01 ms here) before computing features. Time-based features are quantised to it.

**Cell-step.** One simulated cell advanced by one time step. Cells x steps is NeuroSem's
simulator-independent cost measure for protocols.

## 5. Protocols and features

**Protocol template.** A protocol defined relative to rheobase (for example "2 x rheobase
for 500 ms"). It is instantiated once per reference model.

**Concrete protocol.** A template filled in with one model's rheobase, giving exact
amplitudes in nA. Every variant of that model receives the identical stimulus.

**Rheobase normalisation.** Scaling depolarising protocols to each model's own rheobase,
because the same absolute current can be negligible for one model and overwhelming for
another.

**Stimulus component.** One NeuroML input: a `pulseGenerator` (step) or a `rampGenerator`
(ramp).

**Analysis window.** The time interval passed to eFEL as `stim_start` and `stim_end`.
Features are measured relative to it.

**Protocol battery.** A set of protocols run on a model. The *exhaustive battery* is every
implemented candidate protocol plus the canonical protocol, and it defines admissibility.

**Feature state.** Every feature value is `defined`, `undefined` (eFEL could not compute
it) or `not_applicable` (for example fewer spikes than the feature needs). Missing values
are never replaced by zero.

**Definedness mismatch.** A feature is defined in one model but undefined or not
applicable in the other. It counts as a detection (`configs/tolerances.yaml`).

## 6. Tolerances and detection

**Tolerance (tau).** The smallest reference-versus-variant difference that counts as a
detection for one (model, protocol, feature):
tau = max(absolute floor, relative fraction x |f_h|, c x |f_h - f_h/2|).

**Absolute floor.** A fixed feature-specific minimum difference below which a change is
not considered meaningful (for example 0.5 ms for first-spike latency).

**Relative term.** A fraction of the reference value itself (for example 2 % of the
latency). It scales tolerance with the size of the feature.

**Refinement term.** c times the change in the reference feature when the time step is
halved (c = 3, provisional). It keeps solver error from being mistaken for drift.

**Limiting term.** Whichever of the three terms is largest and therefore sets tau. It is
recorded for every entry.

**Excluded (protocol, feature).** A feature whose defined/undefined state or firing-regime
label changes under refinement for that model. It is not trusted for detection, and the
exclusion is recorded rather than silently dropped.

**Tolerance sensitivity analysis.** Repeating the analysis with every tau multiplied by
0.5, 1, 2 and 4, to show whether conclusions depend on the exact tolerance.

**Detection matrix.** A table with one row per admissible discovery mutant and one column
per protocol. Each cell says whether that protocol detects that mutant.

**Coverage.** The fraction of admissible mutants detected by at least one protocol in a
set.

**Greedy maximum coverage.** Protocol selection that repeatedly adds the protocol catching
the most still-uncaught mutants, until a budget of k protocols. Ties go to the cheaper
protocol, then to the lower protocol id.

**Cost-sensitive greedy.** A variant of greedy selection that respects a total cost
budget in cell-steps instead of a protocol count.

**Count-matched random baseline.** Many random protocol sets with the same number of
protocols as the selected battery. They show whether selection beats chance.

**Runtime-matched random baseline.** Random protocol sets whose total cost does not exceed
the selected battery's cost.

## 7. Validity layers

**Structural validity (schema validity).** The files obey the NeuroML schema and its
logical checks. NeuroSem's authoritative check is `jnml -validate`, and libNeuroML's check is
recorded for information only.

**Execution.** The simulator builds and runs the model to completion and writes readable
output. Failures are build errors, runtime errors or timeouts (class 2).

**Numerical convergence (as a validity layer).** Results are stable under time-step
refinement, so a difference reflects the model rather than solver error.

**Tested behaviour preservation.** The variant's features agree with the reference within
tolerance on every protocol tested. This is the *empirical semantic certificate*.

**Biological validity.** Whether the model reproduces real neurons' behaviour. NeuroSem does
not test this. It compares a variant only against its own reference model.

## 8. Testing methods

**Mutation testing.** Deliberately inserting known faults to measure whether a test suite
catches them.

**Mutation operator.** A rule that makes one kind of change at one *site* (for example
`scale_conductance` on `IM_all/@condDensity`, factor 0.5).

**Mutation family.** A group of related operators: stimulus, biophysical, reference or
numerical.

**Site.** One concrete place in a model where an operator can act, identified by file,
locator and parameters.

**Single-fault mutant.** A mutant with exactly one change. Compound faults belong only in a
secondary stress test.

**Metamorphic testing.** Checking a necessary relation between related runs instead of
knowing the exact correct output. Example: converting units must not change behaviour.

**False positive.** A detection on a valid transformation or no-change control.
The *false-positive rate* is the fraction of such controls detected.

**Detection rate.** The fraction of admissible mutants that a validation strategy
detects.

**Silent-survival rate.** The fraction of admissible mutants that pass the canonical test,
i.e. class 6 / (class 5 + class 6).

## 9. Statistics

**Primary endpoint.** The single pre-declared outcome that decides the main hypothesis:
held-out mutant detection rate under the selected battery versus canonical regression.

**Secondary endpoint.** A pre-declared supporting outcome (for example false-positive rate).
Secondary endpoints are reported, but they cannot rescue a failed primary endpoint.

**Unit of analysis.** The thing each outcome is measured on. For detection rates it is one
admissible held-out mutant.

**Denominator.** The number of admissible (class 5 or 6) mutants in the evaluated set.
Crashes, invalid files and equivalent mutants are reported separately and are never in it.

**Cluster.** A group of observations that are not independent. Mutants of the same base
model form a cluster, and models from the same paper and channel files form a larger
*source family*.

**Paired binary outcomes.** Each mutant is scored by two strategies (detected yes/no by
each). The four counts are both, only A, only B and neither.

**Discordant pairs.** Mutants detected by exactly one of two strategies (only A or only B).
Paired tests use only these.

**Cluster bootstrap.** Estimating uncertainty by resampling whole base models with
replacement, keeping all of each model's mutants together, and recomputing the statistic
many times. It respects the correlation between mutants of one model.

**Percentile confidence interval.** The range between, for example, the 2.5th and 97.5th
percentiles of the bootstrap distribution.

**Exact McNemar test.** A paired test that asks whether "only A" and "only B" discordant
counts could plausibly come from a fair coin (two-sided exact binomial). It assumes
independent mutants, which clustering violates.

**Cluster permutation (sign-flip) test.** A test that randomly swaps the two strategies'
labels for whole clusters and asks how often a difference as large as observed appears.
With few clusters it cannot produce small p-values.

**Sensitivity analysis.** Re-running an analysis under changed assumptions (for example
looser tolerances) to check that conclusions do not hinge on one choice.

**Power analysis.** A calculation of the sample size needed to detect an effect of a given
size. None has been done yet: the specification's model and mutant counts are planning
bounds only.
