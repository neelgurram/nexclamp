# Campaign `pilot`: exploratory pilot, iteration 1

**EXPLORATORY / DEVELOPMENTAL DATA.** These results come from the development set. They may
appear in the manuscript as method-development evidence, preliminary findings and
illustrative case studies. They are **never pooled with the held-out data for the primary
confirmatory estimate** (DECISIONS D-026).

- Code and configs: commit `d323afa`, tag `pilot-v1-code`; config copies in `config_snapshot/`.
- Scope versus the pilot bounds Neel set: exceeds them on protocols (10 vs 4-8) and features
  (18 vs 3-8); within them on models, families and mutants (D-028).
- Preservation: `ARCHIVE_MANIFEST.sha256` hashes every raw file, including the Git-ignored traces;
  `ARCHIVE.json` records the write-once tar; `SEALED.json` marks the campaign read-only (D-027).
- Interpretation: `docs/pilot/pilot_interpretation.md`. Register of all pilot iterations:
  `docs/pilot/PILOT_REGISTER.md`.
