# Verification packet 4: Universal workflow for detailed neuronal models (Reva et al. 2023)

**Rank in `docs/PRIOR_ART_MATRIX.md`:** 4 of 36

## Citation

Reva M, Rössert C, Arnaudon A, Damart T, Mandge D, Tuncel A, Ramaswamy S, Markram H, Van Geit W (2023). A universal workflow for creation, validation, and generalization of detailed neuronal models. *Patterns* 4(11): 100855.

- **DOI:** [10.1016/j.patter.2023.100855](https://doi.org/10.1016/j.patter.2023.100855). The Crossref record was checked on 2026-09-16, and doi.org redirects to the publisher.
- **Other identifiers:** PMID 38035193; PMC10682753. Preprint: bioRxiv 10.1101/2022.12.13.520234.

## Where the full text came from (2026-09-16)

- **Europe PMC full-text XML:** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10682753/fullTextXML
  - The whole article body was read, including Experimental procedures and Data and code availability.
- **No page numbers.** The article is numbered 100855 rather than paginated, and the Cell Press PDF could not be downloaded. Locations below are section headings.
- **Equations not visible.** The XML text did not render the equations (Equation 1, the score, and Equation 2, the acceptance rule). Their exact form was **not** read.
- **Prior deep read:** `deepread_r1_b1.json` used the same XML.

## What the paper does (paraphrased, by section)

- **Summary and Introduction.**
  - An open workflow builds canonical e-models from recordings, in four steps: extract features, optimise, validate on extra stimuli, and generalise to many morphologies.
  - It was applied to 40 e-models covering 11 e-types of juvenile rat somatosensory cortex.
  - Stimulus amplitudes are normalised by rheobase.
  - The authors report that the new L5PC model generalises about five times better than an earlier canonical model.
- **Results, "Electrophysiological features of the SSCx neuronal e-types".**
  - The protocols are 2 s depolarising steps, a hyperpolarising step, and a short step for action-potential waveform.
  - All protocols are rescaled to percentages of each cell's rheobase, and feature means and SDs are computed at those levels.
- **Results, "Model construction and optimization", with Table 1.**
  - Each e-type has its own set of protocols and e-features: APWaveform, IV, IDrest/IDthresh at several rheobase percentages, SpikeRec, RMP, input resistance, holding and threshold current, and bAP for pyramidal cells.
  - Evaluation first finds holding current and rheobase by bisection, then runs the step protocols.
- **Results, "Validation and analysis of the detailed neuronal model", with Table 2.**
  - The L5PC model was checked on dendritic attenuation (bAP and EPSP) and on three somatic protocols not used in fitting: Ramp, sAHP and IDHyperpol.
  - Most features were within five SD of experiment. The Ramp spike count and time to first spike were about eight SD away.
- **Same section, sensitivity analysis.**
  - Each parameter was reduced on its own, and the slope of the resulting feature change was computed.
  - 26 of 31 parameters affected the features. Some conductances, such as somatic and axonal K_T, barely affected any feature under the protocols analysed.
  - **Discrepancy:** Results gives the reductions as 1%, 50% and 90%; Experimental procedures gives 10%, 50% and 90%.
- **Results, "Generalization of electrical models".**
  - 1,015 reconstructed morphologies were cloned to 141,733. These gave 366,926 morphology-model combinations, of which 233,941 passed.
  - Acceptance compares each combination's feature scores with the scores on the exemplar morphology (Equation 2, not rendered).
  - Failures were mostly in firing and AHP features. Low axonal sodium conductance explained most L5PC failures.
  - Acceptance rates are reported per e-type. Three irregular e-types generalise poorly.
- **Discussion, fifth paragraph.** Sensitivity analysis could guide which features and protocols to include in the score, so that all parameters are constrained.
- **Experimental procedures, "Electrophysiological features extraction".** "Tolerance" here means a 10% bin around target stimulus amplitudes used when averaging recordings. It is not an output tolerance.
- **Experimental procedures, "Sensitivity analysis".** One parameter is changed at a time. Sensitivity is the regression slope of the feature difference against the percentage change.
- **Data and code availability.**
  - Notebooks are at BlueBrain/SSCxEModelExamples, and the repository runs continuous-integration tests for reproducibility.
  - The workflow can output NEURON HOC or NeuroML models.

## Overlap with Neuraxis, claim by claim

| Neuraxis claim | Overlap | Detail |
|---|---|---|
| Multi-protocol fingerprints | Strong | Rheobase-scaled, multi-protocol e-feature vectors for conductance-based neurons (Table 1, Table 2), with eFEL-family tools. |
| Controlled mutations of neuron models | Partial | One-at-a-time parameter reductions with a parameter-by-feature sensitivity matrix. These are sensitivity probes, not catalogued model-file edits, and are not scored as detected or missed. |
| Canonical-test survivors | Partial, implicit | Some parameter changes barely move any feature in the analysed protocols. A battery would therefore miss them. The model also fits its optimisation protocols but deviates about eight SD on Ramp features. Neither point is framed as survivors of a canonical test. |
| Protocol selection | Partial, suggested only | The Discussion says sensitivity could guide protocol and feature choice. No selection algorithm is given. |
| Held-out generalisation | Partial | Validation on stimuli not used in fitting, and on unseen morphologies. This tests model fidelity, not whether a detector transfers to new models or fault families. |
| Valid-transformation false positives | None | No numerical-refinement tolerance and no false-alarm measurement. The only "tolerance" is a stimulus-binning width. |

## What remains distinct

- **Purpose.** Reva et al. perturb parameters to understand and repair one model. Neuraxis would edit models to test whether a *battery detects* behaviour-changing transformations.
- **Tolerances.** Neuraxis would calibrate tolerances by refinement and control false alarms on valid transformations.
- **Selection and transfer.** Neuraxis would choose a battery on discovery mutants, then show that it transfers to different models and a different mutation family.
- **Reviewer risk.** A reviewer could say that adding a set-cover step over Figure 6A's sensitivity matrix is an obvious extension. The transfer evidence has to answer this.

## Checklist

- [ ] Researcher manual inspection: pending. Also check the PDF for the exact form of Equation 2 and for which perturbation sizes (1% or 10%) were used.
