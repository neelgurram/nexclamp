# Neuraxis (formerly NeuroSem) dependency and version audit

> **Re-verification, 2026-09-16 (Neuraxis execution plan).** Pinned versions in `requirements.lock`
> were checked against the PyPI JSON API and GitHub releases:
> - **Current releases:** pyNeuroML 1.3.22, libNeuroML 0.6.7, eFEL 5.7.34, NumPy 2.5.3, SciPy 1.18.1,
>   pandas 3.0.5, matplotlib 3.11.2, lxml 6.1.3, neuromllite 0.6.1 and pytest 9.1.1 are each the
>   latest release. jNeuroML v0.14.0 is the latest GitHub release (2025-02-12); pyNeuroML v1.3.22 was
>   released 2026-06-02.
> - **ruff:** pinned 0.16.7; 0.16.8 is available.
> - **Not installed:** mypy (2.3.1 available); the type-checking gap is X-15 in
>   `docs/DEVIATION_LOG.md`. The statistics are implemented with SciPy and NumPy
>   (`src/neuraxis/analysis/bootstrap.py`), so statsmodels is not required.
> - **Move and rename:** this file moved from the repository root to `docs/`; the package is now
>   `neuraxis` (`src/neuraxis/`). The body below is the 2026-09-13 audit.


| | |
|---|---|
| Document | Milestone 0 deliverable "Dependency and version audit" (`docs/handoff/NEUROSEM_FINAL_SPEC.extracted.md`, Milestone 0). It also covers M0 item 1 of the handoff's initial prompt: "Separate existing functionality to reuse from genuinely new NeuroSem functionality" (`docs/handoff/NEUROSEM_CLAUDE_HANDOFF.extracted.md`). |
| Date | 2026-09-13 |
| Repository state | Branch `m0-audit`. The brief named commit `3cdb957`. While this document was being written, HEAD moved to `d323afa` ("Provenance dirty flag scoped to simulation-relevant paths"). Between the two commits only `AI_USE_LOG.md` and `src/neuraxis/provenance.py` changed; `requirements.lock` and `pyproject.toml` did not ([T13]). |
| Roles | Neel Gurram is the author and decides. Claude Code built the software and wrote this audit. |
| Study status | The Milestone 6 pilot (`neurosem pilot --campaign pilot`) started on 2026-09-13 at 17:11 UTC on commit `d323afa`, after most of this audit was written. Its results are pending or development-stage, and nothing in `results/` is quoted here as a study result. No study results exist. Development probes are quoted only as development observations, with their file references. |
| Fact-check | Every version, hash, date, code reference and setup-command status was re-checked on 2026-09-13 against the project venv, the installed package source, the evidence files, PyPI/Adoptium/python.org/GitHub APIs and the repository at HEAD `d323afa`. Corrections are made in place. |

## In plain English

- NeuroSem is built on other people's tools. It does not have its own simulator or its own spike detector.
- Think of a recipe that names exact brands. If a brand changes its formula, the cake can change even though the recipe did not.
- So every tool version is written down. The two most important downloads, the Java simulator file and the Java runtime, also have a fingerprint (a SHA-256 hash).
- The shopping list is `requirements.lock`. Today the installed packages match it exactly: 75 of 75.
- Some tools have traps. Example: pyNeuroML answers "False" both when a model is broken and when Java is missing. Section 3 lists each trap and how NeuroSem avoids it.
- The Windows setup was run on this laptop. The Linux, Docker and CI setups are written down but have never been run.
- A first practice run (the pilot) started on 2026-09-13. Its results are not ready, and this document does not use them.
- Section 5 separates what NeuroSem borrows from what NeuroSem adds. "Adds" means code written for this project. It is not a claim that the idea is new.

---

## 1. How to read the sources

| Key | Meaning |
|---|---|
| [E:pynml] | `docs/m0_evidence/tools/pyneuroml-jneuroml.research.json`, corrected by `pyneuroml-jneuroml.verify.json` |
| [E:nml] | `docs/m0_evidence/tools/neuroml-lems.research.json`, corrected by `neuroml-lems.verify.json` |
| [E:efel] | `docs/m0_evidence/tools/efel.research.json`, corrected by `efel.verify.json` |
| [E:omv] | `docs/m0_evidence/tools/omv.research.json`, corrected by `omv.verify.json` |
| [E:snu] | `docs/m0_evidence/tools/sciunit-neuronunit.research.json`, corrected by `sciunit-neuronunit.verify.json` |
| [E:env] | `docs/m0_evidence/environment/setup_commands.json` (M0 install tests in throwaway venvs) |
| [E:fix] | `docs/m0_evidence/fixtures/fixture_verify.json` |
| [C:ID] | A critique issue in `docs/m0_evidence/critique/<LENS>.json`. Only issues the skeptic (`<LENS>.skeptic.json`) upheld or softened are used, with the skeptic's revised severity. |
| D-0xx, N-xx | Entries in `DECISIONS.md` |
| [T#] | A command run for this document on 2026-09-13. The exact commands are in Appendix A. |

Where a `.verify.json` corrects its research file, this document uses the corrected value. "Unverified" means that nobody checked the point by running something or by reading a primary source.

---

## 2. Runtime dependencies at a glance

"Pinned" values were checked today in the project venv with `pip show`, `importlib.metadata` and `__version__` ([T2], [T3]). "Latest" values for PyPI packages come from the PyPI JSON API retrieved today ([T8]); where the M0 evidence recorded the same value, it is cited too.

| Component | Role in NeuroSem | Pinned / installed | Latest seen 2026-09-13 (release date) | Python support | Maintenance |
|---|---|---|---|---|---|
| CPython | Interpreter | 3.12.10 ([T1]) | 3.12.14, released 2026-08-12 ([T9]). The 3.12 line is in "security" status with end of life 2028-10 ([T9]). | Project requires `>=3.12,<3.13` (`pyproject.toml`) | Security fixes only for 3.12 ([T9]) |
| pyNeuroML | Ships the jNeuroML jar; NeuroSem locates the jar through it | 1.3.22 | 1.3.22, PyPI upload 2026-06-02 ([E:pynml], [T8]) | No `requires_python`; classifiers 3.10-3.14 ([T8]) | Active. Releases are cut from the `development` branch; `master` is stale at 1.3.8 ([E:pynml] verify) |
| jNeuroML (jar inside pyNeuroML) | Validation (`-validate`) and LEMS simulation | `jNeuroML-0.14.0-jar-with-dependencies.jar`, 28,904,516 bytes, SHA-256 `45ee565a65a66008a3b41935358d11b7c19cb6b5a67bbec22481d519f53db931` ([T3], [T4]) | GitHub release v0.14.0, 2025-02-12 ([E:pynml]) | Java program compiled for Java 8 (class-file major 52) ([E:pynml] verify) | Stable, low activity; no release since 2025-02-12 ([E:pynml]) |
| jLEMS (inside the jar) | The LEMS interpreter that steps the equations | 0.12.0, as reported by the jar and by its `pom.properties` ([T4]) | Newest GitHub release is v0.11.1 (2024-08-20). 0.12.0 exists only as the `development` branch version, with no tag ([E:nml] verify) | Java 8 target | Repository active, releases infrequent ([E:nml]) |
| org.neuroml.export, .model, .import (inside the jar) | NeuroML loading and export inside jNeuroML | 1.11.0 ([T4]) | No matching v1.11.0 tag seen ([E:pynml] verify) | Java | Not assessed |
| libNeuroML | Informational strict validation; source of the NeuroML v2.3.1 XSD used by transforms and tests | 0.6.7; `current_neuroml_version` = `v2.3.1` ([T3]) | 0.6.7, 2025-06-10 ([E:nml], [T8]) | No `requires_python`; classifiers 3.9-3.13, no 3.14 ([T8]) | Last release 2025-06; repository pushed 2026-07-31 ([E:nml]) |
| PyLEMS | Installed only because pyNeuroML requires it; not imported by NeuroSem | 0.6.9 | 0.6.9, 2025-11-26 ([T8]) | Classifiers 3.8-3.14 ([T8]) | Not assessed beyond release date |
| neuromllite | Installed only because pyNeuroML requires it; not imported by NeuroSem | 0.6.1 | 0.6.1, 2025-06-10 ([T8]) | Classifiers 3.9-3.13 ([T8]) | Not assessed beyond release date |
| eFEL (`efel`) | All electrophysiology feature extraction | 5.7.34 | 5.7.34, 2026-08-25 ([E:efel], [T8]) | `>=3.10`; wheels for win_amd64, manylinux x86_64 and aarch64, macOS arm64 only ([E:efel] verify, [T8]) | Active under openbraininstitute/eFEL; the old BlueBrain/eFEL repository is archived ([E:efel]) |
| numpy | Arrays everywhere; float32 trace storage | 2.5.3 | 2.5.3, 2026-09-06 ([T8]) | `>=3.12` ([T8]) | Release dates only, not reviewed further |
| scipy | `scipy.stats` in analysis; required by eFEL | 1.18.1 | 1.18.1, 2026-08-21 ([T8]) | `>=3.12` ([T8]) | Release dates only |
| pandas | Reading jLEMS `.dat` output; analysis tables | 3.0.5 | 3.0.5, 2026-07-22 ([T8]) | `>=3.11` ([T8]) | Release dates only |
| lxml | XML editing in mutations and transforms; XSD checks in tests | 6.1.3 | 6.1.3, 2026-09-02 ([T8]) | `>=3.8` ([T8]) | Release dates only |
| PyYAML | Loading `configs/*.yaml` | 6.0.3 | 6.0.3, 2025-09-25 ([T8]) | `>=3.8` ([T8]) | Release dates only |
| matplotlib | Figures | 3.11.2 | 3.11.2, 2026-09-11 ([T8]) | `>=3.11` ([T8]) | Release dates only |
| Eclipse Temurin JDK | Java runtime that runs the jar | `jdk-21.0.12.1+1` in `.tools/` ([T4], [T10]); archive SHA-256 `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e` (`.tools/jdk_provenance.json`) | The Adoptium API's "latest 21" today is the same release, `jdk-21.0.12.1+1` ([T8]); `JAVA_VERSION_DATE` 2026-08-18 ([T10]) | Not applicable | LTS. Adoptium lists 21 as supported until at least Dec 2029 ([E:env]; read through a web summariser, so paraphrased) |
| pip | Installer | 26.2.1 ([T1]) | 26.2.1, 2026-08-04 ([T8]) | `>=3.10` ([T8]) | Release dates only |

Every exact pin above is in `requirements.lock`. `pyproject.toml` pins `pyneuroml==1.3.22`, `libNeuroML==0.6.7` and `efel==5.7.34` exactly, and gives only lower bounds for lxml, numpy, scipy, pandas, pyyaml and matplotlib. Its comment says the ranges are "what the package is known to work with", while "the frozen study uses the lock file".

---

## 3. Core runtime dependencies in detail

### 3.1 CPython 3.12

**Why 3.12.** numpy 2.5.3 and scipy 1.18.1 need Python 3.12 or newer ([T8]). libNeuroML, neuromllite and OSBModelValidation claim support only up to 3.13 ([T8]). In M0 the stack also installed and imported on Python 3.14.7, but that was treated as a smoke test only; networkx 3.6.1 explicitly excludes CPython 3.14.1 ([E:env]). Python 3.13 was never tested ([E:env]).

**On this machine.** `py -0p` lists 3.14 as the default (marked `*`) and 3.12 ([T5]). Always pass `-3.12` to the launcher. In Git Bash, `python` resolves to 3.12.10 ([T5]).

**Version drift between routes.** The development venv uses 3.12.10. The Docker image uses 3.12.14, pinned by digest. CI takes whatever 3.12.x `actions/setup-python` provides at run time (`docs/REPRODUCING.md`, "Known limits on reproducibility").

**Guard.** `make setup` checks that both the interpreter and the venv are 3.12 (`Makefile`, `REQUIRE_PY312`). The guard commands were run by hand in Git Bash; make itself was never run (`docs/build_notes/infra.md`).

### 3.2 pyNeuroML 1.3.22

**Purpose.** pyNeuroML is the pip package that brings the jNeuroML jar. NeuroSem deliberately does not call pyNeuroML's Python runner or validator helpers (D-005).

**How NeuroSem uses it.**
- `src/neuraxis/simulators/jneuroml.py`, `find_jar()`: imports `pyneuroml.utils.misc.get_path_to_jnml_jar` to find the jar. The environment variable `NEUROSEM_JNML_JAR` overrides it.
- The transforms module reads unit factors from `NeuroMLCoreDimensions.xml` inside the jar (`docs/build_notes/transforms.md` §3).
- No other file in `src/`, `scripts/`, `workflows/` or `tests/` imports `pyneuroml` ([T6]).

**Support.** No `requires_python`, so pip will install it on untested interpreters. Classifiers list Python 3.10-3.14. Upstream CI runs only on `ubuntu-latest`, so Windows is not CI-tested ([E:pynml]). The wheel is pure Python plus the jar ([E:pynml]).

**Verified pitfalls and how NeuroSem handles them.**

| Pitfall | Evidence | NeuroSem handling |
|---|---|---|
| The jnml-backed validator and runners return a bare `False` both for an invalid model and for a missing Java runtime. On Windows even `return_string=True` returned `(False, '')`, because stderr is not captured when `os.name == 'nt'`. | [E:pynml] and verify | D-005: NeuroSem runs `java -jar <jar>` itself with `subprocess.run(..., capture_output=True)` and an argument list. A missing Java or jar gives `ValidationResult(valid=None)` or `RunStatus.TOOL_FAILURE`, never "invalid" (`JNeuroML.validate`, `JNeuroML.run_lems`). |
| `run_lems_with_jneuroml(skip_run=True)` raises `UnboundLocalError` in 1.3.22. The same code was on the `development` branch when fetched. | [E:pynml] verify (reproduced) | Not used. |
| `sys.exit` paths: `validate_neuroml2_lems_file` hard-codes `exit_on_fail=True` (it raised `SystemExit(1)` in a probe); `run_lems_with_jneuroml` defaults to `exit_on_fail=True`; the `pynml -validate` command line sets `exit_on_fail=True`. | [E:pynml] verify | Not used (D-005). |
| Commands are one shell string (`shell=True`) with include paths joined by `:` inside single quotes. jNeuroML's own `JNeuroML.java` also splits `-I` on `:`, so Windows drive letters would be split. | [E:pynml] verify (source reading; not run with an include path) | NeuroSem passes no `-I` argument. It runs each LEMS file from the file's own folder, by bare file name (`run_lems`). |
| The Java heap default (400M) is read from `JNML_MAX_MEMORY_LOCAL` once, at import time. | [E:pynml] verify | NeuroSem passes `-Xmx2G` explicitly (`JNeuroML(max_memory="2G")`; `configs/study.yaml` has `java_max_memory: 2G`). |
| `pyneuroml.io.write_neuroml2_file` validates through Java by default (`validate=True`). | [E:pynml] verify | Not used; no NeuroSem module imports `pyneuroml.io` ([T6]). |
| Installing from Git `master` gives old pyNeuroML 1.3.8 with jNeuroML 0.13.3. | [E:pynml] verify, [E:nml] verify | The PyPI release is pinned. The jar SHA-256 is part of every `run_id` (D-012) and is reported by `JNeuroML.version_info()`. |
| The analysis helpers (`generate_current_vs_frequency_curve`, `analyse_spiketime_vs_dt`) need `pyelectro` (extra `[analysis]`). pyelectro's last release is 0.2.7 (2023-06-22), with classifiers only up to Python 3.11. | [E:pynml] verify | Not installed ([T2]) and not used. |

**Maintenance.** 1.3.22 was released on 2026-06-02; the previous release was 1.3.21 on 2025-07-22 ([E:pynml]). License metadata: `LGPL-3.0-only` ([T2]); license questions belong to `LICENSE_AUDIT.md`.

### 3.3 jNeuroML 0.14.0 jar, jLEMS 0.12.0 and org.neuroml.export 1.11.0

**Version facts.**
- `JNeuroML().version_info()` runs `java -jar <jar> -v`. Today it reported `jneuroml_version 0.14.0`, `jlems_version 0.12.0`, `org_neuroml_export_version 1.11.0`, the jar SHA-256 above and Java `21.0.12.1` ([T4]).
- The Maven `pom.properties` files inside the jar agree: jNeuroML 0.14.0; jlems 0.12.0; org.neuroml.export, .import, .model, .model.injectingplugin, org.neuroml1.model and neuroml2-base-definitions 1.11.0 ([T4]).
- **Correction history.** The first M0 NeuroML/LEMS research inferred jLEMS 0.11.1, from the `master` branch of org.neuroml.export (1.10.1). The verifier read the jar itself and found 0.12.0 and 1.11.0 ([E:nml] verify). D-004 records this.
- The jar's MANIFEST says `Build-Jdk 1.8.0_91`. It bundles many third-party libraries (Apache, JAXB, JSBML, Jackson and others) whose licenses were not audited ([E:pynml] verify).

**How NeuroSem uses it** (all through `src/neuraxis/simulators/jneuroml.py`, class `JNeuroML`):
- `validate(files)` runs `java -Xmx2G -Djava.awt.headless=true -jar <jar> -validate <absolute paths>`. `validation/structural.py::check` calls it once for the whole include closure of a model (D-006).
- `run_lems(lems_file, outputs)` runs `java -Xmx2G -Djava.awt.headless=true -jar <jar> <LEMS file name> -nogui` inside the LEMS file's folder. `validation/execution.py` (`RunRecorder`) uses it for probe batteries, canonical harness runs and rheobase searches (`docs/ARCHITECTURE.md` §1 and §3.6).
- `version_info()` supplies provenance.
- jnml is called with at most 100 files at a time, because Windows limits a command line to 32,767 characters (`docs/build_notes/transforms.md` §4).

**Verified pitfalls and how NeuroSem handles them.**

| Pitfall | Evidence | NeuroSem handling |
|---|---|---|
| **Included files are not schema-checked.** A corrupted included channel file passed `jnml -validate <cell>`. | D-006 (verified 2026-09-13) | Relative structural oracle: every NeuroML file in the include closure plus the harness network files is validated. A variant is invalid if it adds any error its reference did not already have (`validation/structural.py`). |
| Upstream LTS `IT.channel.nml` and `Ca.nml` fail standalone validation by design (custom LEMS ComponentTypes). `LTS.cell.nml`, which includes them, validates. Only the first schema error per file is printed. | D-006; `transforms.md` §2.3 | A reference needs its cell file and harness network files to validate. Other failures are recorded as baseline errors. |
| **Coverage gap in test 10025** ("Ion channel in channelDensity should exist"): it checks `channelDensity` but not `channelDensityVShift`. RS without `Na.channel.nml` still validates. LTS without `Ca.nml` (used by the concentration model) also still validates. | D-020; `docs/build_notes/mutations.md` §4 | Such variants are sorted out at execution time (class 2) and flagged `canonical_runs_but_battery_failed`. Reporting the gap upstream is N-11. |
| A broken `<include href>` is reported as a missing channel (test 10025), not as a missing file. | `docs/build_notes/core.md`, "Other measured behaviour" | Error lines are normalised per file and compared with the reference's. |
| **Warnings do not fail.** `jnml -validate` exits 0 and prints "... passed with warnings". | D-021; `transforms.md` §2.1 (written before the rule changed) | `JNeuroML.validate` treats exit code 0 with no "N failed" in the summary as valid. Warning lines are kept as messages. |
| `jnml -validate` rejects LEMS files (`cvc-elt.1.a`). | `transforms.md` §2.2 | Edits to a LEMS harness are checked by running the harness. |
| A nonexistent path prints usage text and no summary line. | `core.md` | `validate` raises `FileNotFoundError` before calling Java, so a caller mistake is not recorded as a tool failure. |
| jNeuroML can crash with a Java exception while loading an existing file. | D-021; `docs/build_notes/model-curation.md` §2 | Recorded as a model defect (`valid=False`), not a tool failure. |
| **Integrator.** Reading the jLEMS source: RK4 is used only for "flattened" state types, and flattening needs `Dynamics simultaneous="true"`, which no NeuroML2 core type sets. Standard NeuroML models are therefore stepped with fixed-step forward Euler. The pyNeuroML verifier had read the default as RK4; the numerics skeptic re-read the source and sided with Euler. | [E:nml]; [C:NUM-01] softened to medium; [E:pynml] verify | Development observations agree with a first-order method. In `docs/pilot/dt_probe.md`, spike-time changes shrink roughly in proportion to dt. In `docs/build_notes/core.md`, errors shrank 1.3-5.3 times per halving of dt, not about 16 times as RK4 would give. `configs/study.yaml` records "fixed-step forward Euler". Execution was checked only on these fixtures, so the general statement still rests on the source reading. |
| **`<Meta method=...>` has no observable effect** through jnml 0.14.0. `rk4`, `eulertree` and the invalid value `bogus` all gave byte-identical output files on the RS cell. | `core.md`, "jLEMS ignores Meta" (pinned by `test_meta_integrator_method_does_not_change_trace`); `mutations.md` §4 | `solver_config` mutants are expected to be equivalent and serve as no-op controls. The source reading says `eulertree` does change the code path ([C:SWT-04] softened to medium; [C:STATS-10] softened, medium), so the equivalence is an observation for these models and this version only. |
| **Mid-run divergence.** A x20 time-step mutant (battery step 0.1 ms) overflowed Hodgkin-Huxley rate expressions. jLEMS printed "simulation started" plus a hint that the time step may be too large, then exited 1. | D-020 | `run_lems`: started plus hint gives `UNSTABLE`; started without the hint gives `RUNTIME_ERROR`; never started gives `BUILD_ERROR`. Non-finite or out-of-bound voltages in the output also give `UNSTABLE`; the bound was raised to 10 V (D-021). This is the log-based rule that [C:NUM-11] (upheld, medium) asked for. |
| **Time-label precision.** jLEMS prints time with about 7-8 significant digits of an accumulated clock. At dt 0.001 ms over 1000 ms, labels deviated by up to 3% of a step. | Docstring of `simulators/jneuroml.py::regularize_time`; `core.md` "jLEMS OutputFile format"; `docs/build_notes/features.md` "Observed facts" | `regularize_time` replaces the printed labels with the exact grid `t0 + i*dt`. It rejects a column that deviates by more than 25% of a step (`MAX_TIME_LABEL_JITTER = 0.25`). |
| Output files are tab-separated, SI units (s, V), with a trailing tab; voltage resolution is about 1e-5 mV. | `core.md` | `load_dat` converts to ms and mV. Traces are stored as float32 mV on a verified uniform grid (D-012). |
| jLEMS does not create output folders. | Code comment in `run_lems` | `run_lems` creates the folders and deletes any old output file before running. |
| jLEMS computes with `java.lang.Math`, which is not guaranteed to be bit-for-bit identical across JVMs and CPUs. | [C:NUM-08] softened to low | Expect bitwise-identical traces only with the same JRE and the same kind of host. Across hosts, compare within tolerances (`docs/REPRODUCING.md`, "Known limits", says the same). |
| The NeuroML docs describe jLEMS as suitable for single-compartment models only. | [E:nml] | All current manifest models are single-compartment (`mutations.md` §2). Multicompartment models would need NEURON (section 4.3). |

**Maintenance.** No jNeuroML release since 2025-02-12. Its `master` branch (last commit 2024-08-20, pom version 0.13.3) lags the release; a future NeuroML schema update may need a newer jar ([E:pynml]). The NeuroML2 `development` branch has an empty "v2.3.2" placeholder in `HISTORY.md`, but no v2.3.2 XSD exists yet ([E:nml] verify). jNeuroML's own CI matrix (Java 8, 11, 16, 17, 19, 21) builds from source; it does not test the jar that pyNeuroML ships ([E:pynml] verify).

### 3.4 Eclipse Temurin JDK 21.0.12.1+1

**What is installed.**
- `.tools/jdk-21.0.12.1+1/` holds a full JDK for Windows x64. Its `release` file says `IMPLEMENTOR_VERSION="Temurin-21.0.12.1+1"` and `JAVA_VERSION_DATE="2026-08-18"` ([T10]).
- Archive (`.tools/jdk_provenance.json`): `OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip`, 205,073,461 bytes, SHA-256 `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e`, from `https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip`, metadata source `https://api.adoptium.net/v3/assets/latest/21/hotspot`. D-004 says the hash was checked against the Adoptium API before extraction.
- Checked again today with `scripts/bootstrap_java.py --dry-run` ([T11]). The API returned the same SHA-256, and it matched the publisher's `.sha256.txt` file. The installed runtime's `JAVA_RUNTIME_VERSION=21.0.12.1+1-LTS` matched the release. Nothing was downloaded or written. The script also noted that `.tools/jdk-21.0.12.1+1.provenance.json` does not exist, because the install predates the script (`docs/REPRODUCING.md`).

**How NeuroSem finds it.** Java is not on `PATH` on this machine ([T4]). `simulators/jneuroml.py::find_java()` tries, in order: `NEUROSEM_JAVA`; `.tools/jdk-*/bin/java(.exe)`; `.tools/jdk-*/Contents/Home/bin/java` (macOS layout); `JAVA_HOME`; `PATH`.

**Why Java 21.** It is the newest LTS inside jNeuroML 0.14.0's CI matrix (Java 8-21). Temurin 25 is also LTS but was untested with this jar anywhere the M0 audit looked. A JRE is enough to run the jar ([E:env]).

**Other routes.**
- **Docker** installs the JRE of the same release with a SHA-256 pinned per architecture (`Dockerfile`): amd64 `2413149700df0f7d440500a84a8f764c535f21e5a5e87d38328b64eec2c5b500`, arm64 `14be1f35ebdbd1f6e8d57eb911a3ffb74d6d9aa255abc5daf2b1302002cf2cf2`. The Dockerfile says the API and the publisher's checksum files agreed on these values on 2026-09-13. The archives were not downloaded (`docs/REPRODUCING.md`).
- **CI** (`actions/setup-java@v6`, `java-version: "21"`) takes the newest Temurin 21 at run time, not this exact build (`.github/workflows/ci.yml`; `docs/REPRODUCING.md`).
- **Not executed:** the M0 proposals `winget install --id EclipseAdoptium.Temurin.21.JRE --exact --version 21.0.12.101` (machine-wide, needs admin) and the per-user JRE zip route ([E:env] W13, W13-alt).

**Pitfalls.**
- The Adoptium API answers HTTP 403 to Python urllib's default User-Agent. `bootstrap_java.py` sends its own (`docs/build_notes/infra.md`; script docstring).
- [C:NUM-07] (upheld, high): Java was the blocker for Milestone 1. The skeptic recommended a portable user-level runtime on Windows for pilot-scale work, plus a single Linux reference platform with a pinned JRE for frozen-study data. It also verified that Docker Desktop's documented WSL 2 backend requirements list Windows 11 Enterprise, Pro or Education, not Home; this machine is Windows 11 Home. Choosing the reference platform is Neel's decision.

**License.** The winget manifest lists "GPL-2.0 with Classpath Exception" ([E:env]). Details belong to `LICENSE_AUDIT.md`.

### 3.5 libNeuroML 0.6.7

**How NeuroSem uses it.**
- `validation/structural.py::libneuroml_strict` calls `neuroml.utils.validate_neuroml2` on the cell file. The result is recorded for information only (D-006).
- `transforms/units.py` takes the permitted unit strings from `NeuroML_v2.3.1.xsd`, which ships inside libNeuroML (module docstring; `transforms.md` §3).
- `tests/unit/test_units.py`, `test_generate_xml.py` and `test_transforms.py` import `neuroml` to locate that XSD and validate against it with lxml ([T6]).

**Verified pitfalls.**
- `validate_neuroml2` and `is_valid_neuroml2` are **not XSD validation**. They load the file with its includes and run generateDS object validation (pattern and required-attribute checks) ([E:nml] verify, correction). They do reject unit-pattern errors such as `1mA` for a current ([E:nml] verify).
- `is_valid_neuroml2` raises an exception on malformed XML instead of returning `False`, and is annotated `-> None` although it returns a bool ([E:pynml] verify). `libneuroml_strict` catches every exception and records "not strictly valid".
- Package metadata says `BSD-2-Clause` ([T2]) while the LICENSE text has three clauses ([E:nml]). This belongs to `LICENSE_AUDIT.md`.
- Classifiers stop at Python 3.13; `requires_python` is not declared ([T8]).
- A Windows Git checkout with `core.autocrlf=true` changes file bytes: the XSD becomes 186,517 bytes instead of 182,554 ([E:nml] verify). D-019 turns off line-ending conversion for `models/`, `results/raw/` and `data/splits/`.

**Its own requirements** (pip metadata): lxml, natsort, networkx, numpy, tables ([T2]).

### 3.6 PyLEMS 0.6.9 and neuromllite 0.6.1 (indirect)

- Both are installed only because pyNeuroML requires them ([T7]). No file in `src/`, `scripts/`, `workflows/` or `tests/` imports `lems` or `neuromllite` ([T6]).
- PyLEMS steps with explicit Euler (`x += dt*(expr)`) ([E:nml] verify). It is not a fallback for the pilot: `LEMS_LTS.xml` does not run in PyLEMS 0.6.9 (ZeroDivisionError on the first step) ([E:fix], finding D3).
- neuromllite brings h5py, tables and modelspec. modelspec in turn brings pymongo, cattrs, docstring_parser and tabulate ([T7]). These enlarge the lock file but add no code that NeuroSem calls.

**Why the lock has 75 entries.** NeuroSem's own dependencies are the nine in `pyproject.toml` plus the development tools (pytest, pytest-cov, ruff). Everything else is pulled in by them. For example, `pymongo` comes from modelspec, which comes from neuromllite, which comes from pyNeuroML ([T7]).

### 3.7 eFEL 5.7.34

**How NeuroSem uses it.**
- `features/efel_adapter.py` is the only extraction path (`extract`, `extract_all`, `efel_settings`, `effective_settings`).
- `configs/features.yaml` pins `efel_version: "5.7.34"`, and the adapter raises `FeatureConfigError` if the installed eFEL differs.
- `validation/execution.py` puts `efel.__version__` into the feature-cache key, so features cached under a different eFEL are not reused.
- Frozen settings (D-016; `configs/features.yaml`): `Threshold -20.0`, `DerivativeThreshold 10.0`, `DownDerivativeThreshold -12.0`, `interp_step 0.01` ms, `strict_stiminterval true`, `ignore_first_ISI false`, `strict_burst_factor 2.0`.
- Tests: `tests/unit/test_efel_adapter.py`, `tests/integration/test_features_real_trace.py` ([T6]).

**Verified pitfalls and how NeuroSem handles them.**

| Pitfall | Evidence | NeuroSem handling |
|---|---|---|
| **Settings are process-global** and stay until `efel.reset()`. `set_setting` silently accepts misspelt names (only a debug log line). | [E:efel], confirmed by verify | Names are checked against the fields of `efel.Settings`. Before every eFEL call the adapter runs `reset()` and re-applies all settings, under a module-level `RLock` (`_EFEL_LOCK`). Caveat: `warnings.catch_warnings` is also process-global, so warnings raised by other threads could land in a call's warning list (`features.md`, interpretation 8). |
| **Undefined features come back as `None`.** Count features return `array([0])` when there are no spikes. | [E:efel] | `None` becomes the state `undefined` and is never replaced by zero. Counts are real zeros. A third state, `not_applicable`, comes from `min_spikes` and `requires` rules (`docs/ARCHITECTURE.md` §3.1). |
| **Feature-variant ambiguity.** `steady_state_voltage` measures after the stimulus; `steady_state_voltage_stimend` measures during it. There are three `voltage_deflection` variants and two sag ratios. `burst_number` and `strict_burst_number` disagreed on the same spike train. `time_to_first_spike` is measured to the spike peak. `mean_frequency` gives a rate from a single spike. | [E:efel] | One frozen variant per concept (D-016; `configs/features.yaml`): `steady_state_voltage_stimend`, `voltage_deflection_vb_ssse`, `sag_ratio1` (hyperpolarising protocols only), `spike_count_stimint`, `mean_frequency` with `min_spikes: 2`, `adaptation_index2`, `strict_burst_number`. |
| Deprecated names: `Spikecount`; the chain `ISI_values` -> `ISIs` -> `all_ISI_values`; `set_threshold`, `set_int_setting` and similar functions. | [E:efel] verify | Only `set_setting`, `get_settings` and `reset` are used, and only non-deprecated feature names (`spike_count_stimint`, `all_ISI_values`). |
| The docs say `inv_first_ISI` and `inv_last_ISI` return 0 when there is no interval; the code returns `None`. | [E:efel] | Neither feature is configured. Behaviour is tested against the pinned version, not the docs. |
| eFEL resamples traces to `interp_step` (default 0.1 ms) before extracting, so time features are quantised to that step. | [E:efel]; [C:NUM-05] softened to low | `interp_step: 0.01` is frozen and recorded. The config comment asks for a sensitivity check. |
| `stim_start` and `stim_end` must be lists of exactly one element; longer lists raise an exception. | [E:efel] verify | One analysis window per protocol trace (`docs/ARCHITECTURE.md` §3.1). |
| **Wrong units fail silently:** a trace in seconds and volts gave 0 spikes and no error. | [E:efel] | `load_dat` converts SI output to ms and mV before extraction. |
| Window rules differ between features: `spike_count_stimint` includes the edges, `mean_frequency` counts strictly inside, `trace_check` allows peaks up to 1.05 x `stim_end`. | [E:efel] verify | Rebound features use a separate post-release window (`features.md`, interpretation 3). |
| `get_feature_names()` returns 182 entries but only 179 unique names. | [E:efel] verify; confirmed today ([T3]) | The adapter holds the names as a set (`frozenset`). |
| The message "4 or more spikes are needed for burst calculation" is printed to stdout by the C++ core, not raised as a Python warning. | [E:efel] verify | Not captured. Burst features are gated by `min_spikes: 4`. |
| `AHP_depth` is defined after a single spike. | D-021; `docs/build_notes/science-docs.md` §5 | `ahp_depth` has `min_spikes: 1`. |
| The `impedance` feature imports a deprecated scipy path. | [E:efel] verify | Not used. |
| No macOS x86_64 wheel exists for 5.7.34 (arm64 only). | [E:efel] verify; [T8] | Intel Macs would need a C++17 source build. macOS is not a verified NeuroSem target in any case (`docs/REPRODUCING.md`). |

**License.** PyPI metadata says `LGPLv3` ([T2]); `LICENSE.txt` grants version 3 "or any later version" ([E:efel]). Details belong to `LICENSE_AUDIT.md`.

### 3.8 numpy, scipy, pandas, lxml, PyYAML and matplotlib

| Library | Lock pin | Lower bound in `pyproject.toml` | Where NeuroSem imports it ([T6]) | Verified pitfalls |
|---|---|---|---|---|
| numpy | 2.5.3 | `>=2` | `schemas.py`, `simulators/jneuroml.py`, `features/*`, `protocols/rheobase.py`, `mutations/base.py`, `selection/*`, `analysis/*`, `experiments/{campaign,discovery,heldout,analyze}.py` | Random baselines are reproducible only for a fixed seed **and** the same NumPy version, because NumPy does not promise identical `Generator` streams across versions (`docs/build_notes/selection.md` §3, item 4). Needs Python 3.12 or newer ([T8]). |
| scipy | 1.18.1 | `>=1.12` | `analysis/metrics.py`, `analysis/bootstrap.py` (`scipy.stats`); also required by eFEL | Needs Python 3.12 or newer ([T8]). No other pitfall recorded. |
| pandas | 3.0.5 | `>=2.2` | `simulators/jneuroml.py` (`load_dat` uses `read_csv`), `analysis/metrics.py`, `analysis/figures.py`, `experiments/analyze.py` | None recorded. |
| lxml | 6.1.3 | `>=5` | `mutations/{base,biophysics,numerical}.py`, `transforms/{factoring,formatting,identifiers,units}.py`, `validation/canonical.py`, `experiments/agent.py` | Re-writing a file through lxml keeps its meaning but not its bytes: a no-op read and write changed bytes in 11 of 21 files. Audit mutants with `xml_changes` or `variant.json`, not `git diff` (`mutations.md` §4). Transforms instead use a byte-preserving scanner that is cross-checked against lxml (`transforms.md` §3). |
| PyYAML | 6.0.3 | `>=6` | `config.py`, `experiments/agent.py` | None recorded. |
| matplotlib | 3.11.2 | `>=3.8` | `analysis/figures.py` | Needs Python 3.11 or newer ([T8]). The Docker image sets `MPLBACKEND=Agg` for headless plotting (`Dockerfile`). |

These packages have compiled wheels that differ by operating system. Linux behaviour has not been checked by a real install (`requirements.lock` header).

### 3.9 Tooling pinned in the lock

- pip 26.2.1 is pinned in every route (venv, Docker, CI, Makefile, `environment.yml`).
- Development tools are pinned in `requirements.lock`: pytest 9.1.1, pytest-cov 7.1.0, coverage 7.16.0, ruff 0.16.7.
- The build backend (`setuptools>=69`, fetched by pip's build isolation for `pip install -e .`) is **not** pinned (`docs/REPRODUCING.md`, "Known limits").
- The editable install is required, not optional: `provenance.REPO_ROOT` is derived from the source location, which is where `configs/`, `data/` and `models/` live (`docs/build_notes/infra.md`).

---

## 4. Optional and related tools

None of these is installed in the project venv. `pip list` shows no OSBModelValidation, sciunit, neuronunit, NEURON or pyelectro ([T2]). In M0, OMV and SciUnit/NeuronUnit were installed only in throwaway venvs ([E:omv], [E:snu]).

| Tool | Latest seen 2026-09-13 (release date) | Python / OS | Maintenance | NeuroSem use |
|---|---|---|---|---|
| OMV (PyPI `OSBModelValidation`) | 0.4.0, 2026-06-05 ([E:omv], [T8]) | No `requires_python`; classifiers 3.9-3.13 ([T8]); CI on Linux and macOS only, no Windows runner ([E:omv] verify) | Active (latest scheduled CI run on master 2026-09-01, success) ([E:omv] verify) | None in code. Context and a possible secondary baseline (D-008, N-06). |
| SciUnit (`sciunit`) | 0.2.8, PyPI sdist 2024-01-03 ([E:snu], [T8]) | `>=3.7`; classifiers 3.7-3.9 ([T8]); CI 3.7-3.10 on Linux ([E:snu]) | Low activity; last master commit 2023-12-26 ([E:snu]) | None. Design concepts and prior art only. |
| NeuronUnit (`neuronunit`) | 0.1.8.2, 2016-07-04 ([E:snu], [T8]) | No `requires_python`, no classifiers ([T8]) | Dormant; default branch last commit 2021-04-22 ([E:snu]) | None. Prior art only. |
| NEURON (`NEURON`) | 9.0.2, 2026-08-10 ([T8]) | `>=3.10`; classifiers 3.10-3.14. PyPI wheels for 9.0.2: macOS x86_64, macOS arm64, manylinux x86_64, manylinux aarch64; **no Windows wheel on PyPI** ([T8]). Windows installers outside PyPI: unverified. | Not assessed beyond release date | Stub adapter only; not installed (N-08 deferred). |

### 4.1 OMV (Open Source Brain Model Validation)

**Role.** D-008 makes the canonical protocol the model's shipped LEMS harness, scored with the same NeuroSem features and tolerances as every other protocol. It is not an OMV spike-time check. N-06 leaves an OMV-style secondary check open. `docs/pilot/dt_probe.md` quotes the shipped OMV reference spike times as context only.

**Verified pitfalls** ([E:omv], with verify corrections):
- An OMV tolerance is one relative tolerance per observable, passed to `numpy.allclose` as `rtol` with `atol` 1e-8. A different spike count fails at any tolerance. An expected value of 0 gives an infinite relative error. The test is asymmetric. A missing `tolerance` key defaults to 0.1.
- OMV prints a "better tolerance" fitted to the current output. Using it would tune thresholds on outcomes, so NeuroSem must not use it.
- On Windows, any OMV command (even `omv --version`) crashes with `KeyError: 'HOME'` when `HOME` is unset. Engines start bare executables (for example `pylems`), which must be on `PATH`. The pass mark needs UTF-8 output.
- Missing engines are installed automatically with a bare `pip` or a git clone into home directories. The M0 run cloned NeuroML2 into `C:/Users/gurra/NeuroML2`. Any future use should pre-install pinned engines and treat an auto-install as a failure.
- `--engine=NAME:VERSION` pinning is not reliable: for jNeuroML the version is dropped (verify correction).
- `validate-mep` is broken in both the 0.4.0 wheel and sdist, and exits 0 even for an invalid file. `validate-omt` is not implemented.
- The output-freshness (modification time) check covers only the spike-times, spike-rate and timeseries analyzers (verify correction).
- The required dependency `pyrx` 0.3.0 declares GPLv2 and has been unmaintained since 2013 (verify). This belongs to `LICENSE_AUDIT.md`.
- The README's install name `osb-model-validation` is not registered on PyPI; the real name is `OSBModelValidation` (verify).

**Critique points that apply.**
- [C:INTEG-08] (upheld, high): to check NeuroSem's detection decisions independently, Neel should hand-check a random sample against the evidence trace and recorded tolerance, rather than relying on OMV's `compare_arrays`.
- [C:SWT-12] (softened to medium): the canonical protocol and the battery should share the NeuroSem comparator; an OMV-style check is optional secondary context.
- [C:NEURO-10] (upheld, high): the Pospischil `.mep` spike-time files sit in `NEURON_MODIFIED`, which the repository's MIT license excludes. Do not copy them into NeuroSem.

### 4.2 SciUnit and NeuronUnit

- **sciunit 0.2.8** installs on Python 3.12 in a short path, and basic scoring works. But `TestSuite` without an explicit name raises `TypeError` on 3.12 (`random.randint(0, 1e12)`; upstream issue #218) ([E:snu] verify). It pulls a heavy Jupyter dependency tree. On Windows, deep venv paths broke installs of debugpy, jedi and lxml because of the path-length limit. Importing sciunit writes `~/.sciunit/config.json` ([E:snu] verify). A packaging modernisation pull request (#226) is open and unmerged ([E:snu]).
- **neuronunit 0.1.8.2** (PyPI, 2016): `neuronunit.models` fails to import without the undeclared dependency pyneuroml. The GitHub `dev` branch has merge-conflict markers in 12 files. The `prime` branch (2021-07-18) imports on 3.12 but is unreleased, pins old packages, and the repository has no LICENSE file ([E:snu] verify).
- **Decision in the evidence.** Neither is a NeuroSem dependency. NeuroSem borrows concepts only (separating capabilities, tests and scores; explicit "incomplete" scores). NeuronUnit's rheobase binary search and feature tests are prior art to record in the novelty matrix ([E:snu]).

### 4.3 NEURON

- **NeuroSem code.** `src/neuraxis/simulators/neuron.py` defines `NeuronSimulator`. `available()` tries `import neuron`. `run_lems` returns `RunStatus.TOOL_FAILURE` with "not implemented in the pilot". NEURON is not installed ([T2]). N-08 is deferred.
- **Route if enabled.** `jnml <LEMS file> -neuron -run` through the same jar, which needs both NEURON and Java ([E:pynml]); pyNeuroML offers the extra `[neuron]` ([E:pynml] verify).
- **Pitfall** ([C:NUM-10], upheld, medium). org.neuroml.export's NEURON writer emits fixed-step NEURON unless a `Meta` element requests CVODE. NEURON's default fixed step is first-order implicit (Crank-Nicolson only with `secondorder=2`), while jLEMS is explicit Euler. Tolerances calibrated on jLEMS therefore cannot be reused for NEURON. Recommendation: calibrate NEURON tolerances from NEURON's own refinement, record `secondorder`, CVODE and `nseg`, and run NEURON only on Linux. This matches the PyPI finding above that 9.0.2 has no Windows wheel.

---

## 5. What NeuroSem reuses versus what NeuroSem builds

Left column: existing tools or established methods that NeuroSem uses and does not claim as new. Right column: code written for NeuroSem.

"Built in NeuroSem" is **not** a novelty claim. Novelty is judged only by the prior-art audit (`PRIOR_ART_AUDIT.md`, `docs/novelty_matrix.csv`). The specification's candidate contribution is the combination: mutation-calibrated perturbation fingerprints plus compact stimulation-battery selection, evaluated on held-out models (`NEUROSEM_FINAL_SPEC.extracted.md`, "Novelty boundary"). The specification also lists as already established: NeuroML syntax validation, unit and reference checks, running NeuroML models, saved-trace comparison, running tests in GitHub Actions, feature extraction, multi-protocol characterisation, metamorphic testing of simulations, mutation testing, and generic test-suite minimisation.

| Reused (existing; not claimed as new) | Built in NeuroSem (new code for this project) |
|---|---|
| NeuroML v2.3.1 schema and LEMS simulation files to describe models and runs; core inputs `pulseGenerator`, `rampGenerator`, `compoundInput` ([E:nml]) | Protocol templates and a generator that writes probe networks and LEMS files, with stimulus edges on whole milliseconds so every refinement grid lands on them, in XSD element order (`protocols/definitions.py`, `protocols/generate.py`) |
| `jnml -validate` (schema plus jNeuroML's model tests); libNeuroML generateDS validation ([E:pynml], [E:nml]) | Relative structural oracle over the whole include closure, per-file error parsing, baseline errors and a warnings policy (`validation/structural.py`; D-006, D-020, D-021) |
| jLEMS simulation inside the jNeuroML jar; the Temurin Java runtime | A direct-jar adapter with a status taxonomy (ok, invalid, build error, runtime error, timeout, numerically unstable, tool failure), time-label regularisation and SI-to-ms/mV loading (`simulators/jneuroml.py`; D-005, D-020); batched uncoupled probe populations (D-011); cost counted as simulated cell-steps (D-015) |
| The idea of a rheobase search: NeuronUnit's `RheobaseTest` (binary search) and pyNeuroML's f-I helper (lowest spiking amplitude) exist as prior art ([E:snu], [E:pynml]) | NeuroSem's own grid-refinement rheobase search, rheobase-normalised amplitudes, retry rule and stored spike counts (`protocols/rheobase.py`; D-010, D-012, D-021) |
| eFEL feature algorithms and their documented definitions ([E:efel]) | The eFEL adapter: one frozen variant per concept, settings isolation, three feature states (defined, undefined, not applicable), per-spike aggregation and applicability rules; the firing-regime label; trace alignment and trace metrics (`features/*`; D-016) |
| Saved-output regression with a tolerance, as done by OMV for spike times, rates and timeseries ([E:omv]) | Tolerance calibration per model, protocol and feature from runs at h, h/2 and h/4 with absolute, relative and refinement terms; detections must reproduce at h and h/2; features whose state changes under refinement are excluded (`validation/convergence.py`, `validation/fingerprint.py`; D-013, D-014) |
| Mutation testing as a general method | Single-fault operators for NeuroML/LEMS (stimulus, biophysical, reference, numerical), one-change enforcement, and the six-way classification (`mutations/*`, `validation/fingerprint.py`; D-009) |
| Metamorphic testing of simulations as a general method | Valid-transformation generators: unit conversion limited to XSD-permitted unit strings, formatting, identifier renames, file factoring, reordering, explicit defaults (`transforms/*`) |
| SciUnit concepts: capabilities, `ProtocolToFeaturesTest`, `TestM2M` model-to-model scoring ([E:snu]) | Perturbation fingerprints and a mutant-by-protocol detection matrix, where every detection names its protocol, feature, tolerance and evidence run ids (`validation/fingerprint.py`, `selection/matrix.py`) |
| Greedy set cover and test-suite minimisation as general methods | Greedy battery selection on the discovery matrix with deterministic tie-breaks, count- and cost-matched random baselines, hashed split files and a held-out access gate (`selection/*`; `docs/ARCHITECTURE.md` §3.7) |
| Standard statistics (`scipy.stats`; bootstrap and exact binomial tests as methods) | Base-model-clustered bootstrap, exact McNemar and cluster permutation code for this design (`analysis/bootstrap.py`, `analysis/metrics.py`) |
| GitHub Actions, Docker, `pip freeze`, the Adoptium API and published checksums | Content-addressed, write-once run records that include the jar hash, Java version and an environment digest (`provenance.py`, `validation/execution.py`; D-012); a SHA-checked Java bootstrap (`scripts/bootstrap_java.py`) |

---

## 6. Environment setup commands

### 6.1 Status labels

| Label | Meaning |
|---|---|
| **Executed here** | Run on this Windows 11 machine for the NeuroSem repository. The source is named. |
| **Executed in M0 scratch** | Run on this machine during Milestone 0 in a throwaway venv (`tested_ok` in [E:env]), not in the repository. |
| **Dry run only** | Metadata checked; nothing installed. |
| **Not executed** | Written down; never run. |

### 6.2 Windows 11 (this machine)

| Step | Command | Status |
|---|---|---|
| 1. Check interpreters | `py -0p` and `py -3.12 --version` | Executed here today: lists 3.14 (default) and 3.12 ([T5]). Also M0 step W0 ([E:env]). |
| 2. Create the venv | `py -3.12 -m venv .venv` | Executed in M0 scratch (W1). The repository's fresh-install check was run from Git Bash with `python -m venv` (`docs/REPRODUCING.md`); `python` there is 3.12.10 ([T5]). The exact command that created the current `.venv` was not recorded: unverified. |
| 3. Pin pip | `.\.venv\Scripts\python -m pip install pip==26.2.1` | Executed in M0 scratch (W2). `.venv` has pip 26.2.1 today ([T1]). |
| 4. Install the lock | `.\.venv\Scripts\python -m pip install -r requirements.lock` | Executed here in a fresh venv (`docs/REPRODUCING.md`, verification table). |
| 5. Install NeuroSem | `.\.venv\Scripts\python -m pip install --no-deps -e .` | Executed here (`docs/REPRODUCING.md`). `pip list` shows `neurosem 0.1.0.dev0` installed from the repository ([T2]). |
| 6. Check consistency | `.\.venv\Scripts\python -m pip check` | Executed here today: "No broken requirements found." ([T2]) |
| 7. Compare with the lock | one-liner in section 7.2 | Executed here today: `installed but not in lock: []`, 75 pins, exit 0 ([T7]). |
| 8. Java runtime, exact build | `.\.venv\Scripts\python scripts\bootstrap_java.py --release jdk-21.0.12.1+1 --expect-sha256 f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e` | Dry run only (today [T11], and `docs/REPRODUCING.md`). The full download was not re-run on Windows. The existing `.tools/jdk-21.0.12.1+1` came from the same archive during M0, hash-checked against the API (D-004); the commands used then were not recorded: unverified. |
| 9. Java and jar health check | `.\.venv\Scripts\python -c "from neurosem.simulators.jneuroml import JNeuroML; print(JNeuroML().version_info())"` | Executed here today ([T4]). |
| 10. Tests | `.\.venv\Scripts\python -m pytest -q -m "not jnml"` then `.\.venv\Scripts\python -m pytest -q` | The full suite was run before commit `3cdb957` (`AI_USE_LOG.md`, Entry 002; counts are not recorded there). Not re-run for this document. |

The same sequence as one PowerShell block (from `docs/REPRODUCING.md`):

```powershell
cd C:\Users\gurra\NeuroSem
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install pip==26.2.1
.\.venv\Scripts\python -m pip install -r requirements.lock
.\.venv\Scripts\python -m pip install --no-deps -e .
.\.venv\Scripts\python -m pip check
.\.venv\Scripts\python scripts\bootstrap_java.py --dry-run
.\.venv\Scripts\python scripts\bootstrap_java.py --release jdk-21.0.12.1+1 --expect-sha256 f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e
.\.venv\Scripts\python -m pytest -q -m "not jnml"
.\.venv\Scripts\python -m pytest -q
```

Git Bash uses the same commands with forward slashes (`.venv/Scripts/python ...`).

**Not used on this machine.** `winget install --id EclipseAdoptium.Temurin.21.JRE ...` (not executed; needs admin; [E:env] W13). `make ...` (GNU make is not installed; [T5]). `conda env create -f environment.yml` (conda is not installed; [T5]). `docker ...` (Docker is not installed; [T5]).

**Windows notes.**
- The `py` launcher default here is 3.14. Always pass `-3.12`.
- jnml is called with at most 100 files at a time (command-line length limit; `transforms.md` §4).
- The NeuroSem stack installed without path-length errors in a venv path of about 150 characters ([E:env] W3). sciunit's dependencies did fail in deeper paths ([E:snu] verify). Keep the repository path short, or enable Windows long paths.
- `pip freeze > file` from Git Bash writes CRLF line endings, while `requirements.lock` has LF ([T7]). See section 7.3.

### 6.3 Linux (Debian or Ubuntu, x86_64): not executed

No NeuroSem install has been run on Linux. The lock was checked on paper only by the infra builder (`requirements.lock` header): every pin has a manylinux x86_64 or pure-Python wheel; a `pip install --dry-run --only-binary=:all: --platform manylinux_2_28_x86_64 ...` resolution gave the same 75 pins; no Linux-only dependency marker is missing. Those checks were not repeated for this document.

Interpreter availability (`docs/build_notes/infra.md`; `docs/REPRODUCING.md`, checked there on 2026-09-13): Ubuntu 24.04 ships Python 3.12.3 as `python3`. Debian 13 ships 3.13 and Debian 12 ships 3.11, so neither works as is; use a separately installed 3.12 or the Docker image.

```bash
# NOT EXECUTED (from docs/REPRODUCING.md)
cd /path/to/NeuroSem
python3.12 -m venv .venv
.venv/bin/python -c "import sys; assert sys.version_info[:2] == (3, 12), sys.version"
.venv/bin/python -m pip install pip==26.2.1
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps -e .
.venv/bin/python -m pip check
.venv/bin/python scripts/bootstrap_java.py --dry-run
.venv/bin/python scripts/bootstrap_java.py
.venv/bin/python -m pytest -q -m "not jnml"
.venv/bin/python -m pytest -q
```

With GNU make: `make setup java test` (never executed anywhere).

### 6.4 Docker: never built

```bash
# NOT EXECUTED: Docker is not installed on the authoring machine ([T5]).
docker build --build-arg GIT_COMMIT="$(git rev-parse HEAD)" -t neurosem:dev .
docker run --rm neurosem:dev                                   # full pytest suite
docker run --rm neurosem:dev python -m pytest -q -m "not jnml"
docker image inspect --format '{{.Id}}' neurosem:dev           # record with any results
```

What the `Dockerfile` specifies:
- Base image `python:3.12.14-slim-trixie@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea` (Python 3.12.14, Debian trixie; resolved from Docker Hub on 2026-09-13 according to the file).
- Temurin JRE `jdk-21.0.12.1+1`, installed by `scripts/bootstrap_java.py` into `/opt/java`, with the per-architecture SHA-256 pins in section 3.4.
- pip 26.2.1, then `requirements.lock`, then an editable install, with a build-time check that every lock pin is installed and `pip check` passes.
- A non-root user `neurosem` (uid 10001), and a build-time check that `JNeuroML().available()` finds Java and the jar.
- The `.dockerignore` build context was emulated on Windows, but no image was built (`docs/REPRODUCING.md`).

**Provenance inside the container.** At HEAD `d323afa`, `provenance.git_state()` falls back to the `NEUROSEM_GIT_COMMIT` environment variable when git is unavailable, and then reports `dirty=True` (source read today). The Dockerfile sets that variable from the `GIT_COMMIT` build argument. The `PROVENANCE:` comment in the `Dockerfile` and the "Provenance in containers" note in `docs/REPRODUCING.md` describe this fallback correctly; neither still claims that core code ignores the variable. The fallback has never run in a container, because no image was built. A container run can record the build commit but can never show a clean tree.

**Critique points.**
- [C:NUM-07] (upheld, high): do not make Docker a go/no-go condition on this Windows 11 Home machine (see section 3.4).
- [C:INTEG-10] (softened to medium): a published image would redistribute the LGPL jNeuroML jar and its bundled libraries. Either publish only the Dockerfile with pinned versions and the jar hash, or meet the source-availability duties. This is folded into N-05 and `LICENSE_AUDIT.md`.

### 6.5 Continuous integration: never run

`.github/workflows/ci.yml` has never run, because the repository has no GitHub remote (N-01). It defines two jobs on `ubuntu-latest`:
- `tests`: `actions/checkout@v7`, `actions/setup-python@v7` with Python "3.12", `actions/setup-java@v6` with Temurin "21" (the newest build at run time), install from the lock, lock comparison, environment record (`python -VV`, `java -version`, `JNeuroML().version_string()`), `make -n` on all targets, `bootstrap_java.py --dry-run`, then `pytest -q`.
- `docker`: builds the image with `GIT_COMMIT=${{ github.sha }}` and runs the test suite inside it.

### 6.6 Make and conda: not executed

- `Makefile`: never executed, because GNU make is not installed ([T5]). CI runs `make -n` only.
- `environment.yml`: not tested, because conda is not installed ([T5]). It supplies only Python 3.12 and pip 26.2.1 from conda-forge; all packages come from `requirements.lock`. Unlike the other routes, conda resolves `-e .` together with the lock, so the lock comparison in section 7.2 must be run after creating the environment (`environment.yml` header).

---

## 7. Reproducibility: frozen dependencies

### 7.1 What is frozen, and where it is recorded

- **`requirements.lock`** holds 75 exact `name==version` pins. It was generated on 2026-09-13 with `.venv/Scripts/python -m pip freeze --exclude-editable` on Windows 11 x86_64, CPython 3.12.10, pip 26.2.1 (file header). Its SHA-256 today is `f0bad21229537aaa2a17245048c9d6ffd88afded46b1ba76d8e67646adcc166e` ([T12]). It did not change between `3cdb957` and `d323afa` ([T13]).
- **`pyproject.toml`** declares the nine direct dependencies (three exact pins, six lower bounds) and `requires-python >=3.12,<3.13`.
- **Every run.** `provenance.python_environment()` records every installed distribution and version, the Python version and the platform. `provenance.environment_digest()` adds simulator facts (Java version, jar hash) and, when set, `NEUROSEM_CONTAINER_IMAGE`. Each `run_id` hashes the jar SHA-256 among its inputs (`docs/ARCHITECTURE.md` §2; D-012).
- **Dirty flag.** At HEAD `d323afa`, a run is marked dirty when any of `src`, `configs`, `data`, `models`, `scripts`, `workflows`, `pyproject.toml` or `requirements.lock` differs from the commit (`provenance.PROVENANCE_PATHS`). The code is committed in `d323afa`, the commit the pilot runs on. The D-023 entry describing it was still uncommitted in the working copy of `DECISIONS.md` when this document was fact-checked (2026-09-13).
- **eFEL guard.** `configs/features.yaml` pins `efel_version: "5.7.34"` and the adapter refuses any other installed version (section 3.7).

### 7.2 Check that an environment matches the lock

Executed here today ([T7]). The same check runs in the Dockerfile and in CI.

```bash
.venv/Scripts/python -c "import subprocess, sys; lock = {l.strip() for l in open('requirements.lock') if l.strip() and not l.startswith('#')}; frz = set(subprocess.run([sys.executable, '-m', 'pip', 'freeze', '--exclude-editable'], capture_output=True, text=True, check=True).stdout.split()); print('installed but not in lock:', sorted(frz - lock)); missing = sorted(lock - frz); sys.exit('lock pins not installed: %s' % missing if missing else 0)"
# today: installed but not in lock: []   (exit 0)
```

Then check the Java side:

```bash
.venv/Scripts/python -c "from neurosem.simulators.jneuroml import JNeuroML; print(JNeuroML().version_info())"
# today: jneuroml_version 0.14.0, jlems_version 0.12.0, org_neuroml_export_version 1.11.0,
#        jar_sha256 45ee565a65a66008a3b41935358d11b7c19cb6b5a67bbec22481d519f53db931,
#        java_version openjdk version "21.0.12.1" 2026-08-18 LTS ...
```

### 7.3 Regenerate the lock (only as a deliberate, logged change)

This procedure was **not executed** for this document. Its freeze command is the one recorded in the lock header, and its comparison step uses the check from section 7.2, which was executed.

```bash
# 1. Fresh CPython 3.12 venv (Windows: py -3.12 -m venv .venv-new)
python3.12 -m venv .venv-new
.venv-new/bin/python -m pip install pip==26.2.1
# 2. Install the intended set: either the current lock with one pin edited on purpose ...
.venv-new/bin/python -m pip install -r requirements.lock
.venv-new/bin/python -m pip install --no-deps -e .
#    ... or a fresh resolution within pyproject.toml ranges (this can move many packages)
# .venv-new/bin/python -m pip install -e ".[dev]"
# 3. Freeze without the editable neurosem line
.venv-new/bin/python -m pip freeze --exclude-editable > requirements.lock.new
# 4. Compare with the current lock, ignoring the comment header and Windows CR characters
diff <(grep -v '^#' requirements.lock) <(tr -d '\r' < requirements.lock.new)
```

Then copy the comment header into the new file and update its date, platform, pip version and Linux status. Re-run `pip check`, the section 7.2 checks and `pytest -q`. Record the change and the new file hash in `DECISIONS.md`.

**Observed trap.** A plain `diff` between `requirements.lock` and a `pip freeze` file written from Git Bash reported every line as different. The cause was CRLF versus LF line endings (`file` output, [T7]); the package sets were identical. Compare as sets, as in section 7.2, or strip `\r` first.

### 7.4 Limits

- **No file hashes.** `pip freeze` records versions, not wheel hashes. In M0 a hashed, platform-independent lock was tested in scratch: `uv pip compile requirements.in --universal --python-version 3.12 --generate-hashes`, installed with `pip install --require-hashes --no-deps` (73 packages, 1393 hashes) ([E:env] W11-W12). The repository adopted plain `pip freeze` instead (`docs/REPRODUCING.md`, "Known limits"). Adopting a hashed lock is open for Neel.
- The build backend (`setuptools`) is not pinned.
- The CPython patch version differs by route (3.12.10, 3.12.14, whatever CI gets). CI's Java is the newest Temurin 21; only Docker pins the exact JRE build.
- The lock has not been installed on Linux. Compiled wheels (numpy, scipy, pandas, lxml, efel, h5py, tables, matplotlib and others) differ between operating systems.
- NumPy random streams are reproducible only within one NumPy version (`selection.md`).
- jLEMS floating-point results may differ in the last bits across JVM builds and CPUs ([C:NUM-08]). Compare within tolerances across platforms; expect bitwise equality only on the same JRE and host class.
- Container runs record the build commit but always `dirty=True` (section 6.4).
- The conda route resolves `-e .` together with the lock (section 6.6).
- Checking upstream drift (for example re-resolving the lock later) is informational only. Never update the lock automatically during the frozen study ([E:env], step L11).
- Passing checks show that these particular checks passed. They do not prove that two environments are equivalent (`docs/REPRODUCING.md`).

---

## 8. Open dependency questions for Neel

These are decisions, not facts. Existing decision ids are given where they exist.

1. **Reference platform for frozen-study data** ([C:NUM-07]): WSL 2 Ubuntu, Docker, GitHub Linux runners, or another Linux machine. Windows stays the development platform.
2. **Hashed lock file** (section 7.4): keep plain `pip freeze`, or adopt a hashed universal lock (uv or pip-tools).
3. **Exact Java build in CI** (section 3.4): pin the Temurin build in `actions/setup-java`, or accept Docker as the only exact-JRE route.
4. **Python 3.14 as a secondary CI job** ([E:env], `decision_required`).
5. **NEURON as a cross-simulator** (N-08). If yes, Linux only, with its own tolerance calibration ([C:NUM-10]).
6. **OMV-style secondary canonical check** (N-06), with pre-installed pinned engines and no use of OMV's "better tolerance" hint.
7. **Report the jNeuroML validator gap** for `channelDensityVShift` upstream (N-11).
8. **Container image publication** versus LGPL obligations for the bundled jar ([C:INTEG-10]; N-05).

---

## Appendix A. Commands run for this document (2026-09-13)

All were run on Windows 11 Home 10.0.22631 from Git Bash, in `C:/Users/gurra/NeuroSem`. Scratch outputs are under `work/tmp/m0docs/dependency_audit/`.

| Key | Command(s) |
|---|---|
| T1 | `.venv/Scripts/python -VV`; `.venv/Scripts/python -m pip --version` |
| T2 | `.venv/Scripts/python -m pip show pyNeuroML libNeuroML PyLEMS neuromllite efel numpy scipy pandas lxml PyYAML matplotlib`; `.venv/Scripts/python -m pip check`; `.venv/Scripts/python -m pip list \| grep -iE 'omv\|osbmodel\|sciunit\|neuronunit\|^neuron \|pyelectro\|neurosem'` |
| T3 | Python script printing `importlib.metadata.version()` and `__version__` for pyNeuroML, libNeuroML, PyLEMS, neuromllite, efel, numpy, scipy, pandas, lxml, PyYAML, matplotlib and neurosem; `pyneuroml.JNEUROML_VERSION`; the jar's size and SHA-256 via `get_path_to_jnml_jar()` and `hashlib`; `len(efel.get_feature_names())` and the count of unique names; `neuroml.current_neuroml_version` |
| T4 | `.venv/Scripts/python -c "from neurosem.simulators.jneuroml import JNeuroML; s=JNeuroML(); print(s.java); print(s.jar); print(s.version_info())"`; `.tools/jdk-21.0.12.1+1/bin/java -version`; `which java`; a Python `zipfile` scan of `META-INF/maven/**/pom.properties` inside the jar |
| T5 | `py -0p`; `python --version`; `command -v make`, `command -v docker`, `command -v conda` |
| T6 | ripgrep over `src/`, `scripts/`, `workflows/` and `tests/` for `import`/`from` of efel, pyneuroml, neuroml, lems, neuromllite, numpy, scipy, pandas, lxml, yaml, matplotlib, omv, sciunit, neuronunit and neuron; ripgrep over `src/` for `NeuroML_v2.3.1.xsd`, `efel.__version__` and `get_path_to_jnml_jar` |
| T7 | The section 7.2 lock comparison one-liner; `.venv/Scripts/python -m pip freeze --exclude-editable > work/tmp/m0docs/dependency_audit/freeze_now.txt`; `file requirements.lock work/tmp/m0docs/dependency_audit/freeze_now.txt`; a Python script mapping each lock pin to the installed packages that require it (`importlib.metadata.distributions()` and `.requires`) |
| T8 | `curl -s https://pypi.org/pypi/<name>/json` for pyNeuroML, libNeuroML, PyLEMS, neuromllite, efel, numpy, scipy, pandas, lxml, PyYAML, matplotlib, OSBModelValidation, sciunit, neuronunit, NEURON and pip (latest version, earliest upload time of its files, `requires_python`, classifiers, wheel tags); `curl -s -A "neurosem-audit/0.1" "https://api.adoptium.net/v3/assets/latest/21/hotspot?os=windows&architecture=x64&image_type=jdk"` |
| T9 | `curl -s https://peps.python.org/api/release-cycle.json` (3.12: status security, first release 2023-10-02, end of life 2028-10); `curl -s "https://www.python.org/api/v2/downloads/release/?is_published=true"` (newest 3.12.x: Python 3.12.14, 2026-08-12) |
| T10 | `cat .tools/jdk-21.0.12.1+1/release` |
| T11 | `.venv/Scripts/python scripts/bootstrap_java.py --dry-run --release jdk-21.0.12.1+1 --expect-sha256 f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e` (exit 0) |
| T12 | `sha256sum requirements.lock` |
| T13 | `git log -1`; `git status --short`; `git diff --stat 3cdb957 HEAD`; `git diff --quiet 3cdb957 HEAD -- requirements.lock pyproject.toml`; `git show HEAD:src/neuraxis/provenance.py \| grep -n ...`; `git show HEAD:src/neuraxis/simulators/jneuroml.py \| grep -n ...`; `git diff DECISIONS.md` (all read-only) |

## Appendix B. Sources

**Milestone 0 evidence:** `docs/m0_evidence/tools/{pyneuroml-jneuroml,neuroml-lems,efel,omv,sciunit-neuronunit}.{research,verify}.json`; `docs/m0_evidence/environment/setup_commands.json`; `docs/m0_evidence/fixtures/fixture_verify.json`; `docs/m0_evidence/critique/{NUM,SWT,INTEG,STATS,NEURO}.json` with the matching `.skeptic.json` verdicts (NUM-01, NUM-05, NUM-07, NUM-08, NUM-10, NUM-11, SWT-04, SWT-12, STATS-10, INTEG-08, INTEG-10, NEURO-10).

**Repository files:** `DECISIONS.md` (D-004 to D-023, N-01 to N-12), `docs/ARCHITECTURE.md`, `docs/REPRODUCING.md`, `docs/build_notes/{core,features,infra,mutations,transforms,selection,science-docs,model-curation}.md`, `docs/pilot/dt_probe.md`, `AI_USE_LOG.md`, `requirements.lock`, `pyproject.toml`, `Dockerfile`, `Makefile`, `environment.yml`, `.github/workflows/ci.yml`, `.tools/jdk_provenance.json`, `.tools/jdk-21.0.12.1+1/release`, `configs/features.yaml`, `configs/study.yaml`, `scripts/bootstrap_java.py`, `src/neuraxis/simulators/{jneuroml,neuron}.py`, `src/neuraxis/features/efel_adapter.py`, `src/neuraxis/validation/structural.py`, `src/neuraxis/provenance.py`, `docs/handoff/NEUROSEM_FINAL_SPEC.extracted.md`, `docs/handoff/NEUROSEM_CLAUDE_HANDOFF.extracted.md`.

**Primary-source URLs retrieved on 2026-09-13 for this document:** `https://pypi.org/pypi/<package>/json` for the 16 packages listed under T8; `https://api.adoptium.net/v3/assets/latest/21/hotspot?os=windows&architecture=x64&image_type=jdk`; `https://api.adoptium.net/v3/assets/release_name/eclipse/jdk-21.0.12.1%2B1?os=windows&architecture=x64&image_type=jdk&jvm_impl=hotspot&heap_size=normal` (queried by `bootstrap_java.py --dry-run`); `https://peps.python.org/api/release-cycle.json`; `https://www.python.org/api/v2/downloads/release/?is_published=true`. All other URLs are cited through the evidence files, which record their own retrieval.

**Re-opened during the fact-check (2026-09-13, HTTP 200 unless noted):** the PyPI JSON for all 16 T8 packages plus pyelectro; the two Adoptium queries above plus `?os=linux&image_type=jre` (x64 and aarch64 checksums equal the Dockerfile pins); `https://peps.python.org/api/release-cycle.json`; `https://www.python.org/api/v2/downloads/release/?is_published=true`; the Temurin Windows JDK archive link in section 3.4; `https://github.com/openbraininstitute/eFEL`; `https://github.com/BlueBrain/eFEL` (GitHub API: archived); `https://github.com/NeuroML/jNeuroML/releases/tag/v0.14.0` (published 2025-02-12); `https://github.com/LEMS/jLEMS/releases/tag/v0.11.1` (newest jLEMS release, 2024-08-20); `https://github.com/NeuroML/pyNeuroML`; `https://raw.githubusercontent.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2.3.1.xsd`; `https://github.com/scidash/sciunit/issues/218`; `https://github.com/scidash/sciunit/pull/226`; `https://pypi.org/pypi/osb-model-validation/json` (404, confirming that name is not registered).
