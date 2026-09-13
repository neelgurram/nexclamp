# Build note: agent-study harness (Milestone 9)

Owner files: `configs/agent_policy.yaml`, `agent_study/**`, `src/neurosem/experiments/__init__.py`
(docstring only; it was missing), `src/neurosem/experiments/agent.py`,
`tests/unit/test_agent_harness.py`, `docs/agent_study_protocol.md`.

No agent was launched, and no trials exist. Everything below is harness plumbing and
task-design checks, not study results.

## Requests to other module owners

1. **CLI `evaluate-agent` (owner of `src/neurosem/cli.py`).** `cmd_agent` currently calls
   `agent.score_trial(a.task, Path(a.trial_dir), Path(a.frozen_config) if a.frozen_config else None)`
   and prints with `json.dumps(score, default=str)`. `score_trial` now accepts a path and
   loads it with `load_frozen_config`, and raises `FrozenConfigError` with a clear message for
   `None`. Requested change: make `--frozen-config` required (scoring without a freeze is not
   meaningful), keep passing the path (or call `agent.load_frozen_config(Path(a.frozen_config))`),
   optionally add `--private-dir`, and print with `neurosem.schemas.dumps(score)` so the layer
   details are serialised instead of the dataclass `repr`.
2. **`.gitignore` (owner).** Request `results/agent_study/private/` to be ignored. That folder
   holds baseline copies and export records (the answer keys of seeded tasks); it must never
   be committed or pushed while trials may still run.
3. **ARCHITECTURE 3.6 signatures.** The implemented signatures are used, not the documented
   ones: `RunRecorder(campaign, sim, *, results_root, work_root, features_cfg, timeout_s)`,
   `run_canonical(ws, variant, canonical_proto, level_factor, replicate, need_traces)`,
   `build_fingerprint(rec, ws, variant, protocols, canonical_proto, nominal, level_factor, rcfg,
   settle_ms, include_rheobase, include_canonical)`. Please update ARCHITECTURE to match the code.
4. **No `VariantKind` for agent outputs.** Agent-edited models are recorded as
   `VariantKind.MUTANT` with `family="agent_study"` and `operator="agent_patch"`. The unedited
   oracle is `REFERENCE`; an oracle built with operator steps (t06) is `MUTANT`. Request:
   add `VariantKind.AGENT_TRANSFORM` (or document this convention) so that agent runs can never
   be mixed into mutant manifests.
5. **Unit-typo seed needs a non-default factor.** The `scale_conductance` defaults contain no
   power of ten, so t01 passes `operator_args: {factors: [0.1]}` to the operator's public
   constructor. Request: document constructor arguments as part of the operator contract, or
   add unit-scale factors (0.1, 10, 1e-3, 1e3) as a named variant for unit-error mutants.

## Design decisions and deviations

- **Mutation sites precompute their edits.** The adapter selects the first site whose
  parameters, or whose recorded changes, contain the task's values, and never imposes
  parameters on a different site. t02 uses the existing 0.9 amplitude factor (no 0.8 site).
- **Seeds are written byte-minimally.** Operators re-serialise whole documents (t01's
  multi-line `<neuroml>` start tag collapsed, `<notes></notes>` became `<notes/>` in t02). In
  an export, those artefacts pointed at the seeded file. `apply_steps(minimal=True)` (used only
  for exports) re-applies the operator's attribute edits to the original bytes, checks the
  result is semantically identical to the operator output, and refuses seeds that add/remove
  files or change anything other than existing attribute values. All four seeded exports now
  differ from the pristine snapshot in exactly one line. Consequence: structural operators
  (`omit_include`, `factor_file`, ...) cannot be used as agent-visible seeds without extending
  this; they remain usable as hidden oracle steps.
- **Export timestamps are normalised** to 2000-01-01T00:00:00Z for every file and directory of
  the trial and of `private/baseline` (the seeded file was otherwise ~96 min newer than the
  rest). Creation/inode-change times cannot be set portably; they reflect copy order only.
  The protocol requires a timestamp-preserving transfer and a check in the isolated environment.
- **Private records** default to `results/agent_study/private/<trial name>/` (the only
  in-repository location allowed); a private directory under the trial's parent folder is
  refused. `score_trial` finds the record by trial directory name.
- **Freeze coverage.** The frozen config requires `policy_sha256`, `evaluator_git_commit`,
  `public_runner_sha256` and per task `task_sha256`, `prompt_sha256`, `public_tests_sha256`,
  `hidden_spec_sha256` (`agent.freeze_hashes()`); `provisional: true` is refused. `prepare_trial`
  refuses uncommitted inputs (untracked files in the task folder, public runner, policy,
  `src/neurosem` or the model snapshot count) unless `allow_dirty=True`, which marks the export
  `development_only`. Under a frozen config `score_trial` compares the export record and the
  current files with the frozen hashes and requires the evaluator checkout to be at the frozen
  commit with no uncommitted changes in `src/neurosem`, `agent_study`, `configs`. Git is only
  queried read-only (`rev-parse`, `status --porcelain`).
- **Claim denominator.** `basic_pass_battery_fail` is `None` when the battery is not applicable.
  `summarize_scores` counts only non-provisional trials of transformation task types (t01–t08)
  that changed `model/`, reports every exclusion and a per-task-type breakdown.
- **Edit scope** uses its own semantic diff (not `mutations.xml_changes`; locator conventions
  differ: `/neuroml/...` here). It now compares element namespaces (pseudo-attribute
  `{namespace}`, recorded where it differs from the parent) and tail text (`{tail}`). Ignore
  patterns only hide new files; simulator outputs are recognised only when a LEMS file in the
  baseline or trial declares them (`OutputFile`/`EventOutputFile` `fileName`, `Target`
  `reportFile`/`timesFile`). The policy no longer ignores `model/**/*.dat` or `x86_64/**`.
- **Trial log** has a `logs` list (path + SHA-256); `validate_trial_log` can re-hash transcript,
  patch and logs (`root=`) and regenerate the patch (`private_dir=`, `trial_dir=`); access dates
  must be real calendar dates.
- The public checks share one runner, `agent_study/public_common/run_public_checks.py`, copied
  into each trial; only `public_checks.json` and `canonical_reference.json` are stored per task.
- The trial directory does not export the NeuroSem framework (`export.framework_include` is
  empty): NeuroSem contains the perturbation battery, and the agent may see public tests only.

## Task-design checks run on this machine

Direct XML edits, jNeuroML 0.14.0 / jLEMS 0.12.0, Temurin 21; plumbing checks only:

- jNeuroML does not reproduce the upstream OMV `.mep` spike times exactly (largest difference
  0.65 ms for HH, 1.29 ms for RS). The public canonical check therefore compares against
  `canonical_reference.json`, recorded from the unedited snapshot with the same jNeuroML
  (`agent_study/build_public_references.py`, run on 2026-09-13).
- Seeded exports through the real registries, then the public runner inside each export: every
  fault is visible to the public checks while the model files still validate. t01: 0 spikes
  (reference 7). t02 (0.675 nA): 2 spikes (reference 5). t07: the shipped simulation fails to
  build (`No such child element or variable IM in IM_all`). t09: 5 spikes, largest spike-time
  difference 23.5 ms. (Measured before the byte-minimal seeding change; the seeded values are
  identical, only formatting of other lines differed.)
- `Kd` appears in the quantity paths of the shipped LEMS files (FS 2, IB 1, LTS 1, RS 1). The
  t03 hidden spec requires all of them to be updated; a unit test covers a full rename and a
  channel-file-only rename.
- The canonical layer was run end to end in a unit test (HH, t05) against a **synthetic**
  tolerance table (tolerance 1e-3 per feature, test only): an SI-equal unit rewrite passes,
  a decimal slip on kChans is detected. The battery layer still reaches only the
  "no frozen protocol selection → error" path, because no frozen selection exists yet.

## Provisional values needing Neel's approval before freezing

- Budgets (80 turns, 60 min, 15 USD per trial), permissions and isolation rules in
  `configs/agent_policy.yaml`.
- Public spike-time tolerance of 1.0 ms (policy `public_checks`).
- t08 success threshold: at least a 2x reduction in integration steps (deterministic proxy for
  runtime; other speed-ups need the manual audit).
- Every hidden spec (`status: provisional`), including the permitted-change rules.
- The number of trials per task. The specification plans 20–30 Claude Code tasks; nine task
  definitions (one per task type) is not a sample size.

## Known limitations

- OS-level isolation (separate account/VM that cannot read the repository) is a human
  responsibility, described in the protocol; `prepare_trial` only refuses unsafe locations.
- Namespaced attribute names are compared by local name in the semantic diff (an `xsi:` prefix
  swap on an attribute is invisible); element namespaces are compared.
- Several lines exceed the 110-character ruff limit; the suite does not enforce it (core files
  also exceed it).
