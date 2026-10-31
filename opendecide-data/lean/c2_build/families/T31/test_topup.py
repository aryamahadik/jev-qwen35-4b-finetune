"""families/T31/test_topup.py: the T31 pool top-up (round 2), in memory only (nothing is written).

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T31/test_topup.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402
from families.T31 import plugin as P  # noqa: E402
from families.T31 import topup as T  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return T.files_for2(T.build_batches2(existing={"ch_scope": ["Which listed scope may {REQ_AGENT} use?"]}))


def _pools():
    return {"skins": {}, "attacks": {}, "wordings": {}, "packs_appr": [], "packs_agent": [], "names": [],
            "lexicon": HA.declare_lexicon(LexiconRegistry("T31"))}


TASK = {"task_id": "T31-author_test-000", "prompt_sha": "0" * 64}


def test_topup_tasks_are_self_contained_and_new(built):
    files, manifest = built
    tasks = manifest["tasks"]
    assert manifest["g0_sha256"] == P.POOL_G0_SHA256 and len(tasks) == 11
    assert {t["kind"] for t in tasks} == {"author_skin", "author_freeform", "author_wording"}
    n = {}
    for t in tasks:
        assert t["task_file"].startswith(str(T.ROOT2)) and t["answer_file"].startswith(str(T.ROOT2 / "answers"))
        text = files[t["task_file"].split("/haiku/redo2/")[1]]
        assert t["answer_file"] == text.split("\n")[3] and t["task_file"] in t["allowed_read"]
        assert t["allowed_write"] == [t["answer_file"]]
        items = json.loads(text[text.index("ITEMS (JSON"):].split("\n", 1)[1].rsplit("\n\nReminder", 1)[0])
        assert len(items) == t["n_items"] and all(re.fullmatch(r"q[0-9a-f]{10}", it["qid"]) for it in items)
        assert f"exactly {t['n_items']} objects" in text and all(it["qid"] in text.split("FULL INSTRUCTIONS")[0]
                                                                 for it in items)
        low = text.lower()
        for f in (HA.FORBID_WORDING if t["kind"] == "author_wording" else HA.FORBID_SKIN):
            assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low), (t["task"], f)
        n[t["pool"]] = n.get(t["pool"], 0) + t["n_items"]
    assert n["skin"] == sum(T.TOPUP_SKINS_T.values())
    assert n["freeform"] == 2 * sum(T.TOPUP_SKINS_F.values()) and n["wording"] == sum(T.TOPUP_WORDINGS.values())
    v1 = json.loads((HA.ROOT / "TASKS.json").read_text(encoding="utf-8"))
    assert not {t["batch_id"] for t in tasks} & {t["batch_id"] for t in v1["tasks"]}


def test_log_brief_matches_the_name_lint(built):
    files, manifest = built
    log = [t for t in manifest["tasks"] if t["register"] == "log"][0]
    text = files[log["task_file"].split("/haiku/redo2/")[1]]
    assert "ENTIRELY in lowercase" in text and T.RULE2_OLD not in text and "kind of" in text
    item = {"slots": {"REQ_ID": "leave it out"}}
    bad = "[desk] Hi, {REQUESTER} sent an approval request for the {ITEM}."
    good = "[desk] hi, {REQUESTER} sent an approval request for the {ITEM}.\n[desk] passing it to the desk."
    pools = _pools()
    assert "name: Hi" in HA._load_one(TASK, ["skin", "appr", "log", "T", "0"], item, {"text": bad}, "q0", pools)
    assert HA._load_one(TASK, ["skin", "appr", "log", "T", "1"], item, {"text": good}, "q1", pools) is None


def test_wording_briefs_match_the_wording_lint_and_neg_counts():
    assert "which one" not in T.QUESTION_MEANING_V2["ch_scope"][0].split("never")[0].lower()
    assert "'which of the listed scopes'" in T.QUESTION_MEANING_V2["ch_scope"][0]
    other = T.QUESTION_MEANING_V2["yn_holder_other"][0]
    assert "other than" in other and "Never 'besides'" in other and "'someone else'" not in other
    assert T.HA.QUESTION_SEM_MEANING is HA.QUESTION_SEM_MEANING      # the G-LEX choices are not touched
    item = {"slots": {"REQ_ID": "optional, at most once"}}
    cases = [("ch_scope", "Which one of the listed scopes may {REQ_AGENT} use at the time of the request?", False),
             ("ch_scope", "Going by the records, which of the listed scopes may {REQ_AGENT} use then?", True),
             ("yn_holder_other", "Does someone besides {CANDIDATE} hold the A role at the time of the request?",
              False),
             ("yn_holder_other", "Does a person other than {CANDIDATE} hold the A role at the time of the request?",
              True),
             ("yn_agent_ok", "May {REQ_AGENT} use {REQ_SCOPE} at the time of the request?", False),
             ("yn_agent_ok", "At the time of the request, may {REQ_AGENT} make use of {REQ_SCOPE}?", True),
             ("yn_agent_beyond", "Would using {REQ_SCOPE} go past the authority of {REQ_AGENT} then?", False)]
    pools = _pools()
    for i, (q, text, ok) in enumerate(cases):
        why = HA._load_one(TASK, ["wording", q, str(i)], item, {"text": text}, f"q{i}", pools)
        assert (why is None) == ok, (text, why)


def test_registry_meanings_are_the_v1_ones():
    # the G-LEX choices the new forms are read against are the v1 ones (so the v1 reads still verify)
    reg = HA.declare_lexicon(LexiconRegistry("T31"))
    f = reg.add("Which of the listed scopes may {REQ_AGENT} use when it asks?", "q.t31.ch_scope",
                slots={"REQ_AGENT": "id"}, source="haiku", family="T31",
                haiku_task_id="T31-test-000", haiku_prompt_sha="0" * 64)
    assert reg.unit_test(f.form_id)
    items = T.extraction_batches2(reg, [f.form_id])
    assert [r for r, _ in items] == list(T.READS2)
    choices = {m for _r, b in items for c in b.chunks for it in c["items"] for m in it["choices"]}
    assert choices == {s.meaning for s in reg.sems.values() if s.kind == "question"}
    assert items[0][1].batch_id != items[1][1].batch_id


def test_dedup_keeps_the_v1_piece():
    pools = _pools()
    old = K.make_skin("T31-appr-chat-qffffffffff", "T31", "{REQUESTER}: hi, about {a|ITEM}.",
                      {"REQUESTER": "name", "ITEM": "name"}, register="chat")
    new = K.make_skin("T31-appr-chat-q0000000000", "T31", "{REQUESTER}: hi,  about {a|ITEM}.",
                      {"REQUESTER": "name", "ITEM": "name"}, register="chat")
    pools["skins"] = {old.skin_id: old, new.skin_id: new}
    dropped = T.dedup_merged(pools, {"skins": {old.skin_id}, "attacks": set(), "wordings": set()})
    assert list(pools["skins"]) == [old.skin_id] and dropped[0][0] == f"skins|{new.skin_id}"


@pytest.mark.skipif(not (T.HERE / "pools" / "MANIFEST.json").is_file(), reason="no v1 freeze")
def test_plan_reaches_every_floor_with_spare():
    _files, manifest = T.files_for2(T.build_batches2(existing={}))
    rep = T.plan_report(manifest)
    for cell, d in rep["skin_cells"].items():
        assert d["v1"] < 24 <= d["max"] - 5, cell          # each short cell can lose >= 5 new pieces and still pass
    assert rep["wording_candidates_max"] >= 180
    for q, d in rep["wordings"].items():
        assert d["v1"] + d["new_items"] >= d["plan_v1"], q


def test_v1_redo_answer_merges_by_qid():
    res = T.load()
    redo = [d for d in res["drops"] if d[0].endswith(":redo")]
    assert res["resolved_by_redo"] == ["T31-author_wording-a7e52c11-000"] and not redo
    assert not [d for d in res["drops"] if d[0] == "T31-author_wording-a7e52c11-000" and d[1] == "*"]
    assert res["counts"]["new_lexicon_forms"] >= 1
    with pytest.raises(CH.ChunkError):
        CH.make_batch("author_wording", "T31", [("wording|x|0", {"brief": "escalate"})], seed="s", prompt="p",
                      forbid_strings=HA.FORBID_WORDING)
