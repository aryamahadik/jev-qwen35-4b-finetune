import gzip
import json

import lr_common as lc
import lr_testlib as T
import strategyqa as S


def records(n=20):
    return [{"qid": "q%03d" % i, "term": "Term %d" % i, "question": "Would a thing number %d be found in a place number %d?" % (i, i * 7),
             "answer": (i % 3 == 0), "facts": ["fact"], "decomposition": ["step"], "_src_line": "strategyqa:q%03d" % i} for i in range(n)]


def test_rows_balanced_yes_rate_and_gold():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records(records(20), cap=12)
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=12)
    for r in rows:
        i = int(r["source_row_id"].rsplit("q", 1)[1])
        assert r["answer_text"] == ("Yes" if i % 3 == 0 else "No") and r["options"].count("Yes") == 1
        assert "fact" not in r["context"] and "step" not in r["context"] and "Term" not in r["context"]
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["R7_pass"] and rep["yes_rate"] == 0.5


def test_full_list_keeps_all_when_under_cap():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records(records(20))
    assert len(rows) == 20


def test_drops():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    r = records(4)
    dup = dict(r[0], qid="qdup", _src_line="strategyqa:qdup")
    notbool = dict(r[1], answer="yes")
    rows = m.map_records([r[0], dup, notbool, r[2]])
    assert len(rows) == 2 and m.drops.c["duplicate_item"] == 1 and m.drops.c["non_boolean_answer_or_empty"] == 1


def test_r4_and_reader(tmp_path):
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(3)) == []
    with gzip.open(str(tmp_path / "train.jsonl.gz"), "wt") as f:
        f.write(json.dumps({k: v for k, v in records(1)[0].items() if k != "_src_line"}) + "\n")
    assert [g["qid"] for g in S.read_train(str(tmp_path))] == ["q000"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(S.Mapper)
