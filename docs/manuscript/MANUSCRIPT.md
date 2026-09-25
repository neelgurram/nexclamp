# Canonical regression tests miss behaviour-changing faults in neuron models: a preregistered held-out evaluation of perturbation protocol batteries

**Neel Gurram**¹\*, **Samyak Singh**¹, **Naithik Somisetti**²

¹ Florida Atlantic University, Jupiter, FL, USA
² Florida Atlantic University, Boca Raton, FL, USA

\* Corresponding author: gurramn2025@fau.edu

*Draft v0.1, 2026-09-22. Target journal: Neuroinformatics (Springer), original article. Items in
[square brackets] are open and are listed at the end.*

---

## Abstract

Computational neuron models are routinely modified: refactored, converted between units, ported
between formats. The usual check that a change preserved behaviour is to re-run the one simulation
shipped with the model and compare its output, a canonical regression test. How much protection
this gives has not been measured. We seeded 120 controlled single-site faults into six NeuroML
neuron models that were never used during method development, alongside 48 behaviour-preserving
transformations, and compared the canonical test with a three-protocol current-clamp battery
selected in advance on seven development models. Detection used electrophysiological features
with tolerances calibrated against each model's own numerical error and required reproduction at
two integration step sizes. The design, endpoint, thresholds and analysis were preregistered
before any held-out simulation (AsPredicted #312455). Of 82 faults that changed behaviour, the
canonical test detected 69 (0.841) and the battery 80 (0.976), a paired difference of +0.134
(95 % cluster-bootstrap interval +0.013 to +0.221). No control was flagged by any strategy (0 of
48). Six faults on three models escaped the canonical test even when its full voltage trace was
compared, and all six were detected by the battery. The canonical test's losses were concentrated
in mild faults (0.70 versus 0.95). The selected battery outperformed 55 of 56 random batteries of
equal size. With six models the uncertainty is wide, but a single shipped simulation is not
sufficient evidence that a modified neuron model still behaves as before.

**Keywords:** neuron model validation; regression testing; mutation testing; NeuroML;
electrophysiological features; preregistration

---

## 1 Introduction

Computational models of single neurons are long-lived research artefacts. A published model is
typically re-implemented, converted between description languages, refactored for performance,
ported to a new simulator, or edited to change a parameter, often by people other than its original
authors. Standardised formats and shared repositories have made this reuse routine: NeuroML
describes models in a simulator-independent form (Sinha et al. 2025), NeuroML-DB and Open Source
Brain host and characterise thousands of them (Birgiolas et al. 2023), and each model commonly
ships with a harness that reproduces a reference simulation.

Each modification raises the same question: does the edited model still behave like the original?
In practice the answer usually rests on a canonical regression test. The shipped simulation is
re-run and its output compared with a stored reference, sometimes automatically, as in the Open
Source Brain model validation framework (OMV; Marin and Gleeson, software). A model that passes is
treated as unchanged.

This is a reasonable heuristic, but it has not been tested. A single stimulus probes a small part of
a neuron's input-output behaviour. A change to a slowly activating current may be invisible during a
brief current step and obvious during a long one. A shift in a channel's activation curve may alter
behaviour only near threshold, or only in response to a ramp. Work on neuron model fitting has long
recognised that the choice of stimulus determines which properties a model is constrained by
(Druckmann et al. 2011), and validation suites such as NeuronUnit and HippoUnit compare models
against data under multiple protocols (Gerkin et al. 2019; Sáray et al. 2021). What is missing is a
measurement of how often the canonical test misses a change that does alter behaviour, and whether
a small, fixed set of additional protocols closes that gap on models it was not designed for.

Software engineering offers a direct way to ask this. Mutation testing seeds known faults into a
system and measures which tests detect them (Papadakis et al. 2019). It has been applied to
scientific software (Hook and Kelly 2009; Kelly et al. 2011) and to simulation models of dynamic
systems (Zhan and Clark 2005; Matinnejad et al. 2019). Regression test selection chooses a small
test suite that retains most of the fault-detecting power of a larger one (Yoo and Harman 2012).
Behaviour-preserving transformations, the counterpart of mutants, check that a test suite does not
raise false alarms, an idea close to metamorphic testing (Segura et al. 2016). None of these has
been used to quantify the protection that canonical regression gives neuron models.

We therefore asked two questions. First, what fraction of behaviour-changing faults does the
canonical regression test detect? Second, does a compact battery of perturbation protocols, chosen
on one set of models, detect faults the canonical test misses on models it has never seen? To keep
the answer honest we separated development from evaluation: every method choice was fixed on
development models, the evaluation models and one family of faults were held out, and the design
was preregistered before any held-out simulation. We committed in advance to publishing either
outcome, including that canonical regression is adequate.

## 2 Methods

### 2.1 Overview and preregistration

The study had a development phase and a single confirmatory evaluation. During development we built
and tested the pipeline on seven models in two pilots (section 2.8) and fixed every parameter: the
candidate protocols, the features, the tolerance rule, the fault operators and severities, the
classification rules and the analysis. We then froze the configuration (hash-locked; any change to
a locked file blocks the evaluation), assigned six models and one fault family to a held-out set,
and registered the design at AsPredicted (#312455, 19 September 2026, 17:29 PT) before any held-out
model was mutated or simulated. The registration states the development results that were already
known and the direction they pointed. The confirmatory run was started only after the registration
had been verified, and it ran once.

### 2.2 Models

Candidate models came from public NeuroML repositories. Each was screened on thirteen prespecified
criteria applied to the unmodified model only: licence permitting redistribution, a shipped harness,
schema validity, deterministic execution, a measurable rheobase, spiking under suprathreshold input,
numerical convergence between step sizes, and a runtime budget, among others (full list in Online
Resource 1). Screening never looked at how a model responded to a fault.

Six models met all criteria and came from sources never used in development (Table 1). All are
single-compartment conductance-based cells, because the reference simulator (jLEMS) integrates
single-compartment NeuroML models directly. Development used seven further models from other
sources (section 2.8).

**Table 1.** Held-out models.

| Model | Source | Channels (summary) | Canonical harness |
|---|---|---|---|
| `hay2011_soma` | Hay et al. 2011, L5b pyramidal channel set | Na, K, Ca (HVA, LVA), Ih, SK, M; Ca pool | −0.01 nA 100–200 ms, +0.05 nA 300–400 ms |
| `bbp2015_soma` | Markram et al. 2015, Blue Brain channel set | as Hay, plus NaTs2_t and Kd | as above |
| `traub2005_testseg2` | Traub et al. 2005, channel test cell 2 | Na and K subset; no Ca, no Ih | +0.08 nA 20–80 ms |
| `traub2005_testseg_all` | Traub et al. 2005, all-channel test cell | adds Ca, AHP, anomalous rectifier; Ca pool | +0.08 nA 20–80 ms |
| `smith2013_singlecomp` | Smith et al. 2013, L2/3 pyramidal channel set | Na, Kv, M, K(Ca), Ca, T | shipped step (analysis window 100–400 ms) |
| `migliore2005_ca1_soma` | Migliore et al. 2005, CA1 pyramidal soma | Na (2 types), K (A, DR), Ih | +0.038 nA 20–80 ms |

`hay2011_soma` and `bbp2015_soma` share most of a channel set, and the two Traub cells come from one
paper, so the six models form four source families; this is addressed in the analysis (section 2.7).

### 2.3 Faults and controls

Faults were single, documented edits to a model's NeuroML files, generated by operators in three
families.

- **Biophysical** (development family): scaling a maximal conductance, shifting a reversal
  potential, scaling membrane capacitance, scaling a gate time constant.
- **Reference** (development family): pointing a channel density at a different channel, omitting
  an include, duplicating a conductance, swapping in a channel of the same ion species.
- **Kinetics** (held-out family, never seen by protocol selection): shifting a gate's
  activation midpoint, scaling its slope, shifting the midpoint of a forward rate.

Magnitude operators were applied at two prespecified severities, mild and strong, defined by bands
of |ln k| for multiplicative changes and of millivolts for shifts. Sites were chosen by a seeded
generator (seed 20260917) fixed before generation. Every edit records the file, element, attribute,
old and new values.

Two further strata were generated and analysed separately. **Controls** were eight kinds of
behaviour-preserving transformation per model: unit conversion, whitespace reformatting, added
comments, equivalent numeric literals, consistent renaming of an identifier, moving a component to
an included file, reordering independent elements, and writing an inherited default explicitly.
**Numerical stress tests** changed the integration step, solver setting or recording resolution;
these probe numerical robustness and are never counted as semantic faults.

The frozen generator produced 186 variants: 120 faults, 48 controls and 18 numerical stress tests.

### 2.4 Protocols and features

The **canonical test** (`P00`) was each model's shipped harness, run unchanged. The **candidate
protocols** were eight current-clamp stimuli scaled to each model's measured rheobase: a weak
depolarising step (0.5× rheobase), a rheobase search, a step at 2× rheobase, a long step (1.5×
rheobase, 2 s), a ramp from 0 to 3× rheobase over 1 s, a hyperpolarising step, a rebound protocol
(hyperpolarisation then release), and a short suprathreshold pulse (3 ms at 10× rheobase). Every
protocol began with a 300 ms settling period.

Features were extracted with eFEL (Mandge et al. 2026): spike count, first-spike latency, last
interspike interval, adaptation index, action-potential amplitude and afterhyperpolarisation depth
for spiking protocols, and steady-state voltage and deflection for subthreshold ones. A feature
defined in one model and undefined in the other (for example, a latency when one model does not
spike) counted as a difference.

### 2.5 Tolerances and detection

Each feature difference was compared with a tolerance calibrated on the unmodified model:

τ = max(absolute floor, relative term × |f_h|, 3 × |f_h − f_h/2|),

where f_h and f_h/2 are the reference feature at the nominal step h (0.005 ms) and at h/2. The last
term makes the threshold at least three times the model's own discretisation error, so a difference
the solver could produce by itself cannot count. Floors and relative terms were fixed per feature
before any held-out simulation (Online Resource 1).

A strategy **detected** a fault when one of its protocols showed a difference beyond tolerance, for
the same protocol and feature, at step h **and** at h/2. Faults that the canonical test missed but
another protocol detected were re-simulated at h/4 for confirmation.

We also compared full voltage traces, as a separate validation level that is never merged with the
feature comparison. A trace differed when its spike count differed, when spike times shifted by more
than τ_shift = max(0.5 ms, 3 × the reference's own h versus h/2 shift), or when the root-mean-square
difference exceeded τ_rmse = max(0.5 mV, 3 × the reference's own h versus h/2 RMSE). A model whose
canonical trace tolerance could not be calibrated would be reported as unclassifiable at that level.

### 2.6 Classification and protocol selection

Each fault was classified in order: structurally invalid (fails NeuroML validation where the
original passes), non-executable, numerically unstable, equivalent within the tested domain (no
reproducible feature difference on any protocol), non-equivalent and detected by the canonical test,
or non-equivalent but missed by it (**silent under canonical**). Faults in the last two classes are
**admissible**: they changed behaviour, and they form the denominator of the primary endpoint.

The battery was selected on the development models only, by greedy maximum coverage of their
admissible faults with a budget of k = 4 protocols and ties broken by cost and then identifier. The
kinetics family was excluded from selection. The greedy rule stopped at three protocols, because a
fourth added no coverage: the long step, the 2× step and the ramp.

### 2.7 Endpoints and statistics

The **primary endpoint** was the paired difference in detection rate between the selected battery
and the canonical test, Δ = DR_battery − DR_canonical, over admissible held-out faults. The battery
was evaluated without the canonical protocol, so the comparison is between two alternative checks,
not between a test and a superset of it. We prespecified Δ ≥ 0.10 as the smallest material
difference, and a canonical detection rate ≥ 0.95 as the criterion for calling canonical regression
adequate.

The interval for Δ was a cluster percentile bootstrap resampling base models (B = 10,000, seed
20260917), as registered. Supporting tests were an exact McNemar test on discordant pairs, which
treats faults as independent, and an exact cluster permutation test on per-model differences, which
does not. Because two pairs of models share a source, we additionally report the bootstrap with
source family as the cluster (sensitivity analysis). The result was prespecified as inconclusive if
more than 10 % of controls were flagged, if more than half of apparent canonical survivors failed h/4
confirmation, or if 25 % or more of tolerance entries had to be excluded for refinement instability.

Secondary endpoints (all prespecified) were: detection by random protocol batteries matched for size
(all 56 three-protocol subsets of the eight candidates) and for cost (10,000 random batteries within
the selected battery's cell-step budget); the silent-survival rate; control false-positive rates;
detection by fault family and severity; coverage against the number of protocols; cost per
detection; and robustness to tolerance multipliers of 0.5, 1, 2 and 4.

### 2.8 Development work

Two pilots on development models preceded the evaluation and are reported descriptively. In the
first (two closely related models), the canonical test detected all 22 admissible faults. In the
second (five further models, 88 faults, 40 controls), canonical detection counting either level was
0.921; nine faults were missed at feature level, two of which also survived full-trace comparison,
and no control was flagged. During the second pilot we found and corrected an analysis defect that
had counted faults as full-trace survivors on a model where the canonical trace comparison could not
be calibrated; the correction, which introduced the "unclassifiable" category of section 2.5, was
made before the evaluation and is part of the frozen pipeline. Operator validation had observed the
canonical outcome of nine Pilot 2 faults before that pilot ran; Pilot 2 is therefore reported with
and without them (Online Resource 2). None of this affects the held-out models, which were never
mutated before the confirmatory run.

### 2.9 Software and reproducibility

The method is implemented in **NexClamp**, an open-source Python package (Apache-2.0) that runs
the protocols, extracts the features, calibrates the tolerances, generates the faults and
controls, selects the battery and seals each campaign. Simulations used jNeuroML 0.14.0 and jLEMS
0.12.0 on Temurin JDK 21.0.12.1+1, with Python 3.12.10,
pyNeuroML 1.3.22, libNeuroML 0.6.7 and eFEL 5.7.34, on 12 parallel workers. Every run is stored
write-once under a content-addressed identifier, with its inputs, software versions and outputs.
The held-out campaign was archived and sealed after completion (17,424 files, each with a SHA-256
checksum), and the pipeline refuses to write into a sealed campaign.

## 3 Results

### 3.1 Attrition and controls

Of 120 faults, 114 were schema-valid, 112 executed, 109 were numerically stable, and 82 changed
behaviour (admissible); 27 were equivalent within the tested domain (Fig. 5). If faults whose only
detected change was in the full voltage trace are also counted, 94 changed behaviour; we report the
frozen definition (82) as primary and note both.

No control was flagged by any strategy: 0 of 48 at feature level and 0 of 48 at trace level (exact
95 % upper bound 0.074), including at half the calibrated tolerance. None of the prespecified
inconclusive conditions occurred: 0 % of controls flagged, 0 of 18 canonical survivors failed h/4
confirmation, and no tolerance entry was excluded for refinement instability.

### 3.2 Primary endpoint

The canonical test detected 69 of 82 admissible faults (0.841; 95 % cluster interval 0.78–0.91)
and the selected battery 80 of 82 (0.976; 0.92–1.00) (Fig. 1). The paired counts were: both 67,
battery only 13, canonical only 2, neither 0. The difference was Δ = +0.134, 95 % cluster-bootstrap
interval +0.013 to +0.221 (Fig. 2). The exact McNemar test gave p = 0.007; the cluster permutation
test, with only six clusters and a smallest attainable p of 0.031, gave p = 0.156. With source family
as the cluster the interval was +0.040 to +0.232, flagged as unreliable because only four clusters
remain.

The battery detected more faults than the canonical test on five of six models, by two to four faults
each. On `traub2005_testseg_all` the canonical test detected all 12 faults and the battery 10; the two
it missed were a shifted gate midpoint and a shifted reversal potential detected only by the
canonical protocol.

Against the preregistered criteria: the point estimate exceeds the 0.10 material difference and the
interval excludes zero, but its lower end lies below 0.10, so a material advantage is supported by
the estimate without being established by the interval. Canonical regression did not meet the
adequacy criterion of 0.95.

### 3.3 Faults that escape the canonical test entirely

The feature comparison is one way to read the canonical simulation; its full voltage trace is
another. Of the 94 faults with any detected change, the canonical features detected 69 and the
canonical full trace 87 (features only 1, trace only 19, either 88, neither 6; Fig. 3). The trace
comparison was calibrated on all six models and fired on 11 to 17 faults per model.

Six faults were missed by the canonical test at both levels: four on `hay2011_soma`, one on
`bbp2015_soma` and one on `migliore2005_ca1_soma` (Table 2). All six were detected by the battery,
reproducibly at h, h/2 and h/4, through changes in spike count or spike timing. They include a 10 %
increase in the high-voltage-activated calcium conductance of the Hay cell, which reduced the number
of spikes during the long step from 14 to 13 while leaving the canonical simulation within tolerance;
two changes to the slow M-current (halving its conductance, shifting its reversal potential by
−10 mV) that altered spike timing only under the 2× step; and changes to calcium- and A-type
potassium-channel gating kinetics that altered spike count or timing under the long step and the
ramp. These faults
meet the preregistered criterion for hidden drift (at least two confirmed full-trace survivors across
at least two models).

**Table 2.** Faults missed by the canonical test on both features and full trace.

| Fault | Model | Edit | Detected by (level) |
|---|---|---|---|
| `scale_conductance` (mild) | hay2011_soma | Ca_HVA ×1.1 | long step: spike count, last ISI; ramp: spike timing |
| `scale_conductance` (strong) | hay2011_soma | M-current (Im) ×0.5 | 2× step: spike timing (trace) |
| `shift_reversal` (strong) | hay2011_soma | M-current reversal −85 → −95 mV | 2× step: spike timing (trace) |
| `scale_gate_time_constant` (mild) | hay2011_soma | Ca_HVA activation rates ×1.25 | long step: spike count; ramp: spike timing |
| `scale_gate_time_constant` (mild) | bbp2015_soma | Ca_HVA activation rates ×1.25 | long step: spike count; ramp: spike timing |
| `scale_gate_time_constant` (mild) | migliore2005_ca1_soma | A-type K (kad) gate Q10 ×0.8 | 2× step, long step, ramp: spike timing, trace RMSE |

### 3.4 Where the canonical test fails

The canonical test's losses were concentrated in mild faults, which it detected at 0.70 against the
battery's 0.95; for strong faults the rates were 0.97 and 1.00 (Table 3). By fault type, it missed
most often after changes to maximal conductance (0.65 versus 1.00) and gate time constants (2 of 5
versus 5 of 5). The silent-survival rate, the fraction of admissible faults missed by the canonical
test, was 0.159 (95 % cluster interval 0.089–0.222).

For the held-out kinetics family, which protocol selection never saw, the canonical test detected
0.864 and the battery 0.955 (22 faults; Δ = +0.091, interval −0.10 to +0.22, flagged unreliable
because few models contributed discordant faults). We draw no conclusion about generalisation to the
unseen family. For the families seen in development the difference was +0.150 (interval +0.036 to
+0.232).

**Table 3.** Detection by group (admissible faults).

| Group | n | Canonical | Battery |
|---|---|---|---|
| All | 82 | 0.841 | 0.976 |
| Mild severity | 40 | 0.700 | 0.950 |
| Strong severity | 31 | 0.968 | 1.000 |
| No severity (reference swaps) | 11 | 1.000 | 1.000 |
| Maximal conductance | 17 | 0.647 | 1.000 |
| Gate time constant | 5 | 0.400 | 1.000 |
| Gate voltage dependence (incl. kinetics) | 22 | 0.864 | 0.955 |
| Reversal potential | 15 | 0.933 | 0.933 |
| Passive membrane | 12 | 1.000 | 1.000 |
| Mechanism composition | 11 | 1.000 | 1.000 |

### 3.5 Selection, coverage and cost

The selected battery detected more faults than 55 of the 56 possible three-protocol batteries drawn
from the same candidates (mean 0.846; share at least as good 0.018) and than 97 % of 10,000 random
batteries of equal cost (mean 0.909; share at least as good 0.030) (Fig. 4). Protocol selection on
development models therefore transferred to unseen models. The long step alone reached 90 % of the
coverage of all protocols combined; the three selected protocols reached 95 %. The battery cost 3.3
times as many integration steps per variant as the canonical test (1.0 million against 0.31 million
cell-steps).

### 3.6 Tolerance sensitivity

Across tolerance multipliers of 0.5, 1, 2 and 4, no control was flagged at any multiplier, while the
fraction of faults silent under the canonical test rose from 0.087 to 0.116, 0.152 and 0.203 as
tolerances loosened (all 138 faults and stress tests). The main finding does not depend on the
tolerance being tight.

### 3.7 Cross-simulator check (exploratory)

The evaluation used one simulator. To test whether its reference behaviour is simulator-specific,
each held-out model was exported to NEURON with `jnml -neuron` and its canonical simulation re-run
under NEURON 9.0.2. All six models exported, compiled and ran. Spike counts were identical in every
case (7, 5, 9, 4, 7 and 4 spikes), and matched each model's own published NEURON reference. The
largest difference in any spike time was 0.009 to 0.182 ms, and whole-trace differences were 0.19 to
2.18 mV RMS, consistent with two integrators rather than two behaviours. This check was added after
the confirmatory run, is exploratory, and is reported descriptively: the study's tolerances are
calibrated within one integrator and do not transfer across two. It supports the reference
simulations the detections are measured against; it does not re-test the faults.

## 4 Discussion

On six neuron models never used to develop the method, re-running the shipped simulation missed
about one in six faults that changed the model's behaviour, and a three-protocol battery chosen in
advance missed two of 82. Six faults went unnoticed by the canonical test even when its whole voltage
trace was compared, which is the strictest form a canonical regression test can take. No
behaviour-preserving transformation was flagged by anything. The pilots had suggested the canonical
test was nearly sufficient; the held-out evaluation, preregistered with that expectation stated,
did not bear this out.

The pattern of misses is intelligible. The canonical harnesses are short: their stimulus windows span 60
to 300 ms, and the depolarising steps in four of them last 60 to 100 ms. Faults that act slowly, such as a change to the M-current or to a calcium conductance that shapes
adaptation, alter firing only as a step continues, near threshold, or under a slowly rising input. The long step, the stronger step and the ramp sample exactly those
regimes. Faults with large effects were caught by almost any check; the gap lies in mild faults, which
are also the kind most likely to be introduced unnoticed by a unit conversion or a hand edit.

Two practical consequences follow. First, most of the canonical test's shortfall at feature level is
recovered by comparing its full voltage trace (88 of 94 against 69 of 94), which costs nothing extra.
Tools that check only summary features of the shipped simulation should compare traces as well.
Second, the remaining misses need other stimuli, and a short battery suffices: the long step alone
reached 90 % of the achievable coverage. The battery costs about three times the canonical
simulation, which is small against the effort of reusing a model.

The result is consistent with work on constructing neuron models, where the stimulus set determines
which properties a model is constrained by (Druckmann et al. 2011; Van Geit et al. 2016; Reva et al.
2023), and with multi-protocol validation suites (Gerkin et al. 2019; Sáray et al. 2021;
Appukuttan and Davison 2022). Those tools compare models with experimental data. Our question is
narrower and complementary: whether a modified model still matches its own original. We show that
this question, which is usually answered with one simulation, needs more than one.

### 4.1 Limitations

The evaluation used six models from four source families, so intervals are wide and the model-level
permutation test is underpowered by construction; the interval for Δ excludes zero but does not
establish a material advantage. All models are single-compartment. The faults themselves were evaluated in one
simulator, although every held-out model's reference behaviour reproduced in NEURON (section 3.7);
dendritic faults remain out of scope. Faults were synthetic
single-site edits; real modification errors may be larger, compound or correlated. Admissibility
depends on the definition used (82 by feature classification, 94 including trace-only changes).
The result for the held-out kinetics family is inconclusive. The frozen generator produced 186
variants, above the preregistered estimate of roughly 100 to 150, and selection produced a
three-protocol battery under a four-protocol budget; both are reported as they occurred. An automated
re-check of the 26 audited faults (a random sample of 20 and the six canonical survivors) found every
edit, class and detection consistent with the raw model files and voltage traces; the independent human
audit of the same faults is [pending].

### 4.2 Deviations from the registration

All deviations are logged with their dates and reasons (Online Resource 2). Those bearing on the
evaluation: (i) the runtime criterion for model screening was raised from 1,800 s to 4,200 s per
variant before any held-out model was mutated, because the lower budget left no eligible models;
(ii) the registration estimated roughly 100 to 150 variants and the frozen generator produced 186;
(iii) the battery has three protocols under the registered budget of four; (iv) two co-authors joined
after registration; (v) a locked planning document was edited after the freeze to add them, the
evaluation's integrity check refused to start, and the document was restored byte for byte before the
run, with no change to any hypothesis, endpoint, split or analysis; (vi) the source-family clustering
is reported as a sensitivity analysis.

## 5 Conclusions

A canonical regression test is not sufficient evidence that a modified neuron model still behaves as
before. On unseen models it missed about one in six behaviour-changing faults, some of which its full
voltage trace also missed. Comparing the canonical trace, not only its features, recovers much of the
gap, and a short battery of standard current-clamp protocols recovers nearly all of it without false
alarms. We recommend both as routine checks when neuron models are edited, converted or ported.

---

## Information Sharing Statement

NexClamp, the frozen configuration, model snapshots (with licences), all per-variant records and summary
tables, and the scripts that produce every number and figure in this article are available at
[repository URL] and archived at Zenodo [DOI]. Raw voltage traces (4.5 GB) are archived at [location].
The preregistration is available at https://aspredicted.org/q2ag7w.pdf. All models are third-party
open-source NeuroML models, used under their licences (Online Resource 1).

## Declarations

**Funding.** No funding was received for this work.

**Competing interests.** The authors declare no competing interests.

**Author contributions** (CRediT). Neel Gurram: conceptualization, methodology, software,
investigation, formal analysis, data curation, validation, visualization, project administration,
writing (original draft, review and editing). Samyak Singh: formal analysis. Naithik Somisetti:
formal analysis. [All authors reviewed and approved the final manuscript.]

**Use of AI tools.** The analysis software and parts of this manuscript were developed with the
assistance of an AI coding assistant (Claude, Anthropic). All AI-assisted work was logged, and every
result was produced by deterministic code whose outputs the authors verified. The authors take full
responsibility for the content. No AI system is an author.

**Ethics approval.** Not applicable: no human participants, animals or personal data.

**Data and code availability.** See the Information Sharing Statement.

---

## Figure legends

*Files: Fig. 1–5 = `results/figures/heldout-v1/` `h1_per_model_primary`, `h2_primary_difference`, `h3_validation_levels`, `h4_random_baselines`, `h5_attrition` (PDF versions for submission).*

**Fig. 1** Detection of admissible faults on each held-out model by the canonical regression test
and the selected three-protocol battery. Dashed lines: pooled rates with 95 % cluster-bootstrap
intervals; dotted line: preregistered adequacy threshold (0.95).

**Fig. 2** Primary endpoint. Per-model differences in detection rate (battery minus canonical) and
the pooled difference with its 95 % cluster-bootstrap interval; dashed line: preregistered material
difference (0.10).

**Fig. 3** Validation levels, never merged: faults detected by the canonical test's features, by its
full voltage trace, and by the other protocols, per model. Dashed lines: faults with any detected
change.

**Fig. 4** Held-out detection by all 56 random three-protocol batteries (left) and 10,000 random
batteries within the same cost (right), compared with the selected battery and the canonical test.

**Fig. 5** Attrition of the 120 faults through validation, execution, stability and admissibility.

## References

Appukuttan S, Davison AP (2022) Reproducing and quantitatively validating a biologically-constrained point-neuron model of CA1 pyramidal cells. Frontiers in Integrative Neuroscience 16. https://doi.org/10.3389/fnint.2022.1041423

Birgiolas J, Haynes V, Gleeson P, Gerkin RC, Dietrich SW, Crook S (2023) NeuroML-DB: Sharing and characterizing data-driven neuroscience models described in NeuroML. PLOS Computational Biology 19:e1010941. https://doi.org/10.1371/journal.pcbi.1010941

Druckmann S, Berger TK, Schürmann F, Hill S, Markram H, Segev I (2011) Effective stimuli for constructing reliable neuron models. PLoS Computational Biology 7:e1002133. https://doi.org/10.1371/journal.pcbi.1002133

Gerkin RC, Birgiolas J, Jarvis RJ, Omar C, Crook SM (2019) NeuronUnit: A package for data-driven validation of neuron models using SciUnit. bioRxiv. https://doi.org/10.1101/665331

Hay E, Hill S, Schürmann F, Markram H, Segev I (2011) Models of neocortical layer 5b pyramidal cells capturing a wide range of dendritic and perisomatic active properties. PLoS Computational Biology 7:e1002107. https://doi.org/10.1371/journal.pcbi.1002107

Hook D, Kelly D (2009) Mutation sensitivity testing. Computing in Science & Engineering 11:40-47. https://doi.org/10.1109/MCSE.2009.200

Kelly D, Gray R, Shao Y (2011) Examining random and designed tests to detect code mistakes in scientific software. Journal of Computational Science 2:47-56. https://doi.org/10.1016/j.jocs.2010.12.002

Mandge D, Tuncel A, Jaquier A, Kilic I, Damart T, et al. (2026) eFEL: electrophysiology feature extraction library. Bioinformatics 42. https://doi.org/10.1093/bioinformatics/btag328

Marin B, Gleeson P. OSB Model Validation (OMV), version 0.4.0 [software]. https://github.com/OpenSourceBrain/osb-model-validation

Markram H, Muller E, Ramaswamy S, Reimann MW, et al. (2015) Reconstruction and simulation of neocortical microcircuitry. Cell 163:456-492. https://doi.org/10.1016/j.cell.2015.09.029

Matinnejad R, Nejati S, Briand LC, Bruckmann T (2019) Test generation and test prioritization for Simulink models with dynamic behavior. IEEE Transactions on Software Engineering 45:919-944. https://doi.org/10.1109/TSE.2018.2811489

Migliore M, Ferrante M, Ascoli GA (2005) Signal propagation in oblique dendrites of CA1 pyramidal cells. Journal of Neurophysiology 94:4145-4155. https://doi.org/10.1152/jn.00521.2005

Papadakis M, Kintis M, Zhang J, Jia Y, Le Traon Y, Harman M (2019) Mutation testing advances: an analysis and survey. Advances in Computers:275-378. https://doi.org/10.1016/bs.adcom.2018.03.015

Reva M, Rössert C, Arnaudon A, Damart T, Mandge D, et al. (2023) A universal workflow for creation, validation, and generalization of detailed neuronal models. Patterns 4:100855. https://doi.org/10.1016/j.patter.2023.100855

Sáray S, Rössert CA, Appukuttan S, et al. (2021) HippoUnit: A software tool for the automated testing and systematic comparison of detailed models of hippocampal neurons based on electrophysiological data. PLOS Computational Biology 17:e1008114. https://doi.org/10.1371/journal.pcbi.1008114

Segura S, Fraser G, Sanchez AB, Ruiz-Cortés A (2016) A survey on metamorphic testing. IEEE Transactions on Software Engineering 42:805-824. https://doi.org/10.1109/TSE.2016.2532875

Sinha A, Gleeson P, Marin B, et al. (2025) The NeuroML ecosystem for standardized multi-scale modeling in neuroscience. eLife 13. https://doi.org/10.7554/eLife.95135

Smith SL, Smith IT, Branco T, Häusser M (2013) Dendritic spikes enhance stimulus selectivity in cortical neurons in vivo. Nature 503:115-120. https://doi.org/10.1038/nature12600

Traub RD, Contreras D, Cunningham MO, et al. (2005) Single-column thalamocortical network model exhibiting gamma oscillations, sleep spindles, and epileptogenic bursts. Journal of Neurophysiology 93:2194-2232. https://doi.org/10.1152/jn.00983.2004

Van Geit W, Gevaert M, Chindemi G, et al. (2016) BluePyOpt: leveraging open source software and cloud infrastructure to optimise model parameters in neuroscience. Frontiers in Neuroinformatics 10. https://doi.org/10.3389/fninf.2016.00017

Yoo S, Harman M (2012) Regression testing minimization, selection and prioritization: a survey. Software Testing, Verification and Reliability 22:67-120. https://doi.org/10.1002/stvr.430

Zhan Y, Clark JA (2005) Search-based mutation testing for Simulink models. In: Proceedings of GECCO 2005, pp 1061-1068. https://doi.org/10.1145/1068009.1068188

---

## Open items before submission

1. **Human audit** (Samyak, Naithik): results go into section 3 and the limitations paragraph.
2. **Table 2**: edits filled from the recorded variants; the targeted audit confirms them.
3. **Reference details**: volume and page numbers for references given without them, checked
   against Crossref; confirm author lists abbreviated with "et al.".
4. **Repository and archive**: public repository URL, Zenodo DOI, location for the raw traces.
5. **Online Resources**: 1 (screening criteria, tolerance constants, protocol and operator
   definitions), 2 (deviation log, development pilots, Pilot 2 with and without exposed faults).
6. **All authors** read, correct and approve; confirm contributions.
7. **Journal formatting**: convert to the Springer Nature LaTeX or Word template; check the abstract
   limit and figure requirements in the Neuroinformatics author guidelines.
