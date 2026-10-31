import json

import lr_common as lc
import lr_testlib as T
import social_iqa as S


def records(n=20):
    qs = ["How would Others feel as a result?", "What will Others want to do next?", "Why did Alex do this?", "What does Alex need to do before this?"]
    out = []
    for i in range(n):
        out.append({"context": "Alex did thing number %d for a friend." % i, "question": qs[i % 4],
                    "answerA": "option A %d" % i, "answerB": "option B %d" % i, "answerC": "option C %d" % i,
                    "label": str(i % 3 + 1), "_src_line": "siqa:train#%d" % i})
    return out


def test_rows_gold_and_balance():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records(records(20))
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    assert all(r["k"] == 3 for r in rows)
    for r in rows:
        i = int(r["source_row_id"].split("#")[1])
        assert r["answer_text"] == "option %s %d" % ("ABC"[i % 3], i)
        assert r["context"].startswith("Situation: ") and "\nQuestion: " in r["context"]
    assert T.check_set_report(rows)["R5_position_pass"]


def test_drops():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    r = records(4)
    dup = dict(r[0], _src_line="siqa:train#99")
    badlab = dict(r[1], label="4")
    sameans = dict(r[2], answerB=r[2]["answerA"])
    rows = m.map_records([r[0], dup, badlab, sameans, r[3]])
    assert len(rows) == 2
    assert m.drops.c["duplicate_item"] == 1 and m.drops.c["bad_label_or_empty"] == 1 and m.drops.c["R5_options"] == 1


def test_r4_and_reader_pairs_labels_by_line(tmp_path):
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(3)) == []
    recs = [{k: v for k, v in x.items() if k not in ("label", "_src_line")} for x in records(3)]
    (tmp_path / "train.jsonl").write_text("\n".join(json.dumps(x) for x in recs) + "\n")
    (tmp_path / "train-labels.lst").write_text("1\n2\n3\n")
    (tmp_path / "dev.jsonl").write_text(json.dumps({"context": "DEV"}) + "\n")
    got = list(S.read_train(str(tmp_path)))
    assert [g["label"] for g in got] == ["1", "2", "3"] and all("DEV" not in g["context"] for g in got)


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(S.Mapper)
