# Verification packet 3: The Cardiac Electrophysiology Web Lab (Cooper et al. 2016)

**Rank in `docs/PRIOR_ART_MATRIX.md`:** 3 of 36. The related rows are 10 (Cooper, Mirams and Niederer 2011, the functional-curation origin) and 11 (Daly et al. 2018, the Web Lab follow-up).

## Citation

Cooper J, Scharm M, Mirams GR (2016). The Cardiac Electrophysiology Web Lab. *Biophysical Journal* 110(2): 292-300.

- **DOI:** [10.1016/j.bpj.2015.12.012](https://doi.org/10.1016/j.bpj.2015.12.012). The Crossref record was checked on 2026-09-16, and doi.org redirects to the publisher.
- **Other identifiers:** PMID 26789753; PMC4724653. Open access under CC BY.

## Where the full text came from (2026-09-16)

- **Europe PMC full-text XML:** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4724653/fullTextXML
  - The whole article body was read.
- **No page numbers.** The PDF could not be downloaded: both Europe PMC and PMC returned a bot-check page instead. Locations below are the article's section headings and paragraph order. The journal page range is 292-300, but individual passages are not mapped to pages.
- **Prior deep read:** `deepread_r1_b12.json` used the same XML.

## What the paper does (paraphrased, by section)

- **Abstract.**
  - The Web Lab keeps model equations separate from simulated experimental protocols.
  - It runs virtual experiments on CellML models and holds 36 models and 23 protocols: I-V curves, pacing at several rates, restitution, channel block, and hypo-/hyperkalaemia.
  - Developers can upload new models and see how they behave under the existing protocols.
- **Introduction, fourth paragraph.** No automatic way exists to check even a model's published behaviours. Curated model files sometimes differ from the original implementations.
- **Introduction, last paragraph.** The Web Lab deliberately makes no judgement about whether a model behaves appropriately or which model is best. It only supports comparison.
- **Materials and Methods.**
  - Annotations of model variables form the interface between models and protocols, and units are converted automatically.
  - Every protocol is run on every compatible model.
  - Results are cached and recomputed when a model or protocol is added or updated.
- **Results, opening paragraph.** The colour codes show whether a simulation ran, not whether the model is correct.
- **Results, "Exploring model characteristics".** Different human ventricular models predict very different effects of NCX block (Figure 5).
- **Results, "Correcting errors in model encodings".**
  - Comparing the Decker 2009 restitution results with the original publication revealed an error in the CellML version, which had been public since March 2010. The file was corrected.
  - The BiVeS tool shows the differences between the versions.
  - The authors add that such differences appear only when a model is tested in a range of situations.
- **Results, "Steady states".**
  - The Priebe 1998 model behaves differently after one pace than after 10,000 paces (Figure 6).
  - Some models drift to non-physiological states.
- **Discussion, second paragraph.** Unexpected results can come from numerical problems, from errors in the model or its encoding, or from protocol post-processing. The software itself has an extensive bank of automated tests.
- **Discussion, third paragraph.** Model developers can upload in-development versions, privately if they wish. They can check them against many more protocols than were used to build the model, and iterate until the desired behaviour is reached.
- **Discussion, later paragraphs.** Further automated checking of results, parameter estimation, and links to experimental data are named as future work.

## Overlap with Neuraxis, claim by claim

| Neuraxis claim | Overlap | Detail |
|---|---|---|
| Multi-protocol fingerprints | Strong in idea | The same protocol battery runs on every model and model version, and outputs are compared side by side. There is no feature vector with tolerances. |
| Controlled mutations of neuron models | None | No seeded faults. The evidence is one real encoding error (Results, "Correcting errors in model encodings"), and the models are cardiac. |
| Canonical-test survivors | Partial, anecdotal | A CellML error stayed public for years and was exposed by a restitution protocol. The authors argue that such errors show only across many situations. There is no rate, and no systematic survivor set. |
| Protocol selection | None | Protocols are written by hand. Nothing chooses or minimises them. |
| Held-out generalisation | None | No discovery/held-out split. |
| Valid-transformation false positives | None | No pass/fail rule by design (Introduction). The Discussion lists numerical and post-processing sources of spurious differences, but gives no tolerance or false-alarm measurement. |

## What remains distinct

- **The core idea is not new.** Rerunning a broad protocol battery on each model version, to catch behaviour the headline test misses, appears here, and in Cooper et al. 2011, a decade before Neuraxis. Neuraxis must credit this line for that idea.
- **What Neuraxis could still claim:**
  - a quantitative, mutation-calibrated study of *how often* and *for which kinds of edit* a battery catches changes;
  - tolerances calibrated so that valid transformations do not raise alarms;
  - algorithmic selection of a small battery;
  - transfer to held-out models and a held-out mutation family;
  - all of this for conductance-based neuron models in NeuroML, not cardiac CellML models.

## Checklist

- [ ] Researcher manual inspection: pending. Suggestion: also skim Cooper et al. 2011 (doi:10.1016/j.pbiomolbio.2011.06.003), which introduced functional curation and the idea of using it during incremental model development.
