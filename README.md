# NexClamp

**Perturbation-battery testing for behavioural preservation in computational neuron models.**

Does an edited neuron model still behave like the original? A model file can stay valid, run, and
pass its one standard test while responding differently to other electrical inputs. NexClamp runs
models under several current-clamp protocols, extracts interpretable electrophysiological features
(the model's *perturbation fingerprint*), calibrates detection with controlled mutations and
harmless transformations, and selects a compact stimulation battery. The battery is then evaluated
on models, and on a mutation family, that were not used to choose it.

> **Status: the confirmatory evaluation is complete.** The held-out campaign `heldout-v1` ran once
> under a preregistered, hash-locked configuration (AsPredicted #312455, registered 2026-09-19) and
> is sealed. On six models never used in development, the canonical regression test detected 69 of
> 82 behaviour-changing faults (0.841) and the selected three-protocol battery 80 of 82 (0.976), a
> paired difference of +0.134 (95% cluster interval +0.013 to +0.221), with 0 of 48 controls flagged.
> Six faults escaped the canonical test on both its features and its full voltage trace.
>
> Read in this order:
> - `docs/RESULTS_HELDOUT.md` - the results, with every preregistered criterion;
> - `docs/manuscript/MANUSCRIPT.md` - the paper draft;
> - `docs/PLAIN_LANGUAGE_OVERVIEW.md` - what the study does, in plain English;
> - `docs/manuscript/ONLINE_RESOURCE_1.md` and `docs/manuscript/ONLINE_RESOURCE_2.md` - methods
>   detail and the deviation log;
> - `docs/README.md` - what every other document in `docs/` is for.
>
> Development (pilot) data are exploratory and are never pooled with the confirmatory result.

## What is where

| Path | Contents |
|---|---|
| `src/nexclamp/` | the library: simulators, protocols, features, tolerances, mutations, selection, campaign machinery |
| `configs/` | study configuration; the ten files of the confirmatory study are hash-locked by `configs/FROZEN.lock` |
| `data/` | the model manifest (source, commit, licence per model) and the frozen development/held-out splits |
| `models/` | commit-pinned NeuroML snapshots, each under its own upstream licence |
| `scripts/` | analysis, figures, audit materials and integrity checks, one job per script |
| `workflows/` | the gated run scripts for each milestone of the execution plan |
| `tests/` | 1,002 unit and regression tests, plus integration tests that need the Java toolchain |
| `results/` | write-once raw run records, processed records, tables and figures, per campaign |
| `docs/` | the study documents; start at `docs/README.md` |
| `docs/manuscript/` | the article, its Online Resources, the reference list and the Word build |
| `docs/project/` | how the project was run: plan, decisions, requirements, risk register, audits |
| `agent_study/` | the separate agent-exposure study, with its hidden evaluators kept out of the agent's reach |

## Quick start

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.lock
.venv/Scripts/python -m pip install --no-deps -e .
.venv/Scripts/python scripts/bootstrap_java.py
.venv/Scripts/nexclamp smoke-test --out results/audits/smoke_test/local
```

## Main commands

| Command | What it does |
|---|---|
| `nexclamp smoke-test` | the nine infrastructure checks; failure blocks data collection |
| `nexclamp curate-models` | the model inclusion criteria, using reference simulations only |
| `nexclamp pilot` | a fixed development matrix (exploratory); set `NEXCLAMP_CONFIG_DIR` to a protocol's configs |
| `nexclamp analyze`, `nexclamp reproduce-paper` | tables and figures from recorded results |
| `nexclamp select-protocols` | greedy battery selection on the development split (kinetics family excluded) |
| `nexclamp evaluate-heldout` | gated: requires `configs/FROZEN.lock`; use `workflows/run_heldout.py` |

The workflow scripts in `workflows/` wrap each step of the execution plan
(`docs/handoff/NEURAXIS_EXECUTION_PLAN.pdf`).

## Integrity

- **Raw results** are write-once, and every run records its inputs, configuration, software commit
  and timing.
- **Development data** are labelled exploratory and never pooled with the confirmatory estimate.
- **The held-out evaluation** runs once, after the method is frozen and preregistered on
  AsPredicted.

Licence: Apache-2.0. Upstream model files keep their own licences
(`docs/LICENSING_MATRIX.md`).

## Reproducing the paper

Every table and figure is regenerated from the sealed campaign; nothing is edited by hand.

```bash
make setup                 # environment from requirements.lock, then the Java toolchain
make paper                 # secondary analyses, figures, supplements, audit kit
```

Individually:

```bash
python scripts/heldout_secondary.py --campaign heldout-v1   # S1-S6, levels B/C, sensitivity
python scripts/heldout_figures.py   --campaign heldout-v1   # figures h1-h5
python scripts/build_supplement.py  --campaign heldout-v1   # Online Resources 1 and 2
python scripts/audit_autocheck.py   --campaign heldout-v1   # automated re-check of the audit sample
```

## Verifying the sealed data

```bash
python scripts/verify_archive.py --campaign heldout-v1      # every raw file against its SHA-256
python -c "import hashlib,pathlib; [print(l.split()[1], hashlib.sha256(pathlib.Path(l.split()[1]).read_bytes()).hexdigest()==l.split()[0]) for l in open('configs/FROZEN.lock') if l.strip() and not l.startswith('#')]"
```

## Preregistration and provenance

- Preregistration: https://aspredicted.org/q2ag7w.pdf (AsPredicted #312455); local copy and its
  SHA-256 in `docs/preregistration/` and `docs/PREREGISTRATION_RECORD.json`.
- Frozen study configuration: `configs/FROZEN.lock` (10 files), tag `study-freeze-v1`.
- Code the confirmatory campaign ran on: tag `heldout-v1-code`.
- Every deviation from the plan: `docs/DEVIATION_LOG.md`.
- AI assistance: `AI_USE_LOG.md` and `docs/AI_DISCLOSURE.md`.

## Citing

See `CITATION.cff`. Please cite the manuscript when it is published, and the archived release for
the software and data: https://doi.org/10.5281/zenodo.23175106 (all versions) or https://doi.org/10.5281/zenodo.23175107
(the version used in the article).

## Name

The project was called NexClamp, then NexClamp, and is now NexClamp; each rename followed a
name-conflict audit (`docs/NAME_AUDIT.md`, `docs/NAME_DECISION_PACKET.md`). The `neurosem` and
`neuraxis` import names and the `neurosem` command still work, and the agent harness still
recognises the old module paths, so records written under the old names stay verifiable.
