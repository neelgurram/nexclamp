"""Tolerance calibration by numerical refinement (spec "Tolerance calibration").

For reference model m, protocol p and feature f:

    tau(m, p, f) = max( abs_floor_f,  rel_f * |f_h|,  c * |f_h - f_h/2| )

Plain English: a difference between a reference and a variant only counts if it is bigger
than (a) a fixed floor below which the feature is not scientifically meaningful, (b) a
small fraction of the feature's own size, and (c) several times the change caused merely
by halving the solver time step -- i.e. bigger than what the solver's own error could
produce. A (protocol, feature) whose defined/undefined state, or whose firing-regime
label, flips when the time step is halved cannot be trusted at all and is excluded from
detection for that model (recorded, never silently dropped).
"""

from __future__ import annotations

import csv
import dataclasses as dc
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

EXCLUDED_DEFINEDNESS = "excluded:definedness_changes_under_refinement"
EXCLUDED_REGIME = "excluded:category_changes_under_refinement"
MISSING = "excluded:missing_at_refinement_level"


@dc.dataclass
class TolEntry:
    model_id: str
    protocol_id: str
    feature: str
    kind: str                      # numeric | count | categorical
    f_h: float | str | None
    f_h2: float | str | None
    f_h4: float | str | None
    state_h: str
    state_h2: str
    abs_floor: float
    rel_term: float
    refine_term: float
    tau: float | None              # None = excluded from detection
    limiting: str                  # abs_floor | relative | refinement | exact | both_undefined | excluded:*
    note: str = ""

    @property
    def excluded(self) -> bool:
        return self.limiting.startswith("excluded")


class ToleranceTable:
    COLUMNS = [f.name for f in dc.fields(TolEntry)]

    def __init__(self, entries: list[TolEntry]) -> None:
        self._d: dict[tuple[str, str, str], TolEntry] = {}
        for e in entries:
            key = (e.model_id, e.protocol_id, e.feature)
            if key in self._d:
                raise ValueError(f"duplicate tolerance entry {key}")
            self._d[key] = e

    def get(self, model_id: str, protocol_id: str, feature: str) -> TolEntry | None:
        return self._d.get((model_id, protocol_id, feature))

    def tau(self, model_id: str, protocol_id: str, feature: str) -> float | None:
        e = self.get(model_id, protocol_id, feature)
        return None if e is None else e.tau

    @property
    def entries(self) -> list[TolEntry]:
        return list(self._d.values())

    def merged(self, other: "ToleranceTable") -> "ToleranceTable":
        return ToleranceTable(self.entries + other.entries)

    def to_csv(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=self.COLUMNS, lineterminator="\n")
            w.writeheader()
            for e in sorted(self.entries, key=lambda e: (e.model_id, e.protocol_id, e.feature)):
                row = dc.asdict(e)
                w.writerow({k: ("" if v is None else v) for k, v in row.items()})

    @classmethod
    def from_csv(cls, path: Path) -> "ToleranceTable":
        out = []
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                kind = r["kind"]
                conv = (lambda s: s if s != "" else None) if kind == "categorical" else _float_or_none
                out.append(TolEntry(
                    model_id=r["model_id"], protocol_id=r["protocol_id"], feature=r["feature"], kind=kind,
                    f_h=conv(r["f_h"]), f_h2=conv(r["f_h2"]), f_h4=conv(r["f_h4"]), state_h=r["state_h"],
                    state_h2=r["state_h2"], abs_floor=float(r["abs_floor"]), rel_term=float(r["rel_term"]),
                    refine_term=float(r["refine_term"]), tau=_float_or_none(r["tau"]), limiting=r["limiting"],
                    note=r.get("note", "")))
        return cls(out)


def _float_or_none(s: str) -> float | None:
    return None if s in ("", "None") else float(s)


def _kind(feature: str, features_cfg: Mapping[str, Any]) -> str:
    spec = (features_cfg.get("features") or {}).get(feature, {})
    k = spec.get("kind", "numeric")
    return k if k in ("count", "categorical") else "numeric"


def calibrate(fp_by_factor: Mapping[int, Any], model_id: str, tol_cfg: Mapping[str, Any],
              features_cfg: Mapping[str, Any]) -> list[TolEntry]:
    """Tolerances for one reference model from its fingerprints at refinement factors 1, 2 (, 4)."""
    if 1 not in fp_by_factor or 2 not in fp_by_factor:
        raise ValueError("calibration needs reference fingerprints at refinement factors 1 (h) and 2 (h/2)")
    fh, fh2, fh4 = fp_by_factor[1], fp_by_factor[2], fp_by_factor.get(4)
    c = float(tol_cfg["c_refinement"])
    fcfg = tol_cfg["features"]
    entries: list[TolEntry] = []
    for pid, table in sorted(fh.tables.items()):
        for feat, v1 in sorted(table.items()):
            v2 = fh2.tables.get(pid, {}).get(feat)
            v4 = fh4.tables.get(pid, {}).get(feat) if fh4 is not None else None
            kind = _kind(feat, features_cfg)
            spec = fcfg.get(feat, {})
            abs_floor = float(spec.get("abs_floor", 0.0))
            rel = float(spec.get("rel", 0.0))
            base = dict(model_id=model_id, protocol_id=pid, feature=feat, kind=kind,
                        f_h=v1.value, f_h2=None if v2 is None else v2.value, f_h4=None if v4 is None else v4.value,
                        state_h=v1.state, state_h2="missing" if v2 is None else v2.state)
            if v2 is None:
                entries.append(TolEntry(**base, abs_floor=abs_floor, rel_term=0.0, refine_term=0.0, tau=None, limiting=MISSING))
                continue
            defined1, defined2 = v1.state == "defined", v2.state == "defined"
            if defined1 != defined2:
                entries.append(TolEntry(**base, abs_floor=abs_floor, rel_term=0.0, refine_term=0.0, tau=None,
                                        limiting=EXCLUDED_DEFINEDNESS))
                continue
            if not defined1:
                # Undefined in the reference at both levels: only a variant that becomes defined is a detection.
                entries.append(TolEntry(**base, abs_floor=abs_floor, rel_term=0.0, refine_term=0.0, tau=math.inf,
                                        limiting="both_undefined"))
                continue
            if kind == "categorical":
                if v1.value != v2.value:
                    entries.append(TolEntry(**base, abs_floor=0.0, rel_term=0.0, refine_term=0.0, tau=None,
                                            limiting=EXCLUDED_REGIME))
                else:
                    entries.append(TolEntry(**base, abs_floor=0.0, rel_term=0.0, refine_term=0.0, tau=0.0, limiting="exact"))
                continue
            x1, x2 = float(v1.value), float(v2.value)
            if feat == "rheobase" and fh.rheobase:
                res = fh.rheobase.get("upper_nA"), fh.rheobase.get("lower_nA")
                if None not in res:
                    abs_floor = max(abs_floor, float(spec.get("resolution_multiple", 2.0)) * (res[0] - res[1]))
            terms = {"abs_floor": abs_floor, "relative": rel * abs(x1), "refinement": c * abs(x1 - x2)}
            limiting = max(terms, key=terms.get)
            entries.append(TolEntry(**base, abs_floor=abs_floor, rel_term=terms["relative"],
                                    refine_term=terms["refinement"], tau=terms[limiting], limiting=limiting))
    return entries


def convergence_report(fp_by_factor: Mapping[int, Any]) -> list[dict]:
    """Per (protocol, feature): refinement differences and observed convergence order."""
    fh, fh2, fh4 = fp_by_factor[1], fp_by_factor.get(2), fp_by_factor.get(4)
    rows = []
    for pid, table in sorted(fh.tables.items()):
        for feat, v1 in sorted(table.items()):
            row = {"model_id": fh.model_id, "protocol_id": pid, "feature": feat, "f_h": v1.value, "state_h": v1.state}
            v2 = fh2.tables.get(pid, {}).get(feat) if fh2 else None
            v4 = fh4.tables.get(pid, {}).get(feat) if fh4 else None
            row.update({"f_h2": None if v2 is None else v2.value, "f_h4": None if v4 is None else v4.value,
                        "d12": None, "d24": None, "observed_order": None})
            numeric = all(v is not None and v.state == "defined" and isinstance(v.value, (int, float)) for v in (v1, v2))
            if numeric:
                row["d12"] = abs(float(v1.value) - float(v2.value))
                if v4 is not None and v4.state == "defined" and isinstance(v4.value, (int, float)):
                    row["d24"] = abs(float(v2.value) - float(v4.value))
                    if row["d12"] > 0 and row["d24"] > 0:
                        row["observed_order"] = math.log2(row["d12"] / row["d24"])
            rows.append(row)
    return rows
