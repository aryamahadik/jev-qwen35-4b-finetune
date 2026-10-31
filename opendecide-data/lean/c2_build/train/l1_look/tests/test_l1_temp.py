"""CPU tests of the serving-temperature fit (RULING_L1_PRELOOK item 1: sampler + pack + register groups, calibrate.GRID argmin, then clip) and of its
application (calibrate.scaled). Dev-shaped synthetic data only."""
from __future__ import annotations

import ast
import math
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.dont_write_bytecode = True
TESTS = Path(__file__).resolve().parent
PKG = TESTS.parent
TRAIN = PKG.parent
LEAN = TRAIN.parents[1]
for p in (str(TRAIN), str(TESTS)):
    sys.path.insert(0, p)

from l1_look import l1temp as LT  # noqa: E402


def calibrate_source():
    """The real calibrate.py `scaled`, `nll` and `GRID`, taken from its source by AST (the file is a script: it is not imported)."""
    tree = ast.parse((LEAN / "calibrate.py").read_text())
    ns = {"math": math}
    for n in tree.body:
        if (isinstance(n, ast.FunctionDef) and n.name in ("scaled", "nll")) or \
                (isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "GRID" for t in n.targets)):
            exec(compile(ast.Module([n], []), "calibrate.py", "exec"), ns)
    return ns


CAL = calibrate_source()


def world(t_true, n_packs=12, n_regs=5, per=6, seed=0, qtype="noul", with_family=True):
    """Mixdev-shaped rows (one sampler S5, packs, registers) with predictions of a known true temperature: gold ~ softmax(z / t_true), served p = softmax(z)."""
    rng = np.random.default_rng(seed)
    rows, preds = [], {}
    k = 2 if qtype == "noul" else 3
    for g in range(n_packs):
        for i in range(per):
            z = rng.normal(0, 2.0, size=k)
            p = np.exp(z - z.max())
            p /= p.sum()
            q = np.exp(z / t_true - (z / t_true).max())
            q /= q.sum()
            gi = int(rng.choice(k, p=q))
            rid = f"r{g}-{i}"
            meta = {"sampler": "S5", "domain_pack": f"pk{g}", "format_style": f"fs{(g + i) % n_regs}", **({"family": f"T{g % 4:02d}"} if with_family else {})}
            if qtype == "noul":
                rows.append({"id": rid, "qtype": "noul", "gold": 1 if gi == 0 else 0, "options": None, "meta": meta})
                preds[rid] = {"yes": float(p[0]), "no": float(p[1])}
            else:
                opts = ["a", "b", "c"]
                rows.append({"id": rid, "qtype": "choice", "gold": opts[gi], "options": opts, "meta": meta})
                preds[rid] = dict(zip(opts, map(float, p)))
    return rows, preds


# ------------------------------------------------------------------ equalities with calibrate.py
def test_grid_is_calibrates_grid_and_scaled_is_calibrates_scaled():
    assert LT.CAL_GRID == CAL["GRID"] and LT.CAL_GRID[0] == 0.25 and LT.CAL_GRID[-1] == 10.0 and len(LT.CAL_GRID) == 196
    for probs, T in (({"yes": 0.7, "no": 0.3}, 1.0), ({"a": 0.6, "b": 0.3, "c": 0.1}, 1.2), ({"x": 0.999999, "y": 1e-9}, 0.8), ({"a": 0.5, "_k": 9.0, "b": 0.5}, 1.3)):
        a, b = LT.scaled(probs, T), CAL["scaled"](probs, T)
        assert a.keys() == b.keys() and all(a[k] == pytest.approx(b[k], rel=0, abs=1e-15) for k in a)
    r = LT.apply_T({"yes": 0.7, "no": 0.3}, "noul", {"noul": 1.0, "choice": 1.3})
    assert r == pytest.approx({"yes": 0.7, "no": 0.3}, abs=1e-12)                     # T = 1 only renormalises
    c = LT.apply_T({"a": 0.6, "b": 0.3, "c": 0.1}, "choice", {"noul": 0.8, "choice": 1.3})
    assert c == pytest.approx(CAL["scaled"]({"a": 0.6, "b": 0.3, "c": 0.1}, 1.3), abs=1e-12)


@pytest.mark.parametrize("qtype", ["noul", "choice"])
def test_group_nll_is_bit_for_bit_calibrate_nll(qtype):
    rows, preds = world(1.2, qtype=qtype)
    sel = [r for r in rows if r["qtype"] == qtype]
    members = LT.group_members(sel, LT.group_ids)
    terms = LT.terms_table(sel, preds)
    for T in (0.25, 0.8, 1.0, 1.3, 4.55, 10.0):
        for gid, idx in list(members.items())[:6]:
            tot = 0.0
            for i in idx:
                tot -= terms[T][i]
            mine = tot / max(1, len(idx))
            ref = CAL["nll"]([(sel[i], preds[sel[i]["id"]]) for i in idx], T)
            assert mine == ref, (gid, T)


def reference_fit(rows, preds, qtype, group_fn):
    """The ruling written out with calibrate's own functions and plain python: median over groups of calibrate.nll, first argmin, then clip."""
    sel = [r for r in rows if r["qtype"] == qtype]
    g = {}
    for r in sel:
        for gid in group_fn(r):
            g.setdefault(gid, []).append((r, preds[r["id"]]))
    M = {T: float(np.median([CAL["nll"](items, T) for items in g.values()])) for T in CAL["GRID"]}
    raw = min(CAL["GRID"], key=lambda t: M[t])
    return raw, min(1.3, max(0.8, raw)), len(g)


@pytest.mark.parametrize("t_true,qtype", [(1.0, "noul"), (1.2, "noul"), (0.9, "choice"), (1.15, "choice"), (2.0, "noul"), (0.5, "choice")])
def test_fit_equals_the_ruling_written_out_with_calibrate_functions(t_true, qtype):
    rows, preds = world(t_true, qtype=qtype, seed=3)
    fit = LT.fit_type(rows, preds, qtype)
    raw, clipped, n = reference_fit(rows, preds, qtype, LT.group_ids)
    assert fit["T_raw"] == raw and fit["T"] == clipped and fit["n_groups"] == n


def test_the_argmin_is_taken_on_the_wide_grid_then_clipped():
    rows, preds = world(2.0, qtype="noul", seed=4)              # the NLL optimum is far above 1.3
    fit = LT.fit_type(rows, preds, "noul")
    assert fit["T_raw"] > 1.3 and fit["T"] == 1.3
    rows, preds = world(0.5, qtype="choice", seed=5)
    fit = LT.fit_type(rows, preds, "choice")
    assert fit["T_raw"] < 0.8 and fit["T"] == 0.8
    rows, preds = world(1.0, qtype="noul", seed=6, per=8)
    fit = LT.fit_type(rows, preds, "noul")
    assert 0.8 <= fit["T"] <= 1.3 and fit["T"] == min(1.3, max(0.8, fit["T_raw"])) and fit["M_at_T_raw"] <= fit["M_at_1.0"]


def test_ties_take_the_first_grid_value_then_clip():
    flat = [{"id": f"t{i}", "qtype": "noul", "gold": i % 2, "options": None,
             "meta": {"sampler": "S5", "domain_pack": f"pk{i % 4}", "format_style": f"fs{i % 3}"}} for i in range(60)]
    fp = {r["id"]: {"yes": 0.5, "no": 0.5} for r in flat}
    fit = LT.fit_type(flat, fp, "noul")
    assert fit["T_raw"] == 0.25 and fit["T"] == 0.8                  # every T ties on uniform predictions: calibrate.py's first-T rule, then the clip


# ------------------------------------------------------------------ the groups
def test_groups_are_the_namespaced_union_of_sampler_pack_register():
    row = {"meta": {"sampler": "S5", "domain_pack": "pk-x", "format_style": "runbook/text", "family": "T28"}}
    assert LT.group_ids(row) == ["sampler:S5", "pack:pk-x", "register:runbook/text"]
    assert LT.group_ids({"meta": {"sampler": "S5", "domain_pack": "pk-x", "format_style": None}}) == ["sampler:S5", "pack:pk-x"]   # no register value: no register group
    assert LT.group_ids({"meta": {"domain_pack": "", "format_style": "f"}}) == ["register:f"]
    assert LT.group_ids({}) == []
    assert LT.family_group(row) == ["family:T28"]                     # the family key exists for the report-only fit only
    rows, preds = world(1.0, n_packs=10, n_regs=4, qtype="noul")
    fit = LT.fit_type(rows, preds, "noul")
    assert fit["groups_per_kind"] == {"pack": 10, "register": 4, "sampler": 1} and fit["n_groups"] == 15
    # a pack name equal to a register name is two groups (namespaced), not one
    r2 = [{**r, "meta": {**r["meta"], "domain_pack": "same", "format_style": "same"}} for r in rows]
    assert LT.fit_type(r2, preds, "noul")["groups_per_kind"] == {"pack": 1, "register": 1, "sampler": 1}


def test_a_group_of_one_row_counts_and_fewer_than_two_groups_stop():
    one_each = [{"id": f"q{i}", "qtype": "noul", "gold": i % 2, "options": None, "meta": {"sampler": "S5", "domain_pack": f"pk{i}", "format_style": None}}
                for i in range(4)]
    fp = {r["id"]: {"yes": 0.7, "no": 0.3} for r in one_each}
    assert LT.fit_type(one_each, fp, "noul")["n_groups"] == 5        # 4 packs of ONE row each + the sampler group: no minimum size
    lone = [{"id": "x", "qtype": "choice", "gold": "a", "options": ["a", "b"], "meta": {"sampler": "S5"}}]
    with pytest.raises(ValueError, match="at least 2"):
        LT.fit_type(lone, {"x": {"a": 0.5, "b": 0.5}}, "choice")      # one group only (the sampler): no fallback
    with pytest.raises(ValueError, match="at least 2"):
        LT.fit_type([], {}, "noul")
    assert LT.group_counts(one_each) == {"noul": 5, "choice": 0}


def test_missing_prediction_is_an_error():
    rows, preds = world(1.0, qtype="noul")
    preds.pop(rows[0]["id"])
    with pytest.raises(ValueError, match="no prediction"):
        LT.fit_type(rows, preds, "noul")


def test_types_are_fitted_separately_and_report_only_fits_are_stored():
    r1, p1 = world(1.2, qtype="choice", seed=7)
    r2, p2 = world(0.9, qtype="noul", seed=8)
    r2 = [{**r, "id": "n" + r["id"]} for r in r2]
    p2 = {"n" + k: v for k, v in p2.items()}
    out = LT.fit_all(r1 + r2, {**p1, **p2})
    b, rep = out["binding"], out["report_only"]
    assert LT.T_of(b) == {"noul": b["noul"]["T"], "choice": b["choice"]["T"]} and b["choice"]["T"] >= b["noul"]["T"]
    assert set(rep) == {"family", "pack_only", "register_only"} and rep["family"]["noul"]["n_groups"] == 4
    assert "n_groups" in rep["pack_only"]["choice"]
    assert out["binding"]["noul"]["n_groups"] != rep["family"]["noul"]["n_groups"]           # the family key is NOT the binding grouping
    assert LT.SHIPPED_C1_A5["noul"] == 1.0 and LT.SHIPPED_C1_A5["choice"] == 1.0
    assert "RULING_L1_PRELOOK item 1" in LT.RULE and "clip(T_raw, 0.8, 1.3)" in LT.RULE


def test_rows_outside_the_fit_set_do_not_move_the_fit():
    rows, preds = world(1.2, qtype="noul", seed=9)
    fam = {r["id"]: r["meta"]["family"] for r in rows}
    keep = [r for r in rows if fam[r["id"]] != "T03"]
    a = LT.fit_type(keep, preds, "noul")
    b = LT.fit_type([r for r in rows if r["meta"]["family"] != "T03"], preds, "noul")
    assert a == b
    c = LT.fit_type(rows, preds, "noul")
    assert c["n_rows"] > a["n_rows"]
