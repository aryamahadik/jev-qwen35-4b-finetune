"""Tests for c2_select.py and c2io.py (C2 crowd selection, A37 e). In memory only: no row, pool or file is written
(A37 f); the only disk reads are the guard's string checks. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_c2_select.py
"""
from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
from c2_kit import paths as kp  # noqa: E402


def fam_rows(fam="T28", n_units=600, seed=1, prefix=""):
    """A synthetic C2 family in memory: yes/no rows over 4 wordings (complement partners in some units, same
    call_id) + choice rows with 2-4 and 6 options; per-card yes rates 20-80%."""
    rnd = random.Random(seed)
    rows, rels = [], []
    for u in range(n_units):
        card = u % 10
        rate = 0.2 + 0.6 * card / 9
        base = {"call_id": f"{prefix}c{u}", "group_id": f"{prefix}g{u}", "source": "c2_" + fam.lower(),
                "role": "base", "state": f"s{u}", "card": "card"}
        meta = {"family": fam, "wording_id": f"w{u % 4}", "card_id": f"k{card}", "sampler": f"S{u % 4 + 1}"}
        if u % 3:
            g = int(rnd.random() < rate)
            r = base | {"id": f"{prefix}u{u}a", "qtype": "noul", "gold": g, "options": None,
                        "instructions": "Is it so?", "meta": dict(meta)}
            rows.append(r)
            if u % 5 == 0:
                rows.append(r | {"id": f"{prefix}u{u}b", "gold": 1 - g, "role": "complement"})
                rels.append({"a": f"{prefix}u{u}a", "b": f"{prefix}u{u}b", "type": "complement"})
        else:
            k = [2, 3, 4, 6][u % 4]
            opts = [f"opt{j}" for j in range(k)]
            rows.append(base | {"id": f"{prefix}u{u}a", "qtype": "choice", "gold": opts[rnd.randrange(k)],
                                "options": opts, "instructions": "Which?", "meta": dict(meta)})
    return rows, rels


def crowd(rows, seed=7, vals=(0.99, 0.995, 0.6, 0.8, 0.5, 0.1, 0.2)):
    rnd = random.Random(seed)
    return {r["id"]: rnd.choice(vals) for r in rows}


# ---- the guard and layout (c2io) ------------------------------------------------------------------------------------
@pytest.mark.parametrize("p", ["lean/ohs4_sealed/suite.jsonl", "lean/data/ohs3_parts/x.jsonl",
                               "lean/sealed_nd/score_nd.py", "lean/c_build/preread/x", "lean/logs/jev_raw.jsonl",
                               "bench/external_quarantine/a", "~/.claude/projects/x/memory.md"])
def test_guard_refuses_never_open(p):
    if p.startswith("~"):
        full = p
    elif p.startswith("lean/"):
        full = kp.REPO_ROOT / "opendecide-data" / p
    else:
        full = kp.REPO_ROOT / p
    assert c2io.refusal(full)


def test_guard_allows_c2_inputs_and_checks_names():
    assert c2io.refusal(c2io.C2_PARTS / "T28/out/candidates_c2.jsonl") is None
    assert c2io.refusal(c2io.LEAN / "logs/decontam_counts/pool_drops_r1.json") is None
    with pytest.raises(SystemExit):
        c2io.check_name("ohs4_r")
    with pytest.raises(SystemExit):
        c2io.check_name("preds_jev")
    assert c2io.check_name("c2_mixdev") == "c2_mixdev"
    with pytest.raises(c2io.C2Refused):
        c2io.C2InputLog().check(kp.LEAN / "ohs4_sealed" / "brief.md")


def test_targets_are_spec_2_1_and_5_1():
    assert sum(c2io.AGENT.values()) == 13600 and sum(c2io.EVERYDAY.values()) == 7000
    assert sum(c2io.PROGRAM.values()) == 20600 and len(c2io.PROGRAM) == 17
    assert c2io.T37B == {"T37b": 2000} and c2io.CARRY == {"F5": 1500, "F6": 1000, "F11": 1000, "F4": 500}
    assert sum(c2io.TARGETS.values()) == c2io.NEW_MAX == 26600 and max(c2io.PROGRAM.values()) == 2400
    assert set(c2io.WAVE1) | set(c2io.WAVE2) == set(c2io.TARGETS) | set(c2io.NEW_FAMILIES) and not set(c2io.WAVE1) & set(c2io.WAVE2)
    assert not set(c2io.TRANSFER_DEV) & set(c2io.TARGETS)
    assert c2io.NEW_FAMILIES == {"T40": 1333, "T41": 1166, "T42": 1333, "T43": 1166, "T44": 833, "T45": 833}
    assert c2io.ALL_TARGETS["GB"] == 15000 and c2io.ALL_TARGETS["MD"] == 12000 and c2io.ALL_TARGETS["RTW"] == 8000
    assert set(c2io.NEW_FAMILIES) | set(c2io.BLOCK_TARGETS) <= set(sel.TARGETS) and not set(c2io.BLOCK_TARGETS) & set(c2io.TARGETS)


def test_manifest_contract():
    got = {c2io.CAND: ("a" * 64, 10), c2io.REL: ("b" * 64, 3)}
    man = {"family": "T28", "files": {c2io.CAND: {"sha256": "a" * 64, "rows": 10},
                                      c2io.REL: {"sha256": "b" * 64, "rows": 3}}}
    assert c2io.manifest_problems("T28", man, got) == []
    bad = {"family": "T28", "files": {c2io.CAND: {"sha256": "c" * 64, "rows": 9}}}
    p = c2io.manifest_problems("T28", bad, got)
    assert any("sha256" in x for x in p) and any("10 rows" in x for x in p) and any("does not declare" in x for x in p)
    assert c2io.manifest_problems("T28", {}, got) == ["T28: MANIFEST has no 'files' record"]


def test_candidate_problems():
    rows, _ = fam_rows(n_units=30)
    assert c2io.candidate_problems("T28", rows) == []
    rows[0]["meta"]["sampler"] = "S5"
    rows[1]["meta"]["dev_only"] = True
    rows.append(dict(rows[2]))
    rows[3]["meta"] = dict(rows[3]["meta"], family="T29")
    p = c2io.candidate_problems("T28", rows)
    assert any("S5 / dev_only" in x and "2 " in x for x in p) and any("duplicate" in x for x in p)
    assert any("other families" in x for x in p)
    assert c2io.candidate_problems("T36", rows) == ["T36: transfer-dev family, never trained (spec 2.2)"]


def _snapshot(*paths):
    """(path, size, mtime) of every file under the given paths (absent paths give nothing)."""
    out = []
    for p in paths:
        if p.is_file():
            out.append((str(p), p.stat().st_size, p.stat().st_mtime_ns))
        elif p.is_dir():
            out += [(str(f), f.stat().st_size, f.stat().st_mtime_ns) for f in sorted(p.rglob("*")) if f.is_file()]
    return out


def test_writers_after_a38(tmp_path, monkeypatch):
    """A38 (13 Oct) froze OHS-4, so the writers pass the freeze guard. They still refuse never-open paths, paths
    outside lean/ and a PREREG text without A38, and the commands write only through c2io's guarded writers. Nothing
    reaches disk here: refused writes raise before any open, and the command runs use an empty C2 tree in tmp_path,
    with the writers and the progress log captured in memory."""
    before = _snapshot(sel.OUT, sel.LOG, sel.SHARDS, c2io.C2_PARTS)
    assert kp.a38_frozen()                                   # PREREG_FINAL.md holds the "Ruling A38" block
    kp.require_a38()
    c2io.require_a38()
    with pytest.raises(kp.DataBeforeFreeze):                 # the guard itself is unchanged
        c2io.write_json(sel.OUT / "never.json", {"x": 1}, prereg_text="no freeze in this text")
    with pytest.raises(kp.DataBeforeFreeze):
        c2io.write_jsonl(sel.OUT / "never.jsonl", [{"x": 1}], prereg_text="no freeze in this text")
    with pytest.raises(c2io.C2Refused):                      # never-open paths stay refused after A38
        c2io.write_json(kp.LEAN / "ohs4_sealed" / "never.json", {"x": 1})
    with pytest.raises(c2io.C2Refused):
        c2io.write_jsonl(kp.LEAN / "logs" / "jev_never.jsonl", [{"x": 1}])
    with pytest.raises(PermissionError):                     # outside lean/
        c2io.write_json(tmp_path / "never.json", {"x": 1})
    assert not (tmp_path / "never.json").exists()

    writes, logged = {}, []
    monkeypatch.setattr(c2io, "C2_PARTS", tmp_path / "c2_parts")           # no candidates on disk
    monkeypatch.setattr(c2io, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj) or "0")
    monkeypatch.setattr(c2io, "write_jsonl", lambda p, rows, prereg_text=None: writes.__setitem__(str(p), rows) or "0")
    monkeypatch.setattr(sel, "log_line", lambda path, msg: logged.append((str(path), msg)))
    sel.main(["select", "--fam", "T28"])                     # passes the guard; no candidates -> inputs record only
    assert writes == {str(sel.OUT / "select_inputs.json"): {"inputs": {}}}
    writes.clear()
    sel.main(["tasks", "--write-shards"])
    assert list(writes) == [str(sel.OUT / "crowd_tasks_c2.json")]
    t = writes[str(sel.OUT / "crowd_tasks_c2.json")]
    assert t["model"] == c2io.C1 and t["families"] == {} and t["estimate"]["reads"] == 0
    assert logged and all(p == str(sel.LOG) and m.startswith("c2_select: ") for p, m in logged)
    monkeypatch.setattr(kp, "PREREG", tmp_path / "prereg_without_a38.md")
    (tmp_path / "prereg_without_a38.md").write_text("> **Ruling A37 (13 Oct 2026)**\n", encoding="utf-8")
    with pytest.raises(kp.DataBeforeFreeze):                 # a PREREG without A38 still locks every command
        sel.main(["select", "--fam", "T28"])
    with pytest.raises(kp.DataBeforeFreeze):
        sel.main(["tasks", "--write-shards"])
    assert _snapshot(sel.OUT, sel.LOG, sel.SHARDS, kp.C2_PARTS) == before


# ---- the C1-only crowd ----------------------------------------------------------------------------------------------
def test_view_must_be_one_c1_view():
    v = {"settings": {"name": "q35_4b_main500k", "tta": False, "tta_choice": False, "tta_noul": False,
                      "perm_seed": None}}
    assert sel.view_problem(v) is None
    assert sel.view_problem({"settings": {**v["settings"], "name": "q35_4b_main500k_merged"}}) is None
    assert "C1-only" in sel.view_problem({"settings": {**v["settings"], "name": "q35_4b_pxE"}})
    assert "TTA" in sel.view_problem({"settings": {**v["settings"], "tta_choice": True}})
    assert sel.view_problem(None)


def test_c1_pg_is_c1_probability_on_gold_and_complete():
    rows = [{"id": "a", "qtype": "noul", "gold": 1}, {"id": "b", "qtype": "noul", "gold": 0},
            {"id": "c", "qtype": "choice", "gold": "X", "options": ["X", "Y"]}]
    probs = {"a": {"yes": 0.9, "no": 0.1}, "b": {"yes": 0.9, "no": 0.1}, "c": {"X": 0.3, "Y": 0.7}}
    assert sel.c1_pg(rows, probs) == {"a": 0.9, "b": 0.1, "c": 0.3}
    with pytest.raises(SystemExit, match="incomplete"):
        sel.c1_pg(rows, {"a": probs["a"]})


# ---- selection (crowd_select, unchanged) ----------------------------------------------------------------------------
def test_select_family_caps_balance_units_and_record():
    rows, rels = fam_rows()
    pg = crowd(rows)
    rec = sel.select_family("T28", rows, rels, pg, 300)
    rep = rec["report"]
    assert 270 <= rep["rows"] <= 300 and rec["seed"] == 20261013 and rec["key"] == "T28"
    assert rep["shares"].get("easy", 0) <= 0.25 + 1e-9 and rep["shares"].get("hard", 0) <= 0.30 + 1e-9
    assert rep["crowd_rule"].startswith("A37 (e)") and rec["crowd"] == {"c1": "q35_4b_main500k"}
    ids = set(rec["selected_ids"])
    yn = [r["gold"] for r in rows if r["id"] in ids and r["qtype"] == "noul"]
    assert abs(sum(yn) / len(yn) - 0.5) <= 0.03
    for x in rels:                                  # whole relation units only
        assert (x["a"] in ids) == (x["b"] in ids)
    assert rec["parts"] == [{"key": "T28", "ids": rec["selected_ids"]}]
    p = rep["chi2_label_x_bin"]["yes_no"]
    assert p is None or p > 0.01
    g5 = rec["g5"]
    assert g5["n_low"] == 0 and g5["n_sample"] <= 300      # no p_g < 0.05 in this crowd
    again = sel.select_family("T28", rows, rels, pg, 300)
    assert again["selected_ids"] == rec["selected_ids"]    # seeded, deterministic


def test_select_family_g5_lists_low_pg_and_refuses_s5():
    rows, rels = fam_rows(n_units=200)
    pg = {r["id"]: (0.01 if i % 4 == 0 else 0.7) for i, r in enumerate(rows)}
    rec = sel.select_family("T28", rows, rels, pg, 100)
    assert rec["g5"]["n_low"] == sum(1 for v in pg.values() if v < 0.05)
    rows[0]["meta"]["sampler"] = "S5"
    with pytest.raises(SystemExit, match="S5"):
        sel.select_family("T28", rows, rels, pg, 100)


def test_g13_exclusion_removes_whole_units():
    rows, rels = fam_rows(n_units=60)
    pair = rels[0]
    keep, info = sel.drop_excluded(rows, rels, {pair["b"]})
    ids = {r["id"] for r in keep}
    assert pair["a"] not in ids and pair["b"] not in ids and info["units_removed"] == 1 and info["rows_removed"] == 2
    rec = sel.select_family("T28", rows, rels, crowd(rows), 40, drop_ids={pair["a"]})
    assert pair["a"] not in rec["selected_ids"] and rec["exclude_ids"]["units_removed"] == 1


def test_drop_ids_of_refuses_a_g13_log_that_is_not_complete(tmp_path):
    """--exclude-ids reads G13 logs: a log whose "complete" is not True (False, missing, a string, not an object) is
    refused whole, naming the file; complete logs are merged. Real files through the guarded C2InputLog."""
    import json
    ok = tmp_path / "g13_ok.json"
    ok.write_text(json.dumps({"complete": True, "drop_ids": ["a", "b"]}))
    ok2 = tmp_path / "g13_ok2.json"
    ok2.write_text(json.dumps({"complete": True, "training_ids_to_drop": ["b", "c"]}))
    assert sel.drop_ids_of(c2io.C2InputLog(), [ok, ok2]) == {"a", "b", "c"}
    assert sel.drop_ids_of(c2io.C2InputLog(), None) == set()
    bad = {"g13_false.json": {"complete": False, "drop_ids": ["a"], "incomplete_why": ["x"]},
           "g13_missing.json": {"drop_ids": ["a"]},
           "g13_string.json": {"complete": "true", "drop_ids": ["a"]},
           "g13_one.json": {"complete": 1, "drop_ids": ["a"]},
           "g13_null.json": {"complete": None, "drop_ids": ["a"]},
           "g13_list.json": ["a"]}
    for name, body in bad.items():
        f = tmp_path / name
        f.write_text(json.dumps(body))
        with pytest.raises(SystemExit, match=name):          # the message names the file
            sel.drop_ids_of(c2io.C2InputLog(), [f])
        with pytest.raises(SystemExit, match="not complete"):
            sel.drop_ids_of(c2io.C2InputLog(), [ok, f])      # one bad log among good ones still refuses
    no_list = tmp_path / "g13_nolist.json"
    no_list.write_text(json.dumps({"complete": True}))
    with pytest.raises(SystemExit, match="no drop id list"):  # a complete log without an id list still refuses
        sel.drop_ids_of(c2io.C2InputLog(), [no_list])


def test_reselect_keeps_the_easy_keep_and_balance():
    rows, rels = fam_rows(n_units=900, seed=4)
    pg = crowd(rows, seed=3, vals=(0.99, 0.999, 0.6, 0.8, 0.5, 0.1))
    rec = sel.select_family("T28", rows, rels, pg, 500)
    chosen = set(rec["selected_ids"])
    sub = [r for r in rows if r["id"] in chosen]
    srel = [x for x in rels if x["a"] in chosen and x["b"] in chosen]
    units = cs.units_of(sub, srel)
    bins = {r["id"]: cs.bin_of(pg[r["id"]]) for r in sub}
    assert any(all(bins[sub[i]["id"]] == "easy" for i in u) for u in units)      # some all-easy units were kept
    assert cs.easy_thinned(sub, units, bins, "T28", 20261013) == set()           # same key + seed: none thinned again
    small = sel.reselect(sub, srel, pg, rec["parts"], 250)
    got = set(small["selected_ids"])
    assert got <= chosen and 230 <= len(got) <= 250 and small["parts"][0]["key"] == "T28"
    b = Counter(bins[i] for i in got)
    assert b["easy"] <= 0.25 * len(got) + 1e-9 and b["hard"] <= 0.30 * len(got) + 1e-9
    yn = [r["gold"] for r in sub if r["id"] in got and r["qtype"] == "noul"]
    assert abs(sum(yn) / len(yn) - 0.5) <= 0.03
    for x in srel:
        assert (x["a"] in got) == (x["b"] in got)


# ---- carry-over pools (spec 3.19) -----------------------------------------------------------------------------------
def f5_rows(n=300):
    rows, rels = [], []
    for u in range(n):
        g = u % 2
        meta = {"family": "F5", "wording_id": f"w{u % 3}", "sampler": "S1"}
        base = {"call_id": f"c{u}", "group_id": f"g{u}", "source": "c_f5", "qtype": "noul", "options": None,
                "instructions": "Is it so?", "role": "base", "meta": meta}
        if u % 3 == 0:          # complement + equiv unit (3 rows)
            rows += [base | {"id": f"{u}a", "gold": g}, base | {"id": f"{u}b", "gold": 1 - g, "role": "complement"},
                     base | {"id": f"{u}c", "gold": g, "role": "equiv"}]
            rels += [{"a": f"{u}a", "b": f"{u}b", "type": "complement"}, {"a": f"{u}a", "b": f"{u}c", "type": "equiv"}]
        elif u % 3 == 1:        # inv unit
            rows += [base | {"id": f"{u}a", "gold": g}, base | {"id": f"{u}b", "gold": g, "role": "attack"}]
            rels += [{"a": f"{u}a", "b": f"{u}b", "type": "inv"}]
        else:
            rows.append(base | {"id": f"{u}a", "gold": g})
    return rows, rels


def test_f5_carry_pool_is_complement_and_equiv_units_of_the_round1_selection():
    rows, rels = f5_rows()
    r1 = {r["id"] for r in rows if int(r["id"].rstrip("abc")) < 240}
    pool, prel, info = sel.carry_pool("F5", rows, rels, r1)
    us = cs.units_of(pool, prel)
    assert pool and all(len(u) == 3 for u in us)                   # only the 3-row complement + equiv units
    assert {r["id"].rstrip("abc") for r in pool} <= {str(u) for u in range(0, 240, 3)}
    assert info["units_left_out"]["not_round1_selected"] > 0 and all(x["type"] in ("complement", "equiv") for x in prel)
    assert sel.sel_key("F5") == "F5|c2carry" and sel.sel_key("T28") == "T28"


def test_f11_carry_prefers_xed_mams_units():
    rows, rels = fam_rows("F11", n_units=900, seed=9)
    for i, r in enumerate(rows):
        r["source"] = "c_f11"
        if int(r["id"][1:].rstrip("ab")) % 2 == 0:
            r["meta"]["text_source"] = {"dataset": "xed_en" if i % 3 else "mams"}
    pg = crowd(rows, seed=2)
    allids = {r["id"] for r in rows}
    small = sel.select_carry("F11", rows, rels, pg, 200, allids)        # the preferred units alone fill it
    assert all(sel.preferred("F11", r) for r in rows if r["id"] in set(small["selected_ids"]))
    assert len(small["parts"]) == 1 and small["parts"][0]["key"] == "F11|c2carry|pref"
    big = sel.select_carry("F11", rows, rels, pg, 600, allids)          # more than they can give: the rest fills
    ids = set(big["selected_ids"])
    pref = [r for r in rows if r["id"] in ids and sel.preferred("F11", r)]
    rest = [r for r in rows if r["id"] in ids and not sel.preferred("F11", r)]
    assert pref and rest and [p["key"] for p in big["parts"]] == ["F11|c2carry|pref", "F11|c2carry|rest"]
    assert big["report"]["rows"] == len(ids) <= 600 and big["report"]["checks"]["easy_le_25"]
    assert set(big["g5"]["sample_ids"]) <= ids


def test_manifest_declared_relation_file_must_exist():
    man = {"files": {c2io.CAND: {"sha256": "a" * 64, "rows": 10}, c2io.REL: {"sha256": "b" * 64, "rows": 3}}}
    p = c2io.manifest_problems("T28", man, {c2io.CAND: ("a" * 64, 10)})
    assert p == [f"T28: MANIFEST declares {c2io.REL}, which is not on disk"]
