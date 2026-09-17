"""Generate ``data/protocol_manifest.csv`` from the protocol templates.

The manifest is a *derived* file: the single source of truth is the template catalogue in
``src/neuraxis/protocols/definitions.py`` as overridden by ``configs/study.yaml``. Writing
it out as a table lets reviewers (and the preregistration) see exactly which candidate
protocols exist without reading code, and ``--check`` lets tests fail when someone edits a
template but forgets to regenerate the table.

Columns (docs/ARCHITECTURE.md section 2):
``protocol_id,kind,description,params_json,features,implemented,not_implemented_reason``

Encoding choices:
- ``params_json`` is compact JSON with sorted keys, so the same parameters always give the
  same bytes (stable diffs and hashes).
- ``features`` is the template's feature tuple joined with ``;`` in template order.
- ``implemented`` is ``true`` or ``false``.

Usage::

    python scripts/build_protocol_manifest.py            # (re)write data/protocol_manifest.csv
    python scripts/build_protocol_manifest.py --check    # exit 1 if the file is missing or stale
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from neuraxis import config
from neuraxis.protocols.definitions import ProtocolTemplate, templates_from_config
from neuraxis.provenance import REPO_ROOT

COLUMNS = ("protocol_id", "kind", "description", "params_json", "features", "implemented",
           "not_implemented_reason")
DEFAULT_OUTPUT = REPO_ROOT / "data" / "protocol_manifest.csv"
FEATURE_SEP = ";"
# Kinds that code can run: the batched kinds handled by ProtocolTemplate.instantiate in
# src/neuraxis/protocols/definitions.py, plus the rheobase search (protocols/rheobase.py).
IMPLEMENTED_KINDS = frozenset({"baseline", "step", "ramp", "rebound", "short_pulse", "paired_pulse", "rheobase"})


def template_row(t: ProtocolTemplate) -> dict[str, str]:
    """One manifest row for one template."""
    params: dict[str, Any] = dict(t.params)
    return {
        "protocol_id": t.protocol_id,
        "kind": t.kind,
        "description": t.description,
        "params_json": json.dumps(params, sort_keys=True, separators=(",", ":")),
        "features": FEATURE_SEP.join(t.features),
        "implemented": "true" if t.implemented else "false",
        "not_implemented_reason": t.not_implemented_reason,
    }


def validate_template(t: ProtocolTemplate) -> None:
    """Reject templates that would give a misleading manifest row.

    An id in ``configs/study.yaml`` that is not in the default catalogue and has no ``kind``
    would otherwise appear as an "implemented" candidate that no code can run. Since the
    manifest is what the preregistration freezes as the candidate list, it must fail loudly
    instead.
    """
    if not t.protocol_id:
        raise ValueError("template with empty protocol_id")
    if t.implemented:
        if t.kind not in IMPLEMENTED_KINDS:
            raise ValueError(f"{t.protocol_id}: kind {t.kind!r} is not an implemented protocol kind "
                             f"{sorted(IMPLEMENTED_KINDS)}")
        if not t.features:
            raise ValueError(f"{t.protocol_id}: implemented template has no features")
        if not t.description:
            raise ValueError(f"{t.protocol_id}: implemented template has no description")
    elif not t.not_implemented_reason.strip():
        raise ValueError(f"{t.protocol_id}: not-implemented template needs a not_implemented_reason")


def build_rows(templates: Sequence[ProtocolTemplate]) -> list[dict[str, str]]:
    ids = [t.protocol_id for t in templates]
    if len(set(ids)) != len(ids):
        raise ValueError(f"duplicate protocol ids in templates: {ids}")
    for t in templates:
        validate_template(t)
    return [template_row(t) for t in templates]


def render_csv(rows: Sequence[dict[str, str]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(COLUMNS), lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def parse_csv(text: str) -> list[dict[str, str]]:
    """Read a manifest back (used by tests and by anyone consuming the file)."""
    return list(csv.DictReader(io.StringIO(text)))


def load_templates(study_path: Path | None = None) -> tuple[ProtocolTemplate, ...]:
    """Templates from ``study_path`` (default ``configs/study.yaml``).

    A relative ``study_path`` is resolved against the current working directory, as a
    command-line user expects. ``config.load_yaml`` on its own would resolve it under
    ``configs/``.
    """
    cfg = config.load_yaml(Path(study_path).resolve()) if study_path else config.study()
    return templates_from_config(cfg.get("protocols"))


def manifest_text(study_path: Path | None = None) -> str:
    return render_csv(build_rows(load_templates(study_path)))


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="manifest path to write or check")
    ap.add_argument("--study", type=Path, default=None,
                    help="study config; relative paths are taken from the current directory "
                         "(default configs/study.yaml)")
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if the file differs")
    args = ap.parse_args(argv)

    text = manifest_text(args.study)
    out: Path = args.output
    if args.check:
        current = out.read_text(encoding="utf-8") if out.is_file() else None
        if current != text:
            print(f"STALE: {out} does not match the templates; run scripts/build_protocol_manifest.py")
            return 1
        print(f"OK: {out} matches the templates ({len(parse_csv(text))} protocols)")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    rows = parse_csv(text)
    n_impl = sum(r["implemented"] == "true" for r in rows)
    print(f"wrote {out}: {len(rows)} protocols ({n_impl} implemented, {len(rows) - n_impl} deferred)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
