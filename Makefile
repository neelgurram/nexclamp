# NeuroSem task runner. Needs GNU make and a POSIX shell (Linux, macOS, or Windows Git Bash
# with make installed). Every target is a thin wrapper: `make -n <target>` prints the exact
# commands. On Windows without make, run the equivalent commands in docs/REPRODUCING.md.
# This Makefile has never been executed: GNU make is not installed on the authoring machine.
#
# validate-models, pilot and reproduce-paper call the `neurosem` CLI (src/neuraxis/cli.py,
# docs/ARCHITECTURE.md section 3.9). On 2026-09-13 their argument parsing was checked with
# `neurosem <command> --help`; pilot and reproduce-paper were not run.
#
# Overridable variables, e.g. `make test PYTHON=python` inside the Docker image (no venv there),
# or `make setup SETUP_PYTHON=/opt/python3.12/bin/python3`.

.DEFAULT_GOAL := help

VENV ?= .venv
ifeq ($(OS),Windows_NT)
VENV_BIN := $(VENV)/Scripts
BOOTSTRAP_PYTHON ?= python
SETUP_PYTHON ?= py -3.12
else
VENV_BIN := $(VENV)/bin
BOOTSTRAP_PYTHON ?= python3
SETUP_PYTHON ?= python3.12
endif
PYTHON ?= $(VENV_BIN)/python
NEUROSEM ?= $(VENV_BIN)/neurosem
CURATION ?= curation-v3
CAMPAIGN ?= pilot
IMAGE ?= neurosem:dev
PYTEST_ARGS ?=
JAVA_ARGS ?=

# The project requires CPython 3.12 (pyproject: >=3.12,<3.13) and the lock holds cp312 wheels.
# Checking the interpreter before creating the venv, and the venv itself afterwards (it may
# predate this run), stops with a clear message instead of leaving a half-installed .venv.
REQUIRE_PY312 := -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 12) else 'NeuroSem needs CPython 3.12, found ' + sys.version.split()[0] + ' at ' + sys.executable)"

.PHONY: help setup java test test-fast validate-models pilot reproduce-paper docker-build docker-test lint

help:
	@echo "NeuroSem make targets"
	@echo "  setup            create $(VENV) with $(SETUP_PYTHON) (must be CPython 3.12), install requirements.lock and neurosem (editable), pip check"
	@echo "  java             download Eclipse Temurin 21 into .tools/ (scripts/bootstrap_java.py $(JAVA_ARGS))"
	@echo "  test             full pytest suite (jnml tests are skipped when Java is unavailable)"
	@echo "  test-fast        pytest without jnml-marked tests"
	@echo "  validate-models  neurosem validate-models"
	@echo "  pilot            neurosem pilot --campaign $(CAMPAIGN)"
	@echo "  reproduce-paper  neurosem reproduce-paper --campaign $(CAMPAIGN)"
	@echo "  docker-build     docker build -t $(IMAGE) ."
	@echo "  docker-test      run the test suite inside $(IMAGE)"
	@echo "  lint             ruff check src tests scripts"
	@echo "  readiness        full readiness sequence (suite, lint, types, clean env, smoke, hashes, CLI)"
	@echo "  curation-table   final curation table from a finished curation campaign"
	@echo "  pilot2-prepare   regenerate the frozen Pilot 2 matrix and its pre-run hashes"
	@echo "  pilot2-authorize check every Pilot 2 launch condition (never launches)"
	@echo "  pilot2           run the frozen Pilot 2 campaign (only after pilot2-authorize passes)"

setup:
	test -d "$(VENV)" || { $(SETUP_PYTHON) $(REQUIRE_PY312) && $(SETUP_PYTHON) -m venv "$(VENV)"; }
	$(PYTHON) $(REQUIRE_PY312)
	$(PYTHON) -m pip install pip==26.2.1
	$(PYTHON) -m pip install -r requirements.lock
	$(PYTHON) -m pip install --no-deps -e .
	$(PYTHON) -m pip check

java:
	$(BOOTSTRAP_PYTHON) scripts/bootstrap_java.py $(JAVA_ARGS)

test:
	$(PYTHON) -m pytest -q $(PYTEST_ARGS)

test-fast:
	$(PYTHON) -m pytest -q -m "not jnml" $(PYTEST_ARGS)

validate-models:
	$(NEUROSEM) validate-models

pilot:
	$(NEUROSEM) pilot --campaign $(CAMPAIGN)

reproduce-paper:
	$(NEUROSEM) reproduce-paper --campaign $(CAMPAIGN)

docker-build:
	docker build --build-arg GIT_COMMIT="$$(git rev-parse HEAD 2>/dev/null || echo unknown)" -t $(IMAGE) .

docker-test:
	docker run --rm $(IMAGE)

lint:
	$(PYTHON) -m ruff check src tests scripts

readiness:
	$(PYTHON) scripts/readiness.py

curation-table:
	$(PYTHON) scripts/curation_table.py --curation $(CURATION)

pilot2-prepare:
	NEURAXIS_STUDY_CONFIG=configs/pilot2_frozen.yaml $(PYTHON) scripts/pilot2_prepare.py --curation $(CURATION)

pilot2-authorize:
	$(PYTHON) scripts/pilot2_authorize.py --curation $(CURATION)

pilot2: pilot2-authorize
	NEURAXIS_STUDY_CONFIG=configs/pilot2_frozen.yaml $(PYTHON) -m neuraxis pilot --campaign pilot2
