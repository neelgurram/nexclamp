"""Feature extraction: eFEL adapter, firing-regime labels and trace-level metrics."""

from neuraxis.features.efel_adapter import (
    DEFINED,
    NOT_APPLICABLE,
    UNDEFINED,
    FeatureConfigError,
    FeatureTable,
    FeatureValue,
    efel_settings,
    extract,
    extract_all,
    feature_table_from_json,
    feature_table_to_json,
)
from neuraxis.features.regimes import LABELS as REGIME_LABELS
from neuraxis.features.regimes import firing_regime
from neuraxis.features.trace_metrics import (
    align,
    decimate,
    is_uniform,
    max_abs_diff,
    pack_traces,
    resample,
    rmse,
    spike_times,
    stored_representation,
    uniform_grid,
    unpack_traces,
)

__all__ = [
    "DEFINED", "NOT_APPLICABLE", "UNDEFINED", "FeatureConfigError", "FeatureTable", "FeatureValue", "REGIME_LABELS",
    "align", "decimate", "efel_settings", "extract", "extract_all", "feature_table_from_json", "feature_table_to_json",
    "firing_regime", "is_uniform", "max_abs_diff", "pack_traces", "resample", "rmse", "spike_times",
    "stored_representation", "uniform_grid", "unpack_traces",
]
