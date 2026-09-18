# Cross-simulator validation (N-08)

*Written 2026-09-18. Evidence: `results/audits/cross_simulator/<stamp>/` (CSV, JSON, Markdown, and
the generated NEURON sources with hashes). Code: `src/neuraxis/simulators/neuron.py`,
`scripts/cross_simulator_check.py`, `tests/unit/test_neuron_adapter.py`.*

## Why this exists

Every detection in this study is produced by one integrator: jLEMS's fixed-step forward Euler. A
reviewer is entitled to ask whether a "behaviour change" is a property of the model or of that
integrator. The honest answer requires running the identical NeuroML through a second, independently
written simulator. NEURON is the obvious choice: it is the reference implementation in the field,
and jNeuroML can translate NeuroML into NEURON sources.

## Two levels of evidence, never merged

**Level 1 - portability.** `jnml <LEMS> -neuron` translates a model's shipped simulation into NEURON
sources: one `.mod` mechanism per ion channel and input, a `.hoc` cell definition and a `_nrn.py`
runner. This needs only Java and the jNeuroML jar, so it is collectable anywhere the rest of the
study runs. A model that exports cleanly is written faithfully enough for another simulator to
consume. A model that fails to export is a finding about that model, recorded with its exact error.

**Level 2 - agreement.** The exported model is compiled with `nrnivmodl`, executed, and its
canonical trace compared with the jLEMS trace. Reported quantities: spike counts, first-spike
latency, largest spike-time difference, and trace RMSE.

These are **descriptive numbers with no pass/fail threshold**, and that is deliberate. Every
tolerance in this study is calibrated against one integrator's own discretisation error (h versus
h/2). Two different integrators differ for reasons that have nothing to do with a mutation, so a
cross-simulator threshold would be an unjustified extrapolation of the calibration. Turning
agreement into a detection rule would need its own calibration study, which is out of scope.

## Level 1 result: all seven models export

Run 2026-09-18, jNeuroML 0.14.0 / jLEMS 0.12.0:

| model | source | export | `.mod` mechanisms | runner |
|---|---|---|---|---|
| `pospischil2008_rs` | pospischil2008 | yes | 5 | `LEMS_RS_nrn.py` |
| `pospischil2008_lts` | pospischil2008 | yes | 7 | `LEMS_LTS_nrn.py` |
| `pospischil2008_fs` | pospischil2008 | yes | 4 | `LEMS_FS_nrn.py` |
| `nml2_hh_example` | neuroml2_examples | yes | 4 | `LEMS_NML2_Ex5_DetCell_nrn.py` |
| `acnet2_pyr_soma` | acnet2_traub1991 | yes | 7 | `LEMS_m_in_b_in_nrn.py` |
| `migliore2014_mt_soma` | migliore2014 | yes | 7 | `LEMS_OlfactoryTest_12_nrn.py` |
| `osb_hh2_477127614` | osb_allen_hh2 | yes | 12 | `LEMS_477127614_nrn.py` |

**7 of 7 exported, 0 failures.** Every generated file is copied and hashed under
`results/audits/cross_simulator/<stamp>/exports/<model_id>/`, with the jNeuroML output tail, so the
artefacts are checkable later. This includes the two Pilot 1 models and all five Pilot 2 models.

## Level 2 status: blocked on a runtime, not on the code

The adapter is implemented and tested; what is missing is a NEURON runtime on this machine.

| route | status |
|---|---|
| `pip install neuron` | **unavailable**: no Windows wheel for CPython 3.12 (`No matching distribution found`) |
| WSL + Linux wheel | **unavailable**: `wsl.exe` exists but no distribution is installed (exit 50) |
| Official NEURON Windows installer | possible, but a system-level install that also needs a Python version it supports |
| Docker | unavailable on this machine (recorded earlier as X-13) |

The adapter therefore separates `export_available()` from `available()`. When the runtime is absent,
`run_lems` exports first and then returns `TOOL_FAILURE` with the message that the model
*exported successfully but cannot be executed here* — never `RUNTIME_ERROR`, because the model did
not fail. This distinction is covered by `tests/unit/test_neuron_adapter.py`.

**To complete level 2**, one of: install a WSL distribution and `pip install neuron` there; install
NEURON for Windows with a supported Python; or run `scripts/cross_simulator_check.py` on any Linux
or macOS machine with NEURON present. No code change is needed. The check is read-only with respect
to the study: it touches no campaign and no study result depends on it.

## How a level 2 result would be reported

Per model: jLEMS spike count versus NEURON spike count, first-spike latency in each, the largest
spike-time difference when counts match, and trace RMSE over the shared time grid. Reported as a
table with the two simulator versions beside it, described as agreement between independent
implementations, and explicitly **not** as a validation pass or failure of any model.
