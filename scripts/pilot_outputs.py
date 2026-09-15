"""Build the prespecified pilot outputs for a finished campaign (docs/PILOT_PROTOCOL_V1.md).

Run with the same config directory as the campaign, for example::

    NEUROSEM_CONFIG_DIR=configs/pilot_protocol_v1 python scripts/pilot_outputs.py --campaign pilot-v2
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neurosem import config  # noqa: E402
from neurosem.experiments.pilot_outputs import build_outputs  # noqa: E402
from neurosem.provenance import REPO_ROOT  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--deviations", default="docs/pilot/PILOT_PROTOCOL_V1_DEVIATIONS.md")
    a = ap.parse_args(argv)
    cfg = config.study()
    results, work = config.results_dir(cfg), config.work_dir(cfg)
    processed = results / "processed" / a.campaign
    md_file = processed / "STUDY_METADATA.json"
    meta = json.loads(md_file.read_text(encoding="utf-8")) if md_file.is_file() else config.study_metadata(cfg)
    meta = {k: meta[k] for k in config.STUDY_METADATA_KEYS if k in meta}
    pilot = cfg.get("pilot") or {}
    out = build_outputs(processed, results / "raw" / a.campaign, work / "variants" / a.campaign,
                        work / "runs" / a.campaign, results / "figures" / a.campaign,
                        pilot.get("repeated_models") or [], pilot.get("new_models") or [], meta,
                        REPO_ROOT / a.deviations)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
