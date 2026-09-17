# [Title to be chosen after the frozen held-out study]

<!--
TITLE RULE (execution plan). Use the positive title
  "Perturbation-Fingerprint Testing Reveals Silent Behavioral Drift in Transformed Conductance-Based Neuron Models"
only if the frozen held-out study establishes silent drift. Otherwise use the neutral title
  "Evaluating Perturbation-Fingerprint Tests for Behavioral Preservation in Computational Neuron Models".
The software name is provisional (docs/NAME_AUDIT.md).

STATUS: skeleton only. It contains no results. Every number must come from
`workflows/reproduce_manuscript.py`. Confirmatory statements come only from the locked held-out
results (`workflows/lock_primary_results.py`). Pilot data are exploratory and reported as method
development (DECISIONS D-026), and Pilot 1 only in its corrected form (D-038).
-->

## Abstract

*To be written after the primary results are locked.*

## 1. Introduction

- A model file can remain structurally valid, execute and pass one conventional stimulation test
  while its behaviour under other stimuli has changed.
- Contribution (candidate; see `docs/PRIOR_ART_MATRIX.md`): mutation-calibrated perturbation
  fingerprints, detection of transformation-induced changes missed by a canonical test, and a
  compact stimulation battery evaluated on unseen models and an unseen mutation family.
- Built on NeuroML, LEMS, pyNeuroML, jNeuroML, eFEL and SciUnit/NeuronUnit, which are not claimed
  as contributions.

## 2. Methods

2.1 Models and curation (inclusion criteria; `docs/MODEL_CURATION_REPORT.md`)
2.2 Simulation and numerical calibration (h, h/2, h/4; tolerance rule)
2.3 Stimulation protocols and features (`docs/PROTOCOL_CATALOG.md`, `docs/FEATURE_CATALOG.md`)
2.4 Controlled mutations, strata and valid transformations (`docs/MUTATION_CATALOG.md`)
2.5 Classification and admissibility
2.6 Development phase (pilots; exploratory) and protocol selection
2.7 Frozen held-out evaluation and preregistration (AsPredicted link)
2.8 Statistical analysis (`docs/STATISTICAL_ANALYSIS_PLAN.md`)
2.9 Software, provenance and reproducibility
2.10 AI-assisted development disclosure (`docs/AI_DISCLOSURE.md`)

## 3. Results

3.1 Validation cascade
3.2 Primary comparison: selected battery versus canonical test on held-out models *(confirmatory)*
3.3 Random-battery baselines; coverage versus protocol count
3.4 Generalisation to the held-out mutation family
3.5 False positives on valid transformations
3.6 Robustness to tolerances; numerical stress tests (separate analysis)
3.7 Exploratory development findings (pilots), clearly labelled

## 4. Discussion

Limitations (finite battery, not a proof of equivalence; single simulator; model pool size),
failure modes and implications for model reuse.

## Data and code availability

GitHub release and Zenodo DOI (to be recorded); raw data archive (to be recorded).
