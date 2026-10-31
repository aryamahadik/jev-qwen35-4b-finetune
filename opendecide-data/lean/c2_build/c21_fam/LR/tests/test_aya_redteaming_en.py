import json
import os

import pytest

import lr_common as lc
import lr_testlib as T
from aya_redteaming_en import FORM, Mapper, read_train


def records(n=20):
    cats = ["Hate Speech", "Self-Harm", "Profanity", "Graphic material"]
    out = []
    for i in range(n):
        out.append({"prompt": "Synthetic red-team prompt number %d about topic %s." % (i, cats[i % 4]),
                    "language": "English", "harm_category": json.dumps([cats[i % 4]]), "global_or_local": "global",
                    "explanation": None, "_src_line": i})
    return out


def twins(n=20):
    return [{"id": "t%d" % i, "text": "Synthetic benign request number %d about gardening tools." % i} for i in range(n)]


def test_rows_and_twin_share():
    m = Mapper(T.pools_for(Mapper), seed=1)
    rows = m.map_with_twins(records(), twins(), cap=12)
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=20)
    yes = [r for r in rows if r["answer_text"] == "Yes"]
    no = [r for r in rows if r["answer_text"] == "No"]
    assert len(yes) == len(no) == 12                      # twin share exactly 50%
    assert all(r["extra"]["twin"] for r in no) and not any(r["extra"]["twin"] for r in yes)
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["yes_rate"] == 0.5 and rep["R7_pass"]


def test_non_english_and_unlabelled_dropped():
    m = Mapper(T.pools_for(Mapper), seed=1)
    recs = records(4) + [{"prompt": "Une invite.", "language": "French", "harm_category": "[\"x\"]", "_src_line": 90},
                         {"prompt": "No category here.", "language": "English", "harm_category": "[]", "_src_line": 91}]
    rows = m.map_records(recs)
    assert len(rows) == 4
    assert m.drops.c["A82_9_non_english"] == 1 and m.drops.c["no_prompt_or_no_harm_category"] == 1


def test_r4_mismatch_drops_row():
    m = Mapper(T.pools_for(Mapper), seed=1)
    orig = m.independent_gold
    m.independent_gold = lambda src, cand: "No"
    assert m.map_records(records(3)) == []
    assert m.drops.c["R4_gold_mismatch"] == 3
    m.independent_gold = orig


def test_r12_pii_drop():
    m = Mapper(T.pools_for(Mapper), seed=1)
    recs = [{"prompt": "Mail me at jane.doe@example.com now", "language": "English", "harm_category": "[\"x\"]", "_src_line": 1}]
    assert m.map_records(recs) == []
    assert m.drops.c["R12_PII_email"] == 1


def test_reader_reads_only_train_file(tmp_path):
    (tmp_path / "aya_eng.train.jsonl").write_text(json.dumps(records(1)[0]) + "\n")
    (tmp_path / "aya_eng.holdout10.jsonl").write_text(json.dumps({"prompt": "HOLDOUT", "_src_line": 99}) + "\n")
    got = list(read_train(str(tmp_path)))
    assert len(got) == 1 and got[0]["_src_line"] == 0


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(Mapper)


def test_wording_balance_over_many_rows():
    m = Mapper(T.pools_for(Mapper), seed=3)
    recs = [dict(records(1)[0], prompt="Synthetic prompt %d unique words %d" % (i, i * 7), _src_line=i) for i in range(200)]
    rows = m.map_records(recs, cap=200)
    rep = lc.set_report(rows, yes_no=False)
    assert rep["wording"][FORM]["max_share"] <= 0.02 + 1e-9 or len(rows) < 50


def test_reader_refuses_quarantine_path():
    with pytest.raises(AssertionError):
        list(read_train("/x/bench/c21_eval_quarantine/lr_targets/aya_redteaming_en"))
