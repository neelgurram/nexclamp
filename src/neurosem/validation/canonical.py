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


def recorded_population(ws: Workspace) -> str | None:
    """Population of the harness OutputColumn that the manifest names as the voltage column."""
    parser = etree.XMLParser(remove_comments=True, resolve_entities=False)
    try:
        root = etree.parse(str(ws.harness_path), parser).getroot()
    except (etree.XMLSyntaxError, OSError):
        return None
    for of in root.iter():
        if _local(of.tag) == "OutputFile" and of.get("fileName") == ws.model.harness_output_file:
            cols = [c for c in of if _local(c.tag) == "OutputColumn"]
            k = int(ws.model.harness_v_column) - 1
            if 0 <= k < len(cols) and cols[k].get("quantity"):
                return re.split(r"[/\[]", cols[k].get("quantity").lstrip("./"), maxsplit=1)[0]
    return None


def _targeted_component_ids(files: list[Path], population: str) -> set[str]:
    ids: set[str] = set()
    parser = etree.XMLParser(remove_comments=True, resolve_entities=False)
    for f in files:
        try:
            root = etree.parse(str(f), parser).getroot()
        except (etree.XMLSyntaxError, OSError):
            continue
        for el in root.iter():
            tag = _local(el.tag)
            if tag == "inputList" and el.get("population") == population and el.get("component"):
                ids.add(el.get("component"))
            elif tag == "explicitInput" and el.get("input") and el.get("target"):
                target_pop = re.split(r"[/\[]", el.get("target").lstrip("./"), maxsplit=1)[0]
                if target_pop == population:
                    ids.add(el.get("input"))
    return ids


def canonical_protocol(ws: Workspace, features: tuple[str, ...] = CANONICAL_FEATURES) -> ConcreteProtocol:
    """Canonical analysis window = union of the pulses that target the RECORDED population.

    Harnesses can contain several inputs, some aimed at other cells (e.g. Prinz 2004) or an
    early hyperpolarising test before the depolarising one (e.g. Smith 2013). Only inputs to
    the population whose voltage the harness records define the window; if none can be
    identified, all pulse generators are used and the description says so.
    """
    text = ws.harness_path.read_text(encoding="utf-8", errors="replace")
    _step, length = harness_step_and_length(text)
    length_ms = units.parse(length).to("ms").value
    candidates = harness_nml_files(ws)
    if ws.cell_path.resolve() not in candidates:
        candidates.append(ws.cell_path.resolve())
    population = recorded_population(ws)
    targeted = _targeted_component_ids(candidates, population) if population else set()
    all_comps: list[tuple[str, StimulusComponent]] = []
    for pg in _pulse_generators(candidates):
        try:
            delay = units.parse(pg.get("delay")).to("ms").value
            dur = units.parse(pg.get("duration")).to("ms").value
            amp = units.parse(pg.get("amplitude")).to("nA").value
        except (TypeError, ValueError):
            continue
        all_comps.append((pg.get("id") or "", StimulusComponent("pulse", delay, dur, amp)))
    chosen = [c for cid, c in all_comps if cid in targeted]
    rule = f"pulses targeting population {population!r}"
    if not chosen:
        chosen = [c for _, c in all_comps]
        rule = "all pulse generators (no input targeting the recorded population identified)"
    if chosen:
        start = min(c.delay_ms for c in chosen)
        end = min(max(c.delay_ms + c.duration_ms for c in chosen), length_ms)
    else:
        start, end = 0.1 * length_ms, length_ms
        rule = "no pulse generators; window = last 90% of the simulation"
    if end <= start:
        start, end = 0.0, length_ms
    return ConcreteProtocol(CANONICAL_ID, "canonical", tuple(chosen), length_ms, AnalysisWindow(start, end),
                            tuple(features), description=f"shipped harness {ws.model.harness_lems}; window: {rule}")


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
