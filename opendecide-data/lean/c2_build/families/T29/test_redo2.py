"""c2_build/families/T29/test_redo2.py: the T29 redo2 authoring tasks (redo2.py), built in memory (nothing is written).

Checks: gold-free chunks of <= 50 items with only the chunker's fields; no label word, option text, code word or
stand-in question string in any task file; every task file names its own answer path and holds the inline contract;
the redo2 briefs hold the fixes of the three pool blockers (no yn_permitted gloss on the yn_not_forbidden brief, closed
request vocabulary for Mode F, taken lists = the frozen forms, B15 / B20 meanings verbatim); planned outputs are about
3x each G0 deficit; the files on disk (if written) are the same bytes as the rebuild.
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T29/test_redo2.py
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import chunker  # noqa: E402
from families.T29 import authoring as A  # noqa: E402
from families.T29 import plugin as P  # noqa: E402
from families.T29 import redo2 as R  # noqa: E402


@pytest.fixture(scope="module")
def tasks():
    return R.build_tasks()


def _texts(tasks):
    return [(t, c, t.text(c)) for t in tasks for c in t.batch.chunks]


def test_chunks_are_small_gold_free_and_self_contained(tasks):
    assert R.check(tasks) == []
    ids = [c["task_id"] for t in tasks for c in t.batch.chunks]
    assert len(set(ids)) == len(ids)
    for t, c, text in _texts(tasks):
        assert 1 <= len(c["items"]) <= chunker.MAX_ITEMS
        assert str(t.answer_file(c["task_id"])) in text and "ANSWER CONTRACT" in text
        assert all(it["qid"] in text for it in c["items"])
        for it in c["items"]:
            assert set(it) - {"qid"} <= set(chunker.TASK_KINDS[t.kind])
        assert not any(i in text for i in t.batch.key.values())
        assert "/haiku/redo2/" in str(t.answer_file(c["task_id"]))


def test_label_words_reach_no_brief(tasks):
    for _t, _c, text in _texts(tasks):
        low = f" {text.lower()} ".replace("\n", " ")
        for w in P.T29Plugin.LABEL_WORDS:
            assert f" {w} " not in low, w
        for code in P.CODE_WORDS:
            assert code.lower() not in low


def test_b1_brief_drops_the_permitted_gloss(tasks):
    t = next(t for t in tasks if t.name == "word-notbarred")
    for it in t.batch.chunks[0]["items"]:
        m = it["brief"]["meaning"]
        assert "not barred" in m
        for bad in ("straight away", "confirm", "user", "allow"):
            assert bad not in m, bad
    assert R.NB_MEANING != A.Q_MEANING["yn_not_forbidden"]


def test_b2_closed_request_vocabulary_and_new_facts(tasks):
    t = next(t for t in tasks if t.name == "free-r2")
    assert R.REQUEST_WORDS in t.batch.prompt and R.AGENT_WORDS in t.batch.prompt
    items = [it for c in t.batch.chunks for it in c["items"]]
    assert len(items) == R.FREE_N and {it["register"] for it in items} == set(A.FREE_REGISTERS)
    assert all(it["facts"]["REQUESTER"] in A.FREE_NAMES and it["facts"]["REASON"] in A.REASON_SURFACES for it in items)
    assert all(it["brief"] in R.SITUATIONS_CLEAN for it in items)


def test_b3_lexicon_briefs_carry_the_g0_meanings_and_taken_lists(tasks):
    cmp = next(t for t in tasks if t.name == "lex-cmp-r2")
    v1 = {(sem, typ): m for sem, typ, m, _f in A.CMP_ITEMS}
    for it in cmp.batch.chunks[0]["items"]:
        assert it["meaning"] in {v1[("cmp.gt", "count")], v1[("cmp.ge", "count")]}       # B15 verbatim
        assert it["brief"]["taken"] == R.taken_texts("comparator", ("cmp.gt", "cmp.ge"))
    conf = next(t for t in tasks if t.name == "lex-conf-r2")
    for it in conf.batch.chunks[0]["items"]:
        assert it["meaning"] in set(A.CONF_MEANING.values())                             # B20 verbatim
        assert it["brief"]["taken"]


def test_planned_outputs_cover_about_3x_each_deficit(tasks):
    out = collections.Counter()
    for t in tasks:
        for c in t.batch.chunks:
            out[t.pool] += t.outputs(c)
    assert out["wordings"] >= 3 * (5 - 1)                 # yn_not_forbidden training: have 1, floor 5
    assert out["freeform"] >= 1.5 * (100 - 55)            # Mode F training: have 55, target 100
    assert out["attack"] >= 3 * (60 - 58)
    assert out["lexicon:comparator"] >= 3 * (60 - 53)
    assert out["lexicon:confirmation"] >= 3 * (60 - 53)


def test_files_on_disk_match_the_rebuild(tasks):
    files, _m = R.author_files(tasks)
    if not (R.ROOT / "TASKS.json").is_file():
        pytest.skip("redo2 author files not written yet")
    assert R.check_on_disk(R.ROOT, files) == []
