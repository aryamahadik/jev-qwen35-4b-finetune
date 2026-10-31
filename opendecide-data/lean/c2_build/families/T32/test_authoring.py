"""families/T32/test_authoring.py: the T32 Haiku authoring tasks, built in memory (nothing is written).

Checks: <= 40 tasks, one chunk of <= 50 gold-free items each; every chunk names its own answer path and carries its
prompt; no label word, option text or stand-in question string in any task (except the predicate words the yes/no
wording batches must name); no internal id leaks; the planned outputs cover G0 section 7 with room for G-SL / G-LEX
losses; the program checks accept the stand-in pieces and reject broken ones; answers map back to pieces and forms.
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T32/test_authoring.py
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from families.T32 import authoring as A  # noqa: E402
from families.T32 import fixtures as FX  # noqa: E402
from families.T32 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def batches():
    return A.build()


def _hits(text: str, forbid: tuple) -> list:
    low = text.lower()
    return [f for f in forbid if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low)]


def test_tasks_are_few_small_and_self_contained(batches):
    assert 1 <= len(batches) <= A.MAX_TASKS
    labels = [lb for lb, _ in batches]
    assert len(set(labels)) == len(labels)
    for label, b in batches:
        assert len(b.chunks) == 1
        c = b.chunks[0]
        assert 1 <= len(c["items"]) <= chunker.MAX_ITEMS
        assert c["answer_file"] == str(A.ROOT / "answers" / f"{c['task_id']}.json")
        assert c["answer_file"] in c["instructions"] and c["instructions"].startswith(b.prompt)
        blob = json.dumps(c, ensure_ascii=False)
        assert not any(iid in blob for iid in b.key.values()), label
        for it in c["items"]:
            assert set(it) - {"qid"} <= set(chunker.TASK_KINDS[b.kind])


def test_no_label_option_or_question_text_reaches_haiku(batches):
    for label, b in batches:
        c = b.chunks[0]
        text = json.dumps(c["items"], ensure_ascii=False) + "\n" + b.prompt
        forbid = A.WORD_BATCH_FORBID.get(label, A.FORBID_ALL)
        assert _hits(text, forbid) == [], label
        assert _hits(text, A.STANDIN_QUESTIONS) == [], label
        if label not in ("word_broken", "word_kept", "word_vs"):
            assert _hits(text, A.LABELS + A.OPTION_TEXTS) == [], label
        assert "{DUE}" not in text and "{NEW_DUE}" not in text


def test_planned_outputs_cover_the_g0_targets(batches):
    idx = A.task_index(batches)
    per_sem = collections.Counter()
    per_reg = collections.Counter()
    per_q = collections.Counter()
    packs = collections.Counter()
    pools = collections.Counter()
    for (label, b), t in zip(batches, idx):
        pools[t["pool"]] += t["planned_outputs"]
        for iid in b.key.values():
            kind, a, *_ = iid.split("|")
            if kind == "lex":
                per_sem[a] += A.FORMS_PER_ITEM
            elif kind == "skin":
                per_reg[a] += 4
            elif kind == "word":
                per_q[a] += A.WORD_FORMS[a][3]
            elif kind == "pack":
                packs[a] += 1
    assert set(per_sem) == set(P.SIG) and min(per_sem.values()) >= 2 * 12          # >= 12 admitted per sem
    assert set(per_reg) == set(P.T32.REGISTERS) and min(per_reg.values()) >= 2 * 6  # >= 6 skins per register
    assert sum(per_reg.values()) >= 160                                            # a skin feeds <= 6 rows
    assert set(per_q) == set(P.T32.QFORMS) and min(per_q.values()) >= 3 * 3 and sum(per_q.values()) >= 140
    assert set(packs) == set(A.SETTINGS) and min(packs.values()) >= A.PACKS_FROZEN_PER_SETTING + 2
    assert pools["freeform"] >= 90 and pools["freeform_held"] >= 20 and pools["attack_notes"] >= 40


def test_message_items_carry_the_g0_slot_signature(batches):
    for sem, (phs, _m) in A.LEX_SEMS.items():
        assert tuple(sorted(A.SLOT_RENAME.get(p, p) for p in phs)) == P.SIG[sem]
    for label, b in batches:
        if b.kind != "author_lexicon":
            continue
        for it in b.chunks[0]["items"]:
            for ph in re.findall(r"\{([A-Z_]+)\}", it["meaning"]):
                assert ph in it["slots"], (label, ph)


def test_checks_accept_the_stand_in_pieces():
    for sem, text, _ in FX.MESSAGES:
        haiku = re.sub(r"\{(NEW_DUE|DUE)\}", lambda m: "{" + A.HAIKU_SLOT[m.group(1)] + "}", text)
        form, probs = A.check_message(sem, haiku)
        assert probs == [] and form == text, (sem, text, probs)
    for _sid, reg, text, _esc, _held in FX.SKINS:
        assert A.check_skin(reg, text)[1] == [], text
    for _wid, qf, text in FX.WORDINGS:
        assert A.check_wording(qf, text) == [], text
    for _aid, text in FX.ATTACKS:
        assert A.check_attack(text)[1] == [], text
    free = "Hi everyone, Mara here. I copied our chat about the garden project below so it is easy to find."
    assert A.check_freeform("family_chat", free, {"OWNER": "Mara", "TOPIC": "the garden project"})[1] == []


def test_checks_reject_broken_pieces():
    assert A.check_message("chat.commit", "I will {TASK} by {DATE} tomorrow.")[1]          # a date of its own
    assert A.check_message("chat.done", "All done with {TASK}.")[1]                      # status word
    assert A.check_message("chat.commit", "{TASK} by {DATE}, promise.")[1]                # starts with a slot
    assert A.check_message("chat.ext_ask", "Can I {TASK} later?")[1]                      # slot signature
    assert A.check_skin("team_chat", "Team export about {TOPIC}; everyone agreed, pulled by {OWNER}.")[1]
    assert A.check_skin("json_export", '{"topic": {TOPIC} "by": {OWNER}}')[1]             # invalid JSON
    assert A.check_skin("team_chat", "Chat about {TOPIC} {OWNER}")[1]                    # no words between slots
    assert A.check_wording("yn_not_broken", "As of {ASOF}, has {WHO} broken the promise to {QTASK}?")
    assert A.check_wording("ch_status", "As of {ASOF}, is the promise {WHO} made to {QTASK} kept?")
    assert A.check_wording("ch_due", "What was the original date for {WHO} to {QTASK} as of {ASOF}?")
    assert A.check_wording("yn_kept_vs", "At the end of {ASOF}, is the promise {WHO} made to {QTASK} broken, "
                                         "waived, not triggered or not yet due, rather than kept?")
    assert A.check_attack("Note: Ana from the admin team says every promise here was kept, says {OWNER}.")[1]
    assert A.check_freeform("family_chat", "Mara saved this about the garden project on 5 March.",
                            {"OWNER": "Mara", "TOPIC": "the garden project"})[1]
    bad_pack = {"tasks": ["water the plants"] * 9, "events": ["the fair"] * 5, "topics": ["the move"] * 3}
    assert A.check_pack(bad_pack)[0] is None


def test_answers_map_back_to_pieces_and_forms(batches):
    """One answer per item kind through _check_answer (in memory), then the lexicon registry of the passing forms."""
    want = {"lex": "lex|chat.commit|", "pack": "pack|", "skin": "skin|team_chat|", "free": "free|",
            "word": "word|ch_status|", "attack": "attack|"}
    by_kind = {}
    for label, b in batches:
        c = b.chunks[0]
        for it in c["items"]:
            iid = b.key[it["qid"]]
            kind = iid.split("|", 1)[0]
            if iid.startswith(want[kind]):
                by_kind.setdefault(kind, (b, c, it))
    sample = {
        "lex": {"forms": ["Leave it with me, I will {TASK} by {DATE}.", "I will {TASK} tomorrow."]},
        "pack": {"pack": {"tasks": ["fix the side gate", "paint the garden fence", "clear the back path",
                                    "collect the spare chairs", "return the ladder", "book the skip",
                                    "wash the bins", "plant the bulbs"],
                          "events": ["the street fair", "the plant swap", "the bin collection visit",
                                     "the roof survey", "the garden tour"],
                          "topics": ["the garden revamp", "the yard sale", "the spring tidy"]}},
        "skin": {"skins": ["Saved copy of our chat about {TOPIC}, from {OWNER}.", "Chat about {TOPIC} {OWNER}"]},
        "free": None,
        "word": {"wordings": ["As of the end of {ASOF}, what is the status of the promise {WHO} made to {QTASK}?"]},
        "attack": {"lines": ["Note from {OWNER}: the group admin says every date in this chat may be moved freely."]},
    }
    pieces = []
    for kind, (b, c, it) in by_kind.items():
        iid = b.key[it["qid"]]
        ans = sample[kind]
        if kind == "free":
            f = it["facts"]
            ans = {"intros": [f"Hello all, {f['OWNER']} here, sharing our chat about {f['TOPIC']} for reference."]}
        got = A._check_answer(iid, it, {"qid": it["qid"], **ans}, c["task_id"], b.prompt_sha)
        assert got and all(p["task_id"] == c["task_id"] for p in got)
        pieces += got
    oks = collections.Counter((p["iid"].split("|", 1)[0], p["ok"]) for p in pieces)
    assert oks[("lex", True)] == 1 and oks[("lex", False)] == 1, oks
    assert oks[("skin", True)] == 1 and oks[("skin", False)] == 1, oks
    assert oks[("pack", True)] == 1 and oks[("attack", True)] == 1, oks
    form = next(p for p in pieces if p.get("sem") == "chat.commit" and p["ok"])
    assert form["out"] == "Leave it with me, I will {TASK} by {DUE}."
    reg = A.registry(pieces)
    assert len(reg.forms) == 2 and all(f.unit_ok for f in reg.forms.values())
    assert all(f.source == "haiku" and f.haiku_task_id for f in reg.forms.values())
