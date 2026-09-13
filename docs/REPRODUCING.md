# Reproducing the NeuroSem environment

This guide gives exact commands to rebuild the environment on Windows and Linux, and says plainly
what has and has not been verified. NeuroSem is pre-pilot: there are **no scientific results to
reproduce yet**. The pipeline commands (`neurosem validate-models`, `pilot`, `reproduce-paper`) exist
in `src/neurosem/cli.py`; what was checked about them is listed below and in the last section.

## What was verified, where (2026-09-13)

| Item | Status |
|---|---|
| `requirements.lock` fresh install on Windows 11 x86_64, CPython 3.12.10 | **Verified**: new venv, `pip install -r requirements.lock`, `pip install --no-deps -e .`; `pip check` reported "No broken requirements found"; `pip freeze` equal to the lock (75 pins); `import neurosem, efel, pyneuroml, neuroml` worked; pytest collection worked. Run from Git Bash with `python -m venv`. |
| Same lock on Linux x86_64 | **Not installed on Linux.** Checked only on paper: every pin has a manylinux x86_64 cp312/abi3 or pure-Python wheel; a wheel-tag dry-run resolved to the same 75 pins; no Linux-only dependency marker is missing. The Docker build and CI are the real checks. |
| `scripts/bootstrap_java.py` on Windows | **Verified** with `--dry-run` from Git Bash and PowerShell: live Adoptium API query, SHA-256 agreement with the publisher's `.sha256.txt`, detection of the existing `.tools/jdk-21.0.12.1+1` and a real `java -version`. The full 205 MB download path was **not** re-run on Windows; it is covered by offline tests (loopback HTTP server, real archives) and by the Docker build (Linux JRE). |
| Pinned Linux JRE for Docker (x64 and aarch64) | API and `.sha256.txt` agree with the digests pinned in the `Dockerfile` (dry-run, live). Archive not downloaded here. |
| Docker build context (`.dockerignore`) | **Emulated, not built.** The repository was copied into a scratch directory under the `.dockerignore` rules, using the Python reimplementation in `tests/unit/test_infra_repro_files.py`. The copy had 555 files and 5.1 MB, with `.github` present and `.git`, `.tools` and `work` absent. Git discovery was blocked, and Java came from `NEUROSEM_JAVA` as in the Dockerfile. `pytest -m "not jnml"` there gave 764 passed, 2 skipped, 7 xfailed and 0 failed. That includes `test_ci_workflow_structure`, which failed in this setup while `.dockerignore` excluded `.github`. A full run including jnml tests was stopped at 17% of tests (0 failures by then) because it would have taken hours. This ran on Windows, so Linux wheels, file permissions and the non-root user were not exercised. |
| `Dockerfile` | **Never built**: Docker is not installed on the authoring machine. Base digest resolved live from Docker Hub. |
| `.github/workflows/ci.yml` | **Never run**: the repository has no GitHub remote yet. |
| `Makefile` | **Never executed**: GNU make is not installed on the authoring machine. CI runs `make -n` on all targets. The `setup` Python 3.12 guard commands were run by hand in Git Bash (`py -3.12` passes; `py -3.14` stops with "NeuroSem needs CPython 3.12, found 3.14.7", exit 1). |
| `environment.yml` (conda) | **Not tested**: conda is not installed on the authoring machine. |
| `neurosem` CLI routes | `neurosem validate-models --help`, `pilot --help` and `reproduce-paper --help` parse. `neurosem validate-models --models pospischil2008_rs` ran successfully (exit 0, about 4 s) in the emulated Docker build context. `pilot` and `reproduce-paper` were **not run**. |
| `CITATION.cff` | Validated against the official CFF 1.2.0 JSON schema (jsonschema Draft 7, zero errors). |

## Requirements

- CPython **3.12** (the project requires `>=3.12,<3.13`).
- Internet access for PyPI, the Adoptium API (`api.adoptium.net`) and GitHub release downloads.
- Disk space for the venv (scientific wheels: numpy, scipy, pandas, matplotlib, h5py, tables, ...)
  and for Temurin 21. Download sizes reported by the Adoptium API on 2026-09-13: 205 MB for the
  Windows x64 JDK zip, 52 MB for the Linux x64 JRE tarball. Unpacked sizes were not measured.
- Git, to get the source. There is no public repository yet; copy or clone the project directory.

Java is **not** installed system-wide. `scripts/bootstrap_java.py` puts Eclipse Temurin 21 into
`.tools/`, where `neurosem.simulators.jneuroml.find_java()` looks for it. It uses only the standard
library, so it runs before anything else is installed.

## Windows 11 (PowerShell)

Run from the repository root. Use `py -3.12` explicitly: the Python launcher's default can be a
different version (on the authoring machine it is 3.14).

```powershell
cd C:\path\to\NeuroSem
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install pip==26.2.1
.\.venv\Scripts\python -m pip install -r requirements.lock
.\.venv\Scripts\python -m pip install --no-deps -e .
.\.venv\Scripts\python -m pip check

# Java: first see what would happen, then install (about 205 MB download for the JDK zip)
.\.venv\Scripts\python scripts\bootstrap_java.py --dry-run
.\.venv\Scripts\python scripts\bootstrap_java.py

# Tests: fast subset first (no Java needed), then everything
.\.venv\Scripts\python -m pytest -q -m "not jnml"
.\.venv\Scripts\python -m pytest -q
```

Git Bash uses the same commands with forward slashes (`.venv/Scripts/python ...`). The editable
install (`-e .`) is required: `neurosem.provenance.REPO_ROOT` is derived from the location of the
source tree, which is where `configs/`, `data/` and `models/` live.

## Linux (Debian / Ubuntu, x86_64)

Not run on Linux by the author yet (see the table above). You need a CPython 3.12 interpreter, and
whether the distribution provides one depends on the release (package versions checked on
2026-09-13 at sources.debian.org and Launchpad):

- Ubuntu 24.04 (noble): `python3` is 3.12 (3.12.3). Install `python3.12-venv` if `venv` is missing.
- Debian 13 (trixie): `python3` is **3.13**; Debian 12 (bookworm): **3.11**. Neither works. Use a
  separately installed 3.12 (for example pyenv or a python.org source build) or the Docker image.

```bash
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

Or, with GNU make: `make setup java test`. `make setup` creates the venv with `SETUP_PYTHON`
(default `python3.12`; `py -3.12` on Windows) and stops unless both that interpreter and the venv are
CPython 3.12. Point it elsewhere with `make setup SETUP_PYTHON=/path/to/python3.12`.

**macOS** is not a verified target. `bootstrap_java.py` supports it, but the runtime lands in
`.tools/jdk-<release>/Contents/Home/bin/java`, which `find_java()` does not search yet. Set
`NEUROSEM_JAVA` to the path the script prints (see `docs/build_notes/infra.md`).

## Java runtime details

`scripts/bootstrap_java.py`:

1. picks the Adoptium `os`/`architecture` for this machine (override with `--os`, `--arch`);
2. queries `/v3/assets/latest/21/hotspot` or, with `--release`, `/v3/assets/release_name/eclipse/<release>`;
3. requires one matching HotSpot binary, then checks that the API SHA-256 equals the publisher's
   `.sha256.txt` and, when given, `--expect-sha256`;
4. downloads to a `.part` file while hashing, and keeps the archive only if size and SHA-256 match;
5. extracts into a private temporary directory with path-traversal protection (tar: stdlib `data`
   filter) and runs `java -version` there. Only a runtime that passes is moved into `.tools/`. A
   runtime that fails (for example a wrong `--arch`) is deleted, and the verified archive is kept for a retry;
6. writes `.tools/<install-dir>.provenance.json`: asset metadata, every digest, host, the script's
   own SHA-256, the JDK `release` file and the `java -version` output.

To get **exactly** the runtime used during development instead of the newest Temurin 21:

```bash
python scripts/bootstrap_java.py --release jdk-21.0.12.1+1
# Windows x64 JDK zip SHA-256 (Adoptium API, 2026-09-13):
python scripts/bootstrap_java.py --release jdk-21.0.12.1+1 \
    --expect-sha256 f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e
```

The `.tools/jdk-21.0.12.1+1` install on the authoring machine was made during the Milestone 0
audit, before this script existed; its hash record is `.tools/jdk_provenance.json`. Running the
script without `--dry-run` would add `.tools/jdk-21.0.12.1+1.provenance.json` with
`"action": "existing_install"` and `"archive_verified": false`, because the archive is gone.

Run the live-network test of the script with:

```bash
NEUROSEM_NETWORK_TESTS=1 .venv/bin/python -m pytest -q tests/unit/test_infra_bootstrap_java.py
```

## Docker

Docker was not available on the authoring machine, so these commands have **not** been run. The
`docker` job in `.github/workflows/ci.yml` builds the image and runs the test suite inside it.

```bash
docker build --build-arg GIT_COMMIT="$(git rev-parse HEAD)" -t neurosem:dev .
docker run --rm neurosem:dev                                    # full pytest suite
docker run --rm neurosem:dev python -m pytest -q -m "not jnml"
docker image inspect --format '{{.Id}}' neurosem:dev            # record with any results
```

The image contains:

- `python:3.12.14-slim-trixie`, pinned by index digest `sha256:78387bc3…e184ea` (Python 3.12.14, Debian trixie);
- Temurin JRE `jdk-21.0.12.1+1` from Adoptium, SHA-256 pinned for amd64 and arm64 and installed
  by `bootstrap_java.py` into `/opt/java`;
- pip 26.2.1 and `requirements.lock`, with a build-time check that every pin is installed;
- the source at `/opt/neurosem` as an editable install;
- an unprivileged user `neurosem` (uid 10001).

At build time the image also checks that jNeuroML and Java are found. The default command runs
`python -m pytest -q`, so `.dockerignore` must never exclude a file that a test reads.
`tests/unit/test_infra_repro_files.py` checks this.

> **Provenance in containers.** The specification requires every simulation to record its Git commit.
> The image has no `git` and no `.git`, so `neurosem.provenance.git_state()` falls back to
> `NEUROSEM_GIT_COMMIT`, set from the `GIT_COMMIT` build argument, and reports `dirty=True` because the
> tree cannot be checked. This was implemented after the infra build note, as DECISIONS D-021 records.
> Build with `--build-arg GIT_COMMIT=$(git rev-parse HEAD)`. Pass
> `-e NEUROSEM_CONTAINER_IMAGE=<repo@sha256:...>` so the image digest enters the environment digest.
> The fallback is unit-level only and has not been exercised in a real container, so verify it before
> using container runs as study results.

## Conda (untested alternative)

```bash
conda env create -f environment.yml     # run from the repository root
conda activate neurosem
python -m pip check
python -c "import subprocess, sys; lock = {l.strip() for l in open('requirements.lock') if l.strip() and not l.startswith('#')}; frz = set(subprocess.run([sys.executable, '-m', 'pip', 'freeze', '--exclude-editable'], capture_output=True, text=True, check=True).stdout.split()); print('installed but not in lock:', sorted(frz - lock)); missing = sorted(lock - frz); sys.exit('lock pins not installed: %s' % missing if missing else 0)"
python scripts/bootstrap_java.py
python -m pytest -q
```

Conda provides only Python 3.12 and pip 26.2.1 (conda-forge channel); all packages come from
`requirements.lock`. Unlike the other routes, conda cannot run `pip install --no-deps -e .` as a
separate step. It passes the `pip:` list to pip as a requirements file, and pip does not accept
`--no-deps` there. So `-e .` is resolved together with the lock. Exact lock pins are expected but
not guaranteed, which is why the comparison command above must print `installed but not in lock: []`
and exit 0. The same one-liner printed that and exited 0 on the Windows development venv (2026-09-13).

## Make targets

| Target | Command it runs |
|---|---|
| `setup` | check `$(SETUP_PYTHON)` is 3.12, create `.venv`, check the venv is 3.12, install pip 26.2.1, `requirements.lock`, `--no-deps -e .`, `pip check` |
| `java` | `python scripts/bootstrap_java.py $(JAVA_ARGS)` |
| `test` / `test-fast` | `pytest -q` / `pytest -q -m "not jnml"` |
| `validate-models` | `neurosem validate-models` |
| `pilot` | `neurosem pilot --campaign $(CAMPAIGN)` (default `pilot`) |
| `reproduce-paper` | `neurosem reproduce-paper --campaign $(CAMPAIGN)` |
| `docker-build` / `docker-test` | `docker build -t $(IMAGE) .` / `docker run --rm $(IMAGE)` |
| `lint` | `ruff check src tests scripts` |

`make -n <target>` prints the commands without running them. Without make, run those commands directly.

## Pipeline commands

Defined in `docs/ARCHITECTURE.md` §3.9 and implemented in `src/neurosem/cli.py`:

```bash
neurosem validate-models
neurosem pilot --campaign pilot
neurosem reproduce-paper --campaign pilot
```

Checked on 2026-09-13: all three parse their arguments (`--help`), and `validate-models` completed for one
model (`--models pospischil2008_rs`) in the emulated Docker build context. `pilot` and `reproduce-paper`
have not been run through any route (venv, Make or Docker), so these instructions do not show that they
produce correct outputs.

## Known limits on reproducibility

- `requirements.lock` pins versions, not file hashes (`pip freeze` does not record hashes).
  PyPI does not allow re-uploading a release file, but a new wheel could still be added to an existing version.
- The build backend (`setuptools>=69`, fetched by pip's build isolation for `-e .`) is not pinned.
  It is only used at build time.
- The CPython patch version differs by route: dev venv 3.12.10, Docker 3.12.14, and CI takes whatever
  3.12.x `actions/setup-python` provides at run time.
- CI's `tests` job takes the newest Temurin 21 from `actions/setup-java`. Only the Docker image pins
  the exact JRE build.
- Compiled wheels (numpy, scipy, efel, lxml, …) differ between operating systems, and jLEMS
  floating-point output may differ at the last bits across JVM builds and CPUs. Compare simulated
  quantities within the study's calibrated tolerances, never bit for bit across platforms.
- Inside Docker, runs record the commit from `NEUROSEM_GIT_COMMIT` (the build argument) with
  `dirty=True`. This fallback is untested in a real container (see the Docker section).
- The conda route resolves `-e .` together with the lock instead of using `--no-deps` (see Conda).
- Passing tests show that these specific checks passed. They do not prove that two environments
  are equivalent.
