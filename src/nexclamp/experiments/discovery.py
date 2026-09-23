"""Protocol selection on the discovery split only (Milestone 7).

Leakage barrier: the detection matrix is filtered through ``selection.splits.DiscoveryView``,
which reads only discovery split files and raises if a non-discovery model appears.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from nexclamp import config
from nexclamp.protocols.definitions import CANONICAL_ID
from nexclamp.provenance import REPO_ROOT, sha256_file, utc_now


def select_protocols(campaign: str, budget_k: int | None = None, draws: int | None = None, seed: int | None = None) -> Path:
    from nexclamp.selection import greedy, splits
    from nexclamp.selection.matrix import DetectionMatrix

    cfg = config.study()
    k = int(budget_k or cfg["selection"]["budget_k"])
    draws = int(draws or cfg["selection"]["random_draws"])
    seed = int(seed if seed is not None else cfg["selection"]["seed"])
    processed = config.results_dir(cfg) / "processed" / campaign
    matrix_path = processed / "detection_matrix.csv"
    view = splits.discovery_view(REPO_ROOT)
    from nexclamp.experiments.strata import SELECTION_EXCLUDED_FAMILIES

    # Drop the families held back from selection BEFORE the discovery gate runs. Those rows are
    # held-out by family, so the gate rightly rejects them - but the next line removes them anyway,
    # and raising first would make selection impossible whenever the excluded family is also the
    # held-out family (which is the whole point of holding it back). The gate still guards what
    # remains: every surviving row must be a discovery row.
    raw = DetectionMatrix.from_csv(matrix_path)
    keep = [i for i, mid in enumerate(raw.mutant_ids) if raw.family_of[mid] not in SELECTION_EXCLUDED_FAMILIES]
    full = raw.take_rows(keep)
    m = view.filter_matrix(full)
    candidates = [p for p in m.protocol_ids if p != CANONICAL_ID]
    sel = greedy.greedy_max_coverage(m, k, candidates)
    budget = float(sum(m.cost[p] for p in sel.protocols))
    rc = greedy.random_count_matched(m, len(sel.protocols), draws, seed, candidates)
    rr = greedy.random_runtime_matched(m, budget, draws, seed + 1, candidates)
    result = {
        "campaign": campaign, "created_utc": utc_now(), "budget_k": k, "seed": seed, "draws": draws,
        "detection_matrix": matrix_path.relative_to(REPO_ROOT).as_posix(), "detection_matrix_sha256": sha256_file(matrix_path),
        "n_discovery_mutants": len(m.mutant_ids), "n_excluded_from_selection": raw.n_mutants - full.n_mutants,
        "families_excluded_from_selection": sorted(SELECTION_EXCLUDED_FAMILIES), "discovery_models": list(view.models),
        "selected_protocols": sel.protocols, "coverage_curve": sel.coverage_curve, "selected_cost_cell_steps": budget,
        "rates": {"selected": m.rate(sel.protocols), "canonical": m.rate([CANONICAL_ID]) if CANONICAL_ID in m.protocol_ids else None,
                  "exhaustive": m.rate(m.protocol_ids)},
        "random_count_matched": _dist(rc), "random_runtime_matched": _dist(rr),
        "note": "Discovery-set rates are in-sample and optimistic by construction (the selection saw these mutants; the "
                "exhaustive battery defines admissibility). Only held-out evaluation tests generalisation.",
    }
    out = processed / f"selection_k{k}.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return out


def _dist(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    return {"mean": float(x.mean()), "sd": float(x.std(ddof=1)) if x.size > 1 else 0.0,
            "p05": float(np.quantile(x, 0.05)), "p50": float(np.quantile(x, 0.5)), "p95": float(np.quantile(x, 0.95)),
            "n": int(x.size)}
