# Agent-study protocol (Milestone 9)

This protocol describes how a human runs the Claude Code case study of the NeuroSem
specification ("Claude Code experiment"). It is a secondary study. In the manuscript it
belongs in a subsection titled *Application to AI-assisted neuronal-model transformation*,
and Claude must not appear in the paper title.

The harness (`src/neuraxis/experiments/agent.py`) only prepares and scores trials. It never
starts an agent. Every trial is started by a person, following the steps below.

**Status: provisional.** Budgets, the public spike-time tolerance, the runtime threshold of
task t08 and every hidden spec are proposals. Neel approves them before step 1. After step 1
nothing listed there may change for the study being reported.

## 0. Components

| Item | Location | Seen by the agent? |
|---|---|---|
| Policy (permissions, budgets, isolation) | `configs/agent_policy.yaml` | no |
| Task definitions, including seeded faults | `agent_study/tasks/<task_id>/task.yaml` | no |
| Frozen prompts | `agent_study/tasks/<task_id>/prompt.md` | yes, copied as `TASK.md` |
| Public checks | `agent_study/tasks/<task_id>/public_tests/` + `agent_study/public_common/run_public_checks.py` | yes |
| Hidden evaluator specs | `agent_study/hidden/<task_id>/hidden_checks.yaml` | **never** |
| Frozen evaluation config | `results/agent_study/<study>/frozen_agent_eval.yaml` | no |
| Private trial records (baseline copy, export record = answer key) | `results/agent_study/private/<trial name>/` (default) | **never** |

Private records are never stored next to a trial directory: `prepare_trial` refuses a private
directory that lies under the trial's parent folder, because an agent could reach it with a
relative path (`../<trial>.private/`). Their default location is inside the repository, which
the isolated agent environment cannot read (step 2).

The nine tasks correspond one-to-one to the nine task types in the specification:

| Task | Type |
|---|---|
| t01_unit_repair | Repair a seeded unit error |
| t02_stimulus_restore | Restore a changed stimulus protocol |
| t03_channel_rename | Rename a channel safely |
| t04_include_refactor | Refactor included model files |
| t05_unit_conversion | Convert a quantity to an equivalent unit |
| t06_single_conductance_change | Change one specified conductance while preserving all other parameters |
| t07_channel_reference_repair | Repair a channel reference |
| t08_runtime_improvement | Improve runtime without changing tested outputs |
| t09_behaviour_diagnosis | Diagnose why a schema-valid model changed firing behaviour |

t01–t08 ask for a model transformation. t09 asks for a written diagnosis and forbids model
edits, so its trials are reported separately and never enter the claim fraction (step 6).

The specification plans for 20–30 Claude Code tasks in the full study. Nine task
definitions is not a sample size. The number of trials per task, and whether more task
instances are added (other base models or other seeded sites for the same task types), are
decided and recorded at step 1, before any trial runs.

## 1. Freeze NeuroSem before agent testing

1. Finish the frozen main study first. The frozen tolerance table and the selected protocol
   battery must exist, and must have been chosen without looking at any agent output.
2. Generate the public canonical references with the frozen jNeuroML:
   `python agent_study/build_public_references.py` (writes
   `public_tests/canonical_reference.json` for each task that uses one). Review the files.
3. Run the harness unit tests: `python -m pytest tests/unit/test_agent_harness.py -q`.
4. Commit everything (code, `agent_study/`, `configs/`) and tag the commit. From now on
   exports and scoring run from a clean checkout of that tag (for example a separate
   `git worktree`): `prepare_trial` refuses uncommitted inputs, and `score_trial` refuses to
   run when the evaluator is not at the frozen commit or has uncommitted changes in
   `src/neuraxis`, `agent_study` or `configs`. Do not commit to that checkout until every
   trial is scored.
5. Write `frozen_agent_eval.yaml` (schema `neurosem-agent-frozen/1`) **outside version
   control** (under `results/agent_study/<study>/`) with these fields: `campaign`,
   `results_root`, `dt_ms`, `timeout_s`, `tolerance_table`, `tolerance_table_sha256`,
   `tolerance_multiplier` (1.0 for the primary analysis), `selected_protocols`,
   `reference_rheobase_nA` (per base model, from the frozen reference runs), `configs` (study,
   features and tolerances, each with path and SHA-256), `evaluator_git_commit` (the full
   hash of the tagged commit), and the output of `agent.freeze_hashes()`: `policy_sha256`,
   `public_runner_sha256`, and per task `task_sha256`, `prompt_sha256`,
   `public_tests_sha256` and `hidden_spec_sha256`. Every field is required. Do not set
   `provisional`; a provisional frozen config is refused.
6. Record the commit hash, the SHA-256 of `frozen_agent_eval.yaml`, and the planned number
   of trials per task. `load_frozen_config()` refuses the config if any hashed file changed
   (tolerance table, configs, policy, public runner, any task definition, prompt, public test
   or hidden spec). `score_trial()` also refuses a trial whose export record names another
   commit, another task/prompt/public-test/policy version, or an uncommitted
   (`development_only`) source.

## 2. Prepare the isolated trial environment (once per study)

Tool permission settings are not a security boundary: an agent's shell can read any path its
operating-system account can read. Isolation therefore comes from the environment.

1. Use a dedicated OS account, container or VM that **cannot read** the NeuroSem repository
   (which holds the private records), or earlier trial directories. Keep the repository and
   all private records under a different account.
2. Install Java and a Python environment with `pyneuroml==1.3.22`, and nothing from
   NeuroSem. Check that `python -c "import neurosem"` fails in this environment. If the jar or
   Java cannot be found automatically, set `NEUROSEM_JAVA` / `NEUROSEM_JNML_JAR`.
3. Install the Claude Code version under study. The account must have no user-level Claude
   Code configuration: no CLAUDE.md, memory, skills, plugins, hooks or MCP servers. Network
   access is blocked apart from what the Claude Code session itself needs to reach the model
   service. Web tools are denied.
4. Configure permissions exactly as `configs/agent_policy.yaml` → `permissions` specifies.
   Check the flags and settings against `claude --help` and the documentation **of the
   installed version**. This protocol deliberately does not assume flag names. Record the
   exact command line, and use it unchanged for every trial.
5. Record the version string exactly as the CLI reports it (for example the output of
   `claude --version`), the underlying model identifier as the session reports it, and the
   access date.

## 3. Run one trial

Every trial of a task starts from the same clean export: the `content_sha256` in
`EXPORT_MANIFEST.json` must be identical across trials of that task.

1. **Export** (on the NeuroSem side, in the frozen checkout):
   ```python
   from neurosem.experiments import agent
   exp = agent.prepare_trial("t01_unit_repair", Path("/trials/t01_unit_repair-r01"))
   assert not exp.development_only
   ```
   The export contains `TASK.md`, `model/`, `public_tests/`, `scratch/` and
   `EXPORT_MANIFEST.json`. It contains no `.git`, no hidden spec, no `task.yaml`, no
   `PROVENANCE.json`, no NeuroSem code and no results. The seeded fault is written
   byte-minimally (only the edited attribute value differs from the original file), and every
   file and directory carries the same timestamp, 2000-01-01T00:00:00Z, so neither formatting
   nor modification times point at the edited file. `exp.private_dir`
   (default `results/agent_study/private/t01_unit_repair-r01/`) holds `baseline/` and
   `export_record.json`. The export is refused if its path lies inside the repository, if the
   private directory is reachable from the trial's parent folder, if the inputs are not
   committed, or if the leak scan finds a hidden marker. Check that
   `agent.verify_export(trial_dir)` and `agent.check_export_times(trial_dir)` both return `[]`.
2. **Transfer** only the trial directory into the isolated environment, with a method that
   preserves modification times (for example a `tar` archive extracted with default options,
   `rsync -a` or `cp -a`); never one that stamps the current time. In the isolated
   environment, before the session starts: (a) compare every file's SHA-256 with
   `EXPORT_MANIFEST.json` and check that no other files exist (for example with `sha256sum`);
   (b) check that all files and directories still have the normalised timestamp (for example
   `find . -printf '%T@\n' | sort -u` prints a single value, 946684800). If timestamps were
   not preserved, re-normalise them (for example
   `find . -exec touch -h -d "2000-01-01 00:00:00 UTC" {} +`) and repeat the check.
3. **Start a fresh session** with the working directory set to the trial directory. Never
   resume or continue a session. One trial per session.
4. **Give the prompt verbatim**: the full content of `TASK.md`, sent as the first and only
   human message. Nothing else is said during the trial.
5. **Do not intervene.** Do not answer questions, approve prompts, correct, hint, restart or
   edit files. If anything forces a human action (a permission prompt, a crash that needs a
   restart), stop the trial, record the event in `human_interventions` and treat the trial as
   invalid. It is reported, but excluded from the scored fraction.
6. **Stop** when the agent ends its turn or a budget limit (turns, wall clock, cost) is
   reached. Record which.
7. **Collect** the complete transcript (raw export, unedited), the session's cost and token
   report (if the tool reports them; otherwise record `null` with the source), and every tool
   or session log, each with its SHA-256. Copy the trial directory back without modifying it.
8. **Patch**: `agent.make_patch(private_dir / "baseline", trial_dir, policy.ignore_paths)`.
   Save it next to the transcript. (Ignore patterns and the simulator output files named in
   the LEMS files hide only *new* files; edits to exported files always appear.)
9. **Trial log**: fill a `TrialLog` (version, model identifier, access date, permissions and
   their hash, budget, prompt hash, transcript path and hash, patch path and hash, `logs`
   (list of path and hash), costs, `human_interventions` (must be `[]`), export content hash,
   session details, start and end times, termination). Run
   `agent.validate_trial_log(log, task=..., policy=..., export_record=..., root=<record folder>,
   private_dir=..., trial_dir=...)`, which also re-hashes the transcript, patch and logs and
   regenerates the patch, and write it with `agent.write_trial_log` (write-once) under
   `results/agent_study/<study>/trials/<trial_id>/`.

## 4. Score with the deterministic hidden tests

```python
score = agent.score_trial("t01_unit_repair", trial_dir,
                          Path("results/agent_study/<study>/frozen_agent_eval.yaml"))
agent.write_score(score, trial_record_dir / "score.json")
```

`score_trial` accepts the frozen config object or its path, and finds the private record at
`results/agent_study/private/<trial directory name>/` unless `private_dir` is given.

Layers (the first four form a cascade):

1. `schema_valid`: `jnml -validate` on the files named in the hidden spec.
2. `executes`: the shipped simulation runs (in a copy of the trial).
3. `canonical_passes`: canonical-protocol features, trial versus oracle, within the frozen
   tolerances.
4. `hidden_battery_passes`: the frozen selected perturbation protocols, trial versus oracle,
   within the frozen tolerances.
5. `hidden_assertions_pass`: deterministic parameter, structure and answer checks.
6. `edit_scope`: a semantic XML diff against the exported baseline (comments, whitespace and
   attribute order ignored; element namespaces and tail text compared). Any change not
   permitted by the hidden rules counts as an unauthorized edit. New files count too, except
   in `scratch/`, interpreter caches, and the output files the shipped LEMS simulations
   declare (`OutputFile`/`EventOutputFile` `fileName`, `Target` `reportFile`/`timesFile`).

The oracle is the model the correct edit should produce: the reference snapshot, the
exported state (diagnosis), or the reference with a named operator applied (t06).
`basic_pass` covers layers 1–3. `neurosem_pass` covers all six. A tool failure or an
unavailable evaluator gives `error`, which makes the trial indeterminate. It is never
counted as a pass or a fail. A score made with `FrozenConfig.development()` is marked
`provisional` and never enters a reported fraction.

## 5. Manual patch audit (after automatic scoring)

Audit every patch, including those that passed every layer. Record, per trial:

- whether the automatic classification is correct (and, if not, why; the automatic score is
  never edited, the disagreement is reported);
- whether any `representation_only` edits are acceptable;
- for t08, whether a speed-up not captured by the step-count assertion exists;
- for t09, whether the free-text `suspected_original_value` and `explanation` are correct;
- whether any unauthorized edit is scientifically harmful or merely out of scope.

## 6. Report

Use `agent.summarize_scores(scores, invalid_trials=...)`. Report the Claude Code version,
the model identifier, the access dates, the permissions and budgets, per-task-type
(`by_task_type`) and per-layer counts, indeterminate and invalid trials, the manual-audit
disagreements, and the figure-8 layer breakdown, labelled clearly as secondary. Report t09
(diagnosis) results separately. Publish transcripts and patches where redistribution is
permitted.

### Permitted claim (exactly as the specification states)

> Under the evaluated Claude Code configuration, a specified fraction of transformations
> passed basic checks but failed frozen perturbation tests.

The fraction is `basic_pass_battery_fail.count / basic_pass_battery_fail.denominator`. The
denominator contains only transformations: valid trials, scored under the frozen config, of
the transformation task types (t01–t08), that changed at least one file under `model/`, and
whose basic-validation and battery outcomes are determinate (a battery that errored, was not
evaluated or is not applicable is excluded). Report it together with the denominator and every
exclusion count (`excluded_provisional`, `excluded_not_transformation_task`,
`excluded_no_model_change`, `excluded_model_change_unknown`, `excluded_indeterminate`, and the
invalid trials).

### Prohibited claim (exactly as the specification states)

> Coding agents generally cannot be trusted in computational neuroscience.

The latter would require multiple agents, versions, task distributions, and much broader
evidence.

Also avoid treating a trial that passes every layer as proof that the edited model is
equivalent to the intended one. Passing is evidence about a finite set of protocols and
features only.
