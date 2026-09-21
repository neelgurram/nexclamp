"""Regression: the corrected Pilot 1 facts (D-038) reproduce from the sealed, Git-tracked results.

Pilot 1 is reported only in this form: 22 real model edits (admissible semantic mutants), all detected
by the canonical test, 19 by the battery, none silent; the three earlier silent cases are numerical.
"""

from __future__ import annotations

import csv
import json

import pytest

from neuraxis.experiments import strata
from neuraxis.protocols.definitions import CANONICAL_ID
from neuraxis.provenance import REPO_ROOT
from neuraxis.schemas import MutantClass, RunRecord
from neuraxis.selection.matrix import DetectionMatrix

PILOT = REPO_ROOT / "results" / "processed" / "pilot"

pytestmark = pytest.mark.skipif(not (PILOT / "classification.csv").is_file(), reason="Pilot 1 results not present")


def _rows():
    with open(PILOT / "classification.csv", encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["kind"] == "mutant"]


def test_corrected_counts():
    rows = _rows()
    sem = [r for r in rows if strata.stratum(r["kind"], r["family"], r["operator"]) == strata.SEMANTIC]
    num = [r for r in rows if strata.stratum(r["kind"], r["family"], r["operator"]) == strata.NUMERICAL]
    admissible = [r for r in sem if r["class"] in (MutantClass.NON_EQUIVALENT.value, MutantClass.SILENT.value)]
    assert len(admissible) == 22
    assert not [r for r in sem if r["class"] == MutantClass.SILENT.value]
    assert sorted(r["operator"] for r in num if r["class"] == MutantClass.SILENT.value) == \
        ["increase_dt", "increase_dt", "recording_resolution"]
    m = DetectionMatrix.from_csv(PILOT / "detection_matrix.csv")
    m = m.take_rows([i for i, mid in enumerate(m.mutant_ids) if m.family_of[mid] in strata.SEMANTIC_FAMILIES])
    battery = [p for p in m.protocol_ids if p != CANONICAL_ID]
    can, bat = m.covered([CANONICAL_ID]), m.covered(battery)
    assert (m.n_mutants, int(can.sum()), int(bat.sum()), int((bat & ~can).sum())) == (22, 22, 19, 0)


def test_sealed_pilot_is_registered_exploratory_and_read_only():
    from neuraxis.experiments import registry

    assert registry.role_of("pilot", REPO_ROOT / "results") == registry.EXPLORATORY_PILOT
    assert registry.is_sealed("pilot", REPO_ROOT / "results")


def test_pilot1_run_records_load_under_the_current_schema():
    # Scope to the SEALED Pilot 1 set named in the archive manifest. The campaign directory may also
    # hold foreign runs written later by a tool that named this campaign (X-27); those are not Pilot 1
    # data and are excluded from every Pilot 1 statement.
    manifest = (REPO_ROOT / "results" / "processed" / "pilot" / "ARCHIVE_MANIFEST.sha256").read_text(encoding="utf-8")
    archived = {line.split()[1].split("/")[1] for line in manifest.splitlines()
                if line.strip() and line.split()[1].startswith("raw/r-")}
    runs = [f for f in sorted((REPO_ROOT / "results" / "raw" / "pilot").glob("r-*/run.json"))
            if f.parent.name in archived][:25]
    assert runs
    for f in runs:
        rec = RunRecord(**json.loads(f.read_text(encoding="utf-8")))
        assert rec.campaign == "pilot" and rec.execution_id == ""       # predates the new fields
