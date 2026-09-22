"""Automated, AI-assisted re-check of the audit sample. It is NOT the human audit.

For every mutant in the audit sheets it answers the three audit questions from the files on disk,
without trusting the pipeline's own summaries where an independent route exists:

1. Edit matches label. The variant workspace is compared file by file with the unmodified
   reference workspace. Every attribute change, added element and removed element is listed; the
   check passes only if the actual differences are exactly the recorded edits (one documented
   change, nothing else) and they have the meaning the operator's name claims (a scaled
   conductance is scaled by the recorded factor, a shifted reversal is shifted by the recorded
   amount, and so on).
2. Class plausible. The class is re-derived from the structural record, the run status and the
   raw detection rows, using the classification rule (reproducible = same protocol and feature
   detected at h and at h/2).
3. Detection plausible. Every detection row is recomputed from the per-run feature files in
   ``results/raw``: the difference is recomputed and compared with the calibrated tolerance.
   For spike-count detections the spikes are also counted directly from the stored voltage traces
   (upward crossings of -20 mV inside the protocol window), independently of eFEL.

The human verdict columns are never touched. Output: ``AUTOMATED_CHECK.md`` and
``AUTOMATED_CHECK.csv`` next to the audit packs.

    python scripts/audit_autocheck.py --campaign heldout-v1
"""

from __future__ import annotations

import argparse
import csv
import filecmp
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402

from neuraxis import config  # noqa: E402
from neuraxis.provenance import REPO_ROOT, git_state, utc_now  # noqa: E402

SPIKE_THRESHOLD_MV = -20.0
NUM = re.compile(r"^\s*([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s*([A-Za-z_][A-Za-z_0-9]*)?\s*$")


def read_csv(p: Path) -> list[dict]:
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(s: str) -> tuple[float, str] | None:
    m = NUM.match(str(s))
    return (float(m.group(1)), m.group(2) or "") if m else None


# --------------------------------------------------------------------------- 1. edit check
def _local(tag: str) -> str:
    return tag.split("}", 1)[-1]


def element_map(path: Path) -> dict[str, dict]:
    """Every element keyed by a path of tag[@id] (or tag[n] among same-tag siblings)."""
    out: dict[str, dict] = {}

    def walk(el, prefix):
        counts: dict[str, int] = {}
        for child in el:
            if not isinstance(child.tag, str):
                continue
            t = _local(child.tag)
            counts[t] = counts.get(t, 0) + 1
            key = f"{prefix}/{t}[@id='{child.get('id')}']" if child.get("id") else f"{prefix}/{t}[{counts[t]}]"
            out[key] = dict(child.attrib)
            walk(child, key)

    root = ET.parse(path).getroot()
    rk = f"/{_local(root.tag)}" + (f"[@id='{root.get('id')}']" if root.get("id") else "[1]")
    out[rk] = dict(root.attrib)
    walk(root, rk)
    return out


def workspace_diff(ref: Path, var: Path) -> tuple[list[dict], list[str]]:
    """Attribute-level differences between two model workspaces, plus non-XML file notes."""
    changes, notes = [], []
    ref_files = {p.relative_to(ref).as_posix() for p in ref.rglob("*") if p.is_file()} - {"variant.json"}
    var_files = {p.relative_to(var).as_posix() for p in var.rglob("*") if p.is_file()} - {"variant.json"}
    for f in sorted(ref_files - var_files):
        changes.append({"file": f, "kind": "file_removed"})
    for f in sorted(var_files - ref_files):
        changes.append({"file": f, "kind": "file_added"})
    for f in sorted(ref_files & var_files):
        if filecmp.cmp(ref / f, var / f, shallow=False):
            continue
        try:
            a, b = element_map(ref / f), element_map(var / f)
        except ET.ParseError:
            notes.append(f"{f}: differs but is not parseable XML")
            continue
        for k in sorted(set(a) - set(b)):
            changes.append({"file": f, "kind": "element_removed", "locator": k, "attrs": a[k]})
        for k in sorted(set(b) - set(a)):
            changes.append({"file": f, "kind": "element_added", "locator": k, "attrs": b[k]})
        for k in sorted(set(a) & set(b)):
            for attr in sorted(set(a[k]) | set(b[k])):
                if a[k].get(attr) != b[k].get(attr):
                    changes.append({"file": f, "kind": "attribute", "locator": k, "attribute": attr,
                                    "old": a[k].get(attr), "new": b[k].get(attr)})
        if not any(c["file"] == f for c in changes):
            notes.append(f"{f}: differs only in formatting, comments or text content")
    return changes, notes


def check_edit(op: str, params: dict, execo: dict, changes: list[dict], ref: Path) -> tuple[str, str]:
    attrs = [c for c in changes if c["kind"] == "attribute"]
    added = [c for c in changes if c["kind"] == "element_added"]
    removed = [c for c in changes if c["kind"] == "element_removed"]
    files = [c for c in changes if c["kind"].startswith("file")]
    recorded = params.get("changes", [])

    def only_recorded() -> str | None:
        rec = {(c.get("attribute"), str(c.get("old")), str(c.get("new"))) for c in recorded}
        act = {(c["attribute"], str(c["old"]), str(c["new"])) for c in attrs}
        if files or added or removed:
            return "unexpected added/removed elements or files"
        if rec != act:
            return f"actual changes {sorted(act)} differ from recorded {sorted(rec)}"
        return None

    def ratios() -> list[float]:
        out = []
        for c in attrs:
            o, n = num(c["old"]), num(c["new"])
            if not o or not n or o[1] != n[1] or o[0] == 0:
                return []
            out.append(n[0] / o[0])
        return out

    def shifts() -> list[float]:
        out = []
        for c in attrs:
            o, n = num(c["old"]), num(c["new"])
            if not o or not n or o[1] != n[1]:
                return []
            out.append(n[0] - o[0])
        return out

    if op in ("scale_conductance", "scale_capacitance", "scale_gate_slope") or \
            (op == "scale_gate_time_constant" and recorded):
        bad = only_recorded()
        if bad:
            return "no", bad
        r = ratios()
        k = params.get("factor")
        if not r or max(r) - min(r) > 1e-9:
            return "no", f"changes are not one consistent scaling (ratios {r})"
        if k is not None and abs(r[0] - float(k)) > 1e-9:
            return "no", f"scaled by {r[0]:.6g}, recorded factor {k}"
        target = {"scale_conductance": "condDensity", "scale_capacitance": "value",
                  "scale_gate_slope": "scale"}.get(op)
        if op == "scale_gate_time_constant":
            ok_attrs = {"rate", "fixedQ10"}
            if not {c["attribute"] for c in attrs} <= ok_attrs:
                return "no", f"edited {sorted({c['attribute'] for c in attrs})}, expected gate rates or Q10"
        elif any(c["attribute"] != target for c in attrs):
            return "no", f"edited {sorted({c['attribute'] for c in attrs})}, expected {target}"
        return "yes", f"{len(attrs)} value(s) x{r[0]:.6g}, same units, nothing else changed"

    if op in ("shift_reversal", "shift_gate_midpoint", "shift_forward_rate_midpoint"):
        bad = only_recorded()
        if bad:
            return "no", bad
        s = shifts()
        target = "erev" if op == "shift_reversal" else "midpoint"
        if not s or max(s) - min(s) > 1e-9 or s[0] == 0:
            return "no", f"not one consistent non-zero shift ({s})"
        if any(c["attribute"] != target for c in attrs):
            return "no", f"edited {sorted({c['attribute'] for c in attrs})}, expected {target}"
        d = params.get("delta_mV")
        if d is not None and abs(abs(s[0]) - abs(float(d))) > 1e-9:
            return "no", f"shifted by {s[0]:+g} mV, recorded delta {d}"
        return "yes", f"{len(attrs)} value(s) shifted {s[0]:+g} mV, nothing else changed"

    if op == "scale_gate_time_constant":                      # q10 insertion, no attribute list
        q = [c for c in added if c["locator"].split("/")[-1].startswith("q10Settings")]
        if len(q) == 1 and not attrs and not removed and not files and len(added) == 1:
            f = q[0]["attrs"].get("fixedQ10")
            if f is not None and abs(float(f) - float(params.get("factor", float("nan")))) < 1e-9:
                return "yes", f"q10Settings fixedQ10={f} inserted on {q[0]['locator'].split('/')[-2]}; nothing else"
        return "no", f"expected one inserted q10Settings with fixedQ10={params.get('factor')}"

    if op == "duplicate_conductance":
        if len(added) == 1 and not attrs and not removed and not files:
            a = added[0]
            src_locator = a["locator"].replace(f"@id='{params.get('new_id')}'", f"@id='{params.get('source_id')}'")
            src = element_map(ref / a["file"]).get(src_locator)
            if src is not None and {k: v for k, v in src.items() if k != "id"} == \
                    {k: v for k, v in a["attrs"].items() if k != "id"} and a["attrs"].get("id") == params.get("new_id"):
                return "yes", f"one element {params.get('new_id')} added, identical to {params.get('source_id')} except id"
        return "no", "expected exactly one added element identical to the source except its id"

    if op in ("wrong_channel", "wrong_compatible_component"):
        bad = only_recorded()
        if bad:
            return "no", bad
        if len(attrs) != 1 or attrs[0]["attribute"] != "ionChannel" or attrs[0]["old"] == attrs[0]["new"]:
            return "no", "expected one ionChannel reference changed"
        new = attrs[0]["new"]
        defined = any(f'id="{new}"' in p.read_text(encoding="utf-8", errors="replace")
                      for p in ref.rglob("*.nml"))
        return ("yes" if defined else "no"), (f"ionChannel {attrs[0]['old']} -> {new}; target channel "
                                               f"{'is' if defined else 'is NOT'} defined in the model files")

    if op == "omit_include":
        inc = [c for c in removed if c["locator"].split("/")[-1].startswith("include")]
        if len(inc) == 1 and len(removed) == 1 and not attrs and not added and not files:
            return "yes", f"one include removed ({inc[0]['attrs'].get('href')}); nothing else"
        return "no", "expected exactly one removed include"

    if op == "increase_dt":
        bad = only_recorded()
        if bad:
            return "no", bad
        r = ratios()
        k = params.get("factor")
        if r and abs(r[0] - float(k)) < 1e-9 and float(execo.get("dt_factor", 0)) == float(k):
            return "yes", f"harness step x{k} and probe dt_factor {execo.get('dt_factor')}; nothing else"
        return "no", f"step ratio {r}, dt_factor {execo.get('dt_factor')}, recorded factor {k}"

    if op == "solver_config":
        meta = [c for c in added if c["locator"].split("/")[-1].startswith("Meta")]
        if execo.get("integrator_method") == params.get("method") and len(meta) <= 1 and not removed and not files:
            return "yes", f"integrator {params.get('method')} set in harness Meta and probe override"
        return "no", "harness Meta / probe override do not match the recorded method"

    if op == "recording_resolution":
        return ("yes" if not changes else "no"), "configuration-only mutation: no model file may change"

    return "unchecked", f"no automatic semantics for operator {op}; {len(changes)} change(s) listed"


# --------------------------------------------------------------------------- 2. class re-derivation
def rederive_class(vdir: Path, row: dict) -> str:
    st = json.loads((vdir / "structural.json").read_text(encoding="utf-8")) if (vdir / "structural.json").is_file() else {}
    if st and not st.get("valid", True):
        return "1_structurally_invalid"
    status = row.get("status_h", "")
    if status in ("build_error", "runtime_error", "timeout", "failed", "error"):
        return "2_non_executable"
    if status == "numerically_unstable":
        return "3_numerically_unstable"
    det = read_csv(vdir / "detections.csv") if (vdir / "detections.csv").is_file() else []
    at = {lv: {(d["protocol_id"], d["feature"]) for d in det if d["level_factor"] == lv} for lv in ("1", "2")}
    rep = at["1"] & at["2"]
    if not rep:
        return "4_equivalent_within_tested_domain"
    return "5_non_equivalent" if any(p == "P00_canonical" for p, _ in rep) else "6_silent_under_canonical"


# --------------------------------------------------------------------------- 3. detection recomputation
def features(raw: Path, run_id: str) -> dict:
    f = next((raw / run_id).glob("features*.json"), None)
    if f:
        return json.loads(f.read_text(encoding="utf-8"))["tables"]
    r = raw / run_id / "rheobase.json"                 # rheobase searches store their result here
    if r.is_file():
        res = json.loads(r.read_text(encoding="utf-8"))["result"]
        ok = res.get("status") == "ok" and res.get("rheobase_nA") is not None
        return {"P03_rheobase": {"rheobase": {"state": "defined" if ok else "undefined",
                                              "value": res.get("rheobase_nA")}}}
    return {}


def window(proc: Path, model: str, protocol: str) -> tuple[float, float] | None:
    ref = proc / "references" / model
    if protocol == "P00_canonical":
        d = json.loads((ref / "canonical_protocol.json").read_text(encoding="utf-8"))
        w = d.get("window") or {}
    else:
        w = next((p.get("window") for p in json.loads((ref / "protocols.json").read_text(encoding="utf-8"))
                  if p.get("protocol_id") == protocol), None) or {}
    return (float(w["start_ms"]), float(w["end_ms"])) if w else None


def raw_spike_count(raw: Path, run_id: str, protocol: str, win) -> int | None:
    f = raw / run_id / "traces.npz"
    if not f.is_file():
        return None
    z = np.load(f)
    if f"{protocol}__v" not in z.files:
        return None
    v = z[f"{protocol}__v"]
    t = z[f"{protocol}__t"]
    t = np.arange(len(v)) * float(t[1]) + float(t[0]) if len(t) == 3 else t
    if win:
        m = (t >= win[0]) & (t <= win[1])
        t, v = t[m], v[m]
    up = (v[:-1] < SPIKE_THRESHOLD_MV) & (v[1:] >= SPIKE_THRESHOLD_MV)
    return int(up.sum())


def check_detections(vdir: Path, proc: Path, raw: Path, model: str, tol: dict) -> tuple[str, list[str]]:
    det = read_csv(vdir / "detections.csv") if (vdir / "detections.csv").is_file() else []
    if not det:
        return "n/a (no detections)", []
    notes, ok_all = [], True
    for d in det:
        key = f"h/{d['level_factor']} {d['protocol_id']}:{d['feature']}"
        r = features(raw, d["ref_run_id"]).get(d["protocol_id"], {}).get(d["feature"], {})
        v = features(raw, d["var_run_id"]).get(d["protocol_id"], {}).get(d["feature"], {})
        if r.get("state") != "defined" or v.get("state") != "defined":
            same = r.get("state") == v.get("state")
            notes.append(f"{key}: definedness {r.get('state')} vs {v.get('state')}"
                         + (" (NOT a mismatch)" if same else " (mismatch counts as detection)"))
            ok_all &= not same
            continue
        if not isinstance(r.get("value"), (int, float)) or not isinstance(v.get("value"), (int, float)):
            ok_all &= r.get("value") != v.get("value")
            notes.append(f"{key}: categorical {r.get('value')} vs {v.get('value')}")
            continue
        diff = abs(float(v["value"]) - float(r["value"]))
        tau = float(d["tau"])
        cal = tol.get((model, d["protocol_id"], d["feature"]))
        good = diff > tau and math.isclose(diff, float(d["diff"]), rel_tol=1e-9, abs_tol=1e-12)
        if cal is not None and d["level_factor"] == "1" and not math.isclose(cal, tau, rel_tol=1e-9, abs_tol=1e-12):
            notes.append(f"{key}: recorded tau {tau:g} differs from calibrated {cal:g}")
            good = False
        extra = ""
        if d["feature"] == "spike_count":
            win = window(proc, model, d["protocol_id"])
            a = raw_spike_count(raw, d["ref_run_id"], d["protocol_id"], win)
            b = raw_spike_count(raw, d["var_run_id"], d["protocol_id"], win)
            if a is not None and b is not None:
                extra = f"; raw-trace count {a} -> {b}"
                if (a, b) != (int(r["value"]), int(v["value"])):
                    extra += " (differs from eFEL count)"
                    good = good and (a != b)
        ok_all &= good
        notes.append(f"{key}: {r['value']:.6g} -> {v['value']:.6g}, |diff| {diff:.4g} vs tau {tau:.4g}"
                     f" {'OK' if good else 'PROBLEM'}{extra}")
    return ("yes" if ok_all else "no"), notes


def _trace(raw: Path, run_id: str, protocol: str):
    f = raw / run_id / "traces.npz"
    if not f.is_file():
        return None
    z = np.load(f)
    if f"{protocol}__v" not in z.files:
        return None
    v = z[f"{protocol}__v"]
    t = z[f"{protocol}__t"]
    t = np.arange(len(v)) * float(t[1]) + float(t[0]) if len(t) == 3 else t
    return t, v


def _spike_times(t, v) -> np.ndarray:
    i = np.where((v[:-1] < SPIKE_THRESHOLD_MV) & (v[1:] >= SPIKE_THRESHOLD_MV))[0]
    frac = (SPIKE_THRESHOLD_MV - v[i]) / (v[i + 1] - v[i])     # linear interpolation of the crossing
    return t[i] + frac * (t[i + 1] - t[i])


def check_trace_detections(vdir: Path, proc: Path, raw: Path, model: str) -> tuple[str, list[str]]:
    """Recompute full-trace detections (spike count, spike timing, RMSE) from the raw voltage traces."""
    f = vdir / "detections_trace.csv"
    det = [d for d in read_csv(f) if d.get("metric")] if f.is_file() else []
    if not det:
        return "n/a (no trace detections)", []
    notes, ok_all = [], True
    for d in det:
        lv, prot, metric = d["level_factor"], d["protocol_id"], d["metric"]
        vr = json.loads((vdir / f"fingerprint_L{lv}.json").read_text(encoding="utf-8"))["run_ids"].get(prot)
        rr = json.loads((proc / "references" / model / f"fingerprint_L{lv}.json").read_text(encoding="utf-8"))["run_ids"].get(prot)
        a, b = _trace(raw, rr, prot), _trace(raw, vr, prot)
        key = f"trace h/{lv} {prot}:{metric}"
        if a is None or b is None:
            notes.append(f"{key}: trace missing")
            ok_all = False
            continue
        ta, tb = _spike_times(*a), _spike_times(*b)
        tau = float(d["tau"]) if d.get("tau") else 0.0
        if metric == "spike_count":
            good = len(ta) != len(tb)
            notes.append(f"{key}: raw spikes {len(ta)} -> {len(tb)} {'OK' if good else 'PROBLEM'}")
        elif metric == "spike_timing":
            if len(ta) != len(tb) or not len(ta):
                good = False
                notes.append(f"{key}: counts {len(ta)} vs {len(tb)}, timing not comparable PROBLEM")
            else:
                shift = float(np.max(np.abs(ta - tb)))
                good = shift > tau
                notes.append(f"{key}: {len(ta)} spikes, max shift {shift:.3f} ms vs tau {tau:.3f} "
                             f"(recorded {float(d['diff']):.3f}) {'OK' if good else 'PROBLEM'}")
        else:                                                  # trace_rmse
            n = min(len(a[1]), len(b[1]))
            rmse = float(np.sqrt(np.mean((a[1][:n] - b[1][:n]) ** 2)))
            good = rmse > tau
            notes.append(f"{key}: RMSE {rmse:.3f} mV vs tau {tau:.3f} (recorded {float(d['diff']):.3f}) "
                         f"{'OK' if good else 'PROBLEM'}")
        ok_all &= good
    return ("yes" if ok_all else "no"), notes


# --------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--campaign", required=True)
    a = ap.parse_args(argv)
    proc = config.results_dir() / "processed" / a.campaign
    raw = config.results_dir() / "raw" / a.campaign
    work = REPO_ROOT / "work" / "variants" / a.campaign
    audit = config.results_dir() / "tables" / a.campaign / "audit"
    cls = {r["variant_id"]: r for r in read_csv(proc / "classification.csv")}
    sheet = {r["variant_id"]: r for r in read_csv(proc / "mutant_audit_sheet.csv")}
    tol = {(t["model_id"], t["protocol_id"], t["feature"]): float(t["tau"]) for t in read_csv(proc / "tolerances.csv")
           if t.get("tau") not in ("", None)}
    packs = [(p.name, [r["variant_id"] for r in read_csv(p / "AUDIT_SHEET.csv")])
             for p in sorted(audit.iterdir()) if (p / "AUDIT_SHEET.csv").is_file()]

    rows, md = [], []
    for pack, ids in packs:
        for vid in ids:
            c = cls[vid]
            model = c["model_id"]
            params = json.loads(c["params"] or "{}")
            execo = json.loads(sheet[vid].get("exec_overrides") or "{}")
            ref = work / model / "reference"
            var = work / "mutants" / model / vid
            changes, notes = workspace_diff(ref, var)
            e_ok, e_note = check_edit(c["operator"], params, execo, changes, ref)
            derived = rederive_class(proc / "variants" / vid, c)
            k_ok = "yes" if derived == c["class"] else "no"
            d_ok, d_notes = check_detections(proc / "variants" / vid, proc, raw, model, tol)
            t_ok, t_notes = check_trace_detections(proc / "variants" / vid, proc, raw, model)
            rows.append({"pack": pack, "variant_id": vid, "model_id": model, "operator": c["operator"],
                         "assigned_class": c["class"], "ai_edit_matches_label": e_ok, "ai_edit_note": e_note,
                         "ai_class_rederived": derived, "ai_class_matches": k_ok,
                         "ai_detections_recomputed_ok": d_ok, "n_detection_rows": len(d_notes),
                         "ai_trace_detections_recomputed_ok": t_ok, "n_trace_rows": len(t_notes),
                         "flag": "" if (e_ok in ("yes",) and k_ok == "yes" and d_ok in ("yes", "n/a (no detections)")
                                        and t_ok in ("yes", "n/a (no trace detections)"))
                         else "REVIEW"})
            md += [f"### `{vid}` ({pack})", "",
                   f"- model `{model}`, operator `{c['operator']}`, assigned class `{c['class']}`",
                   f"- **edit matches label: {e_ok}**: {e_note}",
                   *[f"  - diff: {x.get('kind')} {x.get('file', '')} {x.get('attribute', '')} "
                     f"{x.get('old', '')} -> {x.get('new', '')}".rstrip() for x in changes[:8]],
                   *[f"  - note: {n}" for n in notes],
                   f"- **class re-derived: `{derived}`** ({'matches' if k_ok == 'yes' else 'DOES NOT MATCH'})",
                   f"- **detections recomputed: {d_ok}**",
                   *[f"  - {n}" for n in d_notes],
                   f"- **full-trace detections recomputed from raw traces: {t_ok}**",
                   *[f"  - {n}" for n in t_notes], ""]

    cols = list(rows[0])
    with open(audit / "AUTOMATED_CHECK.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    commit, dirty = git_state()
    n_flag = sum(r["flag"] == "REVIEW" for r in rows)
    head = ["# Automated re-check of the audit sample (AI-assisted, not the human audit)", "",
            f"*{len(rows)} mutants from {len(packs)} packs. Generated {utc_now()} at commit `{commit}` "
            f"(tree dirty: {dirty}) by `scripts/audit_autocheck.py`. The human verdict columns in each "
            "`AUDIT_SHEET.csv` are left empty on purpose: the preregistered audit is done by people.*", "",
            "## Summary", "",
            "| check | passed | failed or unchecked |", "|---|---|---|",
            f"| edit matches label (actual file diff = recorded edit, with the operator's meaning) | "
            f"{sum(r['ai_edit_matches_label'] == 'yes' for r in rows)} | "
            f"{sum(r['ai_edit_matches_label'] != 'yes' for r in rows)} |",
            f"| class re-derived from structural record, run status and raw detection rows | "
            f"{sum(r['ai_class_matches'] == 'yes' for r in rows)} | {sum(r['ai_class_matches'] != 'yes' for r in rows)} |",
            f"| detections recomputed from per-run feature files (and raw traces for spike counts) | "
            f"{sum(r['ai_detections_recomputed_ok'] in ('yes', 'n/a (no detections)') for r in rows)} | "
            f"{sum(r['ai_detections_recomputed_ok'] not in ('yes', 'n/a (no detections)') for r in rows)} |",
            f"| full-trace detections recomputed from raw voltage traces (spike count, spike timing, RMSE) | "
            f"{sum(r['ai_trace_detections_recomputed_ok'] in ('yes', 'n/a (no trace detections)') for r in rows)} | "
            f"{sum(r['ai_trace_detections_recomputed_ok'] not in ('yes', 'n/a (no trace detections)') for r in rows)} |", "",
            f"**Flagged for human attention: {n_flag}.**", "",
            "## What each check does", "",
            "- *Edit*: the variant's files are compared with the unmodified reference workspace; every "
            "attribute change, added or removed element is listed. Passes only if the differences are exactly "
            "the recorded edit and have the meaning the operator's name claims.",
            "- *Class*: re-derived with the classification rule; reproducible means the same protocol and "
            "feature are detected at h and at h/2.",
            "- *Detections*: each recorded detection is recomputed from the two runs' feature files and compared "
            "with its tolerance; spike counts are recounted from the voltage traces (-20 mV upward crossings in "
            "the protocol window) without eFEL.", "", "## Per mutant", ""]
    (audit / "AUTOMATED_CHECK.md").write_text("\n".join(head + md) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(rows)} mutants checked; flagged for review: {n_flag}")
    for r in rows:
        if r["flag"]:
            print(f"  REVIEW {r['variant_id']}: edit={r['ai_edit_matches_label']} class={r['ai_class_matches']} "
                  f"det={r['ai_detections_recomputed_ok']} | {r['ai_edit_note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
