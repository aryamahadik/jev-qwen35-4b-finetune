import gzip
import json

import lr_common as lc
import lr_testlib as T
import finqa as F


def report(i):
    pre = ["The company reported revenue of $ %d million in fiscal %d ." % (500 + i, 2000 + i % 10), "Filler sentence number %d about the business and its markets ." % i]
    post = ["Another filler sentence %d after the table with additional words ." % i, "Interest expense would change by $ 3.8 million per 100 basis points ."]
    table = [["", "2009", "2008"], ["revenue", str(500 + i), str(400 + i)], ["costs", str(100 + i), str(90 + i)]]
    return pre, post, table


def records(n=20):
    out = []
    for i in range(n):
        pre, post, table = report(i)
        a, b = 500 + i, 400 + i
        if i % 2 == 0:
            prog = "subtract(%d, %d)" % (a, b)
            ans = str(a - b)
            exe = float(a - b)
            gold = {"table_1": "revenue ..."}
        else:
            prog = "subtract(%d, %d), divide(#0, %d)" % (a, b, b)
            exe = (a - b) / b
            ans = "%.1f%%" % (exe * 100)
            gold = {"table_1": "revenue ..."}
        qa = {"question": "what was the change in revenue in report %d ?" % i, "answer": ans, "program": prog, "exe_ans": exe, "gold_inds": gold, "steps": []}
        out.append({"id": "R%d/page_1.pdf-1" % i, "pre_text": pre, "post_text": post, "table": table, "qa": qa, "_src_line": "finqa:R%d/page_1.pdf-1" % i})
    return out


def test_rows_gold_near_misses_and_format():
    m = F.Mapper(T.pools_for(F.Mapper), seed=1)
    recs = records(20)
    rows = m.map_records(recs, cap=20)
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=14)
    for r in rows:
        assert r["k"] == 4
        i = int(r["source_row_id"].split("R")[1].split("/")[0])
        assert r["answer_text"] == recs[i]["qa"]["answer"]
        pct = r["answer_text"].endswith("%")
        for o in r["options"]:
            assert o.endswith("%") == pct                      # distractors are formatted like the gold
        assert "Question: what was the change in revenue" in r["context"] and "revenue | %d | %d" % (500 + i, 400 + i) in r["context"]
        assert " | " in r["context"] and "2009 | 2008" in r["context"]      # the table header travels with a table fact


def test_program_evaluator_and_style():
    st = F.parse_program("divide(100, 100), divide(3.8, #0)")
    assert F.run_program(st) == 3.8
    assert F.run_program(F.parse_program("multiply(2, const_100), subtract(#0, const_m1)")) == 201
    assert abs(F.run_program(F.parse_program("divide(5.2%, 2)")) - 0.026) < 1e-12
    assert F.answer_style("14.1%") == (True, 1, False) and F.answer_style("380") == (False, 0, False) and F.answer_style("yes") is None
    assert F.fmt(0.141, (True, 1, False)) == "14.1%" and F.fmt(-0.0001, (False, 2, False)) == "0.00"
    # conventions: truncation, absolute value, % already in percent units
    assert F.match_convention("0.96", 0.96667) is not None and F.match_convention("0.96", 0.96667)[2] == "trunc"
    assert F.match_convention("16.7%", -0.16667)[1] is True
    assert F.match_convention("96.55%", 96.55172)[0] == 1.0
    assert F.match_convention("56.25%", 0.97656) is None and F.match_convention("380", 3.8) is None
    for bad in ("table_max(x, none)", "greater(1, 2)"):
        try:
            F.run_program(F.parse_program(bad))
            assert False
        except ValueError:
            pass


def test_drops_for_unsupported_and_mismatched():
    m = F.Mapper(T.pools_for(F.Mapper), seed=1)
    r = records(6)
    r[0]["qa"]["program"] = "table_max(revenue, none)"
    r[1]["qa"]["answer"] = "yes"
    r[2]["qa"]["exe_ans"] = 12345.0
    r[5]["qa"]["answer"] = "9999"
    r[3]["qa"]["gold_inds"] = {}
    r[4]["qa"]["gold_inds"] = {"table_9": "x"}
    m.map_records(r, cap=10)
    c = m.drops.c
    assert c["unsupported_program_op"] == 1 and c["non_numeric_answer"] == 1 and c["program_disagrees_with_exe_ans"] == 1
    assert c["no_gold_inds"] == 1 and c["gold_ind_out_of_range_or_unmatched"] == 1 and c["answer_not_reproduced_by_program"] == 1


def test_budget_drop_never_cuts_supporting_facts():
    m = F.Mapper(T.pools_for(F.Mapper), seed=1)
    r = records(2)[0]
    r["pre_text"] = ["%s ." % " ".join("word%d" % j for j in range(900))] + r["pre_text"]
    r["qa"]["gold_inds"] = {"text_0": r["pre_text"][0], "table_1": "x"}
    assert m.map_records([r], cap=4) == [] and m.drops.c["supporting_facts_exceed_budget"] == 1


def test_r4_and_reader(tmp_path):
    m = F.Mapper(T.pools_for(F.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(4), cap=8) == []
    with gzip.open(str(tmp_path / "train.json.gz"), "wt") as f:
        json.dump([{k: v for k, v in records(1)[0].items() if k != "_src_line"}], f)
    (tmp_path / "test.json").write_text("[]")
    assert [g["id"] for g in F.read_train(str(tmp_path))] == ["R0/page_1.pdf-1"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(F.Mapper)
