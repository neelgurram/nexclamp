# syntax=docker/dockerfile:1
#
# NeuroSem reproducible container: CPython 3.12 (Debian trixie, slim) + Eclipse Temurin 21 JRE
# + the exact Python pins in requirements.lock. The default command runs the full test suite.
#
# STATUS (2026-09-13): NEVER BUILT. Docker is not installed on the authoring machine; the
# `docker` job in .github/workflows/ci.yml is the first place this file will be built and run.
#
#   docker build -t neurosem:dev .
#   docker run --rm neurosem:dev                                   # full pytest suite
#   docker run --rm neurosem:dev python -m pytest -q -m "not jnml"
#
# Base image pinned by OCI image-index digest (multi-arch: linux/amd64 and linux/arm64).
# Resolved 2026-09-13 from registry-1.docker.io: python:3.12.14-slim-trixie, python:3.12-slim
# and python:3.12.14-slim all pointed at this digest; image env PYTHON_VERSION=3.12.14 and the
# root filesystem is Debian trixie. (python:3.12-slim-bookworm is a different digest.)
FROM python:3.12.14-slim-trixie@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea

# Temurin JRE: pinned release and per-architecture archive SHA-256. On 2026-09-13 the Adoptium
# API and the publisher's .sha256.txt files agreed on these digests. scripts/bootstrap_java.py
# refuses to install if the API, the checksum file, this pin or the downloaded bytes disagree.
ARG TEMURIN_RELEASE=jdk-21.0.12.1+1
ARG TEMURIN_JRE_SHA256_AMD64=2413149700df0f7d440500a84a8f764c535f21e5a5e87d38328b64eec2c5b500
ARG TEMURIN_JRE_SHA256_ARM64=14be1f35ebdbd1f6e8d57eb911a3ffb74d6d9aa255abc5daf2b1302002cf2cf2
# Set automatically by BuildKit; the legacy builder leaves it empty, which is treated as amd64.
ARG TARGETARCH
ARG GIT_COMMIT=unknown

LABEL org.opencontainers.image.title="NeuroSem" \
      org.opencontainers.image.version="0.1.0.dev0" \
      org.opencontainers.image.licenses="BSD-3-Clause" \
      org.opencontainers.image.revision="${GIT_COMMIT}"

# PROVENANCE: the image has no git or .git. neuraxis.provenance.git_state() falls back to
# NEUROSEM_GIT_COMMIT (set below from the GIT_COMMIT build argument, like the OCI revision label) and
# reports dirty=True, because the tree cannot be checked. Build with --build-arg GIT_COMMIT=<sha>, and
# pass -e NEUROSEM_CONTAINER_IMAGE=<repo@sha256:...> at run time so the image enters the environment
# digest. Neither path has been exercised in a real container yet (Docker has not been run).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MPLBACKEND=Agg \
    NEUROSEM_GIT_COMMIT=${GIT_COMMIT} \
    JAVA_HOME=/opt/java/${TEMURIN_RELEASE}-jre \
    NEUROSEM_JAVA=/opt/java/${TEMURIN_RELEASE}-jre/bin/java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Unprivileged runtime user (tests and experiments never need root).
RUN groupadd --gid 10001 neurosem \
 && useradd --uid 10001 --gid neurosem --create-home --shell /bin/sh neurosem

WORKDIR /opt/neurosem

# 1) Java runtime (own layer: changes only when the pin changes). The provenance record is
#    written to /opt/java/<release>-jre.provenance.json.
COPY scripts/bootstrap_java.py scripts/bootstrap_java.py
RUN set -eu; \
    case "${TARGETARCH:-amd64}" in \
      amd64) arch=x64;     sha="$TEMURIN_JRE_SHA256_AMD64" ;; \
      arm64) arch=aarch64; sha="$TEMURIN_JRE_SHA256_ARM64" ;; \
      *) echo "unsupported TARGETARCH=${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    python scripts/bootstrap_java.py --dest /opt/java --os linux --arch "$arch" --image-type jre \
        --release "$TEMURIN_RELEASE" --expect-sha256 "$sha"; \
    test -x "$NEUROSEM_JAVA"; \
    java -version

# 2) Exact Python pins. requirements.lock was frozen on Windows; every pin has a manylinux
#    x86_64 wheel, but this step is the real Linux verification (see the header of the lock).
COPY requirements.lock ./
RUN python -m pip install pip==26.2.1 \
 && python -m pip install -r requirements.lock

# 3) Project source, editable install (neuraxis.provenance.REPO_ROOT resolves to the source
#    tree, which is where configs/, data/ and models/ live). The build backend (setuptools>=69)
#    is fetched by pip's build isolation and is not pinned; it is build-time only.
COPY . .
RUN python -m pip install --no-deps -e . \
 && python -m pip check \
 && python -c "import subprocess, sys; lock = {l.strip() for l in open('requirements.lock') if l.strip() and not l.startswith('#')}; frz = set(subprocess.run([sys.executable, '-m', 'pip', 'freeze', '--exclude-editable'], capture_output=True, text=True, check=True).stdout.split()); print('installed but not in lock:', sorted(frz - lock)); missing = sorted(lock - frz); sys.exit('lock pins not installed: %s' % missing if missing else 0)" \
 && chown -R neurosem:neurosem /opt/neurosem

USER neurosem

# Build-time smoke check: the jNeuroML jar from pyNeuroML and the pinned JRE are found and run.
RUN python -c "from neuraxis.simulators.jneuroml import JNeuroML; s = JNeuroML(); assert s.available(), 'Java or jNeuroML jar missing'; print(s.java, s.jar); print(s.version_string())"

CMD ["python", "-m", "pytest", "-q"]
