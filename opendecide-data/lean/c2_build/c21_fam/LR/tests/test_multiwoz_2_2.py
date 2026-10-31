import json

import pytest

import lr_common as lc
import lr_testlib as T
import multiwoz_2_2 as M


def dialogue(i):
    turns, acts = [], {}
    msgs = [("USER", "I need a restaurant in the centre number %d" % i, {"Restaurant-Inform": [["area", "centre"]]}),
            ("SYSTEM", "What price range do you prefer?", {"Restaurant-Request": [["pricerange", "?"]]}),
            ("USER", "cheap please", {"Restaurant-Inform": [["pricerange", "cheap"]]}),
            ("SYSTEM", "Pizza Hut City Centre is cheap and central.", {"Restaurant-Inform": [["name", "Pizza Hut"]]}),
            ("USER", "thanks", {"general-thank": []}),
            ("SYSTEM", "You are welcome.", {"general-welcome": []})]
    for k, (sp, tx, ac) in enumerate(msgs):
        turns.append({"frames": [], "speaker": sp, "turn_id": k, "utterance": tx})
        acts[str(k)] = {"dialog_act": ac, "span_info": []}
    return {"dialogue_id": "MUL%04d.json" % i, "services": ["restaurant"], "turns": turns, "_acts": acts, "_src_line": "MUL%04d.json" % i}


def records(n=20):
    return [dialogue(i) for i in range(n)]


def test_rows_balanced_and_labels_from_system_acts():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    rows = m.map_records(records(), cap=30)
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=20)
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["R7_pass"]
    for r in rows:
        want = "Yes" if any(a.endswith("-Request") for a in r["extra"]["acts"]) else "No"
        assert r["answer_text"] == want
        assert r["context"].splitlines()[0].startswith("User:")


def test_at_most_two_rows_per_dialogue_and_no_user_turn_rows():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    rows = m.map_records(records(5), cap=100)
    per = {}
    for r in rows:
        per[r["source_row_id"].split("#")[0]] = per.get(r["source_row_id"].split("#")[0], 0) + 1
        ti = int(r["source_row_id"].rsplit("#", 1)[1])
        assert ti % 2 == 1                                # SYSTEM turns only (odd indexes in the fixture)
    assert max(per.values()) <= 2


def test_history_budget_and_first_turn_kept():
    turns = [{"speaker": "USER" if i % 2 == 0 else "SYSTEM", "turn_id": i, "utterance": "word " * 40 + str(i)} for i in range(40)]
    h = M._history(turns, 39)
    assert h.splitlines()[0].startswith("User:") and "[... earlier turns omitted ...]" in h and lc.approx_tokens(h) <= M.BUDGET + 20


def test_reader_and_user_acts_never_used(tmp_path):
    (tmp_path / "train").mkdir()
    d = dialogue(1)
    d.pop("_acts"); d.pop("_src_line")
    (tmp_path / "train" / "dialogues_001.json").write_text(json.dumps([d]))
    (tmp_path / "dialog_acts.train.json").write_text(json.dumps({d["dialogue_id"]: dialogue(1)["_acts"]}))
    got = list(M.read_train(str(tmp_path)))
    assert len(got) == 1 and got[0]["_acts"]["1"]["dialog_act"]


def test_r4_and_refusal():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(3)) == []
    T.check_dry_run_refusal(M.Mapper)
