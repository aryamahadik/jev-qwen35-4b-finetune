"""Synthetic-fixture tests for crowd_select.py (spec 2.1 selection, G9 bins, chi-square, G5 list). CPU only."""
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import crowd_select as cs  # noqa: E402


def fam_rows(n_units=600, seed=1):
    """Synthetic family: yes/no rows over 4 wordings (complement twins in some units) + choice rows with 2-4 and 6
    options; per-card yes rates vary 20-80%."""
    rnd = random.Random(seed)
    rows, rels = [], []
    for u in range(n_units):
        card = u % 10
        rate = 0.2 + 0.6 * card / 9
        if u % 3:
            g = int(rnd.random() < rate)
            r = {"id": f"u{u}a", "call_id": f"c{u}", "qtype": "noul", "gold": g, "role": "base", "options": None,
                 "instructions": "Is it so?", "meta": {"wording_id": f"w{u % 4}", "card_id": f"k{card}"}}
            rows.append(r)
            if u % 5 == 0:
                rows.append(r | {"id": f"u{u}b", "gold": 1 - g})
                rels.append({"a": f"u{u}a", "b": f"u{u}b", "type": "complement"})
        else:
            k = [2, 3, 4, 6][u % 4]
            opts = [f"opt{j}" for j in range(k)]
            rows.append({"id": f"u{u}a", "call_id": f"c{u}", "qtype": "choice", "gold": opts[rnd.randrange(k)],
                         "options": opts, "role": "base", "instructions": "Which?", "meta": {"wording_id": "wc"}})
    return rows, rels


def test_units_join_call_id_and_relations():
    rows = [{"id": "a", "call_id": "x"}, {"id": "b", "call_id": "x"}, {"id": "c", "call_id": "y"},
            {"id": "d", "call_id": "z"}]
    us = cs.units_of(rows, [{"a": "c", "b": "d", "type": "inv"}])
    assert sorted(map(sorted, us)) == [[0, 1], [2, 3]]


def test_bins_and_pg():
    assert cs.bin_of(0.98) == "easy" and cs.bin_of(0.97) == "medium" and cs.bin_of(0.31) == "medium"
    assert cs.bin_of(0.30) == "hard" and cs.bin_of(None) == "na"
    r = {"qtype": "noul", "gold": 0}
    assert cs.p_gold(r, {"yes": 0.2, "no": 0.8}) == 0.8
    c = {"qtype": "choice", "gold": "B", "options": ["A", "B"]}
    assert cs.p_gold(c, {"A": 0.4, "B": 0.6}) == 0.6


def test_select_crowd_caps_balance_and_target():
    rows, rels = fam_rows()
    units = cs.units_of(rows, rels)
    rnd = random.Random(7)
    pg = {r["id"]: rnd.choice([0.99, 0.995, 0.6, 0.8, 0.5, 0.1, 0.2]) for r in rows}
    res = cs.select(rows, units, pg, 300, key="T")
    rep = res["report"]
    assert rep["rows"] <= 300 and rep["rows"] >= 270, rep
    assert rep["shares"].get("easy", 0) <= 0.25 + 1e-9 and rep["shares"].get("hard", 0) <= 0.30 + 1e-9
    ids = [i for u in res["sel"] for i in units[u]]
    yn = [rows[i]["gold"] for i in ids if rows[i]["qtype"] == "noul"]
    assert abs(sum(yn) / len(yn) - 0.5) <= 0.03, sum(yn) / len(yn)
    p = rep["chi2_label_x_bin"]["yes_no"]
    assert p is None or p > 0.01
    sel_ids = {rows[i]["id"] for i in ids}            # whole units only
    for x in rels:
        assert (x["a"] in sel_ids) == (x["b"] in sel_ids)


def test_select_deterministic_and_provisional():
    rows, rels = fam_rows(seed=3)
    units = cs.units_of(rows, rels)
    a = cs.select(rows, units, None, 200, key="F")
    b = cs.select(rows, units, None, 200, key="F")
    assert a["sel"] == b["sel"] and a["report"]["rows"] == 200 and set(a["budget"]) == {"na"}


def test_easy_thinning_keeps_about_30_percent():
    rows, rels = fam_rows(n_units=2000, seed=5)
    units = cs.units_of(rows, rels)
    pg = {r["id"]: 0.999 for r in rows}
    res = cs.select(rows, units, pg, 10000, key="E")
    kept = len(units) - res["easy_dropped_units"]
    assert 0.25 <= kept / len(units) <= 0.35


def test_g5_reread_lists_low_pg():
    rows, rels = fam_rows(n_units=100)
    units = cs.units_of(rows, rels)
    pg = {r["id"]: (0.01 if i % 4 == 0 else 0.9) for i, r in enumerate(rows)}
    g = cs.g5_reread(rows, units, list(range(len(units))), pg, "F1")
    assert g["n_low"] == sum(1 for v in pg.values() if v < 0.05) and len(g["sample_ids"]) <= 300


def test_chi2_none_on_single_bin():
    assert cs.chi2_p([[10, 10]]) is None
    assert cs.chi2_p([[50, 50], [50, 50]]) > 0.99


def test_load_crowd_mean_of_three_and_incomplete(tmp_path_factory):
    import json
    import shutil
    from mixio import InputLog
    d = HERE / "_tmp_crowd"
    d.mkdir(exist_ok=True)
    try:
        rows = [{"id": "a", "qtype": "noul", "gold": 1}, {"id": "b", "qtype": "choice", "gold": "X",
                                                           "options": ["X", "Y"]}]
        vals = {"c1": (0.9, 0.6), "e4b": (0.6, 0.3), "base": (0.3, 0.0)}
        dirs = {}
        for k, (pa, pb) in vals.items():
            f = d / f"{k}.jsonl"
            f.write_text(json.dumps({"id": "a", "probs": {"yes": pa, "no": 1 - pa}}) + "\n" +
                         json.dumps({"id": "b", "probs": {"X": pb, "Y": 1 - pb}}) + "\n")
            dirs[k] = f
        pg = cs.load_crowd(InputLog(), rows, dirs)
        assert abs(pg["a"] - 0.6) < 1e-9 and abs(pg["b"] - 0.3) < 1e-9
        (d / "base.jsonl").write_text(json.dumps({"id": "a", "probs": {"yes": 0.5, "no": 0.5}}) + "\n")
        import pytest
        with pytest.raises(SystemExit):
            cs.load_crowd(InputLog(), rows, dirs)
    finally:
        shutil.rmtree(d)


def test_ordinal_strata_keep_levels_uniform():
    rows = []
    for i in range(700):
        k = 5
        o = [f"{j}: lvl" for j in range(k)]
        rows.append({"id": f"o{i}", "call_id": f"c{i}", "qtype": "choice", "options": o, "gold": o[i % k],
                     "meta": {"option_level": {x: j for j, x in enumerate(o)}, "sampler": f"S{i % 2 + 1}"}})
    units = cs.units_of(rows, [])
    res = cs.select(rows, units, None, 300, key="O")
    from collections import Counter
    c = Counter((rows[i]["meta"]["sampler"], rows[i]["meta"]["option_level"][rows[i]["gold"]])
                for u in res["sel"] for i in units[u])
    for s in ("S1", "S2"):
        v = [c[(s, j)] for j in range(5)]
        assert max(v) - min(v) <= 1, v
