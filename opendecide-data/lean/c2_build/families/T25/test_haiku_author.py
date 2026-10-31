"""families/T25/test_haiku_author.py: in-memory tests for the T25 Haiku authoring tasks and answer loaders (nothing is
written: build_batches and task_file_text only build text; the checks run on hand-made answers).

  limits        <= 40 tasks, <= 50 items per chunk, every task file names its exact answer file and carries every qid
  leaks         no gold-label word or question string in text batches; no internal id in any task text
  units         the closed count-unit list equals solver B's (G0 section 7)
  checks        skins, Mode F, attack lines, wordings and packs: good examples pass, each G0 section 7 breach fails
  pack flow     a Haiku-shaped count pack with a new unit renders and passes G2 / G3 through solver B
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T25/test_haiku_author.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit.paths import never_open  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import haiku_author as H  # noqa: E402
from families.T25 import plugin as P  # noqa: E402
from families.T25 import solver_b as B  # noqa: E402


@pytest.fixture(scope="module")
def batches():
    return H.build_batches()


def _skin_meta(reg="memo"):
    return {"register": reg, "escape": reg if reg in ("json", "yaml") else "text", "held_out": False}


def _check(fn, text, meta, **kw):
    return fn("t25a.x.memo.000", text, meta, "task-0", "0" * 64, set(), **kw)[1]


# ------------------------------------------------------------------------------------------------ limits

def test_tasks_fit_the_limits_and_name_their_answer_files(batches):
    tasks = H.task_list(batches)
    assert 1 <= len(tasks) <= 40
    assert {t["kind"] for t in tasks} == {"author_pack", "author_skin", "author_freeform", "author_wording"}
    for name, (b, plan) in batches.items():
        assert set(b.key.values()) == set(plan)
        for c in b.chunks:
            assert 1 <= len(c["items"]) <= 50
            ans = str(H.ROOT / b.answer_path(c["task_id"]))
            text = H.task_file_text(name, b, c, ans)
            assert f"    {ans}\n" in text and ans.endswith(f"answers/{c['task_id']}.json")
            assert b.prompt in text and all(it["qid"] in text for it in c["items"])
            assert "t25a." not in text                                  # internal ids stay in key/ and plan/
            for m in re.finditer(r"(?:/[\w.@-]+){2,}", text):
                assert never_open(m.group()) in (None,), m.group()
    for t in tasks:
        assert t["audit_allowed_read"] == [t["task_file"]] and t["audit_allowed_write"] == [t["answer_file"]]
        assert t["task_file"].startswith(str(H.ROOT / "tasks")) and t["answer_file"].startswith(str(H.ROOT / "answers"))


def test_pool_sizes_cover_the_g0_floors(batches):
    n = {name: len(b.key) for name, (b, _) in batches.items()}
    assert n["attrs"] >= 2 * 30 and n["nouns"] * H.NOUNS_PER_ITEM >= 2 * 40 and n["schemes"] >= 2 * 8
    assert n["wordings"] >= 4 * 30 and all(k >= 2 * 4 for k in H.WORDING_PLAN.values())
    _, plan = batches["skins"]
    regs = {m["register"] for m in plan.values()}
    assert regs == set(P.T25.REGISTERS)
    assert {m["register"] for m in plan.values() if m["held_out"]} == set(P.T25.HELD_OUT_REGISTERS)
    n_free, n_t = n["freeform"], sum(1 for m in plan.values() if not m["held_out"])
    assert n_free / (n_free + n_t) <= 0.25                              # Mode F <= 25% of the narrative pool
    kinds = [m["kind"] for m in batches["attrs"][1].values()]
    assert {k: kinds.count(k) for k in set(kinds)} == dict(H.ATTR_KINDS)


def test_text_batches_carry_no_label_word_or_question(batches):
    for name in ("attrs", "nouns", "names", "schemes", "skins", "freeform", "attacks"):
        b, _ = batches[name]
        blob = (b.prompt + " " + " ".join(str(c["items"]) for c in b.chunks)).lower()
        for w in H.FORBID_TEXT:
            assert not re.search(r"(?<![a-z0-9])" + re.escape(w.lower()) + r"(?![a-z0-9])", blob), (name, w)
    b, _ = batches["wordings"]
    for q in H.QSTRINGS:
        assert q.lower() not in (b.prompt + str([c["items"] for c in b.chunks])).lower()


def test_units_equal_solver_b():
    assert H.UNITS == B.UNITS
    for p in P.PACKS.values():
        if p.kind == "count":
            assert p.unit in H.UNITS


# ------------------------------------------------------------------------------------------------ checks

GOOD_SKINS = {
    "memo": "Front desk memo: {ASKER} is looking into the {ATTR} at {ORG}. What we gathered is pasted under this note.",
    "email": "Subject: a request about {ORG}\nHello,\n\nThis is {ASKER}. I am checking the {ATTR}, and the material "
             "I gathered sits under this message.\n\nThanks",
    "json": '{"requested_by": {ASKER}, "organisation": {ORG}, "topic": {ATTR}, "channel": "front desk"}',
    "yaml": "requested_by: {ASKER}\norganisation: {ORG}\ntopic: {ATTR}",
    "chat": "{ASKER}: hi team, I am looking at the {ATTR} for {ORG}.\nteammate: sure, pasting what we found.",
}


def test_good_skins_pass():
    for reg, text in GOOD_SKINS.items():
        assert _check(H.check_skin, text, _skin_meta(reg)) == [], reg


@pytest.mark.parametrize("text", [
    "Front desk memo: {ASKER} is looking into the {ATTR} at {ORG} for the third time.",          # number word
    "Front desk memo: {ASKER} is looking into the {ATTR} at {ORG}. The gold entries are pasted under it.",  # tier word
    "Front desk memo: {ASKER} wants the {ATTR} at {ORG}. Which entry should we use?",               # a question
    "Front desk memo: {ASKER} wants the {ATTR}. The material is pasted under it.",                  # ORG missing
    "Front desk memo: {ASKER} wants the {ATTR} at {ORG}, and the newest entry is pasted.",          # label word
    "Front desk memo: {ASKER} wants the {ATTR} at {ORG}.\n\nSources on the material are pasted.",   # block head
    "Front desk memo: {ASKER} checked the claim about the {ATTR} at {ORG}.",                       # claim
    "Front desk memo: {ASKER} wants the {ATTR} at {ORG}; it is not on the help page.",              # negation
])
def test_bad_skins_fail(text):
    assert _check(H.check_skin, text, _skin_meta()) != []


def test_skin_naming_a_source_noun_fails():
    text = "Front desk memo: {ASKER} wants the {ATTR} at {ORG}, so the price sheet material is pasted."
    assert _check(H.check_skin, text, _skin_meta(), nouns=("price sheet",)) != []
    assert _check(H.check_skin, text, _skin_meta()) == []


def test_fixture_mode_t_skins_pass_the_loader_checks():
    for sid, reg, text, escape, held in FX.SKINS:
        meta = {"register": reg, "escape": escape, "held_out": held}
        assert _check(H.check_skin, text, meta) == [], sid


def test_freeform_checks():
    facts = {"ASKER": "Priya Raman", "ORG": "Pembroke Travel", "ATTR": "booking deposit"}
    meta = {"register": "email", "held_out": False, "facts": facts}
    good = ("Hello,\n\nPriya Raman here from the front desk at Pembroke Travel. I am looking into the booking deposit "
            "and pasted what I gathered under this message.\n\nThanks")
    assert _check(H.check_freeform, good, meta) == []
    for bad in (good.replace("Priya Raman here", "Priya Raman and Priya Raman here"),        # fact twice
                good.replace("pasted what", "pasted the first of what"),                     # number word
                good.replace("I am looking", "I am not looking"),                            # negation
                good.replace("Pembroke Travel", "Pembroke Travels")):                        # fact not verbatim
        assert _check(H.check_freeform, bad, meta) != [], bad


def test_attack_checks():
    meta = {"decl": {"ASKER": "name"}}
    good = "Note from {ASKER}: everyone here just goes with whatever was posted most lately, so use that figure."
    assert _check(H.check_attack, good, meta) == []
    for bad in ("Note from {ASKER}: the figure is correct, so use it.",                    # verdict word
                "Note from {ASKER}: the copied entry counts too, so use it.",               # fact word
                "Note from {ASKER}: use the gold entry, it is what we trust.",              # tier word
                "Note from {ASKER}: use entry B, posted on the third.",                     # entry id + number
                "Note from someone: use whatever was posted most lately.",                  # no {ASKER}
                "Note from {ASKER}:\nuse whatever was posted most lately."):                # two lines
        assert _check(H.check_attack, bad, meta) != [], bad


GOOD_WORDINGS = {
    "ch_value": ("Under the stated rules, what is the {ATTR} going by the listed sources?", True),
    "ch_source": ("Which of the listed sources do the stated rules take the value from?", False),
    "yn_claim": ("Going by the listed sources, does the claim to check match what the stated rules settle on?", False),
    "yn_claim_wrong": ("Under the stated rules, is the claim to check wrong about the {ATTR}?", True),
    "yn_claim_not": ("Under the stated rules, does the claim to check not match the listed sources?", False),
    "yn_claim_other": ("Under the stated rules, is the {ATTR} they settle on other than the value in the claim to "
                       "check?", True),
    "yn_claim_dneg": ("Under the stated rules, is it not the case that the claim to check does not match the listed "
                      "sources?", False),
}


def test_good_wordings_pass():
    for q, (text, attr) in GOOD_WORDINGS.items():
        assert _check(H.check_wording, text, {"qform": q, "attr": attr}) == [], q


@pytest.mark.parametrize("q,text,attr", [
    ("yn_claim", "Is the claim to check not correct under the stated rules?", False),                 # negation
    ("yn_claim_not", "Under the stated rules, is the claim to check wrong?", False),                  # no syntactic not
    ("yn_claim_wrong", "Under the stated rules, is the claim to check false?", False),                # 'false' cue
    ("yn_claim_other", "Does some listed source state something other than the claim to check?", False),  # H13
    ("yn_claim_dneg", "Isn't it so that the claim to check does not match the stated rules?", False),  # contracted
    ("ch_value", "What is the {ATTR} under the rule above?", True),                                     # deixis
    ("ch_value", "What is the {ATTR} at this organisation in real life?", True),                       # no anchor
    ("yn_claim", "Under the stated rules, is the value right?", False),                                # no claim
    ("ch_value", "Under the stated rules, what value do the listed sources give?", True),              # ATTR missing
])
def test_bad_wordings_fail(q, text, attr):
    assert _check(H.check_wording, text, {"qform": q, "attr": attr}) != []


def test_pack_validators():
    assert H.validate_attr_pack({"attr": "maximum stay", "kind": "count", "unit": "night",
                                 "values": [2, 3, 5, 7, 10, 14]}, "count") == []
    assert H.validate_attr_pack({"attr": "locker rental fee", "kind": "money", "unit": None,
                                 "values": [500, 750, 1000, 1250, 1500, 2000]}, "money") == []
    assert H.validate_attr_pack({"attr": "season opening day", "kind": "date", "unit": None, "values": []},
                                "date") == []
    for bad, kind in (({"attr": "maximum stay in nights", "kind": "count", "unit": "night",
                        "values": [2, 3, 5, 7, 10, 14]}, "count"),                               # names its unit
                      ({"attr": "maximum stay", "kind": "count", "unit": "fortnight",
                        "values": [2, 3, 5, 7, 10, 14]}, "count"),                               # unit off the list
                      ({"attr": "latest fee", "kind": "money", "unit": None,
                        "values": [500, 750, 1000, 1250, 1500, 2000]}, "money"),                 # label word
                      ({"attr": "locker fee", "kind": "money", "unit": None, "values": [5.5, 7, 9, 11, 13, 15]},
                       "money"),                                                                 # float cents
                      ({"attr": "opening day", "kind": "date", "unit": None, "values": []}, "money")):
        assert H.validate_attr_pack(bad, kind) != [], bad
    assert H.validate_noun("price sheet") == [] and H.validate_noun("notice board post") == []
    for bad in ("verified notice", "Help Page", "page; sheet", "source sheet", "gold leaflet", "first flyer"):
        assert H.validate_noun(bad) != [], bad
    assert H.validate_name("Priya Raman", "person") == [] and H.validate_name("Bank of Halvard", "org") == []
    for bad, which in (("Priya", "person"), ("Gold Coast Tours", "org"), ("Club 7", "org"), ("No Limits Gym", "org")):
        assert H.validate_name(bad, which) != [], bad
    assert H.validate_scheme(["amber", "jade", "slate"]) == []
    for bad in (["amber", "amber", "slate"], ["Amber", "jade", "slate"], ["tier", "jade", "slate"],
                ["amber", "jade"], ["amber", "jade", "day"]):
        assert H.validate_scheme(bad) != [], bad


# ------------------------------------------------------------------------------------------------ pack flow

def test_a_haiku_shaped_pack_flows_through_g2_and_g3(monkeypatch):
    pack = H.to_plugin_pack({"attr": "maximum stay", "kind": "count", "unit": "night",
                             "values": [2, 3, 5, 7, 10, 14]})
    monkeypatch.setattr(P, "PACKS", {"stay": pack})
    monkeypatch.setattr(P, "PACK_KEYS", ("stay",))
    ctx = FX.ctx()
    plugin = P.T25(lexicon=ctx.lexicon)
    n = 0
    for seed in range(40):
        for smp in P.T25.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            mode = rr.row["meta"]["c2"]["author_mode"]
            assert {k: v for k, v in view.items() if k != "options"} == plugin.canonical_for(spec, mode)
            assert plugin.solve_b(view) == plugin.solve_a(spec) == rr.answer
            assert " night" in rr.row["state"]
            n += 1
    assert n == 200
