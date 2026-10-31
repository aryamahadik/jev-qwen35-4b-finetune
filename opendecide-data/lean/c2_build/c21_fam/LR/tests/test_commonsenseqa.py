import json

import lr_common as lc
import lr_testlib as T
import commonsenseqa as C


def records(n=20):
    out = []
    for i in range(n):
        letters = "ABCDE"
        texts = ["option %d-%s" % (i, l) for l in letters]
        out.append({"answerKey": letters[i % 5], "id": "id%d" % i,
                    "question": {"question_concept": "concept%d" % (i % 7), "stem": "What is the answer to question number %d?" % i,
                                 "choices": [{"label": l, "text": t} for l, t in zip(letters, texts)]}, "_src_line": "csqa:id%d" % i})
    return out


def test_rows_gold_and_balance():
    m = C.Mapper(T.pools_for(C.Mapper), seed=1)
    rows = m.map_records(records(20))
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    assert all(r["k"] == 5 for r in rows)
    for r in rows:
        i = int(r["source_row_id"].split("id")[1])
        assert r["answer_text"] == "option %d-%s" % (i, "ABCDE"[i % 5])
    rep = T.check_set_report(rows)
    assert rep["R5_position_pass"]
    assert len({r["label"] for r in rows}) == 5


def test_duplicate_choice_and_bad_key_dropped():
    m = C.Mapper(T.pools_for(C.Mapper), seed=1)
    dup = records(1)[0]
    dup["question"]["choices"][1]["text"] = dup["question"]["choices"][0]["text"]
    nokey = dict(records(2)[1], answerKey="Z")
    assert m.map_records([dup, nokey]) == []
    assert m.drops.c["R5_options"] == 1 and m.drops.c["missing_answer_key_or_not_5_choices"] == 1


def test_r4_and_reader(tmp_path):
    m = C.Mapper(T.pools_for(C.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(3)) == []
    (tmp_path / "train_rand_split.jsonl").write_text(json.dumps(records(1)[0]) + "\n")
    (tmp_path / "dev_rand_split.jsonl").write_text(json.dumps({"id": "DEV"}) + "\n")
    assert [g["id"] for g in C.read_train(str(tmp_path))] == ["id0"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(C.Mapper)
