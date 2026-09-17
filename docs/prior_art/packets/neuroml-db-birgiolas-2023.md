# Verification packet 2: NeuroML-DB (Birgiolas et al. 2023)

**Rank in `docs/PRIOR_ART_MATRIX.md`:** 2 of 36

## Citation

Birgiolas J, Haynes V, Gleeson P, Gerkin RC, Dietrich SW, Crook S (2023). NeuroML-DB: Sharing and characterizing data-driven neuroscience models described in NeuroML. *PLOS Computational Biology* 19(3): e1010941.

- **DOI:** [10.1371/journal.pcbi.1010941](https://doi.org/10.1371/journal.pcbi.1010941). The Crossref record was checked on 2026-09-16, and doi.org redirects to PLOS.
- **Other identifiers:** PMID 36867658; PMC10016719. Preprint: bioRxiv 10.1101/2021.09.11.459920.

## Where the full text came from (2026-09-16)

- **PLOS open-access PDF:** https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1010941&type=printable
  - 29 pages, CC BY. The text was extracted page by page and read.
  - Page numbers below are the journal's "n / 29" page labels.
- **Europe PMC full-text XML:** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10016719/fullTextXML
  - Downloaded for cross-checking. The prior deep read (`deepread_r1_b1.json`) used this version.

## What the paper does (paraphrased, with pages)

- **p. 1 (Abstract).** NeuroML-DB holds over 1,500 published channel, cell and network models translated to NeuroML. It characterises their electrophysiology, morphology and computational cost. It also runs a database-wide analysis that finds a tetrahedral cluster structure among cell models.
- **pp. 4-5.** Channel and cell models are characterised with standardised voltage-clamp and current-clamp protocols, and the results are shown as online plots. The electrophysiology of 1,222 cell models was measured with one uniform protocol set, then reduced with PCA and clustered.
- **p. 8.** The authors note that papers report the simulation time step but rarely justify it. How sensitive a model is to changing that step is not easy to know.
- **pp. 9-10.**
  - The NEURON files generated automatically from NeuroML were tested against the original model code with the OSB Model Validation framework.
  - Hand-written code can still run faster than the generated code.
- **p. 10.** Cell models were stimulated with the Allen Cell Types protocols:
  - square, long square, pink noise, ramp, short square and short square triple;
  - 38 membrane properties from Druckmann et al. were then computed, covering action-potential shape and spike-train statistics.
- **p. 11.**
  - The 38 properties were implemented as reusable SciUnit/NeuronUnit tests.
  - Clustering gives four top-level groups.
  - For "Rapidly Adapting" and "Non-positive Rheobase" models, many properties cannot be computed, because the protocol produces too few spikes or rheobase is not positive.
- **p. 19.** Among the limits of the complexity measure: different model clusters might need tailored input waveforms, which could be added later.
- **pp. 19-20 (Discussion, subsection on improving electrophysiology protocols):**
  - The fixed 1.5x and 3.0x rheobase steps work well for regular multi-spiking models but poorly for other clusters.
  - The authors ask whether those multiples are special, and whether they are too strong or too weak for some models.
  - They suggest basing stimulus levels on the model's bifurcation structure, found automatically by a black-box method.
  - Intrinsically spiking models need a different protocol.
- **p. 22 (Methods).** Models were converted with jNeuroML v0.8.3 and simulated in NEURON 7.5.
- **p. 23 (Methods).**
  - Missing property values, such as a second-spike amplitude when a cell spikes only once, were filled with minimum, maximum or mean values before PCA.
  - 42 features were reduced to 21 principal components for 1,222 models.

## Overlap with Neuraxis, claim by claim

| Neuraxis claim | Overlap | Detail |
|---|---|---|
| Multi-protocol fingerprints | Strong | Multi-protocol, rheobase-scaled feature vectors for NeuroML cell models on the same toolchain: jNeuroML to NEURON, with NeuronUnit tests (pp. 10-11, 22-23). |
| Controlled mutations of neuron models | None | The models are separate published models. No edits or faults are introduced. |
| Canonical-test survivors | Weak, conceptual | The authors show that a fixed protocol leaves some model groups poorly described (p. 11, pp. 19-20). That is a protocol-adequacy observation about *different models*, not about edits that pass a canonical test. |
| Protocol selection | Partial, as future work | Better protocol choice, for example based on bifurcation structure, is proposed but not built (p. 20). |
| Held-out generalisation | None | Clustering and PCA only. No train/test split. |
| Valid-transformation false positives | Weak | Correctness of the NeuroML-to-NEURON conversion is attributed to OMV (pp. 9-10) and is not measured in the paper. Time-step sensitivity is raised only as an open question (p. 8). |

## What remains distinct

- **Purpose of the fingerprint.** NeuroML-DB uses fingerprints to *compare different models* for search and clustering. Neuraxis would compare a *reference model with its own transformed versions*.
- **Undefined features.** NeuroML-DB fills undefined features with substitute values (p. 23). Change detection needs "undefined before, defined after" to count as a signal.
- **Tolerances.** NeuroML-DB sets no numerical tolerances and reports no detection or false-alarm rates.
- **Protocol choice.** NeuroML-DB leaves protocol choice as an open question (p. 20). Neuraxis would choose protocols algorithmically from mutant detections and test the choice on held-out models and a held-out mutation family.
- **Framing risk.** A reviewer could say that Neuraxis is "NeuroML-DB fingerprints plus a diff". The defence has to come from the mutation-calibrated adequacy study and the transfer results.

## Checklist

- [ ] Researcher manual inspection: pending
