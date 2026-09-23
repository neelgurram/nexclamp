"""Validation of the ion-channel kinetics operators on development fixtures (DECISIONS D-037, D-042).

For every kinetics operator and every site on each fixture this records:
- the exact edited elements and attributes (old -> new), and whether the change is **atomic**
  (one attribute of one element) or **compound** (several attributes that together form one
  documented change of one gate);
- that nothing else changed (single-operator enforcement: no other file, element or attribute;
  no execution override; the shipped simulation file byte-identical);
- schema validation and simulation of the mutant, with a before/after voltage comparison and a
  before/after plot that a person can inspect.

It writes only under ``--out`` and never touches study campaigns. The output is operator-correctness
evidence, not detection data.
"""

from __future__ import annotations

import dataclasses as dc
import json
import shutil
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

from nexclamp.models import Workspace, copy_workspace, load_models, materialize
from nexclamp.provenance import REPO_ROOT, sha256_file, utc_now
from nexclamp.schemas import ModelRecord, RunStatus, VariantKind, VariantRecord

KINETICS_OPERATORS = ("shift_gate_midpoint", "scale_gate_slope", "shift_forward_rate_midpoint", "shift_channel_vshift")
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "kinetics_fixture"
EQUATIONS = {
    "HHExpRate": "r(V) = rate * exp((V - midpoint) / scale)",
    "HHSigmoidRate": "r(V) = rate / (1 + exp((midpoint - V) / scale))",
    "HHExpLinearRate": "r(V) = rate * x / (1 - exp(-x)), x = (V - midpoint) / scale",
    "HHSigmoidVariable": "x_inf(V) = rate / (1 + exp((midpoint - V) / scale))",
    "HHExpVariable": "x_inf(V) = rate * exp((V - midpoint) / scale)",
    "HHExpLinearVariable": "x_inf(V) = rate * x / (1 - exp(-x)), x = (V - midpoint) / scale",
    "channelDensityVShift": "vShift is passed to the channel; only gates whose own definitions read vShift use it "
                            "(NeuroML core ionChannelVShift: 'The exact usage of vShift ... is determined by the "
                            "individual gates'); core HH rate types do not read it",
}


def fixture_model() -> ModelRecord:
    return ModelRecord(model_id="kinetics_fixture", name="Neuraxis kinetics validation fixture (HH-type, test only)",
                       snapshot="kinetics_fixture", cell_file="KinFix.cell.nml", cell_id="kinfix",
                       harness_lems="LEMS_KinFix.xml", harness_output_file="kinfix_v.dat", harness_v_column="1",
                       temperature="6.3 degC", source_family="neuraxis_test_fixture", citation="Neuraxis test fixture",
                       source_url="tests/fixtures/kinetics_fixture", commit="in-repository", license="Apache-2.0",
                       license_url="LICENSE", download_date="", simulator="jNeuroML",
                       expected_behavior="tonic HH-type spiking", inclusion="test_fixture_only",
                       inclusion_reason="sacrificial fixture for operator correctness; never a study model")


def fixture_workspace(dest: Path) -> Workspace:
    shutil.copytree(FIXTURE_DIR, dest)
    return Workspace(dest, fixture_model())


def atomicity(edits: Sequence[Any]) -> str:
    if len(edits) == 1:
        return "atomic (one attribute of one element)"
    return f"compound ({len(edits)} attributes of one gate, one documented change)"


def _element_types(ws: Workspace, edits: Sequence[Any]) -> list[str]:
    from nexclamp.mutations.base import localname, read_xml, resolve

    out = []
    for e in edits:
        el = resolve(read_xml(ws.path(e.file)).root, e.locator)
        out.append(el.get("type") or localname(el))
    return out


def validate_fixtures(out_dir: Path, fixtures: Sequence[tuple[str, Workspace]], max_sites: int = 16) -> dict:
    from matplotlib.figure import Figure

    from nexclamp.mutations import REGISTRY
    from nexclamp.mutations.base import enforce_single_operator
    from nexclamp.protocols.definitions import CANONICAL_ID
    from nexclamp.simulators.jneuroml import JNeuroML
    from nexclamp.validation import structural
    from nexclamp.validation.canonical import canonical_protocol
    from nexclamp.validation.execution import RunRecorder
    from nexclamp.validation.trace_regression import spikes

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sim = JNeuroML()
    rows: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="neuraxis_kinval_") as tmp:
        rec = RunRecorder("kinetics_validation", sim, results_root=out_dir, work_root=Path(tmp) / "work")
        for label, ref in fixtures:
            tree = ref.tree_sha256()
            refvar = VariantRecord(f"{label}__reference", ref.model.model_id, VariantKind.REFERENCE,
                                   tree_sha256=tree, parent_tree_sha256=tree)
            proto = canonical_protocol(ref)
            base = rec.run_canonical(ref, refvar, proto, need_traces=True)
            ref_tr = base.traces.get(CANONICAL_ID)
            harness_sha = sha256_file(ref.harness_path)
            for name in KINETICS_OPERATORS:
                op = REGISTRY[name]
                sites = op.sites(ref)
                inapplicable = [dc.asdict(i) for i in op.inapplicable(ref)] if hasattr(op, "inapplicable") else []
                if not sites:
                    rows.append({"fixture": label, "operator": name, "site": None, "status": "no_site",
                                 "inapplicable": inapplicable[:6]})
                    continue
                for i, site in enumerate(sites[:max_sites]):
                    var = copy_workspace(ref, Path(tmp) / label / f"{name}_{i}")
                    edits, exec_o, model_o = op.apply(var, site)
                    record = VariantRecord(f"{label}-{name}-{i}", ref.model.model_id, VariantKind.MUTANT,
                                           op.family.value, name, dict(site.params), edits, exec_o, model_o,
                                           tree_sha256=var.tree_sha256(), parent_tree_sha256=tree)
                    row = {"fixture": label, "operator": name, "site": i, "params": site.params,
                           "atomicity": atomicity(edits),
                           "edits": [{"file": e.file, "locator": e.locator, "attribute": e.attribute, "old": e.old,
                                      "new": e.new} for e in edits],
                           "element_types": _element_types(ref, edits),
                           "affected_equations": sorted({EQUATIONS.get(t, t) for t in _element_types(ref, edits)}),
                           "exec_overrides": exec_o, "harness_unchanged": sha256_file(var.harness_path) == harness_sha}
                    try:
                        enforce_single_operator(ref, var, record)
                        row["single_change_enforced"] = True
                    except Exception as exc:  # recorded: this is the check being reported
                        row["single_change_enforced"] = f"FAILED: {exc}"
                    st = structural.check(var, sim, reference=structural.check(ref, sim))
                    row["schema_valid"] = st.valid
                    after = rec.run_canonical(var, record, proto, need_traces=True)
                    row["simulation_status"] = after.status.value
                    tr = after.traces.get(CANONICAL_ID)
                    if ref_tr is not None and tr is not None:
                        n = min(len(ref_tr.v_mV), len(tr.v_mV))
                        row["max_abs_dv_mV"] = float(np.max(np.abs(np.asarray(ref_tr.v_mV[:n]) - np.asarray(tr.v_mV[:n]))))
                        row["spikes_before_after"] = [int(spikes(ref_tr).size), int(spikes(tr).size)]
                        fig = Figure(figsize=(7, 2.6))
                        ax = fig.subplots()
                        ax.plot(ref_tr.t_ms, ref_tr.v_mV, color="#000000", lw=0.7, label="before")
                        ax.plot(tr.t_ms, tr.v_mV, color="#E69F00", lw=0.7, ls="--", label="after")
                        ax.set_xlabel("t (ms)", fontsize=7)
                        ax.set_ylabel("V (mV)", fontsize=7)
                        ax.legend(fontsize=6)
                        ax.set_title(f"{label}: {name} {site.params}", fontsize=7)
                        fig.text(0.005, 0.005, "operator-correctness evidence on a development fixture; not study data",
                                 fontsize=5, color="#555555")
                        fig.tight_layout()
                        png = out_dir / "plots" / f"{label}_{name}_{i}.png"
                        png.parent.mkdir(parents=True, exist_ok=True)
                        fig.savefig(png, dpi=130)
                        row["plot"] = png.relative_to(out_dir).as_posix()
                    row["passed"] = (row["single_change_enforced"] is True and row["harness_unchanged"]
                                     and not exec_o and row["simulation_status"] == RunStatus.OK.value
                                     and row["schema_valid"] is True)
                    rows.append(row)
    report = {"created_utc": utc_now(), "operators": list(KINETICS_OPERATORS), "rows": rows,
              "all_sites_passed": all(r.get("passed", True) for r in rows if r.get("site") is not None)}
    (out_dir / "kinetics_validation.json").write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    return report


def default_fixtures(tmp: Path) -> list[tuple[str, Workspace]]:
    """The synthetic HH-type fixture (core gates) and Pospischil RS (vShift; a Pilot 1 development model)."""
    return [("kinetics_fixture", fixture_workspace(tmp / "kinetics_fixture")),
            ("pospischil2008_rs", materialize(load_models()["pospischil2008_rs"], tmp / "rs"))]
