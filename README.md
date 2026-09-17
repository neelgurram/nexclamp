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

> **Status.** The test framework is built and tested. Only exploratory development data exist (Pilot
> 1, reported in corrected form). There are no confirmatory results yet. Read in this order:
> - `docs/PLAIN_LANGUAGE_OVERVIEW.md`;
> - `docs/CURRENT_REPOSITORY_STATE.md`;
> - `docs/DECISIONS_REQUIRED.md`.

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
