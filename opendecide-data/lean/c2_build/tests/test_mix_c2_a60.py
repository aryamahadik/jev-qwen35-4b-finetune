"""Tests for Ruling A60 in mix_c2.py: the pooled spec 3.18 complement-twin shares asserted on the final mix (implicit >= 25%,
antonym >= 30%, syntactic <= 45% over the complement twins of GB + MD + RTW that enter), the repeat of A60 (c)-(e) on a trim that
broke them, and the refusal when they still do not hold. In memory only. Run from c2_build:
  ../../.venv/bin/python -B -m pytest -q tests/test_mix_c2_a60.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mix_c2 as m  # noqa: E402
from negtwins import a60 as A  # noqa: E402
from test_c2_select import fam_rows  # noqa: E402
from test_mix_c2 import flow  # noqa: E402,F401  (the in-memory build fixture)


def twin(block, i, kind, role="complement", pattern=None, base=None):
    base = base or f"{block}b{i % 40}"
    return {"id": f"{block}t{i}{kind[0]}{role[0]}", "call_id": base, "group_id": f"g-{base}", "_block": block, "role": role, "qtype": "noul",
            "gold": 1 if role == "complement" else 0, "source": "c2_x", "state": f"s{i}", "instructions": f"Is it not {i}?", "card": "",
            "options": None,
            "meta": {"twin_of": base, "negtwin": {"pattern": pattern or f"PAT|{kind}|{i}", "kind": kind if role == "complement" else "equiv"}}}


def mix(counts, equiv=0, other=20):
    """Rows of a mix: complement twins per kind spread over GB / MD / RTW, equiv twins, base rows and T28 rows. -> rows, rels."""
    rows, i = [], 0
    for kind, n in counts.items():
        for _ in range(n):
            rows.append(twin(("GB", "MD", "RTW")[i % 3], i, kind))
            i += 1
    for _ in range(equiv):
        rows.append(twin(("GB", "MD", "RTW")[i % 3], i, "equiv", role="equiv"))
        i += 1
    tw = list(rows)
    rows += [{"id": f"{b}b{k}", "call_id": f"{b}b{k}", "_block": blk, "role": "base", "qtype": "noul", "gold": 1, "source": "c2_x", "meta": {}}
             for b, blk in (("GB", "GB"), ("MD", "MD"), ("RTW", "replay")) for k in range(40)]          # the bases the twins name
    rows += [{"id": f"T28x{k}", "call_id": f"T28x{k}", "_block": "T28", "role": "base", "qtype": "noul", "gold": 1, "source": "c2_t28", "meta": {}}
             for k in range(other)]
    rels = [{"a": r["meta"]["twin_of"], "b": r["id"], "type": r["role"]} for r in tw]
    return rows, rels


def kinds(rows):
    c = Counter(m.a60_kind(r) for r in rows if m.a60_kind(r))
    return {k: c.get(k, 0) for k in A.KINDS}


def test_only_complement_twins_of_gb_md_rtw_count():
    assert m.A60_BLOCKS == ("GB", "MD", "RTW")
    t = twin("GB", 1, "antonym")
    assert m.a60_kind(t) == "antonym"
    assert m.a60_kind(t | {"_block": "RTW"}) == "antonym" and m.a60_kind(t | {"_block": "MD"}) == "antonym"
    assert m.a60_kind(t | {"_block": "T37b"}) is None and m.a60_kind(t | {"_block": "replay"}) is None     # another block
    assert m.a60_kind(twin("GB", 2, "implicit", role="equiv")) is None                                          # an equiv twin
    assert m.a60_kind({"id": "x", "_block": "GB", "role": "base", "meta": {}}) is None                          # a base row


def test_shares_hold_vacuous_and_unknown_kind():
    rows, _ = mix({"antonym": 27, "implicit": 33, "syntactic": 30})
    rep, p = m.a60_shares(rows)
    assert p == [] and rep["by_kind"] == {"syntactic": 30, "implicit": 33, "antonym": 27} and rep["complement_twins"] == 90
    assert rep["shares"] == {"syntactic": 0.3333, "implicit": 0.3667, "antonym": 0.3}
    assert set(rep["by_block"]) == {"GB", "MD", "RTW"}
    rep, p = m.a60_shares([r for r in rows if r["_block"] == "T28"])
    assert p == [] and rep.get("vacuous") is True                                    # no complement twin in the mix: nothing to hold
    bad = rows + [twin("GB", 999, "mystery")]
    assert any("without a known kind" in x for x in m.a60_shares(bad)[1])


@pytest.mark.parametrize("counts,words", [({"antonym": 20, "implicit": 100, "syntactic": 20}, {"antonym"}),
                                          ({"antonym": 30, "implicit": 23, "syntactic": 40}, {"implicit"}),
                                          ({"antonym": 10, "implicit": 20, "syntactic": 70}, {"antonym", "implicit", "syntactic"})])
def test_every_bar_is_asserted(counts, words):
    rep, p = m.a60_shares(mix(counts)[0])
    assert {w for w in ("antonym", "implicit", "syntactic") if any(w in x for x in p)} == words and all("A60" in x for x in p)


def test_bars_exactly_on_the_edge_hold():
    assert m.a60_shares(mix({"antonym": 30, "implicit": 25, "syntactic": 45})[0])[1] == []
    assert m.a60_shares(mix({"antonym": 29, "implicit": 25, "syntactic": 45})[0])[1]                           # 29 / 99 = 29.3%: below 30%


def test_enforce_leaves_a_mix_that_holds_untouched():
    rows, rels = mix({"antonym": 27, "implicit": 19, "syntactic": 26}, equiv=10)             # the dry-run's realised pool: bars hold
    r2, l2, info = m.a60_enforce(rows, rels)
    assert r2 is rows and l2 is rels and info["trimmed"] == 0 and info["before"]["problems"] == []


def test_enforce_repeats_a60_on_a_trim_that_broke_the_shares():
    rows, rels = mix({"antonym": 20, "implicit": 120, "syntactic": 110}, equiv=15)           # a trim took antonym twins: 8% of the pool
    assert m.a60_shares(rows)[1]
    orig_ids = {r["id"] for r in rows}
    r2, l2, info = m.a60_enforce(rows, rels)
    k = kinds(r2)
    assert A.exact_problems(k) == [] and m.a60_shares(r2)[1] == []
    assert k["antonym"] == 20 and sum(k.values()) == A.n_c(20) == 66                          # all antonym twins stay, N_c = floor(20 / 0.30)
    assert info["trimmed"] == 250 - 66
    # hash-earliest per kind
    for kind in ("implicit", "syntactic"):
        pool = sorted((A.trim_key(r["meta"]["twin_of"], r["meta"]["negtwin"]["pattern"]), r["id"]) for r in rows if m.a60_kind(r) == kind)
        assert {r["id"] for r in r2 if m.a60_kind(r) == kind} == {i for _k, i in pool[:k[kind]]}
    # removal only: base rows, other blocks and equiv twins stay; edges of the dropped twins go
    assert {r["id"] for r in r2} <= orig_ids
    assert all(r["id"] in {x["id"] for x in r2} for r in rows if m.a60_kind(r) is None)
    ids = {r["id"] for r in r2}
    assert all(x["b"] in ids and x["a"] in ids for x in l2)
    assert {x["b"] for x in l2} == {r["id"] for r in r2 if r["meta"].get("negtwin")}
    assert [r for r in r2 if m.a60_kind(r)] == [r for r in rows if r["id"] in {q["id"] for q in r2} and m.a60_kind(r)]    # nothing edited


def test_enforce_with_no_antonym_twin_lets_no_complement_twin_in():
    rows, rels = mix({"implicit": 60, "syntactic": 60}, equiv=12)
    r2, l2, info = m.a60_enforce(rows, rels)
    assert kinds(r2) == {"syntactic": 0, "implicit": 0, "antonym": 0}
    assert sum(1 for r in r2 if r["role"] == "equiv") == 12 and info["choose"]["compliant"] is False
    assert m.a60_shares(r2)[1] == [] and m.a60_shares(r2)[0].get("vacuous") is True


# ---- the end-to-end mixer: finish() trims, gates() asserts -------------------------------------------------------------------
def inject(monkeypatch, counts, equiv=0):
    """Append twin rows to the mix after the budget trim (as if the blocks had entered with them)."""
    orig = m.budget_trim
    added = {}

    def bt(a, rows, rels, ntok, pools, parts, ctx, rep, probs):
        rows, rels = orig(a, rows, rels, ntok, pools, parts, ctx, rep, probs)
        extra, erel = mix(counts, equiv=equiv, other=0)
        extra = [r for r in extra if r["id"].startswith(("GBt", "MDt", "RTWt"))]
        erel = [x for x in erel if x["b"] in {r["id"] for r in extra}]
        ntok.update({r["id"]: 200 for r in extra})
        added["n"] = len(extra)
        return rows + extra, rels + erel
    monkeypatch.setattr(m, "budget_trim", bt)
    return added


def test_finish_repeats_a60_after_the_trims_and_the_final_mix_holds(flow, monkeypatch):
    args, writes, inp = flow
    added = inject(monkeypatch, {"implicit": 60, "syntactic": 60}, equiv=6)                    # no antonym twin: nothing may enter
    rep = m.build(args())
    assert rep["a60_trim"]["trimmed"] == 120 and rep["a60_trim"]["before"]["problems"]
    assert rep["a60_pooled_shares"]["problems"] == [] and rep["a60_pooled_shares"]["complement_twins"] == 0
    assert not [p for p in rep["problems"] if "A60" in p]
    assert "after_a60" in rep["replay_rule"]                                                   # the replay followed the smaller mix
    assert added["n"] == 126


def test_gates_refuse_when_the_shares_do_not_hold_on_the_final_mix(flow, monkeypatch):
    args, writes, inp = flow
    inject(monkeypatch, {"implicit": 60, "syntactic": 60})
    monkeypatch.setattr(m, "a60_enforce", lambda rows, rels: (rows, rels, {"trimmed": 0, "before": {}}))     # a trim nobody repaired
    rep = m.build(args())
    bad = [p for p in rep["problems"] if "A60 pooled spec 3.18" in p]
    assert any("antonym" in p for p in bad)                                                    # --final refuses on any problem
    with pytest.raises(SystemExit, match="--final refused"):
        m.write_outputs(args(final=True), rep, [], [])


def test_dry_run_without_twins_reports_a_vacuous_pool(flow):
    args, writes, inp = flow
    rep = m.build(args())
    assert rep["a60_pooled_shares"].get("vacuous") is True and rep["a60_trim"]["trimmed"] == 0
    assert not [p for p in rep["problems"] if "A60" in p]
