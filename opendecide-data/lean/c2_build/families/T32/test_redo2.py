"""families/T32/test_redo2.py: the T32 Mode F redo2 round, in memory (nothing is written; no Haiku answer is read).

Checks: one gold-free authoring chunk of <= 50 items with its own answer path; no label, option or question text; the
sample facts never use a value a fixed authoring check refuses (the swap-probe owner, a topic with a SKIN_BANNED word);
every item's own shape passes the full redo2 lint; the role lint refuses the round-1 participant-style and describing
intros and accepts saver-style ones; the lint is never looser than authoring.check_freeform; an end-to-end pass on
stand-in texts keeps the G3-H contract and bar (template = register within the round, 98%).
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T32/test_redo2.py
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

from c2_kit import chunker, g3h  # noqa: E402
from families.T32 import authoring as A  # noqa: E402
from families.T32 import extract as X  # noqa: E402
from families.T32 import redo2 as R  # noqa: E402

ROUND1_FAILED = [   # round-1 intros whose G3-H owner read was NONE (participant-style or describing the intro)
    ("family_chat", "Family group chat with Priya about the anniversary party, messages below in order of sending.",
     {"OWNER": "Priya", "TOPIC": "the anniversary party"}),
    ("freelance_client", "Log header: Femi is named in this exchange, and the spring clean-up is the subject line.",
     {"OWNER": "Femi", "TOPIC": "the spring clean-up"}),
    ("team_chat", "Export header of a team chat that lists Elif as a member, and the fundraising drive is the main "
                  "topic.", {"OWNER": "Elif", "TOPIC": "the fundraising drive"}),
    ("sms_export", "Text thread with Hana, covering the summer holiday.",
     {"OWNER": "Hana", "TOPIC": "the summer holiday"}),
    ("support_thread", "In any setting, Tomas is the contact for the garden project.",
     {"OWNER": "Tomas", "TOPIC": "the garden project"}),
]
SAVER_STYLE = [
    ("family_chat", "Nadia saved this family chat about the summer holiday.",
     {"OWNER": "Nadia", "TOPIC": "the summer holiday"}),
    ("landlord_tenant", "Messages with our landlord about the lease renewal, copied into the rental file by Leila.",
     {"OWNER": "Leila", "TOPIC": "the lease renewal"}),
    ("team_chat", "Team channel: the office move\nExported by Malik.", {"OWNER": "Malik", "TOPIC": "the office move"}),
    ("support_thread", "Attached chat: the house move\nShared by: Priya",
     {"OWNER": "Priya", "TOPIC": "the house move"}),
    ("forum_thread", "Reposted chat: the garden project\nPosted here by Zara for the forum.",
     {"OWNER": "Zara", "TOPIC": "the garden project"}),
]


@pytest.fixture(scope="module")
def batches():
    return R.author_batches()


def _items(batches):
    return [it for _label, b in batches for c in b.chunks for it in c["items"]]


def test_small_self_contained_authoring_chunks(batches):
    assert [lb for lb, _ in batches] == ["free", "free_held"]
    regs = {}
    for label, b in batches:
        assert len(b.chunks) == 1
        c = b.chunks[0]
        assert 1 <= len(c["items"]) <= chunker.MAX_ITEMS
        assert c["answer_file"] == str(R.AUTHOR_ROOT / "answers" / f"{c['task_id']}.json")
        assert c["answer_file"] in c["instructions"] and c["instructions"].startswith(b.prompt)
        blob = json.dumps(c, ensure_ascii=False)
        assert not any(iid in blob for iid in b.key.values())
        regs[label] = {it["register"] for it in c["items"]}
        for it in c["items"]:
            assert set(it) - {"qid"} <= set(chunker.TASK_KINDS["author_freeform"])
            assert set(it["facts"]) == {"OWNER", "TOPIC"}
            assert it["facts"]["OWNER"] in it["brief"]           # the saver role is stated per item
    assert regs == {"free": set(R.TRAIN_REGS), "free_held": set(R.HELD_REGS)}
    assert regs["free_held"] == set(A.HELD_REGISTERS)
    assert len(_items(batches)) == len(R.TRAIN_REGS + R.HELD_REGS) * R.ITEMS_PER_REGISTER


def test_build_is_deterministic(batches):
    again = R.author_batches()
    for (_l1, a), (_l2, b) in zip(again, batches):
        assert a.key == b.key and a.manifest() == b.manifest()


def test_no_label_option_or_question_text_reaches_haiku(batches):
    for _label, b in batches:
        text = (json.dumps(b.chunks[0]["items"], ensure_ascii=False) + "\n" + b.prompt).lower()
        hits = [f for f in A.FORBID_ALL
                if f and re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", text)]
        assert hits == []


def test_sample_facts_avoid_values_the_fixed_checks_refuse(batches):
    names, topics, excluded = R.safe_values()
    for it in _items(batches):
        f = it["facts"]
        assert f["OWNER"] in names and f["OWNER"] not in excluded
        assert not set(f["TOPIC"].split()) & A.SKIN_BANNED
    assert R.self_check() == []


def test_role_lint_refuses_round1_failures_and_accepts_saver_style():
    for reg, text, facts in ROUND1_FAILED:
        tpl, pr = R.lint(reg, text, facts)
        assert tpl is None and pr, text
    for reg, text, facts in SAVER_STYLE:
        tpl, pr = R.lint(reg, text, facts)
        assert pr == [] and "{OWNER}" in tpl and "{TOPIC}" in tpl, (text, pr)


def test_redo2_lint_is_never_looser_than_check_freeform():
    for reg, text, facts in ROUND1_FAILED + SAVER_STYLE + [
            ("flatmates", "Our flat chat about the quarterly release, saved by Priya.",
             {"OWNER": "Priya", "TOPIC": "the quarterly release"}),
            ("flatmates", "Our flat chat about the spring clean-up, saved by Priya, all done.",
             {"OWNER": "Priya", "TOPIC": "the spring clean-up"})]:
        _sk, base = A.check_freeform(reg, text, facts)
        tpl, pr = R.lint(reg, text, facts)
        if base:
            assert tpl is None and pr


def _stand_in_answers(batches) -> dict:
    """In-memory texts shaped like a good answer (distinct per intro, so the template dedup keeps them)."""
    adjs = ("family", "house", "club", "team", "forum", "project", "garden", "kitchen", "office", "music",
            "reading", "cycling")
    nouns = ("archive", "folder", "binder", "drawer", "shelf", "notebook", "scrapbook", "logbook", "album", "box")
    out, k = {}, 0
    for _label, b in batches:
        out[b.chunks[0]["task_id"]], k = _stand_in_for(b, adjs, nouns, k)
    return out


def _stand_in_for(b, adjs, nouns, k) -> tuple:
    out = []
    for it in b.chunks[0]["items"]:
        o, t = it["facts"]["OWNER"], it["facts"]["TOPIC"]
        texts = []
        for _ in range(R.PER_ITEM):
            w = f"{adjs[k % len(adjs)]} {nouns[(k // len(adjs)) % len(nouns)]}"
            texts.append(f"Group chat about {t}, saved by {o} for the {w}.")
            k += 1
        out.append({"qid": it["qid"], "intros": texts})
    return out, k


def test_end_to_end_keeps_the_g3h_contract_and_bar(batches):
    pieces, probs = R.lint_answers(batches, _stand_in_answers(batches), seen=set())
    assert probs == [] and len(pieces) == R.PER_ITEM * len(_items(batches))
    assert {p["register"] for p in pieces if p["held_out"]} == set(R.HELD_REGS)
    assert all(p["ok"] for p in pieces), [p["problems"] for p in pieces if not p["ok"]][:3]
    gb = R.g3h_batch(pieces)
    assert gb.prompt == X.G3H_PROMPT
    for c in gb.chunks:
        assert c["answer_file"] == str(R.EXTRACT_ROOT / "answers" / f"{c['task_id']}.json")
        for it in c["items"]:
            assert [f["field"] for f in it["schema"]] == ["topic", "owner"]
    inv = chunker.item_by_internal(gb)
    by_pid = {p["iid"]: p for p in pieces}
    good = {c["task_id"]: [{"qid": it["qid"], "topic": by_pid[gb.key[it["qid"]]]["facts"]["TOPIC"],
                            "owner": by_pid[gb.key[it["qid"]]]["facts"]["OWNER"]} for it in c["items"]]
            for c in gb.chunks}
    out = R.score_reads(pieces, gb, good)
    assert out["answer_problems"] == [] and out["report"]["quarantined"] == []
    assert len(out["passed"]) == len(pieces) and len(inv) == len(pieces)
    # one owner read NONE in one register: that whole register (template = register in this round) is quarantined
    bad = json.loads(json.dumps(good))
    first = next(iter(bad))
    bad[first][0]["owner"] = "NONE"
    reg = by_pid[gb.key[bad[first][0]["qid"]]]["register"]
    out = R.score_reads(pieces, gb, bad)
    assert out["report"]["quarantined"] == [f"{R.ROUND}:{reg}"] and out["report"]["bar"] == g3h.PASS_RATE
    assert all(p["register"] != reg for p in out["passed"])


def test_dedup_against_earlier_templates(batches):
    ans = _stand_in_answers(batches)
    b0 = batches[0][1]
    first = ans[b0.chunks[0]["task_id"]][0]["intros"][0]
    it0 = b0.chunks[0]["items"][0]
    seen = {R._norm(R.to_template(first, it0["facts"]))}
    pieces, _ = R.lint_answers(batches, ans, seen=seen)
    assert sum(not p["ok"] for p in pieces) == 1
