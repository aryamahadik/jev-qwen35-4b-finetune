"""transfer/T19/test_redo3_reads.py: in-memory tests of the T19 redo round 3 read step (redo3_reads.py). Nothing here
writes a file. The mutated answers are test inputs for the checks, never answers to a task; no read answer is made."""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

import pytest

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit.paths import never_open  # noqa: E402
from transfer.T19 import extract_build as EX  # noqa: E402
from transfer.T19 import redo3 as R3  # noqa: E402
from transfer.T19 import redo3_reads as RR  # noqa: E402


@pytest.fixture(scope="module")
def task():
    return RR.task()


@pytest.fixture(scope="module")
def raw(task):
    return json.loads(Path(task["answer_file"]).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def res(raw):
    return RR.build(raw)


def test_task_is_the_one_on_disk(task):
    assert task["name"] == "T19-redo3-wordings-000" and task["n_items"] == 2 and task["n_candidates"] == 3
    assert task["order"] == task["qids"] and task["gap"] == 1
    assert RR.AUDIT_FAILED == ()


def test_answer_meets_its_contract(task, raw):
    cands, probs = RR.load_answer(task, raw)
    assert probs == [] and set(cands) == set(task["qids"]) and all(len(v) == 3 for v in cands.values())


@pytest.mark.parametrize("mut", [
    lambda a: {"qid": "qdeadbeef00", "texts": a[0]["texts"]},          # unknown qid
    lambda a: {"qid": a[0]["qid"], "texts": a[0]["texts"][:2]},        # 2 texts
    lambda a: {"qid": a[0]["qid"], "texts": a[0]["texts"], "x": 1},     # extra key
    lambda a: {"qid": a[0]["qid"], "texts": [a[0]["texts"][0]] * 3},    # not all different
    lambda a: {"qid": a[0]["qid"], "texts": a[0]["texts"][:2] + [3]},   # not a string
])
def test_contract_violations_reject_the_whole_answer(task, raw, mut):
    bad = copy.deepcopy(raw)
    bad[0] = mut(bad)
    cands, probs = RR.load_answer(task, bad)
    assert cands == {} and probs


def test_contract_not_an_array_missing_or_repeated(task, raw):
    assert RR.load_answer(task, {"qid": "x"})[0] == {}
    assert RR.load_answer(task, raw[:1])[0] == {}                       # one item unanswered
    assert RR.load_answer(task, [raw[0], raw[0]])[0] == {}              # a qid twice
    assert RR.load_answer(task, raw + [raw[0]])[0] == {}


def test_lint_keeps_all_six(task, raw):
    cands, _ = RR.load_answer(task, raw)
    rows = RR.lint(task, cands)
    assert [r["qid"] for r in rows] == [q for q in task["order"] for _ in range(3)]
    assert [r["j"] for r in rows] == [0, 1, 2, 0, 1, 2]
    assert all(r["ok"] and not r["reasons"] for r in rows)
    assert all(r["text"].count("{SITE}") == 1 for r in rows)


def _lint_one(task, raw, q_index, j, text):
    cands, _ = RR.load_answer(task, raw)
    cands = copy.deepcopy(cands)
    cands[task["order"][q_index]][j] = text
    return [r for r in RR.lint(task, cands) if r["qid"] == task["order"][q_index] and r["j"] == j][0]


@pytest.mark.parametrize("text,why", [
    ("Using the card's definitions, is {SITE} non-compliant with its checklist on the audit date?", "phrase"),
    ("Using the card's definitions, is {SITE} not in compliance with its checklist on the audit date?", "phrase"),
    ("Using the card's definitions, isn't {SITE} not compliant with its checklist on the audit date?", "negation"),
    ("Using the card's definitions, is {SITE} not compliant with its checklist on the audit date, now?", "ending"),
    ("Using the card's definitions, is {SITE} not compliant with its checklist on the 3 audit date?", "digit"),
    ("Using the card's definitions, is {SITE} not compliant with its checklist?", "audit date"),
    ("Using the card's definitions, is {SITE} not compliant with {SITE}'s checklist on the audit date?", "slot"),
    ("Measured against the card, is {SITE} not compliant with its checklist on the audit date?", "opening"),
])
def test_lint_refuses_a_broken_candidate(task, raw, text, why):
    r = _lint_one(task, raw, 0, 0, text)
    assert not r["ok"] and r["reasons"], why


def test_dedup_against_every_earlier_wording(task, raw):
    frozen = json.loads((RR.POOLS_V2 / "wordings.json").read_text(encoding="utf-8"))
    # a pools_v2 wording is a duplicate wherever it is repeated
    same = next(w["text"] for w in frozen if w["qform"] == "yn_not_compliant" and w["text"].startswith("As the records"))
    assert RR._norm(same) in RR.seen_texts()
    # every round 1, redo2 and quarantined text is in the dedup set
    seen = RR.seen_texts()
    assert len(seen) >= 160 and all(RR._norm(w["text"]) in seen for w in frozen)
    q = json.loads((RR.POOLS_V2 / "quarantine.json").read_text(encoding="utf-8"))
    assert all(RR._norm(f["text"]) in seen for s in q.values() for f in s["forms_not_admitted"])
    assert RR._norm("Per the card, is {SITE} not in compliance with its checklist on the audit date?") in seen
    # none of the six is among them, and a repeat inside the answer is refused
    cands, _ = RR.load_answer(task, raw)
    assert not any(RR._norm(t) in seen for v in cands.values() for t in v)
    r = _lint_one(task, raw, 1, 1, cands[task["order"][0]][0])
    assert not r["ok"]


def test_glex_registry_admits_the_six_beside_the_frozen_lexicon(task, res):
    reg, fid_of = res["reg"], res["fid_of"]
    assert len(fid_of) == 6 and res["lex_drops"] == []
    assert len(reg.forms) == 113 + 6
    assert all(reg.forms[f].unit_ok for f in reg.forms)
    frozen = json.loads((RR.POOLS_V2 / "lexicon.json").read_text(encoding="utf-8"))
    assert {f["form_id"] for f in frozen["forms"]} <= set(reg.forms)
    assert set(fid_of.values()).isdisjoint(f["form_id"] for f in frozen["forms"])
    assert all(reg.forms[f].sem_id == "q.t19.yn_not_compliant" and reg.forms[f].required == 2
               for f in fid_of.values())
    # the new extractor ids are new: no frozen form was ever read by them
    used = {e for f in frozen["forms"] for e, _s in f["extractions"]}
    assert not used & {x[1] for x in RR.GLEX_READS}
    assert len({x[1] for x in RR.GLEX_READS}) == len(RR.GLEX_READS) == 2
    # nothing has been read yet: every new form is pending, none admitted by this code
    assert {reg.status(f) for f in fid_of.values()} == {"pending"}


def test_two_independent_reads_one_task_file_each(task, res):
    assert len(res["reads"]) == 2 and len(res["tasks"]) == 2
    assert [t["extractor_id"] for t in res["tasks"]] == [x[1] for x in RR.GLEX_READS]
    b1, b2 = (g["batch"] for g in res["reads"])
    assert b1.batch_id != b2.batch_id and b1.seed != b2.seed and len(b1.chunks) == len(b2.chunks) == 1
    assert sorted(b1.key.values()) == sorted(b2.key.values()) == sorted(res["fid_of"].values())
    c1, c2 = b1.chunks[0]["items"], b2.chunks[0]["items"]
    assert len(c1) == len(c2) == 6
    assert {i["qid"] for i in c1}.isdisjoint({i["qid"] for i in c2})
    assert sorted(i["text"] for i in c1) == sorted(i["text"] for i in c2)
    assert [i["text"] for i in c1] != [i["text"] for i in c2] or [i["choices"] for i in c1] != [i["choices"] for i in c2]
    t1, t2 = res["tasks"]
    assert t1["task_file"] != t2["task_file"] and t1["answer_file"] != t2["answer_file"]
    for t in res["tasks"]:
        assert t["task_file"].startswith(str(RR.XROOT / "tasks")) and t["answer_file"].startswith(str(RR.XROOT / "answers"))
        assert t["allowed_read"] == [t["task_file"]] and t["allowed_write"] == [t["answer_file"]]
        assert not never_open(t["task_file"]) and not never_open(t["answer_file"])
        assert t["n_items"] == t["outputs_expected"] == 6


def test_each_task_text_is_self_contained_and_leaks_nothing(task, res):
    cand_texts = {RR._norm(r["text"].replace("{SITE}", RR.SAMPLE_SITE)) for r in res["lint"]}
    for t in res["tasks"]:
        text = res["files"][f"tasks/{t['task_id']}.md"]
        assert text.startswith(f"# T19 extraction task {t['task_id']}\n")
        assert t["answer_file"] in text and EX.PROMPT_LEX in text
        assert "Answer format: [{\"qid\": \"<qid>\", \"meaning\": \"<one choice, copied exactly>\"}, ...]" in text
        assert "only file you may open" in text
        items = json.loads(text.split("answer every item once, keyed by its qid)\n\n", 1)[1])
        assert len(items) == 6 and all(set(i) == {"qid", "text", "choices"} for i in items)
        assert all(re.fullmatch(r"q[0-9a-f]{10}", i["qid"]) for i in items)
        assert {RR._norm(i["text"]) for i in items} == cand_texts
        assert all(len(i["choices"]) == 6 and len(set(i["choices"])) == 6 for i in items)
        assert all("Larch Street depot" in i["text"] and "{" not in i["text"] for i in items)
        low = text.lower()
        for bad in ("t19a.", "q.t19.", "yn_", "ch_gap", "|c0", "|c1", "|c2", "form_id", "gold", "ohs"):
            assert bad not in low, bad
        for fid in res["fid_of"].values():
            assert fid not in text
    # the closed meaning list is the frozen one, unchanged
    reg_meanings = sorted(s.meaning for s in res["reg"].sems.values())
    assert all(sorted(i["choices"]) == reg_meanings for g in res["reads"] for i in g["batch"].chunks[0]["items"])


def test_the_prompt_is_the_frozen_one(res):
    assert all(g["batch"].prompt == EX.PROMPT_LEX for g in res["reads"])
    assert {g["batch"].prompt_sha for g in res["reads"]} == {RR._sha(EX.PROMPT_LEX)}


def test_file_set_and_key(res):
    fs = res["files"]
    names = set(fs)
    assert {"TASKS.json", "LINT.json", "key/glex_forms.json", "answers/README.txt"} <= names
    assert sum(n.startswith("tasks/") for n in names) == 2 and sum(n.startswith("chunks/") for n in names) == 2
    key = json.loads(fs["key/glex_forms.json"])
    assert len(key) == 6 and all(v["form_id"] for v in key.values())
    tasks_json = json.loads(fs["TASKS.json"])
    assert tasks_json["n_tasks"] == 2 and tasks_json["outputs_expected"] == 12 and tasks_json["lexicon_drops"] == []
    lint_json = json.loads(fs["LINT.json"])
    assert len(lint_json["candidates"]) == 6 and all(c["ok"] for c in lint_json["candidates"])
    assert "may not exceed its target 14" in lint_json["keep_rule"]
    for rel in names:
        assert not never_open(str(RR.XROOT / rel))


def test_build_is_deterministic(res, raw):
    again = RR.build(raw)
    assert again["files"] == res["files"]


def test_nothing_in_g0_or_the_targets_moved():
    assert R3.P.T19Plugin.G0_SHA256_AUTHORED == json.loads(RR.INDEX.read_text(encoding="utf-8"))["g0_sha256"]
    assert R3.shortfalls() == [{"admitted": 13, "item": R3.CELL, "shortfall": 1, "target": 14}]


def test_files_on_disk_equal_the_build_when_written(res):
    if not RR.XROOT.exists():
        pytest.skip("reads not written yet")
    for rel, text in res["files"].items():
        if rel == "LINT.json":
            continue                     # carries the sha of the answer file, built here from the test input
        assert (RR.XROOT / rel).read_text(encoding="utf-8") == text, rel
