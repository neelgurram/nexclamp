"""Protocol selection on discovery data (specification: "Protocol selection", "Leakage controls").

Only discovery-side names are re-exported here. The gate to evaluation-only split data
lives in :mod:`neurosem.selection.splits` and must be imported from there explicitly.
"""

from neurosem.selection.greedy import (
    Selection,
    SelectionSettings,
    count_matched_sets,
    greedy_cost_sensitive,
    greedy_max_coverage,
    random_count_matched,
    random_runtime_matched,
    runtime_matched_sets,
    selection_settings,
)
from neurosem.selection.matrix import DetectionMatrix, cell_step_costs
from neurosem.selection.splits import (
    DiscoveryView,
    LeakageError,
    SplitIntegrityError,
    discovery_view,
    verify_split_hashes,
)

__all__ = [
    "DetectionMatrix",
    "DiscoveryView",
    "LeakageError",
    "Selection",
    "SelectionSettings",
    "SplitIntegrityError",
    "cell_step_costs",
    "count_matched_sets",
    "discovery_view",
    "greedy_cost_sensitive",
    "greedy_max_coverage",
    "random_count_matched",
    "random_runtime_matched",
    "runtime_matched_sets",
    "selection_settings",
    "verify_split_hashes",
]
