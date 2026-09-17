# Build note: infra (reproducibility files)

Owner: infra module (Dockerfile, .dockerignore, environment.yml, Makefile, .github/workflows/ci.yml,
requirements.lock, scripts/bootstrap_java.py, CITATION.cff, docs/REPRODUCING.md). Written 2026-09-13.
Everything below is a request or observation for other owners; no core file was edited.

## Requested core changes

1. **`neurosem.simulators.jneuroml.find_java` misses macOS Temurin layouts.**
   It globs `.tools/jdk-*/bin/java`. Temurin macOS archives unpack to
   `jdk-<release>/Contents/Home/bin/java` (checked on 2026-09-13 by reading the first tar headers of
   `OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.12.1_1.tar.gz`). Suggested fix: also glob
   `jdk-*/Contents/Home/bin/java`. Workaround in place: `scripts/bootstrap_java.py` prints
   `hint set NEUROSEM_JAVA=...` whenever the runtime is nested or installed outside `.tools/`.

2. **Git commit inside Docker (blocks spec-compliant container runs).** `provenance.git_state()` shells
   out to `git`, and the image has neither `git` nor `.git` (excluded by `.dockerignore` to keep the context
   small and machine-independent), so runs inside the container record `commit="unknown", dirty=True`.
   Reproduced on 2026-09-13 in an emulated build context (repository copied with the `.dockerignore`
   rules, git discovery blocked with `GIT_CEILING_DIRECTORIES`): `git_state()` returned `('unknown', True)`.
   The spec's data requirements need the Git commit for every simulation, so container runs are not
   usable as study results until this is fixed; the Dockerfile and REPRODUCING.md say so. The Dockerfile
   already sets `ENV NEUROSEM_GIT_COMMIT=<build-arg GIT_COMMIT>` (CI passes `github.sha`). Suggested fix:
   fall back to `os.environ["NEUROSEM_GIT_COMMIT"]` when `git` fails, and record that the commit came
   from the build argument (the tree cannot be checked for dirtiness in that case).

3. **"Container/environment digest" (spec, Data requirements).** `provenance.environment_digest()` hashes
   the Python package list and simulator facts but has no notion of the container image. An image cannot
   know its own digest at build time; suggested approach: accept an optional `NEUROSEM_CONTAINER_IMAGE`
   environment variable (set with `docker run -e NEUROSEM_CONTAINER_IMAGE=<repo@sha256:...>`) and include
   it in the digest input when present.

## Observations (no action required from infra)

- `pyproject.toml` says exact pins are in `requirements.lock` "(see docs/DEPENDENCY_AUDIT.md)"; that file does
  not exist in the repository at the time of writing.
- The editable install is required, not just convenient: `provenance.REPO_ROOT` is
  `Path(__file__).parents[2]`, which only points at the repository when the package is imported from
  `src/`. A regular (non-editable) install would make `configs/`, `data/` and `models/` unreachable. The
  Dockerfile, CI, Makefile and REPRODUCING.md all use `pip install --no-deps -e .` for this reason.
- The assignment's file list did not include tests. Tests were added as
  `tests/unit/test_infra_bootstrap_java.py` and `tests/unit/test_infra_repro_files.py` (unique basenames).
- The Adoptium API answers HTTP 403 to urllib's default User-Agent (verified 2026-09-13); anything else
  in the project that calls it from Python must send its own User-Agent.

## Review response (2026-09-13)

- **`.dockerignore` excluded `.github`** (high): removed. `test_dockerignore_excludes_local_state_but_keeps_test_inputs`
  now implements the `.dockerignore` matching rules and fails if any repository file a test reads is
  excluded. The build context was emulated by copying the repository with those rules into
  `work/tmp/infra/ctx`, and the full suite was run there (results in docs/REPRODUCING.md).
- **Unchecked runtime left in `.tools/` after a failed `java -version`** (low): `safe_extract` now takes a
  `verify` callback that runs on the extracted directory while it is still in the private temporary
  directory; the move into `dest` happens only after it passes. New tests cover the unit behaviour and
  the end-to-end failure (stub `java` that cannot run; no `jdk-*` directory and no provenance remain).
- **Outdated "CLI does not exist" wording** (low): fixed in the Makefile and REPRODUCING.md. `--help` for
  `validate-models`, `pilot` and `reproduce-paper` was checked, and `neurosem validate-models --models
  pospischil2008_rs` ran successfully in the emulated context. `reproduce-paper` also takes `--campaign`,
  so the Makefile now passes `$(CAMPAIGN)` to it.
- **conda `-e .` without `--no-deps`** (low): the suggested change (`--no-deps -e .` in the `pip:` list)
  was **not** applied, because it would break `conda env create`. Conda writes that list into a temporary
  requirements file and runs `pip install -U -r <file>` (conda/env/installers/pip.py, read 2026-09-13),
  and pip 26.2.1 rejects the option there: `pip install --dry-run -r` on a file containing
  `--no-deps -e .` printed `error: no such option: --no-deps` and exited 1. Applied instead: `pip=26.2.1`
  (on conda-forge), and the "identical package set" claim was replaced by an expectation plus a lock
  comparison command users must run.
- **`make setup` with a non-3.12 interpreter** (low): `SETUP_PYTHON` defaults to `python3.12` (`py -3.12` on
  Windows), and `setup` checks the interpreter for 3.12 both before and after creating the venv. The
  guard commands were run in Git Bash: `py -3.12` passes; `py -3.14` stops with
  "NeuroSem needs CPython 3.12, found 3.14.7" and exit 1. Make itself is still not installed here.
- **Also corrected while checking**: REPRODUCING.md said Debian 13 (trixie) ships Python 3.12 as `python3`.
  It ships 3.13 (python3-defaults 3.13.5-1 in trixie, sources.debian.org, 2026-09-13); Ubuntu 24.04 ships
  3.12.3 (Launchpad, 2026-09-13).
