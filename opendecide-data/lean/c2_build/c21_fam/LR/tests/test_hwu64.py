import csv
import os

import pytest

import lr_common as lc
import lr_testlib as T
import hwu64 as H

INTENTS = [("alarm", "query"), ("alarm", "set"), ("alarm", "remove"), ("audio", "volume_up"), ("audio", "volume_down"),
           ("calendar", "set"), ("calendar", "query"), ("email", "sendemail"), ("email", "query"), ("play", "music")]


def records(n=20):
    out = []
    for i in range(n):
        sc, it = INTENTS[i % len(INTENTS)]
        out.append({"answerid": str(i), "scenario": sc, "intent": it, "answer_annotation": "x",
                    "answer_from_anno": "please %s %s number %d" % (sc, it, i),
                    "answer_from_user": "Please %s [time : at %d pm] %s number %d" % (sc, i, it, i), "_src_line": "f.csv:%d" % i})
    return out


def test_rows_large_label_set_k_rotates():
    m = H.Mapper(T.pools_for(H.Mapper), seed=1)
    rows = m.map_records(records(20))
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    assert {r["k"] for r in rows} == {4, 8}
    assert all(r["k_full"] == 10 for r in rows)
    for r in rows:
        assert "[" not in r["context"]                  # annotation markup replaced by its value
        assert r["answer_text"] in r["options"]
    rep = T.check_set_report(rows)
    assert abs(rep["k_share"][4] - 0.5) <= 0.05 + 1e-9 and rep["R5_position_pass"]


def test_small_label_set_shows_all_labels():
    m = H.Mapper(T.pools_for(H.Mapper), seed=1)
    recs = [r for r in records(40) if r["scenario"] in ("alarm", "audio")]       # 5 intents <= 8 -> all shown (LR-B1)
    rows = m.map_records(recs)
    assert rows and all(r["k"] == 5 for r in rows)


def test_markup_cleaning():
    assert H.clean_utterance("wake me up at [time : five am] on [date : friday]") == "wake me up at five am on friday"
    assert H.clean_utterance("no markup here") == "no markup here"


def test_reader_reads_trainset_only(tmp_path):
    (tmp_path / "KFold_1_trainset").mkdir()
    (tmp_path / "KFold_1_testset_csv").mkdir()
    hdr = "answerid;scenario;intent;answer_annotation;answer_from_anno;answer_from_user\n"
    (tmp_path / "KFold_1_trainset" / "a.csv").write_text(hdr + '1;alarm;set;"x";"y";"Set an alarm."\n')
    (tmp_path / "KFold_1_testset_csv" / "a.csv").write_text(hdr + '2;alarm;set;"x";"y";"HELD OUT."\n')
    got = list(H.read_train(str(tmp_path)))
    assert len(got) == 1 and got[0]["answer_from_user"] == "Set an alarm."


def test_drops_and_r4():
    m = H.Mapper(T.pools_for(H.Mapper), seed=1)
    recs = records(10) + [{"answerid": "x", "scenario": "alarm", "intent": "set", "answer_from_user": "  ", "answer_from_anno": "", "_src_line": "z"}]
    rows = m.map_records(recs)
    assert len(rows) == 10 and m.drops.c["no_text_or_label"] == 1
    m.independent_gold = lambda s, c: "zzz"
    assert m.map_records(records(5)) == [] and m.drops.c["R4_gold_mismatch"] == 5


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(H.Mapper)
