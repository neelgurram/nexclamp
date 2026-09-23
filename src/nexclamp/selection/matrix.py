"""Binary detection matrix: which protocol detects which admissible mutant.

Rows are admissible mutants (classes 5 and 6), columns are candidate protocols, and a
cell is True when at least one prespecified feature of that protocol differs from the
reference by more than its calibrated tolerance (at h and at h/2). Protocol selection
and the random baselines only ever see this matrix, never the simulations behind it,
so the matrix is the single artefact that has to be audited for data leakage.

CSV format (one file, byte-stable):

    mutant_id,model_id,family,<protocol_id>,<protocol_id>,...
    __cost__,,,<cost>,<cost>,...          <- always the first data row
    <mutant_id>,<model_id>,<family>,0|1,0|1,...

Costs are written with ``repr(float)``, which round-trips IEEE doubles exactly, so a
matrix read back from disk selects exactly the same protocols as the one written.
"""

from __future__ import annotations

import csv
import dataclasses as dc
import math
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

import numpy as np

from nexclamp.schemas import ConcreteProtocol

COST_ROW_ID = "__cost__"
ID_COLUMNS = ("mutant_id", "model_id", "family")


def _require_unique(ids: Sequence[str], what: str) -> None:
    dups = sorted(i for i, n in Counter(ids).items() if n > 1)
    if dups:
        raise ValueError(f"duplicate {what}: {dups[:5]}")


@dc.dataclass(eq=False)
class DetectionMatrix:
    """Boolean ``[n_mutants, n_protocols]`` matrix plus the row labels and column costs.

    ``cost`` is the simulation cost of each protocol in cell-steps (cells x integration
    steps), a simulator- and machine-independent runtime measure.
    """

    mutant_ids: list[str]
    protocol_ids: list[str]
    detected: np.ndarray
    model_of: dict[str, str]
    family_of: dict[str, str]
    cost: dict[str, float]

    def __post_init__(self) -> None:
        self.mutant_ids = [str(i) for i in self.mutant_ids]
        self.protocol_ids = [str(p) for p in self.protocol_ids]
        _require_unique(self.mutant_ids, "mutant ids")
        _require_unique(self.protocol_ids, "protocol ids")
        if COST_ROW_ID in self.mutant_ids:
            raise ValueError(f"{COST_ROW_ID!r} is reserved for the cost row")
        for pid in self.protocol_ids:
            if not pid or pid in ID_COLUMNS:
                raise ValueError(f"invalid protocol id {pid!r}")
        det = np.asarray(self.detected)
        expected = (len(self.mutant_ids), len(self.protocol_ids))
        if det.shape != expected:
            raise ValueError(f"detected has shape {det.shape}, expected {expected}")
        if det.dtype != np.bool_:
            if det.size and not np.isin(det, (0, 1)).all():
                raise ValueError("detected must contain only booleans or 0/1")
            det = det.astype(bool)
        self.detected = np.array(det, dtype=bool, copy=True)
        for name, mapping in (("model_of", self.model_of), ("family_of", self.family_of)):
            missing = [m for m in self.mutant_ids if not mapping.get(m)]
            if missing:
                raise ValueError(f"{name} has no non-empty entry for mutants {missing[:5]}")
        self.model_of = {m: str(self.model_of[m]) for m in self.mutant_ids}
        self.family_of = {m: str(self.family_of[m]) for m in self.mutant_ids}
        missing_cost = [p for p in self.protocol_ids if p not in self.cost]
        if missing_cost:
            raise ValueError(f"no cost for protocols {missing_cost}")
        cost = {p: float(self.cost[p]) for p in self.protocol_ids}
        bad = [p for p, c in cost.items() if not math.isfinite(c) or c < 0]
        if bad:
            raise ValueError(f"protocol costs must be finite and non-negative: {bad}")
        self.cost = cost
        self._col = {p: j for j, p in enumerate(self.protocol_ids)}

    # ------------------------------------------------------------------ basics
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DetectionMatrix):
            return NotImplemented
        return (self.mutant_ids == other.mutant_ids and self.protocol_ids == other.protocol_ids
                and np.array_equal(self.detected, other.detected) and self.model_of == other.model_of
                and self.family_of == other.family_of and self.cost == other.cost)

    @property
    def n_mutants(self) -> int:
        return len(self.mutant_ids)

    @property
    def n_protocols(self) -> int:
        return len(self.protocol_ids)

    def column_indices(self, protocols: Iterable[str]) -> np.ndarray:
        """Column indices for protocol ids (``KeyError`` for an unknown id)."""
        out = []
        for p in protocols:
            if p not in self._col:
                raise KeyError(f"protocol {p!r} is not a column of this matrix")
            out.append(self._col[p])
        return np.asarray(out, dtype=np.intp)

    def row_indices(self, rows: np.ndarray | Sequence[int] | None) -> np.ndarray:
        """Normalise ``rows`` (None, boolean mask or integer indices) to integer indices.

        Integer indices may repeat (e.g. a bootstrap resample weights a mutant twice).
        """
        if rows is None:
            return np.arange(self.n_mutants, dtype=np.intp)
        r = np.asarray(rows)
        if r.dtype == np.bool_:
            if r.shape != (self.n_mutants,):
                raise ValueError(f"row mask has shape {r.shape}, expected ({self.n_mutants},)")
            return np.flatnonzero(r)
        if r.size == 0:
            return np.zeros(0, dtype=np.intp)
        if not np.issubdtype(r.dtype, np.integer) or r.ndim != 1:
            raise ValueError("rows must be a boolean mask or a 1-D integer index array")
        if r.min() < 0 or r.max() >= self.n_mutants:
            raise IndexError("row index out of range")
        return r.astype(np.intp)

    def covered(self, protocols: Sequence[str], rows: np.ndarray | Sequence[int] | None = None) -> np.ndarray:
        """Per-row flag: detected by at least one of ``protocols``."""
        idx = self.row_indices(rows)
        cols = self.column_indices(protocols)
        if cols.size == 0:
            return np.zeros(idx.size, dtype=bool)
        return self.detected[np.ix_(idx, cols)].any(axis=1)

    def rate(self, protocols: Sequence[str], rows: np.ndarray | Sequence[int] | None = None) -> float:
        """Fraction of the selected rows detected by at least one protocol of the set.

        A rate over zero mutants is undefined, so it raises instead of returning 0 or NaN.
        """
        cov = self.covered(protocols, rows)
        if cov.size == 0:
            raise ValueError("detection rate is undefined for zero mutants")
        return float(cov.mean())

    def total_cost(self, protocols: Iterable[str]) -> float:
        return math.fsum(self.cost[p] for p in protocols)

    def take_rows(self, rows: np.ndarray | Sequence[int] | None) -> DetectionMatrix:
        """New matrix restricted to ``rows`` (duplicates are rejected: ids must stay unique)."""
        idx = self.row_indices(rows)
        ids = [self.mutant_ids[i] for i in idx]
        return DetectionMatrix(ids, list(self.protocol_ids), self.detected[idx, :], self.model_of, self.family_of,
                               self.cost)

    # ------------------------------------------------------------------ construction
    @classmethod
    def from_detected_sets(cls, mutant_ids: Sequence[str], protocol_ids: Sequence[str],
                           detected_by: Mapping[str, Iterable[str]], model_of: Mapping[str, str],
                           family_of: Mapping[str, str], cost: Mapping[str, float]) -> DetectionMatrix:
        """Build from ``{mutant_id: protocol ids that detect it}``.

        Every mutant must appear in ``detected_by`` (an empty set means "detected by
        nothing"), so a mutant silently missing from the detections cannot be mistaken
        for an undetected one.
        """
        col = {p: j for j, p in enumerate(protocol_ids)}
        det = np.zeros((len(mutant_ids), len(protocol_ids)), dtype=bool)
        for i, mid in enumerate(mutant_ids):
            if mid not in detected_by:
                raise KeyError(f"no detection entry for mutant {mid!r}")
            for p in detected_by[mid]:
                if p not in col:
                    raise KeyError(f"mutant {mid!r} detected by unknown protocol {p!r}")
                det[i, col[p]] = True
        return cls(list(mutant_ids), list(protocol_ids), det, dict(model_of), dict(family_of), dict(cost))

    # ------------------------------------------------------------------ CSV
    def to_csv(self, path: Path | str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow([*ID_COLUMNS, *self.protocol_ids])
            w.writerow([COST_ROW_ID, "", "", *(repr(self.cost[q]) for q in self.protocol_ids)])
            for i, mid in enumerate(self.mutant_ids):
                w.writerow([mid, self.model_of[mid], self.family_of[mid],
                            *("1" if v else "0" for v in self.detected[i])])

    @classmethod
    def from_csv(cls, path: Path | str) -> DetectionMatrix:
        with open(Path(path), newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        if not rows or tuple(rows[0][:3]) != ID_COLUMNS:
            raise ValueError(f"{path}: header must start with {','.join(ID_COLUMNS)}")
        protocol_ids = rows[0][3:]
        width = len(rows[0])
        if len(rows) < 2 or rows[1][:1] != [COST_ROW_ID]:
            raise ValueError(f"{path}: the first data row must be the {COST_ROW_ID!r} row")
        for n, r in enumerate(rows[1:], start=2):
            if len(r) != width:
                raise ValueError(f"{path}: line {n} has {len(r)} fields, expected {width}")
        cost = {q: float(v) for q, v in zip(protocol_ids, rows[1][3:])}
        mutant_ids: list[str] = []
        model_of: dict[str, str] = {}
        family_of: dict[str, str] = {}
        det = np.zeros((len(rows) - 2, len(protocol_ids)), dtype=bool)
        for i, r in enumerate(rows[2:]):
            mid = r[0]
            if mid in model_of:
                raise ValueError(f"{path}: duplicate mutant id {mid!r}")
            mutant_ids.append(mid)
            model_of[mid], family_of[mid] = r[1], r[2]
            for j, v in enumerate(r[3:]):
                if v not in ("0", "1"):
                    raise ValueError(f"{path}: mutant {mid!r} protocol {protocol_ids[j]!r} has value {v!r}, expected 0/1")
                det[i, j] = v == "1"
        return cls(mutant_ids, protocol_ids, det, model_of, family_of, cost)


def cell_step_costs(protocols: Sequence[ConcreteProtocol], dt_ms: float, n_cells: int = 1,
                    measured: Mapping[str, float] | None = None) -> dict[str, float]:
    """Protocol cost in cell-steps: ``n_cells * round(total_ms / dt_ms)``.

    This is the same measure :func:`nexclamp.protocols.generate.write_probe` reports for a
    batched probe run. Protocols whose cost is only known after running (the rheobase
    search is a variable number of steps) must be supplied in ``measured``, which
    overrides the computed value.
    """
    if not (dt_ms > 0 and math.isfinite(dt_ms)):
        raise ValueError("dt_ms must be positive and finite")
    if n_cells < 1:
        raise ValueError("n_cells must be >= 1")
    out = {p.protocol_id: float(n_cells * round(p.total_ms / dt_ms)) for p in protocols}
    for pid, c in (measured or {}).items():
        out[pid] = float(c)
    return out
