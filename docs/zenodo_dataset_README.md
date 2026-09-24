# Raw simulation output of the NexClamp held-out confirmatory campaign (`heldout-v1`)

This dataset is the complete, unedited simulation output of the preregistered held-out evaluation
reported in "Canonical regression tests miss behaviour-changing faults in computational neuron models:
a preregistered held-out evaluation" (Gurram, Singh & Somisetti). It exists so that any reader can
recompute every number in that article from the raw records, not from our summaries.

## What is in the archive

`heldout-v1_raw_and_workspaces.tar.gz` contains **17,424 files**:

- `results/raw/heldout-v1/<run_id>/` — one directory per simulation, each holding
  - `traces.npz`: the recorded voltage trace of every protocol in that run (time axis stored as
    start, step, count),
  - `features_<key>.json`: the electrophysiological features extracted from those traces,
  - `run.json`: the complete provenance of the run (inputs, configuration hashes, software versions,
    simulator version, git commit, timings, exit status),
  - `stdout.txt`, `stderr.txt`, `simulator_output_tail.txt`: the simulator's own output.
  Rheobase searches are stored as `s-<id>/rheobase.json`.
- `work/variants/heldout-v1/` — the model workspace of every variant: the unmodified reference model
  and each edited copy, so any edit can be inspected or re-run.

Run identifiers are content-addressed: the identifier is derived from the inputs, so the same inputs
always produce the same identifier and no run can be silently overwritten.

## Verifying the archive

`ARCHIVE_MANIFEST.sha256` lists the SHA-256 checksum of every file. After extracting:

```bash
sha256sum -c ARCHIVE_MANIFEST.sha256
```

`ARCHIVE.json` records when the campaign was sealed, the code commit it ran on, and the checksum of
the archive itself. The campaign is sealed: the software refuses to write further runs into it.

## How this relates to the other deposits

| Resource | Where |
|---|---|
| Analysis software (NexClamp), frozen configuration, per-variant records, analysis outputs, and the scripts that regenerate every table and figure | software and results archive (see "Related identifiers") |
| Preregistration (AsPredicted #312455, registered 2026-09-19) | https://aspredicted.org/q2ag7w.pdf |
| Article | see "Related identifiers" |

## Provenance of the models

The archive contains copies of six third-party open-source NeuroML neuron models, each redistributed
under its own licence with its source repository and pinned commit recorded in the article's Online
Resource 1: the Hay et al. (2011) layer-5b channel set and the Blue Brain (Markram et al., 2015)
channel set (MIT), the two Traub et al. (2005) test cells (GPL-2.0), the Smith et al. (2013) channel
set (MIT), and the Migliore et al. (2005) CA1 soma model (MIT), all obtained from Open Source Brain.

## Licence

The recorded simulation output and provenance records created by this study are released under
**CC-BY-4.0**. The third-party model files included in the archive remain under their own licences
(MIT or GPL-2.0), which are included alongside them; those licences are not superseded by the licence
of this dataset.

## Software used

jNeuroML 0.14.0 / jLEMS 0.12.0 on Temurin JDK 21.0.12.1+1; Python 3.12.10; pyNeuroML 1.3.22;
libNeuroML 0.6.7; eFEL 5.7.34. Every run records its own versions in `run.json`.
