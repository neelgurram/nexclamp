# Held-out pool plan (amendment H-01)

*Written 2026-09-18, after the pre-launch audit established that no eligible untouched model remains
(`docs/PILOT2_PRELAUNCH_DECISION.md` section 8). Authorised by Neel the same day. This plan governs
how the confirmatory held-out model set is assembled. It is written **before** any candidate's
mutation outcome exists.*

## In plain English

- The development side of the study has used up every model that passed screening: two in Pilot 1,
  five in Pilot 2.
- The models left over were all rejected for one of three reasons: they are too slow under the old
  compute budget, they fire on their own so "rheobase" is undefined, or they have a licence or file
  problem.
- Neel raised the compute budget, which brings six of the slow ones back into play, from four
  different research groups.
- We screen them **without ever mutating them**. Screening only asks "does this model run, behave
  sensibly and stay stable?" It never asks "does our method detect faults in it?" — that question
  stays sealed until the confirmatory run.

## 1. Why a new pool is needed

`manifests/CURATION_FINAL_TABLE.csv` (campaign `curation-v3`): 23 candidates, 7 eligible. All seven
are now development models — `pospischil2008_rs` and `pospischil2008_lts` from Pilot 1, and the five
Pilot 2 models. Their five source repositories are permanently development sources (PILOT2_PROTOCOL
section 3, amendment A-01 rule 5). Eligible untouched models: **zero**.

## 2. The candidate pool after amendment H-01

| source | model | previous status | status under H-01 |
|---|---|---|---|
| `hay2011_bbp_channels` | `hay2011_soma` | excluded, 3,465 s | **candidate** |
| `hay2011_bbp_channels` | `bbp2015_soma` | excluded, 3,618 s | **candidate** |
| `traub2005` | `traub2005_testseg2` | excluded, 3,036 s | **candidate** |
| `traub2005` | `traub2005_testseg_all` | excluded, 4,115 s | **candidate** |
| `smith2013` | `smith2013_singlecomp` | excluded, 2,692 s | **candidate** |
| `migliore2005` | `migliore2005_ca1_soma` | excluded, 2,449 s | **candidate** |
| `prinz_stg` | `prinz2004_abpd`, `prinz2004_lp` | needs human judgement (C08) | still open: see section 4 |
| `bahl2012`, `bezaire2016` | 2 models | no licence / missing files | still excluded |
| `maex1998` | 2 models | no shipped simulation file | still excluded |
| `solinas2007`, `wangbuzsaki1996` | 2 models | NeuroML validation failure | still excluded (D-051 for WB) |

Six models, **four independent untouched sources** (Hay/BBP, Traub 2005, Smith 2013, Migliore 2005).
The plan requires four to six held-out models from sources not used in development, so the pool is
feasible if the six survive the remaining twelve criteria.

## 3. What screening may and may not look at

| allowed during screening | forbidden until the confirmatory run |
|---|---|
| provenance, licence, files present | any mutation of a held-out model |
| NeuroML validation, shipped-harness execution | any detection outcome, at any validation level |
| reference rheobase, firing regime, sag, rebound | any canonical-versus-battery comparison |
| determinism, refinement stability, runtime | any branch-relevant statistic |
| which mutation operators *have a site* (a structural property of the file) | whether those operators are *detected* |

Screening reveals how an unmutated model behaves. The study measures whether perturbation protocols
detect faults that canonical regression misses. Those are different quantities, and no screening
output answers the second. This distinction is what keeps the held-out set genuinely held out, and
it is the distinction that was broken for Pilot 2 by running operator validation on its models
(D-055).

## 4. The Prinz question, still open

`prinz2004_abpd` and `prinz2004_lp` are spontaneously bursting pacemakers: they fire with no injected
current, so rheobase is undefined and criterion C08 cannot be evaluated as written. They are a
genuinely different response type and a fifth independent source, which is scientifically valuable.
Options, for Neel, unchanged by this plan:

1. Exclude them, and accept four sources.
2. Admit them with a prespecified rule for spontaneously active cells: protocol amplitudes scale from
   the configured fallback (0.1 nA) instead of rheobase, and C08 is replaced by "produces a
   reproducible spontaneous firing pattern".
3. Defer, and revisit if fewer than four of the six candidates survive screening.

Option 2 is a real amendment to the inclusion criteria and must be written down before their
screening is interpreted, not after.

## 5. Procedure

1. Run `neuraxis curate-models --campaign curation-v4 --budget-s 4200` over the untouched candidates
   only. Reference simulations only; no mutants are generated or executed.
2. Publish the result as a new final table alongside the existing one. `curation-v3` is preserved
   unchanged.
3. If **four or more** models from **three or more** independent sources are eligible, propose the
   held-out split, freeze it with hashes, and stop for Neel.
4. If fewer than four are eligible, stop and report that the held-out design is not feasible with the
   current pool, and that either the Prinz rule or new candidate models are required. Do not lower a
   criterion to reach four.
5. No held-out model is mutated, and no confirmatory run starts, until the split is frozen, the
   protocol version is fixed, and the AsPredicted preregistration has been submitted and verified
   with the exact authorisation sentence (D-036).

## 6. Timing note

Screening must not run at the same time as a scientific campaign. Criterion C11 measures wall-clock
simulator time, so competing load inflates the estimate and could exclude a model for a reason that
has nothing to do with the model — the failure mode already recorded as X-18. Curation `v4` therefore
runs only when no campaign is executing.
