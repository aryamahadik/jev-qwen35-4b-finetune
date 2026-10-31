"""A45 (b) tests: the T37b noise screen (drop only, never relabel). In memory; no Haiku, no network."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from t37b import builder as BL  # noqa: E402
from t37b import fixtures as FX  # noqa: E402
from t37b import noise as NZ  # noqa: E402
from t37b import select as SEL  # noqa: E402
from t37b.test_t37b import _flow, _yn  # noqa: E402


@pytest.fixture(scope="module")
def flow():
    return _flow(FX.rows(), source_cap=1.0, template_cap=1.0)


def test_none_blind_base_never_reaches_keep(flow):
    _plan, cands = flow
    for c in cands:
        rel = BL.relation_of(c.item.kind)
        part = 1 - c.item.base.row["gold"] if rel == "opposite" else c.item.base.row["gold"]
        for bad in (None, "maybe", "", {"answer": "unsure"}):
            for review in (None, "keep"):
                v, why = BL.decide(c, rel, rel, bad, _yn(part), review=review)
                assert v == "drop" and "no blind base answer" in why
        assert BL.decide(c, rel, rel, _yn(c.item.base.row["gold"]), _yn(part))[0] == "keep"


def test_score_row_rule():
    s = NZ.score_row
    assert s(1, [1, 1])["status"] == "clean"
    assert s(1, [0, 0])["drop"] and s(1, [0, None])["drop"] and s(0, [None, 1])["drop"]
    assert not s(1, [1, 0])["drop"] and s(1, [1, 0])["status"] == "split"
    assert not s(1, [1, None])["drop"] and s(1, [1, None])["status"] == "abstain"
    assert not s(1, [None, None])["drop"]
    assert s(1, [1, "unread"])["status"] == "unread" and not s(1, [0, "unread"])["drop"]     # never drop on missing evidence


def test_over_bar_is_strict_and_has_no_minimum():
    t = NZ.rate_table({"a": (100, 3), "b": (100, 4), "c": (1, 1), "d": (0, 0)})
    assert NZ.over_bar(t) == ["b", "c"]


def test_source_rates_come_only_from_the_screen():
    assert NZ.combine_sources(None) == []
    scr = {"sources": {"x": {"n_read": 100, "not_clean": 4, "drop": 1}, "y": {"n_read": 100, "not_clean": 3, "drop": 3},
                       "z": {"n_read": 0, "not_clean": 0, "drop": 0}}}
    assert NZ.combine_sources(scr) == ["x"] and NZ.combine_sources(scr, stat="drop") == []
    scr["sources"]["y"]["drop"] = 4
    assert NZ.combine_sources(scr, stat="drop") == ["y"]


def test_eligible_applies_the_screen(flow):
    rows = FX.rows()
    base_kw = dict(strict_inputs=False)
    full, _ = SEL.eligible(rows, **base_kw)
    assert full
    ids = [b.row["id"] for b in full]
    src = full[0].row["source"]
    b1, r1 = SEL.eligible(rows, deny_sources=[src], **base_kw)
    assert all(b.row["source"] != src for b in b1)
    b2, r2 = SEL.eligible(rows, deny_ids=[ids[0]], **base_kw)
    assert ids[0] not in {b.row["id"] for b in b2} and len(b2) == len(full) - 1
    b3, r3 = SEL.eligible(rows, allow_ids=ids[:2], **base_kw)       # a base with no blind answer equal to gold is out
    assert {b.row["id"] for b in b3} == set(ids[:2])
    assert any("noise screen" in k for k in r3["drop"])
    b4, _ = SEL.eligible(rows, allow_ids=[], **base_kw)
    assert b4 == []


def test_blocked_templates_are_never_planned(flow):
    plan, _ = flow
    bases, _ = SEL.eligible(FX.rows(), strict_inputs=False)
    tpls = sorted({i.template for i in plan})
    assert tpls
    blocked = {tpls[0]}
    plan2, _ = SEL.plan_block(bases, n_complement=len(plan), n_equiv=0, seed="a45", source_cap=1.0, template_cap=1.0,
                              blocked_templates=blocked)
    assert all(i.template not in blocked for i in plan2)


def test_score_reads_end_to_end(tmp_path):
    """Two fake readers over six rows: the drop list follows the rule and nothing is relabelled."""
    import json
    sys.path.insert(0, str(Path(__file__).resolve().parent / "noise_screen"))
    import score_reads as SR
    from c2_kit import chunker, g5h
    import pilot as PI
    gold = {f"r{i}": g for i, g in enumerate([1, 0, 1, 1, 0, 1])}
    rows = [{"id": i, "qtype": "noul", "state": f"text number {n} about something", "instructions": "Is it so?",
             "card": "- yes: a\n- no: b", "gold": g} for n, (i, g) in enumerate(gold.items())]
    ba, bb = g5h.make_reads(rows, "NS-test", seed="t", prompt=PI.G5H_PROMPT)
    plan = {  # row -> (reader A answer, reader B answer): clean, drop(both wrong), drop(wrong + abstain), split, abstain, clean
        "r0": ("yes", "yes"), "r1": ("yes", "yes"), "r2": ("no", None), "r3": ("no", "yes"), "r4": ("no", "garbage"),
        "r5": ("yes", "yes")}
    tasks, key = [], {"batches": {"gd_x": {"A": PI._batch_record(ba), "B": PI._batch_record(bb)}}, "gold": gold,
                      "source_of": {i: "gd_x" for i in gold}, "refused": {}}
    for rd, bt, k in (("A", ba, 0), ("B", bb, 1)):
        inv = {v: q for q, v in bt.key.items()}
        for c in bt.chunks:
            ans = [{"qid": it["qid"], "answer": plan[bt.key[it["qid"]]][k], "confidence": 0.9} for it in c["items"]
                   if plan[bt.key[it["qid"]]][k] is not None]
            af = tmp_path / f"{c['task_id']}.json"
            af.write_text(json.dumps(ans))
            tasks.append({"source": "gd_x", "tier": 2, "reader": rd, "task_id": c["task_id"], "answer_file": str(af)})
    res = SR.score({"tasks": tasks}, key)
    assert res["drop_ids"] == ["r1", "r2"], res
    assert res["clean_ids"] == ["r0", "r5"]
    s = res["sources"]["gd_x"]
    assert (s["clean"], s["drop"], s["split"], s["abstain"], s["n_read"], s["not_clean"]) == (2, 2, 1, 1, 6, 4)
    assert res["sources_over_bar"] == ["gd_x"]
    assert not (set(res["drop_ids"]) & set(res["clean_ids"]))
