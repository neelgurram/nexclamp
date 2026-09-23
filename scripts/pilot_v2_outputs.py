"""Build the prespecified Pilot 2 outputs and branch classification (docs/PILOT2_PROTOCOL.md).

    NEURAXIS_CONFIG_DIR=configs/pilot_protocol_v2 python scripts/pilot_v2_outputs.py --campaign pilot2-v2
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nexclamp import config  # noqa: E402
from nexclamp.experiments.pilot_v2_outputs import build  # noqa: E402
from nexclamp.provenance import REPO_ROOT  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--deviations", default="docs/pilot/PILOT2_PROTOCOL_DEVIATIONS.md")
    a = ap.parse_args(argv)
    cfg = config.study()
    results, work = config.results_dir(cfg), config.work_dir(cfg)
    processed = results / "processed" / a.campaign
    md_file = processed / "STUDY_METADATA.json"
    meta = json.loads(md_file.read_text(encoding="utf-8")) if md_file.is_file() else config.study_metadata(cfg)
    meta = {k: meta[k] for k in config.STUDY_METADATA_KEYS if k in meta}
    out = build(processed, results / "raw" / a.campaign, work / "variants" / a.campaign, work / "runs" / a.campaign,
                results / "figures" / a.campaign, meta, int(cfg["selection"]["seed"]), REPO_ROOT / a.deviations)
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    print(out)
    print(json.dumps(summary["branch"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
