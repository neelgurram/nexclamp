# Release checklist: public code, data archive and preprint

*What must happen before submission, in order. Items marked **[NEEL]** need a person with accounts;
the rest are prepared in the repository already.*

## 1 Before anything is public

- [ ] **Human audit complete** (Samyak, Naithik): filled Word packets returned, results folded into
      the manuscript and `docs/RESULTS_HELDOUT.md`.
- [ ] All authors have read and approved the manuscript and the author-contribution statement.
- [x] References verified against Crossref (`docs/manuscript/reference_details.json`).
- [x] Online Resources 1 and 2 generated from recorded files (`scripts/build_supplement.py`).
- [x] Every table and figure regenerable with one command (`make paper`).
- [x] Zenodo metadata prepared (`.zenodo.json`).

## 2 Check what goes public

The repository contains third-party models, so check before publishing:

- [x] Licences recorded per model (`data/model_manifest.csv`, `LICENSE_AUDIT.md`). Models are MIT or
      GPL-2.0; the GPL-2.0 models (Traub) are redistributed under their own terms with attribution.
- [x] Study code is Apache-2.0 (`LICENSE`).
- [ ] **[NEEL]** Confirm you are content that the repository will show your email address
      (`gurramn2025@fau.edu`) in `CITATION.cff` and commit history.
- [ ] No private data: the repository holds only public models, generated variants, and results.

## 3 Publish the code [NEEL]

1. ~~Create the repository~~ **done 2026-09-23**: https://github.com/neelgurram/nexclamp (public, owner `neelgurram`).
2. ~~Push `main` and the tags~~ **done**: `study-freeze-v1`, `heldout-v1-code`, `pilot-v1-code`.
3. Check on GitHub that `docs/RESULTS_HELDOUT.md` and the figures display properly.

**Size note.** The raw voltage traces (4.1 GB) are excluded by `.gitignore`; their SHA-256 hashes are
committed in `ARCHIVE_MANIFEST.sha256`, so anyone can verify a copy. The repository itself is small.

## 4 Archive for a DOI [NEEL]

1. Sign in to **zenodo.org** with GitHub.
2. In Zenodo's GitHub settings, switch the repository **on**.
3. In GitHub, create a release tagged `v1.0.0-study1`. Zenodo archives it and issues a DOI.
4. Send me the DOI; I will put it in the manuscript, `CITATION.cff` and the README.

**Raw traces.** Zenodo accepts up to 50 GB per record, so the 4.1 GB archive can be a second record
if you want the traces public. Otherwise state that they are available on request, with hashes
published. Decide before submission.

## 5 Preprint [NEEL]

1. Post the manuscript to **bioRxiv** (free) when you submit, category: Neuroscience /
   Computational Biology. It is a preprint, not a publication, and *Neuroinformatics* permits it.
2. Add the bioRxiv DOI to the repository README.

## 6 Submit [NEEL]

1. *Neuroinformatics* (Springer), original article, **standard (non-open-access) route** so there is
   no charge. Confirm on the journal's "Submission guidelines" page that this route is free.
2. Upload: manuscript (`MANUSCRIPT_v0.1.docx`), figures (PDF versions in
   `results/figures/heldout-v1/`), Online Resources 1 and 2, and the cover letter.
3. In the cover letter, state: the study was preregistered before any held-out data existed
   (AsPredicted #312455), both outcomes were pre-committed to publication, and the code and data are
   public.

## 7 After submission

- [ ] Keep `main` frozen for the submitted version; tag it `submitted-v1`.
- [ ] Record any post-submission change in `docs/DEVIATION_LOG.md`.
- [ ] Reviewer requests for new analyses are answered as *exploratory*, never by re-running the
      sealed campaign.
