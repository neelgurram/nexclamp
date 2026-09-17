"""eFEL adapter: one :data:`FeatureTable` per (trace, protocol) (spec "Initial features").

Each design choice below follows from verified eFEL 5.7.34 behaviour
(docs/m0_evidence/tools/efel.research.json):

* eFEL settings are process-global, and ``set_setting`` silently accepts misspelt names.
  Names are therefore checked against the ``efel.Settings`` fields, and the settings are
  re-applied after ``efel.reset()`` before every eFEL call, under a lock.
* eFEL returns ``None`` for a feature it cannot compute. That becomes ``undefined`` and
  is never replaced by zero. Count features return ``array([0])`` when there are no
  spikes, which is a real, defined zero.
* Some features return numbers where they mean nothing: sag on a depolarising step, or a
  frequency from a single spike. NeuroSem decides applicability before asking eFEL:
  ``min_spikes`` and ``requires`` make a feature ``not_applicable``.
* Per-spike arrays are reduced explicitly (``first``/``last``). ``scalar`` insists on
  exactly one value, so a per-spike feature configured as a scalar fails loudly.
"""

from __future__ import annotations

import dataclasses as dc
import functools
import math
import threading
import warnings as _warnings
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import efel
import numpy as np

from neuraxis.features.regimes import firing_regime
from neuraxis.schemas import ConcreteProtocol, Trace

DEFINED = "defined"
UNDEFINED = "undefined"
NOT_APPLICABLE = "not_applicable"
STATES = (DEFINED, UNDEFINED, NOT_APPLICABLE)
AGGREGATIONS = ("first", "last", "scalar")
REQUIREMENTS = ("hyperpolarizing",)
KINDS = ("numeric", "count", "categorical")
NEUROSEM_FEATURES = ("firing_regime", "rheobase")
FINGERPRINT_ONLY = ("rheobase",)             # filled by validation.fingerprint, never by extract()
SPIKE_COUNT = "spike_count"
REGIME_INPUTS = ("spike_count", "burst_count", "adaptation_index")
_SPEC_KEYS = {"efel", "neurosem", "agg", "unit", "min_spikes", "requires", "kind"}
_JSON_KEYS = ("name", "value", "state", "unit", "source")

# eFEL keeps its settings in module-level state; every reset/set/extract sequence holds this lock.
_EFEL_LOCK = threading.RLock()


class FeatureConfigError(ValueError):
    """The feature configuration, or a protocol's feature list, is inconsistent."""


@dc.dataclass(frozen=True)
class FeatureValue:
    name: str
    value: float | str | None        # str only for categorical features
    state: str                       # "defined" | "undefined" | "not_applicable"
    unit: str
    source: str                      # e.g. "efel:AP_amplitude[first]" or "neurosem:firing_regime"

    def __post_init__(self) -> None:
        if self.state not in STATES:
            raise ValueError(f"{self.name}: unknown feature state {self.state!r}")
        if self.state != DEFINED:
            if self.value is not None:
                raise ValueError(f"{self.name}: a {self.state} feature carries no value")
            return
        if isinstance(self.value, str):
            return
        if self.value is None or isinstance(self.value, bool) or not isinstance(self.value, (int, float, np.number)):
            raise ValueError(f"{self.name}: a defined feature needs a number or a category, got {self.value!r}")
        value = float(self.value)
        if not math.isfinite(value):
            raise ValueError(f"{self.name}: defined values must be finite, got {value!r}")
        object.__setattr__(self, "value", value)

    @property
    def defined(self) -> bool:
        return self.state == DEFINED


FeatureTable = dict[str, FeatureValue]


@dc.dataclass(frozen=True)
class FeatureSpec:
    """One entry of ``configs/features.yaml`` after validation."""

    name: str
    efel: str | None
    neurosem: str | None
    agg: str | None
    unit: str
    min_spikes: int
    requires: str | None
    kind: str

    @property
    def source(self) -> str:
        return f"efel:{self.efel}[{self.agg}]" if self.efel else f"neurosem:{self.neurosem}"


def _data(cfg: Any) -> Mapping[str, Any]:
    data = getattr(cfg, "data", cfg)          # accepts neuraxis.config.LoadedConfig or a plain dict
    if not isinstance(data, Mapping):
        raise FeatureConfigError("feature configuration must be a mapping")
    return data


@functools.cache
def _efel_feature_names() -> frozenset[str]:
    return frozenset(efel.get_feature_names())


def _setting_types() -> dict[str, type | None]:
    by_name = {"float": float, "int": int, "bool": bool, "str": str}
    return {f.name: (f.type if isinstance(f.type, type) else by_name.get(str(f.type))) for f in dc.fields(efel.Settings)}


def efel_settings(cfg: Any) -> dict[str, float | int | bool | str]:
    """Validated eFEL settings from the feature config.

    eFEL stores unknown setting names without complaint, so a typo would silently leave
    the intended setting at its default. Names are therefore checked against the
    ``efel.Settings`` fields. Values must already have the field's type (an int is
    accepted for a float field).
    """
    raw = _data(cfg).get("settings") or {}
    if not isinstance(raw, Mapping):
        raise FeatureConfigError("'settings' must be a mapping of eFEL setting names to values")
    types = _setting_types()
    out: dict[str, float | int | bool | str] = {}
    for name, value in raw.items():
        if name not in types:
            raise FeatureConfigError(f"unknown eFEL setting {name!r}; eFEL {efel.__version__} settings are "
                                     f"{sorted(types)}")
        typ = types[name]
        if typ is bool:
            ok = isinstance(value, bool)
        elif typ is int:
            ok = isinstance(value, int) and not isinstance(value, bool)
        elif typ is float:
            ok = isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
        elif typ is str:
            ok = isinstance(value, str)
        else:
            ok = False
        if not ok:
            expected = typ.__name__ if typ else "an unsupported type"
            raise FeatureConfigError(f"eFEL setting {name!r} expects {expected}, got {value!r}")
        out[name] = typ(value)  # type: ignore[misc]
    return out


def feature_specs(cfg: Any) -> dict[str, FeatureSpec]:
    """Validated feature definitions; checks the pinned eFEL version and every eFEL name."""
    data = _data(cfg)
    pinned = data.get("efel_version")
    if pinned is not None and str(pinned) != efel.__version__:
        raise FeatureConfigError(f"feature config pins eFEL {pinned} but eFEL {efel.__version__} is installed")
    entries = data.get("features")
    if not isinstance(entries, Mapping) or not entries:
        raise FeatureConfigError("feature config has no 'features' section")
    specs: dict[str, FeatureSpec] = {}
    for name, e in entries.items():
        if not isinstance(e, Mapping):
            raise FeatureConfigError(f"feature {name!r}: definition must be a mapping")
        extra = set(e) - _SPEC_KEYS
        if extra:
            raise FeatureConfigError(f"feature {name!r}: unknown keys {sorted(extra)}")
        if ("efel" in e) == ("neurosem" in e):
            raise FeatureConfigError(f"feature {name!r}: needs exactly one of 'efel' or 'neurosem'")
        requires = e.get("requires")
        if requires is not None and requires not in REQUIREMENTS:
            raise FeatureConfigError(f"feature {name!r}: unknown requirement {requires!r}; known: {REQUIREMENTS}")
        min_spikes = e.get("min_spikes", 0)
        if isinstance(min_spikes, bool) or not isinstance(min_spikes, int) or min_spikes < 0:
            raise FeatureConfigError(f"feature {name!r}: min_spikes must be a non-negative integer")
        kind = e.get("kind", "numeric")
        if kind not in KINDS:
            raise FeatureConfigError(f"feature {name!r}: unknown kind {kind!r}; known: {KINDS}")
        unit = str(e.get("unit", ""))
        if "efel" in e:
            if e["efel"] not in _efel_feature_names():
                raise FeatureConfigError(f"feature {name!r}: {e['efel']!r} is not an eFEL {efel.__version__} feature")
            if e.get("agg") not in AGGREGATIONS:
                raise FeatureConfigError(f"feature {name!r}: agg must be one of {AGGREGATIONS}")
            if kind == "categorical":
                raise FeatureConfigError(f"feature {name!r}: eFEL features cannot be categorical")
            specs[name] = FeatureSpec(name, e["efel"], None, e["agg"], unit, min_spikes, requires, kind)
        else:
            if e["neurosem"] not in NEUROSEM_FEATURES:
                raise FeatureConfigError(f"feature {name!r}: unknown NeuroSem feature {e['neurosem']!r}")
            if "agg" in e:
                raise FeatureConfigError(f"feature {name!r}: NeuroSem features take no 'agg'")
            specs[name] = FeatureSpec(name, None, e["neurosem"], None, unit, min_spikes, requires, kind)
    sc = specs.get(SPIKE_COUNT)
    if sc is None or sc.efel is None or sc.agg != "scalar" or sc.min_spikes != 0 or sc.requires is not None:
        raise FeatureConfigError(f"feature config must define {SPIKE_COUNT!r} as a scalar eFEL feature with "
                                 "min_spikes 0 and no requirement (it gates every other feature)")
    return specs


def stimulus_amplitude_sum_nA(protocol: ConcreteProtocol) -> float:
    """Signed sum of the protocol's stimulus amplitudes (nA). A ramp contributes its mean current."""
    total = 0.0
    for c in protocol.components:
        if c.kind == "pulse":
            total += c.amplitude_nA
        elif c.kind == "ramp":
            total += 0.5 * (c.start_nA + c.finish_nA)
        else:
            raise FeatureConfigError(f"{protocol.protocol_id}: unknown stimulus component kind {c.kind!r}")
    return total


def is_hyperpolarizing(protocol: ConcreteProtocol) -> bool:
    """True if the summed stimulus amplitude is negative (the ``requires: hyperpolarizing`` rule)."""
    return stimulus_amplitude_sum_nA(protocol) < 0.0


def _apply_settings(settings: Mapping[str, Any]) -> None:
    efel.reset()
    for name, value in settings.items():
        efel.set_setting(name, value)


def effective_settings(cfg: Any) -> dict[str, Any]:
    """eFEL version and every eFEL setting exactly as applied for extraction (for provenance).

    The dependency-file path is reduced to its file name, because the absolute path
    depends on the machine.
    """
    settings = efel_settings(cfg)
    with _EFEL_LOCK:
        _apply_settings(settings)
        current = efel.get_settings()
        values = {f.name: getattr(current, f.name) for f in dc.fields(current)}
    if "dependencyfile_path" in values:
        values["dependencyfile_path"] = Path(str(values["dependencyfile_path"])).name
    return {"efel_version": efel.__version__, "settings": values}


def _efel_trace(trace: Trace, protocol: ConcreteProtocol, notes: list[str]) -> dict[str, Any]:
    pid = protocol.protocol_id
    t = np.asarray(trace.t_ms, dtype=np.float64)
    v = np.asarray(trace.v_mV, dtype=np.float64)
    if t.ndim != 1 or t.size < 2:
        raise ValueError(f"{pid}: a trace needs at least two samples")
    if not (np.all(np.isfinite(t)) and np.all(np.isfinite(v))):
        raise ValueError(f"{pid}: trace has non-finite samples; features are not extracted from unstable runs")
    if not np.all(np.diff(t) > 0):
        raise ValueError(f"{pid}: trace time must be strictly increasing")
    w = protocol.window
    if not w.end_ms > w.start_ms:
        raise ValueError(f"{pid}: analysis window end must exceed its start")
    if w.start_ms >= t[-1] or w.end_ms <= t[0]:
        raise ValueError(f"{pid}: analysis window [{w.start_ms}, {w.end_ms}] ms lies outside the trace "
                         f"[{t[0]}, {t[-1]}] ms")
    # A window may overrun the trace by at most one recorded step. Output sampling can drop
    # the final sample, which a one-step allowance covers. Anything larger means the window
    # covers time that was never recorded, so eFEL would report 'defined' values (a spike
    # count, a baseline) computed on missing data.
    step = (t[-1] - t[0]) / (t.size - 1)
    slack = 1e-6 * step
    if w.start_ms < t[0] - step - slack or w.end_ms > t[-1] + step + slack:
        raise ValueError(f"{pid}: analysis window [{w.start_ms}, {w.end_ms}] ms extends more than one sample step "
                         f"({step:g} ms) beyond the trace [{t[0]}, {t[-1]}] ms; features would be computed on "
                         "missing data")
    if w.start_ms < t[0] - slack or w.end_ms > t[-1] + slack:
        notes.append(f"analysis window [{w.start_ms}, {w.end_ms}] ms extends beyond the trace [{t[0]}, {t[-1]}] ms "
                     "by less than one sample step")
    return {"T": t, "V": v, "stim_start": [float(w.start_ms)], "stim_end": [float(w.end_ms)]}


def _run_efel(efel_trace: dict[str, Any], names: Sequence[str], settings: Mapping[str, Any], notes: list[str],
              capture: bool) -> dict[str, Any]:
    with _EFEL_LOCK:
        _apply_settings(settings)
        if not capture:
            return efel.get_feature_values([efel_trace], list(names), raise_warnings=True)[0]
        with _warnings.catch_warnings(record=True) as caught:
            _warnings.simplefilter("always")
            result = efel.get_feature_values([efel_trace], list(names), raise_warnings=True)[0]
    notes.extend(f"{w.category.__name__}: {w.message}" for w in caught)
    return result


def _reduce(spec: FeatureSpec, raw: Any, notes: list[str]) -> FeatureValue:
    undefined = FeatureValue(spec.name, None, UNDEFINED, spec.unit, spec.source)
    if raw is None:
        return undefined
    arr = np.asarray(raw, dtype=np.float64).ravel()
    if arr.size == 0:
        return undefined
    if spec.agg == "scalar" and arr.size != 1:
        raise FeatureConfigError(f"feature {spec.name!r}: eFEL {spec.efel} returned {arr.size} values but agg is "
                                 "'scalar'; configure 'first' or 'last'")
    x = float(arr[-1] if spec.agg == "last" else arr[0])
    if not math.isfinite(x):
        notes.append(f"{spec.name}: eFEL {spec.efel} returned non-finite {x!r}; recorded as undefined")
        return undefined
    return FeatureValue(spec.name, x, DEFINED, spec.unit, spec.source)


def extract(trace: Trace, protocol: ConcreteProtocol, cfg: Any, warnings: list[str] | None = None) -> FeatureTable:
    """Feature table for one protocol's trace, in the order of ``protocol.features``.

    ``rheobase`` is left to the fingerprint layer. Pass the *stored* trace (from
    :func:`~neuraxis.features.trace_metrics.unpack_traces` or
    :func:`~neuraxis.features.trace_metrics.stored_representation`) so the numbers
    reproduce from raw files. If ``warnings`` is a list, eFEL warnings and adapter notes
    are appended to it as ``"<protocol_id>: <message>"``. Otherwise they go through
    Python's warning system.
    """
    specs = feature_specs(cfg)
    settings = efel_settings(cfg)
    unknown = [f for f in protocol.features if f not in specs]
    if unknown:
        raise FeatureConfigError(f"{protocol.protocol_id}: features not defined in the feature config: {unknown}")
    wanted = [f for f in dict.fromkeys(protocol.features) if specs[f].neurosem not in FINGERPRINT_ONLY]
    needed = dict.fromkeys([SPIKE_COUNT, *wanted])
    if any(specs[f].neurosem == "firing_regime" for f in wanted):
        needed.update(dict.fromkeys(f for f in REGIME_INPUTS if f in specs))

    capture = warnings is not None
    notes: list[str] = []
    efel_trace = _efel_trace(trace, protocol, notes)

    # Spike count first: it decides which other features are applicable at all.
    sc = specs[SPIKE_COUNT]
    table: FeatureTable = {SPIKE_COUNT: _reduce(sc, _run_efel(efel_trace, [sc.efel], settings, notes, capture)[sc.efel],
                                                 notes)}
    n_spikes = table[SPIKE_COUNT].value
    hyperpolarizing = is_hyperpolarizing(protocol)
    pending: list[FeatureSpec] = []
    for name in needed:
        spec = specs[name]
        if name == SPIKE_COUNT or spec.efel is None:
            continue
        if spec.requires == "hyperpolarizing" and not hyperpolarizing:
            table[name] = FeatureValue(name, None, NOT_APPLICABLE, spec.unit, spec.source)
        elif spec.min_spikes > 0 and n_spikes is None:
            notes.append(f"{name}: spike count undefined, so min_spikes={spec.min_spikes} cannot be checked")
            table[name] = FeatureValue(name, None, UNDEFINED, spec.unit, spec.source)
        elif n_spikes is not None and n_spikes < spec.min_spikes:
            table[name] = FeatureValue(name, None, NOT_APPLICABLE, spec.unit, spec.source)
        else:
            pending.append(spec)
    if pending:
        raw = _run_efel(efel_trace, list(dict.fromkeys(s.efel for s in pending)), settings, notes, capture)
        for spec in pending:
            table[spec.name] = _reduce(spec, raw[spec.efel], notes)
    for name in needed:
        spec = specs[name]
        if spec.neurosem == "firing_regime":
            label = firing_regime(trace, protocol.window, table, cfg)
            table[name] = FeatureValue(name, label, DEFINED, spec.unit, spec.source)

    if warnings is not None:
        warnings.extend(f"{protocol.protocol_id}: {m}" for m in notes)
    else:
        for m in notes:
            _warnings.warn(f"{protocol.protocol_id}: {m}", RuntimeWarning, stacklevel=2)
    return {name: table[name] for name in wanted}


def extract_all(traces: Mapping[str, Trace], protocols: Sequence[ConcreteProtocol], cfg: Any,
                warnings: list[str] | None = None) -> dict[str, FeatureTable]:
    """:func:`extract` for every protocol, using the trace stored under its ``protocol_id``."""
    out: dict[str, FeatureTable] = {}
    for p in protocols:
        if p.protocol_id in out:
            raise ValueError(f"duplicate protocol id {p.protocol_id!r}")
        if p.protocol_id not in traces:
            raise KeyError(f"no trace for protocol {p.protocol_id!r}")
        out[p.protocol_id] = extract(traces[p.protocol_id], p, cfg, warnings)
    return out


def feature_table_to_json(ft: Mapping[str, FeatureValue]) -> dict[str, dict[str, Any]]:
    """``{feature: FeatureValue-dict}`` as stored in ``features.json``."""
    out: dict[str, dict[str, Any]] = {}
    for key, fv in ft.items():
        if key != fv.name:
            raise ValueError(f"feature table key {key!r} does not match feature name {fv.name!r}")
        out[key] = {"name": fv.name, "value": fv.value, "state": fv.state, "unit": fv.unit, "source": fv.source}
    return out


def feature_table_from_json(d: Mapping[str, Any]) -> FeatureTable:
    """Inverse of :func:`feature_table_to_json` (validates states and values)."""
    ft: FeatureTable = {}
    for key, entry in d.items():
        if not isinstance(entry, Mapping) or set(entry) != set(_JSON_KEYS):
            raise ValueError(f"feature {key!r}: expected keys {_JSON_KEYS}")
        value = entry["value"]
        if isinstance(value, bool):
            raise ValueError(f"feature {key!r}: boolean values are not feature values")
        fv = FeatureValue(str(entry["name"]), value, str(entry["state"]), str(entry["unit"]), str(entry["source"]))
        if fv.name != key:
            raise ValueError(f"feature table key {key!r} does not match feature name {fv.name!r}")
        ft[key] = fv
    return ft
