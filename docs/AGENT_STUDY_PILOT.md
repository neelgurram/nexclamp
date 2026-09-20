# Agent study: feasibility pilot (not the confirmatory study)

*Run 2026-09-18 at commit `115673a`. Evidence: `results/agent_study/pilot_20260918/`
(`trials.csv`, `summary.json`, `agent_study_run.md`). Harness:
`src/neuraxis/experiments/agent.py`; operator tool: `scripts/agent_study_run.py`; protocol:
`docs/agent_study_protocol.md`.*

> **This is not the agent study.** It is a feasibility pilot of the harness, run under partial
> isolation and an unfrozen evaluation config. Nothing in it may be reported as a confirmatory
> result about AI agents. The reasons are stated exactly in section 4.

## 1. What was run

Three of the nine tasks were exported as clean trial directories and given to three **separate agent
sessions**, each with no access to this repository, no network, and no sight of the hidden checks or
the answer key:

| trial | task type | base model |
|---|---|---|
| `t01_unit_repair__r01` | repair a seeded unit error | `nml2_hh_example` |
| `t05_unit_conversion__r01` | convert a quantity to an equivalent unit | `nml2_hh_example` |
| `t06_single_conductance_change__r01` | change one conductance, preserve everything else | `pospischil2008_rs` |

Each session saw only `TASK.md`, `model/`, `public_tests/` and `scratch/`. The operator tool prints
trial paths and never prints a hidden assertion or a seed edit, so its output is safe to hand to an
agent session.

## 2. Result

| trial | edit scope | hidden assertions | schema valid | executes | canonical | battery | category |
|---|---|---|---|---|---|---|---|
| `t01_unit_repair__r01` | pass | pass | pass | pass | error | not evaluated | indeterminate |
| `t05_unit_conversion__r01` | pass | pass | pass | pass | error | not evaluated | indeterminate |
| `t06_single_conductance_change__r01` | pass | pass | pass | pass | error | not evaluated | indeterminate |

**What this shows.** All three agents stayed inside the files they were permitted to edit, and all
three made the edit the hidden answer key requires. The models remained schema-valid and executable.
The harness ran its layers in the prescribed order and refused to invent verdicts for the layers it
could not evaluate.

**What it does not show.** Nothing about the quantity this study actually claims -
`basic_pass_battery_fail`, the number of edits that pass the checks a practitioner would normally run
but fail the perturbation battery. That needs the last two layers, which are blocked (section 3).

An agent's own report is not a result. One session reported converting two quantities, another
reported a transient wrong value during editing; the scoring above comes from the hidden evaluator
comparing the trial against the private baseline, not from what any agent said about itself.

## 3. Why the last two layers could not run

The canonical and battery layers need a **populated evaluation config**: the frozen tolerance table,
the selected protocol battery, and the reference rheobase of each base model. `FrozenConfig.development()`
carries none of those by design, so `canonical_passes` returns `error` and the battery layer is
correctly marked `not_evaluated` rather than assumed.

This is the protocol's own ordering (section 1, step 1): *finish the frozen main study first*. Those
values are produced by the main campaigns. Pilot 2 covers `nml2_hh_example` and
`pospischil2008_rs` is covered by Pilot 1, so once Pilot 2 completes, a populated config can be
written for exactly these base models and the full six-layer cascade becomes available.

## 4. Why this is not the confirmatory study

1. **Isolation is partial.** The protocol requires environmental isolation: a separate OS account,
   container or VM that cannot read this repository, which holds the private records and answer keys.
   These sessions ran under the same account. Recorded as `isolation: partial` in every output.
2. **The evaluation config is not frozen.** Every score is `provisional`, and a provisional score is
   excluded from the claim fraction by construction.
3. **The exports are `development_only`.** They were taken from a tree with uncommitted changes, and
   a frozen config refuses to score such an export.
4. **The hidden evaluators have not had independent review.** N-12 is still open: the hidden checks
   were written by the same assistant that built the harness, and Neel has not reviewed them.
5. **Three trials, one replicate each.** No inference of any kind is supported by this sample.

## 5. What a confirmatory run needs

- The frozen main study finished, and a `frozen_agent_eval.yaml` written outside version control with
  the tolerance table, protocol selection, per-model reference rheobase and every required hash.
- A dedicated OS account, container or VM for the agent sessions, with Java and pyNeuroML but no
  copy of this repository, and no user-level agent configuration.
- Neel's review of the nine hidden specs and of the budgets, prompts and thresholds (N-12, and the
  protocol's provisional status).
- A committed, tagged checkout for exports and scoring, and the planned replicate count recorded
  before the first trial.

Until all five hold, agent results stay in this document and are labelled a pilot.
