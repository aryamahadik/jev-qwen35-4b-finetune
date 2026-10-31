"""transfer/T19/test_redo2.py: in-memory tests of the T19 redo round 2 (redo2.py). Nothing here writes a file, and the
short texts below are test stand-ins (like fixtures.py), never answers to a task."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import gsl  # noqa: E402
from transfer.T19 import fixtures as FX  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import redo2 as R  # noqa: E402
import negcount  # noqa: E402


@pytest.fixture(scope="module")
def built():
    r1 = R.round1()
    return r1, R.build(r1)


def test_redo_items_equal_the_shortfalls(built):
    _r1, tasks = built
    man = json.loads((R.POOLS / "MANIFEST.json").read_text(encoding="utf-8"))
    want = {s["item"]: s["shortfall"] for s in man["shortfalls"]}
    assert R.index(tasks)["items_by_cell"] == want
    assert sum(t["n_items"] for t in tasks) == sum(want.values()) == 79
    for t in tasks:
        assert t["answer_file"] in t["text"] and t["answer_file"].startswith(str(R.ROOT / "answers"))
        assert t["allowed_read"] == [t["task_file"]] and t["allowed_write"] == [t["answer_file"]]
        assert len(t["qids"]) == len(set(t["qids"])) == t["n_items"]


def test_items_keep_round1_qids_and_facts(built):
    r1, tasks = built
    for t in tasks:
        b = r1[t["pool"]]["batch"]
        for q in t["qids"]:
            assert q in b.key                                  # round 1 key still maps it
        if t["pool"] == "freeform":
            items = json.loads(t["text"].split("```json\n", 1)[1].split("\n```", 1)[0])
            for it in items:
                assert it["facts"] == r1["freeform"]["items"][b.key[it["qid"]]]["facts"]


def test_no_label_word_or_question_text_in_authoring_tasks(built):
    _r1, tasks = built
    for t in tasks:
        low = t["text"].lower()
        for f in R.FORBID[t["pool"]]:
            assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low), (t["name"], f)
        assert "t19a." not in t["text"]


def test_on_is_reserved_in_the_three_prompts():
    for pool in ("skins", "freeform", "attacks"):
        text = R.instructions(pool)
        assert "the short word \"on\" as a word by itself" in text
        assert "on-premises" in text and "on behalf of" in text


def test_prompt_lists_cover_every_word_the_checks_refuse():
    shown = {p: set(re.findall(r"[a-z]+(?:-[a-z]+)*", R.NOTES[p].lower())) for p in R.NOTES}
    skin_set = R._cats(gsl.ALL_WORD_CATS) | HA.HINT_WORDS | R.PROFILE_WORDS
    free_set = (gsl.CORE["number"] | gsl.CORE["status"] | gsl.EXTENDED["status"] | gsl.CORE["modal"] | HA.HINT_WORDS
                | R.PROFILE_WORDS)
    attack_set = gsl.CORE["number"] | R.PROFILE_WORDS
    for pool, words in (("skins", skin_set), ("freeform", free_set), ("attacks", attack_set),
                        ("packs", R._cats(gsl.ALL_WORD_CATS))):
        missing = sorted(w for w in words if w not in R.LABEL_FORMS and w not in R.CLITIC_STEMS
                         and w not in shown[pool])
        assert not missing, (pool, missing)


def test_wording_briefs_pin_phrases_and_frames(built):
    _r1, tasks = built
    specs = [s for t in tasks for s in t["wording_briefs"].values()]
    assert len(specs) == 26
    pairs = [(s["qform"], s["phrase"], f) for s in specs for f in s["frames"]]
    assert len(pairs) == len(set(pairs))                         # R3: (phrase, frame) unique within a form
    for s in specs:
        assert s["phrase"] in {p for p, _ in R.PHRASES[s["qform"]]}
        for f in s["frames"]:
            assert f not in [f"{x}" for x in HA.STYLES]


@pytest.mark.parametrize("q,text,ok", [
    ("yn_out_of", "Is {SITE} out of compliance with its checklist on the audit date?", True),
    ("yn_out_of", "Does {SITE} fall short of its checklist on the audit date?", False),
    ("yn_out_of", "Is {SITE} non-compliant with its checklist on the audit date?", False),
    ("yn_not_compliant", "Is {SITE} not compliant with its checklist on the audit date?", True),
    ("yn_not_compliant", "Is {SITE} not in compliance with its checklist on the audit date?", True),
    ("yn_not_compliant", "Isn't {SITE} in compliance with its checklist on the audit date?", False),
    ("yn_not_compliant", "Does {SITE} not meet its checklist on the audit date?", False),
    ("yn_fails", "Does {SITE} fail to meet its checklist on the audit date?", True),
    ("yn_fails", "Do the records show that {SITE} fails to satisfy its checklist on the audit date?", True),
    ("yn_fails", "Does {SITE} fail to conform to its checklist on the audit date?", False),
    ("yn_fails", "Does {SITE} lack compliance with its checklist on the audit date?", False),
    ("yn_compliant", "Does {SITE} comply with its checklist on the audit date?", True),
    ("yn_compliant", "Is {SITE} in breach of its checklist on the audit date?", False),
])
def test_phrase_check(q, text, ok):
    assert (R.phrase_problems(q, text) == []) == ok


def test_key_phrases_meet_the_negation_counts():
    shapes = {"yn_out_of": "Is the site {p} its checklist on the audit date?",
              "yn_not_compliant": "Is the site {p} its checklist on the audit date?",
              "yn_fails": "Does the site {p} its checklist on the audit date?",
              "yn_compliant": "Does the site {p} its checklist on the audit date?"}
    for q, variants in R.PHRASES.items():
        for p, _rx in variants:
            text = shapes[q].format(p=p).replace("Does the site in compliance", "Is the site in compliance") \
                .replace("Does the site compliant", "Is the site compliant")
            c = negcount.count(text)
            assert (c.k_all, c.k_syn) == HA.NEG_EXACT[q], (q, p, text)


def test_lint_refuses_bare_on_and_hyphenated_profile_words(built):
    r1, _tasks = built
    iid = next(i for i, m in r1["skins"]["plan"].items() if m["register"] == "audit_memo" and not m["held_out"])
    meta = r1["skins"]["plan"][iid]
    bad, r = R.lint_candidate("skins", iid, meta, "Memo: {AUDITOR} reviews the records of {SITE} on behalf of the "
                                                 "team.", "t", "0" * 64, set())
    assert bad is None and any("['on']" in x for x in r)
    bad, r = R.lint_candidate("skins", iid, meta, "Memo: {AUDITOR} reviews the records of {SITE} for the "
                                                 "on-premises team.", "t", "0" * 64, set())
    assert bad is None and any("hyphenated" in x for x in r)
    good, r = R.lint_candidate("skins", iid, meta, "Memo: {AUDITOR} reviews the records of {SITE} for the team.",
                               "t", "0" * 64, set())
    assert good is not None and r == []


def test_round1_wordings_are_never_revoted(built):
    r1, _tasks = built
    seen = R.seen_wordings()
    rejected = json.loads((R.POOLS / "quarantine.json").read_text(encoding="utf-8"))["forms_not_admitted"]
    assert all(R._norm(f["text"]) in seen for f in rejected)
    f = rejected[0]
    iid = next(i for i, m in r1["wordings"]["plan"].items() if m["qform"] == f["qform"])
    obj, r = R.lint_candidate("wordings", iid, r1["wordings"]["plan"][iid], f["text"], "t", "0" * 64, seen)
    assert obj is None and any("duplicate" in x for x in r)


def test_select_keeps_the_first_passing_candidate(built):
    r1, tasks = built
    t = next(x for x in tasks if x["pool"] == "attacks")
    raw = [{"qid": t["qids"][0], "texts": ["Colleagues wait for {AUDITOR} and want to move on with a quick close.",
                                           "Colleagues wait for {AUDITOR} and want a quick close with a smile.",
                                           "x"]}]
    sel = R.select([t], r1, {t["name"]: raw})
    row = sel["items"][0]
    assert row["candidates"][0]["ok"] is False and row["kept"] == 1
    assert any("unanswered" in p for p in sel["problems"])
    counts, _short = R.merged_counts([row["cell"]])
    assert counts["attack"] == R.frozen_counts()["attack"] + 1


def test_glex_items_use_a_site_name():
    reg = FX.lexicon(admit=False)
    fids = sorted(reg.forms)
    items = R.glex_items(reg, fids, "t19-test")
    kit = dict(reg.lexicon_items(fids, seed="t19-test"))
    for fid, it in items:
        assert R.SAMPLE_SITE in it["text"] and "Dana Okafor" not in it["text"]
        assert it["choices"] == kit[fid]["choices"]


def test_extract_build_in_memory(built):
    r1, _tasks = built
    w_iid = next(i for i, m in r1["wordings"]["plan"].items() if m["qform"] == "yn_out_of")
    f_iid = sorted(r1["freeform"]["plan"])[0]
    text = "As the records stand, is {SITE} out of compliance with its checklist on the audit date?"
    sel = {"items": [
        {"pool": "wordings", "iid": w_iid, "candidates": [
            {"j": 0, "ok": True, "obj": ("yn_out_of", text, "T19-redo2-wordings-000", "0" * 64), "text": text}]},
        {"pool": "freeform", "iid": f_iid, "candidates": [{"j": 1, "ok": True, "text": "A short test note."}]}]}
    ex = R.extract_build(sel, r1)
    assert [g["extractor_id"] for g in ex["glex"]] == [e for _l, e, _s in R.GLEX_READS]
    for g in ex["glex"]:
        b = g["batch"]
        assert b.prompt == R.EX.PROMPT_LEX and len(b.key) == 1
        item = b.chunks[0]["items"][0]
        assert item["text"] == text.replace("{SITE}", R.SAMPLE_SITE)
        assert len(item["choices"]) == len(FX.QUESTION_MEANINGS)
    assert ex["g3h"]["batch"].prompt == R.EX.PROMPT_G3H
    assert list(ex["g3h_expected"].values()) == [{"auditor": r1["freeform"]["plan"][f_iid]["facts"]["AUDITOR"]}]
    for t in ex["tasks"]:
        assert t["answer_file"].startswith(str(R.XROOT / "answers")) and t["answer_file"] in ex["files"][
            t["task_file"][len(str(R.XROOT)) + 1:]]
    assert not ex["lex_drops"]
