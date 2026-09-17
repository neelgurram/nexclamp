# Verification packet 1: OSB Model Validation (OMV)

**Rank in `docs/PRIOR_ART_MATRIX.md`:** 1 of 36

## Citation

- **Software:** Marin B, Gleeson P (OpenSourceBrain). *OSB Model Validation (OMV)*, repository `osb-model-validation`.
  - Repository created 2014-04-16; last push 2026-08-17, per the GitHub API.
  - PyPI package `OSBModelValidation`, version 0.4.0. PyPI lists the authors as Boris Marin and Padraig Gleeson, and the licence as LGPL-3.0-only.
- **DOI:** none. OMV has no DOI of its own. Archival URL: https://github.com/OpenSourceBrain/osb-model-validation
- **Citable description:** Sinha A, Gleeson P, Marin B, Dura-Bernal S, Panagiotou S, Crook S, Cantarelli M, Cannon RC, Davison AP, Gurnani H, Silver RA (2025). The NeuroML ecosystem for standardized multi-scale modeling in neuroscience. *eLife* 13:RP95135.
  - DOI: [10.7554/eLife.95135](https://doi.org/10.7554/eLife.95135). The Crossref record was checked on 2026-09-16.
  - The eLife paper cites an earlier Open Source Brain paper (Gleeson et al. 2019) for OMV. That paper was not read in this pass.

## Where the full text came from (2026-09-16)

| Source | URL | What was read |
|---|---|---|
| README (master branch) | https://raw.githubusercontent.com/OpenSourceBrain/osb-model-validation/master/README.md | Whole file |
| Analyzer base class | https://raw.githubusercontent.com/OpenSourceBrain/osb-model-validation/master/omv/analyzers/analyzer.py | Tolerance handling, lines 52-80 |
| Comparison helper | https://raw.githubusercontent.com/OpenSourceBrain/osb-model-validation/master/omv/analyzers/utils/timeseries.py | `compare_arrays`, lines 49-71 |
| eLife paper, open access | Europe PMC full-text XML, PMC11723582 (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11723582/fullTextXML) | Results section "Validating NeuroML models" and the Figure 7 caption |

The prior deep read (`deepread_r1_b0.json`, `deepread_r1_b8.json`) also read the README and several analyzer files.

Software has no page numbers. Locations below are README headings, source line numbers (master branch on 2026-09-16), and eLife section names.

## What OMV does (paraphrased)

- **README, top section.** OMV automates model checks for Open Source Brain projects. It runs locally or on GitHub Actions on every commit, and it can run a model on many simulation engines. The README says it has been used on the 30+ NeuroML and PyNN models of the 2019 Open Source Brain paper, and on more since.
- **README, "Write MEP files".** A MEP file ("model emergent properties") states what a simulation should produce, for example a list of expected spike times. A MEP file can list several named experiments, and a project can have several MEP files. Its author can also write reduced versions of a model that test particular aspects.
- **README, "Writing OMT files".** An OMT file ("OSB model test") names:
  - the LEMS file to run;
  - the simulation engine, for example jNeuroML or jNeuroML_NEURON;
  - the MEP file to compare against;
  - for each observable: where the data are, how to scale them, how to detect spikes, and a `tolerance`.
- **README, same section, tolerance examples.** The FitzHugh-Nagumo examples set tolerance by hand: about 2.2e-16 for the jNeuroML engine and 0 for jNeuroML_NEURON.
- **README, "Running validation tests locally".** The README presents local runs as a quick way to see whether model changes alter the model's specific outcomes, and whether different engines give similar results.
- **Source, `analyzer.py` lines 52-80:**
  - if an observable has no tolerance, OMV uses 0.1;
  - on failure, OMV prints the observed and expected data and may suggest a tolerance that would pass;
  - on a pass, it may suggest a tighter tolerance.
- **Source, `timeseries.py` lines 49-71:**
  - arrays of different lengths fail outright;
  - otherwise OMV compares them with numpy `allclose`, passing the tolerance as the relative tolerance;
  - the suggested tolerance is the largest relative difference between observed and expected values.
- **eLife, "Validating NeuroML models":**
  - after schema and LEMS checks, OMV tests whether simulation output (for example spike times) is within an allowed tolerance of the expected value, across simulators and simulator versions;
  - OMV has been applied to Open Source Brain models as the models and the simulators are updated;
  - biological validation is a separate, final level, handled by NeuronUnit/SciUnit.

## Overlap with Neuraxis, claim by claim

| Neuraxis claim | Overlap | Detail |
|---|---|---|
| Multi-protocol fingerprints | Partial | A MEP/OMT pair can hold several experiments and observables per model. Authors write them per project. There is no standard protocol library, no rheobase scaling and no feature vector. |
| Controlled mutations of neuron models | None | Nothing in the README or the analyzer code generates or seeds faults. |
| Canonical-test survivors | None as a finding. OMV *is* the canonical test. | OMV checks only the outcomes a project author wrote down. It never measures which behaviour changes pass those checks. Neuraxis's "survivor" set is defined relative to exactly this kind of check. |
| Protocol selection | None | Nothing chooses, ranks or minimises experiments. |
| Held-out generalisation | None | Pass/fail regression per model and engine only. |
| Valid-transformation false positives | Partial | Tolerances exist so that the same model on different engines can pass, which is the purpose of avoiding false alarms. But tolerances are set by hand per observable. The suggested tolerance comes from one observed comparison, not from numerical refinement. No false-alarm rate is measured. |

## What remains distinct

- **Measuring the check.** Neuraxis would measure how adequate an OMV-style canonical check is. It would use controlled mutants and a detection matrix to show which behaviour-changing edits pass the check and which protocols expose them.
- **Tolerances.** Neuraxis would set tolerances from numerical refinement, not by hand. It would also measure false alarms on transformations known to be valid.
- **Selection and transfer.** Neuraxis would choose a small battery and test it on held-out models and a held-out mutation family.
- **Baseline, not contribution.** OMV should be described as the baseline and a reused component, never as something Neuraxis improves on in kind.

## Caveats

- The Gleeson et al. (2019) Open Source Brain paper, which the eLife paper cites for OMV, was not read here. It might describe OMV practice in more detail.
- The source code can change after 2026-09-16. The line numbers apply to the master branch on that date.

## Checklist

- [ ] Researcher manual inspection: pending
