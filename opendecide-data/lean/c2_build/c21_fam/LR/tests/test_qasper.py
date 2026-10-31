import json

import lr_common as lc
import lr_testlib as T
import qasper as Q


def paper(i, n_par=12):
    full = [{"section_name": "Intro %d" % s, "paragraphs": ["Paragraph %d of section %d describes details number %d." % (p, s, i) * 2 for p in range(2)]}
            for s in range(n_par // 2)]
    paras = [p for s in full for p in s["paragraphs"]]
    qas = []

    def ans(unans=False, yn=None, ev=()):
        return {"answer": {"unanswerable": unans, "extractive_spans": [], "yes_no": yn, "free_form_answer": "", "evidence": list(ev),
                           "highlighted_evidence": []}, "annotation_id": "a", "worker_id": "w"}
    qas.append({"question": "Does it work on case %d?" % i, "question_id": "q%d_y" % i, "answers": [ans(yn=True, ev=[paras[3]]), ans(yn=True, ev=[paras[3]])]})
    qas.append({"question": "Is it bad for case %d?" % i, "question_id": "q%d_n" % i, "answers": [ans(yn=False, ev=[paras[7]])]})
    qas.append({"question": "Which unseen thing %d?" % i, "question_id": "q%d_u" % i, "answers": [ans(unans=True)]})
    qas.append({"question": "Annotators disagree %d" % i, "question_id": "q%d_d" % i, "answers": [ans(yn=True, ev=[paras[1]]), ans(unans=True)]})
    qas.append({"question": "Free form %d" % i, "question_id": "q%d_f" % i, "answers": [{"answer": {"unanswerable": False, "extractive_spans": [], "yes_no": None, "free_form_answer": "x", "evidence": [paras[2]], "highlighted_evidence": []}}]})
    qas.append({"question": "Float evidence %d" % i, "question_id": "q%d_fl" % i, "answers": [ans(yn=True, ev=["FLOAT SELECTED: Table 1: results"])]})
    return {"title": "A paper %d" % i, "abstract": "This abstract %d states things." % i, "full_text": full, "qas": qas, "figures_and_tables": [],
            "_pid": "p%d" % i, "_src_line": "qasper:p%d" % i}


def records(n=8):
    return [paper(i) for i in range(n)]


def test_rows_and_labels(monkeypatch):
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=1)
    rows = m.map_records(records(), cap=100)
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=12)
    assert {r["answer_text"] for r in rows} == {"Yes", "No", "Unanswerable"}
    for r in rows:
        assert r["options"] == sorted(Q.OPTIONS, key=lambda o: r["options"].index(o))          # all 3 shown
        assert r["flags"]["native_abstain_label"] == (r["answer_text"] == "Unanswerable")
        assert lc.approx_tokens(r["context"]) <= Q.BUDGET + 60
        assert "Question:" in r["context"] and r["context"].startswith("Paper: ")
    # disagreement, free-form and float-evidence questions never become rows
    ids = {r["extra"]["question_id"] for r in rows}
    assert not any(i.endswith(("_d", "_f", "_fl")) for i in ids)
    assert m.drops.c.get("evidence_is_float_caption", 0) >= 1


def test_all_evidence_paragraphs_kept_and_same_paper_only():
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=2)
    recs = records(4)
    rows = m.map_records(recs, cap=100)
    for r in rows:
        pid = r["extra"]["paper"]
        pi = int(pid[1:])
        if r["answer_text"] == "Yes":
            assert "Paragraph 1 of section 1 describes details number %d" % pi in r["context"]      # paras[3] = section 1, paragraph 1
        for other in range(4):
            if other != pi:
                assert "details number %d." % other not in r["context"]                            # never a paragraph of another paper


def test_unanswerable_has_paragraphs_without_gold_positions():
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=3)
    rows = [r for r in m.map_records(records(3), cap=100) if r["answer_text"] == "Unanswerable"]
    assert rows and all(r["extra"]["gold_positions"] == [] and r["extra"]["n_spans"] >= 1 for r in rows)


def test_gold_over_budget_dropped(monkeypatch):
    monkeypatch.setattr(Q, "BUDGET", 60)
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=1)
    assert [r for r in m.map_records(records(2), cap=100) if r["answer_text"] != "Unanswerable"] == []
    assert any(k.startswith("R10_length_drop_") for k in m.drops.c)


def test_reader_train_only_and_r4(tmp_path):
    (tmp_path / "qasper-train-v0.3.json").write_text(json.dumps({"1": {k: v for k, v in paper(1).items() if not k.startswith("_")}}))
    (tmp_path / "qasper-dev-v0.3.json").write_text(json.dumps({"2": {"title": "HELD OUT"}}))
    got = list(Q.read_train(str(tmp_path)))
    assert len(got) == 1 and got[0]["_pid"] == "1"
    m = Q.Mapper(T.pools_for(Q.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(2), cap=10) == []


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(Q.Mapper)
