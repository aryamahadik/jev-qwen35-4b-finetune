import gzip
import json

import pytest

import lr_common as lc
import lr_testlib as T
import abcd as A

ACTIONS = ["pull-up-account", "verify-identity", "validate-purchase", "search-faq", "enter-details", "ask-the-oracle",
           "select-faq", "update-order", "record-reason", "membership", "shipping-status", "log-out-in"]


def convo(ci):
    orig, dl = [], []

    def add(sp, tx, nxt, act):
        orig.append([sp, tx])
        dl.append({"speaker": sp, "text": tx.lower(), "turn_count": len(orig), "targets": ["return_size", nxt, act, [], -1], "candidates": []})
    add("agent", "Hi! How can I help you?", "retrieve_utterance", None)
    add("customer", "I need to return item number %d please" % ci, None, None)
    add("agent", "Sure, may I have your name?", "retrieve_utterance", None)
    add("customer", "Alex Person%d" % ci, None, None)
    add("action", "Account has been pulled up for alex person%d." % ci, "take_action", ACTIONS[ci % len(ACTIONS)])
    add("agent", "Thanks, what is the reason?", "retrieve_utterance", None)
    add("customer", "wrong size", None, None)
    add("action", "Reason recorded %d." % ci, "take_action", ACTIONS[(ci + 3) % len(ACTIONS)])
    add("agent", "Done. Anything else?", "retrieve_utterance", None)
    return {"convo_id": ci, "scenario": {"flow": "x"}, "original": orig, "delexed": dl, "_src_line": str(ci)}


def records(n=20):
    return [convo(i) for i in range(n)]


def test_rows_both_forms(monkeypatch):
    monkeypatch.setitem(A.RECAST_TABLE["caps"], A.F_NEXT, 20)
    monkeypatch.setitem(A.RECAST_TABLE["caps"], A.F_ACT, 20)
    m = A.Mapper(T.pools_for(A.Mapper), seed=1)
    rows = m.map_records(records())
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    nx = [r for r in rows if r["form"] == A.F_NEXT]
    ac = [r for r in rows if r["form"] == A.F_ACT]
    assert nx and ac
    assert all(r["k"] == 2 for r in nx)
    assert abs(sum(r["extra"]["label"] == "take_action" for r in nx) - len(nx) / 2) <= 1      # declared 50/50 balance
    assert all(r["k"] in (4, 8) or r["k"] == len(ACTIONS) for r in ac)
    for r in ac:
        assert r["answer_text"] in r["options"]
        assert "System:" in r["context"] or "Agent:" in r["context"]


def test_context_excludes_target_turn():
    m = A.Mapper(T.pools_for(A.Mapper), seed=1)
    rows = m.map_records(records(6))
    for r in rows:
        ci = int(r["source_row_id"].split(":")[1].split("#")[0])
        ti = int(r["source_row_id"].rsplit("#", 1)[1])
        target_text = records(ci + 1)[ci]["original"][ti][1]
        assert target_text not in r["context"]


def test_long_history_keeps_first_customer_turn_and_recent_turns():
    orig = [["agent", "Hi"], ["customer", "FIRST ISSUE TEXT"]] + [["agent" if i % 2 else "customer", "filler words " * 25 + str(i)] for i in range(60)]
    txt = A.history_text(orig, len(orig))
    assert "FIRST ISSUE TEXT" in txt and "[... earlier turns omitted ...]" in txt and txt.rstrip().endswith("59")
    assert lc.approx_tokens(txt) <= A.BUDGET + 20


def test_reader_train_only(tmp_path):
    with gzip.open(tmp_path / "abcd_v1.1.train.json.gz", "wt") as f:
        json.dump(records(2), f)
    with gzip.open(tmp_path / "abcd_v1.1.dev.json.gz", "wt") as f:
        json.dump([convo(99)], f)
    got = list(A.read_train(str(tmp_path)))
    assert [g["convo_id"] for g in got] == [0, 1]


def test_r4_and_refusal():
    m = A.Mapper(T.pools_for(A.Mapper), seed=1)
    m.independent_gold = lambda s, c: "zzz"
    assert m.map_records(records(3)) == []
    T.check_dry_run_refusal(A.Mapper)
