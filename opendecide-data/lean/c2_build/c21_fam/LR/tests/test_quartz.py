import gzip
import json

import lr_common as lc
import lr_testlib as T
import quartz as Q


def records(n=20):
    out = []
    for i in range(n):
        out.append({"id": "QRQA-%d-%d" % (100 + i // 2, i % 4), "question": "Question number %d: a ball rolls further when the surface is _____." % i,
                    "choices": {"text": ["smoother %d" % i, "rougher %d" % i], "label": ["A", "B"]}, "answerKey": "AB"[i % 2],
                    "_src_line": "quartz:QRQA-%d-%d" % (100 + i // 2, i % 4)})
    return out


def test_rows_gold_and_balance():
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=1)
    rows = m.map_records(records(20))
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    for r in rows:
        i = int(r["context"].split("number ")[1].split(":")[0])
        assert r["answer_text"] == ("smoother %d" if i % 2 == 0 else "rougher %d") % i and r["k"] == 2
    assert T.check_set_report(rows)["R5_position_pass"]


def test_cap_spreads_over_parent_ids():
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=3)
    rows = m.map_records(records(20), cap=10)
    assert len(rows) == 10 and len({r["extra"]["parent"] for r in rows}) == 10


def test_drops_and_r4():
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=1)
    r = records(4)
    three = dict(r[0], choices={"text": ["a", "b", "c"], "label": ["A", "B", "C"]})
    nokey = dict(r[1], answerKey="Z")
    dup = dict(r[2], id="QRQA-999-9", _src_line="quartz:QRQA-999-9", question=r[3]["question"])
    rows = m.map_records([three, nokey, dup, r[3]])
    assert len(rows) == 1 and m.drops.c["missing_key_or_not_2_choices"] == 2 and m.drops.c["duplicate_item"] == 1
    m2 = Q.Mapper(T.pools_for(Q.Mapper), seed=1)
    m2.independent_gold = lambda s, c: "?"
    assert m2.map_records(records(3)) == []


def test_reader_reads_train_file_only(tmp_path):
    with gzip.open(str(tmp_path / "train.jsonl.gz"), "wt") as f:
        f.write(json.dumps({k: v for k, v in records(1)[0].items() if k != "_src_line"}) + "\n")
    (tmp_path / "test.jsonl.gz").write_bytes(b"not read")
    assert [g["id"] for g in Q.read_train(str(tmp_path))] == ["QRQA-100-0"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(Q.Mapper)
