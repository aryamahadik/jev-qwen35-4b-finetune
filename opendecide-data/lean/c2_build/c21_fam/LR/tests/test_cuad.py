import json

import lr_common as lc
import lr_testlib as T
import cuad as C

CATS = ["Governing Law", "Parties", "Document Name"]


def make_text(i, n_par=14):
    pars = []
    for j in range(n_par):
        pars.append("Section %d.%d of agreement %d: the parties agree to marker%d%d and keep records of item %d for the term." % (i, j, i, i, j, j * 3 + i) + " filler words go here to extend the paragraph length for the window chunker " * 5)
    return "\n\n".join(pars)


def q(cat):
    return 'Highlight the parts (if any) of this contract related to "%s" that should be reviewed by a lawyer. Details: what is %s' % (cat, cat)


def records(n=20):
    out = []
    for i in range(n):
        text = make_text(i)
        marker = "the parties agree to marker%d%d" % (i, 3)
        s = text.index(marker)
        qas = []
        # Governing Law present in even contracts, Parties present in all, Document Name absent in odd ones
        if i % 2 == 0:
            qas.append({"id": "c%d__Governing Law_0" % i, "question": q("Governing Law"), "answers": [{"text": marker, "answer_start": s}], "is_impossible": False})
        else:
            qas.append({"id": "c%d__Governing Law_0" % i, "question": q("Governing Law"), "answers": [], "is_impossible": True})
        s2 = text.index("Section %d.5" % i)
        qas.append({"id": "c%d__Parties_0" % i, "question": q("Parties"), "answers": [{"text": text[s2:s2 + 40], "answer_start": s2}], "is_impossible": False})
        qas.append({"id": "c%d__Document Name_0" % i, "question": q("Document Name"), "answers": [], "is_impossible": True})
        out.append({"title": "CONTRACT_%d" % i, "context": text, "qas": qas, "_src_line": "cuad:CONTRACT_%d" % i})
    return out


def test_rows_yes_no_balance_and_gold_in_excerpt():
    m = C.Mapper(T.pools_for(C.Mapper), seed=1)
    rows = m.map_records(records(20), cap=20)
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=20)
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["R7_pass"] and rep["yes_rate"] == 0.5
    recs = {r["title"]: r for r in records(20)}
    for r in rows:
        src = recs[r["extra"]["contract"]]
        cat = r["extra"]["category"]
        ans = [a for qa in src["qas"] if '"%s"' % cat in qa["question"] for a in qa["answers"]]
        if r["answer_text"] == "Yes":
            assert ans
            for a in ans:                      # EVERY gold answer text is inside the excerpt (spans are never cut)
                assert lc.normalise_ws(a["text"]) in lc.normalise_ws(r["context"].replace("\n[Segment", " [Segment"))
        else:
            assert not ans
        assert r["context"].startswith("Clause type: %s\n" % cat) and "[Segment 1]" in r["context"]
        assert r["tokens_est"] <= lc.TOKEN_ROW_MAX


def test_yes_rows_keep_all_gold_windows_and_distractors_are_same_contract():
    m = C.Mapper(T.pools_for(C.Mapper), seed=2)
    src = records(2)[0]
    rows = []
    for cand in m.build(src, {"category": "Governing Law"}):
        rows.append(m.finish_candidate(src, cand))
    assert rows and rows[0] is not None
    r = rows[0]
    assert r["answer_text"] == "Yes" and r["extra"]["span_info"]["tokens"] <= C.BUDGET_TOKENS
    segs = [s.split("\n", 1)[1] for s in r["context"].split("[Segment ")[1:]]
    seg_text = " ".join(lc.normalise_ws(s) for s in segs)
    assert "agreement 0" in seg_text and "agreement 1" not in seg_text


def test_offset_mismatch_and_budget_drops():
    m = C.Mapper(T.pools_for(C.Mapper), seed=1)
    src = records(1)[0]
    bad = json.loads(json.dumps(src))
    bad["qas"][0]["answers"][0]["answer_start"] += 1
    assert m.build(bad, {"category": "Governing Law"}) == [] and m.drops.c["answer_offset_mismatch"] == 1
    big = json.loads(json.dumps(src))
    big["qas"][0]["answers"] = [{"text": src["context"][:40000], "answer_start": 0}]
    assert m.build(big, {"category": "Governing Law"}) == [] and m.drops.c["gold_windows_exceed_budget"] == 1


def test_r4_mismatch_dropped_and_reader_is_train_only(tmp_path):
    m = C.Mapper(T.pools_for(C.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(4), cap=8) == []
    obj = {"version": "x", "data": [{"title": "T0", "paragraphs": [{"context": "abc " * 50, "qas": []}]}]}
    (tmp_path / "train_separate_questions.json").write_text(json.dumps(obj))
    (tmp_path / "test.json").write_text(json.dumps({"data": [{"title": "TESTDOC", "paragraphs": []}]}))
    assert [g["title"] for g in C.read_train(str(tmp_path))] == ["T0"]


def test_windows_cover_text_with_exact_offsets():
    t = make_text(3)
    w = C.windows(t)
    assert "".join(t[a:b] for a, b in w) == t
    assert all(t[b].isspace() for a, b in w if b < len(t))          # a window never ends inside a word


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(C.Mapper)
