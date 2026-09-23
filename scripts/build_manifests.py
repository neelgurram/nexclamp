"""Build the execution plan's ``manifests/`` tables and ``docs/LICENSING_MATRIX.md`` from code and data.

Writes (all regenerable; nothing here is a result):
- ``manifests/protocols.csv``: every protocol template, with its role (calibration, detection, comparator);
- ``manifests/mutations.csv``: every mutation operator, family, analysis stratum and taxonomy class;
- ``manifests/transformations.csv``: every valid-transformation and no-change operator;
- ``manifests/development_split.csv``: the provisional development (discovery) assignment;
- ``manifests/heldout_split.csv``: header only while no held-out assignment exists;
- ``manifests/model_sources.csv`` and ``docs/LICENSING_MATRIX.md``: provenance and reuse rights of every
  known upstream model;
- ``manifests/hashes/<snapshot>.sha256``: per-file SHA-256 of every stored model snapshot.

``manifests/models.csv`` is written by ``nexclamp curate-models``.

    python scripts/build_manifests.py
"""

from __future__ import annotations

import csv
import inspect
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp.experiments import strata  # noqa: E402
from nexclamp.models import CANDIDATE_MODELS, RAW_MODELS  # noqa: E402
from nexclamp.protocols.definitions import CANONICAL_ID, DEFAULT_TEMPLATES  # noqa: E402
from nexclamp.provenance import REPO_ROOT, sha256_file, tree_sha256, utc_now  # noqa: E402

OUT = REPO_ROOT / "manifests"
SOURCES = ("data/model_manifest.csv", "data/model_candidates.csv", "data/model_candidates_sweep2.csv")
TAXONOMY = {  # D-037 prospective taxonomy of model mutations
    "scale_conductance": "1_static_membrane_biophysical", "scale_capacitance": "1_static_membrane_biophysical",
    "shift_reversal": "1_static_membrane_biophysical", "shift_initial_voltage": "1_static_membrane_biophysical",
    "wrong_segment_group": "1_static_membrane_biophysical",
    "scale_gate_time_constant": "1_static_membrane_biophysical (kinetic parameter; used in Pilot 1, so kept out of the "
                                "held-out kinetics family)",
    "shift_gate_midpoint": "2_ion_channel_kinetics", "scale_gate_slope": "2_ion_channel_kinetics",
    "shift_forward_rate_midpoint": "2_ion_channel_kinetics", "shift_channel_vshift": "2_ion_channel_kinetics",
    "wrong_channel": "3_reference_mechanism_composition", "wrong_compatible_component": "3_reference_mechanism_composition",
    "omit_include": "3_reference_mechanism_composition", "duplicate_conductance": "3_reference_mechanism_composition",
}
PERMISSIVE = ("MIT", "BSD", "Apache", "CC-BY", "CC0", "ISC")
COPYLEFT = ("LGPL", "GPL")
DEPENDENCIES = [  # from LICENSE_AUDIT.md sections 3-5 (not legal advice)
    ("pyNeuroML 1.3.22", "LGPL-3.0-only", "used unmodified; installed by pip"),
    ("jNeuroML 0.14.0 jar (bundles jLEMS 0.12.0 and org.neuroml.export 1.11.0)", "LGPL-3.0", "used unmodified; bundled in pyNeuroML"),
    ("libNeuroML 0.6.7", "BSD (2- vs 3-clause unresolved, L-09)", "used unmodified"),
    ("eFEL 5.7.34", "LGPL-3.0", "used unmodified"),
    ("NumPy, SciPy, pandas, lxml", "BSD-3-Clause family", "used unmodified"),
    ("matplotlib", "matplotlib license (PSF-based)", "used unmodified"),
    ("Eclipse Temurin JDK 21.0.12.1+1", "GPL-2.0 with Classpath Exception", "local tool; not redistributed (L-07)"),
]


def write_csv(path: Path, rows: list[dict], header: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = header or (list(dict.fromkeys(k for r in rows for k in r)) if rows else ["empty"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


DESCRIPTIONS = {  # for operator classes without their own docstring
    "scale_conductance": "Multiply the conductance density of one channel density by a factor.",
    "scale_capacitance": "Multiply the specific membrane capacitance by a factor.",
    "shift_reversal": "Shift the reversal potential of one channel density.",
    "shift_initial_voltage": "Shift the cell's initial membrane potential.",
    "shift_gate_midpoint": "Shift one gate's voltage dependence (core rate/steady-state midpoints) by d mV.",
    "scale_gate_slope": "Multiply one gate's voltage-dependence scale (slope) by k.",
    "shift_forward_rate_midpoint": "Shift only the forward (opening) rate midpoint of one rate gate by d mV.",
    "increase_dt": "Multiply the integration time step of every run (harness and battery) by a factor.",
    "solver_config": "Request another LEMS integration method through <Meta>.",
    "omit_include": "Remove one <include> from the model.",
    "wrong_channel": "Point one channel density at a different existing ion channel.",
    "wrong_compatible_component": "Replace one component reference with another component of a compatible type.",
    "sim_length": "Change the shipped harness simulation length.",
    "stim_amplitude": "Change the amplitude of the shipped harness stimulus.",
    "stim_duration": "Change the duration of the shipped harness stimulus.",
    "stim_onset": "Change the onset (delay) of the shipped harness stimulus.",
}


def doc(cls, name: str = "") -> str:
    """First line of a class's own docstring (never an inherited one), else a fixed description."""
    own = cls.__dict__.get("__doc__")
    return inspect.cleandoc(own).split("\n")[0] if own else DESCRIPTIONS.get(name, "")


def protocols() -> list[dict]:
    rows = [{"protocol_id": CANONICAL_ID, "role": "comparator (canonical regression test)", "kind": "shipped_harness",
             "description": "the simulation shipped with each model, run unchanged", "params": "{}", "features": "",
             "implemented": True, "not_implemented_reason": ""},
            {"protocol_id": "REF_RHEOBASE_CALIBRATION", "role": "calibration procedure", "kind": "rheobase_search",
             "description": "rheobase search on the reference model; sets every stimulus amplitude",
             "params": json.dumps({"see": "configs/study.yaml rheobase"}), "features": "", "implemented": True,
             "not_implemented_reason": ""}]
    for t in DEFAULT_TEMPLATES:
        rows.append({"protocol_id": t.protocol_id,
                     "role": "detection measurement" if t.kind == "rheobase" else "detection protocol",
                     "kind": t.kind, "description": t.description, "params": json.dumps(dict(t.params), sort_keys=True),
                     "features": ";".join(t.features), "implemented": t.implemented,
                     "not_implemented_reason": t.not_implemented_reason})
    return rows


def mutations() -> list[dict]:
    from nexclamp.mutations import REGISTRY

    rows = []
    for name, op in sorted(REGISTRY.items(), key=lambda kv: (kv[1].family.value, kv[0])):
        fam = op.family.value
        rows.append({"operator": name, "family": fam, "analysis_stratum": strata.stratum("mutant", fam, name),
                     "taxonomy_class": TAXONOMY.get(name, "numerical_robustness" if fam == "numerical"
                                                    else "harness_stimulus" if fam == "stimulus" else ""),
                     "excluded_from_protocol_selection": fam in strata.SELECTION_EXCLUDED_FAMILIES,
                     "exec_override_keys": ";".join(sorted(op.exec_override_keys)), "description": doc(type(op), name),
                     "module": type(op).__module__})
    return rows


def transformations() -> list[dict]:
    from nexclamp import transforms

    return [{"operator": name, "kind": getattr(getattr(op, "kind", ""), "value", getattr(op, "kind", "")),
             "description": doc(type(op), name), "module": type(op).__module__}
            for name, op in sorted(transforms.REGISTRY.items())]


def splits() -> tuple[list[dict], list[str]]:
    base = REPO_ROOT / "data" / "splits"
    rows = []
    for kind, fname in (("model", "discovery_models.txt"), ("mutation_family", "discovery_families.txt")):
        f = base / fname
        for line in (f.read_text(encoding="utf-8").splitlines() if f.is_file() else []):
            line = line.strip()
            if line and not line.startswith("#"):
                rows.append({"item_type": kind, "item_id": line, "split": "development", "status": "provisional, not frozen",
                             "source_file": f"data/splits/{fname}"})
    return rows, ["item_type", "item_id", "split", "status", "source_file"]


def redistribution(licence: str) -> tuple[str, str]:
    lic = licence or ""
    if not lic or "unclear" in lic.lower():
        return "unclear: do not bundle; publish a downloader, source URL and expected hash", "unknown"
    if any(k in lic for k in COPYLEFT):
        return "permitted under the same licence (keep notices; mark changes; ship licence texts)", "licence notice"
    if any(k in lic for k in PERMISSIVE):
        note = " (citation condition applies to some upstream folders)" if "citation" in lic.lower() else ""
        return "permitted with licence notice" + note, "copyright and licence notice; cite the source publication"
    return "review needed", "review needed"


def model_sources() -> list[dict]:
    rows, seen = [], set()
    for src in SOURCES:
        path = REPO_ROOT / src
        if not path.is_file():
            continue
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["model_id"] in seen:
                    continue
                seen.add(r["model_id"])
                snap = r.get("snapshot", "")
                root = next((d / snap for d in (RAW_MODELS, CANDIDATE_MODELS) if snap and (d / snap).is_dir()), None)
                redis, attrib = redistribution(r.get("license", ""))
                files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "PROVENANCE.json") if root else []
                rows.append({
                    "model_id": r["model_id"], "title": r.get("name", ""), "source_publication": r.get("citation", ""),
                    "doi": r.get("doi", ""), "url": r.get("source_url", ""), "download_date": r.get("download_date", ""),
                    "commit": r.get("commit", ""), "snapshot": snap,
                    "snapshot_location": root.relative_to(REPO_ROOT).as_posix() if root else "not downloaded",
                    "snapshot_tree_sha256": tree_sha256(root) if root else "", "n_files": len(files),
                    "license": r.get("license", ""), "license_url": r.get("license_url", ""),
                    "redistribution": r.get("redistribution") or redis, "attribution": r.get("attribution") or attrib,
                    "dependencies": r.get("dependencies", "") or ";".join(
                        p.relative_to(root).as_posix() for p in files if p.suffix in (".nml", ".xml")
                        and p.relative_to(root).as_posix() not in (r.get("cell_file"), r.get("harness_lems"))),
                    "manifest": src, "inclusion": r.get("inclusion", "")})
    return rows


def snapshot_hashes() -> int:
    n = 0
    for base in (RAW_MODELS, CANDIDATE_MODELS):
        for snap in sorted(p for p in base.glob("*") if p.is_dir()):
            files = sorted(p for p in snap.rglob("*") if p.is_file())
            out = OUT / "hashes" / f"{snap.name}.sha256"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text("".join(f"{sha256_file(p)}  {p.relative_to(REPO_ROOT).as_posix()}\n" for p in files),
                           encoding="utf-8", newline="\n")
            n += 1
    return n


def licensing_doc(rows: list[dict]) -> str:
    lines = ["# Licensing matrix", "",
             f"*Generated by `scripts/build_manifests.py` on {utc_now()} from the model manifests and snapshot "
             "provenance. Not legal advice; a qualified human review is required before release (LICENSE_AUDIT.md "
             "L-11).*", "",
             "## In plain English", "",
             "- Neuraxis's own code is provisionally licensed Apache-2.0 (execution plan). Upstream model files keep "
             "their own licences and are never relicensed.",
             "- Models with an unclear licence are never bundled: a release ships a downloader, the source URL and the "
             "expected hash instead.",
             "- Copyleft (LGPL) model files may be redistributed only under their own licence, with notices.", "",
             "## Neuraxis code and documentation", "",
             "| item | licence | status |", "|---|---|---|",
             "| Neuraxis source code (`src/`, `scripts/`, `workflows/`, `tests/`) | Apache-2.0 (`LICENSE`) | provisional, "
             "subject to compatibility review; replaced BSD-3-Clause (kept in `docs/licensing/`) |",
             "| Documentation | not yet chosen (L-02 recommends CC-BY-4.0) | decision pending |",
             "| Generated data (traces, features, tables) | not yet chosen (L-03) | decision pending |", "",
             "## Dependencies", "", "| dependency | licence | use |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {c} |" for a, b, c in DEPENDENCIES]
    lines += ["", "## Upstream models", "",
              "| model | source publication | URL @ commit | downloaded | snapshot tree SHA-256 | licence | "
              "redistribution | attribution | dependencies |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        deps = r["dependencies"].split(";") if r["dependencies"] else []
        lines.append(f"| `{r['model_id']}` {r['title']} | {r['source_publication'][:120]} | {r['url']} @ "
                     f"`{r['commit'][:12]}` | {r['download_date']} | "
                     f"{('`' + r['snapshot_tree_sha256'][:16] + '…`') if r['snapshot_tree_sha256'] else r['snapshot_location']} | "
                     f"[{r['license']}]({r['license_url']}) | {r['redistribution']} | {r['attribution']} | "
                     f"{len(deps)} files |")
    lines += ["", "Per-file hashes: `manifests/hashes/<snapshot>.sha256`. Full table: `manifests/model_sources.csv`.", ""]
    return "\n".join(lines)


def main() -> int:
    write_csv(OUT / "protocols.csv", protocols())
    write_csv(OUT / "mutations.csv", mutations())
    write_csv(OUT / "transformations.csv", transformations())
    dev, header = splits()
    write_csv(OUT / "development_split.csv", dev, header)
    heldout = REPO_ROOT / "data" / "splits" / "heldout"
    if not any(p.suffix == ".txt" for p in heldout.glob("*")):
        write_csv(OUT / "heldout_split.csv", [], header)      # header only: nothing assigned
    rows = model_sources()
    write_csv(OUT / "model_sources.csv", rows)
    (REPO_ROOT / "docs" / "LICENSING_MATRIX.md").write_text(licensing_doc(rows), encoding="utf-8")
    n = snapshot_hashes()
    (OUT / "README.md").write_text(
        "# Manifests\n\nGenerated by `scripts/build_manifests.py` (and `nexclamp curate-models` for `models.csv`). "
        "`heldout_split.csv` is header-only until Neel assigns the held-out split; `hashes/` holds per-file SHA-256 of "
        "every stored model snapshot. `pilot_pre_run_*` files belong to PILOT_PROTOCOL_V1.\n", encoding="utf-8")
    print(f"protocols {len(protocols())}, mutations {len(mutations())}, transformations {len(transformations())}, "
          f"development items {len(dev)}, model sources {len(rows)}, snapshot hash files {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
