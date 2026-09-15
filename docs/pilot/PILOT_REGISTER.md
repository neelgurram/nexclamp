# Pilot register

*Every pilot campaign, its code, configuration, scope, exclusions and revisions, so the
manuscript can report the development process transparently (DECISIONS D-026, D-027).
All entries are exploratory/developmental. Machine-readable roles:
`results/campaign_registry.json`.*

## In plain English

- A pilot is a practice run. We are allowed to learn from it and change things.
- Every practice run keeps a separate name and is never overwritten or deleted. A changed
  setting means a new run with a new name.
- When the practice runs are over, everything gets locked. Then the real test runs once on
  models nothing was tuned on. Only that test gives the headline numbers.

## Bounds for a pilot (Neel, 2026-09-13)

2-6 openly licensed NeuroML models; 4-8 stimulation protocols; 3-8 electrophysiological
features; at least 3 mutation families; about 20-60 mutants; valid-transformation controls.

## Campaigns

| | `pilot` (iteration 1) | `pilot-v2` (iteration 2) |
|---|---|---|
| Role | exploratory_pilot | exploratory_pilot |
| Status | complete; archived, verified and sealed | **governed by `docs/PILOT_PROTOCOL_V1.md`; authorised after the readiness gate** (D-033 to D-035) |
| Project / phase labels | none (made before labels existed); reported only in corrected form (D-038) | `Neuraxis` / `development_pilot` / `PILOT_PROTOCOL_V1` on every record |
| Run | 2026-09-13 17:11-18:55 UTC | - |
| Code | `d323afa` (tag `pilot-v1-code`) | - |
| Configs (SHA-256) | study `d6371a7f…`, features `7397da03…`, tolerances `9ca05052…` | `configs/pilot_protocol_v1/` |
| Models | 2 (Pospischil 2008 RS, LTS; one source) | 4: RS and LTS repeated; Wang-Buzsaki and NeuroML2 HH new |
| Detection protocols | 10: P01, P02, P03 rheobase, P04-P10 (plus canonical comparator) | 7: P03-P09 (plus canonical comparator; reference rheobase is calibration) |
| Features | 18, all deciding | 8 primary (deciding) plus 10 secondary (exploratory) = the same 18 |
| Families | 3, all in the primary corpus | 2 semantic (primary) plus numerical as a separate stress test (D-030) |
| Mutants | 52 (40 semantic, 12 numerical, per the D-030 reanalysis) | 32 semantic plus 12 numerical (dry run) |
| Controls | 16 (12 valid transformations, 4 no-change) | 32 |
| Within the feasibility guidelines | protocols and features exceed them (D-028); guidelines, not laws (D-029) | yes |

## Iteration 1 (`pilot`)

**Outcome.** `docs/pilot/pilot_interpretation.md`; automatic report
`results/processed/pilot/pilot_report.md`.

**Exclusions and non-evaluable units** (all retained in the data, none deleted):
- mutants excluded from the admissible denominator by rule: 2 structurally invalid, 8
  non-executable, 1 numerically unstable, 13 equivalent within the tested domain;
- 3 of the non-executable mutants run under the shipped harness but not in the reused battery
  model (`canonical_runs_but_battery_failed`);
- tolerance entries excluded under refinement: 0 of 128;
- reference entries undefined at h and h/2: RS 1 of 64, LTS 20 of 64 (weak battery for LTS, N-07);
- operators that produced no mutant: `reduce_spatial_discretization` (single-compartment cells);
- protocols not implemented: P11 chirp, P12 frozen noise (no NeuroML core input type).

**Revisions before and during development that affect how its numbers were produced**
(Git history is the full record):

| commit | change |
|---|---|
| `5184ce9` | cached features keyed by trace, feature config, eFEL version and feature code |
| `b472ad3` | jLEMS time labels regularised to the exact fixed-step grid |
| `0317355` | mutation and transform generators integrated into campaign stages |
| `4689315` | analysis stage; detection matrix in selection format |
| `74dbab4`, `c34afbf` | mid-run divergence classified as numerically unstable |
| `3cdb957` | builder modules and core fixes from build reviews |
| `d323afa` | provenance dirty flag scoped to simulation-relevant paths (D-023) |

**Reused runs.** 75 cached simulations came from development commits `5184ce9`, `0317355` and
`751ee99`; 38 of them were recorded with a dirty tree. Content addressing guarantees each trace
matches its inputs (D-025).

**Development outputs outside the campaign**: time-step probe `docs/pilot/dt_probe.md`; smoke
runs `work/smoke/`; logs `work/logs/`. The pilot logs are copied into
`results/processed/pilot/logs/`, and the smoke outputs are included in the archive.

**Scope deviation.** 10 protocols and 18 features exceed the bounds. The campaign is kept as
iteration 1 and is not rerun or discarded (D-028).

**Numerical reclassification (D-030).** Read-only reanalysis in
`docs/pilot/numerical_reclassification.md` and `results/derived/pilot/`. It found 0 silent
semantic mutants; the 3 silent mutants were numerical, 2 of them affected by the
unequal-starting-step confound.

**Archive.** `results/processed/pilot/ARCHIVE_README.md`. The local copy is verified; the second
private copy is pending (N-16).

## Iteration 2 (`pilot-v2`)

Design proposal: `docs/pilot/pilot_v2_design.md`. Nothing has run.

## Rules for any further iteration

1. New campaign name; never write into a sealed campaign (enforced by `make_context`).
2. One configuration per campaign (enforced: a changed config or simulator is refused).
3. Seal with `scripts/archive_campaign.py` when finished, then add a column above.
4. Record what changed and why in `DECISIONS.md`.
