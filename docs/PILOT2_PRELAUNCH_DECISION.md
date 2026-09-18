# Pilot 2 pre-launch decision

*Written 2026-09-18 at commit `17b9b06`. Companion to `docs/PILOT2_LEAKAGE_ASSESSMENT.md`. No
frozen file was modified, no data deleted, no history rewritten, and no simulation run for this
document.*

## 1. Verified repository state

| item | verified value |
|---|---|
| branch | `m0-audit` |
| HEAD | `17b9b06` — two commits after `cffd026` (`cffd026` → `17b9b06`) |
| working tree | clean apart from `results/campaign_registry.json` (modified by campaign registration) and untracked audit and result directories |
| files changed `cffd026`→`17b9b06` | `tests/unit/test_models_manifest.py`, `docs/model_selection.md`, `manifests/PILOT2_PRE_RUN.sha256`, plus readiness audit outputs |
| background processes | **none**: no `java.exe`, no `neuraxis` python process, no writes to `results/raw/pilot2` since the stop |

## 2. Readiness status

The second readiness run **completed and passed**: record
`results/audits/readiness/20260917T232100Z/readiness.json`.

| step | result |
|---|---|
| complete test suite, from the beginning | **1,065 passed, 0 failed, 0 errors, 1 skipped**, 2,337 s |
| ruff | 186 findings — recorded baseline (R-15) |
| mypy | 120 findings — recorded baseline (R-15) |
| clean-environment venv, `requirements.lock`, package install | pass |
| end-to-end smoke test in that environment | pass, all nine checks |
| Pilot 1 raw-data hashes | **2,689 files, 0 mismatched or missing** |
| CLI `--help`, canonical import | pass |
| commit / tree | `17b9b06`, clean, no uncommitted inputs |

### 2.1 Reconciling the static-analysis counts

| report | tool and scope | count | explanation |
|---|---|---|---|
| earlier session note | `mypy src` at commit `49c8678`, when mypy was first pinned | 95 | smaller `src/` tree: before the kinetics operators, validation levels, trace regression, Pilot 2 output builders and the promoted-model code paths existed |
| first readiness run | `mypy src`, mypy 2.3.1, commit `cffd026` | 120 | **changed scope, not changed strictness**: new modules added between the two runs |
| second readiness run | same command, commit `17b9b06` | 120 | unchanged, as expected |
| ruff baseline 2026-09-16 | `ruff check src tests scripts`, ruff 0.16.7 | 167 | recorded in `results/audits/static_checks/ruff_2026-09-16.txt` |
| readiness runs | same command, same version | 186 | **+19 from new files**: `scripts/readiness.py`, `pilot2_authorize.py`, `curation_table.py`, `pilot2_prepare.py`, new tests. No configuration or rule-set change; `pyproject.toml` sets only `line-length` and `target-version` |

Neither difference comes from changed code behaviour or a changed environment; both come from more
code being in scope. Nothing was suppressed.

### 2.2 Manual risk classification of scientific-core findings

Of 120 mypy findings, roughly 108 fall in scientific-core modules. By error class: 25 `arg-type`,
22 `operator`, 21 `import-untyped` (third-party stubs, no risk), 12 `attr-defined`, 9
`var-annotated`, 8 `union-attr`. I read every finding in the modules that decide detections:

| module | finding | risk |
|---|---|---|
| `validation/trace_regression.py:103,111` | `rm > t.tau_rmse` where `tau_rmse` is `float \| None` | **low, crash-not-silent**: guarded at runtime by `if t.status != "ok": continue`, and `calibrate` sets both taus whenever status is `ok`. If the invariant were ever broken the result is a `TypeError` recorded as a failed run, never a silently missed detection. Recommend an explicit assertion after Pilot 2. |
| `validation/trace_regression.py:104-112` | `**common` dict typing | none: keyword bundling, no behavioural effect |
| `validation/convergence.py:178,180` | `v1.value` where `v1` is optional | low, crash-not-silent: guarded by the `numeric = all(...)` test mypy cannot narrow through |
| `mutations/base.py:640` | `Match.group` on a possibly-`None` match | low, crash-not-silent: a failed parse raises rather than emitting a wrong edit |
| `protocols/rheobase.py:102-104` | ndarray assigned to `Sequence[int]` | none: annotation mismatch only |

**No finding in the scientific core can produce a silently wrong detection, classification or
denominator.** The worst case in each is an exception, which the pipeline records as a run failure.
This is a reading of the guards, not a proof; the findings stay on the record as a baseline and
should be closed module by module after Pilot 2.

## 3. Authorization status

The gate ran **after** the passing readiness run, at the same commit, and returned **AUTHORIZED** on
all nine conditions (`results/audits/pilot2_authorization/20260918T004554+0000.json`). The gate is
sound as written; its blind spot is that **it has no condition for prior outcome exposure**. That is
the amendment this audit requires.

## 4. Has Pilot 2 started?

**Yes, and it was stopped during this audit.** 564 raw run records, 38 of 143 frozen variants begun
across two models, no aggregate outputs, nothing summarised or inspected. Full detail in the leakage
assessment, section 7. The partial data is preserved and is labelled
`status_uncertain_pending_audit` in `results/CAMPAIGN_STATUS_PILOT2.json`.

## 5. Leakage classification

**L5** (campaign began), with an **L4** component (kinetics outcome exposure while two design
artefacts were still being authored). Evidence: leakage assessment sections 1–6; overlap table;
timeline in section 4 of that document.

**Exact overlap counts:** 48 executions; **9 exact overlaps** with frozen Pilot 2 mutants = 9 of 88
primary semantic mutants (10.2%) and 9 of 12 kinetics mutants (75%); 4 of 5 models affected; 1
analysis family; 1 protocol (the canonical comparator); 0 unreconstructable cases.

## 6. Which claims survive

**Still defensible**

1. The protocol battery was never selected using kinetics information — enforced in code
   (`SELECTION_EXCLUDED_FAMILIES`) and tested.
2. Pilot 2's design — models, protocols, families, severities, thresholds, exclusions, branch rules,
   denominators — was fixed at 16:41 on 2026-09-17, before any Pilot 2 outcome existed, and is
   hash-committed.
3. The executing matrix is exactly the frozen matrix: all 143 variant ids match, verified by set
   comparison after launch.
4. Pilot 1's raw data is unchanged: 2,689 files re-hashed, zero mismatches.
5. The 76 non-kinetics primary semantic mutants, the 40 controls and the 15 numerical stress tests
   carry **no** prior outcome exposure.
6. `pospischil2008_fs` carries no kinetics exposure at all.

**No longer defensible**

1. "Pilot 2 was frozen before any Pilot 2 outcome was observed." False: kinetics outcomes on four of
   the five models were observed before the freeze commit, and the protocol text was edited after.
   The sentence in the protocol header must be amended.
2. "The kinetics family is unseen on the Pilot 2 models." False for nine specific mutants.
3. Any future use of these five models — or their five source repositories — as *held-out*
   confirmatory models. They were already declared development sources in the protocol; this
   confirms it irreversibly.
4. The commit message of `cffd026` ("frozen before execution") is accurate only about the campaign,
   not about outcome exposure. It cannot be rewritten (no history rewriting); it is corrected here
   and in the deviation log.

## 7. Recommended path

**Path C — reclassify as development-exposed** — with the important note that Pilot 2 was *already*
classified as exploratory development data from the outset. Path A is impossible (outcomes were
exposed and the campaign began). Path B is refused because it requires the design to be
demonstrably frozen before exposure, and the protocol file was edited afterwards.

What Path C requires here, concretely:

1. **Keep every byte.** No partial result, log, plot or hash is removed. Done.
2. **Never call Pilot 2 confirmatory.** Already true by construction; the amendment restates it.
3. **Record the nine exposed variants by name** and report Pilot 2's primary result both with and
   without them, prespecified before the campaign resumes. The nine are listed in the leakage
   assessment, section 6.
4. **Do not replace the exposed variants based on their outcomes.** They stay in the matrix; the
   frozen matrix does not change.
5. **Amendment, not silent edit:** a numbered, timestamped amendment to `docs/PILOT2_PROTOCOL.md`
   correcting the freeze claim and adding the with/without-exposed-variants reporting rule.
6. **Reserve a genuinely untouched split for the confirmatory study** — see section 8, which is now
   the binding constraint on publication.

Resuming the stopped campaign is legitimate under this path: the matrix is frozen and
hash-verified, resumption is content-addressed (completed runs are reused, nothing is re-selected),
and no threshold or rule changes. Resuming is *not* a new authorization to treat the result as
confirmatory.

## 8. Is a new held-out split required? Yes — and it is not currently feasible

Development sources are now: `pospischil2008`, `neuroml2_examples`, `acnet2_traub1991`,
`migliore2014`, `osb_allen_hh2`. Against `manifests/CURATION_FINAL_TABLE.csv`:

> **Eligible models from untouched sources: 0 of 7.** All seven eligible models are now development.

The untouched candidate pool is:

| source | models | status | why not eligible |
|---|---|---|---|
| `hay2011_bbp_channels` | `hay2011_soma`, `bbp2015_soma` | excluded | **runtime only** (3,465 s and 3,618 s per variant against an 1,800 s budget) |
| `traub2005` | `traub2005_testseg2`, `traub2005_testseg_all` | excluded | **runtime only** (3,036 s, 4,115 s) |
| `smith2013` | `smith2013_singlecomp` | excluded | **runtime only** (2,692 s) |
| `migliore2005` | `migliore2005_ca1_soma` | excluded | **runtime only** (2,449 s) |
| `prinz_stg` | `prinz2004_abpd`, `prinz2004_lp` | needs human judgement | spontaneously bursting; C08 (rheobase) undefined |
| `bahl2012`, `bezaire2016` | 2 models | excluded | no licence / missing files |
| `maex1998` | 2 models | excluded | no shipped simulation file |
| `solinas2007`, `wangbuzsaki1996` | 2 models | excluded | NeuroML validation failure (D-051 for WB) |

Six models from **four independent untouched sources** fail on the compute-budget criterion alone.
Raising C11 from 1,800 s to about 4,200 s would admit all six and make a four-to-six model held-out
set feasible. That criterion is outcome-independent — it is a statement about compute, not about
behaviour, and none of these models' mutation outcomes has ever been generated. It must still be
changed by a **numbered amendment recorded before any held-out mutant is generated**, because
criterion C11 was already adjusted once (X-18) and a second adjustment needs to be visibly
principled rather than convenient.

Cost estimate at a 4,200 s budget: about 4,000 s per variant × ~25 variants × 5 models ≈ 139 CPU
hours ≈ 12 hours wall-clock on 12 workers.

## 9. Cache-key verification (no campaign run)

The key is the SHA-256 of the whole run payload (`execution.py`, `_run_id`), so every listed field
changes the run id.

| required component | covered? | how |
|---|---|---|
| full dependency closure, not just the top model | **yes** | `inputs_manifest` hashes every file reachable from the LEMS or cell entry point: included NeuroML, channel definitions, LEMS component files, morphology and auxiliary files |
| model-generation code version and digest | yes | `GENERATION_VERSION`, `generation_code_digest()` |
| frozen configuration hash | yes | `config_sha256` (study + features + tolerances) |
| protocol parameters | yes | serialised `ConcreteProtocol` list |
| simulator name, version, jar | yes | `simulator`, `simulator_version`, `jar_sha256` |
| Java runtime build | yes | `java_version` |
| time step, solver, sampling | yes | `exec` (`dt_ms`, `integrator_method`, `sample_every_ms`) |
| simulation duration, initial conditions, units | yes | inside the protocol record and the hashed model files |
| temperature | yes | explicit `temperature` field |
| recording location and variable | yes | `recording` |
| replicate index | yes | `replicate` |
| feature-extraction code and configuration | yes, for feature artefacts | `feature_code_digest()`, `features_cfg_sha256`, eFEL version |
| random seed | not applicable | execution is deterministic; variant-site seeds are recorded in `generation.json` |
| **Git commit of the working tree** | **partial** | recorded in each `run.json` for provenance but **not** part of the cache key — deliberate: the generation-code digest covers the code that builds inputs, so unrelated commits do not invalidate caches |
| **dirty-tree state** | **no** | not in the key |
| **environment or container digest** | **partial** | Java, jar, simulator and eFEL versions are keyed; the full Python dependency set is not |

`tests/unit/test_run_record_fields.py::test_cached_runs_are_reused_only_under_an_identical_cache_key`
already proves a cache miss when the Java build changes and when `GENERATION_VERSION` changes.

**Gaps, recorded as non-blocking with reasons:** dirty-tree state and the full Python environment
digest are not in the key. Neither affects the simulator's output — jNeuroML and the JVM produce the
trace, and both are keyed — but a change to Python-side *feature extraction* would be caught only by
`feature_code_digest`, not by a dependency upgrade. Recommended after Pilot 2: add
`requirements.lock` hash to `cache_context()`, and extend the parametrised cache test to alter each
component in turn. Neither gap justifies altering the frozen campaign now.

## 10. RMSE limitation (documented, not changed)

Measured on the rehearsal reference (`pospischil2008_rs`, `trace_tolerances.json`):

| protocol | reference spikes | reference RMSE (h vs h/2) | resulting τ_rmse |
|---|---|---|---|
| `P04_step_2x` | 22 | 15.5 mV | 46.5 mV |
| `P07_hyperpolarizing_step` | 0 | 0.0005 mV | 0.5 mV (floor) |
| `P00_canonical` | 5 | 2.9 mV | 8.6 mV |

Pointwise RMSE compares voltages at equal times. A sub-millisecond spike-time shift puts a full
action potential (~100 mV) against a resting value, so RMSE grows with spike count rather than with
biological difference. Because the threshold is calibrated on the reference's own h-versus-h/2
error, heavily spiking protocols get very loose thresholds and RMSE becomes insensitive there. This
is the calibration behaving as specified, not a defect: it refuses to call a difference a detection
when the solver alone produces one that large.

In the live campaign this also excluded four model-protocol pairs from trace regression outright
(`osb_hh2` on P05 and P00, `pospischil2008_fs` on P04 and P05), because the reference's own spike
count changes between h and h/2. Recorded, never silently dropped.

- The RMSE rule **was frozen before any Pilot 2 outcome exposure** (`configs/tolerances.yaml`
  unchanged since before 2026-09-17 16:41).
- Changing it now would be methodologically permissible **only** as a pre-launch amendment applied
  before the campaign produces any analysed result, and only if the change is outcome-independent.
  Since 38 variants have already executed (though none analysed), any change would have to invalidate
  and re-run those variants to avoid mixing rules.
- The primary analysis remains valid without any change: level C rests on three metrics, and on
  spiking protocols detection is carried by **spike count** (any change detected, τ = 0.5) and
  **spike timing** (τ = 9.3 ms on P04, 1.5 ms on the canonical harness in the rehearsal).

**Options for Neel, no change made:**
1. Keep the frozen rule and disclose the limitation in the results.
2. Issue a numbered pre-launch amendment, refreeze and restart the campaign from zero.
3. Keep the primary rule and prespecify a time-aligned or spike-aware distance (for example DTW or
   spike-train distance) as a **secondary sensitivity analysis** only.

My recommendation is option 3: it costs nothing, changes no primary result, and directly answers the
reviewer question this limitation invites.

## 11. Statistical plan check

`docs/STATISTICAL_ANALYSIS_PLAN.md` already does **not** treat the 88 mutants as 88 independent
replications: the unit of analysis is a mutant, but the **cluster is the base model** (`model_id`),
with clustering by `source_family` when models share a paper, and the confidence interval and
permutation test are both cluster-level (`cluster_bootstrap_diff`, `cluster_permutation_test`, with
a written caveat about few clusters).

Already satisfied: per-model results, per-family and per-severity tables, attrition counts at every
stage, model-clustered uncertainty, separate reporting of the 40 controls and 15 numerical stress
tests, frozen seeds and tie-breaking, exact denominators, and AI/agent work reported as secondary.

**Amendments required before the results are written up** (not applied in this audit):

1. State explicitly that the **five models are the generalization units**, and that with five
   clusters the interval is coarse — report per-model values alongside any pooled estimate.
2. Require **cost-matched** random-battery comparisons, not only protocol-count-matched.
3. Add the with/without the nine exposed kinetics variants reporting rule.
4. Add an explicit prohibition on claiming universal behavioural equivalence or broad biological
   validation from five single-compartment models.

## 12. Blocking and non-blocking

**Blocking before any Pilot 2 result is reported**

- B1. Protocol amendment correcting the freeze claim and adding the exposed-variant reporting rule.
- B2. The nine exposed variants recorded by id in the protocol and in the deviation log.

**Blocking before any confirmatory held-out study**

- B3. No eligible untouched models exist. C11 must be amended (or the Prinz C08 question resolved)
  before a held-out split is possible.
- B4. External preregistration is **not complete**: no AsPredicted submission, no timestamp, no
  registration URL. `docs/CONFIRMATORY_PREREGISTRATION_DRAFT.md` remains a draft.
- B5. No Git remote is configured, so no off-machine copy of the pre-run commit exists.

**Non-blocking limitations**

- N1. RMSE insensitivity on spiking protocols (section 10).
- N2. Cache key omits dirty-tree state and the Python environment digest (section 9).
- N3. 186 lint and 120 type findings recorded as baselines; none capable of a silent wrong answer.
- N4. Four model-protocol pairs excluded from trace regression by their own refinement instability.
- N5. Per-site run ids and model hashes were not recorded by the kinetics validation table.

## 13. Files that would require amendment

| file | amendment |
|---|---|
| `docs/PILOT2_PROTOCOL.md` | numbered amendment A-01: correct the freeze statement; list the nine exposed variants; add the with/without reporting rule |
| `docs/DEVIATION_LOG.md` | X-23: outcome exposure before the freeze commit; X-24: campaign started before this audit and stopped at 38 of 143 variants |
| `DECISIONS.md` | D-055 recording the L5/L4 classification and Path C |
| `scripts/pilot2_authorize.py` | add a condition that no frozen variant's outcome was generated outside the campaign |
| `docs/STATISTICAL_ANALYSIS_PLAN.md` | the four amendments in section 11 |
| `manifests/PILOT2_PRE_RUN.sha256` | regenerate after the amendment, preserving the existing file as the pre-amendment record |

## 14. Decision

Pilot 2 remains what it always was — exploratory development data — and may be completed on its
frozen matrix under Path C, with the amendment above. It must never be described as confirmatory or
as untouched. The confirmatory held-out study is **blocked** on B3 and B4 and is the real gate on
publication.

`READY FOR HUMAN AUTHORIZATION`
