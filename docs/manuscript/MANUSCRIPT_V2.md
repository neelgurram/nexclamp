# Canonical regression tests miss behaviour-changing faults in computational neuron models: a preregistered held-out evaluation

*Draft v2.0, 2026-09-23. Prepared for* Neuroinformatics *(Springer Nature), Original Article. Items in
[square brackets] are open and are listed at the end of this file; they are not part of the submitted text.*

---

## Title page

**Title.** Canonical regression tests miss behaviour-changing faults in computational neuron models: a
preregistered held-out evaluation

**Authors.**

Neel Gurram¹ · Samyak Singh¹ · Naithik Somisetti²

¹ Florida Atlantic University, Jupiter, FL, USA
² Florida Atlantic University, Boca Raton, FL, USA

**Corresponding author.** Neel Gurram, gurramn2025@fau.edu

**ORCID.** Neel Gurram https://orcid.org/0009-0009-2441-0825 · Samyak Singh https://orcid.org/0009-0003-5825-3975 · Naithik Somisetti https://orcid.org/0009-0009-6638-678X

**Acknowledgements.** We thank the Open Source Brain and NeuroML communities for maintaining the public
model repositories this study depends on. [Add any teacher, mentor or institutional acknowledgement.]

---

## Abstract

Computational neuron models are routinely modified: refactored, converted between units, and ported
between formats and simulators. The usual check that such a change preserved behaviour is to re-run the
single simulation shipped with the model, a canonical regression test. How much protection that gives
has never been measured. We seeded 120 controlled single-site faults into six NeuroML neuron models
that were never used during method development, together with 48 behaviour-preserving transformations
and 18 numerical stress tests, and compared the canonical test against a three-protocol current-clamp
battery selected in advance on seven development models. Detection used electrophysiological features
with tolerances calibrated against each model's own discretisation error, and required reproduction at
two integration step sizes. The design, endpoint, thresholds and analysis were preregistered before any
held-out model was simulated. Of 82 faults that changed behaviour, the canonical test detected 69
(0.841) and the battery 80 (0.976), a paired difference of 0.134 (95% cluster-bootstrap interval 0.013
to 0.221). No behaviour-preserving transformation was flagged by any strategy (0 of 48). Six faults on
three models escaped the canonical test on both its summary features and its full voltage trace; all
six were detected by the battery. Losses were concentrated in mild faults (0.70 versus 0.95). A single
shipped simulation is not sufficient evidence that a modified neuron model still behaves as before.

**Keywords.** Neuron model validation · Regression testing · Mutation testing · NeuroML ·
Electrophysiological features · Preregistration

---

## 1 Introduction

Computational models of single neurons are long-lived research artefacts. A published model is typically
re-implemented, converted between description languages, refactored, ported to another simulator, or
edited to change a parameter, often by people other than its original authors. Standardised formats and
shared repositories have made this reuse routine: NeuroML describes models in a simulator-independent
form (Sinha et al., 2025), and repositories such as NeuroML-DB and Open Source Brain host and
characterise large numbers of them (Birgiolas et al., 2023). Most published models ship with a harness
that reproduces one reference simulation.

Each modification raises the same question: does the edited model still behave like the original? In
practice the answer usually rests on a canonical regression test. The shipped simulation is re-run and
its output compared with a stored reference, sometimes automatically, as in the Open Source Brain model
validation framework (Marin & Gleeson, 2026). A model that passes is treated as unchanged.

This is a reasonable heuristic, but its protective value has not been quantified. A single stimulus
probes a small part of a neuron's input–output behaviour. A change to a slowly activating current may be
invisible during a brief current step and obvious during a long one. A shift in a channel's activation
curve may alter behaviour only near threshold, or only under a slowly rising input. Work on constructing
neuron models has long recognised that the choice of stimulus determines which properties a model is
constrained by (Druckmann et al., 2011; Van Geit et al., 2016; Reva et al., 2023), and validation suites
such as NeuronUnit and HippoUnit compare models with experimental data under multiple protocols (Gerkin
et al., 2019; Sáray et al., 2021; Appukuttan & Davison, 2022). What is missing is a measurement of how
often the canonical test misses a change that does alter behaviour, and whether a small, fixed set of
additional protocols closes that gap on models it was not designed for.

Software engineering offers a direct way to ask this. Mutation testing seeds known faults into a system
and measures which tests detect them (Papadakis et al., 2019); it has been applied to scientific software
(Hook & Kelly, 2009; Kelly et al., 2011) and to simulation models of dynamic systems (Zhan & Clark, 2005;
Matinnejad et al., 2019). Regression test selection chooses a small suite that retains most of the
fault-detecting power of a larger one (Yoo & Harman, 2012). Behaviour-preserving transformations, the
counterpart of mutants, check that a suite does not raise false alarms, an idea close to metamorphic
testing (Segura et al., 2016). None of this has been used to quantify the protection that canonical
regression gives neuron models.

We therefore asked two questions. First, what fraction of behaviour-changing faults does the canonical
regression test detect? Second, does a compact battery of perturbation protocols, chosen on one set of
models, detect faults the canonical test misses on models it has never seen? To keep the answer honest we
separated development from evaluation: every method choice was fixed on development models, the
evaluation models and one mutation family were held out, and the design was preregistered before any
held-out simulation. We committed in advance to publishing either outcome, including the outcome that
canonical regression is adequate.

## 2 Materials and Methods

### 2.1 Design and preregistration

The study had a development phase and a single confirmatory evaluation. During development we built and
tested the pipeline on seven models in two pilots (Section 2.8) and fixed every parameter: the candidate
protocols, the features, the tolerance rule, the fault operators and severities, the classification rules,
and the analysis. We then hash-locked the configuration, assigned six models and one mutation family to a
held-out set, and registered the design at AsPredicted (#312455, 19 September 2026) before any held-out
model was mutated or simulated. The registration states the development results already known and the
direction in which they pointed. The confirmatory evaluation was released only after the registration was
verified, and it ran once. Any change to a locked file blocks the evaluation; this mechanism refused one
launch (Section 4.4).

### 2.2 Models

Candidate models came from public NeuroML repositories and were screened on thirteen prespecified criteria
applied to the unmodified model only: recorded provenance, redistribution rights, required files, NeuroML
validity, unattended execution, an interpretable voltage trace, a resolvable recording location, a
measurable rheobase with spiking at twice rheobase, deterministic re-execution, feature stability under
refinement, a runtime budget, at least three applicable mutation operators, and compatibility with every
protocol (Online Resource 1). Screening examined reference behaviour only; no mutation outcome was
available at screening.

Six models from four source families met all criteria and came from sources never used in development
(Table 1). All are single-compartment conductance-based cells, because the reference simulator integrates
single-compartment NeuroML models directly. Development used seven further models from other sources
(Section 2.8).

### 2.3 Faults and controls

Faults were single, documented edits to a model's NeuroML files, produced by operators in three families.
**Biophysical:** scaling a maximal conductance, shifting a reversal potential, scaling membrane
capacitance, scaling a gate time constant. **Reference:** pointing a channel density at a different
channel, omitting an include, duplicating a conductance, swapping in a channel of the same ion species.
**Kinetics** (held out from protocol selection): shifting a gate's activation midpoint, scaling its slope,
shifting the midpoint of a forward rate.

Magnitude operators were applied at two prespecified severities, mild and strong, defined by bands of
|ln k| for multiplicative changes and of millivolts for shifts. Sites were chosen by a seeded generator
fixed before generation. Every edit records the file, element, attribute, and old and new values.

Two further strata were generated and analysed separately. **Controls** were eight kinds of
behaviour-preserving transformation per model: unit conversion, whitespace reformatting, added comments,
equivalent numeric literals, consistent renaming of an identifier, moving a component into an included
file, reordering independent elements, and writing an inherited default explicitly. **Numerical stress
tests** changed the integration step, the solver setting or the recording resolution; these probe
numerical robustness and are never counted as semantic faults. The frozen generator produced 186 variants:
120 faults, 48 controls and 18 numerical stress tests.

### 2.4 Protocols and features

The canonical test was each model's shipped harness, run unchanged. The candidate protocols were eight
current-clamp stimuli scaled to each model's measured rheobase: a weak step (0.5 × rheobase), a rheobase
search, a step at 2 × rheobase, a long step (1.5 × rheobase, 2 s), a ramp from 0 to 3 × rheobase over 1 s,
a hyperpolarising step, a rebound protocol, and a short suprathreshold pulse (3 ms at 10 × rheobase).
Every protocol began with a 300 ms settling period.

Features were extracted with the eFEL library (Mandge et al., 2026): spike count, first-spike latency,
last interspike interval, adaptation index, action-potential amplitude and afterhyperpolarisation depth
for spiking protocols, and steady-state voltage and deflection for subthreshold protocols. A feature
defined in one model and undefined in the other counted as a difference.

### 2.5 Tolerances and the detection rule

Each feature difference was compared with a tolerance calibrated on the unmodified model,

τ = max(absolute floor, relative term × |f_h|, 3 × |f_h − f_h/2|),

where f_h and f_h/2 are the reference feature at the nominal step h (0.005 ms) and at half that step. The
final term makes the threshold at least three times the model's own discretisation error, so a difference
the solver could produce by itself cannot count. Floors and relative terms were fixed per feature before
any held-out simulation (Online Resource 1).

A strategy **detected** a fault when one of its protocols showed a difference beyond tolerance, for the
same protocol and feature, at h **and** at h/2. Faults that the canonical test missed but another protocol
detected were re-simulated at h/4 for confirmation.

Full voltage traces were compared as a separate validation level that is never merged with the feature
comparison. A trace differed when its spike count differed, when any spike time shifted by more than
τ_shift = max(0.5 ms, 3 × the reference's own h versus h/2 shift), or when the root-mean-square difference
exceeded τ_rmse = max(0.5 mV, 3 × the reference's own h versus h/2 value). A model whose canonical trace
tolerance could not be calibrated would be reported as unclassifiable at that level.

### 2.6 Classification and protocol selection

Each fault was classified in order: structurally invalid, non-executable, numerically unstable, equivalent
within the tested domain (no reproducible feature difference on any protocol), non-equivalent and detected
by the canonical test, or non-equivalent but missed by it (silent under canonical). Faults in the last two
classes are **admissible**: they changed behaviour, and they form the denominator of the primary endpoint.

The battery was selected on the development models alone, by greedy maximum coverage of their admissible
faults under a budget of k = 4 protocols, with ties broken by cost and then by identifier. The kinetics
family was excluded from selection. The greedy rule stopped at three protocols, because a fourth added no
coverage: the long step, the 2 × step, and the ramp.

### 2.7 Endpoints and statistical analysis

The **primary endpoint** was the paired difference in detection rate between the selected battery and the
canonical test, Δ = DR_battery − DR_canonical, over admissible held-out faults. The battery was evaluated
without the canonical protocol, so the comparison is between two alternative checks rather than between a
test and a superset of it. We prespecified Δ ≥ 0.10 as the smallest material difference, and a canonical
detection rate ≥ 0.95 as the criterion for calling canonical regression adequate.

The interval for Δ was a cluster percentile bootstrap resampling base models (B = 10,000, seed 20260917),
as registered. Supporting tests were an exact McNemar test on discordant pairs, which treats faults as
independent, and an exact cluster permutation test on per-model differences, which does not. Because two
pairs of models share a source, we additionally report the bootstrap with source family as the cluster.
The result was prespecified as inconclusive if more than 10% of controls were flagged, if more than half
of apparent canonical survivors failed h/4 confirmation, or if at least 25% of tolerance entries were
excluded for refinement instability.

Prespecified secondary analyses were: detection by random protocol batteries matched for size (all 56
three-protocol subsets of the eight candidates) and for cost (10,000 random batteries within the selected
battery's budget); the silent-survival rate; control false-positive rates; detection by mutation family
and severity; coverage against the number of protocols; cost per detection; and robustness to tolerance
multipliers of 0.5, 1, 2 and 4. Analyses added after the confirmatory run are labelled exploratory
(Sections 3.7 and 4.4).

### 2.8 Development work

Two pilots preceded the evaluation and are reported descriptively (Online Resource 2). In the first (two
closely related models, 22 admissible faults) the canonical test detected all 22 and the battery 19. In
the second (five further models, 88 primary semantic faults, 40 controls) canonical detection counting
either validation level was 0.921; nine faults were missed at feature level, two of which also survived
full-trace comparison, and no control was flagged. During the second pilot we found and corrected an
analysis defect that had counted faults as full-trace survivors on a model whose canonical trace tolerance
could not be calibrated; the correction, which introduced the unclassifiable category of Section 2.5, was
made before the evaluation and is part of the frozen pipeline. Operator validation had observed the
canonical outcome of nine second-pilot faults before that pilot ran, so the pilot is reported both over
all faults and over the 79 unexposed ones. No held-out model is affected: none was mutated before the
confirmatory run.

### 2.9 Software, reproducibility and use of AI tools

The method is implemented in NexClamp (version 0.2.0.dev0), an open-source Python package (Apache-2.0)
that runs the protocols, extracts the features, calibrates the tolerances, generates the faults and
controls, selects the battery, classifies the outcomes and seals each campaign. Simulations used jNeuroML
0.14.0 and jLEMS 0.12.0 on Temurin JDK 21.0.12.1+1, with Python 3.12.10, pyNeuroML 1.3.22, libNeuroML
0.6.7, eFEL 5.7.34 and NumPy 2, on twelve parallel workers. Every simulation is stored write-once under a
content-addressed identifier together with its inputs, software versions and outputs. The confirmatory
campaign was archived and sealed after completion (17,424 files, each with a SHA-256 checksum), and the
pipeline refuses to write into a sealed campaign.

**Use of AI tools.** The analysis software, parts of the documentation and drafts of this manuscript were
produced with the assistance of a large language model (Claude, Anthropic), used under author direction
and logged throughout the project. All AI-assisted code was reviewed and tested by the authors; every
number reported here is produced by deterministic, version-controlled code from recorded outputs, and the
authors verified the outputs against the raw records. The authors take full responsibility for the content
of this article. No AI system is an author.

## 3 Results

### 3.1 Attrition and controls

Of 120 faults, 114 were schema-valid, 112 executed, 109 were numerically stable, and 82 changed behaviour
and are admissible; 27 were equivalent within the tested domain (Fig. 5, Table 2). If faults whose only
detected change appeared in the full voltage trace are also counted, 94 changed behaviour; we report the
frozen feature-level definition (82) as primary and give both.

No control was flagged by any strategy: 0 of 48 at feature level and 0 of 48 at trace level (exact 95%
upper bound 0.074), including at half the calibrated tolerance. None of the prespecified inconclusive
conditions occurred: no control was flagged, 0 of 18 apparent canonical survivors failed h/4 confirmation,
and no tolerance entry was excluded for refinement instability.

### 3.2 Primary endpoint

The canonical test detected 69 of 82 admissible faults (0.841, 95% cluster interval 0.78–0.91) and the
selected battery 80 of 82 (0.976, 0.92–1.00) (Fig. 1). Paired counts were: both 67, battery only 13,
canonical only 2, neither 0. The difference was Δ = 0.134, 95% cluster-bootstrap interval 0.013 to 0.221
(Fig. 2). The exact McNemar test gave p = 0.007; the cluster permutation test, with six clusters and a
smallest attainable p of 0.031, gave p = 0.156. With source family as the cluster the interval was 0.040
to 0.232, flagged by the analysis code as unreliable because only four clusters remain.

The battery detected more faults than the canonical test on five of the six models, by two to four faults
each. On `traub2005_testseg_all` the canonical test detected all 12 admissible faults and the battery 10;
the two it missed, a shifted gate midpoint and a shifted reversal potential, were detected only by the
canonical protocol.

Against the preregistered criteria: the point estimate exceeds the material difference of 0.10 and the
interval excludes zero, but its lower end lies below 0.10, so a material advantage is supported by the
estimate without being established by the interval. Canonical regression did not meet the adequacy
criterion of 0.95.

### 3.3 Faults that escape the canonical test entirely

The feature comparison is one way to read the canonical simulation; its full voltage trace is another. Of
the 94 faults with any detected change, the canonical features detected 69 and the canonical full trace 87
(features only 1, trace only 19, either 88, neither 6; Fig. 3). The trace comparison was calibrated on all
six models and fired on 11 to 17 faults per model, so it was an active test rather than an inert one.

Six faults were missed by the canonical test at both levels: four on `hay2011_soma`, one on `bbp2015_soma`
and one on `migliore2005_ca1_soma` (Table 3). All six were detected by the battery, reproducibly at h, h/2
and h/4, through changes in spike count or spike timing. They include a 10% increase in the
high-voltage-activated calcium conductance of the Hay cell, which reduced the number of spikes during the
long step from 14 to 13 while leaving the canonical simulation within tolerance; two changes to the slow
M-current (halving its conductance; shifting its reversal potential by −10 mV) that altered spike timing
under the 2 × step; and changes to calcium- and A-type potassium-channel gating kinetics that altered
spike count or timing under the long step and the ramp. These cases meet the criterion for hidden drift
fixed before the second pilot: at least two confirmed full-trace survivors across at least two models.

### 3.4 Where canonical testing falls short

The canonical test's losses were concentrated in mild faults, which it detected at 0.70 against the
battery's 0.95; for strong faults the rates were 0.97 and 1.00 (Table 4). By fault type it missed most
often after changes to maximal conductance (0.65 versus 1.00) and to gate time constants (2 of 5 versus
5 of 5). The silent-survival rate, the fraction of admissible faults missed by the canonical test, was
0.159 (95% cluster interval 0.089–0.222). No fault was detected by the canonical protocol at h only.

For the held-out kinetics family, which protocol selection never saw, the canonical test detected 0.864
and the battery 0.955 (22 faults; Δ = 0.091, interval −0.10 to 0.22, flagged unreliable because few
models contributed discordant faults). We therefore draw no conclusion about generalisation to the unseen
family. For the families seen during development the difference was 0.150 (interval 0.036 to 0.232).

### 3.5 Protocol selection, coverage and cost

The selected battery detected more faults than 55 of the 56 possible three-protocol batteries drawn from
the same candidates (mean 0.846; share at least as good as the selected battery 0.018) and than 97% of
10,000 random batteries of equal cost (mean 0.909; share at least as good 0.030) (Fig. 4). Selection on
development models therefore transferred to unseen models. The long step alone reached 90% of the coverage
achieved by all protocols combined, and the three selected protocols reached 95%; 100% is not reached
without the canonical protocol, because two faults were detected only by it. Per variant the battery cost
1.0 million integration cell-steps against 0.31 million for the canonical test (3.3 ×), and per detected
fault 1.03 million against 0.36 million.

### 3.6 Tolerance sensitivity

Across tolerance multipliers of 0.5, 1, 2 and 4, no control was flagged at any multiplier, while the
fraction of faults silent under the canonical test rose from 0.087 to 0.116, 0.152 and 0.203 as tolerances
loosened (computed over all 138 faults and stress tests). The main finding does not depend on the
tolerance being tight.

### 3.7 Cross-simulator reproduction (exploratory)

The evaluation used one simulator. To test whether the reference behaviour is simulator-specific, each
held-out model was exported to NEURON and its canonical simulation re-run under NEURON 9.0.2. All six
models exported, compiled and ran. Spike counts were identical in every case (7, 5, 9, 4, 7 and 4), and
matched each model's own published NEURON reference. The largest difference in any spike time was 0.009 to
0.182 ms and whole-trace differences were 0.19 to 2.18 mV root-mean-square, consistent with two
integrators rather than two behaviours. This check was added after the confirmatory run and is
descriptive: the study's tolerances are calibrated within one integrator and do not transfer across two.
It supports the reference simulations against which detections are measured; it does not re-test the
faults.

### 3.8 Verification of the fault sample

An automated re-check re-derived, from the raw files rather than the pipeline's summaries, the edit, the
class and every detection for 25 faults (a preregistered random sample of 20 plus the six canonical
survivors, one of which fell in both). For each, the differences between the edited and unmodified model
files were exactly the recorded edit and matched the operator's declared meaning; the class re-derived
correctly; all recorded feature detections recomputed from the per-run feature files; spike-count
detections were confirmed by recounting spikes directly from the stored voltage traces; and all 227
full-trace detections recomputed. [The independent human audit of the same faults by two authors is in
progress; its results and any disagreements will be reported here.]

## 4 Discussion

On six neuron models never used to develop the method, re-running the shipped simulation missed about one
in six faults that changed the model's behaviour, while a three-protocol battery chosen in advance missed
two of 82. Six faults went unnoticed by the canonical test even when its entire voltage trace was
compared, which is the strictest form a canonical regression test can take. No behaviour-preserving
transformation was flagged by anything. The pilots had suggested that canonical testing was nearly
sufficient; the preregistered held-out evaluation, registered with that expectation stated, did not bear
this out.

### 4.1 Why the misses happen, and what to do about them

The pattern of misses is intelligible. The canonical harnesses are short: their stimulus windows span 60
to 300 ms, and the depolarising steps in four of the six models last 60 to 100 ms. Faults that act slowly,
such as a change to the M-current or to a calcium conductance that shapes adaptation, alter firing only as
a step continues, near threshold, or under a slowly rising input. The long step, the stronger step and the
ramp sample exactly those regimes. Faults with large effects were caught by almost any check; the gap lies
in mild faults, which are also the kind most likely to be introduced unnoticed by a unit conversion or a
hand edit.

Two practical consequences follow. First, most of the canonical test's shortfall at feature level is
recovered by comparing its full voltage trace (88 of 94 against 69 of 94), at no additional simulation
cost. Tools that compare only summary features of the shipped simulation should compare traces as well.
Second, the remaining misses require other stimuli, and a short battery suffices: the long step alone
reached 90% of the achievable coverage, and the three selected protocols cost about three times the
canonical simulation, which is small against the effort of reusing a model.

### 4.2 Relation to existing work

The result is consistent with work on constructing neuron models, where the stimulus set determines which
properties a model is constrained by (Druckmann et al., 2011; Van Geit et al., 2016; Reva et al., 2023),
and with multi-protocol validation suites that compare models with experimental data (Gerkin et al., 2019;
Sáray et al., 2021; Appukuttan & Davison, 2022). Those tools ask whether a model matches biology. Our
question is narrower and complementary: whether a modified model still matches its own original. We show
that this question, usually answered with one simulation, needs more than one. Methodologically the study
imports mutation testing and test selection from software engineering (Papadakis et al., 2019; Yoo &
Harman, 2012) into neuron model validation, with behaviour-preserving transformations as the specificity
control (Segura et al., 2016).

### 4.3 Limitations

The evaluation used six models from four source families, so the intervals are wide and the model-level
permutation test is underpowered by construction; the interval for Δ excludes zero but does not establish
a material advantage. All models are single-compartment, so dendritic faults were out of scope. The faults
were evaluated in a single simulator, although every held-out model's reference behaviour reproduced in
NEURON (Section 3.7). Faults were synthetic single-site edits; real modification errors may be larger,
compound or correlated. Admissibility depends on the definition used (82 at feature level, 94 including
trace-only changes), and both are reported. The result for the held-out kinetics family is inconclusive.
The frozen generator produced 186 variants against a preregistered estimate of roughly 100 to 150, and
selection produced a three-protocol battery under a four-protocol budget; both are reported as they
occurred. [The human audit is in progress.]

### 4.4 Deviations from the registration

All deviations are logged with dates and reasons (Online Resource 2). Those bearing on the evaluation:
(i) the runtime screening criterion was raised from 1,800 s to 4,200 s per variant before any held-out
model was mutated, because the lower budget left no eligible models; (ii) the registration estimated
roughly 100 to 150 variants and the frozen generator produced 186; (iii) the battery contains three
protocols under the registered budget of four; (iv) two co-authors joined after registration; (v) a
hash-locked planning document was edited after the freeze to add them, the integrity check refused to
start the evaluation, and the document was restored byte-for-byte before the run, with no change to any
hypothesis, endpoint, split or analysis; (vi) source-family clustering is reported as a sensitivity
analysis alongside the registered model-level clustering; and (vii) the cross-simulator check (Section
3.7) was added after the confirmatory run and is exploratory.

## 5 Conclusions

A canonical regression test is not sufficient evidence that a modified neuron model still behaves as
before. On unseen models it missed about one in six behaviour-changing faults, some of which its full
voltage trace also missed. Comparing that trace, rather than only its summary features, recovers much of
the gap at no extra cost, and a short battery of standard current-clamp protocols recovers nearly all of
it without false alarms. We recommend both as routine checks whenever neuron models are edited, converted
or ported.

## Information Sharing Statement

NexClamp, the software used for every step of this study, is open-source under the Apache-2.0 licence and
is distributed from a public repository (https://github.com/neelgurram/nexclamp) with installation and usage documentation; the
exact version that produced the results reported here is archived with a persistent identifier ([Zenodo
DOI], version 0.2.0.dev0). The frozen study configuration, the model manifest with per-model licences and
pinned upstream commits, the preregistration record, every per-variant record (edits, classifications,
detections, tolerances), the analysis outputs, and the scripts that regenerate every table and figure in
this article are included in that archive. The complete raw simulation output of the confirmatory campaign
(17,424 files, 4.1 GB, including all voltage traces) is deposited as a separate archived dataset (https://doi.org/10.5281/zenodo.22928016) together with the SHA-256 manifest that verifies it. The preregistration is publicly readable at
https://aspredicted.org/q2ag7w.pdf (AsPredicted #312455).

All neuron models analysed here are third-party open-source NeuroML models, redistributed under their own
licences (MIT or GPL-2.0) with their source repositories and commit identifiers recorded in Online
Resource 1: the Hay et al. (2011) and Blue Brain (Markram et al., 2015) channel sets, the Traub et al.
(2005) test cells, the Smith et al. (2013) channel set, and the Migliore et al. (2005) CA1 cell, all
obtained from Open Source Brain. Simulations used jNeuroML 0.14.0/jLEMS 0.12.0 and, for the exploratory
cross-simulator check, NEURON 9.0.2, all publicly available.

## Statements and Declarations

**Funding.** This research received no specific grant from any funding agency in the public, commercial or
not-for-profit sectors.

**Competing interests.** The authors declare no competing financial or non-financial interests.

**Ethics approval.** Not applicable. The study involved no human participants, no animals and no personal
data; it analyses published computational models only.

**Consent to participate / Consent for publication.** Not applicable.

**Author contributions.** Neel Gurram: conceptualisation, methodology, software, investigation, formal
analysis, data curation, validation, visualisation, project administration, writing (original draft, and
review and editing). Samyak Singh: formal analysis, validation, writing (review and editing). Naithik
Somisetti: formal analysis, validation, writing (review and editing). All authors read, critically revised
and approved the final manuscript and agree to be accountable for all aspects of the work.

**Data availability.** All data supporting the results are publicly archived as described in the
Information Sharing Statement: derived per-variant records and analysis outputs in the software and
results archive ([Zenodo DOI]), and the complete raw simulation output in the dataset archive (https://doi.org/10.5281/zenodo.22928016). No restrictions apply.

**Code availability.** NexClamp is available under Apache-2.0 at https://github.com/neelgurram/nexclamp and archived at [Zenodo
DOI]. The exact commit, configuration hashes and environment used for the confirmatory campaign are
recorded in the archive and in Online Resource 1.

## References

See `references_apa7.md`, inserted here at compile time (APA 7, alphabetical).

## Figure captions

**Fig. 1** Detection of admissible faults on each held-out model. Bars show the fraction detected by the
canonical regression test (solid) and by the selected three-protocol battery (hatched); counts above each
bar are detected/admissible. Dashed lines mark the pooled rates with their 95% cluster-bootstrap
intervals (canonical 0.841, battery 0.976); the dotted line marks the preregistered adequacy threshold of
0.95. n = 82 faults on six models never used in development; a detection must reproduce at h and h/2

**Fig. 2** Primary endpoint. Grey circles show the per-model difference in detection rate (battery minus
canonical); the green diamond shows the pooled difference with its 95% cluster-bootstrap interval
(0.134; 0.013 to 0.221). The dashed vertical line marks the preregistered material difference of 0.10.
The interval excludes zero; its lower end lies below 0.10. Exact McNemar p = 0.007 treating faults as
independent; exact cluster permutation p = 0.156 over six models, for which the smallest attainable p is
0.031

**Fig. 3** Validation levels, reported separately and never merged: faults detected by the canonical
test's summary features, by the canonical test's full voltage trace, and by the other protocols, for each
model. Dashed lines mark the number of faults with any detected change (n = 94 in total). Six faults
escape the canonical test at both levels

**Fig. 4** Held-out detection rate of random protocol batteries compared with the selected battery. **a**
All 56 possible three-protocol batteries drawn from the eight candidates. **b** 10,000 random batteries
within the selected battery's computational budget. Vertical lines mark the selected battery (0.976) and
the canonical test (0.841). The share of random batteries at least as good as the selected one is 0.018
in **a** and 0.030 in **b**

**Fig. 5** Attrition of the 120 primary semantic faults through schema validation, execution, numerical
stability and admissibility, with the exact count at each stage

## Tables

**Table 1** Held-out models: source, channel complement and canonical stimulus

| Model | Source | Channels (summary) | Canonical stimulus |
|---|---|---|---|
| `hay2011_soma` | Hay et al. (2011) layer-5b pyramidal channel set | Na, K, Ca (HVA, LVA), Ih, SK, M; Ca pool | −0.01 nA at 100–200 ms; +0.05 nA at 300–400 ms |
| `bbp2015_soma` | Markram et al. (2015) Blue Brain channel set | as Hay, plus NaTs2_t and Kd | as above |
| `traub2005_testseg2` | Traub et al. (2005) channel test cell 2 | Na and K subset; no Ca, no Ih | +0.08 nA at 20–80 ms |
| `traub2005_testseg_all` | Traub et al. (2005) all-channel test cell | adds Ca, AHP and anomalous rectifier; Ca pool | +0.08 nA at 20–80 ms |
| `smith2013_singlecomp` | Smith et al. (2013) layer-2/3 pyramidal channel set | Na, Kv, M, K(Ca), Ca, T | shipped step (analysis window 100–400 ms) |
| `migliore2005_ca1_soma` | Migliore et al. (2005) CA1 pyramidal soma | Na (two types), K (A, DR), Ih | +0.038 nA at 20–80 ms |

`hay2011_soma` and `bbp2015_soma` share most of a channel set and the two Traub cells come from one
publication, so the six models form four source families.

**Table 2** Attrition of the 120 primary semantic faults

| Stage | Count |
|---|---|
| Faults generated | 120 |
| Schema-valid | 114 |
| Executable | 112 |
| Numerically stable | 109 |
| Admissible (behaviour changed; frozen feature-level definition) | 82 |
| Equivalent within the tested domain | 27 |

**Table 3** The six faults missed by the canonical test on both summary features and full voltage trace

| Fault | Model | Edit | Detected by (level) |
|---|---|---|---|
| `scale_conductance` (mild) | `hay2011_soma` | Ca_HVA conductance × 1.1 | long step: spike count, last interspike interval; ramp: spike timing |
| `scale_conductance` (strong) | `hay2011_soma` | M-current conductance × 0.5 | 2 × step: spike timing (trace) |
| `shift_reversal` (strong) | `hay2011_soma` | M-current reversal −85 → −95 mV | 2 × step: spike timing (trace) |
| `scale_gate_time_constant` (mild) | `hay2011_soma` | Ca_HVA activation rates × 1.25 | long step: spike count; ramp: spike timing |
| `scale_gate_time_constant` (mild) | `bbp2015_soma` | Ca_HVA activation rates × 1.25 | long step: spike count; ramp: spike timing |
| `scale_gate_time_constant` (mild) | `migliore2005_ca1_soma` | A-type K (kad) gate Q10 × 0.8 | 2 × step, long step, ramp: spike timing, trace RMS |

**Table 4** Detection by fault group (admissible faults)

| Group | n | Canonical | Battery |
|---|---|---|---|
| All | 82 | 0.841 | 0.976 |
| Mild severity | 40 | 0.700 | 0.950 |
| Strong severity | 31 | 0.968 | 1.000 |
| No severity (reference swaps) | 11 | 1.000 | 1.000 |
| Maximal conductance | 17 | 0.647 | 1.000 |
| Gate time constant | 5 | 0.400 | 1.000 |
| Gate voltage dependence (includes the held-out kinetics family) | 22 | 0.864 | 0.955 |
| Reversal potential | 15 | 0.933 | 0.933 |
| Passive membrane | 12 | 1.000 | 1.000 |
| Mechanism composition | 11 | 1.000 | 1.000 |

---

## Open items before submission (not part of the submitted text)

1. **Human audit** (Sections 3.8, 4.3): results and disagreements from the two co-auditors.
2. **Repository URL and two Zenodo DOIs** (software/results archive and raw-trace dataset). The journal
   does not accept "available on request", so the 4.1 GB raw archive must be deposited.
3. **Acknowledgements**: add any mentor, teacher or institutional support.
4. **All authors** read, critically revise and approve; the journal applies ICMJE criteria, so every
   author must satisfy all three conditions (contribution, critical revision, final approval).
5. **Compile to Word**: insert `references_apa7.md` under References, place each figure near its first
   citation, 10-point Times Roman, automatic page numbers, figures as `Fig1.eps`–`Fig5.eps`
   (`results/figures/heldout-v1/journal/`).
6. **Cover letter** stating preregistration, the pre-commitment to publishing either outcome, and public
   code and data.
