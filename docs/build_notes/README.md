# Build notes

These notes were written by the module builders on 2026-09-13, during the parallel build. Each is a
**point-in-time record**: requests, defects, interpretations and observations as they stood when the
module was built and reviewed.

Many items were acted on afterwards, and some values in the notes are now superseded:
- the numerical blow-up bound (250 mV became 10 V);
- the `increase_dt` factor grid (it is now x4, x10, x20);
- the crash-versus-unstable labelling;
- the class-6 canonical rule;
- the q10 fallback;
- container provenance.

The current rules are in `DECISIONS.md` (D-020 to D-023) and `docs/ARCHITECTURE.md`. Where a note and
those files disagree, the decision log and the code win.
