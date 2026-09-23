# Neuraxis

**Perturbation-fingerprint testing for behavioural preservation in computational neuron models.**
*(Name provisional: see `docs/NAME_AUDIT.md`. Formerly NeuroSem; the `neurosem` import name and
command still work.)*

Does an edited neuron model still behave like the original? A model file can stay valid, run, and
pass its one standard test while responding differently to other electrical inputs. Neuraxis runs
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
> - `docs/manuscript/ONLINE_RESOURCE_1.md` and `_2.md` - methods detail and the deviation log.
>
> Development (pilot) data are exploratory and are never pooled with the confirmatory result.

## Quick start

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.lock
.venv/Scripts/python -m pip install --no-deps -e .
.venv/Scripts/python scripts/bootstrap_java.py
.venv/Scripts/neuraxis smoke-test --out results/audits/smoke_test/local
```

## Main commands

| Command | What it does |
|---|---|
| `neuraxis smoke-test` | the nine infrastructure checks; failure blocks data collection |
| `neuraxis curate-models` | the model inclusion criteria, using reference simulations only |
| `neuraxis pilot` | a fixed development matrix (exploratory); set `NEURAXIS_CONFIG_DIR` to a protocol's configs |
| `neuraxis analyze`, `neuraxis reproduce-paper` | tables and figures from recorded results |
| `neuraxis select-protocols` | greedy battery selection on the development split (kinetics family excluded) |
| `neuraxis evaluate-heldout` | gated: requires `configs/FROZEN.lock`; use `workflows/run_heldout.py` |

The workflow scripts in `workflows/` wrap each step of the execution plan
(`docs/handoff/NEURAXIS_EXECUTION_PLAN.pdf`).

## Integrity

- **Raw results** are write-once, and every run records its inputs, configuration, software commit
  and timing.
- **Development data** are labelled exploratory and never pooled with the confirmatory estimate.
- **The held-out evaluation** runs once, after the method is frozen and preregistered on
  AsPredicted.

Licence: Apache-2.0 (provisional). Upstream model files keep their own licences
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

See `CITATION.cff`. Please cite the manuscript when it is published, and the archived release
(Zenodo DOI) for the software and data.
