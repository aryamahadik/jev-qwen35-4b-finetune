"""families/T07/test_validate_answers.py: the strict Haiku answer-contract validator (validate_answers.py).

Contract cases are built in memory or on pytest's tmp_path; the repository is only read.
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T07/test_validate_answers.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T07 import validate_answers as V  # noqa: E402

SCHEMA = [{"field": "store", "type": "name", "describe": "the store"},
          {"field": "region_rule", "type": "enum", "describe": "rule", "choices": ["in", "out", "absent"]},
          {"field": "region_bound", "type": "category", "describe": "value", "choices": ["Arvale"]}]
G3H_ITEM = {"qid": "qaaaaaaaaaa", "text": "t", "schema": SCHEMA}
LEX_ITEM = {"qid": "qbbbbbbbbbb", "text": "t", "choices": ["meaning one", "meaning two"]}


def test_expected_outputs_reads_the_items_own_brief():
    assert V.expected_outputs("author_pack", {"qid": "q", "brief": {"ladder_levels": 3}}) == 1
    assert V.expected_outputs("author_freeform", {"qid": "q", "brief": "write one text"}) == 1
    assert V.expected_outputs("author_skin", {"qid": "q", "brief": "tone: x; write 5 different texts"}) == 5
    assert V.expected_outputs("author_skin", {"qid": "q", "brief": "style: y; write 4 different notes"}) == 4
    assert V.expected_outputs("author_wording", {"qid": "q", "brief": {"how_many": 6}}) == 6
    with pytest.raises(ValueError):
        V.expected_outputs("author_skin", {"qid": "q", "brief": "no count here"})


def test_text_lists_must_have_the_exact_count_and_only_strings():
    item = {"qid": "q", "brief": {"how_many": 3}}
    assert V.check_value("author_lexicon", "forms", item, ["a.", "b.", "c."]) == []
    assert any("asks for 3" in p for p in V.check_value("author_lexicon", "forms", item, ["a.", "b."]))
    assert any("not a non-empty string" in p for p in V.check_value("author_lexicon", "forms", item, ["a.", "", 3]))
    assert V.check_value("author_lexicon", "forms", item, "a.")[0].startswith("not a list")
    assert V.check_value("author_freeform", "text", item, "one text") == []
    assert V.check_value("author_freeform", "text", item, ["one text"]) != []
    assert V.check_value("author_freeform", "text", item, "  ") != []


def test_pack_object_shape():
    item = {"qid": "q", "brief": {"ladder_levels": 3}}
    ok = {"store": "S", "ladder": ["a", "b", "c"], "regions": ["r"] * 4, "categories": ["c"] * 3, "customers": ["n"] * 4}
    assert V.check_value("author_pack", "pack", item, ok) == []
    assert any("keys" in p for p in V.check_value("author_pack", "pack", item, dict(ok, extra=1)))
    assert any("levels" in p for p in V.check_value("author_pack", "pack", item, dict(ok, ladder=["a", "b"])))
    assert V.check_value("author_pack", "pack", item, dict(ok, store=3)) != []
    assert V.check_value("author_pack", "pack", item, "pack") == ["pack is not an object"]


def test_lex_meaning_is_copied_exactly_from_the_choices():
    assert V.check_value("extract_lex", "meaning", LEX_ITEM, "meaning one") == []
    assert V.check_value("extract_lex", "meaning", LEX_ITEM, "Meaning one") != []        # not character for character
    assert V.check_value("extract_lex", "meaning", LEX_ITEM, "meaning one.") != []
    assert V.check_value("extract_lex", "meaning", LEX_ITEM, None) != []


def test_g3h_extraction_has_exactly_the_schema_fields():
    ok = {"store": "Wrenfield", "region_rule": "in", "region_bound": "Arvale"}
    assert V.check_value("extract_g3h", "extraction", G3H_ITEM, ok) == []
    assert V.check_value("extract_g3h", "extraction", G3H_ITEM, dict(ok, region_rule="absent", region_bound=None)) == []
    assert any("missing" in p for p in V.check_value("extract_g3h", "extraction", G3H_ITEM,
                                                      {k: v for k, v in ok.items() if k != "store"}))
    assert any("extra" in p for p in V.check_value("extract_g3h", "extraction", G3H_ITEM, dict(ok, bonus="x")))
    assert any("choices" in p for p in V.check_value("extract_g3h", "extraction", G3H_ITEM, dict(ok, region_rule="maybe")))
    assert any("int" in p for p in V.check_value("extract_g3h", "extraction", G3H_ITEM, dict(ok, region_bound=5)))
    assert V.check_value("extract_g3h", "extraction", G3H_ITEM, [ok]) == ["extraction is not an object"]


def test_array_level_contract():
    chunk = {"items": [dict(LEX_ITEM), dict(LEX_ITEM, qid="qcccccccccc")]}
    good = [{"qid": "qbbbbbbbbbb", "meaning": "meaning one"}, {"qid": "qcccccccccc", "meaning": "meaning two"}]
    assert V.check_answer_array("extract_lex", "meaning", chunk, good, 2) == []
    assert V.check_answer_array("extract_lex", "meaning", chunk, {"a": 1}, 2)[0].startswith("the file holds dict")
    assert any("1 objects" in p for p in V.check_answer_array("extract_lex", "meaning", chunk, good[:1], 2))
    assert any("unanswered" in p for p in V.check_answer_array("extract_lex", "meaning", chunk, good[:1], 1))
    dup = [good[0], dict(good[0])]
    assert any("twice" in p for p in V.check_answer_array("extract_lex", "meaning", chunk, dup, 2))
    foreign = [good[0], {"qid": "qzzzzzzzzzz", "meaning": "meaning two"}]
    assert any("not in this task" in p for p in V.check_answer_array("extract_lex", "meaning", chunk, foreign, 2))
    extra_key = [good[0], dict(good[1], note="x")]
    assert any("keys" in p for p in V.check_answer_array("extract_lex", "meaning", chunk, extra_key, 2))
    wrong_key = [good[0], {"qid": "qcccccccccc", "text": "meaning two"}]
    assert any("keys" in p for p in V.check_answer_array("extract_lex", "meaning", chunk, wrong_key, 2))


def _fake_round(tmp_path: Path, answer_text: str | None) -> tuple:
    """A one-task round under tmp_path; returns (round root, TASKS.json row)."""
    root = tmp_path / "round"
    (root / "chunks").mkdir(parents=True)
    (root / "answers").mkdir()
    (root / "tasks").mkdir()
    tid = "T07-extract_lex-test-000"
    chunk = {"task_id": tid, "kind": "extract_lex", "prompt_sha": "x", "items": [dict(LEX_ITEM)]}
    (root / "chunks" / f"{tid}.json").write_text(json.dumps(chunk), encoding="utf-8")
    task_text = "task text\n"
    (root / "tasks" / f"{tid}.md").write_text(task_text, encoding="utf-8")
    if answer_text is not None:
        (root / "answers" / f"{tid}.json").write_text(answer_text, encoding="utf-8")
    import hashlib
    row = {"task_id": tid, "kind": "extract_lex", "n_items": 1, "outputs_expected": 1,
           "task_file": str(root / "tasks" / f"{tid}.md"), "answer_file": str(root / "answers" / f"{tid}.json"),
           "task_sha256": hashlib.sha256(task_text.encode()).hexdigest()}
    (root / "TASKS.json").write_text(json.dumps({"tasks": [row]}), encoding="utf-8")
    return root, row


def test_validate_task_statuses(tmp_path):
    good = json.dumps([{"qid": "qbbbbbbbbbb", "meaning": "meaning one"}])
    root, row = _fake_round(tmp_path / "a", good)
    assert V.validate_task(root, row)["status"] == "valid"
    root, row = _fake_round(tmp_path / "b", None)
    assert V.validate_task(root, row)["status"] == "missing"
    root, row = _fake_round(tmp_path / "c", "```json\n" + good + "\n```")
    r = V.validate_task(root, row)
    assert r["status"] == "invalid" and "not valid UTF-8 JSON" in r["problems"][0]
    root, row = _fake_round(tmp_path / "d", good + "\nthanks")
    assert V.validate_task(root, row)["status"] == "invalid"
    root, row = _fake_round(tmp_path / "e", json.dumps([{"qid": "qbbbbbbbbbb", "meaning": "invented"}]))
    assert V.validate_task(root, row)["status"] == "invalid"
    root, row = _fake_round(tmp_path / "f", good)
    (root / "tasks" / f"{row['task_id']}.md").write_text("task text changed\n", encoding="utf-8")
    r = V.validate_task(root, row)
    assert r["status"] == "invalid" and any("task file sha256" in p for p in r["problems"])


def test_failed_audit_answers_are_ignored_unread(tmp_path):
    root, row = _fake_round(tmp_path, "not even json")
    rep = V.validate_round("fake", root, failed_audit=[row["task_id"]])
    assert rep["ignored"] == [row["task_id"]] and rep["invalid"] == [] and rep["valid"] == 0


def test_extra_answer_files_are_reported(tmp_path):
    good = json.dumps([{"qid": "qbbbbbbbbbb", "meaning": "meaning one"}])
    root, _row = _fake_round(tmp_path, good)
    (root / "answers" / "README.txt").write_text("x", encoding="utf-8")
    (root / "answers" / "stray.json").write_text("[]", encoding="utf-8")
    rep = V.validate_round("fake", root)
    assert rep["extra_files"] == ["stray.json"] and rep["valid"] == 1


def test_all_real_answer_files_of_every_round_meet_their_contract():
    rep = V.validate_all()
    sizes = {r["round"]: r["tasks"] for r in rep["rounds"]}
    assert sizes == {"v1-author": 27, "v1-extract": 15, "redo2-author": 15, "redo2-extract": 12}
    assert rep["ok"], rep["invalid_task_ids"]
    assert len(rep["valid_task_ids"]) == 69


def test_validator_does_not_write(tmp_path):
    before = {p: p.stat().st_mtime_ns for r in V.ROUNDS.values() for p in (r / "answers").glob("*.json")}
    V.validate_all()
    assert before == {p: p.stat().st_mtime_ns for p in before}
