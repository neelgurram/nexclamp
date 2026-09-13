"""The canonical protocol: the simulation shipped with the model (validation layer 3).

The conventional regression test for a published NeuroML model is to rerun the
simulation distributed with it (e.g. the Open Source Brain OMV spike-time check). NeuroSem
therefore treats the shipped harness as the *canonical protocol* and analyses its voltage
trace with the same features and calibrated tolerances as every other protocol, so that
canonical and battery results differ only in the stimulus -- not in the metric.

The analysis window is taken from the REFERENCE harness and reused for every variant, so
that a variant whose harness stimulus was mutated is judged against the original test.
"""

from __future__ import annotations

import re
from pathlib import Path

from lxml import etree

from neurosem import units
from neurosem.models import Workspace
from neurosem.protocols.definitions import CANONICAL_FEATURES, CANONICAL_ID
from neurosem.protocols.generate import harness_step_and_length
from neurosem.schemas import AnalysisWindow, ConcreteProtocol, StimulusComponent
from neurosem.validation.structural import harness_nml_files


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _pulse_generators(files: list[Path]) -> list[etree._Element]:
    found = []
    parser = etree.XMLParser(remove_comments=True, resolve_entities=False)
    for f in files:
        try:
            root = etree.parse(str(f), parser).getroot()
        except (etree.XMLSyntaxError, OSError):
            continue
        found += [el for el in root.iter() if _local(el.tag) == "pulseGenerator"]
    return found


def canonical_protocol(ws: Workspace) -> ConcreteProtocol:
    text = ws.harness_path.read_text(encoding="utf-8", errors="replace")
    _step, length = harness_step_and_length(text)
    length_ms = units.parse(length).to("ms").value
    candidates = harness_nml_files(ws)
    if ws.cell_path.resolve() not in candidates:
        candidates.append(ws.cell_path.resolve())
    comps: list[StimulusComponent] = []
    for pg in _pulse_generators(candidates):
        try:
            delay = units.parse(pg.get("delay")).to("ms").value
            dur = units.parse(pg.get("duration")).to("ms").value
            amp = units.parse(pg.get("amplitude")).to("nA").value
        except (TypeError, ValueError):
            continue
        comps.append(StimulusComponent("pulse", delay, dur, amp))
    if comps:
        first = min(comps, key=lambda c: c.delay_ms)
        start, end = first.delay_ms, min(first.delay_ms + first.duration_ms, length_ms)
    else:
        start, end = 0.1 * length_ms, length_ms
    if end <= start:
        start, end = 0.0, length_ms
    return ConcreteProtocol(CANONICAL_ID, "canonical", tuple(comps), length_ms, AnalysisWindow(start, end),
                            CANONICAL_FEATURES, description=f"shipped harness {ws.model.harness_lems}")


_STEP_ATTR = re.compile(r'(<(?:Simulation|Component)\b[^>]*?\bstep=")([^"]+)(")', re.DOTALL)


def refine_harness_step(ws_root_harness: Path, factor: float) -> str:
    """Divide the harness time step by ``factor`` in place; returns the new step string."""
    text = ws_root_harness.read_text(encoding="utf-8")
    m = _STEP_ATTR.search(text)
    if not m:
        raise ValueError(f"no step attribute in {ws_root_harness}")
    q = units.parse(m.group(2)).to("ms")
    new = units.format_quantity(q.value / factor, "ms")
    ws_root_harness.write_text(text[: m.start(2)] + new + text[m.end(2):], encoding="utf-8")
    return new
