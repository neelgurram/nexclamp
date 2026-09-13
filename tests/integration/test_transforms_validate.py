"""jNeuroML checks of valid transformations on RS, LTS and the NeuroML2 HH example.

1. Every transform operator's variants validate with ``jnml -validate`` (all changed or new
   NeuroML files plus the cell file). ``jnml -validate`` does not accept LEMS files, so a
   variant that edits a LEMS harness is additionally *run* as a shortened copy of that
   harness and its voltage column compared with the shortened reference harness.
2. For a subset (one variant per operator plus a renamed cell and a factored cell file) a
   short probe battery is simulated for reference and transform, and the voltage columns are
   compared with plain numpy on the raw jLEMS output files.

Bitwise equality is *not* required. Decimal-exact literals can still yield different SI
doubles inside jLEMS: a literal is parsed to the nearest binary double and then scaled by
its unit's power of ten, so ``0.07 mS_per_cm2`` (parse 0.07, multiply by 10) and
``0.7 S_per_m2`` (parse 0.7) may differ in the last bit; reordering summed currents or
multiplied gates changes floating-point evaluation order. Forward-Euler integration can
amplify such last-bit differences. The bound used below (``TRACE_TOL_MV``) is far above
round-off yet far below any physiological change; the observed maxima are printed and saved
so they can be reported. Passing is evidence of no *detected* difference on these finite
tests, not proof of equivalence.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import numpy as np
import pytest

from neurosem.models import materialize
from neurosem.protocols.generate import write_probe
from neurosem.provenance import tree_manifest
from neurosem.schemas import AnalysisWindow, ConcreteProtocol, ExecConfig, StimulusComponent
from neurosem.transforms import REGISTRY, apply_model_overrides, generate_transforms

pytestmark = pytest.mark.jnml

MODELS = ("pospischil2008_rs", "pospischil2008_lts", "nml2_hh_example")
N_PER_OPERATOR = 4
SEED = 20260913
TRACE_TOL_MV = 1e-3
DT_MS = 0.025
# step amplitudes (nA) of each model's shipped harness, used only to make the probe spike
PROBE_AMPLITUDE_NA = {"pospischil2008_rs": 0.75, "pospischil2008_lts": 0.15, "nml2_hh_example": 0.08}


@pytest.fixture(scope="module")
def generated(tmp_path_factory, models):
    root = tmp_path_factory.mktemp("transforms")
    out = {}
    for mid in MODELS:
        model = models[mid]
        records = generate_transforms(model, sorted(REGISTRY), N_PER_OPERATOR, SEED, root / "variants")
        pristine = materialize(model, root / "pristine" / mid)
        out[mid] = (root, pristine, records)
    return out


def _variant_ws(root: Path, pristine, record):
    from neurosem.models import Workspace

    return Workspace(root / "variants" / record.model_id / record.variant_id, pristine.model)


def _changed(pristine_root: Path, var_root: Path) -> list[str]:
    ref, var = tree_manifest(pristine_root), tree_manifest(var_root)
    return sorted(f for f in set(ref) | set(var) if ref.get(f) != var.get(f))


def _read_columns(path: Path) -> np.ndarray:
    """Raw jLEMS OutputFile (SI units): whitespace-separated columns, time first."""
    data = np.loadtxt(path, ndmin=2)
    assert data.shape[0] > 10 and np.all(np.isfinite(data))
    return data


def _short_harness(sim, ws, dest: Path) -> np.ndarray:
    shutil.copytree(ws.root, dest)
    harness = dest / ws.model.harness_lems
    text = harness.read_text(encoding="utf-8")
    text, n_len = re.subn(r'(<(?:Simulation|Component)\b[^>]*?\blength=")[^"]+(")', r"\g<1>60ms\2", text, 1, re.DOTALL)
    text, n_step = re.subn(r'(<(?:Simulation|Component)\b[^>]*?\bstep=")[^"]+(")', rf"\g<1>{DT_MS}ms\2", text, 1, re.DOTALL)
    assert n_len == n_step == 1
    harness.write_text(text, encoding="utf-8")
    res = sim.run_lems(harness, [])
    assert res.status.value == "ok", f"{ws.root.name}: harness run {res.status.value}: {res.message}"
    data = _read_columns(harness.parent / ws.model.harness_output_file)
    return data[:, [0, int(ws.model.harness_v_column)]]


def _probe(sim, ws, amplitude_nA: float) -> np.ndarray:
    protocols = [
        ConcreteProtocol("TX_dep", "step", (StimulusComponent("pulse", 50.0, 200.0, amplitude_nA),), 300.0,
                         AnalysisWindow(50.0, 250.0), ()),
        ConcreteProtocol("TX_hyp", "step", (StimulusComponent("pulse", 50.0, 200.0, -amplitude_nA),), 300.0,
                         AnalysisWindow(50.0, 250.0), ()),
    ]
    bundle = write_probe(ws, protocols, ExecConfig(DT_MS), tag="transform_check")
    res = sim.run_lems(bundle.lems_file, [bundle.output])
    assert res.status.value == "ok", f"{ws.root.name}: probe {res.status.value}: {res.message}"
    return _read_columns(bundle.lems_file.parent / bundle.output.file)


def _compare(ref: np.ndarray, var: np.ndarray) -> dict:
    assert ref.shape == var.shape, f"shape {ref.shape} vs {var.shape}"
    assert np.array_equal(ref[:, 0], var[:, 0]), "time columns differ"
    diff_mV = np.abs(ref[:, 1:] - var[:, 1:]) * 1e3
    return {"max_abs_diff_mV": float(diff_mV.max()), "bitwise_equal": bool(np.array_equal(ref, var)),
            "n_samples": int(ref.shape[0])}


def _key(path: Path) -> str:
    return str(Path(path).resolve()).lower()


def _file_results(raw_output: str) -> dict[str, tuple[bool, frozenset[str]]]:
    """Per-file verdicts from one ``jnml -validate`` call over many files.

    A file counts as valid only with "Valid against schema and all tests" *and* "No warnings",
    matching ``JNeuroML.validate`` (which requires the summary "All valid").
    """
    out = {}
    for block in re.split(r"^Validating: ", raw_output, flags=re.MULTILINE)[1:]:
        path, _, body = block.partition("\n")
        body = re.split(r"^Validated \d+ files?:", body, flags=re.MULTILINE)[0]
        ok = "Valid against schema and all tests" in body and "No warnings" in body
        msgs = frozenset(re.sub(r"\s+", " ", ln.strip()) for ln in body.splitlines()
                         if re.search(r"cvc-|Test: |Warning, check", ln))
        out[_key(Path(path.strip()))] = (ok, msgs)
    return out


def _network_files(root: Path, harness: str) -> set[str]:
    """NeuroML files defining a <network>, reachable from the harness (independent include walk)."""
    from lxml import etree

    seen, todo, nets = set(), [harness], set()
    while todo:
        rel = todo.pop()
        if rel in seen:
            continue
        seen.add(rel)
        tree = etree.parse(str(root / rel)).getroot()
        for el in tree.iter():
            if not isinstance(el.tag, str):
                continue
            local = etree.QName(el).localname
            if local == "network":
                nets.add(rel)
            ref = el.get("href") if local == "include" else (el.get("file") if local == "Include" else None)
            if ref and ((root / rel).parent / ref).is_file():
                todo.append(((root / rel).parent / ref).resolve().relative_to(root.resolve()).as_posix())
    return nets


@pytest.mark.parametrize("model_id", MODELS)
def test_every_transform_validates_with_jnml(sim, generated, model_id, tmp_path, request):
    """Cell and network files must be valid; any other touched file must not become less valid.

    Two files of the LTS snapshot (IT.channel.nml, Ca.nml) already fail ``jnml -validate`` on
    their own because of custom LEMS types, although LTS.cell.nml that includes them is valid.
    A transform touching such a file is accepted only if the file's validation messages are
    identical to those of the pristine file. Files created by a transform must be valid.
    """
    root, pristine, records = generated[model_id]
    assert {r.operator for r in records} == set(REGISTRY), "every operator must produce variants"
    checks: list[tuple[str, str, Path, bool]] = []            # variant, rel, path, must be valid
    lems_changed = []
    for r in records:
        ws = _variant_ws(root, pristine, r)
        changed = _changed(pristine.root, ws.root)
        assert changed, f"{r.variant_id} changed nothing"
        required = {ws.model.cell_file} | _network_files(ws.root, ws.model.harness_lems)
        for rel in sorted(required | {f for f in changed if f.endswith(".nml")}):
            checks.append((r.variant_id, rel, ws.root / rel, rel in required or not (pristine.root / rel).exists()))
        if any(not f.endswith(".nml") for f in changed):
            lems_changed.append((r, ws))

    problems, preexisting = _judge(sim, pristine, checks)
    assert not problems, f"jnml -validate failures introduced by transforms of {model_id}: " \
                         f"{json.dumps(problems, indent=1)}"

    report = {"validated_files": len(checks), "variants": len(records),
              "preexisting_invalid_files_touched": sorted(preexisting), "harness_runs": {}}
    if lems_changed:
        ref = _short_harness(sim, pristine, tmp_path / "ref_harness")
        for r, ws in lems_changed:
            cmp = _compare(ref, _short_harness(sim, apply_model_overrides(ws, r.model_overrides),
                                               tmp_path / f"h_{r.variant_id}"))
            report["harness_runs"][r.variant_id] = cmp
            assert cmp["max_abs_diff_mV"] <= TRACE_TOL_MV, f"{r.variant_id}: {cmp}"
    request.node.user_properties.append(("transform_validation", report))
    (tmp_path / "report.json").write_text(json.dumps(report, indent=1))
    print(f"\n{model_id}: {json.dumps(report, indent=1)}")


VALIDATE_CHUNK = 100          # keeps each jnml command line well below the Windows 32 767-character limit


def _validate_many(sim, paths: list[Path]) -> dict[str, tuple[bool, frozenset[str]]]:
    out: dict[str, tuple[bool, frozenset[str]]] = {}
    unique = list(dict.fromkeys(paths))
    for i in range(0, len(unique), VALIDATE_CHUNK):
        chunk = unique[i:i + VALIDATE_CHUNK]
        out.update(_file_results(sim.validate(chunk, timeout_s=3000).raw_output))
    return out


def _judge(sim, pristine, checks: list[tuple[str, str, Path, bool]]) -> tuple[list[dict], set[str]]:
    """Apply the validity rule of ``test_every_transform_validates_with_jnml`` to many files."""
    results = _validate_many(sim, [c[2] for c in checks])
    ref_rels = sorted({rel for _, rel, _, _ in checks if (pristine.root / rel).exists()})
    ref_results = _validate_many(sim, [pristine.root / rel for rel in ref_rels])
    problems, preexisting = [], set()
    for vid, rel, path, must in checks:
        assert _key(path) in results, f"no validator verdict parsed for {path}"
        ok, msgs = results[_key(path)]
        if ok:
            continue
        ref = ref_results.get(_key(pristine.root / rel))
        if not must and ref is not None and not ref[0] and ref[1] == msgs:
            preexisting.add(rel)
            continue
        problems.append({"variant": vid, "file": rel, "messages": sorted(msgs),
                         "reference_valid": None if ref is None else ref[0]})
    return problems, preexisting


@pytest.mark.slow
@pytest.mark.parametrize("model_id", MODELS)
def test_all_sites_validate_with_jnml(sim, models, model_id, tmp_path, request):
    """Exhaustive form of the validation check: every site of every operator, one variant each.

    Harness runs are not repeated here (the sampled test covers them); this test only asks
    whether any site at all produces a file that jNeuroML rejects.
    """
    model = models[model_id]
    pristine = materialize(model, tmp_path / "pristine")
    checks: list[tuple[str, str, Path, bool]] = []
    counts = {}
    for name, op in sorted(REGISTRY.items()):
        sites = op.sites(pristine)
        counts[name] = len(sites)
        assert sites, f"{name} offers no sites for {model_id}"
        for k, site in enumerate(sites):
            vid = f"{name}_{k:03d}"
            ws = materialize(model, tmp_path / vid)
            op.apply(ws, site)
            changed = _changed(pristine.root, ws.root)
            assert changed, f"{vid} changed nothing"
            required = {model.cell_file} | _network_files(ws.root, model.harness_lems)
            for rel in sorted(required | {f for f in changed if f.endswith(".nml")}):
                checks.append((vid, rel, ws.root / rel, rel in required or not (pristine.root / rel).exists()))
    problems, preexisting = _judge(sim, pristine, checks)
    report = {"sites_per_operator": counts, "variants": sum(counts.values()), "validated_files": len(checks),
              "preexisting_invalid_files_touched": sorted(preexisting), "problems": problems}
    request.node.user_properties.append(("all_sites_validation", report))
    print(f"\n{model_id} all sites: {json.dumps({k: v for k, v in report.items() if k != 'problems'})}")
    assert not problems, f"jnml -validate failures for {model_id}: {json.dumps(problems, indent=1)}"


def _subset(generated, model_id, tmp_path):
    """One generated variant per operator, plus a renamed cell and a factored cell element."""
    root, pristine, records = generated[model_id]
    chosen = {}
    for r in records:
        chosen.setdefault(r.operator, (r.variant_id, _variant_ws(root, pristine, r), r.model_overrides))
    for op_name, pick in (("rename_identifier", lambda s: s.params["kind"] == "cell"),
                          ("factor_file", lambda s: s.params["element"] in ("cell", "ionChannelHH"))):
        op = REGISTRY[op_name]
        site = next(s for s in op.sites(pristine) if pick(s))
        ws = materialize(pristine.model, tmp_path / f"explicit_{op_name}")
        _, _, overrides = op.apply(ws, site)
        chosen[f"{op_name}:{site.params.get('kind', site.params.get('element'))}"] = (op.describe(site), ws, overrides)
    return pristine, chosen


@pytest.mark.parametrize("model_id", MODELS)
def test_probe_traces_match_reference(sim, generated, models, model_id, tmp_path, request):
    pristine, chosen = _subset(generated, model_id, tmp_path)
    ref_ws = materialize(pristine.model, tmp_path / "reference")
    ref = _probe(sim, ref_ws, PROBE_AMPLITUDE_NA[model_id])
    # the depolarising column must actually spike, otherwise the comparison is uninformative
    assert (ref[:, 1] * 1e3).max() > 0.0
    report = {}
    for label, (desc, ws, overrides) in chosen.items():
        if overrides:
            assert overrides == {"cell_id": ws.model.cell_id + "_renamed"}
        var = _probe(sim, apply_model_overrides(ws, overrides), PROBE_AMPLITUDE_NA[model_id])
        report[label] = {"variant": desc, **_compare(ref, var)}
    request.node.user_properties.append(("probe_trace_differences", report))
    (tmp_path / "probe_report.json").write_text(json.dumps(report, indent=1))
    print(f"\n{model_id} probe max |dV| (mV): " + json.dumps({k: v["max_abs_diff_mV"] for k, v in report.items()}))
    for label, r in report.items():
        assert r["max_abs_diff_mV"] <= TRACE_TOL_MV, f"{model_id} {label}: {r}"
