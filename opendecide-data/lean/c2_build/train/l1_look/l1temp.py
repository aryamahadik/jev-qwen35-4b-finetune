"""l1_look.l1temp: the serving temperature T of a model, fitted on the C2 MIXDEV only (dev data; never OHS-4, never Jev) and applied to the aggregated
served output. CPU only; numpy for the median.

BINDING PROCEDURE (c2_build/zed_orch/RULING_L1_PRELOOK.md item 1; teach1/C2_DATA_SPEC.md:777-779; C_TRAIN_RECIPE 6.0; PREREG 3.3 d):
  for each model m in {C1, C2} and type t in {yes/no ('noul'), 'choice'}, on THIS job's reads of split c2_mixdev (T = 1 as served; choice rows
  2-view averaged), rows = the families pre-gate (a) uses (A80 c: the families the final mix trained on; no T33 / T12 / T24, never the report-only file):
  1. groups = the union of three kinds, ids namespaced by kind:  sampler:<meta.sampler>  (all rows are S5: one group),  pack:<meta.domain_pack>,
     register:<meta.format_style>  (a row with no value joins no group of that kind). A group enters t's fit if it has at least ONE row of type t (no
     minimum size). Fewer than 2 groups for t: STOP (ValueError -> the caller refuses); no fallback.
  2. for every T in calibrate.GRID (0.25 .. 10.00, step 0.05): NLL_g(T) = calibrate.nll(rows of g, T)  (mean of -log max(p_T(gold), 1e-12) after
     calibrate.scaled; the same float operations, in the file's row order); M(T) = numpy.median over the groups of NLL_g(T).
  3. T_raw = the FIRST T in GRID order with the smallest M(T) (calibrate.py's tie rule);  T = min(1.3, max(0.8, T_raw))  (choose on the grid, then clip).
  4. T is applied after view aggregation with calibrate.scaled, to every answer (T = 1 only renormalises).
Report only (never binding): the same procedure grouped by meta.family, by pack only, by register only; C1's shipped A5 T (1.00 / 1.00).
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

CAL_GRID = [round(0.25 + 0.05 * i, 2) for i in range(196)]          # calibrate.py:16  (0.25 .. 10.0); a test keeps it equal to the source
T_LO, T_HI = 0.8, 1.3
GROUP_KINDS = (("sampler", "sampler"), ("pack", "domain_pack"), ("register", "format_style"))     # (kind, meta field)
RULE = ("RULING_L1_PRELOOK item 1: per model and type, on this job's c2_mixdev reads of the A80 (c) trained-family rows; groups = sampler + pack + register "
        "groups (union, namespaced, >= 1 row of the type, none smaller dropped); M(T) = median over groups of calibrate.nll on calibrate.GRID; "
        "T_raw = first argmin; T = clip(T_raw, 0.8, 1.3); applied after view aggregation (calibrate.scaled); fewer than 2 groups = stop")
SHIPPED_C1_A5 = {"noul": 1.0, "choice": 1.0, "source": "fastcore.readout.TEMPS (A5 shipped readout)"}


def scaled(probs: dict, T: float) -> dict:
    """calibrate.py's `scaled` (a test keeps this equal to the source)."""
    ks = [k for k in probs if not k.startswith("_")]
    lg = [math.log(max(probs[k], 1e-12)) / T for k in ks]
    m = max(lg)
    ex = [math.exp(x - m) for x in lg]
    s = sum(ex)
    return {k: e / s for k, e in zip(ks, ex)}


def gold_key(row: dict) -> str:
    return ("yes" if row["gold"] == 1 else "no") if row["qtype"] == "noul" else row["gold"]


def group_ids(row: dict, kinds=GROUP_KINDS) -> list:
    """The namespaced groups of one mixdev row: one per kind for which the row has a value."""
    meta = row.get("meta") or {}
    out = []
    for kind, field in kinds:
        v = meta.get(field)
        if v not in (None, ""):
            out.append(f"{kind}:{v}")
    return out


def family_group(row: dict) -> list:
    v = (row.get("meta") or {}).get("family")
    return [f"family:{v}"] if v not in (None, "") else []


def _log_terms(rows: list, preds: dict, T: float) -> list:
    """calibrate.nll's per-row term: math.log(max(q[gold], 1e-12)) after calibrate.scaled (negative numbers; the sum is subtracted)."""
    out = []
    for r in rows:
        p = preds.get(r["id"])
        if p is None:
            raise ValueError(f"no prediction for a mixdev row ({r['id'][:24]})")
        out.append(math.log(max(scaled(p, T).get(gold_key(r), 0.0), 1e-12)))
    return out


def group_members(rows: list, group_fn) -> dict:
    """{group id: [row indices in file order]} (only groups with at least one row of this type: the rows are already one type)."""
    g = defaultdict(list)
    for i, r in enumerate(rows):
        for gid in group_fn(r):
            g[gid].append(i)
    return g


def terms_table(sel: list, preds: dict) -> dict:
    """{T: per-row calibrate.nll terms} for every T of calibrate.GRID (computed once per (model, type); every grouping reuses it)."""
    return {T: _log_terms(sel, preds, T) for T in CAL_GRID}


def _median_table(members: dict, terms: dict) -> dict:
    table = {}
    for T in CAL_GRID:
        t = terms[T]
        means = []
        for idx in members.values():
            tot = 0.0
            for i in idx:
                tot -= t[i]                      # calibrate.nll: tot -= math.log(...)
            means.append(tot / max(1, len(idx)))
        table[T] = float(np.median(means))
    return table


def fit_type(rows: list, preds: dict, qtype: str, group_fn=group_ids, terms: dict | None = None) -> dict:
    """One (model, type) fit by the binding procedure. Raises ValueError with fewer than 2 groups (no fallback)."""
    sel = [r for r in rows if r["qtype"] == qtype]
    members = group_members(sel, group_fn)
    kinds = defaultdict(int)
    for gid in members:
        kinds[gid.split(":", 1)[0]] += 1
    if len(members) < 2:
        raise ValueError(f"{qtype}: {len(members)} group(s) in the fit rows; at least 2 are needed (no fallback)")
    table = _median_table(members, terms if terms is not None else terms_table(sel, preds))
    t_raw = min(CAL_GRID, key=lambda t: table[t])             # first T on ties
    return {"T": min(T_HI, max(T_LO, t_raw)), "T_raw": t_raw, "M_at_T_raw": round(table[t_raw], 6), "M_at_1.0": round(table[1.0], 6),
            "n_rows": len(sel), "n_groups": len(members), "groups_per_kind": dict(sorted(kinds.items()))}


REPORT_ONLY_GROUPINGS = (("family", family_group), ("pack_only", lambda r: [g for g in group_ids(r) if g.startswith("pack:")]),
                         ("register_only", lambda r: [g for g in group_ids(r) if g.startswith("register:")]))


def fit_all(rows: list, preds: dict) -> dict:
    """{'binding': {'noul': {..., 'T'}, 'choice': {...}}, 'report_only': {grouping: {type: {T, T_raw, n_groups}}}}. The log terms are computed once per type."""
    binding, report = {}, {name: {} for name, _ in REPORT_ONLY_GROUPINGS}
    for qt in ("noul", "choice"):
        sel = [r for r in rows if r["qtype"] == qt]
        terms = terms_table(sel, preds)
        binding[qt] = fit_type(rows, preds, qt, group_ids, terms)
        for name, fn in REPORT_ONLY_GROUPINGS:
            try:
                f = fit_type(rows, preds, qt, fn, terms)
                report[name][qt] = {k: f[k] for k in ("T", "T_raw", "n_groups")}
            except ValueError as e:
                report[name][qt] = {"error": str(e)[:80]}
    return {"binding": binding, "report_only": report}


def fit_model(rows: list, preds: dict) -> dict:
    """The binding fit only: {'noul': {...,'T'}, 'choice': {...,'T'}}."""
    return fit_all(rows, preds)["binding"]


def group_counts(rows: list) -> dict:
    """Per type: the number of binding groups (used before the GPU job to stop early when a type would end with fewer than 2)."""
    return {qt: len(group_members([r for r in rows if r["qtype"] == qt], group_ids)) for qt in ("noul", "choice")}


def T_of(fit: dict) -> dict:
    return {"noul": float(fit["noul"]["T"]), "choice": float(fit["choice"]["T"])}


def apply_T(probs: dict, qtype: str, T: dict) -> dict:
    """The look's answer: calibrate.scaled over the aggregated probabilities, for EVERY row (T = 1 only renormalises)."""
    return scaled(probs, float(T["noul" if qtype == "noul" else "choice"]))
