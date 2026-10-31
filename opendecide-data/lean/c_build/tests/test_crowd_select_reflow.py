"""Synthetic-fixture tests for the A27 (c) crowd_select.py fixes: bin-shortfall reflow and the G5 re-read sample.
CPU only. The pre-fix file (crowd_select.py.pre_reflow) is imported to prove a selection with no shortfall is
byte-identical to the old code."""
import importlib.machinery
import importlib.util
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import crowd_select as cs  # noqa: E402
from test_crowd_select import fam_rows  # noqa: E402

_ld = importlib.machinery.SourceFileLoader("crowd_select_pre_reflow", str(HERE.parent / "crowd_select.py.pre_reflow"))
_sp = importlib.util.spec_from_loader("crowd_select_pre_reflow", _ld)
old = importlib.util.module_from_spec(_sp)
_ld.exec_module(old)


def yn_family(n_units=2400, seed=11, hard_yes=0.9, med_share=0.6, hard_share=0.3):
    """Yes/no family over 4 wordings; every 10th unit is a complement pair (two rows, one unit). Bins by pg: medium
    rows have gold yes ~50%; hard rows are mostly gold yes (hard_yes), so the hard cell-balanced pool is small; the
    rest are easy rows."""
    rnd = random.Random(seed)
    rows, rels, pg = [], [], {}
    for u in range(n_units):
        x = rnd.random()
        b, p, rate = (("medium", 0.6, 0.5) if x < med_share else
                      ("hard", 0.1, hard_yes) if x < med_share + hard_share else ("easy", 0.99, 0.5))
        g = int(rnd.random() < rate)
        r = {"id": f"u{u}a", "call_id": f"c{u}", "qtype": "noul", "gold": g, "role": "base", "options": None,
             "instructions": "Is it so?", "meta": {"wording_id": f"w{u % 4}", "card_id": f"k{u % 10}"}}
        rows.append(r)
        pg[r["id"]] = p
        if u % 10 == 0:
            rows.append(r | {"id": f"u{u}b", "gold": 1 - g})
            pg[f"u{u}b"] = p
            rels.append({"a": f"u{u}a", "b": f"u{u}b", "type": "complement"})
    return rows, rels, pg


def cell_imbalance(rows, units, sel, bins):
    """{stratum: (max - min class count, tolerance)} over the selected rows (the selector's own cells and tolerance)."""
    cnt = defaultdict(Counter)
    for u in sel:
        for i in units[u]:
            r = rows[i]
            s = cs.stratum(r, bins[r["id"]])
            cnt[s][cs.label_class(r)] += 1
    out = {}
    for s, c in cnt.items():
        k = cs.n_classes(s)
        if k >= 2:
            out[s] = (max(c[j] for j in range(k)) - min(c[j] for j in range(k)),
                      1 if s[0] == "ord" else max(2, 0.02 * sum(c.values())))
    return out


def whole_units(rows, rels, units, sel):
    ids = {rows[i]["id"] for u in sel for i in units[u]}
    return all((x["a"] in ids) == (x["b"] in ids) for x in rels)


def test_reflow_fills_target_when_spare_supply_exists():
    rows, rels, pg = yn_family()
    units = cs.units_of(rows, rels)
    target = 1000
    a = old.select(rows, units, pg, target, key="R")
    b = cs.select(rows, units, pg, target, key="R")
    assert a["report"]["rows"] < target and not a["report"]["checks"]["total_eq_target"]   # the old shortfall
    rep = b["report"]
    assert rep["rows"] == target and rep["pass"], rep["checks"]
    assert b["reflow"] and b["reflow"][0]["bin"] == "medium" and sum(x["gained"] for x in b["reflow"]) > 0
    assert b["budget"] == a["budget"]                                     # the reported pre-reflow budgets
    sh = rep["shares"]
    assert sh.get("easy", 0) <= cs.CAP["easy"] + 1e-9 and sh.get("hard", 0) <= cs.CAP["hard"] + 1e-9
    assert sh.get("medium", 0) >= cs.MED_MIN - 1e-9
    ps = [p for p in [rep["chi2_label_x_bin"]["yes_no"], *rep["chi2_label_x_bin"]["choice_by_k"].values()]
          if p is not None]
    assert ps and all(p > cs.CHI_P for p in ps)
    assert whole_units(rows, rels, units, b["sel"])
    imb = cell_imbalance(rows, units, b["sel"], b["bins"])
    assert all(d <= t for d, t in imb.values()), {s: v for s, v in imb.items() if v[0] > v[1]}
    for bn, (y, n) in {bn: (Counter(rows[i]["gold"] for u in b["sel"] for i in units[u]
                                    if b["bins"][rows[i]["id"]] == bn)[1],
                            sum(1 for u in b["sel"] for i in units[u] if b["bins"][rows[i]["id"]] == bn))
                       for bn in ("medium", "hard", "easy")}.items():
        if n:
            assert abs(y - (n - y)) <= max(2, 0.02 * n), (bn, y, n)              # yes = no in every bin
    dropped = cs.easy_thinned(rows, units, b["bins"], "R")
    assert dropped and not dropped & set(b["sel"])                        # the 30% easy keep rule still holds
    hard_old = sum(1 for u in a["sel"] for i in units[u] if a["bins"][rows[i]["id"]] == "hard")
    hard_new = sum(1 for u in b["sel"] for i in units[u] if b["bins"][rows[i]["id"]] == "hard")
    assert hard_new <= hard_old                                           # the shortfall went to medium, not hard
    assert cs.select(rows, units, pg, target, key="R")["sel"] == b["sel"]   # deterministic


def test_reflow_infeasible_stays_short_and_keeps_caps():
    rows, rels, pg = yn_family(n_units=900, seed=12, med_share=0.3, hard_share=0.6)
    units = cs.units_of(rows, rels)
    target = 1200                                                         # above every balanced pool
    a = old.select(rows, units, pg, target, key="S")
    b = cs.select(rows, units, pg, target, key="S")
    rep = b["report"]
    assert rep["rows"] < target and not rep["checks"]["total_eq_target"]  # never padded past the rules
    assert rep["rows"] >= a["report"]["rows"]
    assert rep["shares"].get("easy", 0) <= cs.CAP["easy"] + 1e-9 and rep["shares"].get("hard", 0) <= cs.CAP["hard"] + 1e-9
    assert {x["bin"] for x in b["reflow"]} <= set(cs.REFLOW_ORDER) and b["reflow"][-1]["gained"] <= 0
    assert whole_units(rows, rels, units, b["sel"])
    if all(not x["kept"] for x in b["reflow"]):                            # every round undone: the old selection
        assert b["sel"] == a["sel"]
    over = {s: v for s, v in cell_imbalance(rows, units, b["sel"], b["bins"]).items() if v[0] > v[1]}
    over_old = {s: v for s, v in cell_imbalance(rows, units, a["sel"], a["bins"]).items() if v[0] > v[1]}
    assert set(over) <= set(over_old) and all(over[s][0] <= over_old[s][0] for s in over)   # balance never worse


def test_no_shortfall_is_byte_identical_to_pre_reflow():
    cases = 0
    for seed, target, key in ((1, 200, "F1"), (3, 150, "F2"), (5, 250, "F7"), (9, 120, "F9")):
        rows, rels = fam_rows(n_units=600, seed=seed)
        units = cs.units_of(rows, rels)
        rnd = random.Random(seed)
        for pg in ({r["id"]: rnd.choice([0.99, 0.6, 0.8, 0.5, 0.7, 0.2]) for r in rows}, None):
            a = old.select(rows, units, pg, target, key=key)
            if a["report"]["rows"] != target:
                continue
            b = cs.select(rows, units, pg, target, key=key)
            ia = json.dumps([rows[i]["id"] for u in a["sel"] for i in units[u]]).encode()
            ib = json.dumps([rows[i]["id"] for u in b["sel"] for i in units[u]]).encode()
            assert ia == ib and a["budget"] == b["budget"] and b["reflow"] == []
            assert {k: v for k, v in b["report"].items() if k != "reflow"} == a["report"]
            cases += 1
    assert cases >= 6, cases


def test_g5_sample_all_low_plus_300_selected():
    rows, rels = fam_rows(n_units=1500, seed=4)
    units = cs.units_of(rows, rels)
    pg = {r["id"]: (0.01 if i % 5 == 0 else 0.8) for i, r in enumerate(rows)}
    sel = list(range(0, len(units), 2))
    g = cs.g5_reread(rows, units, sel, pg, "F3")
    low = {x for x, v in pg.items() if v < cs.G5_PG}
    chosen = {rows[i]["id"] for u in sel for i in units[u]}
    assert set(g["low_ids"]) == low and g["n_low"] == len(low)
    s = set(g["sample_ids"])
    assert len(s) == cs.G5_N == g["n_sample"] and s <= chosen and not s & low
    rest = sorted(chosen - low, key=lambda x: cs.h64(cs.SEED, "F3", "g5", x))
    assert s == set(rest[:cs.G5_N])                                       # seeded, not hand-picked
    assert set(g["reread_ids"]) == low | s and g["n_reread"] == len(low) + cs.G5_N
    assert cs.g5_reread(rows, units, sel, pg, "F3") == g                 # deterministic
    few = cs.g5_reread(rows, units, sel[:40], pg, "F3")                  # fewer than 300 selected non-low rows
    fc = {rows[i]["id"] for u in sel[:40] for i in units[u]} - low
    assert set(few["sample_ids"]) == fc and set(few["low_ids"]) == low
