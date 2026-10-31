"""families/T24/test_authoring.py: the T24 Haiku authoring tasks, built in memory, and the lint-stage checkers.

Checks: <= 40 tasks, one chunk of <= 50 gold-free items each; no forbidden string (label word, outcome name, stand-in
question) in any task file; every task file names its own answer path; the planned outputs cover the G0 section 3
pools with room for G-SL / G-LEX losses; skins never get {D1} / {D2}; the program checkers accept the stand-ins and
the prompt examples and refuse broken pieces. The loader test writes only to pytest's tmp_path (outside the repo).

Run (from lean/):  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
                   c2_build/families/T24/test_authoring.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T24 import authoring as A  # noqa: E402
from families.T24 import fixtures as FX  # noqa: E402
from families.T24 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def tasks():
    return A.build_tasks()


def test_tasks_are_few_small_gold_free_and_name_their_answer_file(tasks):
    assert 1 <= len(tasks) <= A.MAX_TASKS
    assert A.check(tasks) == []
    ids = [t.task_id for t in tasks]
    assert len(set(ids)) == len(ids)
    for t in tasks:
        assert len(t.batch.chunks) == 1 and 1 <= len(t.chunk["items"]) <= chunker.MAX_ITEMS
        text = t.text()
        assert str(t.answer_file()) in text and t.answer_file().name == f"{t.task_id}.json"
        assert str(t.answer_file()).startswith(str(A.ROOT / "answers"))
        for it in t.chunk["items"]:
            assert set(it) - {"qid"} <= set(chunker.TASK_KINDS[t.kind])
        assert not any(i in text for i in t.batch.key.values())
        assert set(t.meta) == set(t.batch.key.values())


def test_no_label_word_option_or_question_reaches_a_brief(tasks):
    for t in tasks:
        low = " " + t.text().lower().replace("\n", " ") + " "
        if t.kind != "author_wording":                      # wordings ask about the outcome differing (their content)
            for w in P.MATERIAL_WORDS:
                assert f" {w} " not in low, (t.name, w)
        if t.kind != "author_pack":                         # a pack defines its own outcome names
            for o in A.OUTCOME_VOCAB:
                assert f" {o} " not in low, (t.name, o)
        for q in A.STANDIN_QUESTIONS:
            assert q.lower() not in low


def test_planned_outputs_cover_the_g0_pools(tasks):
    out = collections.Counter()
    for t in tasks:
        out[(t.pool, t.held_out)] += t.outputs
    regs = collections.Counter()
    for t in tasks:
        if t.pool == "skins":
            for it in t.chunk["items"]:
                regs[it["register"]] += A.SKINS_PER_ITEM
                assert set(it["slots"]) <= {"CUSTOMER", "CASE_ID", "CAT", "COND", "AMOUNT", "REQ"}   # never D1 / D2
                assert "CUSTOMER" in it["slots"]
                assert (it["register"] in P.T24Plugin.HELD_OUT_REGISTERS) == t.held_out
    assert set(regs) == set(P.T24Plugin.REGISTERS)
    assert all(regs[r] >= 40 for r in A.TRAIN_REGISTERS) and all(regs[r] >= 30 for r in A.HELD_REGISTERS)
    assert out[("freeform", False)] >= 100 and out[("freeform", True)] >= 24
    assert out[("packs", False)] >= 2 * 36                                            # 32 training + 4 held out, x2
    per_form = collections.Counter()
    held_form = collections.Counter()
    for t in tasks:
        if t.pool == "wordings":
            for iid, m in t.meta.items():
                (held_form if m["held_out"] else per_form)[m["qform"]] += A.WORDINGS_PER_ITEM
    target = {"ch_v2": 40, "yn_changes": 16, "yn_same": 8, "yn_not_change": 8, "yn_fail_change": 8, "yn_dneg": 6}
    for qf, n in target.items():                                                      # G0 3.3 targets, x2 for G-LEX
        assert per_form[qf] >= 2 * n, (qf, per_form[qf])
        assert held_form[qf] >= 8, qf
    assert sum(per_form.values()) >= 30
    per_sem = collections.Counter(m["sem"] for t in tasks if t.pool.startswith("lexicon:") for m in t.meta.values())
    assert set(per_sem) == {s for s, _, _ in FX.SEMS}
    assert all(n * A.FORMS_PER_ITEM >= 24 for n in per_sem.values())                 # >= 6 admitted, x4 for 3/3
    neg = [m for t in tasks for m in t.meta.values() if m.get("surface") == "negative"]
    assert {m["sem"] for m in neg} == {f"t24.amt.{op}" for op in P.OPS}               # "... do not qualify" forms


def test_checkers_accept_stand_ins_and_refuse_broken_pieces():
    for reg, (_fmt, ex) in A.REGISTER_FORMAT.items():
        assert A.check_skin(ex, reg, [p.name for p in K.placeholders(ex)]) == [], reg
    for sid, reg, _esc, held, text, decl in FX.SKINS:
        assert A.check_skin(text, reg, list(decl), held_out=held) == [], sid
    for wid, qf, text in FX.WORDINGS + FX.HELD_WORDINGS:
        assert A.check_wording(text, qf) == [], wid
    for sem, text in FX.CLAUSES:
        assert A.check_form(text, sem) == [], text
    dom, probs = A.check_pack({"title": "lost luggage policy", "prefix": "LUG",
                               "date_fields": ["flight date", "report date"], "money_field": "claimed value",
                               "categories": ["suitcases", "backpacks", "sports gear", "instruments"],
                               "conditions": ["tagged", "receipt kept", "photo only"],
                               "outcomes": ["full settlement", "partial settlement", "claim declined"]})
    assert probs == [] and dom.prefix == "LUG"
    assert A.check_skin("{CUSTOMER}: hi, my case {CASE_ID} is the same under the new rules.", "chat",
                        ["CUSTOMER", "CASE_ID"])
    assert A.check_skin("{CUSTOMER} will not wait for case {CASE_ID}.", "memo", ["CUSTOMER", "CASE_ID"])
    assert A.check_skin("Case note: {CUSTOMER} wrote on {D1}.", "memo", ["CUSTOMER"])
    assert A.check_wording("Isn't the outcome for this case different under the revised version?", "yn_changes")
    assert A.check_wording("Does the revised version fail to not alter the outcome for this case?", "yn_fail_change")
    assert A.check_form("The {M} must be at least {X}.", "t24.amt.ge")
    assert A.check_form("Requests are accepted within {N} of the {A}", "t24.ovc")
    assert A.check_freeform("Hi team, Dana Okafor here. Nothing is the same as before.", "Dana Okafor")
    assert A.check_pack({"title": "lost luggage rules"})[1]


def test_loader_maps_answers_back_to_internal_ids(tasks, tmp_path):
    out, manifest = A.files(tasks, root=tmp_path)
    for rel, text in out.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    t = next(t for t in tasks if t.name == "word-held")
    ans = [{"qid": it["qid"], "wordings": ["Under the revised version, which outcome does this case receive?"]}
           for it in t.chunk["items"]]
    Path(t.answer_file(tmp_path)).write_text(json.dumps(ans), encoding="utf-8")
    pools, probs = A.load(tmp_path)
    assert len(pools["wordings"]) == len(t.chunk["items"])
    assert {p["qform"] for p in pools["wordings"]} == set(P.T24Plugin.QFORMS)
    assert all(p["held_out"] and p["task_id"] == t.task_id for p in pools["wordings"])
    assert sum("no answer file" in x for x in probs) == len(tasks) - 1
