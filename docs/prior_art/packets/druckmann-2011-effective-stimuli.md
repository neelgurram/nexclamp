# Verification packet 5: Effective Stimuli for Constructing Reliable Neuron Models (Druckmann et al. 2011)

**Rank in `docs/PRIOR_ART_MATRIX.md`:** 5 of 36

## Citation

Druckmann S, Berger TK, Schürmann F, Hill S, Markram H, Segev I (2011). Effective Stimuli for Constructing Reliable Neuron Models. *PLoS Computational Biology* 7(8): e1002133.

- **DOI:** [10.1371/journal.pcbi.1002133](https://doi.org/10.1371/journal.pcbi.1002133). The Crossref record was checked on 2026-09-16, and doi.org redirects to PLOS.
- **Other identifiers:** PMID 21876663; PMC3158041. Open access under CC BY.

## Where the full text came from (2026-09-16)

- **PLOS open-access PDF:** https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1002133&type=printable
  - 13 pages. The text was extracted page by page and read in full.
  - Page numbers below are the journal page labels, 1-13.
- **Europe PMC full-text XML:** PMC3158041. The prior deep read (`deepread_r1_b8.json`) used this version.

## What the paper does (paraphrased, with pages)

- **p. 1 (Abstract).**
  - The paper proposes a framework, inspired by learning theory, for choosing current stimuli.
  - A stimulus is judged by how well it constrains conductance-based models that then predict responses to new stimuli.
  - Step and ramp currents beat synaptic-like noisy currents.
- **p. 1 (Introduction).**
  - Fitting the training data does not prove a model is valid, because biases may appear only under different conditions.
  - The authors list possible generalisation checks, including stability to small parameter changes. They choose prediction of unseen stimuli.
- **p. 2.**
  - The authors say a clear way is needed to choose an optimal and minimal stimulus set.
  - Recordings of several stimulus types were split into training and generalisation sets.
  - Models trained only on steps predicted ramps and noise well. Models trained on ramps or noise did not.
- **pp. 2-3, Figure 1 (p. 3).**
  - The pipeline has four steps: extract features, run multi-objective optimisation of maximal conductances, apply an acceptance rule of two experimental SDs per feature, and keep the set of acceptable models.
- **pp. 2-3.**
  - Generalisation error falls as the number of training steps rises (Figure 3a).
  - Ramp-trained models do not generalise better to steps as ramp training grows (Figure 3b).
  - Steps shrink the region of acceptable parameters more than ramps (Figure 3c-d).
- **pp. 4-5.** Noise-trained models time spikes well on other noise but match step and ramp responses poorly, at about 2.6-2.9 SD. Generalisation is therefore asymmetric.
- **p. 6.**
  - Step plus ramp was the best training set overall. Adding more than three intensities of one stimulus type brought little extra benefit.
  - Nothing guarantees that good generalisation to one stimulus type carries over to others.
  - Four more cells (different types, ages and species) gave consistent results.
- **p. 8, Table 1.** Every training set is scored against every generalisation set: steps, ramps, and two noise types.
- **p. 8 (Discussion).** The authors explain the ranking by channel kinetics:
  - ramps inactivate fast transient channels, so they reveal little about them;
  - noise barely engages slow channels;
  - steps engage both.
- **pp. 8-9.** Each stimulus carves out its own region of parameter space. Only models in the overlap generalise to both stimuli.
- **p. 9.** The authors restate the goal of an optimal and minimal stimulus set and name more complex protocols as ongoing work.
- **p. 10 (Methods, "Stimulation protocols" and "Neuron model").**
  - Stimuli: six 2 s steps, five ramps, and two 20 s Ornstein-Uhlenbeck noise currents, each scaled per cell and repeated 10-20 times.
  - Model: NEURON, with eight somatic channel types and passive dendrites, giving 11 free parameters.
- **p. 11 (Methods).**
  - Feature distances are measured in experimental SD units. Step responses use six features, and ramps add slope features. Noise responses use a spike-coincidence factor.
  - Training sets are matched for total recording length.
  - Stimuli used in training are excluded from testing.
  - Optimisation uses NSGA-II, implemented in NEURON, repeated ten times.

## Overlap with Neuraxis, claim by claim

| Neuraxis claim | Overlap | Detail |
|---|---|---|
| Multi-protocol fingerprints | Partial | Feature-based responses to several stimulus types and intensities (pp. 10-11). They serve fitting and generalisation scores, not comparison of a model with its edited versions. |
| Controlled mutations of neuron models | None | No edits or faults. Parameter-space regions are mapped (p. 3, pp. 8-9) but not used as a fault catalogue. |
| Canonical-test survivors | Conceptual only | Models that match one stimulus type can fail on others (pp. 2-5, Table 1). This is the same intuition, that one test under-determines behaviour, but it concerns fitted models versus data, not edits that pass a canonical check. |
| Protocol selection | Partial | Several length-matched training sets are compared and step plus ramp is recommended (pp. 6, 8, 11). An optimal minimal set is left as a goal (p. 9). There is no search or budgeted algorithm. |
| Held-out generalisation | Partial | Withheld stimuli (p. 11), and the stimulus ranking re-checked on four more neurons (p. 6). There are no held-out fault families. |
| Valid-transformation false positives | Weak | Tolerance is a two-SD acceptance band from trial-to-trial variability (p. 3, p. 11), not numerical refinement. No false-alarm rate is measured. |

## What remains distinct

- **Objective.** Druckmann et al. rank stimuli by how well they *identify parameters from data*. Neuraxis would rank protocols by how well they *detect behaviour-changing edits* of an existing model, while producing no alarms on valid transformations.
- **The objectives may disagree.** A protocol that constrains parameters well need not expose, for example, unit or kinetics edits. Neuraxis should test this directly, for example by including a "step plus ramp" baseline battery, rather than assume it.
- **What Neuraxis could claim.** The reusable points are the stimulus-set comparison design, the mechanistic explanation of why stimuli differ, and the minimal-set goal. Neuraxis can claim selection *for edit detection* with held-out model and mutation-family transfer. It cannot claim to be the first to choose effective stimuli for conductance-based neurons.

## Checklist

- [ ] Researcher manual inspection: pending
