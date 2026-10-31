"""Tests for A69 (iii) / (f)(iv), as adopted (A80 b): the mixer's re-selection (agent-tier cap, budget trim) re-runs the A69 swap step (c) with its
guard and the faithful drop-only repair step (d) (a69_faithful.stage2) on the trimmed units, with the select_family rules. In memory only. Run from lean/:
  HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/tests/test_c2_select_a69_trim.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import a49c  # noqa: E402
import a69_faithful as a69f  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
import mix_c2 as m  # noqa: E402
from test_c2_select_a69 import FAM, pool  # noqa: E402

SEED = 20261013


def record(n=700, target=500, seed=5, yn_share=0.0, ntok=None, repair=False):
    rows, rels, probs, pg = pool(n, seed=seed, tag_p=0.8, k=4, yn_share=yn_share)
    rec = sel.select_family(FAM, rows, rels, pg, target, probs=probs, repair=repair, ntok=ntok if ntok is not None else {r["id"]: 700 for r in rows})
    by = {r["id"]: r for r in rows}
    chosen = [by[i] for i in rec["selected_ids"]]
    trap = rec["parts"][0].get("trap") or {}
    for r in chosen:
        r["meta"] = dict(r["meta"]) | {"crowd_pg": rec["crowd_pg"][r["id"]], "difficulty_bin": rec["difficulty_bin"][r["id"]],
                                       "pg_bin": rec["pg_bin"][r["id"]], "trap": {"treated": r["id"] in trap, "type": trap.get(r["id"])}}
    pgm = {r["id"]: r["meta"]["crowd_pg"] for r in chosen}
    return chosen, pgm, rec


def toks(rows, lo=700, hi=940):
    return {r["id"]: (lo if i % 2 else hi) for i, r in enumerate(rows)}               # mean 820 > the 800 bar


def test_trim_runs_the_guarded_swap_and_the_faithful_repair_with_the_select_family_arguments(monkeypatch):
    chosen, pgm, rec = record()
    calls = []
    real = a69f.stage2

    def stage2(fam, rows, rels, units, res, treated, type_order, weight, pg, pgbins, ntok, target, key, seed, repair=True, plugin=None):
        calls.append({"fam": fam, "seed": seed, "key": key, "ntok": ntok, "repair": repair, "treated": dict(treated), "type_order": list(type_order),
                      "weight": weight, "pgbins": dict(pgbins), "target": target})
        return real(fam, rows, rels, units, res, treated, type_order, weight, pg, pgbins, ntok, target, key, seed, repair=repair, plugin=plugin)
    monkeypatch.setattr(a69f, "stage2", stage2)
    monkeypatch.setattr(a49c, "swap_balance", lambda *a, **k: (_ for _ in ()).throw(AssertionError("the draft swap is not the A69 (c) swap")))
    monkeypatch.setattr(a49c, "repair_drop_only", lambda *a, **k: (_ for _ in ()).throw(AssertionError("the draft repair is not the A69 (d) repair")))
    nt = toks(chosen)
    out = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.7), ntok=nt)
    assert len(calls) == 1
    c = calls[0]
    assert c["fam"] == FAM and c["seed"] == sel.SEED and c["ntok"] is nt and c["repair"] is True      # fam from the part key
    assert c["type_order"] == rec["parts"][0]["trap_rank"] and c["treated"]                             # the recorded type order and treatment
    assert c["pgbins"] == {r["id"]: r["meta"]["pg_bin"] for r in chosen}                                 # the record's own p_g bins, not a recomputation from the rounded p_g
    a = out["a69"][0]
    assert a["swap"] is not None and a["repair"]["rows_dropped"] >= 0 and "moves" in a["repair"] and a["version"] == 1
    assert set(a["report_checks_additions"]) == set(a69f.F_CHECKS)


def test_trim_repair_drops_only_and_meets_the_token_bar():
    chosen, pgm, rec = record()
    nt = toks(chosen)
    t = int(len(chosen) * 0.7)
    off = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], t, ntok=nt, repair=False)
    on = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], t, ntok=nt)
    assert on["a69"][0]["repair"]["rows_dropped"] > 0 and off["a69"][0]["repair"].startswith("not run")
    assert len(on["selected_ids"]) < len(off["selected_ids"]) <= t                                  # may end short of the target, nothing refills
    by = {r["id"]: r for r in chosen}
    mean = sum(nt[i] for i in on["selected_ids"]) / len(on["selected_ids"])
    mean_off = sum(nt[i] for i in off["selected_ids"]) / len(off["selected_ids"])
    assert mean <= 800 + 1e-9 < mean_off
    assert set(on["bins"]) == set(on["selected_ids"]) and set(on["selected_ids"]) <= set(by)
    assert set(on["selected_ids"]) <= set(off["selected_ids"])                                       # rows only removed
    again = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], t, ntok=nt)
    assert again["selected_ids"] == on["selected_ids"]                                              # deterministic


def test_trim_hard_cap_and_type_cap_hold_after_the_repair():
    chosen, pgm, rec = record(900, 700, seed=9)
    nt = toks(chosen)
    out = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.6), ntok=nt)
    keep = set(out["selected_ids"])
    hard = sum(1 for b in out["bins"].values() if b == "hard")
    assert hard <= 0.30 * len(keep) + 1e-9
    assert out["a69"][0]["hard_rows"] == hard and out["a69"][0]["rows"] == len(keep)                # the record is the realised one
    n_t = Counter(t for i, t in out["parts"][0]["trap"].items() if i in keep)
    if n_t:
        assert max(n_t.values()) <= 0.35 * sum(n_t.values()) + 1e-9
    assert all(out["bins"][i] == "hard" for i in out["parts"][0]["trap"] if i in keep)


def test_trim_without_complete_token_counts_is_refused():
    chosen, pgm, rec = record()
    part = {i: v for i, v in toks(chosen).items()}
    part.pop(chosen[0]["id"])                                                                         # one row uncounted
    with pytest.raises(SystemExit, match="real tokens"):
        sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.7), ntok=part)
    with pytest.raises(SystemExit, match="real tokens"):
        sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.7))


def test_trim_swap_moves_the_yes_rate_toward_the_band_where_the_guard_allows():
    import random
    chosen, pgm, rec = record(400, 300, seed=13, yn_share=0.6)
    rnd = random.Random(13)
    for r in chosen:                                                                                  # yes rate depends on the bin: the label quotas cannot balance it
        if r["qtype"] == "noul":
            r["gold"] = 1 if rnd.random() < (0.9 if r["meta"]["difficulty_bin"] == "hard" else 0.2) else 0
    out = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.6), ntok=toks(chosen, 700, 700), repair=False)
    sw = out["a69"][0]["swap"]
    assert sw["swaps"] > 0 and sw["violation_after"] < sw["violation_before"]                          # the guarded swap step ran on the trimmed units
    assert sw["guard_rejections"] > 0                                                                 # and the guard (A69 c) refused the swaps that broke a passing check
    b, a = sw["totals_before"], sw["totals_after"]
    assert abs(a["yes"] / a["yes_no"] - 0.5) < abs(b["yes"] / b["yes_no"] - 0.5) and a["rows"] == b["rows"]     # swaps keep the row count
    assert sw["violation_after"] == 0.0                                                               # the yes rate, yes/no share and twin share are inside their bands again
    keep = set(out["selected_ids"])
    treated = out["parts"][0]["trap"]                                                                 # swapped-in treated units are still hard, at their own type
    assert all(out["bins"][i] == "hard" for i in treated if i in keep)
    assert len(out["selected_ids"]) <= int(len(chosen) * 0.6) and set(out["bins"]) == keep


def test_non_trap_part_is_untouched():
    rows, rels, probs, pg = pool(300, seed=2)
    rec = sel.select_family(FAM, rows, rels, pg, 200)                                                 # no probs: no trap data
    chosen = [r for r in rows if r["id"] in set(rec["selected_ids"])]
    pgm = {r["id"]: pg[r["id"]] for r in chosen}
    out = sel.reselect(chosen, [], pgm, rec["parts"], 150, ntok=toks(chosen))
    units = cs.units_of(chosen, [])
    ref = cs.select(chosen, units, pgm, 150, key=rec["parts"][0]["key"], seed=sel.SEED)
    assert out["selected_ids"] == [chosen[i]["id"] for u in ref["sel"] for i in units[u]] and not out["a69"]


# ---- the mixer -------------------------------------------------------------------------------------------------------------
def blocked(chosen):
    for r in chosen:
        r["_block"] = FAM
    return chosen


def test_ntok_of_uses_given_counts_and_counts_the_missing_only_with_a_log(monkeypatch):
    rr = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    assert m.ntok_of(rr, {"a": 1, "b": 2, "c": 3, "z": 9}) == {"a": 1, "b": 2, "c": 3}
    assert m.ntok_of(rr, {"a": 1}) is None and m.ntok_of(rr, None) is None
    seen = []

    def fake(ilog, rows, chunk=2000):
        seen.append([r["id"] for r in rows])
        return [10 * (len(x["id"]) + i) for i, x in enumerate(rows)]
    monkeypatch.setattr(m.mx, "token_counts", fake)
    cache = {"a": 5}
    got = m.ntok_of(rr, cache, ilog=object())
    assert seen == [["b", "c"]] and got["a"] == 5 and cache["b"] == got["b"] and set(got) == {"a", "b", "c"}
    assert m.ntok_of(rr, cache, ilog=object()) == got and len(seen) == 1                               # cached: not counted twice


def test_apply_targets_repairs_with_ntok_and_records_it():
    chosen, pgm, rec = record(700, 500, seed=7)
    blocked(chosen)
    nt = toks(chosen)
    parts = {FAM: [dict(p) for p in rec["parts"]]}
    t = int(len(chosen) * 0.7)
    out, _r, info = m.apply_targets(chosen, [], {FAM: t}, parts, ntok=nt)
    a = info[FAM]["a69"][0]
    assert a["repair"]["rows_dropped"] > 0 and a["repair"]["moves"] and len(out) < t               # the (d6) move log rides in the mixer's report
    assert sum(nt[r["id"]] for r in out) / len(out) <= 800 + 1e-9
    assert parts[FAM][0]["trap"] and parts[FAM][0]["trap_rank"]                                       # the next trim still has the data
    hard = sum(1 for r in out if r["meta"]["difficulty_bin"] == "hard")
    assert hard <= 0.30 * len(out) + 1e-9
    assert all(r["meta"]["pg_bin"] for r in out)                                                      # meta.pg_bin rides on every kept row
    tmap = parts[FAM][0]["trap"]
    assert all(r["meta"]["trap"] == {"treated": r["id"] in tmap, "type": tmap.get(r["id"])} for r in out)       # meta.trap follows the surviving treatment
    with pytest.raises(SystemExit, match="real tokens"):                                              # no counts and no log: the A69 repair cannot run, so the trim is refused
        m.apply_targets(blocked(record(700, 500, seed=7)[0]), [], {FAM: t}, {FAM: [dict(p) for p in rec["parts"]]})


def test_apply_targets_counts_tokens_through_the_log_when_given(monkeypatch):
    chosen, pgm, rec = record(700, 500, seed=7)
    blocked(chosen)
    nt = toks(chosen)
    calls = []

    def fake(ilog, rows, chunk=2000):
        calls.append(len(rows))
        return [nt[r["id"]] for r in rows]
    monkeypatch.setattr(m.mx, "token_counts", fake)
    out, _r, info = m.apply_targets(chosen, [], {FAM: int(len(chosen) * 0.7)}, {FAM: [dict(p) for p in rec["parts"]]}, ilog=object())
    assert calls == [len(chosen)] and info[FAM]["a69"][0]["repair"]["rows_pre_repair"] > 0
    other = [dict(r, id="x" + r["id"], _block="T28") for r in chosen[:50]]                           # a block that is not trimmed is not counted
    calls.clear()
    m.apply_targets(other, [], {"T28": 100}, {}, ilog=object())
    assert calls == []


def spy_apply(monkeypatch):
    seen = []

    def stub(rows, rels, targets, parts, seed=m.SEED, **kw):
        seen.append(kw)
        return rows, rels, {}
    monkeypatch.setattr(m, "apply_targets", stub)
    return seen


def test_budget_trim_passes_the_token_counts_to_the_proportional_step(monkeypatch):
    monkeypatch.setattr(m, "project_cost", lambda rows, rels, ntok, seed=m.SEED: {
        "total_usd": round(len(rows) * 0.01, 4), "train_usd": round(len(rows) * 0.01, 4), "rows": len(rows)})
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    monkeypatch.setattr(m, "META_MIN_ROWS", 10 ** 6)
    seen = spy_apply(monkeypatch)
    from test_mix_c2_a61_85 import args_for, mk, md_rows
    rows = md_rows({s: 100 for s in "abcdefgh"}) + [mk(f"a{i}", "T28", source="t28") for i in range(400)]
    nt = {r["id"]: 700 for r in rows}
    rep = {}
    m.budget_trim(args_for(24.0), rows, [], nt, {}, {}, {}, rep, [])
    assert seen and all(k.get("ntok") is nt for k in seen)


def test_the_agent_cap_after_refills_passes_the_token_counts(monkeypatch):
    seen = spy_apply(monkeypatch)
    monkeypatch.setattr(m, "plan_shares", lambda by: {"agent_cap": {"applied": True}, "targets": {"T28": 1}})
    monkeypatch.setattr(m, "replay_to_rule", lambda rows, rels, *a, **k: (rows, rels))
    monkeypatch.setattr(m, "budget_trim_a61", lambda a, rows, rels, *x, **k: (rows, rels))
    monkeypatch.setattr(m, "a60_enforce", lambda rows, rels: (rows, rels, {"trimmed": False}))
    monkeypatch.setattr(m, "arabic_cap_trim", lambda rows, rels: (rows, rels, {"trimmed": False}))
    monkeypatch.setattr(m, "tag_replay_unit", lambda rows, rels: (rows, rels, {}))
    monkeypatch.setattr(m.mx, "e2_final", lambda ctx, rows, rep: [])
    rows = [{"id": "a", "_block": "T28", "meta": {}}]
    nt = {"a": 5}
    rep, probs = {}, []
    m.tail_after_refill(None, rep, probs, rows, [], {}, {}, {}, nt, {}, set())
    assert seen and seen[0].get("ntok") is nt


def test_the_agent_cap_at_assembly_counts_tokens_through_the_log():
    import inspect
    src = inspect.getsource(m.assemble)
    assert 'apply_targets(rows, rels, plan["targets"], parts, ilog=ilog)' in src
