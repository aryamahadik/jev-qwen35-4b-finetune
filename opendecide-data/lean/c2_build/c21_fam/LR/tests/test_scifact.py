import json

import lr_common as lc
import lr_testlib as T
import scifact as S


def corpus(n=30):
    return {1000 + i: {"doc_id": 1000 + i, "title": "Title %d of a paper" % i,
                       "abstract": ["Sentence zero about topic %d." % i, "Sentence one reports result %d." % i, "Sentence two."]} for i in range(n)}


def claims(n=30):
    cp = corpus(n)
    out = []
    for i in range(n):
        if i % 3 == 0:
            ev = {str(1000 + i): [{"sentences": [1], "label": "SUPPORT"}]}
        elif i % 3 == 1:
            ev = {str(1000 + i): [{"sentences": [0, 1], "label": "CONTRADICT"}]}
        else:
            ev = {}
        out.append({"id": i, "claim": "Claim number %d states something." % i, "evidence": ev, "cited_doc_ids": [1000 + i],
                    "_corpus": cp, "_src_line": "scifact:%d" % i})
    return out


def test_rows_balanced_three_way():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records(claims(30), cap=30)
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=30)
    assert {r["k"] for r in rows} == {3}
    shares = {a: sum(r["answer_text"] == a for r in rows) for a in S.OPTIONS}
    assert set(shares.values()) == {10}
    for r in rows:
        want = ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"][int(r["source_row_id"].split(":")[1].split("/")[0]) % 3]
        assert r["answer_text"] == want
        assert r["flags"]["native_abstain_label"] == (want == "NOT ENOUGH INFO")
        assert "Abstract:" in r["context"] and "[0] Sentence zero" in r["context"]


def test_multi_doc_claim_prefers_evidence_doc():
    cp = corpus(3)
    c = {"id": 9, "claim": "x claim here", "evidence": {"1002": [{"sentences": [0], "label": "SUPPORT"}]},
         "cited_doc_ids": [1000, 1001, 1002], "_corpus": cp, "_src_line": "scifact:9"}
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records([c])
    assert len(rows) == 1 and rows[0]["answer_text"] == "SUPPORTS" and rows[0]["extra"]["doc_id"] == 1002


def test_missing_corpus_doc_and_r4():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    c = dict(claims(1)[0], cited_doc_ids=[5555])
    assert m.map_records([c]) == [] and m.drops.c["no_cited_abstract_in_corpus"] >= 1
    m2 = S.Mapper(T.pools_for(S.Mapper), seed=1)
    m2.independent_gold = lambda s, c: "?"
    assert m2.map_records(claims(6)) == []


def test_reader_train_only(tmp_path):
    (tmp_path / "corpus_train_cited.jsonl").write_text(json.dumps(corpus(1)[1000]) + "\n")
    (tmp_path / "claims_train.jsonl").write_text(json.dumps({"id": 0, "claim": "c", "evidence": {}, "cited_doc_ids": [1000]}) + "\n")
    (tmp_path / "claims_dev.jsonl").write_text(json.dumps({"id": 99, "claim": "HELD OUT", "evidence": {}, "cited_doc_ids": [1]}) + "\n")
    got = list(S.read_train(str(tmp_path)))
    assert len(got) == 1 and got[0]["id"] == 0 and 1000 in got[0]["_corpus"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(S.Mapper)
