import json

import lr_common as lc
import lr_testlib as T
import ecare as E


def records(n=20):
    out = []
    for i in range(n):
        out.append({"index": "train-%d" % i, "premise": "Event number %d happened in the town square today." % i,
                    "ask-for": "cause" if i % 2 else "effect", "hypothesis1": "First candidate statement %d about the event." % i,
                    "hypothesis2": "Second candidate statement %d about something else." % i, "label": i % 2,
                    "_src_line": "ecare:train-%d" % i})
    return out


def test_rows_gold_forms_and_balance():
    m = E.Mapper(T.pools_for(E.Mapper), seed=1)
    rows = m.map_records(records(20))
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    for r in rows:
        i = int(r["source_row_id"].split("-")[1])
        want = ("First candidate statement %d about the event." if i % 2 == 0 else "Second candidate statement %d about something else.") % i
        assert r["answer_text"] == want
        assert r["form"] == (E.F_CAUSE if i % 2 else E.F_EFFECT) and r["k"] == 2
    assert {r["form"] for r in rows} == {E.F_CAUSE, E.F_EFFECT}
    rep = T.check_set_report(rows)
    assert rep["R5_position_pass"]


def test_drops_duplicates_bad_label_identical():
    m = E.Mapper(T.pools_for(E.Mapper), seed=1)
    r0 = records(1)[0]
    dup = dict(r0, index="train-dup", _src_line="ecare:train-dup")
    swapped = dict(r0, index="train-sw", _src_line="ecare:train-sw", hypothesis1=r0["hypothesis2"], hypothesis2=r0["hypothesis1"], label=1)
    bad = dict(records(2)[1], label=3)
    same = dict(records(3)[2], hypothesis2=records(3)[2]["hypothesis1"])
    rows = m.map_records([r0, dup, swapped, bad, same])
    assert len(rows) == 1
    assert m.drops.c["duplicate_item"] == 2 and m.drops.c["bad_label_askfor_or_empty"] == 2


def test_r4_mismatch_dropped_and_reader_is_train_only(tmp_path):
    m = E.Mapper(T.pools_for(E.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(3)) == []
    (tmp_path / "train.jsonl").write_text(json.dumps({k: v for k, v in records(1)[0].items() if k != "_src_line"}) + "\n")
    (tmp_path / "dev.jsonl").write_text(json.dumps({"index": "dev-0"}) + "\n")
    got = list(E.read_train(str(tmp_path)))
    assert [g["index"] for g in got] == ["train-0"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(E.Mapper)
